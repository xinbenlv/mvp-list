"""extract_slots — Haiku 4.5 call (Phase 1b).

Parses one user turn into a slot-updates dict consumable by
`state.merge_slot_updates`. Cheap (Haiku) by design — the Extractor is the
hottest path in the intake loop.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Protocol

from agent.state import IntakeState

logger = logging.getLogger(__name__)

EXTRACTOR_MODEL = "claude-haiku-4-5-20251015"
PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompts" / "extractor.md"


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


def _parse_updates(raw: str) -> dict[str, Any]:
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    elif not text.startswith("{"):
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group(0)
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        logger.warning("extract_slots: JSON parse failed; returning empty updates")
        return {}
    if not isinstance(payload, dict):
        return {}
    return payload


def _state_summary(state: IntakeState) -> dict[str, Any]:
    """Compact dump of the current state for the prompt.

    We do NOT send the full pydantic dump — it's verbose and the model only
    needs to know "what's already filled with what confidence" to avoid
    re-emitting low-confidence overwrites. Keep keys aligned with the schema.
    """
    out: dict[str, Any] = {
        "turn_count": state.turn_count,
        "emotional_intent": {
            "values": [v.value for v in state.emotional_intent.values],
            "confidence": state.emotional_intent.confidence,
        },
        "social_config": {
            "values": [v.value for v in state.social_config.values],
            "confidence": state.social_config.confidence,
        },
        "energy_profile": {
            "energy_level": {
                "value": (
                    state.energy_profile.energy_level.value.value
                    if state.energy_profile.energy_level.value is not None
                    else None
                ),
                "confidence": state.energy_profile.energy_level.confidence,
            },
            "chaos_tolerance": {
                "value": (
                    state.energy_profile.chaos_tolerance.value.value
                    if state.energy_profile.chaos_tolerance.value is not None
                    else None
                ),
                "confidence": state.energy_profile.chaos_tolerance.confidence,
            },
            "novelty_appetite": {
                "value": (
                    state.energy_profile.novelty_appetite.value.value
                    if state.energy_profile.novelty_appetite.value is not None
                    else None
                ),
                "confidence": state.energy_profile.novelty_appetite.confidence,
            },
        },
        "practical_constraints": {
            "date": {
                "value": state.practical_constraints.date.value,
                "confidence": state.practical_constraints.date.confidence,
            },
            "time_window": {
                "value": state.practical_constraints.time_window.value,
                "confidence": state.practical_constraints.time_window.confidence,
            },
            "start_location": {
                "value": state.practical_constraints.start_location.value,
                "confidence": state.practical_constraints.start_location.confidence,
            },
            "transport": {
                "value": state.practical_constraints.transport.value,
                "confidence": state.practical_constraints.transport.confidence,
            },
            "max_drive_minutes": {
                "value": state.practical_constraints.max_drive_minutes.value,
                "confidence": state.practical_constraints.max_drive_minutes.confidence,
            },
            "budget": {
                "value": state.practical_constraints.budget.value,
                "confidence": state.practical_constraints.budget.confidence,
            },
            "kid_friendly": {
                "value": state.practical_constraints.kid_friendly.value,
                "confidence": state.practical_constraints.kid_friendly.confidence,
            },
            "needs_parking": {
                "value": state.practical_constraints.needs_parking.value,
                "confidence": state.practical_constraints.needs_parking.confidence,
            },
        },
        "taste_anchors": {
            "desired_vibe": {
                "values": [v.value for v in state.taste_anchors.desired_vibe.values],
                "confidence": state.taste_anchors.desired_vibe.confidence,
            },
            "food_preferences": {
                "values": list(state.taste_anchors.food_preferences.values),
                "confidence": state.taste_anchors.food_preferences.confidence,
            },
        },
        "avoidance": {
            "values": [v.value for v in state.avoidance.values],
            "confidence": state.avoidance.confidence,
        },
        "stopped_reason": state.stopped_reason,
    }
    return out


async def extract_slots(
    user_turn: str,
    current_state: IntakeState,
    anthropic_client: _AnthropicLike,
) -> dict[str, Any]:
    """Haiku 4.5 — parse one user turn into a slot-updates diff.

    Output shape is the same dict that `state.merge_slot_updates` consumes.
    Empty/whitespace input short-circuits to `{}` without an LLM call.
    """
    if not user_turn or not user_turn.strip():
        return {}

    system_prompt = _load_prompt()
    state_block = json.dumps(_state_summary(current_state), ensure_ascii=False, indent=2)

    user_content = (
        "## Current IntakeState (read-only)\n\n"
        f"```json\n{state_block}\n```\n\n"
        "## New user turn\n\n"
        f"{user_turn.strip()}\n\n"
        "Emit ONLY the slot-updates JSON object per the system prompt contract."
    )

    response = await anthropic_client.messages.create(
        model=EXTRACTOR_MODEL,
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
    )
    raw = _extract_text(response)
    return _parse_updates(raw)


__all__ = ["extract_slots"]
