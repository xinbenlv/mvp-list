"""get_weather — Open-Meteo wrapper. [Future PR — Phase 4]"""

from __future__ import annotations

from typing import Any


async def get_weather(date: str, location: str) -> dict[str, Any]:
    """Phase 4 — implementation pending."""
    raise NotImplementedError("Phase 4 enrichment tool")


__all__ = ["get_weather"]
