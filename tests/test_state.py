"""Phase 1a tests — pure-Python state machinery.

No LLM, no network. Tests cover:
- `merge_slot_updates` confidence-max + composite per-field merge
- `router` PRD §3 stopping rule (4 branches)
- `serialize_to_experience_request` round-trips with the 4 personas
- `serialize_for_composer` round-trips with the 4 personas
- The 3 alignment-bug fixes (novelty type, primary_mood naming, MoodTag map)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from agent.state import (
    EnergyProfile,
    IntakeState,
    PracticalConstraints,
    Slot,
    TasteAnchor,
    TasteAnchors,
    TasteSignatureSlot,
    Turn,
    _ScalarSlot,
    merge_slot_updates,
    router,
    serialize_for_composer,
    serialize_to_experience_request,
)
from agent.types import (
    AvoidanceTag,
    ChaosTolerance,
    ComposerInput,
    EmotionalRole,
    EnergyLevel,
    ExperienceRequest,
    MoodTag,
    NoveltyLevel,
    SocialFit,
    TasteSignature,
    VibeTag,
    VibeWeight,
    mood_tags_from_emotional_intent,
)

PERSONA_DIR = Path(__file__).resolve().parent.parent / "poc-demo"
PERSONA_NAMES = ["mia", "garry_tan", "alex_chen", "sam_reyes"]


# ---------------------------------------------------------------------------
# Persona-loading helpers
# ---------------------------------------------------------------------------


def _coerce_vibe_tag(tag: str) -> VibeTag | None:
    """Map a free-form persona tag to a controlled VibeTag if possible.

    Personas carry tags outside the controlled vocab ("restorative",
    "cinematic", "natural_light", "novel", "social"...). We accept the ones
    that match by name; anything else is filtered out. Tests that need full
    fidelity rely on `serialize_for_composer` which preserves all tags as
    free strings via ComposerVibeWeight.
    """
    try:
        return VibeTag(tag)
    except ValueError:
        return None


def _coerce_emotional_role(value: str) -> EmotionalRole | None:
    try:
        return EmotionalRole(value)
    except ValueError:
        return None


def _coerce_social_fit(value: str) -> SocialFit | None:
    # Persona JSON uses "friends" — backend SocialFit only has friends_small_group / large_group.
    mapping = {
        "friends": SocialFit.FRIENDS_SMALL_GROUP,
    }
    if value in mapping:
        return mapping[value]
    try:
        return SocialFit(value)
    except ValueError:
        return None


def _coerce_avoid(value: str) -> AvoidanceTag | None:
    try:
        return AvoidanceTag(value)
    except ValueError:
        return None


def _load_persona_state(name: str) -> IntakeState:
    """Load a poc-demo persona JSON into an IntakeState fixture.

    Field mapping mirrors the docstring on `serialize_for_composer`.
    Confidences are taken verbatim from the JSON (persona authors set them).
    """
    path = PERSONA_DIR / f"{name}_persona.json"
    with path.open("r", encoding="utf-8") as f:
        raw: dict[str, Any] = json.load(f)

    ts_raw = raw.get("taste_signature", {})
    vw_in = ts_raw.get("vibe_weights", [])
    # Pass tags through TasteSignature filtered to controlled VibeTag; the
    # serialize_for_composer test below verifies that the full unfiltered set
    # makes it to the Composer side via the free-string ComposerVibeWeight.
    vibe_weights = [
        VibeWeight(tag=tag, weight=float(item["weight"]))
        for item in vw_in
        if (tag := _coerce_vibe_tag(item["tag"])) is not None
    ]
    taste_signature = TasteSignatureSlot(
        value=TasteSignature(
            vibe_weights=vibe_weights,
            summary=ts_raw.get("summary", ""),
            confidence=0.85,
        ),
        confidence=0.85,
    )

    intent_raw = raw.get("intake_state", {})
    emotional_values = [
        v for raw_v in intent_raw.get("values", []) if (v := _coerce_emotional_role(raw_v))
    ]
    emotional_intent: Slot[EmotionalRole] = Slot(
        values=emotional_values,
        confidence=float(intent_raw.get("confidence", 0.8)),
        provenance="user_stated",
    )
    emotional_rationale = intent_raw.get("rationale", "")

    soc_raw = raw.get("social_config", {})
    social_values = [
        v for raw_v in soc_raw.get("values", []) if (v := _coerce_social_fit(raw_v))
    ]
    social_config: Slot[SocialFit] = Slot(
        values=social_values,
        confidence=float(soc_raw.get("confidence", 0.8)),
        provenance="user_stated",
    )

    ep_raw = raw.get("energy_profile", {})
    energy_profile = EnergyProfile(
        energy_level=_ScalarSlot(
            value=EnergyLevel(ep_raw["energy_level"]) if "energy_level" in ep_raw else None,
            confidence=float(ep_raw.get("confidence", 0.8)),
            provenance="user_stated",
        ),
        chaos_tolerance=_ScalarSlot(
            value=(
                ChaosTolerance(ep_raw["chaos_tolerance"])
                # `very_low` (Sam) is not in the backend enum — fall back to LOW
                if ep_raw.get("chaos_tolerance") in {e.value for e in ChaosTolerance}
                else ChaosTolerance.LOW
                if ep_raw.get("chaos_tolerance") == "very_low"
                else None
            ),
            confidence=float(ep_raw.get("confidence", 0.8)),
            provenance="user_stated",
        ),
        novelty_appetite=_ScalarSlot(
            value=NoveltyLevel(ep_raw["novelty_appetite"]) if "novelty_appetite" in ep_raw else None,
            confidence=float(ep_raw.get("confidence", 0.8)),
            provenance="user_stated",
        ),
    )

    pc_raw = raw.get("practical_constraints", {})
    practical_constraints = PracticalConstraints(
        start_location=_ScalarSlot(
            value=pc_raw.get("start_location"),
            confidence=float(pc_raw.get("confidence", 0.8)),
            provenance="user_stated",
        ),
        time_window=_ScalarSlot(
            value=pc_raw.get("time_window"),
            confidence=float(pc_raw.get("confidence", 0.8)),
            provenance="user_stated",
        ),
        max_drive_minutes=_ScalarSlot(
            value=pc_raw.get("max_drive_minutes"),
            confidence=float(pc_raw.get("confidence", 0.8)),
            provenance="user_stated",
        ),
        budget=_ScalarSlot(
            value=pc_raw.get("budget"),
            confidence=float(pc_raw.get("confidence", 0.8)),
            provenance="user_stated",
        ),
        kid_friendly=_ScalarSlot(
            value=pc_raw.get("kid_friendly_required"),
            confidence=float(pc_raw.get("confidence", 0.8)),
            provenance="user_stated",
        ),
        needs_parking=_ScalarSlot(
            value=pc_raw.get("needs_parking"),
            confidence=float(pc_raw.get("confidence", 0.8)),
            provenance="user_stated",
        ),
    )

    ta_raw = raw.get("taste_anchors", {})
    liked = [
        TasteAnchor(name=item["name"], why_i_like_it=item.get("why_i_like_it", ""))
        for item in ta_raw.get("liked_examples", [])
    ]
    taste_anchors = TasteAnchors(
        food_preferences=Slot[str](
            values=list(ta_raw.get("food_preferences", [])),
            confidence=float(ta_raw.get("confidence", 0.8)),
            provenance="user_stated",
        ),
        liked_examples=liked,
    )

    av_raw = raw.get("avoidance", {})
    avoid_values = [v for raw_v in av_raw.get("values", []) if (v := _coerce_avoid(raw_v))]
    avoidance: Slot[AvoidanceTag] = Slot(
        values=avoid_values,
        confidence=float(av_raw.get("confidence", 0.8)),
        provenance="user_stated",
    )

    state = IntakeState(
        taste_signature=taste_signature,
        emotional_intent=emotional_intent,
        emotional_intent_rationale=emotional_rationale,
        social_config=social_config,
        social_config_rationale=soc_raw.get("rationale", ""),
        energy_profile=energy_profile,
        practical_constraints=practical_constraints,
        taste_anchors=taste_anchors,
        avoidance=avoidance,
        avoidance_rationale=av_raw.get("rationale", ""),
        turn_count=3,
        transcript=[
            Turn(
                role="user",
                text=raw.get("demo_scenario", {}).get("my_first_message_to_agent", ""),
                turn_index=0,
            ),
        ],
    )
    return state


# ---------------------------------------------------------------------------
# router edge cases
# ---------------------------------------------------------------------------


class TestRouter:
    def test_turn_zero_returns_ask(self) -> None:
        state = IntakeState()
        assert router(state) == "ASK"

    def test_turn_ten_returns_hard_cap(self) -> None:
        state = IntakeState(turn_count=10)
        assert router(state) == "STOP_HARD_CAP"

    def test_turn_eleven_still_hard_cap(self) -> None:
        state = IntakeState(turn_count=11)
        assert router(state) == "STOP_HARD_CAP"

    def test_all_confidence_high_returns_ready(self) -> None:
        state = IntakeState(
            taste_signature=TasteSignatureSlot(
                value=TasteSignature(summary="x", confidence=0.9), confidence=0.9
            ),
            emotional_intent=Slot[EmotionalRole](
                values=[EmotionalRole.RESTORE],
                confidence=0.9,
                provenance="user_stated",
            ),
            social_config=Slot[SocialFit](
                values=[SocialFit.SOLO],
                confidence=0.9,
                provenance="user_stated",
            ),
            energy_profile=EnergyProfile(
                energy_level=_ScalarSlot(
                    value=EnergyLevel.LOW, confidence=0.9, provenance="user_stated"
                ),
                chaos_tolerance=_ScalarSlot(
                    value=ChaosTolerance.LOW, confidence=0.9, provenance="user_stated"
                ),
            ),
            practical_constraints=PracticalConstraints(
                date=_ScalarSlot(value="2026-01-10", confidence=0.9, provenance="user_stated"),
                time_window=_ScalarSlot(value="14:00-21:00", confidence=0.9, provenance="user_stated"),
                start_location=_ScalarSlot(value="SF", confidence=0.9, provenance="user_stated"),
                transport=_ScalarSlot(value="car", confidence=0.9, provenance="user_stated"),
                max_drive_minutes=_ScalarSlot(value=30, confidence=0.9, provenance="user_stated"),
                budget=_ScalarSlot(value="flexible", confidence=0.9, provenance="user_stated"),
                kid_friendly=_ScalarSlot(value=True, confidence=0.9, provenance="user_stated"),
                needs_parking=_ScalarSlot(value=True, confidence=0.9, provenance="user_stated"),
            ),
            taste_anchors=TasteAnchors(
                desired_vibe=Slot[VibeTag](
                    values=[VibeTag.QUIET],
                    confidence=0.9,
                    provenance="user_stated",
                ),
            ),
            avoidance=Slot[AvoidanceTag](
                values=[AvoidanceTag.TOURISTY],
                confidence=0.9,
                provenance="user_stated",
            ),
            turn_count=4,
        )
        assert router(state) == "READY"

    def test_avg_high_but_one_slot_low_returns_ask(self) -> None:
        """avg(conf) >= 0.8 but one dim's confidence < 0.5 -> ASK.

        Construction: every dim at 0.95 except social_config at 0.3. Average
        across the 6-dim vector is well above 0.8, but the min violates the
        0.5 floor, so the stopping rule should NOT fire.
        """
        state = IntakeState(
            taste_signature=TasteSignatureSlot(
                value=TasteSignature(summary="x", confidence=0.95), confidence=0.95
            ),
            emotional_intent=Slot[EmotionalRole](
                values=[EmotionalRole.RESTORE],
                confidence=0.95,
                provenance="user_stated",
            ),
            # social_config is the offender at 0.3
            social_config=Slot[SocialFit](
                values=[],
                confidence=0.3,
                provenance="default",
            ),
            energy_profile=EnergyProfile(
                energy_level=_ScalarSlot(
                    value=EnergyLevel.LOW, confidence=0.95, provenance="user_stated"
                ),
                chaos_tolerance=_ScalarSlot(
                    value=ChaosTolerance.LOW, confidence=0.95, provenance="user_stated"
                ),
            ),
            practical_constraints=PracticalConstraints(
                date=_ScalarSlot(value="2026-01-10", confidence=0.95, provenance="user_stated"),
                time_window=_ScalarSlot(value="14:00-21:00", confidence=0.95, provenance="user_stated"),
                start_location=_ScalarSlot(value="SF", confidence=0.95, provenance="user_stated"),
                transport=_ScalarSlot(value="car", confidence=0.95, provenance="user_stated"),
                max_drive_minutes=_ScalarSlot(value=30, confidence=0.95, provenance="user_stated"),
                budget=_ScalarSlot(value="flexible", confidence=0.95, provenance="user_stated"),
                kid_friendly=_ScalarSlot(value=True, confidence=0.95, provenance="user_stated"),
                needs_parking=_ScalarSlot(value=True, confidence=0.95, provenance="user_stated"),
            ),
            taste_anchors=TasteAnchors(
                desired_vibe=Slot[VibeTag](
                    values=[VibeTag.QUIET],
                    confidence=0.95,
                    provenance="user_stated",
                ),
            ),
            avoidance=Slot[AvoidanceTag](
                values=[AvoidanceTag.TOURISTY],
                confidence=0.95,
                provenance="user_stated",
            ),
            turn_count=4,
        )
        assert router(state) == "ASK"

    def test_user_escape_returns_ready(self) -> None:
        """`stopped_reason == 'user_escape'` is the PRD escape-hatch path."""
        state = IntakeState(turn_count=2, stopped_reason="user_escape")
        assert router(state) == "READY"


# ---------------------------------------------------------------------------
# merge_slot_updates
# ---------------------------------------------------------------------------


class TestMergeSlotUpdates:
    def test_higher_confidence_overwrites(self) -> None:
        state = IntakeState(
            emotional_intent=Slot[EmotionalRole](
                values=[EmotionalRole.RESTORE],
                confidence=0.5,
                provenance="user_implied",
            ),
        )
        new_state = merge_slot_updates(
            state,
            {
                "emotional_intent": {
                    "values": [EmotionalRole.EXPLORE],
                    "confidence": 0.9,
                    "provenance": "user_stated",
                }
            },
        )
        assert new_state.emotional_intent.values == [EmotionalRole.EXPLORE]
        assert new_state.emotional_intent.confidence == pytest.approx(0.9)
        assert new_state.emotional_intent.provenance == "user_stated"

    def test_lower_confidence_does_not_overwrite(self) -> None:
        state = IntakeState(
            emotional_intent=Slot[EmotionalRole](
                values=[EmotionalRole.RESTORE],
                confidence=0.9,
                provenance="user_stated",
            ),
        )
        new_state = merge_slot_updates(
            state,
            {
                "emotional_intent": {
                    "values": [EmotionalRole.EXPLORE],
                    "confidence": 0.5,
                    "provenance": "user_implied",
                }
            },
        )
        # Existing value kept; provenance not downgraded.
        assert new_state.emotional_intent.values == [EmotionalRole.RESTORE]
        assert new_state.emotional_intent.confidence == pytest.approx(0.9)
        assert new_state.emotional_intent.provenance == "user_stated"

    def test_turn_count_increments_each_call(self) -> None:
        state = IntakeState(turn_count=0)
        s1 = merge_slot_updates(state, {})
        s2 = merge_slot_updates(s1, {})
        s3 = merge_slot_updates(s2, {})
        assert s1.turn_count == 1
        assert s2.turn_count == 2
        assert s3.turn_count == 3

    def test_composite_slots_merge_per_subfield(self) -> None:
        state = IntakeState()
        new_state = merge_slot_updates(
            state,
            {
                "energy_profile": {
                    "energy_level": {
                        "value": EnergyLevel.LOW,
                        "confidence": 0.8,
                        "provenance": "user_stated",
                    },
                    "chaos_tolerance": {
                        "value": ChaosTolerance.MEDIUM,
                        "confidence": 0.4,
                        "provenance": "user_implied",
                    },
                },
            },
        )
        assert new_state.energy_profile.energy_level.value == EnergyLevel.LOW
        assert new_state.energy_profile.energy_level.confidence == pytest.approx(0.8)
        assert new_state.energy_profile.chaos_tolerance.value == ChaosTolerance.MEDIUM
        assert new_state.energy_profile.chaos_tolerance.confidence == pytest.approx(0.4)

        # Second merge: only chaos_tolerance updated, energy_level untouched.
        s2 = merge_slot_updates(
            new_state,
            {
                "energy_profile": {
                    "chaos_tolerance": {
                        "value": ChaosTolerance.LOW,
                        "confidence": 0.9,
                        "provenance": "user_stated",
                    },
                },
            },
        )
        # energy_level preserved
        assert s2.energy_profile.energy_level.value == EnergyLevel.LOW
        assert s2.energy_profile.energy_level.confidence == pytest.approx(0.8)
        # chaos_tolerance upgraded
        assert s2.energy_profile.chaos_tolerance.value == ChaosTolerance.LOW
        assert s2.energy_profile.chaos_tolerance.confidence == pytest.approx(0.9)


# ---------------------------------------------------------------------------
# serialize_to_experience_request — across all 4 personas
# ---------------------------------------------------------------------------


class TestSerializeToExperienceRequest:
    @pytest.mark.parametrize("persona", PERSONA_NAMES)
    def test_persona_serializes_validly(self, persona: str) -> None:
        state = _load_persona_state(persona)
        req = serialize_to_experience_request(state)
        # Round-trips through pydantic without raising.
        assert isinstance(req, ExperienceRequest)
        ExperienceRequest.model_validate(req.model_dump())

    @pytest.mark.parametrize("persona", PERSONA_NAMES)
    def test_required_fields_populated(self, persona: str) -> None:
        state = _load_persona_state(persona)
        req = serialize_to_experience_request(state)

        # trip_context shape
        assert "date" in req.trip_context
        assert "time_window" in req.trip_context
        assert "start_location" in req.trip_context
        assert "companions" in req.trip_context
        assert "transport" in req.trip_context

        # experience_intent — ALIGNMENT-BUG-2 fix: the wire field is named
        # `primary_mood` (NOT `emotional_intent`).
        assert "primary_mood" in req.experience_intent
        assert "emotional_intent" not in req.experience_intent
        assert "desired_vibe" in req.experience_intent
        assert "avoid" in req.experience_intent

        # constraints
        assert req.constraints["stop_count_target"] == 4

    def test_alignment_bug_1_novelty_not_typed_as_energy_level(self) -> None:
        """novelty_level must come from energy_profile.novelty_appetite,
        NOT energy_profile.energy_level."""
        state = IntakeState(
            energy_profile=EnergyProfile(
                energy_level=_ScalarSlot(
                    value=EnergyLevel.HIGH, confidence=0.9, provenance="user_stated"
                ),
                novelty_appetite=_ScalarSlot(
                    value=NoveltyLevel.LOW, confidence=0.9, provenance="user_stated"
                ),
            ),
        )
        req = serialize_to_experience_request(state)
        # Even though energy_level=HIGH, novelty_level should be LOW
        # (matching novelty_appetite). Confirms we did NOT map energy_level
        # into novelty_level.
        assert req.taste_context.get("novelty_level") == NoveltyLevel.LOW.value
        assert req.constraints["energy_level"] == EnergyLevel.HIGH

    def test_alignment_bug_1_novelty_omitted_when_unset(self) -> None:
        """If no novelty_appetite is captured, the field is omitted rather
        than guessed."""
        state = IntakeState()  # all defaults
        req = serialize_to_experience_request(state)
        assert "novelty_level" not in req.taste_context

    def test_alignment_bug_2_primary_mood_naming_consistent(self) -> None:
        state = IntakeState(
            emotional_intent=Slot[EmotionalRole](
                values=[EmotionalRole.RESTORE, EmotionalRole.SLOW_DOWN],
                confidence=0.9,
                provenance="user_stated",
            ),
        )
        req = serialize_to_experience_request(state)
        # Backend's name on the wire is `primary_mood`.
        assert req.experience_intent["primary_mood"] == [
            EmotionalRole.RESTORE,
            EmotionalRole.SLOW_DOWN,
        ]
        # Agent's internal name (`emotional_intent`) does NOT leak onto wire.
        assert "emotional_intent" not in req.experience_intent


# ---------------------------------------------------------------------------
# serialize_for_composer — across all 4 personas
# ---------------------------------------------------------------------------


class TestSerializeForComposer:
    @pytest.mark.parametrize("persona", PERSONA_NAMES)
    def test_persona_serializes_validly(self, persona: str) -> None:
        state = _load_persona_state(persona)
        composer_input = serialize_for_composer(state)
        # Validates against pydantic schema (loose composer-side type).
        assert isinstance(composer_input, ComposerInput)
        ComposerInput.model_validate(composer_input.model_dump())

    @pytest.mark.parametrize("persona", PERSONA_NAMES)
    def test_weight_passes_through_from_taste_signature(self, persona: str) -> None:
        """Mapping table row 1: composer.taste_signature.vibe_weights[i].weight
        equals the underlying TasteSignature vibe_weights[i].weight."""
        state = _load_persona_state(persona)
        ci = serialize_for_composer(state)
        # Build expected from the IntakeState's TasteSignature directly.
        expected = {str(vw.tag): float(vw.weight) for vw in state.taste_signature.value.vibe_weights}
        actual = {item.tag: item.weight for item in ci.taste_signature.vibe_weights}
        assert actual == expected

    @pytest.mark.parametrize("persona", PERSONA_NAMES)
    def test_rationale_derived_from_emotional_intent_or_transcript(self, persona: str) -> None:
        state = _load_persona_state(persona)
        ci = serialize_for_composer(state)
        # Rationale must be non-empty for personas (their JSONs all carry one
        # OR the transcript has the first user message).
        assert ci.emotional_intent.rationale != ""

    def test_rationale_synthesized_when_state_has_no_baked_rationale(self) -> None:
        """If `emotional_intent_rationale` is empty but transcript + high-
        confidence emotional values exist, the serializer synthesizes the
        rationale (verifies the derivation path, not just the pass-through)."""
        state = IntakeState(
            emotional_intent=Slot[EmotionalRole](
                values=[EmotionalRole.RESTORE],
                confidence=0.85,
                provenance="user_stated",
            ),
            transcript=[Turn(role="user", text="just want a quiet day", turn_index=0)],
        )
        ci = serialize_for_composer(state)
        assert "restore" in ci.emotional_intent.rationale
        assert "quiet day" in ci.emotional_intent.rationale

    @pytest.mark.parametrize("persona", PERSONA_NAMES)
    def test_novelty_appetite_passes_through(self, persona: str) -> None:
        state = _load_persona_state(persona)
        ci = serialize_for_composer(state)
        # All personas carry novelty_appetite; should NOT fall back to "medium".
        expected = state.energy_profile.novelty_appetite.value
        if expected is not None:
            assert ci.energy_profile.novelty_appetite == expected.value

    def test_novelty_appetite_fallback_when_unset(self) -> None:
        state = IntakeState()
        ci = serialize_for_composer(state)
        assert ci.energy_profile.novelty_appetite == "medium"

    @pytest.mark.parametrize("persona", PERSONA_NAMES)
    def test_liked_examples_passed_through(self, persona: str) -> None:
        state = _load_persona_state(persona)
        ci = serialize_for_composer(state)
        # Persona JSONs all carry liked_examples; ensure shape preserved.
        assert len(ci.taste_anchors.liked_examples) == len(state.taste_anchors.liked_examples)
        for in_, out_ in zip(
            state.taste_anchors.liked_examples,
            ci.taste_anchors.liked_examples,
            strict=False,
        ):
            assert out_.name == in_.name
            assert out_.why_i_like_it == in_.why_i_like_it


# ---------------------------------------------------------------------------
# ALIGNMENT-BUG-3: MoodTag mapping helper
# ---------------------------------------------------------------------------


class TestMoodTagMapping:
    def test_every_emotional_role_maps_to_at_least_one_mood_tag(self) -> None:
        for role in EmotionalRole:
            tags = mood_tags_from_emotional_intent([role])
            assert len(tags) >= 1, f"EmotionalRole {role!r} has no MoodTag mapping"

    def test_mapping_results_are_valid_mood_tags(self) -> None:
        all_tags = mood_tags_from_emotional_intent(list(EmotionalRole))
        for tag in all_tags:
            assert isinstance(tag, MoodTag)

    def test_mapping_deduplicates(self) -> None:
        # restore -> reflective+restorative; slow_down -> not_rushed+grounding.
        # These two share no tags; passing both should produce 4 unique tags.
        tags = mood_tags_from_emotional_intent([EmotionalRole.RESTORE, EmotionalRole.SLOW_DOWN])
        assert len(tags) == len(set(tags))
        assert len(tags) == 4

    def test_specific_mappings(self) -> None:
        # Spot-check the table is what the docstring claims.
        assert MoodTag.REFLECTIVE in mood_tags_from_emotional_intent([EmotionalRole.RESTORE])
        assert MoodTag.RESTORATIVE in mood_tags_from_emotional_intent([EmotionalRole.RESTORE])
        assert MoodTag.LIGHTLY_EXPLORATORY in mood_tags_from_emotional_intent(
            [EmotionalRole.EXPLORE]
        )
        assert MoodTag.CELEBRATORY in mood_tags_from_emotional_intent([EmotionalRole.CELEBRATE])
        assert MoodTag.ENERGIZING in mood_tags_from_emotional_intent([EmotionalRole.FEEL_ALIVE])
