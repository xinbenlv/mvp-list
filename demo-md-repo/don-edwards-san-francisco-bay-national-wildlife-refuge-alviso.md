---
schema_version: mvp-list.place.v1
name: "Don Edwards San Francisco Bay National Wildlife Refuge"
place_type: point_of_attraction
status: candidate
site_ids:
  - site: official_site
    id: null
    url: "https://www.fws.gov/desfbay/"
    confidence: high
location:
  lat: null
  lon: null
  normalized_address: "1751 Grand Boulevard, San Jose, CA 95002"
  city: "San Jose"
  region: "CA"
  country: "US"
open_hours:
  raw:
    alviso_environmental_education_center_vehicle_gate: "7:00 AM-5:00 PM"
    alviso_trails: "Open daily sunrise-sunset"
    fremont_visitor_center: "Saturday-Sunday 10:00 AM-2:00 PM; closed Thanksgiving, Christmas, and New Year's Day"
    fremont_vehicle_gate: "Daily 7:00 AM-7:00 PM"
    access_note: "Refuge has multiple public locations; this record centers the Alviso Environmental Education Center, while the official refuge headquarters and visitor center are in Fremont."
  timezone: "America/Los_Angeles"
  source_url: "https://www.fws.gov/refuge/don-edwards-san-francisco-bay/visit-us"
  retrieved_at: "2026-05-16"
family_context:
  visited: null
  liked_if_visited: null
  baby_friendly_notes: "Good candidate for stroller-adjacent bayland walks around the Alviso Environmental Education Center, but trail surfaces, wind, sun exposure, and seasonal closures should be checked before visiting."
tags:
  - point-of-attraction
  - national-wildlife-refuge
  - baylands
  - birding
  - trails
  - alviso
  - san-jose
  - fremont
sources:
  - url: "https://www.fws.gov/desfbay/"
    title: "Don Edwards San Francisco Bay National Wildlife Refuge - U.S. Fish and Wildlife Service"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - other
  - url: "https://www.fws.gov/refuge/don-edwards-san-francisco-bay/visit-us"
    title: "Visit Us - Don Edwards San Francisco Bay National Wildlife Refuge"
    retrieved_at: "2026-05-16"
    used_for:
      - address
      - hours
      - attractions
      - other
  - url: "https://www.fws.gov/refuge/don-edwards-san-francisco-bay/visit-us/trails"
    title: "Trails - Don Edwards San Francisco Bay National Wildlife Refuge"
    retrieved_at: "2026-05-16"
    used_for:
      - attractions
      - other
confidence_notes:
  - "Official U.S. Fish and Wildlife Service pages were used for identity, public access hours, public addresses, and trail/attraction names."
  - "Coordinates are null because the official pages checked did not provide a single canonical lat/lon for the multi-site refuge."
  - "The refuge spans multiple access points; this filename and address focus on the Alviso Environmental Education Center."
  - "Hours, gates, building access, and trail conditions are operational facts; refresh official pages before visiting."
point_of_attraction:
  category: park
  estimated_visit_duration: "1-2 hours for the Alviso Environmental Education Center area; 2-4 hours if combining Alviso trails with birding or a Fremont-side trail."
  attractions:
    - name: "Alviso Environmental Education Center"
      description: "Alviso public access point at 1751 Grand Boulevard with vehicle gate hours listed by the refuge and trails open sunrise to sunset."
      source_url: "https://www.fws.gov/refuge/don-edwards-san-francisco-bay/visit-us"
    - name: "La Riviere Marsh Trail"
      description: "Official refuge trail listing describes this as a 0.8-mile trail at the Alviso Environmental Education Center."
      source_url: "https://www.fws.gov/refuge/don-edwards-san-francisco-bay/visit-us/trails"
    - name: "Tidelands Trail"
      description: "Official refuge trail listing describes Tidelands Trail as a 1.3-mile trail at the Fremont visitor center area."
      source_url: "https://www.fws.gov/refuge/don-edwards-san-francisco-bay/visit-us/trails"
    - name: "Mallard Slough Trail"
      description: "Official refuge trail listing describes Mallard Slough Trail as a 1.6-mile trail associated with the Alviso Environmental Education Center."
      source_url: "https://www.fws.gov/refuge/don-edwards-san-francisco-bay/visit-us/trails"
---

# Don Edwards San Francisco Bay National Wildlife Refuge

## Summary

Don Edwards San Francisco Bay National Wildlife Refuge is a federal baylands refuge with Alviso and Fremont public access points, trails, environmental education, and birding around restored salt marsh and slough habitat.

## Visit Facts

- Alviso access: 1751 Grand Boulevard, San Jose, CA 95002
- Fremont headquarters and visitor center: 1 Marshlands Road, Fremont, CA 94555
- Alviso vehicle gate: 7:00 AM-5:00 PM
- Alviso trails: daily sunrise-sunset
- Fremont visitor center: Saturday-Sunday 10:00 AM-2:00 PM
- Access risk: multiple gate and building schedules; check official refuge pages before a visit

## Point Of Attraction Notes

- Category: park / national wildlife refuge
- Key points of interest: Alviso Environmental Education Center, La Riviere Marsh Trail, Tidelands Trail, Mallard Slough Trail
- Best use: light baylands walk, birding, environmental education, or a combined Alviso/Fremont refuge outing

## Sources

- https://www.fws.gov/desfbay/
- https://www.fws.gov/refuge/don-edwards-san-francisco-bay/visit-us
- https://www.fws.gov/refuge/don-edwards-san-francisco-bay/visit-us/trails

## Confidence Notes

- Official U.S. Fish and Wildlife Service pages were sufficient for identity, access hours, public addresses, and attractions.
- Coordinates are intentionally null because the refuge is multi-site and no single official coordinate was used.
