"""generate_concepts_simple — pure-function POC multi-plan seed generator.

Phase 0 stub: returns two structurally distinct Concepts. The real rule-based
implementation lands in Phase 3b (eng design §6).
"""

from __future__ import annotations

from agent.state import IntakeState
from agent.types import (
    Concept,
    MoodTag,
    PacingRole,
    PlaceCandidate,
    ThemeAnchor,
)


def generate_concepts_simple(
    state: IntakeState,
    candidates: list[PlaceCandidate],
) -> list[Concept]:
    """Return 2 fake-but-structurally-valid Concepts (Phase 0 stub)."""
    canonical_arc = [
        PacingRole.OPENING,
        PacingRole.BREATHING,
        PacingRole.PEAK,
        PacingRole.CLOSING,
    ]
    anchor_ids = [c.place_id for c in candidates[:2]]
    return [
        Concept(
            concept_id="concept_a",
            day_theme="慢起恢复的一天",
            mood_tags=[MoodTag.RESTORATIVE, MoodTag.GROUNDING],
            arc_signature="慢起 → 自然恢复 → 烟火气 → 早收",
            pacing_blueprint=canonical_arc,
            anchor_place_ids=anchor_ids,
            emotional_thesis="围绕安静与温度展开。",
            theme_anchor=ThemeAnchor.CULTURAL_RESTORATIVE,
        ),
        Concept(
            concept_id="concept_b",
            day_theme="轻探索的一天",
            mood_tags=[MoodTag.LIGHTLY_EXPLORATORY, MoodTag.ENERGIZING],
            arc_signature="出门 → 走一段 → 高潮 → 慢慢回",
            pacing_blueprint=canonical_arc,
            anchor_place_ids=anchor_ids,
            emotional_thesis="走出门,看到一点新的东西。",
            theme_anchor=ThemeAnchor.OUTDOOR_EXPLORATORY,
        ),
    ]


__all__ = ["generate_concepts_simple"]
