"""Plan Composer — Agent 2.

Phase 3a: real Sonnet 4.6 call against composer_prompt.md.

Each PlanComposer.run() takes one Concept + the persona's IntakeState +
top-N relevant candidates, asks the LLM to produce a TripPlan as markdown
with an inline `<!-- PLAN_META {...} -->` sidecar at the end. The wrapper
parses the sidecar to populate the structured PlanResult fields, strips
it from the user-facing markdown, and returns the result.

Phase 3b will call this 2-3 times in parallel for diversity.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from agent.state import IntakeState, serialize_for_composer
from agent.types import (
    Concept,
    PlaceCandidate,
    PlanResult,
    ThemeAnchor,
)

logger = logging.getLogger(__name__)

# Path to the composer prompt — symlinked from poc-demo/composer_prompt.md.
_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "composer.md"

# Max candidates to surface to the Composer per call. Anchors are included
# first, then top-fit_score fillers up to this cap. Keeps prompts tractable
# and steers the LLM toward the right pool.
_CANDIDATE_CAP = 8

# Model + token budgets. Pre-Decision #2 picked Sonnet 4.6 for Composer.
_MODEL = "claude-sonnet-4-5"  # current alias for Sonnet 4.x; framework remaps
_MAX_TOKENS = 4096

# Regex for fallback metadata extraction when the LLM forgets the sidecar.
_DAY_THEME_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_PITCH_RE = re.compile(r"^>\s+\*\*一句话\s*pitch\*\*[:：]\s*(.+?)\s*$", re.MULTILINE)
_STOP_HEADER_RE = re.compile(r"^##\s+(\d{1,2}[:：]\d{2})\s*[·.]\s*(.+?)\s*$", re.MULTILINE)
_SIDECAR_RE = re.compile(r"<!--\s*PLAN_META\s*(\{.*?\})\s*-->", re.DOTALL)


class PlanComposer:
    """Composes one TripPlan from one Concept + candidate pool + IntakeState.

    Constructor args:
        anthropic_client: AsyncAnthropic instance (or compatible test fake).
                          If None, run() falls back to Phase 0 stub output
                          (useful for tests that don't want LLM calls and
                          for --mock-intake demos without an API key).
        candidate_cap:    max candidates to pass to the LLM (default 8).
    """

    def __init__(
        self,
        anthropic_client: Any = None,
        candidate_cap: int = _CANDIDATE_CAP,
    ) -> None:
        self.anthropic_client = anthropic_client
        self.candidate_cap = candidate_cap
        self._prompt: str = ""

    def _load_prompt(self) -> str:
        if not self._prompt:
            self._prompt = _PROMPT_PATH.read_text(encoding="utf-8")
        return self._prompt

    def _select_candidates(
        self, concept: Concept, candidates: list[PlaceCandidate]
    ) -> list[PlaceCandidate]:
        """Anchors first, then fill with top-fit_score up to the cap."""
        by_id = {c.place_id: c for c in candidates}
        ordered: list[PlaceCandidate] = []
        seen: set[str] = set()
        for anchor_id in concept.anchor_place_ids:
            if anchor_id in by_id and anchor_id not in seen:
                ordered.append(by_id[anchor_id])
                seen.add(anchor_id)
        remaining = sorted(
            (c for c in candidates if c.place_id not in seen),
            key=lambda c: c.fit_score,
            reverse=True,
        )
        for c in remaining:
            if len(ordered) >= self.candidate_cap:
                break
            ordered.append(c)
        return ordered

    def _build_user_message(
        self,
        concept: Concept,
        candidates: list[PlaceCandidate],
        intake_state: IntakeState,
    ) -> str:
        """Build the JSON-shaped user message the composer prompt expects."""
        composer_input = serialize_for_composer(intake_state)
        selected = self._select_candidates(concept, candidates)

        payload = {
            "concept": concept.model_dump(mode="json"),
            "intake_state": composer_input.model_dump(mode="json"),
            "place_candidates": [c.model_dump(mode="json") for c in selected],
        }
        instruction = (
            "Compose ONE TripPlan following the system prompt's template "
            "EXACTLY. Use `## {day_theme}` (NOT `#`) as the top heading per "
            "Caller context. After the markdown plan, on a final line, emit:\n"
            "<!-- PLAN_META {json} -->\n"
            "where {json} is a single-line JSON object with these keys:\n"
            "  day_theme (str), pitch (str — the 一句话 pitch),\n"
            "  theme_anchor (str — one of the 4 ThemeAnchor enum values),\n"
            "  mood_tags (list[str]), emotional_arc (list[str] of 4 pacing labels),\n"
            "  stop_place_ids (list[str] of length 4; each MUST be a place_id from "
            "place_candidates above, NOT a free-text name),\n"
            "  stop_names (list[str] of length 4 — matching display names),\n"
            "  adaptive_branches (list of {condition, alternative}),\n"
            "  composer_note (str — empty unless you used the 'name the gap' rule).\n"
            "The PLAN_META line is mandatory."
        )

        return f"{instruction}\n\nINPUT:\n```json\n{json.dumps(payload, ensure_ascii=False)}\n```"

    async def _call_llm(self, user_message: str) -> str:
        """Single call; caller handles retry. Returns raw response text."""
        if self.anthropic_client is None:
            raise RuntimeError("PlanComposer has no anthropic_client (stub mode active)")
        response = await self.anthropic_client.messages.create(
            model=_MODEL,
            max_tokens=_MAX_TOKENS,
            system=self._load_prompt(),
            messages=[{"role": "user", "content": user_message}],
        )
        # AsyncAnthropic returns Message; content[0] is the TextBlock.
        content = response.content
        if not content:
            return ""
        first = content[0]
        text = getattr(first, "text", None)
        if text is None and isinstance(first, dict):
            text = first.get("text", "")
        return text or ""

    def _parse_sidecar(self, raw: str) -> tuple[str, dict[str, Any], bool]:
        """Strip the PLAN_META comment from markdown.

        Returns (clean_md, meta, had_sidecar_attempt).
        - had_sidecar_attempt=True means the comment was found, regardless of
          whether JSON parsed (caller uses this to decide retry vs fallback).
        """
        match = _SIDECAR_RE.search(raw)
        if not match:
            return raw.strip(), {}, False
        try:
            meta = json.loads(match.group(1))
        except json.JSONDecodeError as exc:
            logger.warning("PLAN_META JSON parse failed: %s", exc)
            meta = {}
        cleaned = (raw[: match.start()] + raw[match.end() :]).strip()
        return cleaned, meta, True

    def _fallback_extract(
        self, markdown: str, candidates: list[PlaceCandidate]
    ) -> dict[str, Any]:
        """Regex extract when sidecar is missing or malformed.

        Pulls day_theme from the first `##` line, pitch from `> **一句话 pitch**:`,
        stop_names from `## HH:MM · Name` lines, then back-fills stop_place_ids
        by name lookup against the provided candidate pool.
        """
        meta: dict[str, Any] = {}
        if dt := _DAY_THEME_RE.search(markdown):
            meta["day_theme"] = dt.group(1).strip()
        if p := _PITCH_RE.search(markdown):
            meta["pitch"] = p.group(1).strip()
        stops = _STOP_HEADER_RE.findall(markdown)
        if stops:
            meta["stop_names"] = [name.strip() for _, name in stops]
            # Best-effort lookup by exact-or-substring match.
            ids: list[str] = []
            by_name_lower = {c.name.lower(): c.place_id for c in candidates}
            for _, name in stops:
                key = name.strip().lower()
                if key in by_name_lower:
                    ids.append(by_name_lower[key])
                else:
                    # Try substring match against place names.
                    hit = next(
                        (
                            c.place_id
                            for c in candidates
                            if key in c.name.lower() or c.name.lower() in key
                        ),
                        "",
                    )
                    ids.append(hit)
            meta["stop_place_ids"] = ids
        return meta

    def _stub_result(self, concept: Concept, candidates: list[PlaceCandidate]) -> PlanResult:
        """Phase 0-style fallback used when no anthropic_client is provided.

        Lets `--mock-intake` smoke tests + CI run without burning tokens.
        """
        stop_ids = (concept.anchor_place_ids + [c.place_id for c in candidates])[:4]
        while len(stop_ids) < 4:
            stop_ids.append(f"stub_stop_{len(stop_ids)}")
        markdown = (
            f"## {concept.day_theme}\n\n"
            f"> **一句话 pitch**: {concept.emotional_thesis}\n\n"
            f"### 10:00 · {stop_ids[0]}\n*stub mode — no LLM available*\n\n"
            f"### 12:30 · {stop_ids[1]}\n*stub mode*\n\n"
            f"### 15:00 · {stop_ids[2]}\n*stub mode*\n\n"
            f"### 17:30 · {stop_ids[3]}\n*stub mode*\n"
        )
        return PlanResult(
            markdown=markdown,
            day_theme=concept.day_theme,
            pitch=concept.emotional_thesis,
            theme_anchor=concept.theme_anchor,
            stop_place_ids=stop_ids,
            raw_metadata={"stub": True},
        )

    async def run(
        self,
        concept: Concept,
        candidates: list[PlaceCandidate],
        intake_state: IntakeState,
    ) -> PlanResult:
        """Compose one TripPlan. Returns PlanResult with markdown + metadata."""
        if self.anthropic_client is None:
            return self._stub_result(concept, candidates)

        user_message = self._build_user_message(concept, candidates, intake_state)
        selected = self._select_candidates(concept, candidates)

        # First attempt
        raw = await self._call_llm(user_message)
        cleaned, meta, had_sidecar = self._parse_sidecar(raw)

        # Retry once if:
        #   (a) sidecar was attempted but parsed empty (LLM had a JSON typo), OR
        #   (b) no sidecar AND no usable markdown header (LLM produced garbage)
        needs_retry = (had_sidecar and not meta) or (
            not had_sidecar and not _DAY_THEME_RE.search(cleaned)
        )
        if needs_retry:
            logger.warning("Composer response unusable; retrying once")
            retry_msg = user_message + (
                "\n\nIMPORTANT: Your previous response was missing the required "
                "`<!-- PLAN_META {...} -->` line (or its JSON was malformed). "
                "Re-emit, strictly following the template, with valid JSON in PLAN_META."
            )
            raw = await self._call_llm(retry_msg)
            cleaned, meta, had_sidecar = self._parse_sidecar(raw)

        # Fallback: regex-extract from markdown if sidecar still empty
        if not meta:
            meta = self._fallback_extract(cleaned, selected)

        # Build the PlanResult
        theme_anchor_raw = meta.get("theme_anchor") or concept.theme_anchor.value
        try:
            theme_anchor = ThemeAnchor(theme_anchor_raw)
        except ValueError:
            theme_anchor = concept.theme_anchor

        return PlanResult(
            markdown=cleaned or self._stub_result(concept, selected).markdown,
            day_theme=meta.get("day_theme") or concept.day_theme,
            pitch=meta.get("pitch") or concept.emotional_thesis,
            theme_anchor=theme_anchor,
            mood_tags=meta.get("mood_tags") or [],
            emotional_arc=meta.get("emotional_arc") or list(concept.pacing_blueprint),
            stop_place_ids=meta.get("stop_place_ids") or [],
            stop_names=meta.get("stop_names") or [],
            adaptive_branches=meta.get("adaptive_branches") or [],
            composer_note=meta.get("composer_note") or "",
            raw_metadata=meta,
        )


__all__ = ["PlanComposer"]
