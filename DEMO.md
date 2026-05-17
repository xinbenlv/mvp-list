# Day Composer v2 — Demo Guide

How to run the end-to-end Day Composer POC: backend agent → real LLM → frontend renderer.

> The original `README.md` covers v1 (the place-curation skill). This file covers the v2 Day Composer system that proposes 2–3 distinct day plans for Bay Area Saturdays. See `prd-v2-day-composer.md` for the product spec.

---

## 90-second elevator pitch

User drops a few screenshots (taste samples, not candidate places) + answers ≤10 lightweight questions. Agent responds with **2–3 structurally-distinct trip plans** — each with a narrative day theme, 4 stops, an emotional arc, dish recommendations, and an adaptive branch. The 3 plans differ by `theme_anchor` (cultural_restorative / outdoor_exploratory / social_high_energy / quiet_intimate) so the user can pick the day shape that fits today's mood.

Backend is a 2-agent system (Intake Orchestrator + Plan Composer × N parallel) wrapping a Claude Sonnet 4.6 core. Frontend is Next.js with 3 visual templates. End-to-end output is committed in `poc-demo/garry-demo/v3/` and rendered at `/demo/agent-live`.

---

## Quickstart — see the demo in 60 seconds

If you just want to see what it does:

```bash
# Option 1 — pre-built static site (no install needed)
cd poc-demo/garry-demo/
unzip garry-saturdays.zip -d garry-demo-out/
cd garry-demo-out/
./START.command   # macOS — opens browser
# OR manually: python3 -m http.server 8080 → open http://localhost:8080

# Option 2 — live Next.js dev server
cd day-composer-app/
pnpm install
pnpm dev
# open http://localhost:3000/demo
```

The `/demo` index links to:
- `/demo/family-day`, `/demo/cultural-day`, `/demo/golden-night` — hand-curated polished references
- `/demo/agent-live` — **real LLM agent output** rendered through all 3 templates

---

## Full end-to-end live demo (agent → frontend)

### Prerequisites

```bash
# Backend (Python agent)
brew install uv                              # if not already installed
cd mvp-list/
uv sync                                       # installs anthropic, pytest, ruff, mypy, pydantic
cp .env.example .env
# Edit .env: paste real ANTHROPIC_API_KEY (starts with sk-ant-)

# Frontend (Next.js)
cd day-composer-app/
pnpm install
```

### Step 1 — Run the agent end-to-end (real LLM)

```bash
cd mvp-list/

# Quickest path: --mock-intake bypasses the live intake conversation and
# loads a persona JSON as the pre-built IntakeState, then runs the real
# Composer (3 parallel Sonnet calls).
uv run python -m agent.main --mock-intake --persona garry_tan \
  < tests/fixtures/garry_first_turn.txt
```

You'll see ~300 lines of Markdown output with:
- A comparison table (3 plans at a glance)
- 3 full plan bodies — each with 4 stops, transitions, dish recommendations, adaptive branches
- A coaching block (`🫧 给今天的你`) if the persona triggers it

Available personas: `mia`, `garry_tan`, `alex_chen`, `sam_reyes`. Each has a matching fixture under `tests/fixtures/{persona}_first_turn.txt`.

### Step 2 — Generate frontend-shaped JSONs

```bash
mkdir -p poc-demo/garry-demo/v3/

uv run python -m agent.main --mock-intake --persona garry_tan \
  --emit-frontend-json poc-demo/garry-demo/v3/ \
  < tests/fixtures/garry_first_turn.txt
```

This writes 3 files in the `{plan, trip_context}` envelope shape the frontend expects (per `poc-demo/garry-demo/HANDOFF.md`):

```
poc-demo/garry-demo/v3/
├── garry_cultural_restorative.json
├── garry_outdoor_exploratory.json
└── garry_social_high_energy.json
```

### Step 3 — Sync the new JSONs into the Next.js app

```bash
cp poc-demo/garry-demo/v3/*.json \
   day-composer-app/lib/data/agent-v3/
```

(Static export requires JSONs co-located with the app; `next.config.js` doesn't enable cross-directory imports.)

### Step 4 — Rebuild + open

```bash
cd day-composer-app/
pnpm build && pnpm dev
# open http://localhost:3000/demo/agent-live
```

You'll see all 3 agent-generated plans rendered through the 3 templates (Polaroid → Cinematic → Aurora).

---

## Architecture (one-paragraph)

```
USER (CLI or OpenClaw)
   │ screenshots + chat
   ▼
[Intake Orchestrator]  ── (vision_extract_taste / extract_slots / generate_question) ──┐
   │ IntakeState (typed, 6-dim ontology)                                                │
   ▼                                                                                    │
[search_places]  ──►  [generate_concepts_simple] (rule-based, 2-3 distinct concepts)    │
   │ PlaceCandidate[]                  │                                                │
   └──────────────────────► [Plan Composer × N] (parallel Sonnet 4.6, real LLM)        │
                                  │ PlanResult (markdown + structured stops)            │
                                  ▼                                                     │
                            [check_diversity] → [deduplicate_first_stops]               │
                                  │                                                     │
                                  ▼                                                     │
                       [format_proposals] → final Markdown ProposalSet                  │
                       [transformer]      → frontend TripPlan JSON                      │
                                  │                                                     │
                                  ▼                                                     │
                         CLI stdout / day-composer-app/                                 │
```

Full architecture: `agent-engineering-design.md`. Test plan: `~/Documents/mia-second-brain/projects/day-composer/Test-and-Eval-plan-poc.md`. Implementation runbook: `~/Documents/mia-second-brain/projects/day-composer/Implement-poc.md`.

---

## Test suite

```bash
cd mvp-list/
uv run pytest tests/ -v --tb=short
# 108 tests, ~0.15s; all mocked (no live API)

# Live smoke (burns ~$0.05 per persona):
RUN_LIVE_LLM=1 uv run pytest tests/ -m live -v
```

---

## Project layout

```
mvp-list/                                ← repo root (xinbenlv/mvp-list)
├── README.md                            ← v1 (xinbenlv's place-curation skill)
├── DEMO.md                              ← this file
├── prd-v2-day-composer.md               ← v2 product PRD
├── backend-data-schema-v2.md            ← data contract specs
├── agent-engineering-design.md          ← architecture (HOW)
├── .env / .env.example                  ← ANTHROPIC_API_KEY lives in .env
├── pyproject.toml + uv.lock             ← Python deps via uv
├── agent/                               ← backend agent code
│   ├── main.py                          ← CLI entrypoint
│   ├── state.py                         ← IntakeState + serializers
│   ├── intake/orchestrator.py           ← cyclical intake agent
│   ├── compose/composer.py              ← Plan Composer (real LLM)
│   ├── compose/concepts.py              ← rule-based concept generator
│   ├── present/format.py                ← ProposalSet markdown wrapper
│   ├── present/diversity.py             ← Phase 3b diversity enforcement
│   ├── present/transformer.py           ← PlanResult → frontend JSON
│   ├── tools/                           ← vision, extract, qgen, backend
│   ├── critic/                          ← Phase 5 scaffold (not implemented)
│   └── prompts/composer.md              ← symlink → poc-demo/composer_prompt.md
├── tests/                               ← 108 tests, pytest-vcr-ready
│   └── fixtures/                        ← 4 personas × first-turn stdin
├── poc-demo/                            ← demo assets
│   ├── composer_prompt.md               ← the system prompt
│   ├── demo_places.json                 ← 22 hand-tagged Bay Area places (mock backend)
│   ├── {mia,garry_tan,alex_chen,sam_reyes}_persona.json
│   ├── dry-run/, dry-run-v2/, dry-run-v3/  ← captured LLM outputs for regression
│   └── garry-demo/                      ← frontend handoff + 3 reference JSONs + offline zip
│       ├── HANDOFF.md                   ← backend-frontend contract
│       ├── {cultural,family,golden}-day.json  ← hand-curated references
│       └── v3/                          ← generated by `--emit-frontend-json`
└── day-composer-app/                    ← Next.js frontend (collaborator's territory)
    ├── lib/types/trip-plan.ts           ← TypeScript contract
    ├── lib/data/                        ← sample-plan-en.ts + agent-generated.ts + agent-v3/
    ├── app/demo/                        ← /demo/family-day, /cultural-day, /golden-night, /agent-live
    ├── components/templates/            ← Polaroid / Cinematic / Aurora
    └── scripts/build-static.mjs         ← offline export
```

---

## Common demo failure modes (and rescues)

| Failure | Symptom | Rescue |
|---|---|---|
| `ANTHROPIC_API_KEY` missing / placeholder | Backend errors "API key not set" | Edit `.env`; or run with `--mock-intake` (still needs key for Composer) |
| Sonnet 4.x deprecated | API returns model-not-found | Edit `_MODEL` in `agent/compose/composer.py:42` to the current alias |
| Composer truncates → `stops: []` in JSONs | Frontend `/demo/agent-live` renders without per-stop content | Post-process: `MOCK_BACKEND=1 uv run python -c "..."` re-extracts stops from `markdown_full` (see commit `c227e31` message) |
| Live API rate limit | Composer times out / 429 | Fall back to `garry-saturdays.zip` offline bundle |
| Frontend out-of-sync with new JSONs | `/demo/agent-live` shows old data | Repeat Step 3 (cp JSONs into `agent-v3/`) + `pnpm build` |

---

## Persona test suite

4 personas span opposing axes — see `poc-demo/README.md` for the contrast table:

| Persona | Profile | Triggers |
|---|---|---|
| **Mia** | South Bay AI engineer + new mom; restoration-anchored | `cultural_restorative`, `outdoor_exploratory`, `quiet_intimate` themes |
| **Garry** | SF VC + vlogger + dad; high-energy urban exploration | `social_high_energy` + cinematic narrative |
| **Alex** | Newcomer to SF (3 weeks), solo/friends, transit-native | high `chaos_tolerance`, novelty-chasing |
| **Sam** | Burnout-edge solo Marin recovery, photofacial-aware | `🫧 coaching block` (restore + slow_down + low energy) |

Switch with `--persona {persona_id}` and the matching `tests/fixtures/{persona}_first_turn.txt`.

---

## What's intentionally out of scope (v3 / post-POC)

- Real HTTP `/compose` endpoint (currently the frontend reads static JSON files; Pattern 1 from HANDOFF would let it `fetch()` the agent live)
- Phase 5 Critic agent body (scaffold-only; would auto-retry weakest plan when avg score < threshold)
- Image URL enrichment (13 of 22 place_ids currently render with gradient fallback)
- Live intake via screenshots (the cyclical intake loop exists + is tested; the CLI defaults to `--mock-intake` because live screenshot upload needs OpenClaw runtime)
- Multi-day, multi-user collaboration, real bookings

---

## Where to read more

- **Product story** → `prd-v2-day-composer.md`
- **Data schema** → `backend-data-schema-v2.md`
- **Architecture** → `agent-engineering-design.md`
- **Implementation runbook** → `~/Documents/mia-second-brain/projects/day-composer/Implement-poc.md`
- **Test plan** → `~/Documents/mia-second-brain/projects/day-composer/Test-and-Eval-plan-poc.md`
- **Frontend contract** → `poc-demo/garry-demo/HANDOFF.md`
- **Original v1 README** → `README.md`
