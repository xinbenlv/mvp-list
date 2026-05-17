"""PlanResult → frontend TripPlan JSON transformer.

The frontend (day-composer-app) consumes a different shape than the backend
PlanResult: emotional_arc is flattened to two strings, score_summary is a
fixed sub-dict, etc. See `day-composer-app/lib/types/trip-plan.ts` for the
exact contract and `poc-demo/garry-demo/HANDOFF.md` §3 for the diffs vs the
backend spec.

This module is the single conversion point. It owns:
  - reshape rules (emotional_arc list → text + visual)
  - per-stop coercion via PlanResult.stops (already the right shape)
  - score_summary stub (live LLM runs don't carry a numeric score today)
  - {plan, trip_context} envelope construction
"""

from __future__ import annotations

from typing import Any

from agent.types import PlanResult, Stop

# Default score_summary when we don't have a Critic-produced one. The
# frontend reads but never renders this today (see HANDOFF.md §6). Marking
# everything 0 + a clear note keeps it obviously a placeholder.
_DEFAULT_SCORE_SUMMARY: dict[str, Any] = {
    "stranger_test": 0,
    "arc_coherence": 0,
    "specificity": 0,
    "avoidance_respect": 0,
    "adaptive_branch": 0,
    "notes": "live LLM run — score_summary not computed (Critic Phase 5 pending)",
}


def _stop_to_dict(stop: Stop, index: int) -> dict[str, Any]:
    """Dump one Stop into the frontend's per-stop shape.

    Pydantic's `model_dump(mode="json")` already matches the frontend keys
    1:1 (we designed Stop / Logistics / OrderRecs to mirror trip-plan.ts).
    We only enforce stop_index here in case the LLM forgot to set it.
    """
    data = stop.model_dump(mode="json")
    if not data.get("stop_index"):
        data["stop_index"] = index
    # image_url defaults to null — frontend renders gradient fallbacks when
    # absent (HANDOFF §4 pattern B). Leaving here as a hook for backend-set
    # images later.
    data.setdefault("image_url", None)
    return data


def _emotional_arc_text(plan: PlanResult) -> str:
    """Join the pacing labels into the frontend's one-liner format.

    Frontend expects a single string like `"Light & shadow opening → visual
    peak → lawn breathing → neighborhood-heat dinner"`. Our PlanResult
    carries the same info as a list — we join with the unicode arrow the
    reference JSONs use.
    """
    arc = plan.emotional_arc or []
    return " → ".join(str(beat).strip() for beat in arc if str(beat).strip())


def plan_result_to_frontend_dict(
    plan: PlanResult,
    *,
    persona_id: str,
    plan_id: str,
    version: str = "v1",
) -> dict[str, Any]:
    """Convert one PlanResult into the dict the frontend `TripPlan` TS type expects.

    Args:
        plan: backend PlanResult
        persona_id: e.g. "garry" — frontend uses this for image lookup defaults
        plan_id: e.g. "garry_cultural_day" — stable id; frontend keys on it
        version: schema version string, default "v1"

    Returns:
        dict matching `TripPlan` in `day-composer-app/lib/types/trip-plan.ts`.
        Suitable for `json.dump`-ing to a file or returning as an HTTP body.
    """
    stops_payload: list[dict[str, Any]] = []
    if plan.stops:
        for i, stop in enumerate(plan.stops):
            stops_payload.append(_stop_to_dict(stop, i))

    return {
        "plan_id": plan_id,
        "persona_id": persona_id,
        "version": version,
        "day_theme": plan.day_theme,
        "theme_anchor": plan.theme_anchor.value if plan.theme_anchor else None,
        "pitch": plan.pitch or None,
        "mood_tags": list(plan.mood_tags),
        "emotional_arc_text": _emotional_arc_text(plan),
        # Composer doesn't produce the ASCII-emoji visual block as a separate
        # field today; the markdown body has it but extracting cleanly would
        # be brittle. Leaving empty — frontend ignores when blank.
        "emotional_arc_visual": "",
        "stops": stops_payload,
        "adaptive_branches": list(plan.adaptive_branches),
        "markdown_full": plan.markdown or "",
        "coaching_block": None,
        "composer_note": plan.composer_note or None,
        "score_summary": dict(_DEFAULT_SCORE_SUMMARY),
    }


def build_envelope(
    plan: PlanResult,
    *,
    persona_id: str,
    plan_id: str,
    trip_context: dict[str, Any],
    version: str = "v1",
) -> dict[str, Any]:
    """Wrap a PlanResult + trip_context stub into the `{plan, trip_context}`
    envelope the frontend reads at `/api/plans/[id]` and writes from `--emit-frontend-json`."""
    return {
        "plan": plan_result_to_frontend_dict(
            plan, persona_id=persona_id, plan_id=plan_id, version=version
        ),
        "trip_context": trip_context,
    }


__all__ = [
    "plan_result_to_frontend_dict",
    "build_envelope",
]
