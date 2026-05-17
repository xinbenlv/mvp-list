---
name: mvp-list-render
description: Use when turning an approved MVP List proposal into a timed agenda. Renders commute, tour, meal, rest, dish, highlight, weather, and tip sections with Google Maps links and clear time ranges.
---

# MVP List Render

Render turns a selected plan into a polished timed agenda. It assumes `mvp-list-propose` has already selected the places, but it can also render a user-provided ordered list.

## Inputs

- Date and day of week.
- Start/end location, or “home” with a provided/known map link.
- Ordered stops and desired time windows.
- Place Markdown records from the repo for map links, open hours, dishes, and attractions.
- Weather location and date when weather should be included.

## Rendering Rules

- Use 24-hour compact time ranges like `0900-0945`.
- Include commute rows between every stop.
- Link each place name to a Google Maps URL when available; otherwise use the best canonical URL.
- For restaurants, include 2-4 dish suggestions from `restaurant.top_dishes`.
- For attractions, include 2-4 key points from `point_of_attraction.attractions`.
- Include buffers for parking, bathroom, baby care, photo setup, and exit time when relevant.
- Call out closure/open-hour risks inline.
- For weather on real dates, verify current forecast before presenting it as fact; otherwise label it as a planning placeholder.

## Output Format

```markdown
YYYY-MM-DD Saturday

- 0900-0945 commute [home](<gmap>) to [Place](<gmap>)
- 0945-1245 tour at [Place](<gmap>): point A, point B, point C
- 1245-1300 commute to [Restaurant](<gmap>)
- 1300-1400 lunch at [Restaurant](<gmap>): dish A, dish B, dish C
- 1400-1430 commute to [Next Place](<gmap>)

## Highlights Of The Trip

- ...

## Weather

- ...

## Tips

- ...
```

Keep the agenda readable enough to use on the day of the trip; avoid burying the schedule in prose.
