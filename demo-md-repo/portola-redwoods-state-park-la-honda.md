---
schema_version: mvp-list.place.v1
name: "Portola Redwoods State Park"
place_type: point_of_attraction
status: candidate
site_ids:
  - site: google_maps
    id: "0x808fad0ad2546139:0x606d96ef1572f5a2"
    url: "https://www.google.com/maps/place/Portola+Redwoods+State+Park/@37.2621677,-122.6285319,10z/data=!4m10!1m2!2m1!1sNational+Parks!3m6!1s0x808fad0ad2546139:0x606d96ef1572f5a2!8m2!3d37.2621402!4d-122.195833!15sCg5OYXRpb25hbCBQYXJrc1oQIg5uYXRpb25hbCBwYXJrc5IBCnN0YXRlX3BhcmuaAURDaTlEUVVsUlFVTnZaRU5vZEhsalJqbHZUMnRuTkZVelFUVlRSa0Y2VXpOT1NWTnFXakZpYkVKdVpWWk9SRTV1WXhBQuABAPoBBAgAEEw!16zL20vMDY4dncx!5m1!1e2?entry=ttu&g_ep=EgoyMDI2MDUxMy4wIKXMDSoASAFQAw%3D%3D"
    confidence: high
  - site: official_site
    id: null
    url: "https://www.parks.ca.gov/?lang=en&page_id=539"
    confidence: high
location:
  lat: 37.2621402
  lon: -122.195833
  normalized_address: "9000 Portola State Park Road, La Honda, CA 94020"
  city: "La Honda"
  region: "CA"
  country: "US"
open_hours:
  raw:
    day_use: "6:00 AM-sunset"
    visitor_center: "Monday-Sunday 9:00 AM-5:00 PM"
    closure_note: "In severe weather the park might be closed."
  timezone: "America/Los_Angeles"
  source_url: "https://www.parks.ca.gov/?lang=en&page_id=539"
  retrieved_at: "2026-05-16"
family_context:
  visited: null
  liked_if_visited: null
  baby_friendly_notes: "Sequoia Nature Trail is described as an easy family option near the visitor center; longer trails such as Peters Creek are strenuous and not stroller-friendly. Dogs are not allowed on hiking trails except service animals."
tags:
  - point-of-attraction
  - state-park
  - redwoods
  - hiking
  - waterfall
  - family-friendly-option
  - la-honda
sources:
  - url: "https://www.google.com/maps/place/Portola+Redwoods+State+Park/@37.2621677,-122.6285319,10z/data=!4m10!1m2!2m1!1sNational+Parks!3m6!1s0x808fad0ad2546139:0x606d96ef1572f5a2!8m2!3d37.2621402!4d-122.195833!15sCg5OYXRpb25hbCBQYXJrc1oQIg5uYXRpb25hbCBwYXJrc5IBCnN0YXRlX3BhcmuaAURDaTlEUVVsUlFVTnZaRU5vZEhsalJqbHZUMnRuTkZVelFUVlRSa0Y2VXpOT1NWTnFXakZpYkVKdVpWWk9SRTV1WXhBQuABAPoBBAgAEEw!16zL20vMDY4dncx!5m1!1e2?entry=ttu&g_ep=EgoyMDI2MDUxMy4wIKXMDSoASAFQAw%3D%3D"
    title: "Google Maps place URL for Portola Redwoods State Park"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - other
  - url: "https://www.parks.ca.gov/?lang=en&page_id=539"
    title: "Portola Redwoods State Park - California State Parks"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - hours
      - attractions
      - other
  - url: "https://www.parks.ca.gov/pages/539/files/PortolaRedwoodsWeb2016.pdf"
    title: "Portola Redwoods State Park brochure - California State Parks"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - address
      - attractions
      - other
  - url: "https://sempervirens.org/visit/portola-redwoods-state-park/"
    title: "Portola Redwoods State Park - Sempervirens Fund"
    retrieved_at: "2026-05-16"
    used_for:
      - attractions
      - hours
      - other
  - url: "https://openspacetrust.org/hike/portola-redwoods-state-park/"
    title: "Peters Creek Loop Trail - Peninsula Open Space Trust"
    retrieved_at: "2026-05-16"
    used_for:
      - attractions
      - other
confidence_notes:
  - "Google Maps URL provided stable place identity, feature id, and coordinates."
  - "Official California State Parks page and brochure confirmed address, hours, park amenities, trails, and restrictions."
  - "Sempervirens Fund and Peninsula Open Space Trust were used to enrich key points of interest with trail names and visit context."
  - "The Google Maps URL search text says National Parks, but this place is a California state park; `category` is set to `park`."
  - "Seasonal bridge and weather closures can change access; refresh official advisories before visiting."
  - "Written as Markdown into ./.tmp/gbrain; no local gbrain CLI was available to verify query ingestion."
point_of_attraction:
  category: park
  estimated_visit_duration: "1 hour for Sequoia Nature Trail; about 2 hours for Tip Toe Falls; 6-7 hours for Peters Creek Loop; half-day to full-day depending on route."
  attractions:
    - name: "Sequoia Nature Trail"
      description: "Easy interpretive loop near the visitor center along Pescadero Creek; Sempervirens describes it as a family-friendly option with interpretive signs."
      source_url: "https://sempervirens.org/visit/portola-redwoods-state-park/"
    - name: "Tip Toe Falls"
      description: "Small waterfall reached by an easy out-and-back hike via Iverson Trail and Sequoia Nature Trail; Sempervirens describes a 1.6-mile round trip that usually takes about two hours."
      source_url: "https://sempervirens.org/visit/portola-redwoods-state-park/"
    - name: "Peters Creek Trail and old-growth grove"
      description: "Strenuous backcountry redwood hike; California State Parks brochure describes Bear Creek Trail leading to Peters Creek Trail and an ancient old-growth redwood loop, while POST calls Peters Creek Loop an 11.5-mile hike through the third-largest old-growth redwood grove in the Santa Cruz Mountains."
      source_url: "https://openspacetrust.org/hike/portola-redwoods-state-park/"
    - name: "Visitor Center and interpretive displays"
      description: "Accessible visitor center near park headquarters with interpretive and educational displays; the official park page lists visitor center hours as 9 AM-5 PM."
      source_url: "https://www.parks.ca.gov/pages/539/files/PortolaRedwoodsWeb2016.pdf"
    - name: "Slate Creek Trail Camp"
      description: "Backcountry trail camp with six sites available seasonally; useful for turning longer redwood hikes into an overnight trip."
      source_url: "https://www.parks.ca.gov/pages/539/files/PortolaRedwoodsWeb2016.pdf"
---

# Portola Redwoods State Park

## Summary

Portola Redwoods State Park is a 2,800-acre California state park near La Honda with coast redwoods, creeks, waterfalls, camping, and hiking routes ranging from short family-friendly trails to strenuous old-growth redwood loops. The structured fields for search live in the YAML frontmatter; this body is a readable review layer.

## Visit Facts

- Address: 9000 Portola State Park Road, La Honda, CA 94020
- Coordinates: 37.2621402, -122.195833
- Day use hours: 6:00 AM-sunset
- Visitor center: Monday-Sunday 9:00 AM-5:00 PM
- Fee signal: official page lists a vehicle day-use fee
- Current caution: official page notes seasonal creek bridges have been removed and severe weather may close the park

## Point Of Attraction Notes

- Key points of interest: Sequoia Nature Trail, Tip Toe Falls, Peters Creek Trail/Grove, visitor center, Slate Creek Trail Camp
- Family option: Sequoia Nature Trail is the most clearly family-friendly short walk from the sources checked
- Longer adventure: Peters Creek Loop is a full-day, strenuous redwood hike
- Dogs: allowed only in campsites, picnic areas, paved roads, and limited road corridors; not on hiking trails except service animals

## Sources

- Google Maps place URL supplied by user
- California State Parks official page: https://www.parks.ca.gov/?lang=en&page_id=539
- California State Parks brochure: https://www.parks.ca.gov/pages/539/files/PortolaRedwoodsWeb2016.pdf
- Sempervirens Fund: https://sempervirens.org/visit/portola-redwoods-state-park/
- Peninsula Open Space Trust: https://openspacetrust.org/hike/portola-redwoods-state-park/

## Confidence Notes

- High confidence this is Portola Redwoods State Park at 9000 Portola State Park Road, La Honda, CA.
- Attraction enrichment is source-backed and written into `point_of_attraction.attractions` for structured search.
- Hours, fees, bridges, and closures are dynamic and should be refreshed before a visit.
- This record was written into `./.tmp/gbrain`; no local gbrain query tool was available to verify ingestion beyond file existence and schema validation.
