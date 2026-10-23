---
name: freeastroapi
description: "Trigger: freeastroapi, api.freeastroapi.com, calculate natal chart, bazi true solar, 4-in-1 numerology, kp v2 astrology, astrocartography geojson, electional timing contracts, tcm health bazi, neijing lifespan, vargas d1-d60, muhurat search. High-performance multi-tradition REST calculation engine exposing 197 routes across 15 domains."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.6"
---

# `freeastroapi` — Multi-Tradition Calculation Engine (v2.6)

## Activation Contract
Unified multi-tradition REST API calculations: Western Natal, Chinese BaZi & TCM Health, Neijing Lifespan, Vedic KP V2 & Vargas D1–D60, 4-in-1 Numerology, Astrocartography GeoJSON, and Commercial Electional timing (`https://api.freeastroapi.com/api/`).

## Core Directives & Invariants
- **Authentication & Headers**: Authenticate with `x-api-key: $FREEASTRO_API_KEY`. Pass `Idempotency-Key: $(uuidgen)` on billable report requests.
- **True Solar Time**: Apply `"time_standard": "true_solar"` with exact longitude/latitude for BaZi and TCM health evaluations.
- **Plan Boundaries**: Enforce `"include_crossings": false` on Astrocartography calls to comply with Entry plan limits. For transits on Entry plan, use snapshot `POST /api/v1/natal/transits/calculate`.
- **Bounded Execution**: Enforce `timeout 10s` on all HTTP calls and apply `sleep 0.25` throttle (5 RPS limit) in batch loops.
- **Two-Tier Storage**: Persist raw JSON responses to `raw/json/dumps/` and condense extracted features into typed XML (<2.5 KB) in `raw/feeds/`.

## Decision Gates & References

| Domain | Route Pattern | Key Requirements | Reference |
|---|---|---|---|
| Western Natal & Wheel | `POST /api/v1/natal/calculate` | 7 house systems, dominants, SVG wheel | [`usage.md`](file:///var/www/zerops-astro-skills/freeastroapi/references/usage.md) |
| BaZi & TCM Health | `POST /api/v1/chinese/bazi` | `"time_standard": "true_solar"`, Neijing organ health | [`usage.md`](file:///var/www/zerops-astro-skills/freeastroapi/references/usage.md) |
| 4-in-1 Numerology | `POST /api/v1/numerology/profile` | Pythagorean, Chaldean, Kabbalah, Ank Jyotish | [`usage.md`](file:///var/www/zerops-astro-skills/freeastroapi/references/usage.md) |
| Vedic KP & Vargas | `POST /api/v2/vedic/kp` | Sub-lords, Dashas 5 levels, D1–D60 | [`usage.md`](file:///var/www/zerops-astro-skills/freeastroapi/references/usage.md) |
| Astrocartography | `POST /api/v1/western/astrocartography/lines` | `"include_crossings": false` (Entry plan) | [`usage.md`](file:///var/www/zerops-astro-skills/freeastroapi/references/usage.md) |
| Commercial Electional | `POST /api/v2/western/electional/<cat>/search` | Algorithmic window search (10 categories) | [`usage.md`](file:///var/www/zerops-astro-skills/freeastroapi/references/usage.md) |
| Infrastructure | Rate limits, quotas, recovery | Entry plan ($8/mo, 50k req, 5 RPS) | [`infra.md`](file:///var/www/zerops-astro-skills/freeastroapi/references/infra.md) |

## Output Contract
Verify HTTP 200 on all JSON responses and parse payloads directly with `jq` before passing downstream.
