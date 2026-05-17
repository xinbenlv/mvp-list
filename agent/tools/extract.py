"""extract_slots — Haiku 4.5 call (Phase 1b).

Phase 0 stub: returns an empty SlotUpdates dict; no LLM call.
"""

from __future__ import annotations

from typing import Any

from agent.state import IntakeState


async def extract_slots(user_turn: str, state: IntakeState) -> dict[str, Any]:
    """Phase 0 stub: returns empty dict."""
    return {}


__all__ = ["extract_slots"]
