"""Plan Critic — Phase 5 scaffold only.

The full body is deferred (see Implement-poc.md Phase 5). This file exists so the
import path is wired and CritiqueResult validates.
"""

from __future__ import annotations

from agent.state import IntakeState
from agent.types import CritiqueResult, PlanResult


def score_plans(plans: list[PlanResult], state: IntakeState) -> list[CritiqueResult]:
    """Phase 5 — quality gate. See agent/prompts/critic.md for the 5-dim rubric."""
    raise NotImplementedError("Phase 5 — implement if time permits")


__all__ = ["score_plans"]
