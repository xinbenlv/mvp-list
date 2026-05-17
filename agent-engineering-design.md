# Day Composer — Agent Engineering Design

> **Document purpose**: HOW we build the agent layer. PRD (`prd-v2-day-composer.md`) is WHAT/WHY. Backend schema (`backend-data-schema-v2.md`) defines the data contracts. Read both as prerequisites.
>
> **Scope**: only the agent code that sits between OpenClaw (UI) and G-Brain (data).
>
> **Audience**: implementer (Mia), code reviewer, friend on the backend side.
>
> **v2 update (this version)**: collapsed from 10-pseudo-agents to **2 true agents + ~11 tools**. Rationale in §5.

---

## 1. Goals & Non-Goals

### Goals
- G1. Take a user conversation (screenshots + ≤10 chat turns) and output **2–3 distinct TripPlan proposals** they can compare and pick from.
- G2. Use **the minimum agent count that achieves the quality bar** — start simple, add specialists only when measurably needed (per Anthropic's "Building Effective Agents" guidance).
- G3. Leverage **existing MCPs / CLIs / standards** (Foursquare Places MCP, Ticketmaster MCP, OSMMCP, Open-Meteo) instead of reinventing. Wrap them as Tools.
- G4. Implementable on **小龙虾 (OpenClaw)** runtime. No LangGraph dependency. Architecture borrows LangGraph's cyclical-state-graph pattern as 2 Python loops + a tool registry.
- G5. POC ships in **1–2 days**, Full architecture in **1–2 weeks**.

### Non-Goals
- ❌ UI / chat rendering (OpenClaw)
- ❌ Place index / data ingestion (G-Brain + friend)
- ❌ Booking / payments
- ❌ In-trip real-time adaptation (general AI handles)
- ❌ Multi-day trips, multi-user collaboration

---

## 2. Locked Assumptions

| Dependency | Status | What we assume it does |
|---|---|---|
| **OpenClaw (小龙虾)** | ✅ ready (friend) | Receives screenshots + chat; hosts agent; renders Markdown back |
| **G-Brain backend** | ✅ ready (friend) | `POST /experience` → `PlaceCandidate[]` per backend schema v2 |
| **Claude API** | ✅ ready | Sonnet 4.6 (main), Haiku 4.5 (cheap), vision + tool use |
| **MCPs** | install per-tool | Foursquare Places, Ticketmaster Discovery, OSMMCP |
| **Open-Meteo** | ✅ public | Free weather API, no key |

---

## 3. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│ USER (in OpenClaw chat)                                                  │
└────────────────────────┬─────────────────────────────────────────────────┘
                         │ screenshots + chat turns
                         ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ AGENT 1: INTAKE ORCHESTRATOR  (one LLM loop with tool use)               │
│                                                                          │
│   while not router(state).is_ready:                                      │
│       tool: vision_extract_taste(images)                                 │
│       tool: extract_slots(user_turn, state)                              │
│       if router says ASK:                                                │
│           tool: generate_question(state) → ask user                      │
│       else:                                                              │
│           break                                                          │
└────────────────────────┬─────────────────────────────────────────────────┘
                         │ IntakeState (sufficient)
                         ▼
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
    tool: search_places   tool: fetch_enrichment
    (G-Brain backend)     (weather + events,                    PARALLEL
                           parallel sub-calls)
                │                 │
                └────────┬────────┘
                         ▼
              tool: generate_concepts(state, candidates, enrichment)
                         │
                         ▼ 2–3 Concepts
┌──────────────────────────────────────────────────────────────────────────┐
│ AGENT 2: PLAN COMPOSER × 2-3  (parallel; one true agent instance each)   │
│                                                                          │
│   Each instance has tools:                                               │
│     ─ get_place_details (Foursquare MCP)                                 │
│     ─ get_route (OSMMCP)                                                 │
│     ─ web_search (last-mile verification)                                │
│                                                                          │
│   Loops internally to verify hours, swap stops if logistics break, etc.  │
│                                                                          │
│   Output per instance: one TripPlan (Markdown-ready)                     │
└────────────────────────┬─────────────────────────────────────────────────┘
                         │ TripPlan[]
                         ▼
              [optional] tool: critic_score(plans)                ┐ if any
                         │                                        │ score < τ
                         │   ◄────── retry weakest 1-2 plans      │ → loop
                         ▼                                        ┘
              format_proposals(plans)  ← pure template, no LLM
                         │
                         ▼
                   render to OpenClaw
                         │
                         ▼
              user picks / says "refine"
                         │
                         ▼
              Composer re-invoked on chosen plan w/ delta (≤2 rounds)
```

---

## 4. Agent Catalog

> Only entities with **autonomous LLM loops and tool use** count as agents. Everything else is a tool (§5) or a pure function (§6).

| # | Agent | Role | Model | Inputs | Outputs | Tools used | Loop? |
|---|---|---|---|---|---|---|---|
| 1 | **Intake Orchestrator** | Run the cyclical intake state machine; ask user smart questions until state is sufficient | Sonnet 4.6 | screenshots + chat turns | finalized `IntakeState` | `vision_extract_taste`, `extract_slots`, `generate_question` | yes, ≤10 turns |
| 2 | **Plan Composer** (× 2–3 parallel instances) | Turn one Concept into one TripPlan; verify facts and adjust stops as needed | Sonnet 4.6 | one `Concept` + `PlaceCandidate[]` + `EnrichedContext` | one `TripPlan` (Markdown) | `get_place_details`, `get_route`, `web_search` | yes, internal until quality ok |
| 3 *(optional, Phase 4+)* | **Plan Critic** | Score TripPlans on stranger-test, arc coherence, avoidance respect; trigger retry | Sonnet 4.6 | `TripPlan[]` | scored plans + retry directives | none | no |

**Why only 2 agents** (full rationale in commit history of this doc, v1 had 10):
- A "single-LLM-call with structured output" is a **tool**, not an agent. We previously over-classified.
- Modern LLMs (Sonnet 4.6) handle multi-step reasoning + tool use within one loop well enough that splitting into specialized agents adds latency + cost + debugging surface area without quality gains.
- **Genuine multi-agent value**: parallel Composer × 3 with different Concepts → diversity. This is preserved.
- **If quality testing shows the Composer's output is generic / un-specific, add the Critic agent in Phase 4.** Don't add specialists speculatively.

---

## 5. Tool Catalog

> Most "intelligence" lives in tools, not agents. Tools are stateless, cacheable, parallelizable, and have crisp input/output contracts.

| Tool | Implementation | Wraps | Used by | Cost |
|---|---|---|---|---|
| `vision_extract_taste` | Sonnet 4.6 + vision, single call | n/a (LLM-as-function) | Intake Orchestrator | per call |
| `extract_slots` | Haiku 4.5, single call | n/a | Intake Orchestrator | per call (cheap) |
| `generate_question` | Sonnet 4.6, single call, info-gain prompt | n/a | Intake Orchestrator | per call |
| `search_places` | HTTP POST | G-Brain `/experience` | (between agents) | free |
| `get_weather` | HTTP GET | Open-Meteo | (between agents, in `fetch_enrichment`) | **free, no key** |
| `search_events` | MCP call + RSS parse | Ticketmaster MCP + Funcheap RSS | (between agents) | free 5k/day |
| `fetch_enrichment` | Python wrapper that calls `get_weather` + `search_events` in parallel | composed | (between agents) | composed |
| `generate_concepts` | Sonnet 4.6, single call, diversity-encouraging prompt | n/a | (between agents) | per call |
| `get_place_details` | MCP call | Foursquare Places MCP | Composer | free starter credit |
| `get_route` | MCP call | OSMMCP | Composer | **free, no key** |
| `web_search` | Claude native tool | Anthropic API | Composer (sparingly) | per Claude pricing |
| `critic_score` *(Phase 4+)* | Sonnet 4.6, single call, evaluation rubric | n/a | (Phase 4 quality gate) | per call |
| `format_proposals` | Python template | n/a | (final formatting step) | **free, no LLM** |

### Why some "tools" are LLM-backed
A tool is **anything with a clean function signature**. It doesn't have to be deterministic. `vision_extract_taste` and `extract_slots` are LLM-backed because that's the right implementation for their I/O contract — but they're not agents because they don't loop or make autonomous decisions about what to do next.

### MCP installation (one-time, in OpenClaw config)
```
foursquare-places-mcp     → needs FOURSQUARE_API_KEY (free)
osmmcp                    → no key
mcp-server-ticketmaster   → needs TICKETMASTER_API_KEY (free, 5k/day)
```

### Tools NOT to add (anti-pattern, per earlier research)
- ❌ Yelp Fusion / Yelp MCP — paid, opaque billing
- ❌ Eventbrite Public Search — dead since 2020
- ❌ Google Places API — billing risk; Foursquare covers 90%

---

## 6. Pure Python Functions

> Logic that should never be in an LLM call. Deterministic, testable, free.

| Function | Job | Why pure code |
|---|---|---|
| `router(state) → ASK | READY | STOP_HARD_CAP` | Stopping rule per PRD: `turn >= 10` OR `avg(confidence) >= 0.8 AND min >= 0.5` OR user said done | Determinism — LLM cannot decide its own stopping rule reliably |
| `state.serialize_to_experience_request(state) → ExperienceRequest` | Map IntakeState → backend contract; handle the 3 alignment bugs from PRD | Must be exact; LLM would drift |
| `state.merge_slot_updates(state, updates) → state` | Apply Extractor's slot updates with confidence merge logic | Straightforward dict merge |
| `format_proposals(plans) → markdown` | Render 2-3 TripPlans into a single response with side-by-side comparison | Pure template; LLM adds no value |

---

## 7. Data Contracts

> Most types in `backend-data-schema-v2.md` or `prd-v2-day-composer.md`. New types defined here.

### Referenced existing contracts
- `IntakeState` — PRD §Interaction Layer 架构 §A
- `TasteSignature` — backend schema §2.5
- `ExperienceRequest` — backend schema §2.6
- `PlaceCandidate` — backend schema §2.7
- `TripPlan` — backend schema §2.9

### New contracts (defined here)

#### `EnrichedContext`
```typescript
type EnrichedContext = {
  weather: {
    forecast_summary: string;    // "sunny 64°F, no rain"
    impact_note: string;         // "outdoor stops are fine"
  };
  events: Event[];               // time-bounded events overlapping user window
};
```

#### `Concept`
```typescript
type Concept = {
  concept_id: string;
  day_theme: string;             // "旧湾区与恢复感的一天"
  mood_tags: MoodTag[];
  arc_signature: string;         // "慢起 → 自然恢复 → 烟火气 → 早收"
  pacing_blueprint: PacingRole[]; // length 4
  anchor_place_ids: string[];    // 1-2 must-have "spine"
  emotional_thesis: string;      // 1 sentence: why this concept for THIS user
};
```

#### `ProposalSet`
```typescript
type ProposalSet = {
  intake_summary: string;        // "I heard you want X, Y. Here are 2-3 ways:"
  plans: TripPlan[];
  comparison: {
    plan_id: string;
    one_line_pitch: string;      // "the quiet recovery option"
    best_for: string;            // "if you're more tired than expected"
  }[];
};
```

---

## 8. Sequence Diagram — Happy Path

```
T+0s    User drops 5 screenshots into OpenClaw chat
T+1s    Intake Orchestrator wakes; calls vision_extract_taste(images)
T+8s    TasteSignature returned; loop begins

T+9s    router(state) → ASK (low confidence everywhere)
T+10s   generate_question(state) → "今天想 restore 还是 explore？"
T+25s   user answers; extract_slots(...) updates emotional_intent
T+27s   router(state) → still ASK
        ... (loop 2-3 more turns)

T+90s   router(state) → READY

T+91s   search_places(serialize_to_experience_request(state)) → 12 PlaceCandidates
T+93s   fetch_enrichment() in parallel:
            ├── get_weather(Bay Area, Sat) → sunny, 64°F
            └── search_events(...) → 3 events
T+96s   EnrichedContext ready

T+97s   generate_concepts(state, candidates, enrichment) → 3 Concepts

T+99s   Plan Composer × 3 in parallel (each ~12s):
            ├── Composer A (Concept "South Bay 慢恢复")
            ├── Composer B (Concept "SF 轻探索")
            └── Composer C (Concept "Peninsula reconnect")
            (each internally calls get_place_details / get_route / web_search as needed)
T+115s  3 TripPlans ready

T+115s  [Phase 4 only: critic_score(plans); retry if any < τ]

T+116s  format_proposals(plans) → final Markdown bundle
T+118s  OpenClaw renders to user

T+150s  user: "Plan B 太赶了，能慢一点吗？"
T+151s  Composer re-invoked on Plan B with delta → revised B
T+165s  OpenClaw renders revised B

Total intake-to-3-plans: ~120s. Full demo with refine: ~165s.
```

---

## 9. Failure Modes & Fallbacks

| Failure | Detection | Fallback |
|---|---|---|
| Vision tool fails | exception / empty TasteSignature | Skip; tell user "I couldn't read the screenshots — describe in words" |
| Backend `/experience` timeout/500 | HTTP error / >10s | Local seed JSON (`poc-demo/demo_places.json`); flag "cached recommendations" |
| `<4` PlaceCandidates returned | count check | Composer builds shorter plan; Presenter outputs fewer plans |
| Weather API down | HTTP error | Skip; Composer must not reference weather |
| Event search returns 0 | count check | No event-based closing; use cafe/dessert closing instead |
| Web search rate-limited | exception | Skip; Composer flags `[hours TBD]` in output |
| Composer output fails TripPlan schema | parse fail | Retry once with stricter prompt; if still bad, drop from ProposalSet |
| All Composers fail | count check | Hard error: "Try again or rephrase" |
| User refine ambiguous | Composer detects + asks 1 clarifying turn | One clarifying turn, then re-compose |

---

## 10. POC Scope vs Full Scope

### POC (hackathon, 1–2 days, ~7 hours)

| Layer | POC | Cut |
|---|---|---|
| Intake | Intake Orchestrator with 3 tools (vision, extract, qgen) | Critic |
| Backend | Mock with local JSON (10 places) | Real `/experience` |
| Enrichment | **Skip entirely** | weather / events / web_search |
| Composition | **1 Composer call, 1 plan + 1 adaptive branch** | Concepts + parallel ×3 |
| Critic | none | yes (Phase 4) |
| Refine | single-shot | full loop |

→ POC: **1 Agent + 4 Tools + 2 pure functions**.

### Full (1–2 weeks post-POC, ~13 hours)

| Layer | Full |
|---|---|
| Intake | Same orchestrator + info-gain prompt for Q-Gen |
| Backend | Real `/experience` + graceful fallback |
| Enrichment | weather + events + web_search via `fetch_enrichment` |
| Composition | `generate_concepts` + parallel Composer × 2-3 |
| Critic | quality gate, retry weakest plans |
| Refine | ≤2 rounds |

---

## 11. Build Order

> Each phase ends with something runnable + committable.

### Phase 0 — Scaffolding (30 min)
- `agent/` folder + module skeletons
- Define `IntakeState` type in `state.py`
- Stub all functions to return fake data
- `main.py` runs end-to-end on fakes, prints fake TripPlan

**Exit**: `python main.py` runs without crashing.

### Phase 1 — Intake Orchestrator (3 hours)
- Implement `vision_extract_taste`, `extract_slots`, `generate_question` as tools
- Implement `router` and `state.merge_slot_updates` as pure functions
- Wire the loop in Intake Orchestrator agent

**Exit**: Can run a real intake conversation against Mia's persona.

### Phase 2 — Backend integration (1 hour)
- Implement `search_places` (HTTP + local fallback via `MOCK_BACKEND=1`)
- Implement `state.serialize_to_experience_request` (fix the 3 alignment bugs)

**Exit**: Real `/experience` call returns candidates for Mia's persona.

### Phase 3 — Composer single-plan (2.5 hours)
- Implement Plan Composer agent
- Prompt = `poc-demo/composer_prompt.md`
- No tools yet (skip get_route / get_place_details)

**Exit**: One demo-quality TripPlan for Mia's persona.

### → POC ENDS HERE. ~7 hours total. ShippABLE for hackathon. →

### Phase 4 — Enrichment + multi-plan (4 hours)
- Implement `get_weather`, `search_events`, `fetch_enrichment`
- Implement `generate_concepts`
- Composer × 2-3 in parallel via `asyncio.gather`
- Install MCPs (Foursquare, OSMMCP, Ticketmaster) in OpenClaw config
- Composer gains tool access (`get_place_details`, `get_route`, `web_search`)

**Exit**: 2-3 visibly distinct plans with side-by-side comparison.

### Phase 5 — Critic + Refine polish (2 hours)
- Implement Plan Critic agent
- Quality gate with retry on weakest plan
- Refine loop with ≤2 round cap

**Exit**: Bad plans get auto-improved; "更安静一点" produces meaningfully different plan.

---

## 12. Code Structure

```
agent/
├── main.py                  # entrypoint; runs the orchestration
├── state.py                 # IntakeState type, serializers, merge logic, router
├── intake/
│   └── orchestrator.py      # Agent 1: Intake Orchestrator (the loop)
├── compose/
│   ├── composer.py          # Agent 2: Plan Composer
│   └── concepts.py          # generate_concepts tool
├── critic/
│   └── critic.py            # [Phase 4+] Plan Critic agent
├── tools/
│   ├── vision.py            # vision_extract_taste
│   ├── extract.py           # extract_slots
│   ├── qgen.py              # generate_question
│   ├── backend.py           # search_places (HTTP + local fallback)
│   ├── weather.py           # get_weather (Open-Meteo)
│   ├── events.py            # search_events (Ticketmaster + Funcheap)
│   ├── enrichment.py        # fetch_enrichment (parallel composite)
│   ├── place_details.py     # get_place_details (Foursquare MCP)
│   ├── routes.py            # get_route (OSMMCP)
│   └── websearch.py         # web_search (Claude native)
├── present/
│   └── format.py            # format_proposals (pure template)
└── prompts/
    ├── orchestrator.md
    ├── vision.md
    ├── extractor.md
    ├── qgen.md
    ├── concepts.md
    ├── composer.md          # symlink to poc-demo/composer_prompt.md
    └── critic.md            # [Phase 4+]
```

**Module count**: 14 (was 20+ in v1).

---

## 13. Open Questions / Decisions

| # | Question | Default |
|---|---|---|
| 1 | Should `web_search` be in Intake Orchestrator's tool set too (e.g., to clarify a place the user mentioned)? | **No for POC.** Only Composer uses web_search. |
| 2 | Cache `IntakeState` across user sessions? | **POC: no.** Full: yes, keyed by user. |
| 3 | Fixed 3 Concepts/Plans or dynamic 2-4? | Fixed 3 for POC; `generate_concepts` may emit fewer if diversity fails. |
| 4 | Refine round cap | 2 rounds, then prompt "lock or restart." |
| 5 | When intake confidence is low, does Q-Gen assume + flag, or always ask? | Always ask if any dim `<0.5`; otherwise assume + flag in output. |
| 6 | OpenClaw streaming | **Stream** the Composer output — perceived latency matters. |
| 7 | Multi-language | Mix Chinese-English by default; bias toward user's input language. |

---

## 14. Success Criteria

| Dimension | Metric | Target |
|---|---|---|
| Latency | Intake start → 2-3 plans rendered | ≤ 2 minutes |
| Correctness | TripPlan schema validates | 100% (or drop, don't crash) |
| Diversity | Pairwise edit distance between plans | ≥40% (no 2 plans share 3+ stops) |
| Robustness | Survives any single tool failure | Yes (per §9) |
| Composer quality | "Stranger can't tell who this user is" test on `why_fits_today` | Pass on Mia's persona + 1 contrast persona |
| Cost | Per full session (intake + 3 plans + 1 refine) | ≤ $0.30 |

---

## 15. References

- PRD: `mvp-list/prd-v2-day-composer.md`
- Backend schema: `mvp-list/backend-data-schema-v2.md`
- POC demo assets: `mvp-list/poc-demo/`
- Anthropic "Building Effective Agents" (2024-12): https://www.anthropic.com/research/building-effective-agents
- SymptomAI inspiration: arXiv 2605.04012
- Adaptive Question Selection algorithm: arXiv 2604.22067
- Foursquare Places MCP: github.com/foursquare/foursquare-places-mcp
- OSMMCP: github.com/NERVsystems/osmmcp
- Ticketmaster MCP: github.com/delorenj/mcp-server-ticketmaster
- Open-Meteo: open-meteo.com/en/docs
