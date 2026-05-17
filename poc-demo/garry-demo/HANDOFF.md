# Day Composer — Frontend ↔ Backend Handoff

This is what the frontend rendering layer expects from the Composer.
Three demo plans, all for Garry, three templates.

---

## 1. Demo URLs (local dev)

| Plan | Demo route | JSON endpoint | Template |
|---|---|---|---|
| Family Day | `http://localhost:3000/demo/family-day` | `http://localhost:3000/api/plans/family-day` | Polaroid Keepsake |
| Cultural Day | `http://localhost:3000/demo/cultural-day` | `http://localhost:3000/api/plans/cultural-day` | Cinematic Editorial |
| Golden Night | `http://localhost:3000/demo/golden-night` | `http://localhost:3000/api/plans/golden-night` | Aurora Romance |

List of all plans: `http://localhost:3000/api/plans`

To run the frontend yourself:

```bash
cd mvp-list/day-composer-app
pnpm install
pnpm dev   # http://localhost:3000/demo
```

---

## 2. Reference JSON files

Committed in this directory — these are the exact outputs the frontend
renders today. Use them as the **target shape** when wiring the Composer.

```
poc-demo/garry-demo/
├── index.json           # the 3-plan list (matches /api/plans response)
├── family-day.json      # full TripPlan + TripContext, matches /demo/family-day
├── cultural-day.json    # ditto, /demo/cultural-day
└── golden-night.json    # ditto, /demo/golden-night
```

Each `.json` is `{ "plan": TripPlan, "trip_context": TripContext }`.

---

## 3. Type contract

Single source of truth in TypeScript:

- **`mvp-list/day-composer-app/lib/types/trip-plan.ts`** — `TripPlan`, `Stop`, `Logistics`, `OrderRecs`, `AdaptiveBranch`, `ScoreSummary`, `TripContext` (file is short, ~145 LOC, fully commented).

### Headline shape

```ts
interface TripPlan {
  plan_id: string;             // "garry_family_day"
  persona_id: string;          // "garry"
  version: string;             // "v1"
  day_theme: string;
  theme_anchor: string | null; // "cultural_restorative" | "social_high_energy" | ...
  pitch: string | null;
  mood_tags: string[];         // free strings, frontend does substring matching for palette
  emotional_arc_text: string;  // narrative one-liner
  emotional_arc_visual: string;// optional emoji ASCII art (frontend may ignore)
  stops: Stop[];
  adaptive_branches: AdaptiveBranch[];
  markdown_full: string;       // literal Composer markdown (frontend ignores today)
  coaching_block: unknown | null;
  composer_note: unknown | null;
  score_summary: ScoreSummary;
}

interface Stop {
  stop_index: number;
  time: string;                // "14:30"
  place_id: string;            // canonical id — drives image lookup
  place_name: string;
  one_liner: string;           // short evocative tagline
  why_fits_today: string;      // paragraph, references vibe_signature etc.
  logistics: Logistics;        // see types file
  order_recommendations: OrderRecs | null;  // restaurants only
  tip: string | null;
  transition_to_next: string | null;
  transition_drive_min: number | null;
  image_url?: string | null;   // OPTIONAL — see §4 below
}

interface OrderRecs {
  menu_listed: string[];       // each: "88 烤生蚝 · grilled oyster" (number + name)
  bold_picks: string[];        // subset of menu_listed
  logic_text: string;          // markdown prose with **bold** dishes
}
```

### Important quirks vs the original spec (`backend-data-schema-v2.md §2.9`)

The real backend output already diverged from the spec; the frontend types
match the **real output**, not the spec. Diffs:

| Spec | Reality (what frontend expects) |
|---|---|
| `emotional_arc: ArcBeat[]` with numeric `vibe_curve_value` | `emotional_arc_text` (string) + `emotional_arc_visual` (string). Frontend derives a numeric curve client-side. |
| `transitions: Transition[]` top-level | inline on each Stop: `transition_to_next` + `transition_drive_min`. |
| `dish_recommendations: DishRecommendation[]` top-level | per-stop: `stop.order_recommendations` (nullable). |
| `mood_tags: MoodTag[]` enum | `string[]` free-form. |
| `adaptive_branches[].branch_at_stop_index` | not present — branches don't anchor to a stop. |
| `stops[].image_url` not in spec | **Optional**. If backend sets, frontend uses it. If absent, frontend renders gradient fallbacks. See §4. |

---

## 4. Image URL convention

Each `Stop.image_url` is optional. Today the frontend hardcodes a
`place_id → URL` map in `lib/data/sample-plan-en.ts` (9 Wikimedia
hotlinks) and injects it post-construction.

Two acceptable backend approaches:

**A. Backend sets `image_url` directly** — best long-term. Any
hotlinkable HTTPS image URL works (Wikimedia, Unsplash, S3, CDN).

**B. Backend leaves `image_url` null** — frontend uses gradient placeholders.
Acceptable for v0 but visually weaker; the /demo pages today only look the
way they do because of the image injection.

If you go with (A), please use **stable** URLs (no Google Image redirects,
no expiring S3 signed URLs).

---

## 5. How frontend will consume backend output

Today the frontend imports plans as static TS exports at build time.
Three integration patterns possible:

### Pattern 1 — Backend POSTs JSON to frontend (preferred)

Backend has its own `POST /compose` endpoint. Frontend calls it from
the Intake page, receives a `TripPlan` JSON, navigates to `/preview` or
a dynamic route that renders it.

```ts
// Frontend side (already partly wired in /preview Paste-JSON):
const res = await fetch(BACKEND_URL + "/compose", {
  method: "POST",
  body: JSON.stringify(experienceRequest),
});
const { plan, trip_context } = await res.json();
// pass to <PolaroidKeepsake plan={plan} tripContext={trip_context} />
```

### Pattern 2 — Backend writes JSON to disk, frontend reads at request time

Backend writes `TripPlan` JSON files to a known location. Frontend has a
route `/plan/[id]` that reads from there (or via a fetch from `/api/plans/[id]`).

### Pattern 3 — Backend pre-renders (build-time)

Backend output goes into `lib/data/`, frontend builds a static demo set.
Useful for marketing/share-link generation. Less useful for the live agent flow.

For the POC we recommend Pattern 1.

---

## 6. What the frontend ignores (today)

These TripPlan fields are accepted but not currently rendered:

- `markdown_full` — the original Composer markdown output
- `coaching_block`, `composer_note` — both nullable, schema placeholders
- `pitch` — currently null in all 3 references
- `score_summary` — internal metadata, never user-facing

Safe for backend to populate them or leave null.

---

## 7. Open questions for the Composer team

1. **`image_url`** — will backend populate? If yes, where do you source
   images from (Maps Places photos API, vendor CDN, hand-curated)?
2. **`trip_context`** — currently a frontend-only convenience. Should
   it move into `TripPlan` as a sub-field, or stay separate and ride
   alongside in the API response (as we do in `/api/plans/[id]`)?
3. **Adaptive branches** — do you want them anchored to a stop
   (`branch_at_stop_index`) for richer rendering, or keep them
   page-level as today?
4. **Streaming** — should `/compose` stream the TripPlan as it's
   generated (NDJSON / SSE), or always return the full document?

---

## Contact

Frontend changes for this set live on branch
`mia/day-composer-v2-spec-yolo`. The relevant files:

- `day-composer-app/lib/types/trip-plan.ts` — type contract
- `day-composer-app/lib/data/sample-plan-en.ts` — the 3 reference plans
- `day-composer-app/app/api/plans/**` — the REST endpoints
- `day-composer-app/app/demo/**` — the user-facing renders
- `day-composer-app/components/templates/**` — the three visual templates

Ping Mia for anything ambiguous.
