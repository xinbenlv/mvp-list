---
name: mvp-list-curate
description: Use when extracting candidate MVP List places from a URL, image, pasted itinerary, map link, menu link, or free-form note. Identifies restaurant and point_of_attraction places, resolves canonical references, and creates minimal schema-shaped Markdown candidates for later enrichment.
---

# MVP List Curate

Curate turns raw discovery inputs into one or more candidate Place Markdown records. It does identity resolution and light normalization only; use `mvp-list-enrich` to fill hours, ratings, dishes, attractions, and family context.

## Inputs

- Single place URL: Google Maps, Yelp, Apple Maps, official site, menu page.
- Image or screenshot: extract visible names, signs, addresses, menus, or landmarks first.
- Itinerary text: extract every public place, including alternate options; skip non-public stops such as home breakfast.

## Workflow

1. Extract place candidates
   - Keep both restaurants and attractions.
   - Treat sub-items inside a venue as nested facts unless they are independently visitable public places.
   - For itinerary options, create separate candidates for each option.

2. Resolve identity
   - Cross-check name, city, address, coordinates, official site, or map URL.
   - Prefer one canonical reference: Google Maps stable URL/id, Yelp alias, Apple Maps URL/id, or official site.
   - If multiple same-name places remain plausible, stop and ask for disambiguation.

3. Classify
   - `restaurant`: food service is the primary reason to visit.
   - `point_of_attraction`: parks, gardens, museums, landmarks, trails, stores used as historic sites, photo spots.

4. Write candidate Markdown when requested
   - Use `../_shared/references/place-markdown-template.md` as the shape.
   - Frontmatter must follow `../_shared/references/place.schema.json`.
   - Keep uncertain fields as `null`; do not invent missing address, coordinates, hours, ratings, dishes, or attractions.
   - Set `status: candidate`.
   - Save into the requested Markdown repo, for example `./demo-md-repo` or `./.tmp/gbrain`.

## Google Maps Parsing

- Decode `/place/<name>` into the name candidate, treating `+` as spaces.
- Extract `!3d<lat>!4d<lon>` as the preferred coordinates.
- Extract `!1s<feature_id>` or `!16s<token>` as Google reference hints.
- Ignore sharing parameters such as `entry` and `g_ep` for identity.

## Output

Return a concise list of candidates:

```markdown
- <name> — <restaurant | point_of_attraction> — <canonical_reference> — <candidate_file_or_needs_disambiguation>
```

Then hand off each candidate to `mvp-list-enrich` when the user wants fully searchable records.
