"""CLI entrypoint — wires the stub orchestration end-to-end.

Reads one user turn from stdin, runs the intake / search / concept / compose /
present pipeline using Phase 0 stubs, prints a fake ProposalSet markdown to
stdout. This proves the module wiring is correct before Phase 1 fills the
boxes with real LLM calls.
"""

from __future__ import annotations

import asyncio
import sys

from agent.compose.composer import PlanComposer
from agent.compose.concepts import generate_concepts_simple
from agent.intake.orchestrator import InitialInput, IntakeOrchestrator
from agent.present.format import format_proposals
from agent.state import serialize_to_experience_request
from agent.tools.backend import BackendClient
from agent.types import PlanResult


async def run_once(initial_text: str) -> str:
    """End-to-end stub pipeline. Returns the final ProposalSet markdown."""
    orchestrator = IntakeOrchestrator()
    state = await orchestrator.run(InitialInput(text=initial_text, images=[]))

    backend = BackendClient()
    request = serialize_to_experience_request(state)
    candidates = await backend.search_places(request)

    concepts = generate_concepts_simple(state, candidates)

    composer = PlanComposer()
    plans: list[PlanResult] = await asyncio.gather(
        *(composer.run(c, candidates, state) for c in concepts)
    )

    intake_summary = (
        f"你说: “{initial_text.strip()[:60]}” — Phase 0 stub run."
    )
    return format_proposals(plans, intake_summary)


def main() -> None:
    initial_text = sys.stdin.read()
    markdown = asyncio.run(run_once(initial_text))
    sys.stdout.write(markdown)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
