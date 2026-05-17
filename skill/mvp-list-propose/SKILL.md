---
name: mvp-list-propose
description: Use when selecting and ranking MVP List places from a Markdown repo to propose trip plans. Applies filters such as location, open hours, infant friendliness, visited/liked history, place type, route fit, and user preferences, then composes three candidate plans.
---

# MVP List Propose

Propose reads schema-shaped Place Markdown records and creates three candidate plans. It does not render final timed agendas; use `mvp-list-render` after the user picks or approves a plan.

## Inputs

- Markdown repo path, usually `./demo-md-repo`, `./.tmp/gbrain`, or `$GBRAIN_REPO`.
- Trip date, start/end time, home/base location, driving radius, must-visit places, avoid list, meal needs, infant constraints, visited/liked history.
- If any critical constraint is missing, make a conservative assumption and list it.

## Workflow

1. Load places
   - Read `*.md` files.
   - Parse YAML frontmatter between `---`.
   - Validate against `../_shared/references/place.schema.json` when practical.
   - Ignore records that cannot be parsed unless the user asks for repair.

2. Filter
   - Type balance: usually one or two `point_of_attraction` stops plus lunch/dinner restaurants.
   - Location: keep places within the requested area or route corridor.
   - Open hours: remove places clearly closed during intended visit windows; keep uncertain hours with a risk note.
   - Infant friendliness: prefer short walks, parking, picnic/rest areas, flexible timing, easy exits, lower noise.
   - Been-to status: use `family_context.visited` and `liked_if_visited`; avoid repeats unless liked or requested.
   - Weather/season/access risks: consider outdoor exposure, closures, weekend-only or weekday-only restrictions.

3. Score
   - Assign a transparent 1-5 score for route fit, hours fit, infant fit, novelty, confidence, and meal fit.
   - Penalize missing critical data; do not hide uncertainty.

4. Compose three plans
   - Plan A: safest/default family-friendly plan.
   - Plan B: scenic or highlight-heavy plan.
   - Plan C: fallback or lower-effort plan.
   - Each plan should include ordered stops, rough windows, why it works, risks, and backup swaps.

## Output

```markdown
## Plan A — <short name>

- Stops: <ordered places>
- Why this works: <route/hours/infant rationale>
- Risks: <closures, missing hours, weather, access>
- Backup swaps: <place -> place>
- Score: <summary>

## Plan B — <short name>
...

## Plan C — <short name>
...
```

Ask the user to choose one plan or request a merge before using `mvp-list-render`.
