"""generate_question — Sonnet 4.6 info-gain Q-Gen (Phase 1b).

Phase 0 stub: returns a hardcoded MI/OARS-styled placeholder question.
"""

from __future__ import annotations

from agent.state import IntakeState


async def generate_question(state: IntakeState, target_slot: str) -> str:
    """Phase 0 stub: returns a placeholder question string."""
    return f"[stub-qgen for slot={target_slot}] 你想要的是恢复还是探索？"


__all__ = ["generate_question"]
