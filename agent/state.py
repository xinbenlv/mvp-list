"""IntakeState typed schema + pure-function implementations.

Source of truth: PRD §Interaction Layer §A. Phase 1a fills out the slot
ladder, merge logic, router, and serializers (no LLM — pure Python).

Three alignment bugs from PRD §B are handled in `serialize_to_experience_request`
and helpers in `agent.types`; see ALIGNMENT-BUG-{1,2,3} markers below.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from agent.types import (
    AvoidanceTag,
    ChaosTolerance,
    ComposerAvoidance,
    ComposerEmotionalIntent,
    ComposerEnergyProfile,
    ComposerInput,
    ComposerLikedExample,
    ComposerPracticalConstraints,
    ComposerSocialConfig,
    ComposerTasteAnchors,
    ComposerTasteSignature,
    ComposerVibeWeight,
    EmotionalRole,
    EnergyLevel,
    ExperienceRequest,
    NoveltyLevel,
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

# Provenance ladder (low -> high). Used by `merge_slot_updates` to ensure we
# only ever *upgrade* provenance, never downgrade.
_PROVENANCE_RANK: dict[str, int] = {
    "default": 0,
    "user_implied": 1,
    "user_stated": 2,
    "inferred_from_screenshots": 3,
}


# ---------------------------------------------------------------------------
# Typed sub-slots
# ---------------------------------------------------------------------------


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
    # ALIGNMENT-BUG-1 (PRD §B alignment bugs): backend schema §2.6 types
    # `taste_context.novelty_level` as EnergyLevel which is a name collision.
    # We model `novelty_appetite` here on the agent side as NoveltyLevel
    # (semantic enum) and write it through to backend with the matching
    # EnergyLevel string until backend ships a real NoveltyLevel enum.
    novelty_appetite: _ScalarSlot[NoveltyLevel] = Field(default_factory=_ScalarSlot)
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


class TasteAnchor(BaseModel):
    """One entry in `taste_anchors.liked_examples` (persona-fixture shape)."""

    name: str
    why_i_like_it: str = ""


class TasteAnchors(BaseModel):
    # `desired_vibe` mirrors PRD §A; carries VibeTag slot (controlled vocab).
    desired_vibe: Slot[VibeTag] = Field(default_factory=Slot[VibeTag])
    food_preferences: Slot[str] = Field(default_factory=Slot[str])
    # `liked_examples` is what personas actually carry; we model it as a
    # separate slot so `serialize_for_composer` can pipe it through unchanged.
    liked_examples: list[TasteAnchor] = Field(default_factory=list)
    last_updated_turn: int = 0


# ---------------------------------------------------------------------------
# IntakeState
# ---------------------------------------------------------------------------


class IntakeState(BaseModel):
    """Typed conversation state (PRD §A)."""

    taste_signature: TasteSignatureSlot = Field(default_factory=TasteSignatureSlot)
    emotional_intent: Slot[EmotionalRole] = Field(default_factory=Slot[EmotionalRole])
    # `emotional_intent.rationale` is not modeled in PRD §A but personas carry
    # it and Composer wants it. We keep it on the side here.
    emotional_intent_rationale: str = ""

    social_config: Slot[SocialFit] = Field(default_factory=Slot[SocialFit])
    social_config_rationale: str = ""

    energy_profile: EnergyProfile = Field(default_factory=EnergyProfile)
    practical_constraints: PracticalConstraints = Field(default_factory=PracticalConstraints)
    taste_anchors: TasteAnchors = Field(default_factory=TasteAnchors)
    avoidance: Slot[AvoidanceTag] = Field(default_factory=Slot[AvoidanceTag])
    avoidance_rationale: str = ""

    turn_count: int = 0
    transcript: list[Turn] = Field(default_factory=list)
    stopped_reason: Literal["hard_cap", "sufficient_info", "user_escape"] | None = None


# ---------------------------------------------------------------------------
# merge_slot_updates
# ---------------------------------------------------------------------------


def _merge_into_slot(slot: dict[str, Any], new: dict[str, Any], turn_count: int) -> dict[str, Any]:
    """Merge a single slot dict (kind: `Slot[T]` or `_ScalarSlot[T]`).

    Rule (per task spec + PRD): take new value IF new confidence > existing
    confidence; otherwise keep existing. Provenance upgrades along the ladder.
    """
    new_confidence = float(new.get("confidence", 0.0))
    old_confidence = float(slot.get("confidence", 0.0))

    if new_confidence > old_confidence:
        # Overwrite values / value.
        if "values" in new:
            slot["values"] = list(new["values"])
        if "value" in new:
            slot["value"] = new["value"]
        slot["confidence"] = new_confidence
        # Provenance upgrades to whichever is higher on the ladder.
        old_prov = slot.get("provenance", "default")
        new_prov = new.get("provenance", "default")
        if _PROVENANCE_RANK.get(new_prov, 0) >= _PROVENANCE_RANK.get(old_prov, 0):
            slot["provenance"] = new_prov
        slot["last_updated_turn"] = turn_count
    return slot


def merge_slot_updates(state: IntakeState, updates: dict[str, Any]) -> IntakeState:
    """Phase 1a — confidence-max merge + provenance ladder upgrade.

    `updates` shape: per-slot dict keyed by IntakeState attribute name. Examples:
        {
          "emotional_intent": {"values": ["restore"], "confidence": 0.8,
                               "provenance": "user_stated"},
          "energy_profile": {
              "energy_level": {"value": "low", "confidence": 0.7,
                               "provenance": "user_stated"},
          },
        }

    Composite slots (energy_profile, practical_constraints, taste_anchors)
    merge each sub-field independently (per-field confidence-max).

    Returns a NEW IntakeState (pydantic immutable copy via .model_dump round
    trip). `turn_count` is incremented exactly once.
    """
    data = state.model_dump()
    new_turn = data["turn_count"] + 1
    data["turn_count"] = new_turn

    # Top-level `Slot[T]` fields:
    for key in ("emotional_intent", "social_config", "avoidance"):
        if key in updates:
            data[key] = _merge_into_slot(dict(data[key]), updates[key], new_turn)

    # Top-level TasteSignatureSlot (single value with confidence):
    if "taste_signature" in updates:
        ts = dict(data["taste_signature"])
        new = updates["taste_signature"]
        if float(new.get("confidence", 0.0)) > float(ts.get("confidence", 0.0)):
            if "value" in new:
                ts["value"] = new["value"]
            ts["confidence"] = float(new["confidence"])
        data["taste_signature"] = ts

    # Composite: energy_profile (per-sub-field merge)
    if "energy_profile" in updates:
        ep = dict(data["energy_profile"])
        upd_ep = updates["energy_profile"]
        for sub in ("energy_level", "chaos_tolerance", "novelty_appetite"):
            if sub in upd_ep:
                ep[sub] = _merge_into_slot(dict(ep[sub]), upd_ep[sub], new_turn)
        ep["last_updated_turn"] = new_turn
        data["energy_profile"] = ep

    # Composite: practical_constraints (per-sub-field merge)
    if "practical_constraints" in updates:
        pc = dict(data["practical_constraints"])
        upd_pc = updates["practical_constraints"]
        for sub in (
            "date",
            "time_window",
            "start_location",
            "transport",
            "max_drive_minutes",
            "budget",
            "kid_friendly",
            "needs_parking",
        ):
            if sub in upd_pc:
                pc[sub] = _merge_into_slot(dict(pc[sub]), upd_pc[sub], new_turn)
        pc["last_updated_turn"] = new_turn
        data["practical_constraints"] = pc

    # Composite: taste_anchors (slot sub-fields + pass-through liked_examples)
    if "taste_anchors" in updates:
        ta = dict(data["taste_anchors"])
        upd_ta = updates["taste_anchors"]
        for sub in ("desired_vibe", "food_preferences"):
            if sub in upd_ta:
                ta[sub] = _merge_into_slot(dict(ta[sub]), upd_ta[sub], new_turn)
        if "liked_examples" in upd_ta:
            # Replace wholesale — caller owns dedup. Provenance not modeled for
            # this sub-field; the Composer just wants a list.
            ta["liked_examples"] = list(upd_ta["liked_examples"])
        ta["last_updated_turn"] = new_turn
        data["taste_anchors"] = ta

    # Pass-through rationales / bookkeeping
    for key in ("emotional_intent_rationale", "social_config_rationale", "avoidance_rationale"):
        if key in updates:
            data[key] = str(updates[key])
    if "stopped_reason" in updates:
        data["stopped_reason"] = updates["stopped_reason"]

    return IntakeState.model_validate(data)


# ---------------------------------------------------------------------------
# router
# ---------------------------------------------------------------------------


def _confidence_vector(state: IntakeState) -> list[float]:
    """Confidence across the 6 ontology dims (PRD §3 stopping rule input).

    Dim list (matching PRD §A):
      0 taste_signature (vision)
      1 emotional_intent
      2 social_config
      3 energy_profile (avg of energy_level + chaos_tolerance)
      4 practical_constraints (avg of the populated sub-slots; 0 if none)
      5 taste_anchors.desired_vibe + avoidance combined (avg)
    """
    energy_pair = [
        state.energy_profile.energy_level.confidence,
        state.energy_profile.chaos_tolerance.confidence,
    ]
    energy_avg = sum(energy_pair) / len(energy_pair) if energy_pair else 0.0

    pc = state.practical_constraints
    pc_subs = [
        pc.date.confidence,
        pc.time_window.confidence,
        pc.start_location.confidence,
        pc.transport.confidence,
        pc.max_drive_minutes.confidence,
        pc.budget.confidence,
        pc.kid_friendly.confidence,
        pc.needs_parking.confidence,
    ]
    pc_avg = sum(pc_subs) / len(pc_subs) if pc_subs else 0.0

    anchors_avg = (
        state.taste_anchors.desired_vibe.confidence + state.avoidance.confidence
    ) / 2.0

    return [
        state.taste_signature.confidence,
        state.emotional_intent.confidence,
        state.social_config.confidence,
        energy_avg,
        pc_avg,
        anchors_avg,
    ]


def router(state: IntakeState) -> RouterDecision:
    """Phase 1a — implements PRD §3 deterministic stopping rule.

    Returns one of: "ASK", "READY", "STOP_HARD_CAP".

    Order of checks (matches PRD §3):
      1. turn_count >= 10                              -> STOP_HARD_CAP
      2. stopped_reason == "user_escape" (user said    -> READY
         "好了 / 直接给我看 plan / done"; in Phase 1b
         the orchestrator sets this on user intent)
      3. avg(confidence_i) >= 0.8 AND min >= 0.5       -> READY
      4. else                                           -> ASK

    NOTE: task spec used the symbol `state.user_explicit_done`; we adopt the
    PRD's existing `stopped_reason == "user_escape"` instead (same semantic,
    no new field needed). Phase 0 IntakeState already carries this slot.
    """
    if state.turn_count >= 10:
        return "STOP_HARD_CAP"
    if state.stopped_reason == "user_escape":
        return "READY"
    confidences = _confidence_vector(state)
    if not confidences:
        return "ASK"
    avg_c = sum(confidences) / len(confidences)
    min_c = min(confidences)
    if avg_c >= 0.8 and min_c >= 0.5:
        return "READY"
    return "ASK"


# ---------------------------------------------------------------------------
# serialize_to_experience_request
# ---------------------------------------------------------------------------


def serialize_to_experience_request(state: IntakeState) -> ExperienceRequest:
    """Map IntakeState -> backend ExperienceRequest (schema §2.6).

    Handles the 3 alignment bugs from PRD §B inline.
    """
    pc = state.practical_constraints

    trip_context: dict[str, Any] = {
        "date": pc.date.value,
        "time_window": pc.time_window.value,
        "start_location": pc.start_location.value,
        "companions": [v for v in state.social_config.values],
        "transport": pc.transport.value,
    }

    # ALIGNMENT-BUG-2 (PRD §B): backend calls this `primary_mood`, agent
    # IntakeState calls it `emotional_intent`. We adopt backend's name on
    # the wire so this is the one source of truth for serialize output.
    experience_intent: dict[str, Any] = {
        "primary_mood": [v for v in state.emotional_intent.values],
        "desired_vibe": [v for v in state.taste_anchors.desired_vibe.values],
        "avoid": [v for v in state.avoidance.values],
    }

    constraints: dict[str, Any] = {
        "max_drive_minutes": pc.max_drive_minutes.value,
        "kid_friendly": pc.kid_friendly.value,
        "needs_parking": pc.needs_parking.value,
        "budget": pc.budget.value,
        "energy_level": state.energy_profile.energy_level.value,
        "chaos_tolerance": state.energy_profile.chaos_tolerance.value,
        "stop_count_target": 4,
    }

    # ALIGNMENT-BUG-1 (PRD §B): backend types `taste_context.novelty_level`
    # as EnergyLevel (low|medium|high). We carry novelty_appetite on
    # IntakeState.energy_profile (NoveltyLevel: low|medium|high — same string
    # values), so we write through directly. If the value is unset, we omit
    # the key rather than guessing — backend's schema marks it optional.
    # TODO(backend): introduce NoveltyLevel enum (familiar/balanced/
    # novelty_seeking) so the type matches the semantic.
    taste_context: dict[str, Any] = {
        "taste_signature": state.taste_signature.value.model_dump(),
        "food_preferences": list(state.taste_anchors.food_preferences.values),
    }
    novelty = state.energy_profile.novelty_appetite.value
    if novelty is not None:
        taste_context["novelty_level"] = novelty

    # ALIGNMENT-BUG-3 (PRD §B): MoodTag vs EmotionalRole — `ExperienceRequest`
    # keeps EmotionalRole on the wire (per backend §2.6.primary_mood).
    # The agent-side mapping helper `mood_tags_from_emotional_intent` lives in
    # agent.types and is used by the Composer side (not on this request).
    return ExperienceRequest(
        trip_context=trip_context,
        experience_intent=experience_intent,
        constraints=constraints,
        taste_context=taste_context,
    )


# ---------------------------------------------------------------------------
# serialize_for_composer
# ---------------------------------------------------------------------------


def _last_user_turn_text(state: IntakeState) -> str:
    for t in reversed(state.transcript):
        if t.role == "user":
            return t.text
    return ""


def _build_emotional_rationale(state: IntakeState) -> str:
    """Derive the Composer's `emotional_intent.rationale` per the mapping table.

    Rule (Implement-poc.md Phase 1a table): combine values with confidence>0.7
    + most relevant transcript quote. We keep this deterministic: if the
    IntakeState already carries an `emotional_intent_rationale` (e.g. baked
    in by persona fixtures or the Extractor), prefer it verbatim. Else
    synthesize "<values> — <last user msg>".
    """
    if state.emotional_intent_rationale:
        return state.emotional_intent_rationale
    high_conf_values: list[str] = []
    if state.emotional_intent.confidence > 0.7:
        high_conf_values = [v.value for v in state.emotional_intent.values]
    last_msg = _last_user_turn_text(state)
    if high_conf_values and last_msg:
        return f"{', '.join(high_conf_values)} — \"{last_msg.strip()}\""
    if high_conf_values:
        return ", ".join(high_conf_values)
    return last_msg


def serialize_for_composer(state: IntakeState) -> ComposerInput:
    """Flatten typed IntakeState -> Composer prompt's loose Input schema.

    This is the bridge Codex flagged. Field mapping (see Implement-poc.md
    Phase 1a table):

      | IntakeState                               | ComposerInput               |
      |-------------------------------------------|-----------------------------|
      | taste_signature.value.vibe_weights        | taste_signature.vibe_weights|
      |                                           |   tag = vw.tag              |
      |                                           |   weight = vw.weight        |
      |                                           |     (weight == confidence   |
      |                                           |      when emitted by vision)|
      | emotional_intent.values + transcript      | emotional_intent.rationale  |
      | energy_profile.novelty_appetite.value     | energy_profile              |
      |                                           |   .novelty_appetite         |
      |                                           |     (fallback "medium")     |
      | taste_anchors.liked_examples              | taste_anchors.liked_examples|
      |                                           |   (passed through)          |

      Pass-throughs (no transformation):
        social_config.values+rationale, practical_constraints.*,
        avoidance.values+rationale.
    """
    ts = state.taste_signature.value
    composer_taste = ComposerTasteSignature(
        # Weight = the per-tag weight emitted by the vision LLM (already in
        # [0,1]). When a future Extractor needs to overlay confidence, do it
        # at that layer — this serializer is a faithful flatten.
        vibe_weights=[
            ComposerVibeWeight(tag=str(vw.tag), weight=float(vw.weight))
            for vw in ts.vibe_weights
        ],
        summary=ts.summary,
    )

    composer_intent = ComposerEmotionalIntent(
        values=[v.value for v in state.emotional_intent.values],
        rationale=_build_emotional_rationale(state),
    )

    composer_social = ComposerSocialConfig(
        values=[v.value for v in state.social_config.values],
        rationale=state.social_config_rationale,
    )

    novelty = state.energy_profile.novelty_appetite.value
    composer_energy = ComposerEnergyProfile(
        energy_level=(
            state.energy_profile.energy_level.value.value
            if state.energy_profile.energy_level.value is not None
            else None
        ),
        chaos_tolerance=(
            state.energy_profile.chaos_tolerance.value.value
            if state.energy_profile.chaos_tolerance.value is not None
            else None
        ),
        novelty_appetite=(novelty.value if novelty is not None else "medium"),
    )

    pc = state.practical_constraints
    composer_pc = ComposerPracticalConstraints(
        start_location=pc.start_location.value,
        max_drive_minutes=pc.max_drive_minutes.value,
        time_window=pc.time_window.value,
        kid_friendly_required=pc.kid_friendly.value,
        needs_parking=pc.needs_parking.value,
        budget=pc.budget.value,
        transport=pc.transport.value,
    )

    composer_anchors = ComposerTasteAnchors(
        liked_examples=[
            ComposerLikedExample(name=la.name, why_i_like_it=la.why_i_like_it)
            for la in state.taste_anchors.liked_examples
        ],
        food_preferences=list(state.taste_anchors.food_preferences.values),
    )

    composer_avoid = ComposerAvoidance(
        values=[v.value for v in state.avoidance.values],
        rationale=state.avoidance_rationale,
    )

    return ComposerInput(
        taste_signature=composer_taste,
        emotional_intent=composer_intent,
        social_config=composer_social,
        energy_profile=composer_energy,
        practical_constraints=composer_pc,
        taste_anchors=composer_anchors,
        avoidance=composer_avoid,
    )


__all__ = [
    "Provenance",
    "Slot",
    "Turn",
    "TasteSignatureSlot",
    "EnergyProfile",
    "PracticalConstraints",
    "TasteAnchor",
    "TasteAnchors",
    "IntakeState",
    "merge_slot_updates",
    "router",
    "serialize_to_experience_request",
    "serialize_for_composer",
]
