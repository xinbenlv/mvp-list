---
schema_version: mvp-list.place.v1
name: "The Tech Interactive"
place_type: point_of_attraction
status: candidate
site_ids:
  - site: official_site
    id: null
    url: "https://www.thetech.org/"
    confidence: high
location:
  lat: null
  lon: null
  normalized_address: "201 S. Market St., San Jose, CA 95113"
  city: "San Jose"
  region: "CA"
  country: "US"
open_hours:
  raw: "Visitor page showed today's hours as 10AM-5PM and says dates/hours vary by seasonal calendar. Announced future public hours beginning June 10, 2026: closed Mondays and Tuesdays; June 10-August 9, 2026 Wednesday-Saturday 10 a.m.-5 p.m., Sunday 11 a.m.-5 p.m.; September 2, 2026-June 9, 2027 Wednesday-Friday 10 a.m.-3 p.m., Saturday 10 a.m.-5 p.m., Sunday 11 a.m.-5 p.m."
  timezone: "America/Los_Angeles"
  source_url: "https://www.thetech.org/visit/"
  retrieved_at: "2026-05-16"
family_context:
  visited: null
  liked_if_visited: null
  baby_friendly_notes: "Strong hands-on family STEM option with over 100 experiences, a cafe with family-friendly items, sensory resources, and an IMAX theater; check the daily schedule for hours and age fit."
tags:
  - point-of-attraction
  - museum
  - science
  - technology
  - stem
  - san-jose
  - family
sources:
  - url: "https://www.thetech.org/visit/"
    title: "The Tech Interactive Visit"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - hours
      - attractions
      - other
  - url: "https://www.thetech.org/about-us/press-office/press-releases/press-releases/announcement-05-14-26/"
    title: "The Tech Interactive Updates Public Hours Beginning June 10"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - hours
      - other
  - url: "https://www.thetech.org/explore/exhibits/"
    title: "The Tech Interactive Exhibits"
    retrieved_at: "2026-05-16"
    used_for:
      - attractions
  - url: "https://www.thetech.org/explore/imax-dome-theater/"
    title: "The Tech Interactive IMAX Dome Theater"
    retrieved_at: "2026-05-16"
    used_for:
      - attractions
      - other
confidence_notes:
  - "The visit page says hours vary on a seasonal calendar, so the daily schedule should be checked before a specific trip."
  - "The public-hours change begins June 10, 2026; retrieval date is before that change."
  - "Coordinates were not recorded because the official visitor pages used here did not publish lat/lon in visible content."
point_of_attraction:
  category: museum
  estimated_visit_duration: "2-4 hours depending on IMAX, labs, and hands-on exhibit pace."
  attractions:
    - name: "Innovation in Bloom"
      description: "Two-story interactive exhibit where visitors launch balls through winding tubes and build ball tracks that trigger a cascading finale."
      source_url: "https://www.thetech.org/explore/exhibits/"
    - name: "Dream Garden"
      description: "AI-powered immersive exhibit that transforms visitor ideas and movements into a surreal ecosystem for all ages and abilities."
      source_url: "https://www.thetech.org/explore/exhibits/"
    - name: "Pixel Playground"
      description: "Interactive gallery blending digital innovation with physical play, including AI animal training, coaster design, and digital painting."
      source_url: "https://www.thetech.org/explore/exhibits/"
    - name: "IMAX Dome Theater"
      description: "Bay Area IMAX dome theater with educational films included with general admission and separate Hollywood and laser offerings."
      source_url: "https://www.thetech.org/explore/imax-dome-theater/"
---

# The Tech Interactive

## Summary

The Tech Interactive is a downtown San Jose science and technology center built around hands-on exhibits, labs, design challenges, and an IMAX Dome Theater.

## Visit Facts

- Type: point_of_attraction / museum
- Address: 201 S. Market St., San Jose, CA 95113
- Hours: seasonal; visitor page showed 10AM-5PM for the retrieval day, with changed public hours announced for June 10, 2026 onward.
- Estimated visit duration: 2-4 hours
- Family notes: particularly strong for school-age children; includes cafe, sensory resources, labs, and IMAX options.

## Point Of Attraction Notes

- Key points of interest: Innovation in Bloom, Dream Garden, Pixel Playground, IMAX Dome Theater.

## Sources

- https://www.thetech.org/visit/
- https://www.thetech.org/about-us/press-office/press-releases/press-releases/announcement-05-14-26/
- https://www.thetech.org/explore/exhibits/
- https://www.thetech.org/explore/imax-dome-theater/

## Confidence Notes

- Official pages support the structured facts above.
- Coordinates remain null because they were not independently confirmed from the requested official visitor pages.
