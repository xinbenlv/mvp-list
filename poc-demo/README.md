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
| `README.md` | This file | When the asset list changes |

---

## Typical Personas (test fixtures)

The two persona JSONs serve as the **canonical contrast pair** for testing the Day Composer agent. They are deliberately chosen to span opposing axes of the intake ontology:

| Dimension | Mia (Persona A) | Garry (Persona B) |
|---|---|---|
| `emotional_intent` | restore + reconnect | explore + reconnect |
| `energy_level` | medium | **high** |
| `chaos_tolerance` | **low** | medium |
| `novelty_appetite` | high | high |
| `start_location` | South Bay (Sunnyvale-ish) | **San Francisco** |
| `max_drive_minutes` | 45 | **30 (urban, walking-friendly)** |
| `vibe_signature` peaks | restorative · cinematic · natural_light · intimate | **cinematic · lively · authentic · hip** |
| `social_config` | couple + family_with_baby | family_with_baby |
| Top `avoidance` | touristy, rushed, parking_uncertain | touristy, **polished_but_soulless**, rushed |

→ **Quality bar**: If the Composer produces a magical TripPlan for BOTH personas, it's not overfit. If it produces a great plan for one and a generic plan for the other, the prompt or Concept Generator needs work.

→ **Stranger test**: Read any `why_fits_today` from a plan. Can you tell which persona it was generated for? If no, the prompt is too generic.

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
