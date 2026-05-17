import type { TripPlan } from "@/lib/types/trip-plan";

/**
 * English translation of the `mia_v1` plan from sample-plans.json.
 * Hand-translated for the demo (Aman/Vogue editorial register, not literal).
 *
 * Reference: /tmp/day-composer-en-translations.md + per-field guidance in
 * the mid-task pivot note. Place names, plan_id, persona_id, version,
 * theme_anchor, score_summary are kept as-is — internal metadata.
 *
 * Dish names: number kept, bilingual format "<number> <chinese> · <english>".
 */
export const SAMPLE_PLAN_MIA_V1_EN: TripPlan = {
  plan_id: "mia_v1",
  persona_id: "mia",
  version: "v1",
  day_theme: "A sun-warmed Saturday in the South Bay",
  pitch: null,
  mood_tags: [
    "restorative",
    "sun-warmed",
    "quietly cultural",
    "low-friction",
    "lingering",
  ],
  emotional_arc_text:
    "Slow start in light → lakeside drift → neighborhood heat → easy close",
  emotional_arc_visual:
    "🕰️ slow start ──► 🌿 breathing ──► 🍜 heat ──► ☕ afterglow\n14:30           15:45             18:00         20:00",
  theme_anchor: "cultural_restorative",
  stops: [
    {
      stop_index: 0,
      time: "14:30",
      place_id: "alviso_adobe",
      place_name: "Alviso Adobe Park",
      one_liner:
        "A 19th-century adobe turned into one small history-room. Western light comes in sideways, the roof beams are at arm's reach — 45 minutes is enough to slow the week down.",
      why_fits_today:
        "You said you wanted \"a little aesthetic / cultural spark, but nothing draining\" — Alviso runs eight people per tour, no one performing for cameras, which lands directly on your avoidance list (touristy, crowded). The adobe's natural light and quiet hit the top two weights in your vibe_signature (restorative 0.92 / cinematic 0.86) without burning the patience you already spent getting the baby out the door.",
      logistics: {
        raw: "🚗 22min from Sunnyvale · 🅿️ free parking · 👶 stroller-friendly (west entrance avoids the stone steps) · 🎟️ free, 2nd Saturday of the month 14:30 tour · ⏰ 45min is right",
        drive_time_min: 22,
        parking: "free",
        kid_friendly: true,
        reservation_note: "free, 2nd Saturday of the month 14:30 tour",
        booking_links: [],
        transit_estimate_usd: null,
      },
      order_recommendations: null,
      tip: "Take the west entrance with the stroller — skips the stone steps.",
      transition_to_next: "indoor narrative → outdoor breathing",
      transition_drive_min: 8,
    },
    {
      stop_index: 1,
      time: "15:45",
      place_id: "sandy_wool_lake",
      place_name: "Sandy Wool Lake (Ed Levin Park)",
      one_liner:
        "A reservoir reshaped into a park. Birds drifting, a few grandfathers fishing, a sub-1-mile walking loop, and the baby can sleep right in the car.",
      why_fits_today:
        "Your taste_anchors mention \"coastline, mountain views, gardens, lawns, spaces with strong natural light…  somewhere that pulls her down from cognitive overload.\" Sandy Wool isn't the coast, but it has the same quality: open, no performance, stroller-pushable. If the baby sleeps, you and your husband actually get a few uninterrupted minutes — the rare window where reconnect can happen on a baby-day.",
      logistics: {
        raw: "🚗 8min from Alviso · 🅿️ free at the circular lakeside lot · 👶 stroller-friendly · ⏰ sunset around 17:15, bring a jacket",
        drive_time_min: 8,
        parking: "free (circular lakeside lot)",
        kid_friendly: true,
        reservation_note: null,
        booking_links: [],
        transit_estimate_usd: null,
      },
      order_recommendations: null,
      tip: "The west bench has a view of small planes landing at KMTN — something for the baby to watch if she wakes up.",
      transition_to_next: "outdoor reset → appetite reopening",
      transition_drive_min: 25,
    },
    {
      stop_index: 2,
      time: "18:00",
      place_id: "dong_que",
      place_name: "Dong Que",
      one_liner:
        "One of the Bay Area's rare \"like a Saigon street stall\" Vietnamese places — order by menu number so you don't have to think, the lap cheong crispy rice is the signature.",
      why_fits_today:
        "The first two stops are in a low key; by dinner you need a little sound and heat to ground the day. Your food_preferences point to \"fusion / modern Asian / menus with expression\" — Dong Que isn't fine dining, but it has expression: numbered ordering eliminates decision fatigue, which goes around your avoidance of over_planned. 18:00 grabs a table while skipping the 7pm peak — fits your chaos_tolerance: low.",
      logistics: {
        raw: "🚗 25min from Sandy Wool · 🅿️ spacious outer lot · 👶 baby-friendly, high chairs · 💵 ~$60 for two · ⏰ walk-in only",
        drive_time_min: 25,
        parking: "outer lot, spacious",
        kid_friendly: true,
        reservation_note: "walk-in only",
        booking_links: [],
        transit_estimate_usd: 60,
      },
      order_recommendations: {
        menu_listed: [
          "88 烤生蚝 · grilled oyster",
          "92 鱼籽扇贝 · roe scallop",
          "15 香松腊肠锅巴饭 · lap cheong crispy rice",
          "103 铁板螺丝 · iron-plate snail",
        ],
        bold_picks: [
          "88 烤生蚝 · grilled oyster",
          "92 鱼籽扇贝 · roe scallop",
          "15 香松腊肠锅巴饭 · lap cheong crispy rice",
          "103 铁板螺丝 · iron-plate snail",
        ],
        logic_text:
          "Open with **88 烤生蚝 · grilled oyster** and **92 鱼籽扇贝 · roe scallop** — small, sharp, the palate wakes up. Anchor with **15 香松腊肠锅巴饭 · lap cheong crispy rice** (the signature; not ordering it is leaving without arriving — the crispy rice carries the day's pivot into heat). Add **103 铁板螺丝 · iron-plate snail** for one loud, hot plate — the first two stops were too quiet, this dish hits the table with sound. Two adults + baby splits this exactly; no leftovers.",
      },
      tip: "Ask the front desk for a bib and a high chair the moment you sit down — they won't offer.",
      transition_to_next: "high-noise dinner → low-key closing",
      transition_drive_min: 18,
    },
    {
      stop_index: 3,
      time: "20:00",
      place_id: "philz_milpitas",
      place_name: "Philz Coffee (Milpitas Square)",
      one_liner:
        "A hot coffee on the way home — no more decisions tonight. The barista remembers your Mint Mojito order.",
      why_fits_today:
        "You said energy is medium but chaos_tolerance is low, so today doesn't need a \"night activity\" to cap off — a coffee that's already on the way home is more respectful of where you are than a forced trip to standup. It lands on your ground_truth_expectations line about \"closing gently, not rushed, not messy, ideally with something warm.\" Philz doesn't hurry you, the baby is fine in the car, and the cup runs out exactly as you pull into Sunnyvale.",
      logistics: {
        raw: "🚗 on the way home (880 northbound) · 🅿️ free · 👶 fine · ⏰ open until 20:00, last order in time",
        drive_time_min: null,
        parking: "free",
        kid_friendly: true,
        reservation_note: null,
        booking_links: [],
        transit_estimate_usd: null,
      },
      order_recommendations: null,
      tip: null,
      transition_to_next: null,
      transition_drive_min: null,
    },
  ],
  adaptive_branches: [
    {
      condition:
        "If the baby gets fussy at Sandy Wool / misses the nap window and by 4pm she's already in car-reset mode",
      alternative:
        "Skip the rest of the Sandy Wool walk; head straight to Dong Que 30 min early at 17:00 (they open at 11:00, 17:00 is nearly empty). Take the window table so the baby has the street to look at, then bump Philz up to 19:00 — the whole arc compresses by an hour, you're home at the same time, and you can still be done bathing by 9pm.",
    },
  ],
  coaching_block: null,
  composer_note: null,
  markdown_full: "",
  score_summary: {
    stranger_test: 9,
    arc_coherence: 9,
    specificity: 9,
    avoidance_respect: 8,
    adaptive_branch: 9,
    notes: "v1 baseline",
  },
};
