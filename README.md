# MVP List

Video:

- Loom: https://www.loom.com/share/ca3b0206677b4876ab366be071eea700
- YouTube: https://youtu.be/UkfaMJhq5qk
- Twitter: https://x.com/ZainanZhou/status/2055841420318261731?s=20

Powered by GBrain and built with GStack, "MVP List" is a small project for planning family getaway trips from a growing backlog of restaurants and points of attraction.

The current focus is the MVP List pipeline: curate candidate places, enrich place Markdown for structured search, propose ranked day plans, and render the chosen plan as a timed agenda.

![MVP List deck animation](images-v2.1/mvp-list-animation.gif)

## Current Scope

- Curate places discovered from social media, search, map links, screenshots, photos, or itinerary text.
- Enrich each place into a structured Markdown `Place` record.
- Propose ranked plans from a Markdown place repo.
- Render selected plans as timed agendas.
- Support two first-class place types:
  - `restaurant`
  - `point_of_attraction`
- Capture canonical external references such as Google Maps, Yelp, Apple Maps, or official site IDs/URLs.
- Preserve source URLs and retrieval dates for facts such as address, hours, ratings, price, dishes, and attractions.

Out of scope for the first version:

- Overview image generation.
- Fully automatic weekly scheduling without user constraints.

## Repository Layout

- `prd.md`: product notes and first-pass requirements.
- `skill/mvp-list-curate/`: extract candidate places from URLs, images, and itineraries.
- `skill/mvp-list-enrich/`: enrich one place Markdown record using public sources.
- `skill/mvp-list-propose/`: filter/rank places and compose three plan proposals.
- `skill/mvp-list-render/`: render an approved plan as a timed agenda.
- `skill/_shared/references/place-markdown-template.md`: gbrain-ready Markdown template for indexed places.
- `skill/_shared/references/place.schema.json`: JSON Schema for indexed places.
- `skill/_shared/references/place-template.json`: empty draft template that validates against the schema.
- `demo-md-repo/`: shareable demo Markdown place corpus for deployment and testing.
- `deck-prompt-*.md`: prompt drafts for the project deck.
- `image-v2/`, `images-v1/`, `images-v2.1/`: generated deck images.

## Install The Skill

See [INSTALLATION.md](INSTALLATION.md) for installing the `mvp-list` skill into Codex and Claude.

## Example Invocation

```text
Use mvp-list-curate on this itinerary, then mvp-list-enrich each place into ./demo-md-repo.
```

```text
Use mvp-list-propose to make three Saturday family trip plans from ./demo-md-repo, then mvp-list-render the safest one.
```
