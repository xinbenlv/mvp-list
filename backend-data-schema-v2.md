# Backend Data Schema v2 — Day Composer

> Audience: backend / index-layer engineer.
> Purpose: enumerate every entity the **interaction layer** (Mia) will send to or expect from the **place-intelligence layer** for Day Composer v2.
> Status: **draft for review**. Each schema is marked `[POC required]` (must ship for hackathon demo) or `[Vision]` (design now so we don't paint ourselves into a corner, build later).
> All JSON Schemas are draft 2020-12.

---

## Section 1. Entity Overview

### Relationship diagram

```
                       ┌────────────────────────┐
                       │  TasteSignature        │  extracted from user screenshots
                       │  [POC]                 │  (vibe vector, not place list)
                       └───────────┬────────────┘
                                   │ feeds
                                   ▼
   ┌──────────────────────┐   ┌────────────────────────┐   ┌────────────────────────┐
   │ ExperienceRequest    │──▶│  PlaceQuery            │──▶│  PlaceCandidate[]      │
   │ [POC]                │   │  [POC]                 │   │ [POC]                  │
   │ (interaction→backend)│   │ (structured filter set)│   │ (backend→interaction)  │
   └──────────────────────┘   └────────────────────────┘   └───────────┬────────────┘
                                                                       │
                                                                       │ references
                                                                       ▼
                          ┌────────────────────────────────────────────────────┐
                          │  Place  [POC, v2 upgrade of place.schema.v1]       │
                          │  ┌────────────────────────────────────────────┐   │
                          │  │ + composition fields:                      │   │
                          │  │   vibe_tags, pacing_role, energy_cost,     │   │
                          │  │   chaos_tolerance, social_fit,             │   │
                          │  │   emotional_roles, compatibility_hints,    │   │
                          │  │   logistics (parking, walkin/reservation,  │   │
                          │  │              booking_links)                │   │
                          │  └────────────────────────────────────────────┘   │
                          └────────┬───────────────────────────┬───────────────┘
                                   │ 1:N                       │ 1:N
                                   ▼                           ▼
                       ┌───────────────────────┐   ┌────────────────────────┐
                       │ Event [POC]           │   │ Transition [Vision]    │
                       │ (time-bounded show /  │   │ POC: LLM generates     │
                       │  tour / exhibition    │   │ transition_reason at   │
                       │  attached to a Place) │   │ compose time, inline   │
                       └───────────────────────┘   └────────────────────────┘
                                                              ▲
                                                              │ (precomputed only in Vision)
                                                              │
                                                   ┌──────────┴───────────┐
                                                   │ PlaceCompatibility   │
                                                   │ [Vision]             │
                                                   │ POC: LLM picks combos│
                                                   │ inline at compose    │
                                                   └──────────────────────┘

                       ┌────────────────────────────────────────────────────┐
                       │  TripPlan  [POC]                             │
                       │  ├─ day_theme, mood_tags, emotional_arc            │
                       │  ├─ stops[]  (ordered, ref Place + Event)          │
                       │  ├─ transitions[]                                  │
                       │  ├─ dish_recommendations[]                         │
                       │  └─ adaptive_branches[]                            │
                       └────────────────────────────────────────────────────┘

                       ┌────────────────────────────────────────────────────┐
                       │  TripPlanTemplate  [Vision]                  │
                       │  (creator-authored SKU; anchor_stops + flex_slots) │
                       └────────────────────────────────────────────────────┘

   Controlled vocabularies (enums consumed by all of the above)
   ─────────────────────────────────────────────────────────────
   VibeTag · MoodTag · PacingRole · EmotionalRole · SocialFit
   EnergyLevel · ChaosTolerance · AvoidanceTag
```

### Entity list (one-liners)

| Entity | Status | Purpose |
|---|---|---|
| **Place** (v2) | POC | Upgraded place record — adds composition fields on top of v1 (vibe / pacing / compatibility / logistics). |
| **Event** | POC | Time-bounded activity attached to a Place (standup show, 2nd-Saturday tour, exhibit run). Distinct from always-open places. |
| **Transition** | **Vision** | Directed edge `from → to` with drive minutes + qualitative `transition_reason`. **POC**: LLM generates transition_reason inline at compose time as a TripPlan field, no precomputed entity. |
| **PlaceCompatibility** | **Vision** | First-class A+B combo record. **POC**: LLM picks combinations inline using each Place's `vibe_tags` + `pacing_role`, no precomputed lookup. |
| **TasteSignature** | POC | Vibe vector extracted from user screenshots; *not* a candidate list. |
| **ExperienceRequest** | POC | Full request shape interaction layer sends to backend. |
| **PlaceQuery** | POC | Structured filter/intent payload derived from ExperienceRequest, optimized for backend retrieval. |
| **PlaceCandidate** | POC | Backend response item with `fit_score` + `fit_reason`. |
| **TripPlan** | POC | Final composed plan (theme + arc + cards + branches). |
| **TripPlanTemplate** | Vision | Creator-authored SKU with `anchor_stops` + `flex_slots`. |
| Controlled vocabs (VibeTag etc.) | POC | Enums referenced by Place + Query + Composition. |

---

## Section 2. JSON Schemas

> All schemas live under `$id: https://daycomposer.local/schemas/<name>.schema.json`. Cross-refs use relative `$ref`.
> Conventions: snake_case fields. Required = MUST be present and non-null. Enums are closed unless noted.

---

### 2.0 Controlled vocabularies (enums) `[POC required]`

These are referenced by everything below. **Start with these closed enums**; open them later when we have real coverage gaps.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://daycomposer.local/schemas/vocab.schema.json",
  "title": "Day Composer Controlled Vocabularies",
  "$defs": {
    "VibeTag": {
      "type": "string",
      "enum": [
        "quiet", "lively", "cinematic", "warm", "cool",
        "cultural", "historic", "natural", "urban", "industrial",
        "intimate", "social", "romantic", "family",
        "slow", "fast",
        "polished", "rustic", "gritty",
        "low_stimulation", "high_stimulation",
        "novelty", "familiar",
        "indoor", "outdoor",
        "scenic", "hidden_gem",
        "casual", "upscale"
      ]
    },
    "MoodTag": {
      "type": "string",
      "description": "Higher-level day-mood descriptors (used in TripPlan, not on individual Place).",
      "enum": [
        "reflective", "restorative", "celebratory",
        "lightly_exploratory", "deeply_exploratory",
        "warm", "intimate", "social", "playful",
        "not_rushed", "energizing", "grounding"
      ]
    },
    "PacingRole": {
      "type": "string",
      "description": "Position in a day's emotional arc this place is suited to fill.",
      "enum": ["opening", "breathing", "peak", "recovery", "closing"]
    },
    "EmotionalRole": {
      "type": "string",
      "description": "What emotional intent this place serves (matches ExperienceRequest.primary_mood).",
      "enum": ["restore", "explore", "celebrate", "reconnect", "slow_down", "feel_alive"]
    },
    "SocialFit": {
      "type": "string",
      "enum": [
        "solo", "couple", "family_with_baby", "family_with_kids",
        "friends_small_group", "friends_large_group",
        "parents_visiting", "business_casual"
      ]
    },
    "EnergyLevel": {
      "type": "string",
      "enum": ["low", "medium", "high"]
    },
    "ChaosTolerance": {
      "type": "string",
      "description": "How much sensory/logistical chaos this place imposes on the visitor.",
      "enum": ["low", "medium", "high"]
    },
    "AvoidanceTag": {
      "type": "string",
      "description": "Things a user might want to avoid; same vocabulary place can be tagged with.",
      "enum": [
        "touristy", "overcrowded", "loud", "queued", "rushed",
        "tired_classic", "instagram_bait",
        "hard_parking", "reservation_required", "long_drive",
        "kid_unfriendly", "stroller_unfriendly"
      ]
    },
    "Season": {
      "type": "string",
      "enum": ["spring", "summer", "fall", "winter", "any"]
    },
    "TimeOfDay": {
      "type": "string",
      "enum": ["early_morning", "morning", "midday", "afternoon", "golden_hour", "evening", "late_night"]
    }
  }
}
```

**Example:** `{ "vibe": "quiet", "pacing_role": "opening" }`

---

### 2.1 Place (v2) `[POC required]`

This is the **v2 upgrade** of `place.schema.v1`. It is **additive** — every v1 field is preserved (the friend's existing curated places keep working). New top-level group: `composition` (everything Day Composer needs that v1 doesn't have).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://daycomposer.local/schemas/place.schema.json",
  "title": "Day Composer Place",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "place_id",
    "name",
    "place_type",
    "status",
    "site_ids",
    "location",
    "open_hours",
    "tags",
    "sources",
    "confidence_notes",
    "composition"
  ],
  "properties": {
    "schema_version": { "const": "mvp-list.place.v2" },
    "place_id": {
      "type": "string",
      "description": "Stable internal ID; referenced by PlaceCandidate, TripPlan.stops, Transition.from/to, etc.",
      "pattern": "^[a-z0-9_]+$"
    },
    "name": { "type": ["string", "null"] },
    "place_type": {
      "type": "string",
      "enum": ["restaurant", "point_of_attraction", "venue", "shop", "bar_cafe"],
      "description": "v2 widens v1's two values. `venue` = comedy clubs, theaters, music spots. `bar_cafe` = drinking/coffee. `shop` = browsable retail with vibe."
    },
    "status": {
      "type": "string",
      "enum": ["candidate", "indexed", "needs_disambiguation", "needs_review"]
    },
    "site_ids": { "type": "array", "items": { "$ref": "#/$defs/site_id" } },
    "location": { "$ref": "#/$defs/location" },
    "open_hours": { "$ref": "#/$defs/open_hours" },
    "family_context": { "$ref": "#/$defs/family_context" },
    "tags": { "type": "array", "items": { "type": "string" } },
    "sources": { "type": "array", "items": { "$ref": "#/$defs/source" } },
    "confidence_notes": { "type": "array", "items": { "type": "string" } },

    "restaurant": { "$ref": "#/$defs/restaurant" },
    "point_of_attraction": { "$ref": "#/$defs/point_of_attraction" },

    "composition": { "$ref": "#/$defs/composition" },
    "logistics": { "$ref": "#/$defs/logistics" },
    "events": {
      "type": "array",
      "description": "Time-bounded events attached to this place. Empty for always-open places.",
      "items": { "$ref": "https://daycomposer.local/schemas/event.schema.json" }
    }
  },

  "$defs": {

    "composition": {
      "type": "object",
      "description": "Composition-layer metadata. The core v2 addition.",
      "additionalProperties": false,
      "required": ["vibe_tags", "pacing_roles", "energy_cost", "chaos_tolerance", "social_fit"],
      "properties": {
        "vibe_tags": {
          "type": "array",
          "description": "Weighted vibe signature. 3-8 tags recommended.",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["tag", "weight"],
            "properties": {
              "tag": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/VibeTag" },
              "weight": { "type": "number", "minimum": 0, "maximum": 1 }
            }
          },
          "minItems": 1
        },
        "pacing_roles": {
          "type": "array",
          "description": "Which arc positions this place fits. A place can fit multiple (e.g. ['opening', 'breathing']).",
          "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/PacingRole" },
          "minItems": 1,
          "uniqueItems": true
        },
        "emotional_roles": {
          "type": "array",
          "description": "Which emotional intents this place serves well.",
          "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/EmotionalRole" },
          "uniqueItems": true
        },
        "energy_cost": {
          "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/EnergyLevel",
          "description": "How much physical/mental energy this place drains."
        },
        "chaos_tolerance": {
          "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/ChaosTolerance",
          "description": "How chaotic the experience is — required tolerance from visitor."
        },
        "social_fit": {
          "type": "array",
          "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/SocialFit" },
          "uniqueItems": true,
          "minItems": 1
        },
        "avoidance_tags": {
          "type": "array",
          "description": "Honest negatives: tag this place with what it IS that someone might want to AVOID.",
          "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/AvoidanceTag" },
          "uniqueItems": true
        },
        "compatibility_hints": {
          "type": "object",
          "description": "Heuristic neighbors. The fuller A+B compatibility lives in PlaceCompatibility.",
          "additionalProperties": false,
          "properties": {
            "good_before": { "type": "array", "items": { "type": "string" }, "description": "place_ids that flow nicely INTO this place" },
            "good_after":  { "type": "array", "items": { "type": "string" }, "description": "place_ids this place flows nicely INTO" }
          }
        },
        "best_time_of_day": {
          "type": "array",
          "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/TimeOfDay" },
          "uniqueItems": true
        },
        "best_season": {
          "type": "array",
          "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/Season" },
          "uniqueItems": true
        },
        "narrative_hook": {
          "type": ["string", "null"],
          "description": "1-sentence story-context the creator would say about this place. Powers PlaceCandidate.story_context and TripPlan card copy."
        },
        "hero_image_url": { "type": ["string", "null"], "format": "uri" },
        "vibe_image_urls": {
          "type": "array",
          "description": "Additional images that *show* the vibe (used as visual anchor in the experience card).",
          "items": { "type": "string", "format": "uri" }
        }
      }
    },

    "logistics": {
      "type": "object",
      "additionalProperties": false,
      "required": ["estimated_duration_minutes", "reservation_model"],
      "properties": {
        "estimated_duration_minutes": {
          "type": ["integer", "null"],
          "minimum": 0
        },
        "reservation_model": {
          "type": "string",
          "enum": ["walk_in_only", "reservation_recommended", "reservation_required", "ticketed_event", "free_admission", "mixed"]
        },
        "booking_links": {
          "type": "array",
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["platform", "url"],
            "properties": {
              "platform": {
                "type": "string",
                "enum": ["opentable", "resy", "eventbrite", "spothero", "yelp", "tock", "official_site", "google_maps", "other"]
              },
              "url": { "type": "string", "format": "uri" },
              "purpose": { "type": "string", "enum": ["dining_reservation", "ticket", "parking", "tour_signup", "info"] }
            }
          }
        },
        "parking": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "availability": { "type": "string", "enum": ["easy", "moderate", "hard", "none"] },
            "cost_usd": { "type": ["number", "null"], "minimum": 0, "description": "0 = free. null = unknown." },
            "notes": { "type": ["string", "null"], "description": "e.g. 'lake circle parking', '$8/spot at 350 W Santa Clara'." },
            "pre_book_url": { "type": ["string", "null"], "format": "uri", "description": "e.g. SpotHero link." }
          }
        },
        "ride_share_estimate_usd": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "low":  { "type": "number", "minimum": 0 },
            "high": { "type": "number", "minimum": 0 },
            "from_area": { "type": "string", "description": "e.g. 'downtown San Jose'" }
          }
        },
        "kid_friendly": { "type": ["boolean", "null"] },
        "stroller_friendly": { "type": ["boolean", "null"] },
        "dog_friendly": { "type": ["boolean", "null"] },
        "accessibility_notes": { "type": ["string", "null"] }
      }
    },

    "site_id":     { "type": "object", "additionalProperties": false, "required": ["site", "id", "url", "confidence"],
      "properties": {
        "site": { "type": "string", "enum": ["google_maps", "yelp", "apple_maps", "official_site", "other"] },
        "id":   { "type": ["string", "null"] },
        "url":  { "type": ["string", "null"], "format": "uri" },
        "confidence": { "type": "string", "enum": ["high", "medium", "low"] }
      }
    },
    "location":    { "type": "object", "additionalProperties": false, "required": ["lat", "lon", "normalized_address", "city", "region", "country"],
      "properties": {
        "lat": { "type": ["number", "null"], "minimum": -90, "maximum": 90 },
        "lon": { "type": ["number", "null"], "minimum": -180, "maximum": 180 },
        "normalized_address": { "type": ["string", "null"] },
        "city":    { "type": ["string", "null"] },
        "region":  { "type": ["string", "null"] },
        "country": { "type": ["string", "null"] }
      }
    },
    "open_hours":  { "type": "object", "additionalProperties": false, "required": ["raw", "timezone", "source_url", "retrieved_at"],
      "properties": {
        "raw": { "type": ["string", "object", "array", "null"] },
        "timezone": { "type": ["string", "null"] },
        "source_url": { "type": ["string", "null"], "format": "uri" },
        "retrieved_at": { "type": ["string", "null"], "format": "date" }
      }
    },
    "family_context": { "type": "object", "additionalProperties": false, "required": ["visited", "liked_if_visited", "baby_friendly_notes"],
      "properties": {
        "visited": { "type": ["boolean", "null"] },
        "liked_if_visited": { "type": ["boolean", "null"] },
        "baby_friendly_notes": { "type": ["string", "null"] }
      }
    },
    "source":     { "type": "object", "additionalProperties": false, "required": ["url", "title", "retrieved_at", "used_for"],
      "properties": {
        "url":   { "type": "string", "format": "uri" },
        "title": { "type": ["string", "null"] },
        "retrieved_at": { "type": "string", "format": "date" },
        "used_for": {
          "type": "array",
          "items": { "type": "string",
            "enum": ["identity", "address", "hours", "rating", "price", "dishes", "attractions", "vibe", "parking", "booking", "other"] },
          "minItems": 1, "uniqueItems": true
        }
      }
    },
    "restaurant": {
      "type": "object", "additionalProperties": false,
      "required": ["cuisine_type", "ratings", "top_dishes", "price_range", "vibe"],
      "properties": {
        "cuisine_type": { "type": "array", "items": { "type": "string" } },
        "ratings":      { "type": "array", "items": { "$ref": "#/$defs/rating" } },
        "top_dishes":   { "type": "array", "items": { "$ref": "#/$defs/top_dish" } },
        "price_range":  { "$ref": "#/$defs/price_range" },
        "vibe":         { "type": ["string", "null"], "description": "Free-text legacy field from v1. Prefer composition.vibe_tags for new records." },
        "menu_url":     { "type": ["string", "null"], "format": "uri" },
        "menu_numbered": {
          "type": ["boolean", "null"],
          "description": "True if menu uses numbered items (e.g. Dong Que: '15 香松腊肠锅巴饭'). Enables clean dish_recommendations rendering."
        }
      }
    },
    "rating":     { "type": "object", "additionalProperties": false, "required": ["site", "rating", "review_count", "source_url", "retrieved_at"],
      "properties": {
        "site": { "type": "string", "enum": ["google_maps", "yelp", "apple_maps", "michelin", "other"] },
        "rating":       { "type": ["number", "string", "null"] },
        "review_count": { "type": ["integer", "null"], "minimum": 0 },
        "source_url":   { "type": "string", "format": "uri" },
        "retrieved_at": { "type": "string", "format": "date" }
      }
    },
    "top_dish": {
      "type": "object", "additionalProperties": false,
      "required": ["name", "description", "source_url"],
      "properties": {
        "name": { "type": "string" },
        "menu_number":  { "type": ["string", "null"], "description": "Optional menu number for ordering, e.g. '15', '103', '88'." },
        "description":  { "type": ["string", "null"] },
        "source_url":   { "type": ["string", "null"], "format": "uri" },
        "dish_role":    { "type": "string", "enum": ["appetizer", "small_plate", "main", "side", "rice_noodle", "dessert", "drink", "signature"], "description": "Used by composition layer to construct ordering_logic." },
        "spice_level":  { "type": ["string", "null"], "enum": ["none", "mild", "medium", "hot", "extra_hot", null] },
        "kid_friendly": { "type": ["boolean", "null"] }
      }
    },
    "price_range": { "type": "object", "additionalProperties": false, "required": ["symbol", "text", "source_url"],
      "properties": {
        "symbol": { "type": ["string", "null"], "enum": ["$", "$$", "$$$", "$$$$", null] },
        "text":   { "type": ["string", "null"] },
        "source_url": { "type": ["string", "null"], "format": "uri" }
      }
    },
    "point_of_attraction": { "type": "object", "additionalProperties": false,
      "required": ["attractions", "estimated_visit_duration", "category"],
      "properties": {
        "attractions": { "type": "array", "items": { "$ref": "#/$defs/attraction" } },
        "estimated_visit_duration": { "type": ["string", "null"] },
        "category": { "type": ["string", "null"],
          "enum": ["museum", "park", "national_park", "landmark", "historic_site", "beach", "garden", "trail", "lake", "viewpoint", "other", null] }
      }
    },
    "attraction": { "type": "object", "additionalProperties": false,
      "required": ["name", "description", "source_url"],
      "properties": {
        "name": { "type": "string" },
        "description": { "type": "string" },
        "source_url": { "type": ["string", "null"], "format": "uri" }
      }
    }
  },

  "allOf": [
    { "if": { "properties": { "place_type": { "const": "restaurant" } }, "required": ["place_type"] },
      "then": { "required": ["restaurant"] } },
    { "if": { "properties": { "place_type": { "const": "point_of_attraction" } }, "required": ["place_type"] },
      "then": { "required": ["point_of_attraction"] } }
  ]
}
```

**Example (abridged):**
```json
{
  "schema_version": "mvp-list.place.v2",
  "place_id": "alviso_adobe",
  "name": "Alviso Adobe Park",
  "place_type": "point_of_attraction",
  "status": "indexed",
  "location": { "lat": 37.434, "lon": -121.890, "city": "Milpitas", "region": "CA", "country": "US", "normalized_address": "..." },
  "open_hours": { "raw": "Saturday tour 14:30, 2nd Sat of month", "timezone": "America/Los_Angeles", "source_url": null, "retrieved_at": "2026-01-05" },
  "composition": {
    "vibe_tags": [
      { "tag": "quiet", "weight": 0.9 },
      { "tag": "historic", "weight": 0.95 },
      { "tag": "cultural", "weight": 0.8 },
      { "tag": "low_stimulation", "weight": 0.85 }
    ],
    "pacing_roles": ["opening", "breathing"],
    "emotional_roles": ["restore", "slow_down"],
    "energy_cost": "low",
    "chaos_tolerance": "low",
    "social_fit": ["family_with_baby", "couple", "solo"],
    "avoidance_tags": [],
    "best_time_of_day": ["afternoon"],
    "narrative_hook": "19th-century adobe with quiet Bay Area history — perfect indoor cultural opening before outdoor breathing."
  },
  "logistics": {
    "estimated_duration_minutes": 45,
    "reservation_model": "free_admission",
    "parking": { "availability": "easy", "cost_usd": 0 },
    "kid_friendly": true,
    "stroller_friendly": true
  },
  "events": [
    { "event_id": "alviso_adobe_2nd_sat_tour", "title": "2nd-Saturday docent tour", "starts_at": "2026-01-10T14:30:00-08:00", "duration_minutes": 60 }
  ],
  "point_of_attraction": { "attractions": [...], "category": "historic_site", "estimated_visit_duration": "45-60min" },
  "site_ids": [...], "tags": [...], "sources": [...], "confidence_notes": []
}
```

---

### 2.2 Event `[POC required]`

Time-bounded activities — Spaced Out comedy, Alviso 2nd-Sat tour, a temporary exhibition. **Always attached to a Place** (1:N from Place).

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://daycomposer.local/schemas/event.schema.json",
  "title": "Event",
  "type": "object",
  "additionalProperties": false,
  "required": ["event_id", "place_id", "title", "starts_at", "duration_minutes", "event_type"],
  "properties": {
    "event_id": { "type": "string", "pattern": "^[a-z0-9_]+$" },
    "place_id": { "type": "string", "description": "FK → Place.place_id (the venue)." },
    "title":    { "type": "string" },
    "event_type": {
      "type": "string",
      "enum": ["comedy_show", "concert", "tour", "exhibition", "workshop", "tasting", "screening", "performance", "other"]
    },
    "starts_at": { "type": "string", "format": "date-time" },
    "duration_minutes": { "type": "integer", "minimum": 0 },
    "recurrence": {
      "type": ["string", "null"],
      "description": "Human-readable recurrence, e.g. '2nd Saturday of month'. Leave null for one-off."
    },
    "price": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "amount_usd": { "type": ["number", "null"], "minimum": 0 },
        "per": { "type": "string", "enum": ["person", "group", "vehicle"], "default": "person" },
        "is_free": { "type": "boolean", "default": false }
      }
    },
    "booking_url":      { "type": ["string", "null"], "format": "uri" },
    "booking_platform": { "type": ["string", "null"], "enum": ["eventbrite", "ticketmaster", "official_site", "yelp", "other", null] },
    "age_restriction": { "type": ["string", "null"], "description": "e.g. '18+', 'all ages'." },
    "notes": { "type": ["string", "null"] }
  }
}
```

**Example:**
```json
{
  "event_id": "spaced_out_2026_01_10",
  "place_id": "spaced_out_san_jose",
  "title": "Spaced Out standup comedy",
  "event_type": "comedy_show",
  "starts_at": "2026-01-10T20:00:00-08:00",
  "duration_minutes": 90,
  "price": { "amount_usd": 12.99, "per": "person", "is_free": false },
  "booking_url": "https://eventbrite.com/...",
  "booking_platform": "eventbrite"
}
```

---

### 2.3 Transition `[Vision]` (POC: inline in TripPlan, no entity)

Directed edge between two places.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://daycomposer.local/schemas/transition.schema.json",
  "title": "Transition",
  "type": "object",
  "additionalProperties": false,
  "required": ["from_place_id", "to_place_id", "drive_minutes", "transition_reason"],
  "properties": {
    "from_place_id": { "type": "string" },
    "to_place_id":   { "type": "string" },
    "drive_minutes": { "type": "integer", "minimum": 0 },
    "walk_minutes":  { "type": ["integer", "null"], "minimum": 0 },
    "transit_minutes": { "type": ["integer", "null"], "minimum": 0 },
    "transition_reason": {
      "type": "string",
      "description": "1-line qualitative explanation, e.g. 'indoor history → outdoor nature reset'."
    },
    "arc_shift": {
      "type": ["string", "null"],
      "description": "Optional structured arc move, e.g. 'opening→breathing'.",
      "pattern": "^(opening|breathing|peak|recovery|closing)→(opening|breathing|peak|recovery|closing)$"
    },
    "energy_delta": {
      "type": ["string", "null"],
      "enum": ["down", "flat", "up", null]
    }
  }
}
```

**Example:**
```json
{
  "from_place_id": "alviso_adobe",
  "to_place_id": "sandy_wool_lake",
  "drive_minutes": 8,
  "transition_reason": "indoor history → outdoor nature reset",
  "arc_shift": "opening→breathing",
  "energy_delta": "flat"
}
```

---

### 2.4 PlaceCompatibility `[Vision]` (POC: LLM picks combos inline, no entity)

First-class A+B = vibe-outcome record. For POC, populate a handful by hand to demo the concept; later the index learns these.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://daycomposer.local/schemas/place_compatibility.schema.json",
  "title": "PlaceCompatibility",
  "type": "object",
  "additionalProperties": false,
  "required": ["pair", "combo_vibe", "score"],
  "properties": {
    "pair": {
      "type": "array",
      "minItems": 2, "maxItems": 2,
      "items": { "type": "string", "description": "place_id" },
      "description": "ORDERED pair [A, B] meaning A → B."
    },
    "combo_vibe": {
      "type": "string",
      "description": "1-line vibe outcome, e.g. 'calm reflective', 'appetite reopening', 'socially lighthearted'."
    },
    "score": { "type": "number", "minimum": 0, "maximum": 1, "description": "Compatibility confidence." },
    "valid_arc_roles": {
      "type": "array",
      "description": "Which arc-role pairings this combo supports.",
      "items": {
        "type": "string",
        "pattern": "^(opening|breathing|peak|recovery|closing)→(opening|breathing|peak|recovery|closing)$"
      }
    },
    "rationale": { "type": ["string", "null"] },
    "source": {
      "type": "string",
      "enum": ["hand_curated", "creator_authored", "learned_from_compositions"],
      "default": "hand_curated"
    }
  }
}
```

**Example:**
```json
{
  "pair": ["sandy_wool_lake", "dong_que_restaurant"],
  "combo_vibe": "appetite reopening",
  "score": 0.82,
  "valid_arc_roles": ["breathing→peak"],
  "rationale": "Light hike + bird-watching builds hunger and grounding for boisterous numbered-menu dinner.",
  "source": "hand_curated"
}
```

---

### 2.5 TasteSignature `[POC required]`

The vibe vector extracted from the user's screenshots. **Not** a candidate list — that's the whole insight.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://daycomposer.local/schemas/taste_signature.schema.json",
  "title": "TasteSignature",
  "type": "object",
  "additionalProperties": false,
  "required": ["vibe_weights", "sample_count"],
  "properties": {
    "signature_id": { "type": ["string", "null"], "description": "Optional cache key for re-use within a session." },
    "vibe_weights": {
      "type": "array",
      "description": "Weighted vibe tags inferred from all uploaded samples.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["tag", "weight"],
        "properties": {
          "tag": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/VibeTag" },
          "weight": { "type": "number", "minimum": 0, "maximum": 1 }
        }
      },
      "minItems": 1
    },
    "liked_examples": {
      "type": "array",
      "description": "Short descriptions of the original samples — used by LLM for prompt grounding and by why_fits_today copy.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["description"],
        "properties": {
          "description":  { "type": "string", "description": "e.g. 'Tokyo jazz bar', 'quiet tea house in Kyoto'." },
          "image_url":    { "type": ["string", "null"], "format": "uri" },
          "extracted_vibe_tags": {
            "type": "array",
            "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/VibeTag" }
          },
          "why_user_liked": { "type": ["string", "null"], "description": "LLM-inferred or user-confirmed reason." }
        }
      }
    },
    "sample_count": { "type": "integer", "minimum": 1 },
    "avoidance_signals": {
      "type": "array",
      "description": "Vibe tags that appeared in samples user explicitly DIS-liked (or that LLM inferred as negative).",
      "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/AvoidanceTag" }
    },
    "confidence": { "type": "number", "minimum": 0, "maximum": 1, "description": "Overall extraction confidence." }
  }
}
```

**Example:**
```json
{
  "vibe_weights": [
    { "tag": "quiet",    "weight": 0.9 },
    { "tag": "intimate", "weight": 0.7 },
    { "tag": "warm",     "weight": 0.7 },
    { "tag": "low_stimulation", "weight": 0.8 }
  ],
  "liked_examples": [
    { "description": "Tokyo jazz bar", "extracted_vibe_tags": ["quiet", "intimate", "warm"], "why_user_liked": "low light, no crowd noise, attentive bartender" }
  ],
  "sample_count": 5,
  "avoidance_signals": ["touristy", "loud"],
  "confidence": 0.78
}
```

---

### 2.6 ExperienceRequest `[POC required]`

The full request shape from interaction layer → backend.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://daycomposer.local/schemas/experience_request.schema.json",
  "title": "ExperienceRequest",
  "type": "object",
  "additionalProperties": false,
  "required": ["trip_context", "experience_intent", "constraints"],
  "properties": {
    "request_id": { "type": ["string", "null"] },
    "trip_context": {
      "type": "object",
      "additionalProperties": false,
      "required": ["date", "time_window", "start_location", "companions", "transport"],
      "properties": {
        "date":           { "type": "string", "format": "date" },
        "time_window":    { "type": "string", "description": "e.g. '14:00-22:00'", "pattern": "^\\d{2}:\\d{2}-\\d{2}:\\d{2}$" },
        "start_location": { "type": "string", "description": "Free-form city/neighborhood, e.g. 'Sunnyvale'." },
        "companions":     {
          "type": "array",
          "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/SocialFit" },
          "minItems": 1
        },
        "transport": { "type": "string", "enum": ["car", "rideshare", "transit", "walk_bike", "mixed"] }
      }
    },
    "experience_intent": {
      "type": "object",
      "additionalProperties": false,
      "required": ["primary_mood", "desired_vibe", "avoid"],
      "properties": {
        "primary_mood": {
          "type": "array",
          "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/EmotionalRole" },
          "minItems": 1
        },
        "desired_vibe": {
          "type": "array",
          "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/VibeTag" }
        },
        "avoid": {
          "type": "array",
          "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/AvoidanceTag" }
        }
      }
    },
    "constraints": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "max_drive_minutes":         { "type": ["integer", "null"], "minimum": 0 },
        "max_drive_minutes_per_leg": { "type": ["integer", "null"], "minimum": 0 },
        "kid_friendly":     { "type": ["boolean", "null"] },
        "stroller_friendly":{ "type": ["boolean", "null"] },
        "needs_parking":    { "type": ["boolean", "null"] },
        "budget": {
          "type": ["string", "null"],
          "enum": ["tight", "moderate", "flexible", "splurge", null]
        },
        "energy_level":  { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/EnergyLevel" },
        "chaos_tolerance": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/ChaosTolerance" },
        "stop_count_target": { "type": ["integer", "null"], "minimum": 2, "maximum": 8, "default": 4 }
      }
    },
    "taste_context": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "taste_signature": { "$ref": "https://daycomposer.local/schemas/taste_signature.schema.json" },
        "food_preferences": { "type": "array", "items": { "type": "string" } },
        "novelty_level":   { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/EnergyLevel" }
      }
    }
  }
}
```

---

### 2.7 PlaceQuery `[POC required]`

Lower-level retrieval payload. The interaction layer may send this directly when it already knows what role-slot it's filling (e.g. "give me a 'lively' dinner candidate after place X"). For POC the backend can also derive this internally from `ExperienceRequest`.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://daycomposer.local/schemas/place_query.schema.json",
  "title": "PlaceQuery",
  "type": "object",
  "additionalProperties": false,
  "required": ["pacing_role"],
  "properties": {
    "pacing_role":     { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/PacingRole" },
    "desired_vibe":    {
      "type": "array",
      "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/VibeTag" }
    },
    "avoid":           {
      "type": "array",
      "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/AvoidanceTag" }
    },
    "social_fit":      { "type": "array", "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/SocialFit" } },
    "energy_cost_max": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/EnergyLevel" },
    "chaos_tolerance_max": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/ChaosTolerance" },
    "place_type_in":   { "type": "array", "items": { "type": "string", "enum": ["restaurant", "point_of_attraction", "venue", "shop", "bar_cafe"] } },
    "near_place_id":   { "type": ["string", "null"], "description": "Restrict to candidates that have a known good Transition from this place." },
    "max_drive_minutes_from_anchor": { "type": ["integer", "null"], "minimum": 0 },
    "time_window":     { "type": ["string", "null"], "description": "Filter on open_hours/event availability." },
    "exclude_place_ids": { "type": "array", "items": { "type": "string" }, "description": "Already-picked stops." },
    "top_k": { "type": "integer", "minimum": 1, "default": 10 }
  }
}
```

---

### 2.8 PlaceCandidate `[POC required]`

Backend response items. Always returned as a ranked list, paired with a `possible_transitions` block.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://daycomposer.local/schemas/place_candidate_response.schema.json",
  "title": "PlaceCandidateResponse",
  "type": "object",
  "additionalProperties": false,
  "required": ["candidates"],
  "properties": {
    "candidates": {
      "type": "array",
      "items": { "$ref": "#/$defs/PlaceCandidate" }
    },
    "possible_transitions": {
      "type": "array",
      "items": { "$ref": "https://daycomposer.local/schemas/transition.schema.json" }
    }
  },
  "$defs": {
    "PlaceCandidate": {
      "type": "object",
      "additionalProperties": false,
      "required": ["place_id", "name", "fit_score", "fit_reason"],
      "properties": {
        "place_id": { "type": "string" },
        "name":     { "type": "string" },
        "place_type": { "type": "string" },
        "pacing_role_suggested": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/PacingRole" },
        "fit_score":  { "type": "number", "minimum": 0, "maximum": 1 },
        "fit_reason": {
          "type": "string",
          "description": "Short reason citing intent + taste, e.g. 'matches cultural + light exploration intent, low chaos for baby'."
        },
        "matched_vibe_tags": {
          "type": "array",
          "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/VibeTag" }
        },
        "story_context": { "type": ["string", "null"], "description": "Mirrors Place.composition.narrative_hook for convenience." },
        "hero_image_url": { "type": ["string", "null"], "format": "uri" },
        "logistics_summary": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "parking":  { "type": ["string", "null"], "enum": ["easy", "moderate", "hard", "none", null] },
            "kid_friendly": { "type": ["boolean", "null"] },
            "estimated_duration_minutes": { "type": ["integer", "null"], "minimum": 0 },
            "reservation_model": { "type": ["string", "null"] }
          }
        },
        "booking_url": { "type": ["string", "null"], "format": "uri" },
        "event_id":    { "type": ["string", "null"], "description": "If the candidate is a time-bounded event, the specific Event id." }
      }
    }
  }
}
```

**Example:**
```json
{
  "candidates": [
    {
      "place_id": "alviso_adobe",
      "name": "Alviso Adobe",
      "pacing_role_suggested": "opening",
      "fit_score": 0.87,
      "fit_reason": "matches restore + lightly_exploratory; low chaos suitable for baby; cultural-quiet vibe matches taste signature.",
      "matched_vibe_tags": ["quiet", "historic", "low_stimulation"],
      "story_context": "19th-century adobe with Bay Area history",
      "logistics_summary": { "parking": "easy", "kid_friendly": true, "estimated_duration_minutes": 45, "reservation_model": "free_admission" }
    }
  ],
  "possible_transitions": [
    { "from_place_id": "alviso_adobe", "to_place_id": "sandy_wool_lake", "drive_minutes": 8, "transition_reason": "indoor history → outdoor breathing", "arc_shift": "opening→breathing" }
  ]
}
```

---

### 2.9 TripPlan `[POC required]`

The final composed plan — what the UI renders as the one-page output.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://daycomposer.local/schemas/day_composition.schema.json",
  "title": "TripPlan",
  "type": "object",
  "additionalProperties": false,
  "required": ["day_theme", "mood_tags", "emotional_arc", "stops"],
  "properties": {
    "composition_id": { "type": ["string", "null"] },
    "day_theme": { "type": "string", "description": "Narrative anchor, e.g. '旧湾区与恢复感的一天'." },
    "mood_tags": {
      "type": "array",
      "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/MoodTag" },
      "minItems": 1
    },
    "emotional_arc": {
      "type": "array",
      "description": "Ordered arc beats. Each beat maps to a stop (by index).",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["label", "pacing_role"],
        "properties": {
          "label":        { "type": "string", "description": "e.g. 'slow opening', 'lively dinner'." },
          "pacing_role":  { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/PacingRole" },
          "vibe_curve_value": { "type": ["number", "null"], "minimum": 0, "maximum": 1, "description": "0=low energy/intimate, 1=high energy/social. Powers the visualization curve." }
        }
      }
    },
    "stops": {
      "type": "array",
      "minItems": 1,
      "items": { "$ref": "#/$defs/Stop" }
    },
    "transitions": {
      "type": "array",
      "description": "Same length as stops[] - 1.",
      "items": { "$ref": "https://daycomposer.local/schemas/transition.schema.json" }
    },
    "dish_recommendations": {
      "type": "array",
      "description": "One entry per restaurant stop with non-empty recommendations.",
      "items": { "$ref": "#/$defs/DishRecommendation" }
    },
    "adaptive_branches": {
      "type": "array",
      "items": { "$ref": "#/$defs/AdaptiveBranch" }
    },
    "source_template_id": {
      "type": ["string", "null"],
      "description": "If composed via fast-path from a TripPlanTemplate, the source SKU id."
    }
  },
  "$defs": {
    "Stop": {
      "type": "object",
      "additionalProperties": false,
      "required": ["place_id", "time", "why_fits_today"],
      "properties": {
        "place_id": { "type": "string" },
        "event_id": { "type": ["string", "null"], "description": "If this stop is a specific Event, not just the venue." },
        "time":     { "type": "string", "pattern": "^\\d{2}:\\d{2}$", "description": "Local start time HH:MM." },
        "duration_minutes": { "type": ["integer", "null"], "minimum": 0 },
        "title":           { "type": ["string", "null"], "description": "Card headline, e.g. 'A quiet historical opening'." },
        "why_fits_today":  { "type": "string", "description": "Reason copy referencing taste + mood. Required and must be specific." },
        "transition_to_next": { "type": ["string", "null"], "description": "1-line transition note, e.g. 'indoor narrative → outdoor breathing'." },
        "optional_tip":    { "type": ["string", "null"] },
        "image_url":       { "type": ["string", "null"], "format": "uri" },
        "logistics_inline":{
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "drive_minutes_from_prev": { "type": ["integer", "null"], "minimum": 0 },
            "parking":      { "type": ["string", "null"], "enum": ["easy", "moderate", "hard", "none", null] },
            "kid_friendly": { "type": ["boolean", "null"] }
          }
        }
      }
    },
    "DishRecommendation": {
      "type": "object",
      "additionalProperties": false,
      "required": ["place_id", "dishes", "ordering_logic"],
      "properties": {
        "place_id": { "type": "string" },
        "dishes": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "additionalProperties": false,
            "required": ["name"],
            "properties": {
              "name":         { "type": "string" },
              "menu_number":  { "type": ["string", "null"] },
              "dish_role":    { "type": ["string", "null"], "enum": ["appetizer", "small_plate", "main", "side", "rice_noodle", "dessert", "drink", "signature", null] },
              "note":         { "type": ["string", "null"], "description": "Why this dish, ordering hint." }
            }
          }
        },
        "ordering_logic": {
          "type": "string",
          "description": "1-2 sentence ordering narrative, e.g. '先点 15 + 88 开胃,再加 92 做主菜,103 收尾'."
        }
      }
    },
    "AdaptiveBranch": {
      "type": "object",
      "additionalProperties": false,
      "required": ["condition", "alternative"],
      "properties": {
        "branch_at_stop_index": { "type": ["integer", "null"], "minimum": 0, "description": "Which stop this branch forks from (0-indexed). null = global." },
        "condition":   { "type": "string", "description": "Trigger, e.g. 'if baby is fussy', 'if energy higher than expected'." },
        "alternative": { "type": "string", "description": "What to do instead, e.g. 'skip comedy, go to nearby dessert (place_id: ...)'." },
        "alternative_place_id": { "type": ["string", "null"] },
        "alternative_event_id": { "type": ["string", "null"] }
      }
    }
  }
}
```

**Example (abridged, mirroring the sample itinerary):**
```json
{
  "day_theme": "旧湾区与恢复感的一天",
  "mood_tags": ["reflective", "warm", "lightly_exploratory", "not_rushed"],
  "emotional_arc": [
    { "label": "slow opening",  "pacing_role": "opening",   "vibe_curve_value": 0.2 },
    { "label": "breathing",     "pacing_role": "breathing", "vibe_curve_value": 0.3 },
    { "label": "lively dinner", "pacing_role": "peak",      "vibe_curve_value": 0.85 },
    { "label": "light closing", "pacing_role": "closing",   "vibe_curve_value": 0.55 }
  ],
  "stops": [
    { "place_id": "alviso_adobe", "event_id": "alviso_adobe_2nd_sat_tour", "time": "14:30",
      "title": "A quiet historical opening",
      "why_fits_today": "你今天想 restore，又不想完全静止；adobe 比 museum 轻盈，宝宝也好带。",
      "transition_to_next": "indoor narrative → outdoor breathing" },
    { "place_id": "sandy_wool_lake", "time": "15:00",
      "title": "Lakeside breathing",
      "why_fits_today": "8 分钟 drive，circle parking 好停；湖边走走、看鸟，正好把上一段消化。",
      "transition_to_next": "outdoor reset → appetite-opening dinner" },
    { "place_id": "dong_que_restaurant", "time": "18:30",
      "title": "Lively neighborhood dinner",
      "why_fits_today": "你说不想 touristy；这家 walk-in only、本地客为主、菜有编号好点。",
      "transition_to_next": "warm fullness → light social closer",
      "optional_tip": "外侧 parking，提早 10 分钟到避免 wait list 高峰" },
    { "place_id": "spaced_out_san_jose", "event_id": "spaced_out_2026_01_10", "time": "20:00",
      "title": "Light closing — local comedy",
      "why_fits_today": "downtown 一点烟火气但不通宵；$13/人，散场你们还有体力开回家。",
      "optional_tip": "SpotHero 提前订 $8/spot at 350 W Santa Clara" }
  ],
  "transitions": [
    { "from_place_id": "alviso_adobe",        "to_place_id": "sandy_wool_lake",     "drive_minutes": 8,  "transition_reason": "indoor history → outdoor breathing",  "arc_shift": "opening→breathing" },
    { "from_place_id": "sandy_wool_lake",     "to_place_id": "dong_que_restaurant", "drive_minutes": 25, "transition_reason": "nature reset → lively dinner",         "arc_shift": "breathing→peak" },
    { "from_place_id": "dong_que_restaurant", "to_place_id": "spaced_out_san_jose", "drive_minutes": 10, "transition_reason": "warm fullness → social light closing", "arc_shift": "peak→closing" }
  ],
  "dish_recommendations": [
    {
      "place_id": "dong_que_restaurant",
      "dishes": [
        { "name": "香松腊肠锅巴饭", "menu_number": "15",  "dish_role": "rice_noodle", "note": "签到菜，先点" },
        { "name": "铁板螺丝",       "menu_number": "103", "dish_role": "small_plate", "note": "热炒收尾" },
        { "name": "烤生蚝",         "menu_number": "88",  "dish_role": "appetizer",   "note": "开胃" },
        { "name": "鱼籽扇贝",       "menu_number": "92",  "dish_role": "signature",   "note": "主菜" }
      ],
      "ordering_logic": "先 88 + 15 开胃打底，再上 92 做主菜，最后 103 热炒收尾。两个人吃刚好不剩。"
    }
  ],
  "adaptive_branches": [
    { "branch_at_stop_index": 3, "condition": "宝宝困了/状态不好", "alternative": "skip comedy, 去附近 dessert place", "alternative_place_id": "san_jose_dessert_alt" },
    { "branch_at_stop_index": 3, "condition": "如果 energy 更高",   "alternative": "加 downtown wine bar",          "alternative_place_id": "san_jose_wine_bar_alt" }
  ]
}
```

---

### 2.10 TripPlanTemplate `[Vision]`

Creator-authored SKU. Design it now so v2 Place schema isn't blind to template needs.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://daycomposer.local/schemas/day_composition_template.schema.json",
  "title": "TripPlanTemplate",
  "type": "object",
  "additionalProperties": false,
  "required": ["template_id", "author", "day_theme", "mood_tags", "emotional_arc", "anchor_stops"],
  "properties": {
    "template_id": { "type": "string", "pattern": "^sku_[a-z0-9_]+$" },
    "author": {
      "type": "object",
      "additionalProperties": false,
      "required": ["creator_id", "display_name"],
      "properties": {
        "creator_id":   { "type": "string" },
        "display_name": { "type": "string" }
      }
    },
    "day_theme": { "type": "string" },
    "mood_tags": { "type": "array", "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/MoodTag" } },
    "emotional_arc": {
      "type": "array",
      "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/PacingRole" }
    },
    "social_fit": { "type": "array", "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/SocialFit" } },
    "season_fit": { "type": "array", "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/Season" } },
    "anchor_stops": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["place_id", "pacing_role", "fixed"],
        "properties": {
          "place_id":    { "type": "string" },
          "pacing_role": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/PacingRole" },
          "fixed":       { "type": "boolean", "description": "If true, AI cannot swap this stop." }
        }
      }
    },
    "flex_slots": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["slot", "role"],
        "properties": {
          "slot": { "type": "string", "description": "Semantic slot, e.g. 'dinner', 'closing'." },
          "role": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/PacingRole" },
          "tag_constraints": { "type": "array", "items": { "$ref": "https://daycomposer.local/schemas/vocab.schema.json#/$defs/VibeTag" } },
          "alternatives":    { "type": "array", "items": { "type": "string" }, "description": "Suggested place_type or VibeTag alternatives the AI may swap in." }
        }
      }
    },
    "private_tips": { "type": "array", "items": { "type": "string" } },
    "narrative":    { "type": ["string", "null"], "description": "Creator's longform voice-of-author opening." }
  }
}
```

---

## Section 3. v1 → v2 Diff for `place.schema.json`

| Field | v1 | v2 | Rationale |
|---|---|---|---|
| `schema_version` | `mvp-list.place.v1` | `mvp-list.place.v2` | Version bump. |
| `place_id` | (missing — `name` was effectively the key) | **Required string, snake_case** | Other entities (Transition, Composition.stops, PlaceCompatibility) need a stable FK. |
| `place_type` enum | `restaurant`, `point_of_attraction` | + `venue`, `shop`, `bar_cafe` | Comedy clubs, wine bars, dessert shops are first-class in sample itinerary. |
| `composition` | — | **New required object** | Holds all v2 composition fields. Group keeps diff clean for friend. |
| `composition.vibe_tags` | — | Weighted list of VibeTag | Core to vibe matching insight. **Weighted, not flat** (see open questions). |
| `composition.pacing_roles` | — | List of PacingRole | A place can play multiple arc roles. |
| `composition.emotional_roles` | — | List of EmotionalRole | Maps to ExperienceRequest.primary_mood. |
| `composition.energy_cost` | — | low/medium/high | For energy-budget matching. |
| `composition.chaos_tolerance` | — | low/medium/high | Avoidance is informative — chaos is the avoidance lever the user named. |
| `composition.social_fit` | partially via `family_context.baby_friendly_notes` | Required list of SocialFit enum | Make it queryable, not narrative. |
| `composition.avoidance_tags` | — | List of AvoidanceTag | Honest negatives; lets the index match `avoid` queries. |
| `composition.compatibility_hints` | — | `{ good_before, good_after }` | Cheap heuristic neighbors; full A+B lives in PlaceCompatibility. |
| `composition.best_time_of_day`, `best_season` | — | enums | Sample itinerary's "sunset 前到湖边" was lost otherwise. |
| `composition.narrative_hook` | — | string | Powers PlaceCandidate.story_context and card copy. |
| `composition.hero_image_url`, `vibe_image_urls` | — | URIs | One-page demands big imagery. |
| `logistics` | — | **New object** | Pulls scattered v1 affordances (kid_friendly, parking) into one place + adds new ones. |
| `logistics.estimated_duration_minutes` | was string `estimated_visit_duration` on POA only | integer minutes, top-level | Used by composition to time-budget the day. |
| `logistics.reservation_model` | — | enum incl. `walk_in_only` | Sample itinerary's Dong Que "walk-in only". |
| `logistics.booking_links[]` | partial in `site_ids` | structured list with `platform` + `purpose` | Eventbrite, SpotHero, OpenTable each matter. |
| `logistics.parking` | — | `{ availability, cost_usd, notes, pre_book_url }` | "$8/spot at 350 W Santa Clara"; SpotHero pre-book. |
| `logistics.ride_share_estimate_usd` | — | object | Sample had "Uber estimate $40-50". |
| `logistics.kid_friendly`, `stroller_friendly`, `dog_friendly` | partial via `family_context` | Top-level booleans | Queryable. Keep `family_context.baby_friendly_notes` as free-text supplement. |
| `events[]` | — | List of Event | Time-bounded activities live here, attached to their venue Place. |
| `restaurant.menu_url`, `menu_numbered` | — | new | Sample's numbered-menu pattern enables clean DishRecommendation rendering. |
| `restaurant.top_dish.menu_number`, `dish_role`, `spice_level`, `kid_friendly` | — | new fields on existing struct | Enables ordering_logic ("先 88 开胃, 再 92 主菜"). |
| `point_of_attraction.category` | enum | + `historic_site`, `lake`, `viewpoint` | Sample needs these. |
| `source.used_for` | + `vibe`, `parking`, `booking` | extended | Tracks new evidence types. |

**Migration**: v1 records are forward-compatible if the friend writes a one-pass enricher that fills `composition` with sensible defaults (empty arrays, `energy_cost: "medium"`, etc.) and synthesizes `place_id` from slug(`name` + city).

---

## Section 4. Open questions for the friend

1. **Vibe tags: weighted vs flat?** I went with **weighted** (`{tag, weight}` pairs) for both `Place.composition.vibe_tags` and `TasteSignature.vibe_weights`, because vibe-matching is fundamentally similarity scoring and a flat list throws away signal. Cost: ~30s more per hand-tagged place. **OK to lock in?** If you want flat for POC speed, propose `weight: number | null` so we can upgrade later.

2. ~~PlaceCompatibility ordering~~ — **moved to Vision; POC does not precompute compatibility. LLM judges A+B inline at compose time using each Place's `vibe_tags` + `pacing_role`.**

3. **`pacing_roles` plural vs singular?** I let a place be in multiple roles (Alviso fits `opening` AND `breathing`). This makes retrieval easier but ranking harder (which role is "best"?). Alternative: single `primary_pacing_role` + `secondary_pacing_roles[]`. **Recommend plural for now; revisit if ranking gets messy.**

4. **Event vs Place separation: do all venues need a Place even if they're event-only?** Spaced Out comedy could be modeled as `place_type: "venue"` with an `events[]` array, or as a standalone Event with embedded location. I went with **Place + nested Events** so transitions and parking attach to the venue, not the show. **Confirm this matches your indexing intuition?**

5. **`PlaceQuery` — does the backend derive it from `ExperienceRequest`, or does interaction layer send both?** I designed it so interaction layer can send one `ExperienceRequest` and get back a full ranked set, OR send N targeted `PlaceQuery`s when it's iteratively building the day. **For POC let's just do `POST /experience` (request → candidates); leave per-slot query for later.** Confirm?

6. **Where does TasteSignature extraction happen?** Interaction layer extracts it from screenshots and embeds in `ExperienceRequest.taste_context.taste_signature`, OR backend exposes `POST /taste/extract` that accepts images and returns signature. **Recommend: extraction lives in interaction layer (it owns the vision LLM); backend just consumes the structured signature.** OK?

7. **Controlled vocab governance — closed or extensible?** I made all enums closed for type safety. If a creator wants a vibe that doesn't exist ("dreamy-shoegaze"), they're stuck. **Recommend: closed for POC; add a process for adding tags in v2.1.** Alternative: allow free-form `custom_tags[]` alongside the closed list.

8. ~~`compatibility_hints` on Place vs full `PlaceCompatibility` records~~ — **POC keeps `compatibility_hints` on Place as creator's "I usually pair this with X" heuristic. Full `PlaceCompatibility` records are Vision.**

---

## Section 5. POC Minimum Viable Backend

What MUST exist for the 90-second demo to land. Everything else is post-POC.

1. **30 hand-curated Bay Area places** conforming to `Place v2`, covering at minimum: 5 historic / cultural; 5 nature / park / lake; 8 restaurants (mix of cuisines, at least 2 walk-in-only, 1 numbered-menu); 4 bars/cafes; 4 venues with events; 4 dessert/light-closing spots.
2. **~15 attached Events** (recurring tours, weekly comedy nights, current exhibitions) so the demo can show a time-bounded stop.
3. **All 30 places hand-tagged** with `composition.vibe_tags` (weighted), `pacing_roles`, `energy_cost`, `chaos_tolerance`, `social_fit`, `avoidance_tags`, `narrative_hook`, `hero_image_url`.
4. **One HTTP endpoint:** `POST /experience` — accepts `ExperienceRequest`, returns `PlaceCandidateResponse` with ranked candidates (ranking can be hand-coded weighted-tag overlap, no embeddings needed for 30 records).
5. **In-memory or single-file JSON store.** No DB. Schema validation via AJV / pydantic.
6. **Static booking links** for any candidate that has one (no real booking integration).

**Out of POC backend** (LLM handles at compose time, no precomputed data):
- ❌ Transition matrix — interaction layer's composer prompts LLM to write `transition_reason` and estimate drive_minutes from addresses
- ❌ PlaceCompatibility records — LLM judges A+B compatibility inline using each place's `vibe_tags` + `pacing_role`

That's it. Marketplace, creator dashboard, real index, embeddings, multi-day, refine deltas — all out of POC scope.
