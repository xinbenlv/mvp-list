"""Plan Composer — Agent 2.

Phase 0 stub: returns a fake PlanResult with a placeholder markdown block.
Phase 3a replaces this with a real Sonnet 4.6 call against composer_prompt.md.
"""

from __future__ import annotations

from agent.state import IntakeState
from agent.types import Concept, PlaceCandidate, PlanResult


class PlanComposer:
    """Composes one TripPlan from one Concept + candidate pool + IntakeState."""

    def __init__(self) -> None:
        # Phase 3a: read prompts/composer.md (symlink -> poc-demo/composer_prompt.md).
        self._prompt: str = ""

    async def run(
        self,
        concept: Concept,
        candidates: list[PlaceCandidate],
        intake_state: IntakeState,
    ) -> PlanResult:
        """Return one PlanResult (Phase 0 stub: hardcoded markdown shell)."""
        stop_ids = (concept.anchor_place_ids + [c.place_id for c in candidates])[:4]
        # Pad to 4 stops with sentinel ids if the candidate pool is too small.
        while len(stop_ids) < 4:
            stop_ids.append(f"stub_stop_{len(stop_ids)}")

        markdown = (
            f"## {concept.day_theme}\n\n"
            f"> **一句话 pitch**: {concept.emotional_thesis}\n\n"
            f"### 10:00 · {stop_ids[0]}\n"
            f"*why_fits_today*: stub justification — Phase 3a fills this in.\n\n"
            f"### 12:30 · {stop_ids[1]}\n"
            f"*why_fits_today*: stub justification.\n\n"
            f"### 15:00 · {stop_ids[2]}\n"
            f"*why_fits_today*: stub justification.\n\n"
            f"### 17:30 · {stop_ids[3]}\n"
            f"*why_fits_today*: stub justification.\n\n"
            f"## 🔀 如果今天有变化\n\n"
            f"Phase 3a will fill in the adaptive branch.\n"
        )
        return PlanResult(
            markdown=markdown,
            day_theme=concept.day_theme,
            pitch=concept.emotional_thesis,
            theme_anchor=concept.theme_anchor,
            stop_place_ids=stop_ids,
            raw_metadata={"stub": True},
        )


__all__ = ["PlanComposer"]
