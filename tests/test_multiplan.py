"""Phase 3b tests — diversity enforcement + format_proposals + end-to-end mock.

Pure unit tests on PlanResult fixtures; we don't re-invoke the Composer
LLM here (test_composer.py covers that). End-to-end test (e) mocks the
Anthropic client with the same _FakeClient pattern.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from agent.compose.composer import PlanComposer
from agent.compose.concepts import generate_concepts_simple
from agent.present.diversity import check_diversity, deduplicate_first_stops
from agent.present.format import format_proposals
from agent.state import IntakeState, TasteSignatureSlot
from agent.types import (
    PlaceCandidate,
    PlanResult,
    TasteSignature,
    ThemeAnchor,
    VibeTag,
    VibeWeight,
)

# --------------------------------------------------------------------------- #
# Fake Anthropic client — same shape as tests/test_composer.py.               #
# --------------------------------------------------------------------------- #


@dataclass
class _FakeTextBlock:
    text: str


@dataclass
class _FakeMessage:
    content: list[_FakeTextBlock]


@dataclass
class _FakeMessages:
    queued_texts: list[str] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)

    async def create(
        self,
        *,
        model: str,
        max_tokens: int,
        system: str,
        messages: list[dict[str, Any]],
    ) -> _FakeMessage:
        self.calls.append({"model": model, "user": messages[0]["content"]})
        if not self.queued_texts:
            raise RuntimeError("FakeMessages exhausted")
        return _FakeMessage(content=[_FakeTextBlock(text=self.queued_texts.pop(0))])


@dataclass
class _FakeClient:
    messages: _FakeMessages = field(default_factory=_FakeMessages)

    def queue(self, *texts: str) -> None:
        self.messages.queued_texts.extend(texts)


# --------------------------------------------------------------------------- #
# PlanResult fixtures                                                         #
# --------------------------------------------------------------------------- #


def _plan(
    *,
    theme: ThemeAnchor,
    day_theme: str,
    pitch: str,
    stop_ids: list[str],
    stop_names: list[str] | None = None,
    mood_tags: list[str] | None = None,
) -> PlanResult:
    return PlanResult(
        markdown=(
            f"## {day_theme}\n\n"
            f"> **一句话 pitch**: {pitch}\n\n"
            f"## 10:00 · {(stop_names or stop_ids)[0]}\nbody...\n\n"
            f"## 12:30 · {(stop_names or stop_ids)[1]}\nbody...\n"
        ),
        day_theme=day_theme,
        pitch=pitch,
        theme_anchor=theme,
        mood_tags=mood_tags or [],
        stop_place_ids=stop_ids,
        stop_names=stop_names or stop_ids,
    )


def _three_distinct_plans() -> list[PlanResult]:
    return [
        _plan(
            theme=ThemeAnchor.CULTURAL_RESTORATIVE,
            day_theme="旧湾区的安静一天",
            pitch="安静历史 + 湖边呼吸。",
            stop_ids=["alviso_adobe", "sandy_wool_lake", "saigon_seafood", "mill_valley_park"],
            stop_names=["Alviso Adobe Park", "Sandy Wool Lake", "Saigon Seafood", "Mill Valley Park"],
            mood_tags=["reflective", "warm"],
        ),
        _plan(
            theme=ThemeAnchor.OUTDOOR_EXPLORATORY,
            day_theme="开阔的山海一日",
            pitch="走路 + 海风 + 慢午餐。",
            stop_ids=["muir_woods", "stinson_beach", "parkside_cafe", "headlands_overlook"],
            stop_names=["Muir Woods", "Stinson Beach", "Parkside Cafe", "Headlands Overlook"],
            mood_tags=["energizing", "grounding"],
        ),
        _plan(
            theme=ThemeAnchor.QUIET_INTIMATE,
            day_theme="只属于你们俩的角落",
            pitch="低光 + 小空间 + 慢节奏。",
            stop_ids=["sausalito_pier", "il_piccolo", "books_inc", "bridgeway_lookout"],
            stop_names=["Sausalito Pier", "Il Piccolo", "Books Inc", "Bridgeway Lookout"],
            mood_tags=["intimate", "not_rushed"],
        ),
    ]


def _three_same_first_stop_plans() -> list[PlanResult]:
    """Three plans whose first stop is identical — worst-case for dedupe."""
    return [
        _plan(
            theme=ThemeAnchor.CULTURAL_RESTORATIVE,
            day_theme="A",
            pitch="A pitch",
            stop_ids=["mill_valley_downtown", "alt_a_2", "alt_a_3", "alt_a_4"],
            stop_names=["Mill Valley", "Alt A2", "Alt A3", "Alt A4"],
        ),
        _plan(
            theme=ThemeAnchor.OUTDOOR_EXPLORATORY,
            day_theme="B",
            pitch="B pitch",
            stop_ids=["mill_valley_downtown", "alt_b_2", "alt_b_3", "alt_b_4"],
            stop_names=["Mill Valley", "Alt B2", "Alt B3", "Alt B4"],
        ),
        _plan(
            theme=ThemeAnchor.QUIET_INTIMATE,
            day_theme="C",
            pitch="C pitch",
            stop_ids=["mill_valley_downtown", "alt_c_2", "alt_c_3", "alt_c_4"],
            stop_names=["Mill Valley", "Alt C2", "Alt C3", "Alt C4"],
        ),
    ]


# --------------------------------------------------------------------------- #
# format_proposals tests                                                      #
# --------------------------------------------------------------------------- #


def test_format_proposals_3_plans_title_and_table() -> None:
    plans = _three_distinct_plans()
    out = format_proposals(plans, "Mia 周六想 restore 一下。")

    assert "# 你的周六，3 种走法" in out
    assert "> Mia 周六想 restore" in out
    assert "## 速览对比" in out
    # Comparison table with 3 rows (after the header + separator)
    table_rows = [
        line for line in out.splitlines() if line.startswith("|") and "---" not in line
    ]
    # 1 header + 3 plan rows
    assert len(table_rows) == 4
    # All 3 day_themes appear in the body
    for plan in plans:
        assert plan.day_theme in out
    # Plans separated by ---
    assert out.count("\n---\n") == 3


def test_format_proposals_2_plans_n_aware_title() -> None:
    plans = _three_distinct_plans()[:2]
    out = format_proposals(plans, "summary")
    assert "# 你的周六，2 种走法" in out
    table_rows = [
        line for line in out.splitlines() if line.startswith("|") and "---" not in line
    ]
    assert len(table_rows) == 3  # 1 header + 2 rows


def test_format_proposals_empty_mood_tags_falls_back_to_theme() -> None:
    plan = _plan(
        theme=ThemeAnchor.SOCIAL_HIGH_ENERGY,
        day_theme="X",
        pitch="X pitch",
        stop_ids=["s1", "s2", "s3", "s4"],
        mood_tags=[],  # explicit empty
    )
    out = format_proposals([plan], "summary")
    # The vibe column should fall back to theme_anchor.value
    assert "social_high_energy" in out


def test_format_proposals_missing_stop_names_falls_back() -> None:
    plan = _plan(
        theme=ThemeAnchor.QUIET_INTIMATE,
        day_theme="X",
        pitch="X",
        stop_ids=["", "", "", ""],  # all empty → triggers "未指定"
        stop_names=["", "", "", ""],
    )
    out = format_proposals([plan], "s")
    assert "未指定" in out


def test_format_proposals_empty_plans_returns_placeholder() -> None:
    out = format_proposals([], "anything")
    assert "No plans available" in out


# --------------------------------------------------------------------------- #
# diversity tests                                                             #
# --------------------------------------------------------------------------- #


def test_check_diversity_distinct_plans_returns_empty() -> None:
    plans = _three_distinct_plans()
    assert check_diversity(plans) == []


def test_check_diversity_same_first_stop_flags_violations() -> None:
    plans = _three_same_first_stop_plans()
    violations = check_diversity(plans)
    # plan[1] shares with plan[0], plan[2] shares with plan[0] → 2 first-stop
    # violations. The pairwise-overlap rule also fires for each pair where
    # they share >1 stop, but in this fixture each plan only shares the FIRST
    # stop with the others (alt_X_2..4 differ), so overlap=1 — no extra
    # violations from rule 2.
    first_stop_violations = [v for v in violations if "shares first stop" in v]
    assert len(first_stop_violations) == 2


def test_check_diversity_repeated_theme_anchor_flags() -> None:
    p = _three_distinct_plans()
    # Force plan[1] to reuse plan[0]'s theme
    p[1] = p[1].model_copy(update={"theme_anchor": ThemeAnchor.CULTURAL_RESTORATIVE})
    violations = check_diversity(p)
    assert any("theme_anchor" in v for v in violations)


def test_deduplicate_first_stops_swaps_when_possible() -> None:
    plans = _three_same_first_stop_plans()
    fixed = deduplicate_first_stops(plans, candidates=[])
    first_stops = [p.stop_place_ids[0] for p in fixed]
    # plan[0] stays as mill_valley_downtown; plan[1] and plan[2] swap to
    # their alt_b_2 / alt_c_2 respectively
    assert first_stops[0] == "mill_valley_downtown"
    assert first_stops[1] == "alt_b_2"
    assert first_stops[2] == "alt_c_2"
    # After dedupe, check_diversity should be clean (or at least no
    # first-stop violations)
    assert all(
        "shares first stop" not in v for v in check_diversity(fixed)
    )
    # stop_names should be reordered in lockstep with stop_place_ids
    assert fixed[1].stop_names[0] == "Alt B2"
    assert fixed[2].stop_names[0] == "Alt C2"


def test_deduplicate_first_stops_unresolvable_leaves_plan() -> None:
    """If all stops in a plan point to the same place, dedupe can't help."""
    plans = [
        _plan(
            theme=ThemeAnchor.CULTURAL_RESTORATIVE,
            day_theme="A",
            pitch="a",
            stop_ids=["dup", "x", "y", "z"],
        ),
        _plan(
            theme=ThemeAnchor.OUTDOOR_EXPLORATORY,
            day_theme="B",
            pitch="b",
            stop_ids=["dup", "dup", "dup", "dup"],  # nothing to swap to
        ),
    ]
    fixed = deduplicate_first_stops(plans, candidates=[])
    # Second plan is left as-is — violations will persist
    assert fixed[1].stop_place_ids[0] == "dup"
    violations = check_diversity(fixed)
    assert any("shares first stop" in v for v in violations)


def test_check_diversity_pairwise_overlap_flags() -> None:
    """Two plans sharing 3 stops should violate the >1 overlap rule."""
    plans = [
        _plan(
            theme=ThemeAnchor.CULTURAL_RESTORATIVE,
            day_theme="A",
            pitch="a",
            stop_ids=["s1", "s2", "s3", "s4"],
        ),
        _plan(
            theme=ThemeAnchor.OUTDOOR_EXPLORATORY,
            day_theme="B",
            pitch="b",
            stop_ids=["sX", "s2", "s3", "s4"],
        ),
    ]
    violations = check_diversity(plans)
    overlap_vios = [v for v in violations if "share" in v and "stops" in v]
    assert len(overlap_vios) >= 1


# --------------------------------------------------------------------------- #
# End-to-end mocked: concepts → Composer × N → diversity → format             #
# --------------------------------------------------------------------------- #


def _mia_state() -> IntakeState:
    state = IntakeState()
    ts = TasteSignature(
        vibe_weights=[
            VibeWeight(tag=VibeTag.QUIET, weight=0.9),
            VibeWeight(tag=VibeTag.WARM, weight=0.7),
            VibeWeight(tag=VibeTag.OUTDOOR, weight=0.6),
            VibeWeight(tag=VibeTag.SLOW, weight=0.6),
        ],
        summary="Quiet, slow, warm, outdoor.",
        confidence=0.9,
    )
    return state.model_copy(
        update={
            "taste_signature": TasteSignatureSlot(
                value=ts, confidence=0.9, provenance="inferred_from_screenshots"
            )
        }
    )


def _demo_candidates() -> list[PlaceCandidate]:
    """Hand-built pool with enough variety for generate_concepts_simple to
    produce 3 distinct themes (cultural_restorative, outdoor_exploratory,
    quiet_intimate for the Mia-like state)."""
    return [
        PlaceCandidate(
            place_id="alviso_adobe",
            name="Alviso Adobe Park",
            fit_score=0.9,
            fit_reason="quiet + cultural",
            composition={"vibe_tags": [{"tag": t} for t in ["quiet", "cultural", "warm", "slow"]]},
        ),
        PlaceCandidate(
            place_id="sandy_wool_lake",
            name="Sandy Wool Lake",
            fit_score=0.85,
            fit_reason="outdoor + quiet",
            composition={"vibe_tags": [{"tag": t} for t in ["outdoor", "spacious", "walkable"]]},
        ),
        PlaceCandidate(
            place_id="muir_woods",
            name="Muir Woods",
            fit_score=0.88,
            fit_reason="outdoor",
            composition={"vibe_tags": [{"tag": t} for t in ["outdoor", "walkable", "spacious"]]},
        ),
        PlaceCandidate(
            place_id="stinson_beach",
            name="Stinson Beach",
            fit_score=0.82,
            fit_reason="outdoor + lively",
            composition={"vibe_tags": [{"tag": t} for t in ["outdoor", "lively", "spacious"]]},
        ),
        PlaceCandidate(
            place_id="sausalito_pier",
            name="Sausalito Pier",
            fit_score=0.78,
            fit_reason="quiet + warm",
            composition={"vibe_tags": [{"tag": t} for t in ["quiet", "warm", "slow", "low_noise"]]},
        ),
        PlaceCandidate(
            place_id="il_piccolo",
            name="Il Piccolo",
            fit_score=0.76,
            fit_reason="intimate + warm",
            composition={"vibe_tags": [{"tag": t} for t in ["intimate", "warm", "slow", "low_noise"]]},
        ),
        PlaceCandidate(
            place_id="books_inc",
            name="Books Inc",
            fit_score=0.7,
            fit_reason="quiet",
            composition={"vibe_tags": [{"tag": t} for t in ["quiet", "warm"]]},
        ),
        PlaceCandidate(
            place_id="parkside_cafe",
            name="Parkside Cafe",
            fit_score=0.72,
            fit_reason="warm + slow",
            composition={"vibe_tags": [{"tag": t} for t in ["warm", "slow", "outdoor"]]},
        ),
    ]


def _mock_plan_response(
    *,
    day_theme: str,
    pitch: str,
    theme_anchor: str,
    stop_ids: list[str],
    stop_names: list[str],
) -> str:
    """Build a PLAN_META-carrying markdown response."""
    import json

    meta = {
        "day_theme": day_theme,
        "pitch": pitch,
        "theme_anchor": theme_anchor,
        "mood_tags": ["reflective", "warm"],
        "emotional_arc": ["opening", "breathing", "peak", "closing"],
        "stop_place_ids": stop_ids,
        "stop_names": stop_names,
        "adaptive_branches": [],
        "composer_note": "",
    }
    body = (
        f"## {day_theme}\n\n"
        f"> **一句话 pitch**: {pitch}\n\n"
        f"## 10:00 · {stop_names[0]}\nopening narrative...\n\n"
        f"## 12:30 · {stop_names[1]}\nbreathing narrative...\n\n"
        f"## 15:00 · {stop_names[2]}\npeak narrative...\n\n"
        f"## 17:30 · {stop_names[3]}\nclosing narrative...\n\n"
        f"<!-- PLAN_META {json.dumps(meta, ensure_ascii=False)} -->\n"
    )
    return body


@pytest.mark.asyncio
async def test_end_to_end_three_plans_through_pipeline() -> None:
    """concepts → 3× Composer (mocked) → diversity → format produces a
    valid ProposalSet markdown with 3 distinct first stops + 3 plan bodies."""
    state = _mia_state()
    candidates = _demo_candidates()
    concepts = generate_concepts_simple(state, candidates)
    assert len(concepts) >= 2  # generator should produce 2+ for Mia-like state

    client = _FakeClient()
    # Queue one canned response per concept, each with a distinct first stop
    # drawn from the concept's anchor pool.
    canned_first_stops = ["alviso_adobe", "muir_woods", "sausalito_pier"]
    for i, concept in enumerate(concepts):
        # Build a 4-stop list rooted at a distinct first stop. If concept has
        # fewer than 4 anchor_place_ids, pad from the candidate pool.
        first = (
            canned_first_stops[i]
            if i < len(canned_first_stops)
            and canned_first_stops[i] in {c.place_id for c in candidates}
            else (concept.anchor_place_ids[0] if concept.anchor_place_ids else "alviso_adobe")
        )
        fillers = [
            c.place_id for c in candidates if c.place_id != first
        ][:3]
        ids = [first, *fillers]
        names_by_id = {c.place_id: c.name for c in candidates}
        names = [names_by_id.get(pid, pid) for pid in ids]
        client.queue(
            _mock_plan_response(
                day_theme=f"Theme {i}",
                pitch=f"Pitch {i}.",
                theme_anchor=concept.theme_anchor.value,
                stop_ids=ids,
                stop_names=names,
            )
        )

    composer = PlanComposer(anthropic_client=client)
    import asyncio

    plans: list[PlanResult] = list(
        await asyncio.gather(*(composer.run(c, candidates, state) for c in concepts))
    )

    # Diversity pass
    violations = check_diversity(plans)
    plans_after = (
        deduplicate_first_stops(plans, candidates) if violations else plans
    )

    out = format_proposals(plans_after, "Mia 周六想 restore 一下。")
    assert f"# 你的周六，{len(plans_after)} 种走法" in out
    assert "## 速览对比" in out
    # 1 header row + N data rows
    table_rows = [
        line for line in out.splitlines() if line.startswith("|") and "---" not in line
    ]
    assert len(table_rows) == 1 + len(plans_after)
    # No two plans share their first stop
    first_stops = [p.stop_place_ids[0] for p in plans_after]
    assert len(set(first_stops)) == len(first_stops)
