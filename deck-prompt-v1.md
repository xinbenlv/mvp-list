# Family Getaway Planner — 5-Deck Image Prompts

Visual style for **all** decks (apply this as the base system prompt before each slide prompt):

> **Global style — Anthropic.ai aesthetic.** Warm off-white / cream background (#F4EFE6 ~ #EFE9DD), generous whitespace, editorial layout, premium calm feel. Typography: large serif headline (Tiempos / Söhne-style), small clean sans-serif for body. Accent color: muted coral / terracotta (#D97757) with secondary muted sage, dusty blue, and warm grey. Illustrations should feel hand-drawn / pencil-sketched, soft line weight, slightly imperfect, organic. No harsh gradients, no glossy 3D, no neon. Subtle paper grain. Centered composition with quiet confidence. 16:9 aspect ratio. No stock-photo people.

---

## Deck 1 — Title / Problem

**Headline on slide:** "Planning a Saturday Getaway, With a 1-Year-Old in Tow"
**Subhead:** "A GBrain-powered pipeline for family-friendly trip discovery."

**Image prompt:**
> Anthropic.ai editorial style illustration on a warm cream background. A hand-drawn pencil-sketch scene: a young family — two parents and a toddler in a stroller — standing at a crossroads of soft, winding paths that fan out toward small icons of a restaurant, a museum, a park bench, and a mountain. Soft terracotta and sage accents, organic line work, slight paper grain. Generous negative space on the right side reserved for the headline. Minimal, editorial, calm. 16:9.

---

## Deck 2 — Curate

**Headline on slide:** "Curate"
**Subhead:** "100–1,000 spots, gathered from the wild."

**Image prompt:**
> Anthropic.ai editorial illustration, warm cream background. A hand-drawn pencil-sketch of an open notebook or pinboard in the center, with soft sketched threads / strings radiating outward to small floating cards: a screenshotted Instagram post, a TikTok thumbnail, a Google search result, a friend's text message, a Reddit thread. Each card rendered with light line work and a single muted color accent (terracotta, sage, dusty blue). The notebook is the gravitational center; the sources orbit loosely. Slight paper grain, generous whitespace. Editorial, calm, not cluttered. 16:9.

---

## Deck 3 — Index (GBrain at the Center)

**Headline on slide:** "Index — Structuring with GBrain"
**Subhead:** "Hours, budget, cuisine, vibe, popular dishes, main attractions."

**Image prompt:**
> Anthropic.ai editorial style, warm cream background (#F4EFE6), generous whitespace. **Center of the composition: the word "gbrain" set in a large, soft lowercase serif (Tiempos-style), in muted terracotta (#D97757), enclosed in a hand-drawn pencil circle.** Radiating outward in four directions (top, bottom, left, right) and at the diagonals are eight clean, recognizable logos of data sources, each drawn in its own brand color but rendered with a soft, slightly hand-sketched outline so they feel cohesive with the editorial style: **Google Maps, Apple Maps, Yelp, TripAdvisor, Lonely Planet, OpenTable, Instagram, Eater**. Each logo sits inside a faint pencil circle, connected to the central "gbrain" with a thin, hand-drawn line — like a constellation diagram. The whole layout feels like a calm, hand-annotated knowledge graph. No 3D, no glow, no neon. Paper grain, organic lines. 16:9.
>
> **Critical:** the text in the center must read exactly **"gbrain"** (verbatim, lowercase). Do not stylize, abbreviate, or rename.

---

## Deck 4 — Trigger & Ranking (Funnel Workflow)

**Headline on slide:** "Trigger & Ranking"
**Subhead:** "Every Wednesday, a funnel from 1,000 → 2."

**Image prompt:**
> Anthropic.ai editorial style, warm cream background, hand-drawn pencil-sketch funnel workflow flowing left-to-right (or top-to-bottom) across the slide. The funnel has four labeled stages, each drawn as a soft rounded container connected by thin hand-drawn arrows:
>
> 1. **Proposal** — a wide opening labeled "1,000 spots" with many tiny dot-icons representing restaurants and attractions clustering in.
> 2. **Filtering** — a narrower stage labeled "remove visited · match calendar · family-friendly," with a few dots being gently crossed out with pencil strikes.
> 3. **Ranking** — a narrower stage labeled "score by vibe, distance, weather," with remaining dots being reordered into a neat vertical list.
> 4. **Two Options** — the funnel exits into **two parallel cards** side by side, each labeled "Option A" and "Option B," each card showing a tiny sketch of a map pin + restaurant + attraction. One card has a small "new" badge, the other a small "loved before" badge.
>
> Above the whole funnel, a small calendar icon with "Wednesday" pencil-circled, with a thin line trailing down into the Proposal stage to indicate the weekly trigger.
>
> Color palette: terracotta accent on labels, muted sage and dusty blue for the funnel walls, warm grey for body text. Soft pencil lines, organic, slightly imperfect. Generous whitespace around the funnel. Editorial, calm, premium. 16:9.

---

## Deck 5 — Output

**Headline on slide:** "Output"
**Subhead:** "A full agenda + a generated overview image."

**Image prompt:**
> Anthropic.ai editorial style, warm cream background. Two soft hand-drawn cards placed side by side at a slight angle, like they were just set down on a desk:
>
> - **Left card:** a sketched document titled "Agenda" with a few pencil-ruled lines representing time blocks (10:00 · museum, 12:30 · lunch, 15:00 · park), and small callouts in the margin reading "Reason for Picking" and "Highlights."
> - **Right card:** a sketched map-overview illustration — a soft top-down map with three pin markers connected by a dotted route, a tiny restaurant plate icon next to one pin, a tiny tree/mountain icon next to another, and a small "generated by GPT Image" pencil annotation at the bottom corner.
>
> Both cards rendered with thin hand-drawn lines, terracotta and sage accents on key elements, warm cream background, slight paper grain. Editorial, calm, premium feel, generous whitespace. No photorealistic UI, no app screenshots — these should feel like hand-illustrated artifacts. 16:9.

---

## Notes for the image model

- If using **GPT Image / DALL·E**: paste the **Global style** paragraph first, then the per-deck prompt.
- For **Deck 3**, do a second pass if the model misspells "gbrain" — explicitly re-prompt: *"the center word must be the exact lowercase string g-b-r-a-i-n with no spaces, no hyphens, no other text inside the central circle."*
- For **Deck 4**, if the funnel comes out cluttered, regenerate with the instruction *"reduce to four stages, large clear labels, fewer dots, more whitespace between stages."*
