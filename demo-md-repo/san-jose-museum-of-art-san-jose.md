---
schema_version: mvp-list.place.v1
name: "San Jose Museum of Art"
place_type: point_of_attraction
status: candidate
site_ids:
  - site: official_site
    id: null
    url: "https://sjmusart.org/"
    confidence: high
location:
  lat: null
  lon: null
  normalized_address: "110 South Market Street, San Jose, CA 95113"
  city: "San Jose"
  region: "CA"
  country: "US"
open_hours:
  raw: "Museum + Store: Thursday 4-9pm; Friday 11am-9pm; Saturday-Sunday 11am-6pm. Museum Cafe: Thursday 4-9pm; Friday 11am-9pm; Saturday-Sunday 11am-3pm."
  timezone: "America/Los_Angeles"
  source_url: "https://sjmusart.org/visit"
  retrieved_at: "2026-05-16"
family_context:
  visited: null
  liked_if_visited: null
  baby_friendly_notes: "Youth 17 and under receive free individual tickets. Best fit for art-looking and short gallery visits with children; note the visitor page's temporary elevator outage notice before bringing a stroller."
tags:
  - point-of-attraction
  - museum
  - art
  - contemporary-art
  - san-jose
  - family
sources:
  - url: "https://sjmusart.org/visit"
    title: "San Jose Museum of Art Visit"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - hours
      - other
  - url: "https://sjmusart.org/exhibitions"
    title: "San Jose Museum of Art On View"
    retrieved_at: "2026-05-16"
    used_for:
      - attractions
      - other
confidence_notes:
  - "Official SJMA pages confirm identity, address, public hours, admissions notes, and current/on-going exhibition highlights."
  - "Visitor page included a temporary elevator-out-of-service notice; refresh before stroller-dependent visits."
  - "Coordinates were not recorded because the official pages used here did not publish lat/lon in visible content."
point_of_attraction:
  category: museum
  estimated_visit_duration: "1.5-2.5 hours for galleries, store, cafe, and optional docent tour."
  attractions:
    - name: "Motherboards"
      description: "Exhibition through January 10, 2027 exploring women's foundational contributions to the technology industry."
      source_url: "https://sjmusart.org/exhibitions"
    - name: "Koret Gallery: Art Learning Lab"
      description: "Ongoing STEAM-inspired exhibition space with permanent-collection works focused on cross-disciplinary art-making."
      source_url: "https://sjmusart.org/exhibitions"
    - name: "Tending and Dreaming: Stories from the Collection"
      description: "Ongoing collection-gallery exhibition presenting core works in San Jose's publicly held art collection."
      source_url: "https://sjmusart.org/exhibitions"
    - name: "Docent-led public tours"
      description: "Drop-in tours are offered Thursday at 5pm and Friday-Sunday at 1 and 2:30pm, meeting in the Museum lobby."
      source_url: "https://sjmusart.org/visit"
---

# San Jose Museum of Art

## Summary

San Jose Museum of Art is a downtown contemporary art museum with rotating exhibitions, collection galleries, a store, cafe, community events, and public tours.

## Visit Facts

- Type: point_of_attraction / museum
- Address: 110 South Market Street, San Jose, CA 95113
- Hours: Thursday 4-9pm; Friday 11am-9pm; Saturday-Sunday 11am-6pm.
- Estimated visit duration: 1.5-2.5 hours
- Family notes: youth 17 and under are free; refresh accessibility status if using stroller or elevator access.

## Point Of Attraction Notes

- Key points of interest: Motherboards, Art Learning Lab, Tending and Dreaming, docent-led public tours.

## Sources

- https://sjmusart.org/visit
- https://sjmusart.org/exhibitions

## Confidence Notes

- Official pages support the structured facts above.
- Coordinates remain null because they were not independently confirmed from the requested official visitor pages.
