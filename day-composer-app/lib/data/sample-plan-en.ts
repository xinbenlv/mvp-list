import type { TripContext, TripPlan } from "@/lib/types/trip-plan";

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

// ============================================================
// Garry demo set — three Saturdays, one persona
// ============================================================
// Garry: SF-based dad of a toddler, cinematic eye (vibe_signature 0.95),
// vlog-curious, design-driven. Three plans share the same persona but each
// hits a different mood / template:
//   1. family_day  → Polaroid    (South Bay decompression, family keepsake)
//   2. cultural_day → Cinematic  (SF art-day, magazine spread)
//   3. golden_night → Aurora     (SF cinematic with skybar closing)
// ============================================================

// ---------- 1. GARRY · FAMILY DAY (Polaroid) ----------

export const SAMPLE_PLAN_GARRY_FAMILY_DAY_EN: TripPlan = {
  plan_id: "garry_family_day",
  persona_id: "garry",
  version: "v1",
  day_theme: "A South Bay decompression",
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
        "You said you wanted \"a little aesthetic spark, but nothing draining\" — Alviso runs eight people per tour, no one performing for cameras, which lands directly on your avoidance list (touristy, crowded). The adobe's natural light and quiet hit the top of your vibe_signature (cinematic 0.95 / restorative 0.86) without burning the patience you already spent getting the toddler out the door. After a high-stim week in the city, this is the lowest-friction entry into Saturday.",
      logistics: {
        raw: "🚗 ~50min from SF · 🅿️ free parking · 👶 stroller-friendly (west entrance avoids the stone steps) · 🎟️ free, 2nd Saturday of the month 14:30 tour · ⏰ 45min is right",
        drive_time_min: 50,
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
        "A reservoir reshaped into a park. Birds drifting, a few grandfathers fishing, a sub-1-mile walking loop, and the kid can sleep right in the car.",
      why_fits_today:
        "Your taste_anchors mention coastline, mountain views, gardens, lawns — spaces with strong natural light that pull you down from cognitive overload. Sandy Wool isn't the coast, but it has the same quality: open, no performance, stroller-pushable. If the kid sleeps, you and your partner actually get a few uninterrupted minutes — the rare window where a real conversation can happen on a family-day. The west-facing benches double as a vlog C-roll position if the urge strikes.",
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
      tip: "The west bench has a view of small planes landing at KMTN — something for the kid to watch if he wakes up.",
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
        "The first two stops are in a low key; by dinner you need a little sound and heat to ground the day. Your food_preferences point to \"fusion / modern Asian / menus with expression\" — Dong Que isn't fine dining, but it has expression: numbered ordering eliminates decision fatigue, which goes around your avoidance of over_planned. 18:00 grabs a table while skipping the 7pm peak — fits your chaos_tolerance: low when the kid is with you. Also: the open kitchen wok-fire is a free B-roll if the camera comes out.",
      logistics: {
        raw: "🚗 25min from Sandy Wool · 🅿️ spacious outer lot · 👶 kid-friendly, high chairs · 💵 ~$60 for two · ⏰ walk-in only",
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
          "Open with **88 烤生蚝 · grilled oyster** and **92 鱼籽扇贝 · roe scallop** — small, sharp, the palate wakes up. Anchor with **15 香松腊肠锅巴饭 · lap cheong crispy rice** (the signature; not ordering it is leaving without arriving — the crispy rice carries the day's pivot into heat). Add **103 铁板螺丝 · iron-plate snail** for one loud, hot plate — the first two stops were too quiet, this dish hits the table with sound. Two adults + kid splits this exactly; no leftovers.",
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
        "Your energy reads medium and your chaos_tolerance is low when the kid is in tow, so today doesn't need a \"night activity\" — a coffee that's already on the way home is more respectful of where you are than a forced extra stop. It lands on your line about \"closing gently, not rushed, not messy, ideally with something warm.\" Philz doesn't hurry you, the kid is fine in the car, and the cup runs out exactly as you pull back into the city.",
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
        "If the kid gets fussy at Sandy Wool / misses the nap window and by 4pm he's already in car-reset mode",
      alternative:
        "Skip the rest of the Sandy Wool walk; head straight to Dong Que 30 min early at 17:00 (they open at 11:00, 17:00 is nearly empty). Take the window table so the kid has the street to look at, then bump Philz up to 19:00 — the whole arc compresses by an hour, you're home at the same time, and you can still be done bathing by 9pm.",
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
    notes: "Garry family day — South Bay decompression",
  },
};

// ---------- 2. GARRY · CULTURAL DAY (Cinematic) ----------

export const SAMPLE_PLAN_GARRY_CULTURAL_DAY_EN: TripPlan = {
  plan_id: "garry_cultural_day",
  persona_id: "garry",
  version: "v1",
  day_theme: "A cinematic line through the city",
  pitch: null,
  mood_tags: [
    "cinematic",
    "lively",
    "authentic",
    "vlog-ready",
    "walkable throughout",
  ],
  emotional_arc_text:
    "Light & shadow opening → visual peak → lawn breathing → neighborhood-heat dinner",
  emotional_arc_visual:
    "☕ light ──► 🎨 visual peak ──► 🌿 breathing ──► 🍜 heat\n10:00      11:30             14:00            17:30",
  theme_anchor: "cultural_restorative",
  stops: [
    {
      stop_index: 0,
      time: "10:00",
      place_id: "sightglass_sf",
      place_name: "Sightglass Coffee (SoMa)",
      one_liner:
        "A double-height industrial warehouse, north light pouring through the second-floor windows, the barista pulling shots in front of you — a café that earns the tired \"feels like Tokyo\" comparison.",
      why_fits_today:
        "Your vibe_signature pulls cinematic to 0.95 and hip to 0.85 — Sightglass's northern light and bare concrete are exactly those two weights made physical. You said you wanted \"inspiration waking up and the light captured\"; the 11 o'clock north light here is SF's most reliable natural-light window for vlogging, and 10:00 lands you in the 30-minute gap between opening and the breakfast crush.",
      logistics: {
        raw: "🚗 step out from SF · 🅿️ street parking is rough — Uber or the 7th St garage · 👶 stroller OK but no elevator to the upper floor · ⏰ lines start after 11am Saturday",
        drive_time_min: null,
        parking: "street difficult (Uber or 7th St garage)",
        kid_friendly: true,
        reservation_note: null,
        booking_links: [],
        transit_estimate_usd: null,
      },
      order_recommendations: {
        menu_listed: ["Pour-over single origin", "Cortado"],
        bold_picks: ["Pour-over single origin", "Cortado"],
        logic_text:
          "**Pour-over single origin** — ask the barista for today's lightest roast; the visual reads better on camera than the flavor argues for. Add a **Cortado** for the parent (you) to ground the caffeine — no real meal until 5:30. Skip anything frappé-shaped; it doesn't fit today's palette.",
      },
      tip: "B-roll from the upper railing looking down at the barista station — three seconds at a time, the light holds.",
      transition_to_next: "still light → visual density rising",
      transition_drive_min: null,
    },
    {
      stop_index: 1,
      time: "11:30",
      place_id: "sfmoma",
      place_name: "SFMOMA",
      one_liner:
        "Seven floors of contemporary art, but you don't need to walk them all — an hour in the third-floor photography wing is enough to feel like you've \"been somewhere.\"",
      why_fits_today:
        "Your taste_anchors already list SFMOMA + Mission — this stop isn't to introduce something new, it's the anchor in today's line that gives the wandering on either side weight. Your energy is high, chaos_tolerance medium; the third-floor image walls feed your novelty_appetite at the right density without pushing the toddler past his edge. The photography wing is one of the few SF interiors where you can roll a vlog with a kid — low light, low crowds, a frame that composes itself.",
      logistics: {
        raw: "🚗 0min from Sightglass (6 min walk) · 🅿️ 5th & Mission garage · 👶 stroller-accessible throughout · 🎟️ $30, book an hour ahead online to skip the line · ⏰ closes 17:00 Saturday, 1.5 hr is right",
        drive_time_min: 0,
        parking: "5th & Mission garage",
        kid_friendly: true,
        reservation_note: "$30, book online 1 hr ahead",
        booking_links: [
          { label: "Tickets ($30)", url: "https://www.sfmoma.org/visit/tickets/" },
        ],
        transit_estimate_usd: 30,
      },
      order_recommendations: null,
      tip: "Take the elevator straight to 3 — skip the big-installation crush on 1–2, the visual noise makes it un-cuttable.",
      transition_to_next: "indoor density → outdoor lawn",
      transition_drive_min: null,
    },
    {
      stop_index: 2,
      time: "14:00",
      place_id: "yerba_buena_gardens",
      place_name: "Yerba Buena Gardens",
      one_liner:
        "The grass island between SFMOMA and Metreon — by afternoon this is the single biggest reset button in walkable SoMa.",
      why_fits_today:
        "Your social_config is family_with_baby — even a high-energy dad needs to give a toddler a \"let him run\" window. Yerba Buena is the only point on this line where you can spend 30 minutes burning the kid out without breaking the city's rhythm. Your ideal_mood_arc mentions \"the chance encounter, weaving SF's neighborhoods together\" — this lawn is the midway breath. The MLK waterfall wall catches afternoon sun for another stable shot.",
      logistics: {
        raw: "🚗 outdoor walk 0 min · 🅿️ shared Metreon garage · 👶 lawn + fountains, kid runs freely · ⏰ 06:00–22:00, always free",
        drive_time_min: 0,
        parking: "shared Metreon garage",
        kid_friendly: true,
        reservation_note: null,
        booking_links: [],
        transit_estimate_usd: null,
      },
      order_recommendations: null,
      tip: "When the kid is tired, the bench row on the shaded side of the MLK waterfall is the calmest — low wind, the white noise covers the city, good for recording voiceover.",
      transition_to_next: "afternoon breath → neighborhood heat",
      transition_drive_min: 20,
    },
    {
      stop_index: 3,
      time: "17:30",
      place_id: "burma_superstar",
      place_name: "Burma Superstar (Clement Street)",
      one_liner:
        "Twenty years of lines on Clement Street, and the tea leaf salad is mixed tableside — a ritual no other place can hand you.",
      why_fits_today:
        "Your food_preferences read \"Japanese ramen / modern Asian fusion / proper Cantonese\" — ramen isn't on the board today, but Burma Superstar is one of the few SF modern-Asian spots that maxes out authentic (vibe weight 0.8). Your avoidance lists \"polished_but_soulless\" at the top; this is the opposite — slightly worn, a little crowded, and the tableside salad mix is your day's hero shot. 17:30 is the golden 15 minutes of walk-in time; past 18:00 it's a 45-min wait and the kid breaks.",
      logistics: {
        raw: "🚗 ~20min Uber from Yerba Buena · 🅿️ Clement St parking is rough — Uber strongly recommended · 👶 kid-friendly, high chairs on hand · 💵 ~$80 for two + kid · ⏰ walk-in with wait; 17:30 walks straight in",
        drive_time_min: 20,
        parking: "street difficult (Uber recommended)",
        kid_friendly: true,
        reservation_note: "walk-in with wait",
        booking_links: [],
        transit_estimate_usd: 80,
      },
      order_recommendations: {
        menu_listed: [
          "Tea Leaf Salad",
          "Samusa Soup",
          "Coconut Chicken Curry Noodles",
          "Rainbow Salad",
        ],
        bold_picks: [
          "Tea Leaf Salad",
          "Samusa Soup",
          "Coconut Chicken Curry Noodles",
          "Rainbow Salad",
        ],
        logic_text:
          "**Tea Leaf Salad** is non-negotiable — not ordering it means you didn't come; the tableside mix is the hero shot. Add **Samusa Soup** for a warm opener. One main of **Coconut Chicken Curry Noodles** (coconut-forward, the kid can eat it), and a cold **Rainbow Salad** (ten ingredients mixed at the table — double the B-roll). Two adults + kid, four dishes is exactly right; leftovers wrap as a late snack.",
      },
      tip: "Ask for the second table on the left as you walk in — best light, sightline straight into the open kitchen. The five seconds of salad-mixing composes itself.",
      transition_to_next: null,
      transition_drive_min: null,
    },
  ],
  adaptive_branches: [
    {
      condition:
        "If the kid breaks coming out of SFMOMA and can't hold to 5:30 dinner (the classic toddler late-afternoon crash)",
      alternative:
        "Pull Burma Superstar forward to 16:30 (their lunch ends 15:30, dinner opens 17:00 — slot in early). Skip Yerba Buena; instead walk Mission Street ten minutes from SFMOMA to Burma. The walking-as-breathing function folds straight into the commute. Whatever happens, save the salad-mix hero shot.",
    },
  ],
  coaching_block: null,
  composer_note: null,
  markdown_full: "",
  score_summary: {
    stranger_test: 10,
    arc_coherence: 7,
    specificity: 9,
    avoidance_respect: 9,
    adaptive_branch: 9,
    notes: "Garry cultural day — v1 baseline",
  },
};

// ---------- 3. GARRY · GOLDEN NIGHT (Aurora) ----------

export const SAMPLE_PLAN_GARRY_GOLDEN_NIGHT_EN: TripPlan = {
  plan_id: "garry_golden_night",
  persona_id: "garry",
  version: "v2",
  day_theme: "A cinematic line, closing on golden hour",
  pitch: null,
  mood_tags: [
    "cinematic",
    "lively",
    "authentic",
    "vlog-ready",
    "golden-hour closing",
  ],
  emotional_arc_text:
    "Light & shadow opening → visual density → neighborhood-heat dinner → city-lights close",
  emotional_arc_visual:
    "☕ light ──► 🎨 density ──► 🍜 heat ──► 🌅 city-lights\n10:00      11:30          17:30          19:30",
  theme_anchor: "social_high_energy",
  stops: [
    {
      stop_index: 0,
      time: "10:00",
      place_id: "sightglass_sf",
      place_name: "Sightglass Coffee (SoMa)",
      one_liner:
        "A double-height industrial warehouse, north light pouring through the second-floor windows, the barista pulling shots in front of you — a café that earns the tired \"feels like Tokyo\" comparison.",
      why_fits_today:
        "Your vibe_signature pulls cinematic to 0.95 and hip to 0.85 — Sightglass's northern light and bare concrete are exactly those two weights made physical. The 11 o'clock north light here is SF's most reliable natural-light window for vlogging; 10:00 lands you in the 30-minute gap between opening and the crush. Today's three later stops all need this cup as the base.",
      logistics: {
        raw: "🚗 step out from SF · 🅿️ street parking is rough — Uber or the 7th St garage · 👶 stroller OK but no elevator to the upper floor · ⏰ lines start after 11am Saturday",
        drive_time_min: null,
        parking: "street difficult (Uber or 7th St garage)",
        kid_friendly: true,
        reservation_note: null,
        booking_links: [],
        transit_estimate_usd: null,
      },
      order_recommendations: {
        menu_listed: ["Pour-over single origin", "Cortado"],
        bold_picks: ["Pour-over single origin", "Cortado"],
        logic_text:
          "**Pour-over single origin** — ask the barista for today's lightest roast; the visual reads better on camera than the flavor argues for. Add a **Cortado** for the parent (you) to ground the caffeine — no real meal until 5:30. Skip anything frappé-shaped; it doesn't fit today's palette.",
      },
      tip: "B-roll from the upper railing looking down at the barista station — three seconds at a time, the light holds.",
      transition_to_next: "still light → visual density rising",
      transition_drive_min: null,
    },
    {
      stop_index: 1,
      time: "11:30",
      place_id: "sfmoma",
      place_name: "SFMOMA",
      one_liner:
        "Seven floors of contemporary art, but you don't need to walk them all — an hour and a half in the third-floor photography wing is enough to feel like you've \"been somewhere.\"",
      why_fits_today:
        "Your taste_anchors already list SFMOMA + Mission — this stop isn't a discovery, it's the anchor that fills the visual-density slot between morning light and evening heat. Your energy is high, chaos_tolerance medium; the third-floor image walls feed your novelty_appetite. The photography wing is one of the few SF interiors where you can vlog with a kid — low light, low crowds, frames that compose themselves. SFMOMA plays the \"sustained immersion\" role here, not the spike — the spike is saved for the closing.",
      logistics: {
        raw: "🚗 0min from Sightglass (6 min walk) · 🅿️ 5th & Mission garage · 👶 stroller-accessible throughout · 🎟️ $30, book an hour ahead online to skip the line · ⏰ closes 17:00 Saturday, 1.5 hr is right",
        drive_time_min: 0,
        parking: "5th & Mission garage",
        kid_friendly: true,
        reservation_note: "$30, book online 1 hr ahead",
        booking_links: [
          { label: "Tickets ($30)", url: "https://www.sfmoma.org/visit/tickets/" },
        ],
        transit_estimate_usd: 30,
      },
      order_recommendations: null,
      tip: "Take the elevator straight to 3 — skip the big-installation crush on 1–2, the visual noise makes it un-cuttable.",
      transition_to_next: "visual immersion → street-food peak",
      transition_drive_min: 25,
    },
    {
      stop_index: 2,
      time: "17:30",
      place_id: "burma_superstar",
      place_name: "Burma Superstar (Clement Street)",
      one_liner:
        "Twenty years of lines on Clement Street, and the tea leaf salad is mixed tableside — a ritual no other place can hand you.",
      why_fits_today:
        "Your food_preferences read \"Japanese ramen / modern Asian fusion / proper Cantonese\" — ramen isn't on the board today, but Burma Superstar is one of the few SF modern-Asian spots that maxes out authentic (vibe weight 0.8). Your avoidance lists \"polished_but_soulless\" at the top; this is the opposite — slightly worn, a little crowded, and the tableside salad mix is your day's hero shot. 17:30 is the golden 15 minutes of walk-in time; past 18:00 it's a 45-min wait and the kid breaks.",
      logistics: {
        raw: "🚗 ~25min Uber from SFMOMA · 🅿️ Clement St parking is rough — Uber strongly recommended · 👶 kid-friendly, high chairs on hand · 💵 ~$80 for two + kid · ⏰ walk-in with wait; 17:30 walks straight in",
        drive_time_min: 25,
        parking: "street difficult (Uber recommended)",
        kid_friendly: true,
        reservation_note: "walk-in with wait",
        booking_links: [],
        transit_estimate_usd: 80,
      },
      order_recommendations: {
        menu_listed: [
          "Tea Leaf Salad",
          "Samusa Soup",
          "Coconut Chicken Curry Noodles",
          "Rainbow Salad",
        ],
        bold_picks: [
          "Tea Leaf Salad",
          "Samusa Soup",
          "Coconut Chicken Curry Noodles",
          "Rainbow Salad",
        ],
        logic_text:
          "**Tea Leaf Salad** is non-negotiable — not ordering it means you didn't come; the tableside mix is the hero shot. Add **Samusa Soup** for a warm opener. One main of **Coconut Chicken Curry Noodles** (coconut-forward, the kid can eat it), and a cold **Rainbow Salad** (ten ingredients mixed at the table — double the B-roll). Two adults + kid, four dishes is exactly right — leave appetite for the cocktail at Top of the Mark.",
      },
      tip: "Ask for the second table on the left as you walk in — best light, sightline straight into the open kitchen. The five seconds of salad-mixing composes itself.",
      transition_to_next: "street-level food → 19th-floor city-lights",
      transition_drive_min: 22,
    },
    {
      stop_index: 3,
      time: "19:30",
      place_id: "top_of_the_mark",
      place_name: "Top of the Mark",
      one_liner:
        "Nob Hill's 19th-floor 360° lounge — Golden Gate, the Bay, downtown lights all in one frame, and the evening lands you on the edge of golden hour rolling into night.",
      why_fits_today:
        "Your ideal_mood_arc, fourth act, in your own words: \"creative thought or a warm family talk under SF's gorgeous city lights.\" Top of the Mark isn't being sold to you — it's the closing you already wrote. cinematic 0.95, photogenic 0.9, polished 0.8 all max out together, and it's the one spot tonight that solves \"vlog closing shot\" and \"kid can come\" at the same time (19th-floor bars are usually 21+, but family-with-baby is on the OK list here). The first three stops worked horizontally across neighborhoods; this one lifts vertically — the arc actually closes.",
      logistics: {
        raw: "🚗 ~22min Uber from Clement · 🅿️ Mark Hopkins valet ($) or nearby garage · 👶 kid-friendly, ask for north-window seating toward the Golden Gate · ⏰ golden hour starts ~18:50; 19:30 catches the city lighting up · 💵 cocktails $18–22",
        drive_time_min: 22,
        parking: "Mark Hopkins valet ($) or nearby garage",
        kid_friendly: true,
        reservation_note: null,
        booking_links: [],
        transit_estimate_usd: 20,
      },
      order_recommendations: null,
      tip: "Tell the host at the door: \"north window facing Golden Gate.\" That side films cleaner than the Bay Bridge east; the bridge silhouette is your closing shot. The kid's attention is good for 30–40 minutes — don't push past.",
      transition_to_next: null,
      transition_drive_min: null,
    },
  ],
  adaptive_branches: [
    {
      condition:
        "If the kid breaks coming out of SFMOMA and can't hold to 5:30 dinner (the classic toddler late-afternoon crash)",
      alternative:
        "Pull Burma Superstar forward to 16:30 (lunch ends 15:30, dinner opens 17:00). Skip the walking gap between Sightglass and SFMOMA; arrive at Top of the Mark an hour earlier (18:30) for a cocktail. The Golden Gate lighting time doesn't move — save the closing shot.",
    },
  ],
  coaching_block: null,
  composer_note: null,
  markdown_full: "",
  score_summary: {
    stranger_test: 10,
    arc_coherence: 9,
    specificity: 9,
    avoidance_respect: 9,
    adaptive_branch: 9,
    notes: "Garry golden night — v2, added Top of the Mark for golden-hour closing",
  },
};

// ---------- TripContexts for the demo set ----------

export const TRIP_CONTEXT_GARRY_FAMILY_DAY: TripContext = {
  date_label: "Sat · Jan 10 · 2026",
  time_window: "14:30 → 21:00",
  origin: "San Francisco",
  companions: ["+partner", "+toddler"],
  vehicle: "car",
};

export const TRIP_CONTEXT_GARRY_CULTURAL_DAY: TripContext = {
  date_label: "Sat · Jan 17 · 2026",
  time_window: "10:00 → 19:30",
  origin: "San Francisco",
  companions: ["+partner", "+toddler"],
  vehicle: "walk + uber",
};

export const TRIP_CONTEXT_GARRY_GOLDEN_NIGHT: TripContext = {
  date_label: "Sat · Jan 24 · 2026",
  time_window: "10:00 → 21:00",
  origin: "San Francisco",
  companions: ["+partner", "+toddler"],
  vehicle: "walk + uber",
};
