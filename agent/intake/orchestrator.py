"""Intake Orchestrator — Agent 1.

Phase 0 stub: skips the cyclical Extract/Route/Q-Gen loop and returns a
minimally-populated IntakeState. Phase 1b replaces this with the real loop.
"""

from __future__ import annotations

from dataclasses import dataclass

from agent.state import IntakeState
from agent.tools.vision import vision_extract_taste


@dataclass
class InitialInput:
    text: str = ""
    images: list[str] | None = None


class IntakeOrchestrator:
    """Drives the cyclical intake state machine until `router(state)` says done."""

    async def run(self, initial_input: InitialInput) -> IntakeState:
        state = IntakeState()
        if initial_input.images:
            taste = await vision_extract_taste(initial_input.images)
            state.taste_signature.value = taste
            state.taste_signature.confidence = taste.confidence
        # Phase 1b: while not router(state).is_ready: extract_slots -> qgen -> ask.
        # For Phase 0 we treat the first turn as "ready" — router returns READY by stub.
        return state


__all__ = ["IntakeOrchestrator", "InitialInput"]
