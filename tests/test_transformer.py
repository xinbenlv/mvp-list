"""Tests for `agent.present.transformer` — the PlanResult → frontend dict bridge.

The shape contract under test is documented in
`day-composer-app/lib/types/trip-plan.ts` + `poc-demo/garry-demo/HANDOFF.md`.
We pin top-level keys, the emotional_arc reshape, the per-stop dump including
order_recommendations being preserved for restaurants and null for non-
restaurants, and the markdown_full passthrough.
"""

from __future__ import annotations

from agent.present.transformer import build_envelope, plan_result_to_frontend_dict
from agent.types import (
    BookingLink,
    Logistics,
    OrderRecs,
    PlanResult,
    Stop,
    ThemeAnchor,
)


def _make_plan() -> PlanResult:
    """Build a PlanResult with one restaurant stop + one non-restaurant stop.

    Tight enough to assert against, rich enough to exercise the reshape rules
    and the order_recommendations null vs non-null branching.
    """
    restaurant = Stop(
        stop_index=0,
        time="18:00",
        place_id="dong_que",
        place_name="Dong Que",
        one_liner="A Saigon street-stall in disguise.",
        why_fits_today="你 food_preferences 写过越南菜 — Dong Que 是 authentic 的代表。",
        logistics=Logistics(
            raw="🚗 25min · 🅿️ free · 👶 high chairs",
            drive_time_min=25,
            parking="free",
            kid_friendly=True,
            reservation_note="walk-in only",
            booking_links=[],
            transit_estimate_usd=60,
        ),
        order_recommendations=OrderRecs(
            menu_listed=["15 锅巴饭", "88 烤生蚝"],
            bold_picks=["15 锅巴饭"],
            logic_text="**15 锅巴饭** 招牌不点白来。",
        ),
        tip="ask for high chair upfront",
        transition_to_next="warm dinner → drive-home coda",
        transition_drive_min=10,
    )
    non_restaurant = Stop(
        stop_index=1,
        time="20:00",
        place_id="philz_milpitas",
        place_name="Philz Coffee",
        one_liner="A hot coffee on the way home.",
        why_fits_today="顺路、不催你 — 这一杯 closes the loop。",
        logistics=Logistics(
            raw="🚗 顺路 · 🅿️ 免费",
            drive_time_min=None,
            parking="free",
            kid_friendly=True,
            booking_links=[BookingLink(label="Order ahead", url="https://philz.com")],
        ),
        order_recommendations=None,
        tip=None,
        transition_to_next=None,
        transition_drive_min=None,
    )
    return PlanResult(
        markdown="## stub markdown\n\nbody...",
        day_theme="South Bay decompression",
        pitch="A low-key version with one warm dinner.",
        theme_anchor=ThemeAnchor.CULTURAL_RESTORATIVE,
        mood_tags=["restorative", "warm"],
        emotional_arc=["slow start", "lakeside drift", "neighborhood heat", "easy close"],
        stop_place_ids=["dong_que", "philz_milpitas"],
        stop_names=["Dong Que", "Philz Coffee"],
        stops=[restaurant, non_restaurant],
        adaptive_branches=[
            {"condition": "kid is fussy", "alternative": "skip to dinner early"}
        ],
        composer_note="",
    )


def test_top_level_keys_match_frontend_contract() -> None:
    """All keys in trip-plan.ts `TripPlan` must be present in the dict."""
    plan = _make_plan()
    out = plan_result_to_frontend_dict(
        plan, persona_id="garry", plan_id="garry_test_day"
    )
    required = {
        "plan_id",
        "persona_id",
        "version",
        "day_theme",
        "theme_anchor",
        "pitch",
        "mood_tags",
        "emotional_arc_text",
        "emotional_arc_visual",
        "stops",
        "adaptive_branches",
        "markdown_full",
        "coaching_block",
        "composer_note",
        "score_summary",
    }
    missing = required - out.keys()
    assert not missing, f"missing keys: {missing}"
    assert out["plan_id"] == "garry_test_day"
    assert out["persona_id"] == "garry"
    assert out["version"] == "v1"
    assert out["theme_anchor"] == "cultural_restorative"


def test_emotional_arc_list_reshapes_into_text() -> None:
    plan = _make_plan()
    out = plan_result_to_frontend_dict(
        plan, persona_id="garry", plan_id="garry_test_day"
    )
    assert out["emotional_arc_text"] == (
        "slow start → lakeside drift → neighborhood heat → easy close"
    )
    # visual is intentionally empty; frontend tolerates blank
    assert out["emotional_arc_visual"] == ""


def test_restaurant_stop_preserves_order_recommendations() -> None:
    plan = _make_plan()
    out = plan_result_to_frontend_dict(
        plan, persona_id="garry", plan_id="garry_test_day"
    )
    first = out["stops"][0]
    assert first["place_id"] == "dong_que"
    recs = first["order_recommendations"]
    assert recs is not None
    assert recs["menu_listed"] == ["15 锅巴饭", "88 烤生蚝"]
    assert recs["bold_picks"] == ["15 锅巴饭"]
    assert "**15 锅巴饭**" in recs["logic_text"]
    # logistics dumped 1:1
    assert first["logistics"]["raw"].startswith("🚗 25min")
    assert first["logistics"]["transit_estimate_usd"] == 60
    # image_url defaults to null so frontend renders gradient
    assert first["image_url"] is None


def test_non_restaurant_stop_has_null_order_recommendations() -> None:
    plan = _make_plan()
    out = plan_result_to_frontend_dict(
        plan, persona_id="garry", plan_id="garry_test_day"
    )
    second = out["stops"][1]
    assert second["place_id"] == "philz_milpitas"
    assert second["order_recommendations"] is None
    # Booking link dict shape preserved
    assert second["logistics"]["booking_links"] == [
        {"label": "Order ahead", "url": "https://philz.com"}
    ]
    # Trailing stop: transitions are null
    assert second["transition_to_next"] is None
    assert second["transition_drive_min"] is None


def test_markdown_full_populated_from_plan_markdown() -> None:
    plan = _make_plan()
    out = plan_result_to_frontend_dict(
        plan, persona_id="garry", plan_id="garry_test_day"
    )
    assert out["markdown_full"] == plan.markdown
    # coaching_block and composer_note nullable defaults
    assert out["coaching_block"] is None
    assert out["composer_note"] is None  # empty string normalized to None
    # score_summary stub with sentinel notes
    assert out["score_summary"]["stranger_test"] == 0
    assert "live LLM run" in out["score_summary"]["notes"]


def test_build_envelope_wraps_plan_and_trip_context() -> None:
    plan = _make_plan()
    trip_ctx = {"persona_id": "garry", "today_is": "2026-01-10"}
    env = build_envelope(
        plan,
        persona_id="garry",
        plan_id="garry_test_day",
        trip_context=trip_ctx,
    )
    assert set(env.keys()) == {"plan", "trip_context"}
    assert env["trip_context"] is trip_ctx
    assert env["plan"]["plan_id"] == "garry_test_day"


def test_empty_stops_yields_empty_array_not_error() -> None:
    """Stub mode produces no stops; transformer must not crash."""
    plan = PlanResult(
        markdown="## stub\n",
        day_theme="Stub",
        pitch="",
        theme_anchor=ThemeAnchor.CULTURAL_RESTORATIVE,
    )
    out = plan_result_to_frontend_dict(
        plan, persona_id="mia", plan_id="mia_stub"
    )
    assert out["stops"] == []
    assert out["emotional_arc_text"] == ""
    assert out["mood_tags"] == []
