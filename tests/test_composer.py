"""Phase 3a tests for PlanComposer.

Same Protocol-typed fake-client pattern as test_intake.py: a small
_FakeAnthropicClient with a queued response list. No live API calls by
default; the `@pytest.mark.live` smoke at the bottom runs only when
`RUN_LIVE_LLM=1`.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

import pytest

from agent.compose.composer import PlanComposer
from agent.compose.concepts import generate_concepts_simple
from agent.state import IntakeState, TasteSignatureSlot, serialize_to_experience_request
from agent.tools.backend import search_places
from agent.types import (
    Concept,
    PacingRole,
    PlaceCandidate,
    TasteSignature,
    ThemeAnchor,
    VibeTag,
    VibeWeight,
)

# --------------------------------------------------------------------------- #
# Fake Anthropic client (mirrors the test_intake.py pattern)                  #
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
        self.calls.append(
            {
                "model": model,
                "max_tokens": max_tokens,
                "system_first_120": system[:120],
                "user_message_full": messages[0]["content"],
            }
        )
        if not self.queued_texts:
            raise RuntimeError("FakeMessages exhausted; queue more responses")
        text = self.queued_texts.pop(0)
        return _FakeMessage(content=[_FakeTextBlock(text=text)])


@dataclass
class _FakeClient:
    messages: _FakeMessages = field(default_factory=_FakeMessages)

    def queue(self, *texts: str) -> None:
        self.messages.queued_texts.extend(texts)


# --------------------------------------------------------------------------- #
# Fixtures                                                                    #
# --------------------------------------------------------------------------- #


def _mia_concept() -> Concept:
    return Concept(
        concept_id="cultural_restorative_test",
        day_theme="旧湾区的安静一天",
        mood_tags=["reflective", "warm"],
        arc_signature="慢起 → 呼吸 → 烟火气 → 早收",
        pacing_blueprint=[
            PacingRole.OPENING,
            PacingRole.BREATHING,
            PacingRole.PEAK,
            PacingRole.CLOSING,
        ],
        anchor_place_ids=["alviso_adobe", "sandy_wool_lake"],
        emotional_thesis="安静历史 + 自然呼吸，最 low-key 的一版。",
        theme_anchor=ThemeAnchor.CULTURAL_RESTORATIVE,
    )


def _two_candidates() -> list[PlaceCandidate]:
    return [
        PlaceCandidate(
            place_id="alviso_adobe",
            name="Alviso Adobe Park",
            fit_score=0.9,
            fit_reason="matches: quiet 0.9 / cultural 0.8",
            place_type="point_of_attraction",
            city="Milpitas",
            address="2087 Alviso Adobe Ct",
            hours_note="2nd Sat tour 14:30",
            narrative_hook="A 19th-century adobe house preserved as a small history room.",
        ),
        PlaceCandidate(
            place_id="sandy_wool_lake",
            name="Sandy Wool Lake (Ed Levin Park)",
            fit_score=0.85,
            fit_reason="matches: outdoor 0.9 / quiet 0.7",
            place_type="point_of_attraction",
            city="Milpitas",
            address="901 Downing Rd",
            narrative_hook="A reservoir-turned-park with bird-watching and gentle loops.",
        ),
    ]


def _mia_state() -> IntakeState:
    """Minimal state with a TasteSignature so serialize_for_composer succeeds."""
    state = IntakeState()
    ts = TasteSignature(
        vibe_weights=[
            VibeWeight(tag=VibeTag.QUIET, weight=0.9),
            VibeWeight(tag=VibeTag.WARM, weight=0.7),
        ],
        summary="Quiet, slow, warm.",
        confidence=0.9,
    )
    return state.model_copy(
        update={
            "taste_signature": TasteSignatureSlot(
                value=ts, confidence=0.9, provenance="inferred_from_screenshots"
            )
        }
    )


def _good_response_with_sidecar() -> str:
    """LLM response with markdown + valid PLAN_META sidecar."""
    return """## 旧湾区的安静一天

> **一句话 pitch**: 安静历史 + 湖边呼吸 + 早收。

## 14:30 · Alviso Adobe Park
> A quiet adobe with sun-warmed walls.

**Why this fits today**
你说今天最不想要"网红打卡感"——Alviso 的 tour 一次只 8 个人。
*regulates a nervous system that's been firing on Slack all week.*

## 15:30 · Sandy Wool Lake (Ed Levin Park)
> Reservoir-turned-park, bird-watching, stroller loops.

**Why this fits today**
你 liked_examples 写过 Tomales Bay —— 同样的"宽敞、无表演"气质。
*opens a quiet outdoor pocket between the morning and dinner.*

<!-- PLAN_META {"day_theme": "旧湾区的安静一天", "pitch": "安静历史 + 湖边呼吸 + 早收。", "theme_anchor": "cultural_restorative", "mood_tags": ["reflective", "warm"], "emotional_arc": ["慢起", "呼吸", "烟火气", "早收"], "stop_place_ids": ["alviso_adobe", "sandy_wool_lake"], "stop_names": ["Alviso Adobe Park", "Sandy Wool Lake (Ed Levin Park)"], "adaptive_branches": [{"condition": "宝宝累了", "alternative": "skip Sandy Wool, 直接回家"}], "composer_note": ""} -->
"""


def _response_no_sidecar() -> str:
    """Same plan but the LLM forgot the sidecar (triggers fallback)."""
    return """## 旧湾区的安静一天

> **一句话 pitch**: fallback test.

## 14:30 · Alviso Adobe Park
narrative...

## 15:30 · Sandy Wool Lake (Ed Levin Park)
narrative...
"""


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_run_with_good_sidecar_populates_all_fields() -> None:
    client = _FakeClient()
    client.queue(_good_response_with_sidecar())
    composer = PlanComposer(anthropic_client=client)
    plan = await composer.run(_mia_concept(), _two_candidates(), _mia_state())

    assert plan.day_theme == "旧湾区的安静一天"
    assert "湖边呼吸" in plan.pitch
    assert plan.theme_anchor == ThemeAnchor.CULTURAL_RESTORATIVE
    assert plan.stop_place_ids == ["alviso_adobe", "sandy_wool_lake"]
    assert "Alviso Adobe Park" in plan.stop_names
    assert plan.adaptive_branches[0]["condition"] == "宝宝累了"
    # Sidecar comment should be stripped from user-facing markdown.
    assert "<!-- PLAN_META" not in plan.markdown
    # But the body should remain.
    assert "Alviso Adobe Park" in plan.markdown


@pytest.mark.asyncio
async def test_sidecar_stripped_from_markdown_only() -> None:
    client = _FakeClient()
    client.queue(_good_response_with_sidecar())
    composer = PlanComposer(anthropic_client=client)
    plan = await composer.run(_mia_concept(), _two_candidates(), _mia_state())
    # Comment gone from markdown
    assert "PLAN_META" not in plan.markdown
    # Metadata captured into raw_metadata
    assert plan.raw_metadata.get("day_theme") == "旧湾区的安静一天"


@pytest.mark.asyncio
async def test_fallback_when_sidecar_missing() -> None:
    """Missing sidecar triggers retry, retry also missing -> regex fallback."""
    client = _FakeClient()
    # Queue twice: first attempt no sidecar, retry also no sidecar.
    client.queue(_response_no_sidecar(), _response_no_sidecar())
    composer = PlanComposer(anthropic_client=client)
    plan = await composer.run(_mia_concept(), _two_candidates(), _mia_state())

    # Day theme extracted via regex fallback
    assert plan.day_theme == "旧湾区的安静一天"
    # Stop names extracted from ## HH:MM · Name lines
    assert "Alviso Adobe Park" in plan.stop_names
    # Place IDs back-filled via name lookup against candidate pool
    assert plan.stop_place_ids[0] == "alviso_adobe"
    assert plan.stop_place_ids[1] == "sandy_wool_lake"


@pytest.mark.asyncio
async def test_malformed_json_in_sidecar_triggers_retry() -> None:
    """First call has broken JSON in sidecar; retry succeeds."""
    broken = (
        "## title\n\n> **一句话 pitch**: x\n\n"
        "## 14:30 · X\n\n<!-- PLAN_META {not valid json} -->\n"
    )
    client = _FakeClient()
    client.queue(broken, _good_response_with_sidecar())
    composer = PlanComposer(anthropic_client=client)
    plan = await composer.run(_mia_concept(), _two_candidates(), _mia_state())
    assert plan.day_theme == "旧湾区的安静一天"
    assert len(client.messages.calls) == 2  # made 2 calls (initial + retry)


@pytest.mark.asyncio
async def test_composer_prompt_loaded_from_disk() -> None:
    """The composer prompt is loaded from agent/prompts/composer.md."""
    client = _FakeClient()
    client.queue(_good_response_with_sidecar())
    composer = PlanComposer(anthropic_client=client)
    await composer.run(_mia_concept(), _two_candidates(), _mia_state())
    # The system prompt sent should be the composer.md content,
    # which contains the "Day Composer" role definition.
    first_call = client.messages.calls[0]
    assert "Day Composer" in first_call["system_first_120"]


@pytest.mark.asyncio
async def test_theme_anchor_propagates_to_user_message() -> None:
    """The Concept's theme_anchor should appear in the user message."""
    client = _FakeClient()
    client.queue(_good_response_with_sidecar())
    composer = PlanComposer(anthropic_client=client)
    await composer.run(_mia_concept(), _two_candidates(), _mia_state())
    first_call = client.messages.calls[0]
    assert "cultural_restorative" in first_call["user_message_full"]


@pytest.mark.asyncio
async def test_candidate_selection_anchors_first() -> None:
    """Anchor place_ids must appear in the user message before fillers."""
    client = _FakeClient()
    client.queue(_good_response_with_sidecar())
    composer = PlanComposer(anthropic_client=client)
    # Add a filler candidate with higher fit_score; anchor should still come first.
    extra = PlaceCandidate(
        place_id="filler_high_fit",
        name="Filler",
        fit_score=0.99,
        fit_reason="filler",
    )
    candidates = [extra, *_two_candidates()]
    await composer.run(_mia_concept(), candidates, _mia_state())
    # Build same selection ourselves to confirm ordering
    selected = composer._select_candidates(_mia_concept(), candidates)
    assert [c.place_id for c in selected[:2]] == ["alviso_adobe", "sandy_wool_lake"]
    assert "filler_high_fit" in [c.place_id for c in selected]


@pytest.mark.asyncio
async def test_stub_mode_when_no_client() -> None:
    """PlanComposer with anthropic_client=None returns Phase 0 stub."""
    composer = PlanComposer(anthropic_client=None)
    plan = await composer.run(_mia_concept(), _two_candidates(), _mia_state())
    assert plan.raw_metadata.get("stub") is True
    assert plan.day_theme == "旧湾区的安静一天"
    assert len(plan.stop_place_ids) == 4
    assert "stub mode" in plan.markdown


@pytest.mark.live
@pytest.mark.asyncio
async def test_live_smoke_real_anthropic_api() -> None:
    """LIVE smoke: real Anthropic call, manual quality inspection of the plan.

    Requires RUN_LIVE_LLM=1 + ANTHROPIC_API_KEY. Skipped by default via the
    conftest.py auto-skip. Burns ~$0.05.
    """
    import os

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY not set")
    from anthropic import AsyncAnthropic  # type: ignore[import-not-found]

    client = AsyncAnthropic(api_key=api_key)
    state = _mia_state()
    request = serialize_to_experience_request(state)
    candidates = await search_places(request)
    concepts = generate_concepts_simple(state, candidates)
    composer = PlanComposer(anthropic_client=client)
    plan = await composer.run(concepts[0], candidates, state)

    assert plan.markdown.strip()
    assert plan.day_theme
    assert len(plan.stop_place_ids) >= 1
    # No PLAN_META leakage to the user-facing markdown
    assert "PLAN_META" not in plan.markdown


# Helper to keep the queue draining test honest if `Iterable` ever changes.
def _flush(it: Iterable[Any]) -> None:
    for _ in it:
        pass
