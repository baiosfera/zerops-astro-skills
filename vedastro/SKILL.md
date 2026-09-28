---
name: vedastro
description: "Trigger: vedastro, api.vedastro.org, horoscope predictions yogas, all planet data, all house data, dasa at range 5 levels, match report 16 kutas, classical texts rag. High-precision Vedic REST computation engine exposing 6 macro endpoints and 677 atomic calculators."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.3"
---
# VedAstro PRO Calculation & Classical Texts Engine (v1.3)

High-precision Vedic calculation REST API powered by Swiss Ephemeris and NASA JPL algorithms, exposing 6 macro endpoints and 677 granular atomic calculators.

## Core Architecture

VedAstro operates via high-speed REST endpoints (`https://api.vedastro.org/api/`) authenticated with `x-api-key: $VEDASTRO_API_KEY`. The active PRO Unlimited tier ($1/mo) provides unlimited requests, sub-200ms responses, and priority compute queue.

- **Primary Reference**: [`references/usage.md`](file:///var/www/.agents/skills/vedastro/references/usage.md) — REST payloads (cURL), schemas, and CoHaLo token compression architecture.
- **Advanced Catalog SSoT**: [`assets/advanced_calculators_catalog.json`](file:///var/www/.agents/skills/vedastro/assets/advanced_calculators_catalog.json) (symlinked at [`references/advanced_calculators_catalog.json`](file:///var/www/.agents/skills/vedastro/references/advanced_calculators_catalog.json)) — Machine-readable catalog of all 677 atomic methods.
- **Infrastructure Guide**: [`references/infra.md`](file:///var/www/.agents/skills/vedastro/references/infra.md) — PRO Unlimited specs, REST data lake pipeline, POST/GET date rules, and process hygiene.

## Flagship Engine Modules

1. **Horoscope Predictions (200+ Yogas & Doshas)**: Parashari and Jaimini combinations with classical citations (`POST /api/Calculate/HoroscopePredictions`).
2. **All Planet Data & Ephemeris**: Batch-calculates 144 factors for 9 planets (longitudes, avasthas, dignities, Shadbala) (`POST /api/Calculate/AllPlanetData`).
3. **All House Data & Bhavas**: Batch-calculates 40 factors for 12 houses (cusps, lords, occupants, aspects) (`POST /api/Calculate/AllHouseData`).
4. **Vimshottari Dashas (5 Levels)**: Maha, Antar, Pratyantar, Sookshma, and Prana dashas (`POST /api/Calculate/DasaAtRange` or `GET`).
5. **Match Report & Compatibility**: 16 Kutas / 36 Gunas Ashtakoota score and Dosha checks (`POST /api/Calculate/MatchReport`).
6. **Ashtakavarga Matrix & Charts**: Sarva and Bhinna Ashtakavarga points (`POST /api/Calculate/Ashtakvarga`).
7. **Classical Vedic Texts RAG**: Semantic vector search across ancient textbooks (`GET /api/Calculate/SearchSourceText/...`).
8. **Kundli SVG Visuals**: Vector chart rendering in South Indian, North Indian, and SkyChart formats (`GET /api/Calculate/SouthIndianChart/...`).

## Operational Discipline (CoHaLo)

1. **Date Delimitation**: Use forward slash `/` in POST (`"StdTime": "HH:mm DD/MM/YYYY +ZZ:ZZ"`) and hyphen `-` in GET (`/Time/<HH:mm>/<DD-MM-YYYY>/<+/-ZZ:ZZ>/`).
2. **Bounded Execution**: Enforce `timeout 10s` on all cURL requests and terminate detached processes with `manage_task action="kill"`.
3. **Circuit Breaker**: Cap retries at 2 attempts on 500 or timeout; inspect `Status: "Pass"`.
4. **Data Lake Storage**: Store full raw JSON in `raw/json/dumps/` and condense extracted features into typed XML (<2.5 KB) in `raw/feeds/`.
