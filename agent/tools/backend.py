"""search_places — backend client.

Phase 0 stub: returns a small fake PlaceCandidate list. Phase 2 wires the real
weighted-vibe overlap ranking against poc-demo/demo_places.json.
"""

from __future__ import annotations

from agent.types import ExperienceRequest, PlaceCandidate


class BackendClient:
    """Wraps the G-Brain `/experience` API. POC defaults to in-memory mock."""

    async def search_places(self, request: ExperienceRequest) -> list[PlaceCandidate]:
        """Phase 0 stub: 6 fake candidates."""
        return [
            PlaceCandidate(
                place_id=f"stub_place_{i}",
                name=f"Stub Place {i}",
                fit_score=0.9 - 0.1 * i,
                fit_reason="stub reason",
                composition={"vibe_tags": []},
            )
            for i in range(6)
        ]

    async def search_places_real(
        self, request: ExperienceRequest
    ) -> list[PlaceCandidate]:
        """Phase 2 — POST /experience via httpx. Stubbed in Phase 0."""
        raise NotImplementedError("Phase 2 — real backend call")


__all__ = ["BackendClient"]
