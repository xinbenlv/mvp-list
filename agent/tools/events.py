"""search_events — Ticketmaster MCP + Funcheap RSS. [Future PR — Phase 4]"""

from __future__ import annotations

from typing import Any


async def search_events(date: str, location: str) -> list[dict[str, Any]]:
    """Phase 4 — implementation pending."""
    raise NotImplementedError("Phase 4 enrichment tool")


__all__ = ["search_events"]
