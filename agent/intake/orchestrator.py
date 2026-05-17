"""Intake Orchestrator — Agent 1.

Drives the cyclical Extract -> Route -> Q-Gen loop until `router(state)`
returns READY or STOP_HARD_CAP. The user-input and agent-output seams are
injectable callables so tests can script a deterministic conversation
without touching stdin/stdout.

Pseudocode (eng-design §4, PRD §interaction-layer):

    state = empty IntakeState
    if images: state.taste_signature = await vision_extract_taste(images)
    if initial_text: state = merge_slot_updates(state, await extract_slots(initial_text, state))
    while True:
        decision = router(state)
        if decision in ("READY", "STOP_HARD_CAP"): break
        target = lowest_confidence_slot(state)
        question = await generate_question(state, target)
        await emit_question(question)
        user_turn = await read_user_turn()
        state = append_turn(state, user_turn)
        state = merge_slot_updates(state, await extract_slots(user_turn, state))
"""

from __future__ import annotations

import logging
import sys
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

from agent.state import IntakeState, TasteSignatureSlot, Turn, merge_slot_updates, router
from agent.tools.extract import extract_slots
from agent.tools.qgen import generate_question, lowest_confidence_slot
from agent.tools.vision import vision_extract_taste

logger = logging.getLogger(__name__)


@dataclass
class InitialInput:
    text: str = ""
    images: list[str] | None = None


async def _default_read_user_turn() -> str:
    """Read one line from stdin (the CLI path)."""
    # Use a thread to avoid blocking the event loop on stdin.
    import asyncio

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, sys.stdin.readline)


async def _default_emit_question(text: str) -> None:
    """Write the next question to stdout (the CLI path)."""
    sys.stdout.write(text.rstrip() + "\n")
    sys.stdout.flush()


@dataclass
class IntakeOrchestrator:
    """Drives the cyclical intake state machine until `router(state)` says done.

    Constructor args:
        anthropic_client: AsyncAnthropic instance (or compatible test fake).
        read_user_turn:   async callable that returns the next user reply
                          string. Defaults to stdin reader.
        emit_question:    async callable that takes the agent's next question
                          and surfaces it (stdout, OpenClaw, test sink, etc.).
                          Defaults to stdout writer.
        max_turns:        safety net for tests; mirrors the router hard-cap
                          but caps the Python loop so a buggy `read_user_turn`
                          can never infinite-loop.
    """

    anthropic_client: Any
    read_user_turn: Callable[[], Awaitable[str]] = field(default=_default_read_user_turn)
    emit_question: Callable[[str], Awaitable[None]] = field(default=_default_emit_question)
    max_turns: int = 12  # router hard-caps at 10; this is the python-side guard

    async def run(self, initial_input: InitialInput) -> IntakeState:
        state = IntakeState()

        # 1. Vision — optional, skipped cleanly when no images supplied.
        if initial_input.images:
            taste = await vision_extract_taste(initial_input.images, self.anthropic_client)
            new_ts = TasteSignatureSlot(
                value=taste,
                confidence=taste.confidence,
            )
            state = state.model_copy(update={"taste_signature": new_ts})

        # 2. Initial text — record as the first user turn + extract slots.
        if initial_input.text and initial_input.text.strip():
            state = _append_turn(state, "user", initial_input.text.strip())
            updates = await extract_slots(initial_input.text, state, self.anthropic_client)
            state = merge_slot_updates(state, updates)

        # 3. Cyclical loop.
        loop_iter = 0
        while loop_iter < self.max_turns:
            loop_iter += 1
            decision = router(state)
            if decision in ("READY", "STOP_HARD_CAP"):
                if state.stopped_reason is None:
                    # Stamp the reason for downstream consumers; router's
                    # decision is the source of truth.
                    reason = (
                        "sufficient_info" if decision == "READY" else "hard_cap"
                    )
                    state = state.model_copy(update={"stopped_reason": reason})
                break

            target_slot = lowest_confidence_slot(state)
            question = await generate_question(state, target_slot, self.anthropic_client)
            state = _append_turn(state, "agent", question)
            await self.emit_question(question)

            user_reply = await self.read_user_turn()
            if user_reply is None or not user_reply.strip():
                # Empty / closed input — treat as user-escape so we don't spin.
                state = state.model_copy(update={"stopped_reason": "user_escape"})
                logger.info("intake: empty user reply, stopping with user_escape")
                continue

            state = _append_turn(state, "user", user_reply.strip())
            updates = await extract_slots(user_reply, state, self.anthropic_client)
            state = merge_slot_updates(state, updates)

        # Safety stamp if we fell out of the loop without stopped_reason set.
        if state.stopped_reason is None:
            state = state.model_copy(update={"stopped_reason": "hard_cap"})
        return state


def _append_turn(state: IntakeState, role: str, text: str) -> IntakeState:
    """Append one Turn to the transcript without bumping turn_count.

    `turn_count` is owned by `merge_slot_updates` (incremented once per
    extractor merge). Adding turns here keeps the transcript faithful so the
    Composer can quote it later.
    """
    new_turn = Turn(role=role, text=text, turn_index=len(state.transcript))  # type: ignore[arg-type]
    new_transcript = [*state.transcript, new_turn]
    return state.model_copy(update={"transcript": new_transcript})


__all__ = ["IntakeOrchestrator", "InitialInput"]
