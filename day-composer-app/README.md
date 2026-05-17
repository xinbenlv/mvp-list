# Day Composer — frontend app

Next.js 14 + Tailwind + framer-motion. Renders a `TripPlan` JSON in three visual
templates (Polaroid Keepsake / Cinematic Editorial / Aurora Romance).

## Run

```bash
cd day-composer-app
pnpm install   # already done at scaffold time
pnpm dev
# open http://localhost:3000  → redirects to /preview
```

## What's in `/preview`

- Top control bar: Auto / Polaroid / Cinematic / Aurora, plus a "Paste JSON"
  toggle. Selection syncs to `?template=...`.
- Auto mode runs `pickTemplate(plan, tripContext)` — currently picks
  **Polaroid** for the Jan 10 sample (reflective + baby).
- Paste a valid TripPlan JSON to swap the data. Reset button restores the
  stub.

## Project layout

```
app/
  layout.tsx        — Google fonts via next/font, CSS var wiring
  page.tsx          — redirects to /preview
  preview/page.tsx  — switcher + JSON paste
  globals.css       — Tailwind + per-template scoped helpers (noise, mesh, sparkles)

components/templates/
  polaroid-keepsake/  — cover, arc curve, stop pages, menu block, branches, refine bar
  cinematic-editorial/ — masthead, hero, TOC, spread, pull quote, restaurant, branches, refine bar
  aurora-romance/      — hero, arc card, stop rows, menu card, branches, refine bar

lib/
  types/trip-plan.ts   — TS types matching backend schema §2.9
  hooks/use-palette.ts — CSS-var palette per template, lightly nudged by mood_tags
  utils/
    arc-path.ts            — d3-shape catmullRom curve generator
    format-logistics.ts    — drive/parking/baby chips + mood tag formatter
    pick-template.ts       — auto-pick rules
  data/sample-plan.ts  — hardcoded Jan 10 trip
```

## Notes

- Each template owns its CSS-var namespace via inline `style` on the root —
  vars do NOT leak between templates.
- framer-motion handles all animation (hero fade-in stagger, arc pathLength,
  scroll-reveal cards). No GSAP, no Lenis.
- No backend / `/api/*` routes here.
- The real Jan 10 JSON sample is expected at
  `../sample-plans/jan-10.json`. When it lands, reconcile against the
  assumption block at the top of `lib/types/trip-plan.ts`.
