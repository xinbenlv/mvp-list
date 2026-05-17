"""search_places — backend client (Phase 2 implementation).

Phase 2: `MOCK_BACKEND=1` reads `poc-demo/demo_places.json` directly and ranks
places by weighted vibe overlap against `request.taste_context.taste_signature
.vibe_weights`. No HTTP — pure in-memory. Real backend HTTP is stubbed and
raises `NotImplementedError` until Phase 4 (eng design §10 boundary).

Ranking algorithm (per task spec):
    fit_score = sum(min(req_weight_i, place_weight_i)) / sum(req_weight_i)
where the sum runs over the union of tag names appearing on the request side.
Result is in [0, 1] when the request side has at least one positive weight.

Hard filters:
- `constraints.kid_friendly` → drop places with `logistics.kid_friendly == false`
- `constraints.needs_parking` → drop places whose `logistics.parking` value
  signals "no parking" (e.g. `transit_required`).
- `constraints.max_drive_minutes` → SKIPPED for POC. The demo set has no real
  driving-distance signal; geographic fit is implicit via vibe ranking.
  TODO(phase4): when backend wires real lat/lon + travel-time, apply this
  filter here.

Soft penalty:
- `experience_intent.avoid` → for each matching avoidance tag found on the
  place's `vibe_tags` (string-name match), subtract 0.05 from `fit_score`.
  Avoidance is a soft preference for ranking, not a hard cut.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from agent.types import ExperienceRequest, PlaceCandidate

# poc-demo lives at the repo root, two levels up from agent/tools/.
_DEMO_PLACES_PATH = (
    Path(__file__).resolve().parent.parent.parent / "poc-demo" / "demo_places.json"
)

# How many candidates to return from the mock backend (eng design §10:
# Composer-side concept filters need a healthy pool; 12 leaves room for
# theme-anchored filtering to find ≥2 viable candidates per theme even when
# multiple themes overlap on the same vibe vocab).
_TOP_N = 12

# Avoidance soft-penalty magnitude per matching tag.
_AVOIDANCE_PENALTY = 0.05

# Parking values that count as "no/uncertain parking" when needs_parking=True.
# Conservative: only `transit_required` is explicitly a deal-breaker; the
# demo set doesn't currently use that value, but we keep it future-proof.
_NO_PARKING_VALUES = {"transit_required"}


def _load_demo_places() -> list[dict[str, Any]]:
    """Read the 22-place demo set off disk. Single read per call — POC scale."""
    with _DEMO_PLACES_PATH.open("r", encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    places: list[dict[str, Any]] = data.get("places", [])
    return places


def _request_vibe_weights(request: ExperienceRequest) -> dict[str, float]:
    """Extract a flat {tag_name: weight} dict from the request's taste_signature.

    Returns {} when nothing is set — caller falls back to uniform ranking.
    """
    ts = request.taste_context.get("taste_signature") or {}
    if isinstance(ts, dict):
        vw_raw = ts.get("vibe_weights") or []
    else:
        # pydantic model passed by mistake — defensive
        vw_raw = getattr(ts, "vibe_weights", []) or []
    out: dict[str, float] = {}
    for item in vw_raw:
        if isinstance(item, dict):
            tag = item.get("tag")
            weight = item.get("weight")
        else:
            tag = getattr(item, "tag", None)
            weight = getattr(item, "weight", None)
        if tag is None or weight is None:
            continue
        # tag may be a StrEnum — normalize to string for comparison with the
        # demo_places.json strings (which use vocab outside VibeTag too).
        out[str(tag)] = float(weight)
    return out


def _place_vibe_weights(place: dict[str, Any]) -> dict[str, float]:
    """Pull `composition.vibe_tags` into a flat {tag: weight} dict."""
    comp = place.get("composition") or {}
    tags = comp.get("vibe_tags") or []
    return {str(item["tag"]): float(item["weight"]) for item in tags}


def _compute_fit(
    request_weights: dict[str, float],
    place_weights: dict[str, float],
) -> tuple[float, list[tuple[str, float]]]:
    """Return (fit_score, contributing_tags_sorted_desc).

    Score:
        numerator = sum_t min(request_weights[t], place_weights[t]) over t in
                    intersection
        denominator = sum_t request_weights[t]
        score = numerator / denominator if denominator > 0 else 0
    Contributing tags: per-tag contribution (the `min()` value), ordered desc.
    """
    if not request_weights:
        # Caller will fall back to uniform ranking.
        return 0.0, []

    denominator = sum(request_weights.values())
    if denominator <= 0.0:
        return 0.0, []

    contribs: list[tuple[str, float]] = []
    numerator = 0.0
    for tag, req_w in request_weights.items():
        place_w = place_weights.get(tag)
        if place_w is None:
            continue
        contrib = min(req_w, place_w)
        numerator += contrib
        contribs.append((tag, contrib))

    score = numerator / denominator
    contribs.sort(key=lambda x: x[1], reverse=True)
    return score, contribs


def _build_fit_reason(contribs: list[tuple[str, float]]) -> str:
    """1-liner naming the top-3 contributing tags + their contribution weights."""
    if not contribs:
        return "no overlapping vibe tags"
    top = contribs[:3]
    parts = [f"{tag} {val:.1f}" for tag, val in top]
    return "matches: " + " / ".join(parts)


def _passes_hard_filters(place: dict[str, Any], request: ExperienceRequest) -> bool:
    """Apply the POC hard filters. Returns False to drop the place."""
    logistics = place.get("logistics") or {}
    constraints = request.constraints or {}

    if constraints.get("kid_friendly") and logistics.get("kid_friendly") is False:
        return False

    if constraints.get("needs_parking"):
        parking = logistics.get("parking")
        if parking in _NO_PARKING_VALUES:
            return False

    # TODO(phase4): apply `constraints.max_drive_minutes` once real
    # driving-distance signals are available from backend. POC has no
    # lat/lon-grade distance, so geographic fit is implicit in ranking.
    return True


def _avoidance_penalty(
    place: dict[str, Any], request: ExperienceRequest
) -> float:
    """Soft penalty per matching avoidance tag on the place's vibe vocab."""
    avoid = (request.experience_intent or {}).get("avoid") or []
    if not avoid:
        return 0.0
    avoid_set = {str(a) for a in avoid}
    place_tags = set(_place_vibe_weights(place).keys())
    # Match by string name (avoidance tags don't always exist on VibeTag —
    # this is a name-overlap heuristic, e.g. `loud` vs nothing on the place
    # side; `touristy` not on vibe_tags side; etc.). Keep conservative.
    overlap = avoid_set & place_tags
    return _AVOIDANCE_PENALTY * len(overlap)


def _to_place_candidate(
    place: dict[str, Any], fit_score: float, fit_reason: str
) -> PlaceCandidate:
    return PlaceCandidate(
        place_id=str(place["place_id"]),
        name=str(place["name"]),
        place_type=place.get("place_type"),
        city=place.get("city"),
        address=place.get("address"),
        hours_note=place.get("hours_note"),
        composition=place.get("composition") or {},
        logistics=place.get("logistics") or {},
        narrative_hook=place.get("narrative_hook"),
        restaurant=place.get("restaurant"),
        hero_image_url=place.get("hero_image_url"),
        fit_score=round(max(fit_score, 0.0), 4),
        fit_reason=fit_reason,
    )


# ---------------------------------------------------------------------------
# Public entrypoints
# ---------------------------------------------------------------------------


async def search_places(request: ExperienceRequest) -> list[PlaceCandidate]:
    """Phase 2 — `MOCK_BACKEND=1` reads demo_places.json + does weighted
    vibe overlap ranking. Real backend (HTTP) raises NotImplementedError.

    Returns top-12 PlaceCandidates sorted by `fit_score` desc.

    Empty request taste_signature → uniform 0.5 score (graceful degrade so
    downstream Concept generation still gets ranked candidates).
    """
    if os.getenv("MOCK_BACKEND") != "1":
        # TODO(phase4): wire httpx HTTP client to POST /experience and parse
        # the response into PlaceCandidate[]. POC explicitly forbids this.
        raise NotImplementedError("Real backend not wired in POC")

    places = _load_demo_places()
    request_weights = _request_vibe_weights(request)

    scored: list[PlaceCandidate] = []
    for place in places:
        if not _passes_hard_filters(place, request):
            continue
        place_weights = _place_vibe_weights(place)

        if request_weights:
            fit_score, contribs = _compute_fit(request_weights, place_weights)
            fit_reason = _build_fit_reason(contribs)
        else:
            # Uniform fallback: average of the place's vibe weights so the
            # ordering is at least informative (places with stronger overall
            # vibe presence bubble to the top).
            place_avg = (
                sum(place_weights.values()) / len(place_weights)
                if place_weights
                else 0.0
            )
            fit_score, fit_reason = place_avg, "no taste signature — uniform rank"

        # Soft penalty for avoidance overlap.
        penalty = _avoidance_penalty(place, request)
        fit_score = max(fit_score - penalty, 0.0)

        scored.append(_to_place_candidate(place, fit_score, fit_reason))

    scored.sort(key=lambda c: c.fit_score, reverse=True)
    return scored[:_TOP_N]


class BackendClient:
    """Wraps the G-Brain `/experience` API. POC defaults to in-memory mock.

    Kept as a thin OO wrapper around the module-level functions so older call
    sites that hold a `BackendClient` instance keep working. Eng design §10
    treats `search_places(request)` as the canonical surface.
    """

    async def search_places(self, request: ExperienceRequest) -> list[PlaceCandidate]:
        return await search_places(request)

    async def search_places_real(
        self, request: ExperienceRequest
    ) -> list[PlaceCandidate]:
        """Phase 4 — POST /experience via httpx."""
        raise NotImplementedError("Real backend not wired in POC")


__all__ = ["search_places", "BackendClient"]
