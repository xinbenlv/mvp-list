"""IntakeState typed schema + pure-function stubs.

Source of truth: PRD §Interaction Layer §A. Phase 0 ships a minimal typed
shell so the stub flow type-checks; Phase 1a fills out the full slot ladder,
merge logic, router, and serializers.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from agent.types import (
    AvoidanceTag,
    ChaosTolerance,
    EmotionalRole,
    EnergyLevel,
    ExperienceRequest,
    RouterDecision,
    SocialFit,
    TasteSignature,
    VibeTag,
)

Provenance = Literal[
    "inferred_from_screenshots",
    "user_stated",
    "user_implied",
    "default",
]


class Slot[T](BaseModel):
    """Generic typed slot mirroring PRD §A `Slot<T>`."""

    values: list[T] = Field(default_factory=list)
    confidence: float = 0.0
    provenance: Provenance = "default"
    last_updated_turn: int = 0


class Turn(BaseModel):
    role: Literal["user", "agent"]
    text: str
    turn_index: int


class TasteSignatureSlot(BaseModel):
    value: TasteSignature = Field(default_factory=TasteSignature)
    confidence: float = 0.0
    provenance: Literal["inferred_from_screenshots"] = "inferred_from_screenshots"


class _ScalarSlot[T](BaseModel):
    value: T | None = None
    confidence: float = 0.0
    provenance: Provenance = "default"


class EnergyProfile(BaseModel):
    energy_level: _ScalarSlot[EnergyLevel] = Field(default_factory=_ScalarSlot)
    chaos_tolerance: _ScalarSlot[ChaosTolerance] = Field(default_factory=_ScalarSlot)
    last_updated_turn: int = 0


class PracticalConstraints(BaseModel):
    date: _ScalarSlot[str] = Field(default_factory=_ScalarSlot)
    time_window: _ScalarSlot[str] = Field(default_factory=_ScalarSlot)
    start_location: _ScalarSlot[str] = Field(default_factory=_ScalarSlot)
    transport: _ScalarSlot[str] = Field(default_factory=_ScalarSlot)
    max_drive_minutes: _ScalarSlot[int] = Field(default_factory=_ScalarSlot)
    budget: _ScalarSlot[str] = Field(default_factory=_ScalarSlot)
    kid_friendly: _ScalarSlot[bool] = Field(default_factory=_ScalarSlot)
    needs_parking: _ScalarSlot[bool] = Field(default_factory=_ScalarSlot)
    last_updated_turn: int = 0


class TasteAnchors(BaseModel):
    desired_vibe: Slot[VibeTag] = Field(default_factory=Slot[VibeTag])
    food_preferences: Slot[str] = Field(default_factory=Slot[str])
    last_updated_turn: int = 0


class IntakeState(BaseModel):
    """Typed conversation state (PRD §A)."""

    taste_signature: TasteSignatureSlot = Field(default_factory=TasteSignatureSlot)
    emotional_intent: Slot[EmotionalRole] = Field(default_factory=Slot[EmotionalRole])
    social_config: Slot[SocialFit] = Field(default_factory=Slot[SocialFit])
    energy_profile: EnergyProfile = Field(default_factory=EnergyProfile)
    practical_constraints: PracticalConstraints = Field(default_factory=PracticalConstraints)
    taste_anchors: TasteAnchors = Field(default_factory=TasteAnchors)
    avoidance: Slot[AvoidanceTag] = Field(default_factory=Slot[AvoidanceTag])

    turn_count: int = 0
    transcript: list[Turn] = Field(default_factory=list)
    stopped_reason: Literal["hard_cap", "sufficient_info", "user_escape"] | None = None


# ---------------------------------------------------------------------------
# Pure-function stubs (real implementations in Phase 1a)
# ---------------------------------------------------------------------------


def merge_slot_updates(state: IntakeState, updates: dict[str, Any]) -> IntakeState:
    """Phase 1a — confidence-max merge + provenance ladder upgrade."""
    # Phase 0 stub: return state unchanged so the smoke flow is happy.
    return state


def router(state: IntakeState) -> RouterDecision:
    """Phase 1a — implements PRD §3 deterministic stopping rule.

    Phase 0 stub: always return READY so the smoke run skips the intake loop.
    """
    return "READY"


def serialize_to_experience_request(state: IntakeState) -> ExperienceRequest:
    """Phase 1a — handles the 3 alignment bugs from PRD §B."""
    return ExperienceRequest(
        trip_context={},
        experience_intent={},
        constraints={"stop_count_target": 4},
        taste_context={"taste_signature": state.taste_signature.value.model_dump()},
    )


class ComposerInput(BaseModel):
    """Loose shape the Composer prompt's `Input:` block expects.

    Phase 1a fills this out per the field-mapping table in Implement-poc.md.
    """

    taste_signature: dict[str, Any] = Field(default_factory=dict)
    emotional_intent: dict[str, Any] = Field(default_factory=dict)
    energy_profile: dict[str, Any] = Field(default_factory=dict)
    taste_anchors: dict[str, Any] = Field(default_factory=dict)
    social_config: dict[str, Any] = Field(default_factory=dict)
    practical_constraints: dict[str, Any] = Field(default_factory=dict)
    avoidance: dict[str, Any] = Field(default_factory=dict)


def serialize_for_composer(state: IntakeState) -> ComposerInput:
    """Phase 1a — flatten typed IntakeState into Composer prompt input shape."""
    return ComposerInput(
        taste_signature={
            "vibe_weights": [
                vw.model_dump() for vw in state.taste_signature.value.vibe_weights
            ],
            "summary": state.taste_signature.value.summary,
        },
        emotional_intent={
            "values": [v.value for v in state.emotional_intent.values],
            "rationale": "",
        },
        energy_profile={"novelty_appetite": "medium"},
        taste_anchors={"liked_examples": []},
        social_config={"values": [v.value for v in state.social_config.values]},
        practical_constraints={},
        avoidance={
            "values": [v.value for v in state.avoidance.values],
            "rationale": "",
        },
    )


__all__ = [
    "Provenance",
    "Slot",
    "Turn",
    "TasteSignatureSlot",
    "EnergyProfile",
    "PracticalConstraints",
    "TasteAnchors",
    "IntakeState",
    "ComposerInput",
    "merge_slot_updates",
    "router",
    "serialize_to_experience_request",
    "serialize_for_composer",
]
