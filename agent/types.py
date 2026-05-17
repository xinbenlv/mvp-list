"""Pydantic mirrors of backend schema controlled vocabs + agent-only types.

References:
- backend-data-schema-v2.md §2.0 (controlled vocab)
- backend-data-schema-v2.md §2.5–2.9 (TasteSignature, ExperienceRequest, etc.)
- agent-engineering-design.md §7 (Concept, EnrichedContext, ProposalSet)

Phase 0 scaffold: minimum surface area to make the stub flow type-check and run.
Full field-by-field mirroring happens in Phase 1a.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Controlled vocabulary enums (mirror backend-data-schema-v2.md §2.0)
# ---------------------------------------------------------------------------


class VibeTag(StrEnum):
    QUIET = "quiet"
    LIVELY = "lively"
    CINEMATIC = "cinematic"
    WARM = "warm"
    COOL = "cool"
    CULTURAL = "cultural"
    HISTORIC = "historic"
    NATURAL = "natural"
    URBAN = "urban"
    INDUSTRIAL = "industrial"
    INTIMATE = "intimate"
    SOCIAL = "social"
    ROMANTIC = "romantic"
    FAMILY = "family"
    SLOW = "slow"
    FAST = "fast"
    POLISHED = "polished"
    RUSTIC = "rustic"
    GRITTY = "gritty"
    LOW_STIMULATION = "low_stimulation"
    HIGH_STIMULATION = "high_stimulation"
    NOVELTY = "novelty"
    FAMILIAR = "familiar"
    INDOOR = "indoor"
    OUTDOOR = "outdoor"
    SCENIC = "scenic"
    HIDDEN_GEM = "hidden_gem"
    CASUAL = "casual"
    UPSCALE = "upscale"
    AUTHENTIC = "authentic"  # Used in some places lists; tolerated as alias.
    WALKABLE = "walkable"
    SPACIOUS = "spacious"
    HIP = "hip"
    LOW_NOISE = "low_noise"


class MoodTag(StrEnum):
    REFLECTIVE = "reflective"
    RESTORATIVE = "restorative"
    CELEBRATORY = "celebratory"
    LIGHTLY_EXPLORATORY = "lightly_exploratory"
    DEEPLY_EXPLORATORY = "deeply_exploratory"
    WARM = "warm"
    INTIMATE = "intimate"
    SOCIAL = "social"
    PLAYFUL = "playful"
    NOT_RUSHED = "not_rushed"
    ENERGIZING = "energizing"
    GROUNDING = "grounding"


class PacingRole(StrEnum):
    OPENING = "opening"
    BREATHING = "breathing"
    PEAK = "peak"
    RECOVERY = "recovery"
    CLOSING = "closing"


class EmotionalRole(StrEnum):
    RESTORE = "restore"
    EXPLORE = "explore"
    CELEBRATE = "celebrate"
    RECONNECT = "reconnect"
    SLOW_DOWN = "slow_down"
    FEEL_ALIVE = "feel_alive"


class SocialFit(StrEnum):
    SOLO = "solo"
    COUPLE = "couple"
    FAMILY_WITH_BABY = "family_with_baby"
    FAMILY_WITH_KIDS = "family_with_kids"
    FRIENDS_SMALL_GROUP = "friends_small_group"
    FRIENDS_LARGE_GROUP = "friends_large_group"
    PARENTS_VISITING = "parents_visiting"
    BUSINESS_CASUAL = "business_casual"


class EnergyLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ChaosTolerance(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AvoidanceTag(StrEnum):
    TOURISTY = "touristy"
    OVERCROWDED = "overcrowded"
    LOUD = "loud"
    QUEUED = "queued"
    RUSHED = "rushed"
    TIRED_CLASSIC = "tired_classic"
    INSTAGRAM_BAIT = "instagram_bait"
    HARD_PARKING = "hard_parking"
    RESERVATION_REQUIRED = "reservation_required"
    LONG_DRIVE = "long_drive"
    KID_UNFRIENDLY = "kid_unfriendly"
    STROLLER_UNFRIENDLY = "stroller_unfriendly"


class ThemeAnchor(StrEnum):
    """POC theme axes used by generate_concepts_simple to drive structural diversity."""

    CULTURAL_RESTORATIVE = "cultural_restorative"
    OUTDOOR_EXPLORATORY = "outdoor_exploratory"
    SOCIAL_HIGH_ENERGY = "social_high_energy"
    QUIET_INTIMATE = "quiet_intimate"


# ---------------------------------------------------------------------------
# Backend-mirror types (minimal Phase 0 surface; full schema lands in Phase 1a)
# ---------------------------------------------------------------------------


class VibeWeight(BaseModel):
    tag: VibeTag
    weight: float = Field(ge=0.0, le=1.0)


class TasteSignature(BaseModel):
    """Phase 0 stub — see backend §2.5 for full type."""

    vibe_weights: list[VibeWeight] = Field(default_factory=list)
    summary: str = ""
    confidence: float = 0.0


class ExperienceRequest(BaseModel):
    """Phase 0 stub — see backend §2.6 for full type."""

    trip_context: dict[str, Any] = Field(default_factory=dict)
    experience_intent: dict[str, Any] = Field(default_factory=dict)
    constraints: dict[str, Any] = Field(default_factory=dict)
    taste_context: dict[str, Any] = Field(default_factory=dict)


class PlaceCandidate(BaseModel):
    """Phase 0 stub — see backend §2.7 for full type."""

    place_id: str
    name: str
    fit_score: float = 0.0
    fit_reason: str = ""
    composition: dict[str, Any] = Field(default_factory=dict)
    restaurant: dict[str, Any] | None = None


# ---------------------------------------------------------------------------
# Agent-only types
# ---------------------------------------------------------------------------


class Concept(BaseModel):
    """A single seed used to drive one PlanComposer call (eng design §7)."""

    concept_id: str
    day_theme: str
    mood_tags: list[MoodTag] = Field(default_factory=list)
    arc_signature: str = ""
    pacing_blueprint: list[PacingRole] = Field(default_factory=list)
    anchor_place_ids: list[str] = Field(default_factory=list)
    emotional_thesis: str = ""
    theme_anchor: ThemeAnchor


class PlanResult(BaseModel):
    """Composer output wrapper (eng design Phase 3a)."""

    markdown: str
    day_theme: str
    pitch: str
    theme_anchor: ThemeAnchor
    stop_place_ids: list[str] = Field(default_factory=list)
    raw_metadata: dict[str, Any] = Field(default_factory=dict)


class CritiqueResult(BaseModel):
    """Phase 5 Critic output (scaffold only — body deferred)."""

    plan_id: str
    scores: dict[str, float] = Field(default_factory=dict)
    retry_recommended: bool = False
    notes: str = ""


# Router decision codomain
RouterDecision = Literal["ASK", "READY", "STOP_HARD_CAP"]


__all__ = [
    "VibeTag",
    "MoodTag",
    "PacingRole",
    "EmotionalRole",
    "SocialFit",
    "EnergyLevel",
    "ChaosTolerance",
    "AvoidanceTag",
    "ThemeAnchor",
    "VibeWeight",
    "TasteSignature",
    "ExperienceRequest",
    "PlaceCandidate",
    "Concept",
    "PlanResult",
    "CritiqueResult",
    "RouterDecision",
]
