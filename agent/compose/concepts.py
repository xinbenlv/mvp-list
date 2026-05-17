"""generate_concepts_simple — pure-function POC multi-plan seed generator.

Implements eng design §6 end-to-end:

  Step 1 — Theme selection (deterministic from intent + energy + chaos):
    - Mia-like (restore/slow_down in intent OR energy=low OR chaos=low|very_low)
        → [cultural_restorative, outdoor_exploratory, quiet_intimate]
    - Garry/Alex-like (energy=high AND explore in intent)
        → [social_high_energy, outdoor_exploratory, cultural_restorative]
    - Default mixed
        → [cultural_restorative, outdoor_exploratory, social_high_energy]

  Step 2 — Per-theme any-match vibe_tag filter:
    - cultural_restorative: {warm, slow, authentic, cultural, quiet}
    - outdoor_exploratory:  {outdoor, lively, walkable, spacious}
    - social_high_energy:   {lively, social, hip, cinematic}
    - quiet_intimate:       {intimate, quiet, romantic, slow, warm, low_noise}
        (relaxed per eng design §6: include warm + low_noise because the
         current 12-place demo set has zero places tagged
         `intimate` / `romantic` — without the relaxation Mia-like personas
         steady-state at N=2.)

  Step 3 — Anchor selection: top-2 places by fit_score within each filter.

  Step 4 — Drop-to-N-1: if a theme yields <2 viable candidates, drop it.
           If final N < 2, raise diagnostic.

  Step 5 — Build Concept objects with day_theme + arc_signature templated
           from theme + dominant emotional_intent.

No LLM, no I/O. Pure function — test in isolation.
"""

from __future__ import annotations

import hashlib

from agent.state import IntakeState
from agent.types import (
    ChaosTolerance,
    Concept,
    EmotionalRole,
    EnergyLevel,
    MoodTag,
    PacingRole,
    PlaceCandidate,
    ThemeAnchor,
    mood_tags_from_emotional_intent,
)

# ---------------------------------------------------------------------------
# Constants (§6 — keep in one place so tests can import + introspect)
# ---------------------------------------------------------------------------


# Per-theme any-match vibe_tag filter. Tag matches are case-sensitive string
# comparisons against `PlaceCandidate.composition.vibe_tags[i].tag`.
THEME_FILTERS: dict[ThemeAnchor, frozenset[str]] = {
    ThemeAnchor.CULTURAL_RESTORATIVE: frozenset(
        {"warm", "slow", "authentic", "cultural", "quiet"}
    ),
    ThemeAnchor.OUTDOOR_EXPLORATORY: frozenset(
        {"outdoor", "lively", "walkable", "spacious"}
    ),
    ThemeAnchor.SOCIAL_HIGH_ENERGY: frozenset(
        {"lively", "social", "hip", "cinematic"}
    ),
    ThemeAnchor.QUIET_INTIMATE: frozenset(
        # Relaxed per §6: warm + low_noise included because the 22-place demo
        # set has zero places tagged `intimate` / `romantic`.
        {"intimate", "quiet", "romantic", "slow", "warm", "low_noise"}
    ),
}

# Canonical 4-act pacing blueprint shared by every theme.
CANONICAL_PACING: list[PacingRole] = [
    PacingRole.OPENING,
    PacingRole.BREATHING,
    PacingRole.PEAK,
    PacingRole.CLOSING,
]

# Per-theme day-theme + arc-signature templates. `{intent_word}` is replaced
# by the dominant EmotionalRole's display word, in Chinese to match the
# Composer prompt's output language (eng design §6 + persona demo arcs).
_INTENT_WORD_ZH: dict[EmotionalRole, str] = {
    EmotionalRole.RESTORE: "慢恢复",
    EmotionalRole.SLOW_DOWN: "慢下来",
    EmotionalRole.RECONNECT: "重新连接",
    EmotionalRole.EXPLORE: "探索",
    EmotionalRole.CELEBRATE: "庆祝",
    EmotionalRole.FEEL_ALIVE: "活过来",
}

_THEME_LABEL_ZH: dict[ThemeAnchor, str] = {
    ThemeAnchor.CULTURAL_RESTORATIVE: "文化慢恢复",
    ThemeAnchor.OUTDOOR_EXPLORATORY: "户外轻探索",
    ThemeAnchor.SOCIAL_HIGH_ENERGY: "高能量社交",
    ThemeAnchor.QUIET_INTIMATE: "安静私密",
}

_THEME_ARC_ZH: dict[ThemeAnchor, str] = {
    ThemeAnchor.CULTURAL_RESTORATIVE: "慢起 → 自然恢复 → 烟火气 → 早收",
    ThemeAnchor.OUTDOOR_EXPLORATORY: "出门 → 走一段 → 高点眺望 → 慢慢回",
    ThemeAnchor.SOCIAL_HIGH_ENERGY: "暖身 → 街区穿梭 → 高潮聚餐 → 夜场收尾",
    ThemeAnchor.QUIET_INTIMATE: "安静起步 → 树下停留 → 一顿不用决定的饭 → 早归",
}

# Per-theme additional mood-tag bias. Mood tags derived from
# emotional_intent are unioned with these so the Concept's mood_tags reflect
# both "what the user wants" and "what shape of day this is".
_THEME_MOOD_BIAS: dict[ThemeAnchor, list[MoodTag]] = {
    ThemeAnchor.CULTURAL_RESTORATIVE: [MoodTag.RESTORATIVE, MoodTag.GROUNDING],
    ThemeAnchor.OUTDOOR_EXPLORATORY: [MoodTag.LIGHTLY_EXPLORATORY, MoodTag.NOT_RUSHED],
    ThemeAnchor.SOCIAL_HIGH_ENERGY: [MoodTag.ENERGIZING, MoodTag.SOCIAL],
    ThemeAnchor.QUIET_INTIMATE: [MoodTag.NOT_RUSHED, MoodTag.INTIMATE],
}


# ---------------------------------------------------------------------------
# Step 1 — theme selection
# ---------------------------------------------------------------------------


def select_themes(state: IntakeState) -> list[ThemeAnchor]:
    """Deterministic theme selection per §6 of the engineering design.

    Inputs:
      - state.emotional_intent.values   list[EmotionalRole]
      - state.energy_profile.energy_level.value   EnergyLevel | None
      - state.energy_profile.chaos_tolerance.value   ChaosTolerance | None

    Branching order:
      (a) Mia-like — restore OR slow_down in intent, OR energy_level=low,
          OR chaos_tolerance ∈ {low}. (We don't have `very_low` in the
          backend enum — Sam's `very_low` is coerced to LOW by the loader.)
          → [cultural_restorative, outdoor_exploratory, quiet_intimate]
      (b) Garry/Alex-like — energy_level=high AND explore in intent
          → [social_high_energy, outdoor_exploratory, cultural_restorative]
      (c) Default mixed
          → [cultural_restorative, outdoor_exploratory, social_high_energy]
    """
    intent_values = {v for v in state.emotional_intent.values}
    energy = state.energy_profile.energy_level.value
    chaos = state.energy_profile.chaos_tolerance.value

    mia_like = (
        EmotionalRole.RESTORE in intent_values
        or EmotionalRole.SLOW_DOWN in intent_values
        or energy == EnergyLevel.LOW
        or chaos == ChaosTolerance.LOW
    )

    explore_high = (
        energy == EnergyLevel.HIGH and EmotionalRole.EXPLORE in intent_values
    )

    # Branch order matters: Mia-like takes precedence over Garry/Alex-like
    # when both signals appear (e.g. someone who is high-energy + explore
    # AND also says "restore" — the restore signal dominates).
    if mia_like:
        return [
            ThemeAnchor.CULTURAL_RESTORATIVE,
            ThemeAnchor.OUTDOOR_EXPLORATORY,
            ThemeAnchor.QUIET_INTIMATE,
        ]
    if explore_high:
        return [
            ThemeAnchor.SOCIAL_HIGH_ENERGY,
            ThemeAnchor.OUTDOOR_EXPLORATORY,
            ThemeAnchor.CULTURAL_RESTORATIVE,
        ]
    return [
        ThemeAnchor.CULTURAL_RESTORATIVE,
        ThemeAnchor.OUTDOOR_EXPLORATORY,
        ThemeAnchor.SOCIAL_HIGH_ENERGY,
    ]


# ---------------------------------------------------------------------------
# Step 2 + 3 — filter candidates and pick top-2 anchors per theme
# ---------------------------------------------------------------------------


def _place_vibe_tag_set(candidate: PlaceCandidate) -> set[str]:
    """Return the set of vibe tag *names* on a candidate (strings only)."""
    tags = candidate.composition.get("vibe_tags") or []
    return {str(item.get("tag")) for item in tags if item.get("tag") is not None}


def filter_candidates_for_theme(
    theme: ThemeAnchor, candidates: list[PlaceCandidate]
) -> list[PlaceCandidate]:
    """Any-match filter against THEME_FILTERS[theme] on `composition.vibe_tags`."""
    accept = THEME_FILTERS[theme]
    out: list[PlaceCandidate] = []
    for c in candidates:
        if _place_vibe_tag_set(c) & accept:
            out.append(c)
    # Sort by fit_score desc — candidate list typically already arrives sorted
    # from `search_places`, but we re-sort defensively so callers can pass
    # arbitrary lists.
    out.sort(key=lambda c: c.fit_score, reverse=True)
    return out


# ---------------------------------------------------------------------------
# Step 5 — Build Concept objects
# ---------------------------------------------------------------------------


def _dominant_intent(state: IntakeState) -> EmotionalRole | None:
    """Pick the most relevant emotional_intent value for templating.

    Priority: first value whose role is in `_INTENT_WORD_ZH` (all 6 are), in
    insertion order. If the slot is empty, return None and templates fall
    back to a generic phrase.
    """
    for v in state.emotional_intent.values:
        if v in _INTENT_WORD_ZH:
            return v
    return None


def _concept_id(state: IntakeState, theme: ThemeAnchor) -> str:
    """Stable, persona-hash-suffixed concept id.

    POC has no `user_id`, so we hash the persona's emotional intent +
    avoidance values to get a deterministic short suffix per session.
    """
    persona_signal = "|".join(
        [
            ",".join(sorted(v.value for v in state.emotional_intent.values)),
            ",".join(sorted(v.value for v in state.avoidance.values)),
            str(state.energy_profile.energy_level.value),
            str(state.energy_profile.chaos_tolerance.value),
        ]
    )
    short = hashlib.md5(persona_signal.encode("utf-8")).hexdigest()[:6]
    return f"{theme.value}_{short}"


def _build_day_theme(theme: ThemeAnchor, intent: EmotionalRole | None) -> str:
    """Templated day_theme — Chinese, matches Composer prompt's output style."""
    theme_label = _THEME_LABEL_ZH[theme]
    intent_word = _INTENT_WORD_ZH.get(intent) if intent else None
    if intent_word:
        return f"{theme_label}的一天 · {intent_word}"
    return f"{theme_label}的一天"


def _build_mood_tags(state: IntakeState, theme: ThemeAnchor) -> list[MoodTag]:
    """Mood tags = intake-derived ∪ theme bias (de-duped, intake-first)."""
    base = mood_tags_from_emotional_intent(state.emotional_intent.values)
    out: list[MoodTag] = list(base)
    seen = set(out)
    for t in _THEME_MOOD_BIAS.get(theme, []):
        if t not in seen:
            out.append(t)
            seen.add(t)
    return out


def _build_emotional_thesis(
    theme: ThemeAnchor, anchors: list[PlaceCandidate]
) -> str:
    """1-line `emotional_thesis` template referencing the lead anchor."""
    theme_label = _THEME_LABEL_ZH[theme]
    if anchors:
        lead = anchors[0]
        return f"a {theme_label} version of today, anchored on {lead.name}"
    return f"a {theme_label} version of today"


def _build_concept(
    state: IntakeState, theme: ThemeAnchor, anchors: list[PlaceCandidate]
) -> Concept:
    dominant = _dominant_intent(state)
    return Concept(
        concept_id=_concept_id(state, theme),
        day_theme=_build_day_theme(theme, dominant),
        mood_tags=_build_mood_tags(state, theme),
        arc_signature=_THEME_ARC_ZH[theme],
        pacing_blueprint=list(CANONICAL_PACING),
        anchor_place_ids=[a.place_id for a in anchors],
        emotional_thesis=_build_emotional_thesis(theme, anchors),
        theme_anchor=theme,
    )


# ---------------------------------------------------------------------------
# Public entrypoint
# ---------------------------------------------------------------------------


class ConceptGenerationError(RuntimeError):
    """Raised when fewer than 2 themes survive filtering — diagnostic with
    per-theme remaining-candidate counts."""


def generate_concepts_simple(
    state: IntakeState,
    candidates: list[PlaceCandidate],
) -> list[Concept]:
    """Phase 2 (Phase 3b in the original eng design phase numbering): rule-
    based multi-plan seed generator.

    See module docstring for the algorithm. Returns 2–3 Concepts with
    distinct `theme_anchor`s. Raises `ConceptGenerationError` if the final
    list would have <2 concepts (eng design §6 hard stop — the caller
    should surface this to the user as "I couldn't build diverse enough
    options for today, can you tell me more about what you want?").
    """
    themes = select_themes(state)

    concepts: list[Concept] = []
    diagnostics: dict[ThemeAnchor, int] = {}
    for theme in themes:
        filtered = filter_candidates_for_theme(theme, candidates)
        diagnostics[theme] = len(filtered)
        if len(filtered) < 2:
            # Drop this theme. N falls 3 → 2.
            continue
        anchors = filtered[:2]
        concepts.append(_build_concept(state, theme, anchors))

    if len(concepts) < 2:
        details = ", ".join(
            f"{t.value}={n}" for t, n in diagnostics.items()
        )
        raise ConceptGenerationError(
            "generate_concepts_simple: fewer than 2 viable themes after "
            f"filtering. Per-theme candidate counts: {details}"
        )

    return concepts


__all__ = [
    "THEME_FILTERS",
    "CANONICAL_PACING",
    "ConceptGenerationError",
    "filter_candidates_for_theme",
    "generate_concepts_simple",
    "select_themes",
]
