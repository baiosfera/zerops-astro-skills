---
name: freeastroapi
description: "Trigger: freeastroapi, api.freeastroapi.com, calculate natal chart, bazi true solar, 4-in-1 numerology, kp v2 astrology, astrocartography geojson, electional timing contracts, tcm health bazi, neijing lifespan, vargas d1-d60, muhurat search. High-performance multi-tradition REST calculation engine exposing 197 routes across 15 domains."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.5"
---
# FreeAstroAPI Engine (v2.5)

Unified multi-tradition REST API calculation engine supporting Western Natal, Chinese BaZi & TCM Health, Neijing Lifespan, Vedic KP V2 & Vargas D1–D60, 4-in-1 Numerology, Astrocartography GeoJSON, and Commercial Electional timing (`https://api.freeastroapi.com/api/`).

## Architecture & Dual-RAG SSoT

FreeAstroAPI operates via authenticated JSON REST endpoints and SVG chart renderers authenticated with `x-api-key: $FREEASTRO_API_KEY`. The canonical OpenAPI 3.1 specification documents 197 unique routes (207 REST operations) across 15 functional domains:

- **Complete API Catalog & Payloads**: [`references/usage.md`](file:///var/www/.agents/skills/freeastroapi/references/usage.md) — Exhaustive payloads, schemas, parameters, and two-tier storage architecture.
- **Infrastructure & Environment Guide**: [`references/infra.md`](file:///var/www/.agents/skills/freeastroapi/references/infra.md) — Plan tiers (Entry $8/mo, 50k req/mo, 5 RPS), rate limits, idempotency, and error recovery.

## Core Engines & Domains

1. **Western Natal & Ephemeris**: Positions, 7 house systems, royal fixed stars, dominants, and untimed birth failsafe (`POST /api/v1/natal/calculate`).
2. **Visual Vector Wheels**: SVG/PNG charts for natal, transits, composite, and synastry (`POST /api/v1/natal/chart/`).
3. **Chinese BaZi & TCM Health**: Day Master, Ten Gods, Hidden Stems, Da Yun cycles, *Huangdi Neijing* 5 elements organ constitution, temperature/moisture indexes, and stochastic lifespan curve (`POST /api/v1/chinese/bazi`, `/bazi/health`, `/bazi/lifespan`). Requires `"time_standard": "true_solar"`.
4. **4-in-1 Unified Numerology**: Pythagorean (compound master numbers 11/22/33, karmic debts), Chaldean, Kabbalah, and Ank Jyotish (`POST /api/v1/numerology/profile`).
5. **Vedic Jyotish & KP V2**: Sidereal cusps, 4-level Sub-Lords, Vimshottari Dashas (5 levels), Shodashavargas D1–D60, and Muhurat search across 6 life purposes (`POST /api/v2/vedic/kp`, `/vargas`, `/muhurat/search`).
6. **Astrocartography GeoJSON**: WGS84 lines for 4 angles (`asc`, `dsc`, `mc`, `ic`) with `include_crossings: false` on Entry plan (`POST /api/v1/western/astrocartography/lines`).
7. **Commercial Electional Astrology**: Algorithmic window search across 10 business and life categories (`POST /api/v2/western/electional/<category>/search`).
8. **Progressions & Annual Profections**: Secondary, converse, tertiary, and quotidian progressions with exact aspect search windows (`POST /api/v1/western/progressions/*`) and Hellenistic annual profections (`POST /api/v1/western/profections/annual`).

## Operational Directives (CoHaLo)

1. **Schema Integrity**: Verify exact JSON keys and payload schemas in [`usage.md`](file:///var/www/.agents/skills/freeastroapi/references/usage.md) before dispatching requests.
2. **True Solar Correction**: Apply `"time_standard": "true_solar"` with exact geographic coordinates for all BaZi and TCM evaluations.
3. **Plan Boundaries**: Enforce `"include_crossings": false` on Astrocartography calls to comply with Entry plan limits. Note that continuous transit timelines require High plan; use snapshot `POST /api/v1/transits/calculate` on Entry.
4. **Bounded Execution**: Enforce `timeout 10s` on all HTTP calls and apply `sleep 0.25` throttle (5 RPS limit) in batch loops.
5. **Idempotency**: Pass `Idempotency-Key: $(uuidgen)` header on all billable report requests and chat completions.
6. **Two-Tier Storage**: Persist full JSON responses to `raw/json/dumps/` and condense extracted features into typed XML (<2.5 KB) in `raw/feeds/`.

## Output Contract

Inspect HTTP 200 status on all JSON responses and parse payloads directly with `jq` or standard JSON parsers before passing data downstream.
