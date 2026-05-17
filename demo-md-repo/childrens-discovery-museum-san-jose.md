---
schema_version: mvp-list.place.v1
name: "Children's Discovery Museum of San Jose"
place_type: point_of_attraction
status: candidate
site_ids:
  - site: official_site
    id: null
    url: "https://www.cdm.org/"
    confidence: high
location:
  lat: null
  lon: null
  normalized_address: "180 Woz Way, San Jose, CA 95110"
  city: "San Jose"
  region: "CA"
  country: "US"
open_hours:
  raw: "School-year hours: Tuesday through Friday 9:30 am-1:00 pm; Saturday and Sunday 9:30 am-4:30 pm. Memorial Day Monday, May 25: 9:30 am-4:30 pm."
  timezone: "America/Los_Angeles"
  source_url: "https://www.cdm.org/hours-pricing/"
  retrieved_at: "2026-05-16"
family_context:
  visited: null
  liked_if_visited: null
  baby_friendly_notes: "Purpose-built for families with young children; Wonder Cabinet is for ages 0-4, infants under 1 are free, exhibit spaces are wheelchair accessible, and the fact sheet notes a quiet/private room for nursing or calming down."
tags:
  - point-of-attraction
  - museum
  - childrens-museum
  - san-jose
  - family
  - toddler-friendly
sources:
  - url: "https://www.cdm.org/contact-us/"
    title: "Children's Discovery Museum Contact Us"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - hours
      - other
  - url: "https://www.cdm.org/hours-pricing/"
    title: "Children's Discovery Museum Hours & Pricing"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - hours
      - other
  - url: "https://www.cdm.org/exhibits/"
    title: "Children's Discovery Museum Exhibits"
    retrieved_at: "2026-05-16"
    used_for:
      - attractions
      - other
  - url: "https://www.cdm.org/wp-content/uploads/2025/07/Museum-Fact-Sheet-June-2024.pdf"
    title: "Children's Discovery Museum Fact Sheet June 2024"
    retrieved_at: "2026-05-16"
    used_for:
      - attractions
      - other
confidence_notes:
  - "Official website pages confirm school-year hours, address, admission context, access notes, and exhibit names."
  - "The June 2024 fact sheet is useful background but may be less current than the live hours page."
  - "Coordinates were not recorded because the official pages used here did not publish lat/lon in visible content."
point_of_attraction:
  category: museum
  estimated_visit_duration: "2-3 hours for young children; shorter for toddlers depending on energy and nap timing."
  attractions:
    - name: "Wonder Cabinet"
      description: "Hands-on environment rich in materials and textures for the museum's youngest visitors, ages 0-4."
      source_url: "https://www.cdm.org/exhibits/"
    - name: "WaterWays"
      description: "Splash-zone exhibit where children follow balls through spouts, whirlpools, and a water course while learning physics."
      source_url: "https://www.cdm.org/exhibits/"
    - name: "Bill's Backyard"
      description: "Half-acre outdoor nature space designed for curiosity, outdoor appreciation, and exploration."
      source_url: "https://www.cdm.org/exhibits/"
    - name: "Mammoth Discovery!"
      description: "Exhibit featuring Lupe, a 14,000-year-old mammoth whose fossils were discovered near the Guadalupe River."
      source_url: "https://www.cdm.org/exhibits/"
---

# Children's Discovery Museum of San Jose

## Summary

Children's Discovery Museum of San Jose is a family-focused children's museum with indoor play-based exhibits, outdoor nature spaces, and dedicated experiences for toddlers and young children.

## Visit Facts

- Type: point_of_attraction / museum
- Address: 180 Woz Way, San Jose, CA 95110
- Hours: school-year hours Tuesday-Friday 9:30 am-1:00 pm; Saturday-Sunday 9:30 am-4:30 pm.
- Estimated visit duration: 2-3 hours
- Family notes: very baby/toddler friendly; infants under 1 are free, Wonder Cabinet is for ages 0-4, and the museum notes a quiet/private room for nursing or calming down.

## Point Of Attraction Notes

- Key points of interest: Wonder Cabinet, WaterWays, Bill's Backyard, Mammoth Discovery.

## Sources

- https://www.cdm.org/contact-us/
- https://www.cdm.org/hours-pricing/
- https://www.cdm.org/exhibits/
- https://www.cdm.org/wp-content/uploads/2025/07/Museum-Fact-Sheet-June-2024.pdf

## Confidence Notes

- Official pages support the structured facts above.
- Coordinates remain null because they were not independently confirmed from the requested official visitor pages.
