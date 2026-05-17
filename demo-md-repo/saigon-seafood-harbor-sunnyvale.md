---
schema_version: mvp-list.place.v1
name: "Saigon Seafood Harbor"
place_type: restaurant
status: candidate
site_ids:
  - site: official_site
    id: null
    url: "https://saigonharbors.com/"
    confidence: medium
  - site: other
    id: null
    url: "https://dinfo.me/saigon/index.php/welcome/menu"
    confidence: medium
location:
  lat: null
  lon: null
  normalized_address: "1135 N. Lawrence Exp, Sunnyvale, CA 94089"
  city: "Sunnyvale"
  region: "CA"
  country: "US"
open_hours:
  raw:
    Monday-Friday:
      lunch: "11:00 AM - 2:30 PM"
      dinner: "4:30 PM - 7:30 PM"
    Saturday-Sunday:
      lunch: "10:00 AM - 2:30 PM"
      dinner: "4:30 PM - 7:30 PM"
  timezone: "America/Los_Angeles"
  source_url: "https://dinfo.me/saigon/index.php/welcome/menu"
  retrieved_at: "2026-05-16"
family_context:
  visited: null
  liked_if_visited: null
  baby_friendly_notes: "Large dim sum and seafood dining room with cart service per Eater; likely better for group/family meals than quiet naps. Confirm high-chair availability and wait times."
tags:
  - restaurant
  - dim-sum
  - cantonese
  - seafood
  - sunnyvale
sources:
  - url: "https://sf.eater.com/maps/best-san-jose-south-bay-area-restaurants"
    title: "The 25 Best South Bay Area Restaurants"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - dishes
      - other
  - url: "https://saigonharbors.com/"
    title: "Saigon Seafood Harbor"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
  - url: "https://dinfo.me/saigon/index.php/welcome/menu"
    title: "Saigon Seafood Harbor Sunnyvale Order/Menu"
    retrieved_at: "2026-05-16"
    used_for:
      - address
      - hours
      - dishes
      - price
  - url: "https://www.tripadvisor.com/Restaurant_Review-g33146-d811727-Reviews-Saigon_Seafood_Harbor-Sunnyvale_California.html"
    title: "Saigon Seafood Harbor on Tripadvisor"
    retrieved_at: "2026-05-16"
    used_for:
      - rating
      - price
      - address
      - other
confidence_notes:
  - "Eater links the saigonharbors.com domain, but the current structured menu/hours were available on dinfo.me/saigon."
  - "Tripadvisor hours differ from dinfo menu hours; structured hours use the menu/order page because it appears operational."
  - "Coordinates were not copied because no stable coordinate source was captured in this pass."
restaurant:
  cuisine_type:
    - "Cantonese"
    - "Dim sum"
    - "Chinese seafood"
  ratings:
    - site: other
      rating: 3.9
      review_count: 61
      source_url: "https://www.tripadvisor.com/Restaurant_Review-g33146-d811727-Reviews-Saigon_Seafood_Harbor-Sunnyvale_California.html"
      retrieved_at: "2026-05-16"
  top_dishes:
    - name: "Pork rice noodle rolls"
      description: "Eater lists pork rice noodle rolls among dim sum standouts."
      source_url: "https://sf.eater.com/maps/best-san-jose-south-bay-area-restaurants"
    - name: "Scallop dumplings"
      description: "Eater lists scallop dumplings among dim sum standouts."
      source_url: "https://sf.eater.com/maps/best-san-jose-south-bay-area-restaurants"
    - name: "House special chicken"
      description: "Order/menu page lists house special chicken as a Saigon Special item."
      source_url: "https://dinfo.me/saigon/index.php/welcome/menu"
    - name: "Steamed pork buns"
      description: "Eater lists steamed pork buns among dim sum standouts."
      source_url: "https://sf.eater.com/maps/best-san-jose-south-bay-area-restaurants"
  price_range:
    symbol: "$$"
    text: "Tripadvisor lists price as $$ - $$$; menu page shows individual item prices such as sliced beef shank and BBQ pork at $20.80."
    source_url: "https://www.tripadvisor.com/Restaurant_Review-g33146-d811727-Reviews-Saigon_Seafood_Harbor-Sunnyvale_California.html"
  vibe: "Busy Cantonese dim sum and seafood restaurant with cart service, seafood tanks, large dining room, and group-friendly energy."
---

# Saigon Seafood Harbor

## Summary

Saigon Seafood Harbor is a Sunnyvale Cantonese dim sum and seafood restaurant. Eater highlights cart service, seafood selection, and a large dining room.

## Visit Facts

- Type: restaurant
- Address: 1135 N. Lawrence Exp, Sunnyvale, CA 94089
- Hours: menu/order page lists weekday lunch 11:00 AM-2:30 PM and dinner 4:30 PM-7:30 PM; weekend lunch 10:00 AM-2:30 PM and dinner 4:30 PM-7:30 PM
- Price: Tripadvisor $$ - $$$
- Rating: Tripadvisor 3.9 from 61 reviews as retrieved

## Restaurant Notes

- Cuisine: Cantonese dim sum and seafood
- Sourced dishes: pork rice noodle rolls, scallop dumplings, house special chicken, steamed pork buns
- Family note: group dining energy; verify wait, noise, and baby seating.

## Sources

- Eater South Bay list: https://sf.eater.com/maps/best-san-jose-south-bay-area-restaurants
- Eater-linked official site: https://saigonharbors.com/
- Menu/order page: https://dinfo.me/saigon/index.php/welcome/menu
- Tripadvisor: https://www.tripadvisor.com/Restaurant_Review-g33146-d811727-Reviews-Saigon_Seafood_Harbor-Sunnyvale_California.html

## Confidence Notes

- Official domain is sparse in the fetched text; menu/order page supplied operational details.
- Hours conflict across public sources, so verify before final planning.
