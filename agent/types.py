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


class NoveltyLevel(StrEnum):
    """Novelty appetite axis.

    NOTE — ALIGNMENT-BUG-1 (PRD §B alignment-bugs): backend schema §2.6 types
    `taste_context.novelty_level` as `EnergyLevel` (low/medium/high). That is
    a name collision (energy != novelty). We define the *semantic* enum here
    on the agent side, but on serialize we fall back to writing the matching
    EnergyLevel string into `taste_context.novelty_level` so backend round-
    trips. Once backend schema is fixed (NoveltyLevel as `familiar | balanced |
    novelty_seeking`), serialize_to_experience_request will switch over.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


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
    """Phase 2 — mirrors backend schema §2.7 PlaceCandidate, slimmed to the
    fields the Composer prompt actually reads.

    Optional fields are nullable so the Phase 0 fake stubs and Phase 2 mock
    backend can both populate this shape without churn. Future Phase 4 wires
    the real backend HTTP response into the same fields.
    """

    place_id: str
    name: str
    place_type: str | None = None
    city: str | None = None
    address: str | None = None
    hours_note: str | None = None
    fit_score: float = 0.0
    fit_reason: str = ""
    composition: dict[str, Any] = Field(default_factory=dict)
    logistics: dict[str, Any] = Field(default_factory=dict)
    narrative_hook: str | None = None
    restaurant: dict[str, Any] | None = None
    hero_image_url: str | None = None


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


class BookingLink(BaseModel):
    """Booking link mirroring frontend Logistics.booking_links entries.

    Frontend tolerates either a bare URL string OR a `{label, url}` dict; we
    standardize on the dict form so JSON output is consistent.
    """

    label: str
    url: str


class Logistics(BaseModel):
    """Per-stop logistics, mirrors frontend `Logistics` in trip-plan.ts.

    `raw` is the pre-formatted human-readable line with emoji ("🚗 22min · 🅿️
    free · …"). All other fields are nullable since not every stop surfaces
    every detail.
    """

    raw: str = ""
    drive_time_min: int | None = None
    parking: str | None = None
    kid_friendly: bool | None = None
    reservation_note: str | None = None
    booking_links: list[BookingLink] = Field(default_factory=list)
    transit_estimate_usd: float | None = None


class OrderRecs(BaseModel):
    """Per-restaurant ordering recommendations, mirrors frontend `OrderRecs`.

    Set to None on `Stop` for non-restaurant stops.
    """

    menu_listed: list[str] = Field(default_factory=list)
    bold_picks: list[str] = Field(default_factory=list)
    logic_text: str = ""


class Stop(BaseModel):
    """Per-stop structured payload, mirrors frontend `Stop` in trip-plan.ts.

    Composer LLM emits this directly inside the PLAN_META sidecar so we can
    avoid fragile markdown parsing downstream. `image_url` is optional —
    Composer doesn't source images today; frontend renders gradient fallbacks
    when null.
    """

    stop_index: int
    time: str = ""
    place_id: str = ""
    place_name: str = ""
    one_liner: str = ""
    why_fits_today: str = ""
    logistics: Logistics = Field(default_factory=Logistics)
    order_recommendations: OrderRecs | None = None
    tip: str | None = None
    transition_to_next: str | None = None
    transition_drive_min: int | None = None
    image_url: str | None = None


class PlanResult(BaseModel):
    """Composer output wrapper (eng design Phase 3a).

    `markdown` is the user-facing plan (the wrapper strips the PLAN_META
    sidecar comment before storing). The rest of the fields are parsed
    metadata used by Phase 3b's diversity check + downstream rendering.

    `stops` carries the per-stop structured payload the Composer LLM now
    emits directly in PLAN_META (so the frontend transformer doesn't have to
    re-parse markdown). May be empty when the LLM is in stub mode or when
    the sidecar omitted it.
    """

    markdown: str
    day_theme: str
    pitch: str = ""
    theme_anchor: ThemeAnchor
    mood_tags: list[str] = Field(default_factory=list)
    emotional_arc: list[str] = Field(default_factory=list)
    stop_place_ids: list[str] = Field(default_factory=list)
    stop_names: list[str] = Field(default_factory=list)
    stops: list[Stop] = Field(default_factory=list)
    adaptive_branches: list[dict[str, str]] = Field(default_factory=list)
    composer_note: str = ""
    raw_metadata: dict[str, Any] = Field(default_factory=dict)


class CritiqueResult(BaseModel):
    """Phase 5 Critic output (scaffold only — body deferred)."""

    plan_id: str
    scores: dict[str, float] = Field(default_factory=dict)
    retry_recommended: bool = False
    notes: str = ""


# Router decision codomain
RouterDecision = Literal["ASK", "READY", "STOP_HARD_CAP"]


# ---------------------------------------------------------------------------
# ComposerInput — loose schema the Composer prompt's `Input` block reads.
# See poc-demo/composer_prompt.md "## Input (you will receive)" for the
# canonical shape we mirror here.
# ---------------------------------------------------------------------------


class ComposerVibeWeight(BaseModel):
    """Flat (tag, weight) pair the Composer reads — `tag` is a free string
    because TasteSignature.vibe_weights may carry tags outside the controlled
    VibeTag vocab (persona JSONs use 'restorative', 'natural_light', 'novel',
    etc. that are not in VibeTag). The Composer prompt accepts any string."""

    tag: str
    weight: float = Field(ge=0.0, le=1.0)


class ComposerTasteSignature(BaseModel):
    vibe_weights: list[ComposerVibeWeight] = Field(default_factory=list)
    summary: str = ""


class ComposerEmotionalIntent(BaseModel):
    values: list[str] = Field(default_factory=list)
    rationale: str = ""


class ComposerSocialConfig(BaseModel):
    values: list[str] = Field(default_factory=list)
    rationale: str = ""


class ComposerEnergyProfile(BaseModel):
    energy_level: str | None = None
    chaos_tolerance: str | None = None
    novelty_appetite: str = "medium"


class ComposerPracticalConstraints(BaseModel):
    start_location: str | None = None
    max_drive_minutes: int | None = None
    time_window: str | None = None
    kid_friendly_required: bool | None = None
    needs_parking: bool | None = None
    budget: str | None = None
    transport: str | None = None


class ComposerLikedExample(BaseModel):
    name: str
    why_i_like_it: str = ""


class ComposerTasteAnchors(BaseModel):
    liked_examples: list[ComposerLikedExample] = Field(default_factory=list)
    food_preferences: list[str] = Field(default_factory=list)


class ComposerAvoidance(BaseModel):
    values: list[str] = Field(default_factory=list)
    rationale: str = ""


class ComposerInput(BaseModel):
    """Bridge type — flat shape that matches the Composer prompt's `Input`
    JSON block. Built by `state.serialize_for_composer(IntakeState)`.

    Codex flagged this as a missing bridge: the typed IntakeState (slot-based)
    cannot be fed directly to the Composer prompt because the prompt reads a
    *flattened* schema (vibe_weights as a flat list, energy_profile with
    novelty_appetite, etc.). This type owns the mapping.
    """

    taste_signature: ComposerTasteSignature = Field(default_factory=ComposerTasteSignature)
    emotional_intent: ComposerEmotionalIntent = Field(default_factory=ComposerEmotionalIntent)
    social_config: ComposerSocialConfig = Field(default_factory=ComposerSocialConfig)
    energy_profile: ComposerEnergyProfile = Field(default_factory=ComposerEnergyProfile)
    practical_constraints: ComposerPracticalConstraints = Field(
        default_factory=ComposerPracticalConstraints
    )
    taste_anchors: ComposerTasteAnchors = Field(default_factory=ComposerTasteAnchors)
    avoidance: ComposerAvoidance = Field(default_factory=ComposerAvoidance)


# ---------------------------------------------------------------------------
# EmotionalRole -> MoodTag mapping (ALIGNMENT-BUG-3 helper).
# Backend has BOTH MoodTag (TripPlan.mood_tags) and EmotionalRole
# (ExperienceRequest.experience_intent.primary_mood AND Place.composition.
# emotional_roles). No owner has yet published a canonical mapping table.
# This function is the agent-side mapping, documented inline so the friend
# on backend can replace it with the canonical table later.
#
# The mapping below is "rough but covers all 6 EmotionalRoles":
#   restore       -> reflective, restorative
#   slow_down     -> not_rushed, grounding
#   reconnect     -> warm, intimate
#   explore       -> lightly_exploratory
#   celebrate     -> celebratory, social
#   feel_alive    -> energizing, playful
# Test_state.py asserts every EmotionalRole produces at least one MoodTag.
# ---------------------------------------------------------------------------


def mood_tags_from_emotional_intent(roles: list[EmotionalRole]) -> list[MoodTag]:
    """Map EmotionalRole[] -> deduplicated MoodTag[].

    See block comment above for the mapping table and rationale. This is
    ALIGNMENT-BUG-3 from PRD §B — agent-side mapping until backend owns one.
    """
    table: dict[EmotionalRole, list[MoodTag]] = {
        EmotionalRole.RESTORE: [MoodTag.REFLECTIVE, MoodTag.RESTORATIVE],
        EmotionalRole.SLOW_DOWN: [MoodTag.NOT_RUSHED, MoodTag.GROUNDING],
        EmotionalRole.RECONNECT: [MoodTag.WARM, MoodTag.INTIMATE],
        EmotionalRole.EXPLORE: [MoodTag.LIGHTLY_EXPLORATORY],
        EmotionalRole.CELEBRATE: [MoodTag.CELEBRATORY, MoodTag.SOCIAL],
        EmotionalRole.FEEL_ALIVE: [MoodTag.ENERGIZING, MoodTag.PLAYFUL],
    }
    out: list[MoodTag] = []
    seen: set[MoodTag] = set()
    for r in roles:
        for tag in table.get(r, []):
            if tag not in seen:
                seen.add(tag)
                out.append(tag)
    return out


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
    "NoveltyLevel",
    "VibeWeight",
    "TasteSignature",
    "ExperienceRequest",
    "PlaceCandidate",
    "Concept",
    "BookingLink",
    "Logistics",
    "OrderRecs",
    "Stop",
    "PlanResult",
    "CritiqueResult",
    "RouterDecision",
    "ComposerVibeWeight",
    "ComposerTasteSignature",
    "ComposerEmotionalIntent",
    "ComposerSocialConfig",
    "ComposerEnergyProfile",
    "ComposerPracticalConstraints",
    "ComposerLikedExample",
    "ComposerTasteAnchors",
    "ComposerAvoidance",
    "ComposerInput",
    "mood_tags_from_emotional_intent",
]
