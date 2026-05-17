"""Phase 2 tests — `generate_concepts_simple` rule-based multi-Concept seed.

No LLM, no network. Each test feeds a persona's IntakeState + the candidate
pool produced by `search_places` (also POC mock) and asserts the theme
selection + filter + drop-to-N-1 behavior matches eng design §6.
"""

from __future__ import annotations

import pytest

from agent.compose.concepts import (
    ConceptGenerationError,
    filter_candidates_for_theme,
    generate_concepts_simple,
    select_themes,
)
from agent.state import serialize_to_experience_request
from agent.tools.backend import search_places
from agent.types import (
    PlaceCandidate,
    ThemeAnchor,
)
from tests.test_state import _load_persona_state

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _enable_mock_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MOCK_BACKEND", "1")


async def _state_and_candidates(persona: str):
    state = _load_persona_state(persona)
    request = serialize_to_experience_request(state)
    candidates = await search_places(request)
    return state, candidates


# ---------------------------------------------------------------------------
# Step 1 — Theme selection per persona
# ---------------------------------------------------------------------------


def test_mia_theme_selection() -> None:
    """Mia has restore in intent + chaos=low → Mia-like branch."""
    state = _load_persona_state("mia")
    themes = select_themes(state)
    assert themes == [
        ThemeAnchor.CULTURAL_RESTORATIVE,
        ThemeAnchor.OUTDOOR_EXPLORATORY,
        ThemeAnchor.QUIET_INTIMATE,
    ], themes


def test_garry_theme_selection() -> None:
    """Garry has energy=high + explore in intent → Garry/Alex-like branch."""
    state = _load_persona_state("garry_tan")
    themes = select_themes(state)
    assert themes == [
        ThemeAnchor.SOCIAL_HIGH_ENERGY,
        ThemeAnchor.OUTDOOR_EXPLORATORY,
        ThemeAnchor.CULTURAL_RESTORATIVE,
    ], themes


def test_alex_theme_selection() -> None:
    """Alex has energy=high + explore in intent → Garry/Alex-like branch."""
    state = _load_persona_state("alex_chen")
    themes = select_themes(state)
    assert themes == [
        ThemeAnchor.SOCIAL_HIGH_ENERGY,
        ThemeAnchor.OUTDOOR_EXPLORATORY,
        ThemeAnchor.CULTURAL_RESTORATIVE,
    ], themes


def test_sam_theme_selection() -> None:
    """Sam has restore/slow_down in intent + energy=low + chaos=very_low
    (coerced to LOW by the loader) → Mia-like branch."""
    state = _load_persona_state("sam_reyes")
    themes = select_themes(state)
    assert themes == [
        ThemeAnchor.CULTURAL_RESTORATIVE,
        ThemeAnchor.OUTDOOR_EXPLORATORY,
        ThemeAnchor.QUIET_INTIMATE,
    ], themes


# ---------------------------------------------------------------------------
# Step 2 — Per-theme filter sanity (Mia gets ≥2 in each of her themes)
# ---------------------------------------------------------------------------


async def test_mia_each_theme_has_two_viable_candidates() -> None:
    """The relaxed `quiet_intimate` filter (+ warm/low_noise) is the
    specific design fix that makes this hold for Mia + Sam. Regression
    guard: if someone re-tightens the filter, Mia drops to N=2 here."""
    state, candidates = await _state_and_candidates("mia")
    themes = select_themes(state)
    for theme in themes:
        filtered = filter_candidates_for_theme(theme, candidates)
        assert len(filtered) >= 2, (
            f"Mia / {theme.value} only has {len(filtered)} viable candidates "
            f"after filtering. Eng design §6 expects ≥2 for the POC demo set."
        )


# ---------------------------------------------------------------------------
# Step 4 — Drop-to-N-1 synthetic edge case
# ---------------------------------------------------------------------------


def _fake_candidate(place_id: str, tags: list[str], fit_score: float = 0.8) -> PlaceCandidate:
    """Synthesize a minimal PlaceCandidate carrying a fixed vibe_tag set."""
    return PlaceCandidate(
        place_id=place_id,
        name=place_id.replace("_", " ").title(),
        composition={"vibe_tags": [{"tag": t, "weight": 0.8} for t in tags]},
        fit_score=fit_score,
        fit_reason="synthetic",
    )


async def test_drop_to_n_minus_one_when_one_theme_starves() -> None:
    """If a theme has 0 candidates after filtering, generate_concepts_simple
    must drop that theme and return N-1.

    Synthesized pool:
      - 2 cultural_restorative-only places (tags ⊂ {authentic, cultural} —
        which intersect cultural_restorative's filter but NOT quiet_intimate's)
      - 2 outdoor-only places (tags ⊂ {outdoor, walkable, spacious} —
        which intersect outdoor_exploratory but NOT quiet_intimate)

    Mia's theme order is [cultural_restorative, outdoor_exploratory,
    quiet_intimate]. With this pool, quiet_intimate has 0 viable candidates,
    so generate_concepts_simple must drop it → 2 Concepts.
    """
    state = _load_persona_state("mia")
    pruned = [
        _fake_candidate("cult_a", ["authentic", "cultural"], 0.9),
        _fake_candidate("cult_b", ["authentic", "cultural"], 0.85),
        _fake_candidate("out_a", ["outdoor", "walkable"], 0.88),
        _fake_candidate("out_b", ["outdoor", "spacious"], 0.84),
    ]

    concepts = generate_concepts_simple(state, pruned)
    assert len(concepts) == 2, (
        f"Expected drop-to-N-1=2 when quiet_intimate starves; got "
        f"{[c.theme_anchor.value for c in concepts]}"
    )
    # The surviving themes must be the first two (cultural_restorative,
    # outdoor_exploratory) — quiet_intimate dropped.
    assert {c.theme_anchor for c in concepts} == {
        ThemeAnchor.CULTURAL_RESTORATIVE,
        ThemeAnchor.OUTDOOR_EXPLORATORY,
    }


async def test_diagnostic_raised_when_less_than_two_themes_viable() -> None:
    """Final N < 2 must raise ConceptGenerationError with per-theme counts."""
    state = _load_persona_state("mia")
    # 0 candidates → every theme has 0 viable matches.
    with pytest.raises(ConceptGenerationError) as exc:
        generate_concepts_simple(state, [])
    # Message must include diagnostic detail (per-theme counts).
    assert "cultural_restorative=0" in str(exc.value)


# ---------------------------------------------------------------------------
# Step 5 — Concept fields are populated correctly
# ---------------------------------------------------------------------------


async def test_concept_fields_populated_for_mia() -> None:
    state, candidates = await _state_and_candidates("mia")
    concepts = generate_concepts_simple(state, candidates)

    assert len(concepts) >= 2

    seen_themes: set[ThemeAnchor] = set()
    for concept in concepts:
        # day_theme is a non-empty Chinese string (contains at least one CJK
        # char — easiest check: any char > U+4E00).
        assert any(ord(ch) >= 0x4E00 for ch in concept.day_theme), (
            f"day_theme not Chinese: {concept.day_theme!r}"
        )
        # anchor_place_ids length == 2 (top-2 per theme).
        assert len(concept.anchor_place_ids) == 2, concept.anchor_place_ids
        # theme_anchor is a ThemeAnchor enum member.
        assert isinstance(concept.theme_anchor, ThemeAnchor)
        # Pacing blueprint is the canonical 4-act.
        assert [p.value for p in concept.pacing_blueprint] == [
            "opening",
            "breathing",
            "peak",
            "closing",
        ]
        # mood_tags non-empty.
        assert concept.mood_tags, "mood_tags must not be empty"
        # emotional_thesis is a non-empty string referencing the lead anchor.
        assert concept.emotional_thesis
        # concept_id well-formed.
        assert concept.theme_anchor.value in concept.concept_id

        seen_themes.add(concept.theme_anchor)

    # All concepts have distinct theme_anchors (structural diversity guarantee).
    assert len(seen_themes) == len(concepts), (
        f"Theme anchors must be distinct; got {[c.theme_anchor.value for c in concepts]}"
    )


@pytest.mark.parametrize("persona", ["mia", "garry_tan", "alex_chen", "sam_reyes"])
async def test_each_persona_produces_at_least_two_concepts(persona: str) -> None:
    """Smoke: every persona in the test suite must yield ≥2 distinct Concepts."""
    state, candidates = await _state_and_candidates(persona)
    concepts = generate_concepts_simple(state, candidates)
    assert len(concepts) >= 2, (
        f"{persona}: expected ≥2 Concepts, got {len(concepts)}"
    )
    assert len({c.theme_anchor for c in concepts}) == len(concepts), (
        f"{persona}: theme_anchors must be distinct"
    )
