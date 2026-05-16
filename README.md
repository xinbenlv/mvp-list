# MVP List

MVP List is a small project for planning family getaway trips from a growing backlog of restaurants and points of attraction.

The current focus is the curation and indexing stage: take a place from a URL or image, resolve a canonical reference for it, enrich the place with structured metadata, and prepare a Markdown record for gbrain indexing.

![MVP List deck animation](images-v2.1/mvp-list-animation.gif)

## Current Scope

- Curate places discovered from social media, search, map links, screenshots, or photos.
- Index each place into a structured Markdown `Place` record.
- Support two first-class place types:
  - `restaurant`
  - `point_of_attraction`
- Capture canonical external references such as Google Maps, Yelp, Apple Maps, or official site IDs/URLs.
- Preserve source URLs and retrieval dates for facts such as address, hours, ratings, price, dishes, and attractions.

Out of scope for the first version:

- Weekly trigger and ranking.
- Agenda generation.
- Overview image generation.
- Automatic trip planning across multiple places.

## Repository Layout

- `prd.md`: product notes and first-pass requirements.
- `skill/mvp-list/`: installable Codex/Claude skill package.
- `skill/mvp-list/SKILL.md`: skill workflow for `/mvp-list add <url>` and `/mvp-list add <image>`.
- `skill/mvp-list/references/place-markdown-template.md`: gbrain-ready Markdown template for indexed places.
- `skill/mvp-list/references/place.schema.json`: JSON Schema for indexed places.
- `skill/mvp-list/references/place-template.json`: empty draft template that validates against the schema.
- `deck-prompt-*.md`: prompt drafts for the project deck.
- `image-v2/`, `images-v1/`, `images-v2.1/`: generated deck images.

## Install The Skill

See [INSTALLATION.md](INSTALLATION.md) for installing the `mvp-list` skill into Codex and Claude.

## Example Invocation

```text
/mvp-list add https://example.com/place-page
```

```text
/mvp-list add <image>
```

The skill should identify the place, resolve one canonical reference, fill the Place fields as much as possible, and either write Markdown to gbrain or pause with a Markdown draft if gbrain is not installed or configured.
