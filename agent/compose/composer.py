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
    Logistics,
    OrderRecs,
    PlaceCandidate,
    PlanResult,
    Stop,
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
# Bumped from 4096 → 8192 because the PLAN_META sidecar now carries a full
# `stops` array (one_liner + why_fits_today + logistics + order_recs for
# 4 stops). Real Garry runs hit the old cap mid-sidecar and the JSON parser
# silently dropped stops to []. 8192 leaves ~3500 tokens of headroom.
_MAX_TOKENS = 16384  # BLOCKER FIX: 8192 truncated Chinese-heavy plans mid-PLAN_META → empty stops[]

# Regex for fallback metadata extraction when the LLM forgets the sidecar.
_DAY_THEME_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_PITCH_RE = re.compile(r"^>\s+\*\*一句话\s*pitch\*\*[:：]\s*(.+?)\s*$", re.MULTILINE)
_STOP_HEADER_RE = re.compile(r"^##\s+(\d{1,2}[:：]\d{2})\s*[·.]\s*(.+?)\s*$", re.MULTILINE)
# Sidecar matches `<!-- PLAN_META { … } -->`. We capture the full body
# between the `PLAN_META` token and the closing `-->` so nested objects
# inside the JSON (logistics, order_recommendations, …) don't trick a
# non-greedy `{.*?}` into truncating at the first inner `}`. `_extract_meta_json`
# below scans for the matching outer brace.
_SIDECAR_RE = re.compile(r"<!--\s*PLAN_META\s*(\{.*?)-->", re.DOTALL)


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
            "  composer_note (str — empty unless you used the 'name the gap' rule),\n"
            "  stops (list of length 4 — structured per-stop payload that mirrors "
            "what you wrote in the markdown body so the frontend doesn't have to "
            "re-parse). Each element MUST be:\n"
            "    {\n"
            "      \"stop_index\": 0..3,\n"
            "      \"time\": \"HH:MM\",\n"
            "      \"place_id\": \"<must be from place_candidates>\",\n"
            "      \"place_name\": \"<display name>\",\n"
            "      \"one_liner\": \"<the > sensory quote line for this stop>\",\n"
            "      \"why_fits_today\": \"<full Why this fits today paragraph>\",\n"
            "      \"logistics\": {\n"
            "        \"raw\": \"<full Logistics line(s) exactly as written>\",\n"
            "        \"drive_time_min\": <int or null>,\n"
            "        \"parking\": \"<short note or null>\",\n"
            "        \"kid_friendly\": <bool or null>,\n"
            "        \"reservation_note\": \"<text or null>\",\n"
            "        \"booking_links\": [{\"label\": \"...\", \"url\": \"...\"}],\n"
            "        \"transit_estimate_usd\": <number or null>\n"
            "      },\n"
            "      \"order_recommendations\": null  // OR for restaurants: "
            "{\"menu_listed\": [...], \"bold_picks\": [...], \"logic_text\": "
            "\"<the ordering reasoning paragraph with **bold** dishes>\"},\n"
            "      \"tip\": \"<insider tip or null>\",\n"
            "      \"transition_to_next\": \"<qualitative phrase or null for last "
            "stop>\",\n"
            "      \"transition_drive_min\": <int or null>\n"
            "    }\n"
            "The PLAN_META line is mandatory and stops MUST be length 4 "
            "matching the 4 markdown stops in the same order."
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
        body = match.group(1).strip()
        json_str = self._balanced_json_slice(body)
        try:
            meta = json.loads(json_str)
        except json.JSONDecodeError as exc:
            # BLOCKER FIX: silently empty meta hid LLM token-truncation bugs.
            # Loud warning so devs see the truncation in stderr immediately.
            logger.warning(
                "PLAN_META JSON parse failed (likely token truncation — bump "
                "_MAX_TOKENS or trim prompt): %s; raw_len=%d, sidecar_excerpt=%r",
                exc,
                len(raw),
                json_str[:200],
            )
            meta = {}
        cleaned = (raw[: match.start()] + raw[match.end() :]).strip()
        return cleaned, meta, True

    @staticmethod
    def _balanced_json_slice(body: str) -> str:
        """Scan `body` (which starts with `{`) and return the substring that
        ends at the matching outer `}`. String-literal aware so quoted braces
        inside values don't throw off the depth counter. Handles the nested
        logistics / order_recs objects the new `stops` sidecar carries.

        Falls back to the original body when unbalanced so the JSONDecodeError
        the caller raises stays informative.
        """
        depth = 0
        in_str = False
        esc = False
        for i, ch in enumerate(body):
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return body[: i + 1]
        return body

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

    def _extract_stops_from_markdown(
        self, markdown: str, candidates: list[PlaceCandidate]
    ) -> list[Stop]:
        """Best-effort: parse the 4 stop blocks out of the user-facing markdown.

        Used when the PLAN_META `stops` array is missing or its JSON failed
        to parse (the LLM occasionally emits unescaped quotes inside
        why_fits_today strings). The markdown body has all the same info in
        a more forgiving format, so we can reconstruct enough for the
        frontend renderer.

        Per-stop block shape (from composer_prompt.md template):

            ## HH:MM · Place Name

            > one_liner

            **Why this fits today**
            <paragraph>

            **Logistics**
            <line(s)>

            **Order**   ← restaurants only
            Menu: <items>
            **Your picks**: <prose with **bold** dishes>

            💡 *<tip>*

            *(transition: <phrase> · ~Nmin <drive|walk>)*

        Returns 4 Stops (or however many it found) — fields it can't
        confidently extract are left as their defaults.
        """
        by_name_lower = {c.name.lower(): c.place_id for c in candidates}

        # Match each stop block: `## HH:MM · Name` up to the next stop header
        # or the adaptive-branch section.
        block_re = re.compile(
            r"^##\s+(\d{1,2}[:：]\d{2})\s*[·.]\s*(.+?)\n(.*?)(?=^##\s+\d{1,2}[:：]\d{2}|^##\s+🔀|\Z)",
            re.MULTILINE | re.DOTALL,
        )
        one_liner_re = re.compile(r"^>\s+(.+?)$", re.MULTILINE)
        why_re = re.compile(
            r"\*\*Why this fits today\*\*\s*\n(.+?)(?=\n\s*\*\*|\n\s*💡|\n\s*\*\(transition|\Z)",
            re.DOTALL,
        )
        logistics_re = re.compile(
            r"\*\*Logistics\*\*\s*\n(.+?)(?=\n\s*\*\*|\n\s*💡|\n\s*\*\(transition|\Z)",
            re.DOTALL,
        )
        order_block_re = re.compile(
            r"\*\*Order\*\*\s*\n(.+?)(?=\n\s*\*\*Logistics|\n\s*💡|\n\s*\*\(transition|\Z)",
            re.DOTALL,
        )
        menu_line_re = re.compile(r"^Menu:\s*(.+?)$", re.MULTILINE)
        picks_re = re.compile(r"\*\*Your picks\*\*[:：]\s*(.+)", re.DOTALL)
        bold_re = re.compile(r"\*\*(.+?)\*\*")
        tip_re = re.compile(r"^💡\s*\*(.+?)\*\s*$", re.MULTILINE)
        transition_re = re.compile(
            r"\*\(transition:\s*(.+?)\s*·\s*~?(\d+)\s*min", re.IGNORECASE
        )
        drive_time_re = re.compile(r"🚗\s*~?(\d+)\s*min", re.IGNORECASE)
        kid_friendly_re = re.compile(r"👶")
        booking_re = re.compile(r"🔗[^:：]*[:：]?\s*(https?://\S+)")
        url_re = re.compile(r"(https?://\S+)")

        stops: list[Stop] = []
        for idx, (time, name, body) in enumerate(block_re.findall(markdown)):
            name = name.strip()
            # Place_id lookup against the candidate pool
            key = name.lower()
            place_id = by_name_lower.get(key, "")
            if not place_id:
                place_id = next(
                    (
                        c.place_id
                        for c in candidates
                        if key in c.name.lower() or c.name.lower() in key
                    ),
                    "",
                )

            one_liner = ""
            if m := one_liner_re.search(body):
                one_liner = m.group(1).strip()

            why = ""
            if m := why_re.search(body):
                why = m.group(1).strip()

            logistics_raw = ""
            if m := logistics_re.search(body):
                logistics_raw = m.group(1).strip()

            drive_min: int | None = None
            if m := drive_time_re.search(logistics_raw):
                drive_min = int(m.group(1))
            kid_friendly: bool | None = None
            if kid_friendly_re.search(logistics_raw):
                kid_friendly = True

            booking_urls: list[str] = []
            for m in booking_re.finditer(logistics_raw):
                booking_urls.append(m.group(1).rstrip(".,);"))
            if not booking_urls:
                # Pick up any bare URL in logistics block as a fallback
                booking_urls = [u.rstrip(".,);") for u in url_re.findall(logistics_raw)]

            logistics = Logistics(
                raw=logistics_raw,
                drive_time_min=drive_min,
                kid_friendly=kid_friendly,
                booking_links=[
                    {"label": "book", "url": u} for u in booking_urls
                ],  # pydantic coerces dicts → BookingLink
            )

            order_recs: OrderRecs | None = None
            if om := order_block_re.search(body):
                order_body = om.group(1).strip()
                menu_items: list[str] = []
                if mm := menu_line_re.search(order_body):
                    raw_menu = mm.group(1)
                    menu_items = [
                        item.strip() for item in re.split(r"\s*·\s*", raw_menu) if item.strip()
                    ]
                logic_text = ""
                bold_picks: list[str] = []
                if pm := picks_re.search(order_body):
                    logic_text = pm.group(1).strip()
                    bold_picks = [m.group(1).strip() for m in bold_re.finditer(logic_text)]
                # Dedupe & restrict bold_picks to menu items when possible
                if menu_items and bold_picks:
                    menu_lower = [m.lower() for m in menu_items]
                    bold_picks = [
                        bp
                        for bp in dict.fromkeys(bold_picks)
                        if any(bp.lower() in ml or ml in bp.lower() for ml in menu_lower)
                    ]
                order_recs = OrderRecs(
                    menu_listed=menu_items,
                    bold_picks=bold_picks,
                    logic_text=logic_text,
                )

            tip: str | None = None
            if m := tip_re.search(body):
                tip = m.group(1).strip()

            transition_to_next: str | None = None
            transition_drive_min: int | None = None
            if m := transition_re.search(body):
                transition_to_next = m.group(1).strip()
                transition_drive_min = int(m.group(2))

            stops.append(
                Stop(
                    stop_index=idx,
                    time=time.replace("：", ":").strip(),
                    place_id=place_id,
                    place_name=name,
                    one_liner=one_liner,
                    why_fits_today=why,
                    logistics=logistics,
                    order_recommendations=order_recs,
                    tip=tip,
                    transition_to_next=transition_to_next,
                    transition_drive_min=transition_drive_min,
                )
            )
            if len(stops) == 4:
                break

        return stops

    @staticmethod
    def _extract_mood_tags_from_markdown(markdown: str) -> list[str]:
        """Pull the `**Mood**: a · b · c` line if PLAN_META didn't carry mood_tags."""
        m = re.search(r"^\*\*Mood\*\*[:：]\s*(.+?)$", markdown, re.MULTILINE)
        if not m:
            return []
        return [t.strip() for t in re.split(r"\s*·\s*", m.group(1)) if t.strip()]

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

        stops = self._coerce_stops(meta.get("stops") or [])
        # Markdown-based fallback for `stops`: triggered when the sidecar
        # JSON failed to parse (or omitted stops) but the markdown body
        # still has the 4 stop blocks. This keeps the frontend renderable
        # even when the LLM emits unescaped quotes inside why_fits_today
        # strings.
        if not stops and cleaned:
            stops = self._extract_stops_from_markdown(cleaned, selected)

        mood_tags = meta.get("mood_tags") or []
        if not mood_tags and cleaned:
            mood_tags = self._extract_mood_tags_from_markdown(cleaned)

        # Back-fill stop_place_ids / stop_names from the recovered stops if
        # the sidecar didn't carry them.
        stop_place_ids = meta.get("stop_place_ids") or []
        stop_names = meta.get("stop_names") or []
        if not stop_place_ids and stops:
            stop_place_ids = [s.place_id for s in stops if s.place_id]
        if not stop_names and stops:
            stop_names = [s.place_name for s in stops if s.place_name]

        return PlanResult(
            markdown=cleaned or self._stub_result(concept, selected).markdown,
            day_theme=meta.get("day_theme") or concept.day_theme,
            pitch=meta.get("pitch") or concept.emotional_thesis,
            theme_anchor=theme_anchor,
            mood_tags=mood_tags,
            emotional_arc=meta.get("emotional_arc") or list(concept.pacing_blueprint),
            stop_place_ids=stop_place_ids,
            stop_names=stop_names,
            stops=stops,
            adaptive_branches=meta.get("adaptive_branches") or [],
            composer_note=meta.get("composer_note") or "",
            raw_metadata=meta,
        )

    @staticmethod
    def _coerce_stops(raw_stops: list[Any]) -> list[Stop]:
        """Convert raw sidecar `stops` entries into typed Stop models.

        Tolerant of partial data: if the LLM forgets a field we let Pydantic's
        defaults (mostly empty strings / None) take over rather than blow up.
        Backfills `stop_index` from list position when the LLM omits it.
        """
        out: list[Stop] = []
        for i, item in enumerate(raw_stops):
            if not isinstance(item, dict):
                continue
            if "stop_index" not in item:
                item = {**item, "stop_index": i}
            try:
                out.append(Stop.model_validate(item))
            except Exception as exc:  # pragma: no cover - defensive logging path
                logger.warning("Stop sidecar entry %s failed validation: %s", i, exc)
        return out


__all__ = ["PlanComposer"]
