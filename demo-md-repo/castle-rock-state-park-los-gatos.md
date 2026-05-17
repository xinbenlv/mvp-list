---
schema_version: mvp-list.place.v1
name: "Castle Rock State Park"
place_type: point_of_attraction
status: candidate
site_ids:
  - site: official_site
    id: null
    url: "https://www.parks.ca.gov/?lang=en&page_id=538"
    confidence: high
location:
  lat: null
  lon: null
  normalized_address: "Highway 35, 2.5 miles southeast of the junction with Highway 9, Los Gatos, CA"
  city: "Los Gatos"
  region: "CA"
  country: "US"
open_hours:
  raw:
    day_use_hours: "6:00 AM-sunset"
    kirkwood_entrance_station_hours: "8:00 AM-5:00 PM, Monday-Sunday"
    reservation_note: "Trail camps require registration or reservations; backcountry trail camps are reservable."
    restrictions: "Dogs are prohibited throughout the park except for service animals; drones, glass containers, smoking, firearms, and off-trail damage/removal of natural features are prohibited."
    access_note: "No visitor center or store facilities; no cell reception within the park and surrounding area, so ridesharing services are not recommended. Climbing facilities can close for up to three days after measurable rain."
  timezone: "America/Los_Angeles"
  source_url: "https://www.parks.ca.gov/?lang=en&page_id=538"
  retrieved_at: "2026-05-16"
family_context:
  visited: null
  liked_if_visited: null
  baby_friendly_notes: "Strong hiking and viewpoints, but not a stroller-forward park: dogs are prohibited except service animals, cell reception is poor, and many routes are rugged."
tags:
  - point-of-attraction
  - state-park
  - hiking
  - santa-cruz-mountains
  - rock-formations
  - waterfall
  - viewpoints
  - los-gatos
sources:
  - url: "https://www.parks.ca.gov/?lang=en&page_id=538"
    title: "Castle Rock State Park - California State Parks"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - hours
      - attractions
      - other
confidence_notes:
  - "Official California State Parks page was used for identity, location, hours, reservation/access notes, restrictions, and attraction names."
  - "Coordinates are null because only official-page-confirmed structured facts are used."
  - "Trail-camp reservations, no cell reception, no visitor center/store, dog restrictions, and post-rain climbing closures are key planning risks."
  - "Address is represented as the official highway location text because the official page checked did not expose a street-number address."
point_of_attraction:
  category: park
  estimated_visit_duration: "2-4 hours for Castle Rock and viewpoint hikes; half-day to full-day for longer Saratoga Gap or backpacking routes."
  attractions:
    - name: "Castle Rock formations"
      description: "Official park page describes the park as known for sculpted sandstone, including Castle Rock and other formations used for hiking and climbing context."
      source_url: "https://www.parks.ca.gov/?lang=en&page_id=538"
    - name: "Castle Rock Trail Camp"
      description: "Official park page lists remote and hike-and-bike camping and says trail camps require registration or reservations."
      source_url: "https://www.parks.ca.gov/?lang=en&page_id=538"
    - name: "Saratoga Gap Trail"
      description: "Official park page identifies Saratoga Gap Trail among park route options and highlights the broader trail network."
      source_url: "https://www.parks.ca.gov/?lang=en&page_id=538"
    - name: "Castle Rock Falls"
      description: "Official page highlights waterfalls and scenic Santa Cruz Mountains features as part of the park experience."
      source_url: "https://www.parks.ca.gov/?lang=en&page_id=538"
---

# Castle Rock State Park

## Summary

Castle Rock State Park is a California state park in the Santa Cruz Mountains near Los Gatos, known for sandstone formations, hiking, climbing context, waterfalls, and ridge viewpoints.

## Visit Facts

- Location: Highway 35, 2.5 miles southeast of Highway 9, Los Gatos area
- Hours: 6:00 AM-sunset
- Kirkwood entrance station: 8:00 AM-5:00 PM, Monday-Sunday
- Access risk: trail camps require registration or reservations
- Trail/climbing risk: climbing facilities can close after measurable rain; current page showed climbing, trail, and trail camp status open
- Connectivity risk: no cell reception in the park and surrounding area; ridesharing not recommended
- Restrictions: dogs prohibited except service animals; drones, smoking, and glass containers prohibited

## Point Of Attraction Notes

- Category: park / state park
- Key points of interest: Castle Rock formations, Castle Rock Trail Camp, Saratoga Gap Trail, Castle Rock Falls
- Best use: rugged hike, scenic viewpoint plan, climbing-adjacent visit, or longer Santa Cruz Mountains route

## Sources

- https://www.parks.ca.gov/?lang=en&page_id=538

## Confidence Notes

- Official California State Parks page was sufficient for identity, hours, restrictions, access notes, and attractions.
- Coordinates are intentionally null because no official coordinate was used.
