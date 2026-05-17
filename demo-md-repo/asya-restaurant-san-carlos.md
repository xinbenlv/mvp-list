---
schema_version: mvp-list.place.v1
name: "Asya Restaurant"
place_type: restaurant
status: candidate
site_ids:
  - site: official_site
    id: null
    url: "https://asya-restaurant.com/"
    confidence: high
location:
  lat: null
  lon: null
  normalized_address: null
  city: "San Carlos"
  region: "CA"
  country: "US"
open_hours:
  raw: null
  timezone: "America/Los_Angeles"
  source_url: "https://asya-restaurant.com/"
  retrieved_at: "2026-05-16"
family_context:
  visited: null
  liked_if_visited: null
  baby_friendly_notes: "Itinerary intent is a simple nearby lunch before photos, with lighter Japanese-style food to avoid bloating."
tags:
  - restaurant
  - japanese
  - casual-lunch
  - san-carlos
sources:
  - url: "https://asya-restaurant.com/"
    title: "Asya Restaurant"
    retrieved_at: "2026-05-16"
    used_for:
      - identity
      - dishes
      - other
  - url: "https://asya-restaurant.com/menu/"
    title: "Asya Restaurant Menu"
    retrieved_at: "2026-05-16"
    used_for:
      - dishes
      - price
confidence_notes:
  - "The itinerary links the official Asya menu and describes the lunch as nearby Japanese-style simple food."
  - "Address, hours, ratings, and actual popular-item frequency were not independently confirmed in this run."
  - "Top dishes below are menu-backed candidates, not verified popularity rankings."
restaurant:
  cuisine_type:
    - "Japanese"
  ratings: []
  top_dishes:
    - name: "Sushi"
      description: "Menu-backed Japanese lunch option; exact preparation varies by menu item."
      source_url: "https://asya-restaurant.com/menu/"
    - name: "Sashimi"
      description: "Menu-backed lighter seafood option suitable for a simple lunch before photos."
      source_url: "https://asya-restaurant.com/menu/"
    - name: "Rolls"
      description: "Menu-backed casual Japanese option; use current menu for exact roll names."
      source_url: "https://asya-restaurant.com/menu/"
  price_range:
    symbol: null
    text: "Use current official menu for item-level prices."
    source_url: "https://asya-restaurant.com/menu/"
  vibe: "Casual Japanese-style lunch stop."
---

# Asya Restaurant

## Summary

Asya Restaurant is the itinerary's simple nearby lunch option before the Filoli photo session.

## Visit Facts

- Cuisine: Japanese-style casual lunch
- Menu: https://asya-restaurant.com/menu/
- Itinerary reason: keep lunch simple before afternoon photography

## Restaurant Notes

- Menu-backed candidates: sushi, sashimi, rolls
- Confirm exact address, hours, and current popular items before finalizing the itinerary.

## Sources

- Official site: https://asya-restaurant.com/
- Official menu: https://asya-restaurant.com/menu/

## Confidence Notes

- This is structurally indexed, but key dynamic fields remain incomplete.
