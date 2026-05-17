// Generated from /poc-demo/sample-plans.json (real backend output). Differs from spec §2.9 — see commit message.
//
// Key differences from spec:
//   - `emotional_arc` is flattened to TWO string fields: `emotional_arc_text`
//     (narrative one-liner) + `emotional_arc_visual` (emoji ASCII art). The
//     numeric vibe curve is derived client-side via `lib/utils/derive-arc.ts`.
//   - `transitions[]` is GONE as a top-level array. Per-stop fields
//     `transition_to_next` + `transition_drive_min` carry the same info inline.
//   - `dish_recommendations[]` top-level is GONE. Per-stop
//     `stop.order_recommendations` carries `menu_listed`, `bold_picks`,
//     `logic_text` (markdown string).
//   - `mood_tags` is a FREE `string[]` — not a closed enum. Use lowercase
//     substring matching to detect "restorative", "celebratory", etc.
//   - `stops[].image_url` is NOT present. Templates use gradient placeholders.
//   - `adaptive_branches[]` is simpler — no `branch_at_stop_index`,
//     no `alternative_place_id`.

// ---------- File wrapper (multiple plans per JSON file) ----------

export interface SamplesFile {
  _meta: SamplesMeta;
  plans: TripPlan[];
}

export interface SamplesMeta {
  purpose: string;
  schema_note: string;
  plan_count: number;
  personas_covered: string[];
  versions_covered: string[];
  regenerated_from: string[];
  place_id_source: string;
  scoring_provenance: string;
}

// ---------- One plan ----------

export interface TripPlan {
  plan_id: string;
  persona_id: string;
  version: string;
  day_theme: string;
  theme_anchor: string | null;
  pitch: string | null;
  /** Free strings — NOT the spec's enum. Use lowercase .includes() to match. */
  mood_tags: string[];
  /** Narrative one-liner: "Slow start in light → lakeside drift → ..." */
  emotional_arc_text: string;
  /** Emoji art, multi-line. Templates may render raw or ignore. */
  emotional_arc_visual: string;
  stops: Stop[];
  adaptive_branches: AdaptiveBranch[];
  /** Literal Composer markdown output. Templates can ignore. */
  markdown_full: string;
  coaching_block: unknown | null;
  composer_note: unknown | null;
  score_summary: ScoreSummary;
}

export interface Stop {
  stop_index: number;
  /** e.g. "14:30" */
  time: string;
  place_id: string;
  place_name: string;
  /** NEW — short evocative tagline. Surface prominently in templates. */
  one_liner: string;
  why_fits_today: string;
  logistics: Logistics;
  /** null for non-restaurant stops */
  order_recommendations: OrderRecs | null;
  tip: string | null;
  transition_to_next: string | null;
  transition_drive_min: number | null;
  /**
   * Optional frontend convenience. Direct image URL (hotlinkable).
   * Templates fall back to gradient placeholders when null/undefined.
   */
  image_url?: string | null;
}

export interface Logistics {
  /** Pre-formatted human-readable summary with emoji ("🚗 22min · 🅿️ free · ..."). */
  raw: string;
  drive_time_min: number | null;
  /** Free form: "free", "paid", "street", "easy", etc. */
  parking: string | null;
  kid_friendly: boolean | null;
  reservation_note: string | null;
  /** Array of URLs OR objects with { label, url }. Real samples mix both. */
  booking_links: Array<string | { label: string; url: string }>;
  transit_estimate_usd: number | null;
}

export interface OrderRecs {
  /** Each entry: `"<num> <chinese> · <english>"` e.g. `"88 烤生蚝 · grilled oyster"`. Use parseDish() to split. */
  menu_listed: string[];
  /** Subset of menu_listed. Same string format. */
  bold_picks: string[];
  /** Markdown prose with **bold** dish names. Render via react-markdown. */
  logic_text: string;
}

export interface AdaptiveBranch {
  condition: string;
  alternative: string;
}

export interface ScoreSummary {
  stranger_test: number;
  arc_coherence: number;
  specificity: number;
  avoidance_respect: number;
  adaptive_branch: number;
  notes: string;
}

// ---------- Mood tag is now an open string, not an enum ----------

export type MoodTag = string;

// ---------- TripContext (frontend convenience, NOT in backend schema) ----------

export interface TripContext {
  date_label: string; // "Sat · Jan 10 · 2026"
  time_window: string; // "14:30 → 22:00"
  origin: string; // "Sunnyvale"
  companions: string[]; // ["+1", "+baby"]
  vehicle: string; // "car"
}

// ---------- Template props ----------

export type TemplateId = "polaroid" | "cinematic" | "aurora";

export interface TemplateProps {
  plan: TripPlan;
  tripContext?: TripContext;
  onRefine?: (instruction: string) => void;
}

// ---------- Derived arc (computed client-side) ----------

export interface ArcPoint {
  x: number; // 0..1 normalized
  y: number; // 0..1 normalized vibe (1 = peak)
  label: string;
  time: string;
}
