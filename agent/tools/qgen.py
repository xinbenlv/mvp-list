"""generate_question — Sonnet 4.6 info-gain Q-Gen (Phase 1b).

Implements the 5-step Q-Generator algorithm from PRD §4 / eng-design §6:

  1. (Router already picked the target slot — we never re-decide here.)
  2. Enumerate 5–8 candidate questions for that slot.
  3. Score each by predicted info-gain.
  4. Pick top-1.
  5. Wrap in MI/OARS reflective-listening style.

Step 2–4 happen *inside the LLM call* (the prompt instructs Sonnet to do all
five steps internally and return only the final question string). We do not
expose intermediate candidates — that would require a separate LLM call per
candidate, doubling latency for no quality lift.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Protocol

from agent.state import IntakeState

logger = logging.getLogger(__name__)

QGEN_MODEL = "claude-sonnet-4-5-20250929"
PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "qgen.md"


class _AnthropicLike(Protocol):
    messages: Any


def _load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def _extract_text(response: Any) -> str:
    content = getattr(response, "content", None)
    if content is None and isinstance(response, dict):
        content = response.get("content")
    if not content:
        return ""
    for block in content:
        text = getattr(block, "text", None)
        if text is None and isinstance(block, dict):
            text = block.get("text")
        if isinstance(text, str) and text.strip():
            return text
    return ""


def _short_state_summary(state: IntakeState) -> dict[str, Any]:
    """Trimmed state for the Q-Gen prompt — just what's filled + transcript."""
    last_turns = state.transcript[-6:]  # last 3 exchanges max
    return {
        "turn_count": state.turn_count,
        "filled": {
            "emotional_intent": [v.value for v in state.emotional_intent.values]
            if state.emotional_intent.confidence > 0
            else [],
            "social_config": [v.value for v in state.social_config.values]
            if state.social_config.confidence > 0
            else [],
            "energy_level": (
                state.energy_profile.energy_level.value.value
                if state.energy_profile.energy_level.value is not None
                else None
            ),
            "chaos_tolerance": (
                state.energy_profile.chaos_tolerance.value.value
                if state.energy_profile.chaos_tolerance.value is not None
                else None
            ),
            "start_location": state.practical_constraints.start_location.value,
            "time_window": state.practical_constraints.time_window.value,
            "kid_friendly": state.practical_constraints.kid_friendly.value,
            "avoidance": [v.value for v in state.avoidance.values]
            if state.avoidance.confidence > 0
            else [],
        },
        "transcript_tail": [{"role": t.role, "text": t.text} for t in last_turns],
    }


def lowest_confidence_slot(state: IntakeState) -> str:
    """Pick the IntakeState dimension with lowest current confidence.

    This is the deterministic "which slot to ask next" routing function that
    Router calls before invoking generate_question. Returns the IntakeState
    attribute name of the lowest-confidence dim.

    Ties broken in dim-priority order (most user-visible first):
    emotional_intent > social_config > energy_profile > practical_constraints
    > taste_anchors.desired_vibe > avoidance.
    """
    # Composite dims report the min sub-confidence so the slot that's most
    # starved drives selection.
    ep = state.energy_profile
    energy_min = min(
        ep.energy_level.confidence,
        ep.chaos_tolerance.confidence,
        ep.novelty_appetite.confidence,
    )
    pc = state.practical_constraints
    pc_min = min(
        pc.date.confidence,
        pc.time_window.confidence,
        pc.start_location.confidence,
        pc.transport.confidence,
        pc.max_drive_minutes.confidence,
        pc.budget.confidence,
        pc.kid_friendly.confidence,
        pc.needs_parking.confidence,
    )
    ranked: list[tuple[float, str]] = [
        (state.emotional_intent.confidence, "emotional_intent"),
        (state.social_config.confidence, "social_config"),
        (energy_min, "energy_profile"),
        (pc_min, "practical_constraints"),
        (state.taste_anchors.desired_vibe.confidence, "taste_anchors.desired_vibe"),
        (state.avoidance.confidence, "avoidance"),
    ]
    # Stable sort preserves declaration order on ties, which gives us the
    # priority ordering above for free.
    ranked.sort(key=lambda x: x[0])
    return ranked[0][1]


async def generate_question(
    state: IntakeState,
    target_slot: str,
    anthropic_client: _AnthropicLike,
) -> str:
    """Sonnet 4.6 — one MI/OARS-styled question targeting `target_slot`."""
    system_prompt = _load_prompt()
    state_block = json.dumps(_short_state_summary(state), ensure_ascii=False, indent=2)

    user_content = (
        f"## Target slot\n\n`{target_slot}`\n\n"
        "## Current IntakeState snapshot\n\n"
        f"```json\n{state_block}\n```\n\n"
        "Run the 5-step algorithm internally and return ONLY the final "
        "question string. No JSON, no preamble, no Markdown."
    )

    response = await anthropic_client.messages.create(
        model=QGEN_MODEL,
        max_tokens=512,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )
    text = _extract_text(response).strip()
    if not text:
        # Last-resort fallback — Router will move on after one more empty turn
        # via the hard-cap rule. Should be unreachable in practice.
        logger.warning("generate_question: empty response for slot=%s", target_slot)
        return "Tell me a bit more about what you're hoping for today?"
    return text


__all__ = ["generate_question", "lowest_confidence_slot"]
