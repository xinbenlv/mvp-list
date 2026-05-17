---
name: mvp-list-enrich
description: Use when enriching an MVP List Place Markdown record using all available public data sources. Completes schema-shaped YAML frontmatter for structured search, including restaurant top_dishes and attraction points of interest, then validates against place.schema.json.
---

# MVP List Enrich

Enrich takes a candidate Place Markdown record or a resolved place and fills the structured YAML frontmatter for search. The Markdown body is only for human review; structured fields must live in frontmatter.

## References

- Schema: `../_shared/references/place.schema.json`
- Markdown template: `../_shared/references/place-markdown-template.md`
- Empty JSON field reference: `../_shared/references/place-template.json`

## Source Strategy

- Verify dynamic facts from current public sources: official site, Google Maps, Yelp, Apple Maps, OpenTable, delivery apps, booking pages, government/park pages, official PDFs, maps, brochures, trail organizations, and reputable local guides.
- Preserve source URL and retrieval date for every factual group.
- Never fabricate uncertain facts. Use `null` and `confidence_notes`.

## Required Enrichment

Common fields:

- `site_ids`: at least one canonical reference.
- `location`: address, city, region, country, coordinates when source-confirmed.
- `open_hours`: raw hours, timezone, source URL, retrieval date.
- `family_context`: visited/liked fields if known; infant/baby notes from evidence or explicit itinerary context.
- `sources` and `confidence_notes`.

For `restaurant`:

- Fill `restaurant.cuisine_type`, `ratings`, `price_range`, and `vibe` where available.
- Fill `restaurant.top_dishes` with sourced popular dishes, signature dishes, or high-frequency menu items.
- Dish source priority: official menu, ordering platform, reservation platform, review platform, menu aggregator.
- Each dish must have `name`, `description`, and `source_url`; use `description: null` if only the name is confirmed.

For `point_of_attraction`:

- Fill `point_of_attraction.category`, `estimated_visit_duration`, and `attractions`.
- Fill `point_of_attraction.attractions` with sourced key points of interest: trails, viewpoints, exhibits, buildings, gardens, picnic areas, photo spots, landmarks, or activity zones.
- Attraction source priority: official venue/park page, official map/PDF/brochure, public agency page, conservation/trail organization, reputable local guide.
- Each attraction must have `name`, `description`, and `source_url`.

## Markdown Writing

When writing to a directory-style Markdown repo:

1. Resolve target path from user input, `$GBRAIN_REPO`, `./demo-md-repo`, or `./.tmp/gbrain`.
2. Use a slug file name like `<place-name>-<city>.md`.
3. Put the full schema-shaped object in YAML frontmatter.
4. Put readable notes in `Summary`, `Visit Facts`, `Restaurant Notes` or `Point Of Attraction Notes`, `Sources`, and `Confidence Notes`.
5. Parse the `---` frontmatter and validate it against `../_shared/references/place.schema.json`.
6. If no gbrain query tool exists, report only “Markdown written and schema-valid”; do not claim query indexing.

## Output

```markdown
已更新 MVP List Place：

- 地点：<name>
- 类型：<restaurant | point_of_attraction>
- 文件：<path>
- 结构化状态：frontmatter 已通过 schema 校验
- gbrain 状态：<已查询验证 | 已写入 Markdown，未验证查询索引>
- 主要缺口：<none 或字段列表>
```
