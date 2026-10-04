---
name: astrologyapi
description: "Trigger: astrologyapi, astrology-api.io, core numerology, kabbalah gematria, hellenistic timing timeline, relocation acg, drik bala. Motor REST de astrologia, numerologia y timing helenistico."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---
# Astrology-API.io Engine (v2.1)

Developer-first astrological, numerological, and Hellenistic REST API engine powered by Swiss Ephemeris SE 2.10 across 349 endpoints.

## Core Architecture

Operates via high-speed JSON endpoints (`https://api.astrology-api.io/api/v3/`). Authenticates via Bearer tokens (`Authorization: Bearer ${ASTROLOGY_API_IO:-$ASTROLOGY_API_KEY}`).

- **Primary Reference**: [references/usage.md](file:///var/www/.agents/skills/astrologyapi/references/usage.md) — REST payloads for 34 namespaces, Almuten Figuris with Brent solver, and 7 Gematria ciphers.
- **Infrastructure Guide**: [references/infra.md](file:///var/www/.agents/skills/astrologyapi/references/infra.md) — Auth cascade, Free Tier 3-call strategy, and CoHaLo process hygiene.

## Available Engines & Modules

1. **Western Natal & 23 House Systems**: Tropical/sidereal natal charts and aspects (`POST /api/v3/western/natal-chart`).
2. **Core Numerology (5 Pillars)**: Life Path, Expression, Soul Urge, Personality, Birthday (`POST /api/v3/numerology/core-numbers`).
3. **Kabbalistic Gematria (7 Methods & 72 Angels)**: Standard, Gadol, Katan, Ordinal, Atbash, Albam, Shem HaMephorash (`POST /api/v3/kabbalah/*`).
4. **Hellenistic Timing Suite**: Profections, Firdaria, Decennials, ZR, and Timeline Aggregator (`/api/v3/timing/*`).
5. **Traditional Dignities & Almuten**: Bonatti 5/4/3/2/1 weights, prenatal syzygy Brent solver, Hyleg (`POST /api/v3/traditional/almuten`).
6. **Vedic Jyotish & Drishti**: BPHS Graha Drishti (Ch.27) vs Drik Bala (Ch.26) in virupas matching JHora 8.0 (`POST /api/v3/vedic/*`).
7. **Horoscope Engine**: Multi-horizon horoscopes in 17 languages (`GET /api/v3/horoscope/*`).
8. **Relocation & ACG**: Astrocartography, Local Space azimuths, and multi-city ranking (`POST /api/v3/analysis/relocation-report`).
9. **Graphic Ephemeris SVG**: 1st-16th harmonic continuous planetary curves (`POST /api/v3/render/graphic-ephemeris`).

## Free Tier 3-Call Ingestion Strategy (50 req/mo)

For Phase 0 extraction, exactly 3 calls ingest the complete profile per client:
1. `POST /api/v3/timing/timeline`: Profections, Firdaria, Decennials, and ZR in 1 call (1 credit).
2. `POST /api/v3/data/positions/enhanced`: Positions, dignities, joys, sect, and 9 Arabic lots in 1 call (1 credit).
3. `POST /api/v3/numerology/core-numbers`: 5 core master numbers and name vibrations (1 credit).
Total: 3 credits per client (16 full client audits per month on Free tier).

## Critical Workflows

1. **Defensive Throttling**: Enforce `sleep 2.0` between requests on Free tier.
2. **Process Hygiene**: Timeouts `timeout 10s`, `WaitMsBeforeAsync: 10000`, zero orphaned tasks (`manage_task action="kill"`).
3. **Circuit Breaker**: Max 2 retries on 500/timeout; verify HTTP 200 and `status: "OK"`.
4. **Universal Schemas**: Standardize birth parameters (`YYYY`, `MM`, `DD`, `HH`, `MIN`, `LAT`, `LNG`, `TZ_NAME`). Zero PII.

## Output Contract

Parse JSON with standard tools (`jq`). Verify `status: "OK"`. Downstream routing feeds diagnostic and branding modules.
