"""Phase 1b tests — Intake Orchestrator + LLM tool seams.

The Anthropic client is injected so we run all tests with a deterministic
fake client (no network, no API key, no cassettes required). The fake
mirrors the `messages.create(...)` coroutine surface and returns scripted
responses keyed by call-order or by model.

Why no pytest-vcr cassettes here:
  Cassettes require an initial live recording pass with a real API key.
  For a Phase 1b deliverable that must run deterministically in CI before
  any live recording exists, a typed fake is more reliable. The `--live`
  smoke test at the bottom is the contract that catches model-drift if
  the user later turns on `RUN_LIVE_LLM=1` with a real key. If cassettes
  are added later, the fake can be retired in favor of `pytest-vcr`'s
  cassette replay — both honor the same `messages.create(...)` shape.
"""

from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any

import pytest

from agent.intake.orchestrator import InitialInput, IntakeOrchestrator
from agent.state import IntakeState, serialize_to_experience_request
from agent.types import ExperienceRequest

# ---------------------------------------------------------------------------
# Fake Anthropic client
# ---------------------------------------------------------------------------


@dataclass
class _FakeContentBlock:
    type: str
    text: str


@dataclass
class _FakeResponse:
    content: list[_FakeContentBlock]


@dataclass
class _FakeMessages:
    """Routes `messages.create(...)` to a scripted response.

    The routing rule is: if the model name starts with `claude-haiku-`,
    take the next response from the `extractor_queue`; if it starts with
    `claude-sonnet-` AND the request carries an image block, take from
    `vision_queue`; else take from `qgen_queue`. This avoids brittle
    per-call-index assertions.
    """

    extractor_queue: list[str] = field(default_factory=list)
    vision_queue: list[str] = field(default_factory=list)
    qgen_queue: list[str] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)

    async def create(self, *, model: str, messages: list[dict[str, Any]], **_: Any) -> _FakeResponse:
        has_image = False
        for msg in messages:
            content = msg.get("content")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "image":
                        has_image = True
                        break
        if model.startswith("claude-haiku-"):
            queue = self.extractor_queue
            kind = "extractor"
        elif has_image:
            queue = self.vision_queue
            kind = "vision"
        else:
            queue = self.qgen_queue
            kind = "qgen"
        if not queue:
            raise AssertionError(
                f"FakeMessages: no scripted response left in {kind}_queue "
                f"(model={model}, has_image={has_image})"
            )
        text = queue.pop(0)
        self.calls.append({"kind": kind, "model": model, "text": text})
        return _FakeResponse(content=[_FakeContentBlock(type="text", text=text)])


@dataclass
class _FakeAnthropicClient:
    messages: _FakeMessages = field(default_factory=_FakeMessages)


# ---------------------------------------------------------------------------
# Scripted-user helper
# ---------------------------------------------------------------------------


def _scripted_user(replies: list[str]) -> Callable[[], Awaitable[str]]:
    pending = list(replies)

    async def _read() -> str:
        if not pending:
            return ""  # signals user_escape to the orchestrator
        return pending.pop(0)

    return _read


def _sink_emit() -> tuple[list[str], Callable[[str], Awaitable[None]]]:
    sink: list[str] = []

    async def _emit(q: str) -> None:
        sink.append(q)

    return sink, _emit


# ---------------------------------------------------------------------------
# Slot-update JSON builders (so tests stay readable)
# ---------------------------------------------------------------------------


def _mia_turn1_updates() -> str:
    return json.dumps(
        {
            "emotional_intent": {
                "values": ["restore", "explore"],
                "confidence": 0.85,
                "provenance": "user_stated",
            },
            "social_config": {
                "values": ["family_with_baby"],
                "confidence": 0.7,
                "provenance": "user_implied",
            },
            "energy_profile": {
                "energy_level": {"value": "medium", "confidence": 0.7, "provenance": "user_implied"},
                "chaos_tolerance": {"value": "low", "confidence": 0.75, "provenance": "user_implied"},
            },
            "practical_constraints": {
                "kid_friendly": {"value": True, "confidence": 0.8, "provenance": "user_implied"},
                "needs_parking": {"value": True, "confidence": 0.7, "provenance": "user_implied"},
            },
            "emotional_intent_rationale": "Tired but doesn't want to flat-out rest; wants a touch of novelty.",
        }
    )


def _mia_turn2_updates() -> str:
    return json.dumps(
        {
            "practical_constraints": {
                "start_location": {"value": "Mountain View", "confidence": 0.95, "provenance": "user_stated"},
                "time_window": {"value": "14:00-21:00", "confidence": 0.9, "provenance": "user_stated"},
                "max_drive_minutes": {"value": 45, "confidence": 0.85, "provenance": "user_stated"},
                "budget": {"value": "flexible", "confidence": 0.7, "provenance": "user_implied"},
            },
            "energy_profile": {
                "novelty_appetite": {"value": "high", "confidence": 0.85, "provenance": "user_stated"},
            },
        }
    )


def _mia_turn3_updates() -> str:
    return json.dumps(
        {
            "taste_anchors": {
                "desired_vibe": {
                    "values": ["quiet", "warm", "intimate", "cultural"],
                    "confidence": 0.85,
                    "provenance": "user_stated",
                },
            },
            "avoidance": {
                "values": ["touristy", "loud", "queued", "rushed"],
                "confidence": 0.9,
                "provenance": "user_stated",
            },
            "avoidance_rationale": "Crowds + waits would defeat the recovery goal.",
            # User signals they're done — natural way to reach READY in a
            # text-only session (no images means taste_signature.confidence
            # stays at 0, so router's avg/min rule cannot trigger READY).
            "stopped_reason": "user_escape",
        }
    )


def _garry_turn1_updates() -> str:
    return json.dumps(
        {
            "emotional_intent": {
                "values": ["explore", "reconnect"],
                "confidence": 0.85,
                "provenance": "user_stated",
            },
            "social_config": {
                "values": ["family_with_baby"],
                "confidence": 0.8,
                "provenance": "user_stated",
            },
            "energy_profile": {
                "energy_level": {"value": "high", "confidence": 0.85, "provenance": "user_stated"},
                "chaos_tolerance": {"value": "medium", "confidence": 0.7, "provenance": "user_implied"},
                "novelty_appetite": {"value": "high", "confidence": 0.8, "provenance": "user_implied"},
            },
            "practical_constraints": {
                "start_location": {"value": "San Francisco", "confidence": 0.95, "provenance": "user_stated"},
            },
        }
    )


def _garry_turn2_updates() -> str:
    return json.dumps(
        {
            "practical_constraints": {
                "time_window": {"value": "09:00-21:00", "confidence": 0.85, "provenance": "user_stated"},
                "max_drive_minutes": {"value": 30, "confidence": 0.7, "provenance": "user_implied"},
                "kid_friendly": {"value": True, "confidence": 0.8, "provenance": "user_stated"},
                "needs_parking": {"value": False, "confidence": 0.7, "provenance": "user_implied"},
                "budget": {"value": "flexible", "confidence": 0.75, "provenance": "user_implied"},
            },
        }
    )


def _garry_turn3_updates() -> str:
    return json.dumps(
        {
            "taste_anchors": {
                "desired_vibe": {
                    "values": ["lively", "cinematic", "cultural", "authentic", "hip"],
                    "confidence": 0.88,
                    "provenance": "user_stated",
                },
            },
            "avoidance": {
                "values": ["touristy", "rushed"],
                "confidence": 0.85,
                "provenance": "user_stated",
            },
            "stopped_reason": "user_escape",
        }
    )


def _alex_turn1_updates() -> str:
    return json.dumps(
        {
            "emotional_intent": {
                "values": ["explore", "feel_alive", "celebrate"],
                "confidence": 0.9,
                "provenance": "user_stated",
            },
            "social_config": {
                "values": ["solo"],
                "confidence": 0.8,
                "provenance": "user_stated",
            },
            "energy_profile": {
                "energy_level": {"value": "high", "confidence": 0.9, "provenance": "user_stated"},
                "chaos_tolerance": {"value": "high", "confidence": 0.85, "provenance": "user_stated"},
                "novelty_appetite": {"value": "high", "confidence": 0.9, "provenance": "user_stated"},
            },
            "practical_constraints": {
                "start_location": {"value": "Lower Haight, San Francisco", "confidence": 0.95, "provenance": "user_stated"},
                "transport": {"value": "transit", "confidence": 0.85, "provenance": "user_implied"},
                "max_drive_minutes": {"value": 0, "confidence": 0.8, "provenance": "user_implied"},
            },
        }
    )


def _alex_turn2_updates() -> str:
    return json.dumps(
        {
            "practical_constraints": {
                "time_window": {"value": "09:30-23:30", "confidence": 0.85, "provenance": "user_stated"},
                "budget": {"value": "moderate", "confidence": 0.8, "provenance": "user_stated"},
                "kid_friendly": {"value": False, "confidence": 0.7, "provenance": "user_implied"},
                "needs_parking": {"value": False, "confidence": 0.9, "provenance": "user_stated"},
            },
        }
    )


def _alex_turn3_updates() -> str:
    return json.dumps(
        {
            "taste_anchors": {
                "desired_vibe": {
                    "values": ["lively", "authentic", "walkable", "social", "hip"],
                    "confidence": 0.88,
                    "provenance": "user_stated",
                },
            },
            "avoidance": {
                "values": ["touristy", "overcrowded"],
                "confidence": 0.9,
                "provenance": "user_stated",
            },
            "stopped_reason": "user_escape",
        }
    )


# ---------------------------------------------------------------------------
# Per-persona happy-path tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_mia_intake_reaches_ready_in_few_turns() -> None:
    client = _FakeAnthropicClient()
    # 3 user turns; Extractor is called once per turn (including the initial text).
    client.messages.extractor_queue = [
        _mia_turn1_updates(),
        _mia_turn2_updates(),
        _mia_turn3_updates(),
    ]
    client.messages.qgen_queue = [
        "听起来这周挺重的——你想从 Mountain View 出发，大概几点开始几点回？",
        "明白要带宝宝且不想折腾——今天最不能接受的是什么？比如人多、排队、还是开车太远？",
    ]
    sink, emit = _sink_emit()
    initial = InitialInput(
        text="这周有点累，但我不想只是躺平。帮我安排一个周六吧，最好有点漂亮、有点好吃、宝宝也可能一起。",
        images=[],
    )
    orch = IntakeOrchestrator(
        anthropic_client=client,
        read_user_turn=_scripted_user(
            [
                "从 Mountain View 出发，下午 2 点到晚上 9 点这段。开车 45 分钟以内。",
                "最怕排队和人多，宝宝也不能在那种地方待太久。喜欢安静一点、有质感的地方。",
            ]
        ),
        emit_question=emit,
    )
    state = await orch.run(initial)

    # READY via user_escape (text-only sessions can't hit "sufficient_info"
    # because taste_signature.confidence stays at 0 without images, breaking
    # router's `min(confidence) >= 0.5` rule).
    assert state.stopped_reason == "user_escape"
    assert state.turn_count <= 6
    assert state.emotional_intent.confidence >= 0.8
    assert state.avoidance.confidence >= 0.8
    assert len(sink) == 2  # one question per follow-up
    # The orchestrator's serializer must produce a structurally valid request.
    req: ExperienceRequest = serialize_to_experience_request(state)
    assert req.experience_intent["primary_mood"]


@pytest.mark.asyncio
async def test_garry_intake_reaches_ready_in_few_turns() -> None:
    client = _FakeAnthropicClient()
    client.messages.extractor_queue = [
        _garry_turn1_updates(),
        _garry_turn2_updates(),
        _garry_turn3_updates(),
    ]
    client.messages.qgen_queue = [
        "听起来这周脑子被 AI 填满——大概是哪几个小时段，想怎么排？",
        "明白要带孩子且想找 local 灵感——今天最不能接受什么？",
    ]
    sink, emit = _sink_emit()
    initial = InitialInput(
        text="YC 开训这周脑子全被 AI 填满了。周六想在 SF 城区里整点真正厉害的拉面或者亚洲融合菜，顺便拍点好看的 Vlog 素材。",
        images=[],
    )
    orch = IntakeOrchestrator(
        anthropic_client=client,
        read_user_turn=_scripted_user(
            [
                "早上 9 点到晚上 9 点，不开太远，30 分钟以内。带娃但娃能跟得上。",
                "最怕被推荐 touristy 的、没本地灵魂的地方。要 local 要 hip。",
            ]
        ),
        emit_question=emit,
    )
    state = await orch.run(initial)

    assert state.stopped_reason == "user_escape"
    assert state.emotional_intent.confidence >= 0.8
    assert state.energy_profile.energy_level.confidence >= 0.8


@pytest.mark.asyncio
async def test_alex_intake_reaches_ready_in_few_turns() -> None:
    client = _FakeAnthropicClient()
    client.messages.extractor_queue = [
        _alex_turn1_updates(),
        _alex_turn2_updates(),
        _alex_turn3_updates(),
    ]
    client.messages.qgen_queue = [
        "刚搬来 3 周还在 honeymoon——今天大概想从早到晚走多久？",
        "明白要 local 不要游客陷阱——今天最不能接受什么？",
    ]
    sink, emit = _sink_emit()
    initial = InitialInput(
        text="刚搬来 SF 三周一个地方都还没去，今天想暴走一天，最好是真的 local 会去的那种。预算不要太离谱，没车，从 Lower Haight 出发。",
        images=[],
    )
    orch = IntakeOrchestrator(
        anthropic_client=client,
        read_user_turn=_scripted_user(
            [
                "早上 9 点半出门，到深夜没问题。预算 moderate，没车也不需要 parking。",
                "最不能接受 chain restaurant 和 touristy 的地方。",
            ]
        ),
        emit_question=emit,
    )
    state = await orch.run(initial)

    assert state.stopped_reason == "user_escape"
    assert state.emotional_intent.confidence >= 0.85


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_user_escape_short_circuits_to_ready() -> None:
    """User saying '好了 / 直接给我看 plan' -> READY via stopped_reason='user_escape'."""
    client = _FakeAnthropicClient()
    # Only the first turn's extractor call happens; the user-escape signal
    # is emitted in that same extractor response.
    client.messages.extractor_queue = [
        json.dumps(
            {
                "emotional_intent": {
                    "values": ["restore"],
                    "confidence": 0.6,
                    "provenance": "user_stated",
                },
                "stopped_reason": "user_escape",
            }
        ),
    ]
    sink, emit = _sink_emit()
    orch = IntakeOrchestrator(
        anthropic_client=client,
        read_user_turn=_scripted_user([]),
        emit_question=emit,
    )
    state = await orch.run(InitialInput(text="不要再问了，直接给我看 plan。", images=[]))
    assert state.stopped_reason == "user_escape"
    assert sink == []  # no questions asked
    # Router treats user_escape as READY; serializer should still work.
    req = serialize_to_experience_request(state)
    assert isinstance(req, ExperienceRequest)


@pytest.mark.asyncio
async def test_hard_cap_at_10_turns() -> None:
    """If the extractor never raises confidence enough, we must stop at turn 10."""
    client = _FakeAnthropicClient()
    # Every extract call emits a deliberately-low confidence update — confidence
    # never crosses 0.8, so router keeps asking.
    low_update = json.dumps(
        {
            "emotional_intent": {
                "values": ["explore"],
                "confidence": 0.3,
                "provenance": "user_implied",
            }
        }
    )
    # The router increments turn_count via merge_slot_updates; hard cap fires
    # at turn_count >= 10. Our orchestrator's max_turns=12 guards the loop.
    # Pad both queues so they can never be exhausted before the cap.
    client.messages.extractor_queue = [low_update] * 15
    client.messages.qgen_queue = ["再问一句？"] * 15
    sink, emit = _sink_emit()
    orch = IntakeOrchestrator(
        anthropic_client=client,
        read_user_turn=_scripted_user(["..."] * 15),
        emit_question=emit,
    )
    state = await orch.run(InitialInput(text="嗯。", images=[]))
    assert state.stopped_reason == "hard_cap"
    assert state.turn_count >= 10


@pytest.mark.asyncio
async def test_empty_image_paths_skips_vision_cleanly() -> None:
    client = _FakeAnthropicClient()
    client.messages.extractor_queue = [
        json.dumps(
            {
                "emotional_intent": {
                    "values": ["restore"],
                    "confidence": 0.6,
                    "provenance": "user_stated",
                },
                "stopped_reason": "user_escape",
            }
        )
    ]
    sink, emit = _sink_emit()
    orch = IntakeOrchestrator(
        anthropic_client=client,
        read_user_turn=_scripted_user([]),
        emit_question=emit,
    )
    state = await orch.run(InitialInput(text="just give me the plan", images=[]))
    # No vision call must have been recorded.
    vision_calls = [c for c in client.messages.calls if c["kind"] == "vision"]
    assert vision_calls == []
    # TasteSignature stayed at default (empty).
    assert state.taste_signature.value.vibe_weights == []
    assert state.taste_signature.confidence == 0.0


@pytest.mark.asyncio
async def test_vision_path_invoked_when_images_provided(tmp_path: Any) -> None:
    # Create a tiny valid PNG so the encoder doesn't error.
    png = tmp_path / "scene.png"
    # 1x1 transparent PNG (smallest valid).
    png.write_bytes(
        bytes.fromhex(
            "89504E470D0A1A0A0000000D49484452000000010000000108060000001F15C4"
            "890000000A49444154789C6300010000000500010D0A2DB40000000049454E44"
            "AE426082"
        )
    )
    client = _FakeAnthropicClient()
    client.messages.vision_queue = [
        json.dumps(
            {
                "vibe_weights": [
                    {"tag": "quiet", "weight": 0.8},
                    {"tag": "warm", "weight": 0.7},
                    {"tag": "intimate", "weight": 0.6},
                ],
                "summary": "leaning quiet/warm/intimate",
                "confidence": 0.72,
            }
        )
    ]
    client.messages.extractor_queue = [
        json.dumps(
            {
                "emotional_intent": {
                    "values": ["restore"],
                    "confidence": 0.7,
                    "provenance": "user_stated",
                },
                "stopped_reason": "user_escape",
            }
        )
    ]
    sink, emit = _sink_emit()
    orch = IntakeOrchestrator(
        anthropic_client=client,
        read_user_turn=_scripted_user([]),
        emit_question=emit,
    )
    state = await orch.run(InitialInput(text="just plan it", images=[str(png)]))
    # Vision must have been called exactly once.
    vision_calls = [c for c in client.messages.calls if c["kind"] == "vision"]
    assert len(vision_calls) == 1
    assert state.taste_signature.value.confidence == pytest.approx(0.72)
    assert state.taste_signature.confidence == pytest.approx(0.72)
    assert state.stopped_reason == "user_escape"


@pytest.mark.asyncio
async def test_vision_retries_once_then_returns_empty() -> None:
    """First two vision attempts both fail to parse -> empty TasteSignature."""
    import tempfile
    from pathlib import Path

    from agent.tools.vision import vision_extract_taste

    with tempfile.TemporaryDirectory() as td:
        png = Path(td) / "s.png"
        png.write_bytes(
            bytes.fromhex(
                "89504E470D0A1A0A0000000D49484452000000010000000108060000001F15C4"
                "890000000A49444154789C6300010000000500010D0A2DB40000000049454E44"
                "AE426082"
            )
        )
        client = _FakeAnthropicClient()
        client.messages.vision_queue = [
            "I cannot read these images, sorry.",
            "Still cannot, here is some prose.",
        ]
        result = await vision_extract_taste([str(png)], client)
        assert result.vibe_weights == []
        assert result.confidence == 0.0
        # 2 attempts must have been recorded
        vision_calls = [c for c in client.messages.calls if c["kind"] == "vision"]
        assert len(vision_calls) == 2


@pytest.mark.asyncio
async def test_lowest_confidence_slot_drives_targeting() -> None:
    """The Q-Gen target_slot reflects the lowest-confidence dim."""
    from agent.state import merge_slot_updates
    from agent.tools.qgen import lowest_confidence_slot

    state = IntakeState()
    state = merge_slot_updates(
        state,
        {
            "emotional_intent": {
                "values": ["restore"],
                "confidence": 0.9,
                "provenance": "user_stated",
            }
        },
    )
    # Everything else is 0 — emotional_intent at 0.9, social_config at 0,
    # so social_config (next in priority order) should win.
    assert lowest_confidence_slot(state) == "social_config"


# ---------------------------------------------------------------------------
# Live smoke (skipped unless RUN_LIVE_LLM=1)
# ---------------------------------------------------------------------------


@pytest.mark.live
@pytest.mark.asyncio
async def test_mia_live_smoke() -> None:
    """End-to-end Mia flow against real Anthropic. ~$0.05, gated on RUN_LIVE_LLM=1."""
    import os

    from anthropic import AsyncAnthropic

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        pytest.skip("ANTHROPIC_API_KEY not set")
    client = AsyncAnthropic(api_key=api_key)
    sink, emit = _sink_emit()
    replies = [
        "从 Mountain View 出发，下午 2 点到晚上 9 点这段。开车 45 分钟以内，带宝宝。",
        "最怕排队和人多。喜欢安静一点、有质感、好吃但不折腾的地方。",
        "好了，直接给我看 plan。",
    ]
    orch = IntakeOrchestrator(
        anthropic_client=client,
        read_user_turn=_scripted_user(replies),
        emit_question=emit,
    )
    state = await orch.run(
        InitialInput(
            text="这周有点累，但我不想只是躺平。帮我安排一个周六吧，最好有点漂亮、有点好吃、宝宝也可能一起。",
            images=[],
        )
    )
    print("final state:", state.model_dump_json(indent=2))
    assert state.stopped_reason in ("sufficient_info", "user_escape", "hard_cap")
    assert state.turn_count > 0
