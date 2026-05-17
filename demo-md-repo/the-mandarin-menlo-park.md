---
schema_version: mvp-list.place.v1
name: "The Mandarin"
place_type: restaurant
status: candidate
site_ids:
  - site: google_maps
    id: "0x808fa5f215c2da1b:0xcffcb988178e1620"
    url: "https://www.google.com/maps/place/The+Mandarin/@37.453024,-122.184826,17z/data=!3m1!4b1!4m6!3m5!1s0x808fa5f215c2da1b:0xcffcb988178e1620!8m2!3d37.453024!4d-122.1822457!16s%2Fg%2F11rc76w1m6!5m1!1e2?entry=ttu&g_ep=EgoyMDI2MDUxMy4wIKXMDSoASAFQAw%3D%3D"
    confidence: high
  - site: official_site
    id: null
    url: "http://www.themandarinbistro.com/"
    confidence: medium
location:
  lat: 37.453024
  lon: -122.1822457
  normalized_address: "1029 El Camino Real, Menlo Park, CA 94025"
  city: "Menlo Park"
  region: "CA"
  country: "US"
open_hours:
  raw:
    monday: "11:30 AM-2:30 PM, 5:00 PM-9:00 PM"
    tuesday: "11:30 AM-2:30 PM, 5:00 PM-9:00 PM"
    wednesday: "11:30 AM-2:30 PM, 5:00 PM-9:00 PM"
    thursday: "11:30 AM-2:30 PM, 5:00 PM-9:00 PM"
    friday: "11:30 AM-2:30 PM, 5:00 PM-9:30 PM"
    saturday: "11:30 AM-2:30 PM, 5:00 PM-9:30 PM"
    sunday: "11:30 AM-2:30 PM, 5:00 PM-9:00 PM"
  timezone: "America/Los_Angeles"
  source_url: "https://www.opentable.com/r/the-mandarin-menlo-park"
  retrieved_at: "2026-05-16"
family_context:
  visited: null
  liked_if_visited: null
  baby_friendly_notes: "Family-style Sichuan and Chinese restaurant; public listings mention casual dining and groups, but baby-specific amenities were not confirmed."
tags:
  - restaurant
  - chinese
  - sichuan
  - menlo-park
  - family-style
sources:
  - url: "https://www.google.com/maps/place/The+Mandarin/@37.453024,-122.184826,17z/data=!3m1!4b1!4m6!3m5!1s0x808fa5f215c2da1b:0xcffcb988178e1620!8m2!3d37.453024!4d-122.1822457!16s%2Fg%2F11rc76w1m6!5m1!1e2?entry=ttu&g_ep=EgoyMDI2MDUxMy4wIKXMDSoASAFQAw%3D%3D"
    title: "Google Maps place URL for The Mandarin"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - other
  - url: "https://www.opentable.com/r/the-mandarin-menlo-park"
    title: "The Mandarin - OpenTable"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - hours
      - rating
      - price
      - dishes
  - url: "https://www.ubereats.com/store/the-mandarin-menlo-park/0jhe95L0XO6CQfAtV8iOaA"
    title: "The Mandarin Menlo Park - Uber Eats"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - hours
      - rating
      - dishes
  - url: "https://usarestaurants.info/explore/united-states/california/san-mateo-county/menlo-park/the-mandarin-650-391-9811.htm"
    title: "The Mandarin - usarestaurants.info"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - hours
confidence_notes:
  - "Google Maps URL provided a stable place feature id, name, and coordinates."
  - "Identity and address were cross-checked against OpenTable, Uber Eats, and usarestaurants.info."
  - "Hours, ratings, and price are dynamic and should be refreshed before a visit."
  - "Official website URL appears in public listings, but the official website itself was not independently fetched in this run."
  - "Written as Markdown into ./.tmp/gbrain; no local gbrain CLI was available to verify query ingestion."
restaurant:
  cuisine_type:
    - "Sichuan"
    - "Chinese"
  ratings:
    - site: opentable
      rating: 4.3
      review_count: 53
      source_url: "https://www.opentable.com/r/the-mandarin-menlo-park"
      retrieved_at: "2026-05-16"
    - site: ubereats
      rating: 4.7
      review_count: 290
      source_url: "https://www.ubereats.com/store/the-mandarin-menlo-park/0jhe95L0XO6CQfAtV8iOaA"
      retrieved_at: "2026-05-16"
  top_dishes:
    - name: "Green Onion Pancake"
      description: "Listed on OpenTable menu."
      source_url: "https://www.opentable.com/r/the-mandarin-menlo-park"
    - name: "Boiled Fish in Sichuan Style"
      description: "Listed on OpenTable menu."
      source_url: "https://www.opentable.com/r/the-mandarin-menlo-park"
    - name: "Dan-Dan Noodle"
      description: "Listed on OpenTable menu."
      source_url: "https://www.opentable.com/r/the-mandarin-menlo-park"
    - name: "Fried Rice"
      description: "Uber Eats listed fried rice as a highly liked featured item."
      source_url: "https://www.ubereats.com/store/the-mandarin-menlo-park/0jhe95L0XO6CQfAtV8iOaA"
  price_range:
    symbol: "$$"
    text: "OpenTable lists $30 and under; public menu listings show many dishes in the teens through $30 range, with larger whole-fish dishes higher."
    source_url: "https://www.opentable.com/r/the-mandarin-menlo-park"
  vibe: "Casual Sichuan and Chinese restaurant suitable for groups and family-style dining."
---

# The Mandarin

## Summary

The Mandarin is a Sichuan and Chinese restaurant at 1029 El Camino Real in Menlo Park, California. The structured fields for search live in the YAML frontmatter; this body is a readable summary for review.

## Visit Facts

- Address: 1029 El Camino Real, Menlo Park, CA 94025
- Coordinates: 37.453024, -122.1822457
- Hours: daily lunch 11:30 AM-2:30 PM; dinner Sunday-Thursday 5:00 PM-9:00 PM; dinner Friday-Saturday 5:00 PM-9:30 PM
- Price: OpenTable lists $30 and under
- Ratings seen: OpenTable 4.3 from 53 reviews; Uber Eats 4.7 from 290+ ratings

## Restaurant Notes

- Cuisine: Sichuan, Chinese
- Dishes to consider: green onion pancake, boiled fish in Sichuan style, dan-dan noodle, fried rice
- Vibe: casual, group-friendly, family-style dining

## Sources

- Google Maps place URL supplied by user
- OpenTable: https://www.opentable.com/r/the-mandarin-menlo-park
- Uber Eats: https://www.ubereats.com/store/the-mandarin-menlo-park/0jhe95L0XO6CQfAtV8iOaA
- usarestaurants.info: https://usarestaurants.info/explore/united-states/california/san-mateo-county/menlo-park/the-mandarin-650-391-9811.htm

## Confidence Notes

- High confidence this is The Mandarin at 1029 El Camino Real, Menlo Park, CA.
- Hours, ratings, and price are dynamic.
- This record was regenerated as schema-shaped Markdown frontmatter for structured gbrain search.
