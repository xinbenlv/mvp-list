# POC Demo Assets

> Hand-curated assets for the Day Composer POC + reusable across the test suite once code lands.
>
> Used to dry-run the Composer prompt, validate end-to-end behavior, and as fixtures for the eventual Plan Critic agent (`agent-engineering-design.md` §4).

---

## Contents

| File | What | When to update |
|---|---|---|
| `composer_prompt.md` | System prompt for the Plan Composer agent (with full few-shot example) | When iterating Composer output quality |
| `demo_places.json` | 10 hand-curated Bay Area places (slim `Place v2` schema) covering multiple day shapes | When backend `/experience` is not yet ready, or when adding test coverage for new vibes |
| `mia_persona.json` | **Typical Persona A** — South Bay AI engineer + new mom; restoration-anchored | Re-extract from ChatGPT when Mia's life context shifts materially |
| `garry_tan_persona.json` | **Typical Persona B** — SF VC / vlogger / dad; high-energy urban exploration | Re-extract when Garry's profile materially shifts |
| `alex_chen_persona.json` | **Typical Persona C** — newcomer to SF (3 weeks in), solo / friends, transit-native, moderate budget, maximal exploration | Re-author when newcomer assumptions change (e.g. neighborhood, budget tier, time-in-city) |
| `sam_reyes_persona.json` | **Typical Persona D** — burnout-edge SF Mission PM, solo recovery, post-photofacial medical constraints, top-down systems thinker who needs coaching not curation; triggers the 🫧 coaching block | Re-author if coaching-mode product surface evolves or if medical_recovery_context / family_dynamics_avoidance schema extensions get promoted to backend schema v3 |
| `README.md` | This file | When the asset list changes |

---

## Typical Personas (test fixtures)

The four persona JSONs serve as the **canonical contrast quartet** for testing the Day Composer agent. They are deliberately chosen to span opposing axes of the intake ontology — if a Composer prompt can produce a magical TripPlan for all four, it's not overfit to one user archetype.

| Dimension | Mia (Persona A) | Garry (Persona B) | Alex (Persona C) | Sam (Persona D) |
|---|---|---|---|---|
| `emotional_intent` | restore + reconnect | explore + reconnect | explore + feel_alive + celebrate | **restore + slow_down + decompress + regulate_nervous_system + solo_recovery** |
| `energy_level` | medium | high | high | **low (burnout dip)** |
| `chaos_tolerance` | low | medium | high | **very_low (NEW — lowest on the axis)** |
| `novelty_appetite` | high | high | maxed (chasing it) | **low (NEW — wants familiar > novel; recovery, not discovery)** |
| `start_location` | South Bay (Sunnyvale-ish) | San Francisco | SF (Lower Haight) | **SF (Mission, 24th & Valencia)** |
| `max_drive_minutes` | 45 | 30 (urban) | 0 — no car | **90 (NEW — willing to drive to Marin; the drive IS the ritual)** |
| `time_window` | 14:00–21:00 (half-day) | 09:00–21:00 (full-day) | 09:30–23:30 (early-to-late) | **09:00–19:00 (home before dark, post-procedure)** |
| `budget` | flexible | flexible | moderate | **flexible (but cognitive load IS the cost; willing to pay to avoid decisions)** |
| `social_config` | couple + family_with_baby | family_with_baby | solo OR friends | **solo (recovery-mode, NOT exploration-mode — different REASON than Alex)** |
| `kid_friendly_required` | true | true | false | **false** |
| Local knowledge | high (Bay Area years) | very high (deeply local) | low — moved 3 weeks ago | **high (knows Marin intimately, returns to same trusted spots)** |
| Attitude to famous things | avoid touristy | avoid touristy | wants the local version of famous things | **strongly avoid touristy AND avoid novel — wants known-safe-familiar** |
| `vibe_signature` peaks | restorative · cinematic · natural_light · intimate | cinematic · lively · authentic · hip | novel · lively · authentic · walkable · social | **restorative · quiet · intimate · low_noise · natural_light · familiar** |
| Top `avoidance` | touristy, rushed, parking_uncertain | touristy, polished_but_soulless, rushed | boring_suburbia, chain_restaurant, requires_car | **loud, rushed, crowded, obligation_triggering, decision_fatigue, social_performance_required, direct_sun (medical), menus_with_more_than_8_choices** |
| Wants from agent | composition | composition | composition | **coaching: state diagnosis + permission slips + nervous-system regulation prescription** |
| Schema extensions used | — | — | — | **medical_recovery_context, cognitive_style, family_dynamics_avoidance (NEW — see "Persona D specific notes" below)** |

→ **Quality bar**: If the Composer produces a magical TripPlan for ALL FOUR personas, it's not overfit. If it produces a great plan for three and a generic plan for the fourth, the prompt or Concept Generator needs work.

→ **Stranger test**: Read any `why_fits_today` from a plan. Can you tell which persona it was generated for? If no, the prompt is too generic.

→ **Coverage note (Alex)**: Alex's profile (solo / friends, transit-native, moderate budget, kid-free, low local knowledge) exposes whole place categories that `demo_places.json` currently underserves — see "Place coverage gap for Persona C" below.

→ **Coverage note (Sam)**: Sam's profile (solo recovery + Marin-anchored + medical constraints) exposes a **second, separate place inventory gap** — current inventory has 0 Marin coverage. See "Place coverage gap for Persona D" below.

---

## Persona D specific notes (Sam Reyes — coaching mode trigger)

Persona D is structurally different from A/B/C in three ways. These differences are intentional, not accidental:

### 1. Uses 3 NEW intake dimensions (tests schema extensibility)

The other three personas fit cleanly into backend-data-schema-v2. Sam introduces three fields that **do not exist** in schema v2:

- **`medical_recovery_context`** — `{ procedure, days_since, constraints[] }`. Procedural recovery imposes hard constraints (no direct UV, no chlorine, no high heat) that change place feasibility in ways the existing schema can't express. Tests whether the Composer prompt can read and respect a free-text constraint block.
- **`cognitive_style`** — Currently `["top_down_systems_thinker"]`. Informs the **type** of advice the agent should give (prescription with reasoning) rather than the type of **place**. Tests whether the Composer can modulate its **output form** based on intake, not just place selection.
- **`family_dynamics_avoidance`** — `{ active: true, note, duration }`. A contextual hard constraint that overrides default social_fit logic for this specific occasion. Tests whether the Composer respects "don't suggest activities with parents/in-laws this weekend" even when the place's `social_fit` includes them.

For the POC, the Composer prompt reads these as **plain text intake context** (no schema change needed). Future: if Persona D-style coaching mode becomes a product mode, promote these to schema v3.

### 2. Triggers the 🫧 coaching block (the main test value)

The Composer prompt (`composer_prompt.md`) has a `🫧 coaching block` that conditionally fires when `emotional_intent` includes `restore` / `slow_down` AND `energy_level` is `low`. Personas A/B/C don't reliably trigger it:
- Mia has `restore` but also `explore + feel_alive` and `energy_level: medium` — coaching block may or may not fire.
- Garry is `explore + reconnect`, `energy: high` — block definitively does not fire.
- Alex is `explore + feel_alive + celebrate`, `energy: high` — block definitively does not fire.

Sam is the **only persona that reliably forces the coaching block to fire**. Without Persona D, the coaching-mode output category exposed by GT Plan B has no fixture and silently regresses if anyone edits that branch of the Composer prompt.

### 3. Inverts the "novelty is good" assumption baked into A/B/C

All three other personas have `novelty_appetite: high` (Mia, Garry) or `high+` (Alex). Sam is the first persona with `novelty_appetite: low`. This is a deliberate test of whether the Composer can resist its likely default behavior of "surface a hidden gem" when the user actually wants "return me to a trusted ritual". Most concierge AIs fail this test by reflex.

---

## Place coverage gap for Persona C (Alex)

Audit of the current 12-place `demo_places.json` against Alex's intake:

**What fits (roughly)**: `sightglass_sf` (SoMa cafe), `burma_superstar` (Clement St), `sfmoma` (if discounted ticket), `yerba_buena_gardens`, `tartine_mission`, `top_of_the_mark` (cinematic but $$ + dress code), `true_laurel_mission` (cocktail bar, $$$ — over his casual budget but socially right). Roughly **5–7 of 12** are usable; the rest are South Bay / kid-anchored / car-required.

**What's missing that Alex absolutely needs** (TODO for `demo_places.json` expansion — do NOT add as part of this task):

1. **A Mission / Outer Sunset cheap-eats anchor under $15** — Taqueria-style burrito, banh mi, or Chinatown noodle place that fits his "local-not-touristy + budget" sweet spot. Burma Superstar is close but $$ and on Clement, not in the high-density Mission walking corridor.
2. **A small live music / underground venue** — The Independent, Bottom of the Hill, Knockout, Rickshaw Stop. Currently zero music / nightlife in inventory; closest is `spaced_out_comedy` (San Jose, not transit-accessible for Alex).
3. **A Dolores Park or comparable free urban hangout** — Sit-on-the-grass + people-watch + skyline view. Currently Yerba Buena Gardens is the only urban free park, and it's a transit-segment of a different vibe (corporate plaza, not "Saturday afternoon scene").
4. **A walkable shopping / browsing street as an entity** — Valencia Street, Divisadero, Hayes Valley, Clement Street. Right now individual restaurants live on these streets but the *street itself as a 90-minute walking experience* (with attached bookstore / vintage / record store stops) isn't represented.
5. **A Chinatown / Japantown anchor that's not the tourist version** — Stockton St dim sum (e.g. Good Mong Kok), Mister Jiu's at the casual hour, Japantown ramen alleys. Currently zero Chinatown or Japantown coverage in the inventory at all.

---

## Place coverage gap for Persona D (Sam)

Audit of the current 12-place `demo_places.json` against Sam's intake:

**What fits (roughly)**: Almost nothing. `philz_milpitas` (warm + slow + familiar — but wrong geography, South Bay not Marin), `yerba_buena_gardens` (quiet-ish + walkable — but urban SF plaza, wrong vibe for "Marin recovery day"), `sightglass_sf` (polished + slow — but SoMa, not on the route from Mission to Marin and too "designed cafe" for her recovery aesthetic). Generously **1–3 of 12** fit, and even those are weak matches. The inventory is heavy on South Bay + SF urban; **Marin coverage is zero**.

**What's missing that Sam absolutely needs** (TODO for `demo_places.json` expansion — do NOT add as part of this task):

1. **A Marin Headlands / Mt. Tam trail with morning-light + tree-canopy SPF safety** — Bohemian Grove Trail (Muir Woods, pre-9:30am window before tour buses), Matt Davis Trail (Tam), Tennessee Valley Trail. Currently zero Marin trail coverage and zero "tree-canopy = SPF-friendly post-procedure" annotation in any place's logistics block.
2. **A Stinson Beach off-season weekday anchor (cloud-covered, north-end walking)** — distinct from the summer-sunbathe stereotype. Currently zero coast coverage at all.
3. **A Mill Valley downtown small-square anchor (Equator Coffee + the indie bookstore that isn't Book Passage)** — the "Mill Valley as Saturday-morning ritual town" entity. Currently zero Mill Valley coverage.
4. **A Tomales Bay / Hog Island farm-side oyster experience (NOT the Ferry Building outpost)** — the actual farm at Marshall, weekday lunch, picnic tables, BYO bread. Currently zero oyster / Tomales Bay coverage.
5. **A non-chlorine, non-high-heat spa or mineral-bath anchor** — Osmosis Day Spa (Freestone, cedar enzyme bath), Wilbur Hot Springs, Vichy Springs (Ukiah edge of range). Critical because every "spa day" suggestion in standard concierge tooling defaults to chlorine pools or high-heat saunas, both blocked by Sam's post-procedure constraints.

---

## How these flow through the agent

```
[persona.json]            ← demo input (stubs for real intake)
        │
        ▼
[IntakeState]             ← serialize_to_experience_request
        │
        ▼
[backend /experience]     ← in POC, falls back to demo_places.json
        │
        ▼
[PlaceCandidate[]]
        │
        ▼
[Composer + composer_prompt.md]
        │
        ▼
[TripPlan as Markdown]    ← rendered by OpenClaw
```

---

## Adding a new persona

1. Open ChatGPT (with Memory enabled).
2. Paste the persona-extraction prompt (lives in conversation history, search "persona-extraction prompt").
3. Adjust the prompt's framing if the new persona doesn't fit "Bay Area family Saturday" assumption.
4. Save the returned JSON as `<name>_persona.json` in this folder.
5. Update the table in this README under "Typical Personas" if it's a new test fixture, OR keep it in a `personas/adhoc/` subfolder if it's just a one-off.

---

## Adding a new demo place

1. Find the place in real Bay Area inventory (Foursquare OS dataset, Google Maps, your own memory).
2. Match the slim Place v2 schema in `demo_places.json` (composition.vibe_tags weighted, pacing_roles, narrative_hook, logistics).
3. Hand-tag vibe — 30 seconds per place if you have a sense of the place; longer if you need to look it up.
4. Add `compatibility_hints.good_after` / `good_before` if you can think of natural pairings — this directly improves Composer arc quality.
5. Update `_meta.place_count` and `_meta.city_coverage` if it adds a new city.
