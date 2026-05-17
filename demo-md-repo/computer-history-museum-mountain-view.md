---
schema_version: mvp-list.place.v1
name: "Computer History Museum"
place_type: point_of_attraction
status: candidate
site_ids:
  - site: official_site
    id: null
    url: "https://computerhistory.org/"
    confidence: high
location:
  lat: null
  lon: null
  normalized_address: "1401 N. Shoreline Blvd., Mountain View, CA 94043"
  city: "Mountain View"
  region: "CA"
  country: "US"
open_hours:
  raw: "Regular hours: Monday and Tuesday closed; Wednesday through Sunday 10 a.m.-5 p.m. Check holiday and special hours before visiting."
  timezone: "America/Los_Angeles"
  source_url: "https://computerhistory.org/hours-admission/"
  retrieved_at: "2026-05-16"
family_context:
  visited: null
  liked_if_visited: null
  baby_friendly_notes: "Good indoor museum option for mixed ages; exhibits include hands-on coding and demonstrations, but demo times and child attention span should be checked before planning a long visit."
tags:
  - point-of-attraction
  - museum
  - computer-history
  - technology
  - mountain-view
  - family
sources:
  - url: "https://computerhistory.org/hours-admission/"
    title: "Computer History Museum Hours & Admission"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - hours
      - other
  - url: "https://computerhistory.org/visit/"
    title: "Computer History Museum Visit"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - hours
      - attractions
      - other
  - url: "https://computerhistory.org/exhibits/"
    title: "Computer History Museum Exhibits"
    retrieved_at: "2026-05-16"
    used_for:
      - attractions
  - url: "https://computerhistory.org/exhibits/revolution/"
    title: "Revolution: The First 2000 Years of Computing"
    retrieved_at: "2026-05-16"
    used_for:
      - attractions
confidence_notes:
  - "Official CHM pages confirm identity, address, regular hours, and exhibit highlights."
  - "Coordinates were not recorded because the requested official pages did not publish lat/lon in the visible visitor content."
  - "Holiday and special closures can override regular hours."
point_of_attraction:
  category: museum
  estimated_visit_duration: "2-3 hours for the main exhibits; longer if attending demonstrations or tours."
  attractions:
    - name: "Revolution: The First 2000 Years of Computing"
      description: "A 25,000-square-foot exhibition with 19 galleries, 1,100 objects, and multimedia experiences covering computing from the abacus to the smartphone."
      source_url: "https://computerhistory.org/exhibits/revolution/"
    - name: "Chatbots Decoded: Exploring AI"
      description: "Immersive AI exhibit where visitors can explore chatbot history, interact with a chatbot-powered robot, and consider the future of conversational AI."
      source_url: "https://computerhistory.org/exhibits/"
    - name: "Make Software: Change the World!"
      description: "Hands-on software exhibit featuring applications such as MP3, Photoshop, MRI, car crash simulation, Wikipedia, texting, and World of Warcraft."
      source_url: "https://computerhistory.org/exhibits/"
    - name: "IBM 1401 and PDP-1 Demo Labs"
      description: "Demonstration labs for restored historic systems; visitors should check demonstration times in advance."
      source_url: "https://computerhistory.org/exhibits/"
---

# Computer History Museum

## Summary

Computer History Museum in Mountain View is a major technology-history museum with deep computing exhibits, AI-focused displays, historic demonstrations, and hands-on software experiences.

## Visit Facts

- Type: point_of_attraction / museum
- Address: 1401 N. Shoreline Blvd., Mountain View, CA 94043
- Hours: Monday and Tuesday closed; Wednesday through Sunday 10 a.m.-5 p.m.
- Estimated visit duration: 2-3 hours
- Family notes: indoor, stroller-friendly in spirit, but best for children who can engage with technology exhibits; check demo times before anchoring a visit around demonstrations.

## Point Of Attraction Notes

- Key points of interest: Revolution, Chatbots Decoded, Make Software, IBM 1401 and PDP-1 demos.

## Sources

- https://computerhistory.org/hours-admission/
- https://computerhistory.org/visit/
- https://computerhistory.org/exhibits/
- https://computerhistory.org/exhibits/revolution/

## Confidence Notes

- Official pages support the structured facts above.
- Coordinates remain null because they were not independently confirmed from the requested official visitor pages.
