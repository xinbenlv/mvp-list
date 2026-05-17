"""vision_extract_taste — Sonnet 4.6 + vision call (Phase 1b).

Phase 0 stub: returns a canned TasteSignature so the smoke flow can run offline.
"""

from __future__ import annotations

from agent.types import TasteSignature, VibeTag, VibeWeight


async def vision_extract_taste(image_paths: list[str]) -> TasteSignature:
    """Phase 0 stub: canned fake TasteSignature; no LLM call."""
    return TasteSignature(
        vibe_weights=[
            VibeWeight(tag=VibeTag.QUIET, weight=0.8),
            VibeWeight(tag=VibeTag.WARM, weight=0.7),
            VibeWeight(tag=VibeTag.AUTHENTIC, weight=0.6),
        ],
        summary="stub taste — quiet/warm/authentic leaning",
        confidence=0.5,
    )


__all__ = ["vision_extract_taste"]
