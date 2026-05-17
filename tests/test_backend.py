"""Phase 2 tests — backend mock + weighted vibe overlap ranking.

No LLM, no network. Reads `poc-demo/demo_places.json` directly through the
mock backend path and asserts that ranking is real (not constant), respects
hard filters, and round-trips correctly from `serialize_to_experience_request`.
"""

from __future__ import annotations

import os

import pytest

from agent.state import serialize_to_experience_request
from agent.tools.backend import search_places
from agent.types import ExperienceRequest, TasteSignature, VibeTag, VibeWeight

# Reuse the persona loader from test_state.py via a relative import. This
# keeps a single source of truth for "what does Mia/Garry/Alex/Sam look
# like as an IntakeState?" — Phase 2 tests should not duplicate that
# fixture-loading logic.
from tests.test_state import PERSONA_NAMES, _load_persona_state

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _enable_mock_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    """All Phase 2 tests run with MOCK_BACKEND=1 unless explicitly toggled."""
    monkeypatch.setenv("MOCK_BACKEND", "1")


async def _candidates_for(persona: str):
    state = _load_persona_state(persona)
    request = serialize_to_experience_request(state)
    return await search_places(request)


# ---------------------------------------------------------------------------
# Per-persona round-trip — ≥4 candidates, all fit_score > 0
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("persona", PERSONA_NAMES)
async def test_persona_round_trip_returns_candidates(persona: str) -> None:
    candidates = await _candidates_for(persona)

    assert len(candidates) >= 4, (
        f"{persona}: expected ≥4 candidates, got {len(candidates)}"
    )
    assert all(c.fit_score > 0 for c in candidates), (
        f"{persona}: every candidate must have positive fit_score; got "
        f"{[(c.place_id, c.fit_score) for c in candidates]}"
    )


# ---------------------------------------------------------------------------
# Top candidate matches persona's strongest vibe — Mia case
# ---------------------------------------------------------------------------


async def test_mia_top_candidate_matches_quiet_warm() -> None:
    """Mia's vibe weights peak on restorative / cinematic / natural_light /
    intimate / warm / quiet. Her top candidate should carry at least one of
    {quiet, warm, restorative, slow, low_noise} in its vibe_tags — these are
    the demo-vocab analogs of her top weights.
    """
    candidates = await _candidates_for("mia")
    top = candidates[0]
    top_tags = {t["tag"] for t in top.composition.get("vibe_tags", [])}
    expected_any = {"quiet", "warm", "restorative", "slow", "low_noise"}
    assert top_tags & expected_any, (
        f"Mia's top candidate {top.place_id} should match at least one of "
        f"{expected_any}; got tags={top_tags}"
    )
    # Sanity: fit_reason mentions a contributing tag.
    assert top.fit_reason.startswith("matches:"), top.fit_reason


# ---------------------------------------------------------------------------
# Ranking is real — different personas get different orderings
# ---------------------------------------------------------------------------


async def test_ranking_differs_between_personas() -> None:
    """Mia (restorative-leaning) and Garry (cinematic-leaning) must produce
    different top-3 orderings on the same 22-place demo set. If they don't,
    the ranking is constant and the POC fails the eng design §10 integrity
    bar."""
    mia = await _candidates_for("mia")
    garry = await _candidates_for("garry_tan")

    mia_top3 = [c.place_id for c in mia[:3]]
    garry_top3 = [c.place_id for c in garry[:3]]

    assert mia_top3 != garry_top3, (
        f"Mia and Garry must rank differently (ranking is real, not constant).\n"
        f"  Mia top-3:   {mia_top3}\n"
        f"  Garry top-3: {garry_top3}"
    )


# ---------------------------------------------------------------------------
# Hard filter — kid_friendly_required drops adult-only places
# ---------------------------------------------------------------------------


async def test_kid_friendly_filter_drops_adult_only() -> None:
    """Mia carries kid_friendly_required=True. Adult-only demo places
    (spaced_out_comedy, true_laurel_mission, the_independent_divisadero,
    osmosis_freestone) must NOT appear in her candidate list."""
    candidates = await _candidates_for("mia")
    place_ids = {c.place_id for c in candidates}
    adult_only = {
        "spaced_out_comedy",
        "true_laurel_mission",
        "the_independent_divisadero",
        "osmosis_freestone",
    }
    assert not (place_ids & adult_only), (
        f"kid_friendly filter failed; adult-only places leaked into Mia's "
        f"candidates: {place_ids & adult_only}"
    )


# ---------------------------------------------------------------------------
# MOCK_BACKEND flag actually flips behavior
# ---------------------------------------------------------------------------


async def test_mock_backend_unset_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    """When MOCK_BACKEND is unset, search_places must raise NotImplementedError
    so we never silently hit a non-existent real backend."""
    monkeypatch.delenv("MOCK_BACKEND", raising=False)
    state = _load_persona_state("mia")
    request = serialize_to_experience_request(state)
    with pytest.raises(NotImplementedError):
        await search_places(request)


async def test_mock_backend_set_returns_results() -> None:
    """Sanity flip: with MOCK_BACKEND=1 we always get results."""
    assert os.getenv("MOCK_BACKEND") == "1"
    state = _load_persona_state("mia")
    request = serialize_to_experience_request(state)
    out = await search_places(request)
    assert len(out) > 0


# ---------------------------------------------------------------------------
# Bad input — empty TasteSignature falls back to uniform ranking
# ---------------------------------------------------------------------------


async def test_empty_taste_signature_returns_top12_uniform() -> None:
    """No vibe_weights → ranking falls back to a uniform-ish default. We
    still expect 12 candidates (or fewer if any hard filters drop some),
    each with `fit_reason` documenting the fallback."""
    request = ExperienceRequest(
        trip_context={},
        experience_intent={},
        constraints={},
        taste_context={"taste_signature": TasteSignature().model_dump()},
    )
    out = await search_places(request)
    assert len(out) == 12, f"expected top-12 default, got {len(out)}"
    assert all(c.fit_reason.startswith("no taste signature") for c in out)


# ---------------------------------------------------------------------------
# Avoidance soft-penalty — present but doesn't fully drop a place
# ---------------------------------------------------------------------------


async def test_avoidance_is_soft_not_hard() -> None:
    """Avoidance tags must NOT hard-drop places — they only penalize ranking.

    We craft a request whose taste_signature would normally rank
    `dong_que` (lively + warm + authentic) near the top. Adding `lively`
    as an avoidance tag should still leave it in the candidate set (not
    a hard filter) but with a lower fit_score than without.
    """
    base_request = ExperienceRequest(
        trip_context={},
        experience_intent={},
        constraints={},
        taste_context={
            "taste_signature": TasteSignature(
                vibe_weights=[
                    VibeWeight(tag=VibeTag.LIVELY, weight=0.9),
                    VibeWeight(tag=VibeTag.WARM, weight=0.7),
                    VibeWeight(tag=VibeTag.AUTHENTIC, weight=0.8),
                ],
                summary="lively warm authentic",
                confidence=0.9,
            ).model_dump()
        },
    )
    penalized_request = base_request.model_copy(deep=True)
    penalized_request.experience_intent = {"avoid": ["lively"]}

    base = await search_places(base_request)
    penalized = await search_places(penalized_request)

    base_dq = next((c for c in base if c.place_id == "dong_que"), None)
    pen_dq = next((c for c in penalized if c.place_id == "dong_que"), None)

    assert base_dq is not None, "dong_que should appear in base ranking"
    assert pen_dq is not None, (
        "avoidance must be soft — dong_que should still appear even when "
        "'lively' is in avoid"
    )
    assert pen_dq.fit_score < base_dq.fit_score, (
        f"avoidance soft-penalty did not lower dong_que's fit_score: "
        f"base={base_dq.fit_score} penalized={pen_dq.fit_score}"
    )
