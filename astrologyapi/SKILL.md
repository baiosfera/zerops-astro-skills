---
name: astrologyapi
description: "Trigger: astrologyapi, astrology-api.io, core numerology, kabbalah gematria, hellenistic timing timeline, relocation acg, drik bala. Motor REST de astrologia, numerologia y timing helenistico."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---
# Astrology-API.io Engine (V3)

High-performance developer-first astrological, numerological, and Hellenistic time-lord REST API engine powered by Swiss Ephemeris SE 2.10 across 100+ endpoints.

## Core Architecture

Astrology-API.io operates via high-speed JSON endpoints (`https://api.astrology-api.io/api/v3/`) delivering sub-300ms responses worldwide. Authentication uses Bearer tokens prioritizing `$ASTROLOGY_API_IO` with fallback to `$ASTROLOGY_API_KEY` (`Authorization: Bearer ${ASTROLOGY_API_IO:-$ASTROLOGY_API_KEY}`).

- **Primary Reference**: [references/usage.md](file:///var/www/.agents/skills/astrologyapi/references/usage.md) — Comprehensive REST payloads (cURL) for all 9 core functional modules and multi-aggregators.
- **Infrastructure Guide**: [references/infra.md](file:///var/www/.agents/skills/astrologyapi/references/infra.md) — Authentication cascade, Free Tier (50 req/mo) quota stretching, rate limits, and CoHaLo process hygiene.

## Available Engines & Modules

1. **Western Natal & 23 House Systems**: Tropical/sidereal natal charts, aspects, and planetary tables (`POST /api/v3/western/natal-chart`).
2. **Multi-Name Core Numerology (5 Pillars)**: Life Path, Expression, Soul Urge, Personality, and Birthday numbers (`POST /api/v3/numerology/core-numbers`).
3. **Hebrew Kabbalistic Gematria (4 Systems)**: Standard, Absolute, Ordinal, and Reduced values (`POST /api/v3/kabbalah/gematria`).
4. **Hellenistic Timing Suite**: Profections, Firdaria, Decennials, Zodiacal Releasing, and Timeline Aggregator (`/api/v3/timing/*`).
5. **Vedic Jyotish & Drishti**: Lahiri birth details, BPHS Drik Bala, Graha Drishti, and Jaimini aspects (`POST /api/v3/vedic/*`).
6. **Horoscope Engine**: Daily, weekly, monthly, and yearly horoscopes in 17 languages (`GET /api/v3/horoscope/*`).
7. **Relocation & ACG World Analysis**: Astrocartography, Local Space azimuths, and multi-city ranking (`POST /api/v3/analysis/relocation-report`).
8. **Graphic Ephemeris & Harmonics SVG**: 1st through 16th harmonic continuous planetary curves (`POST /api/v3/render/graphic-ephemeris`).
9. **Astrology AI & Multi-Aggregators**: LLM agent, horary, and batch aggregators (`/api/v3/timing/timeline`, `/api/v3/data/positions/enhanced`, `/api/v3/data/global-positions`).

## Free Tier Quota Maximization (50 req/mo)

1. **Mundane Daily Cache**: 1 call/day at 00:00 UTC to `/data/global-positions` serves all users (30 reqs/mo).
2. **Hellenistic Timeline Aggregator**: `/api/v3/timing/timeline` combines profections, firdaria, decennials, and ZR (1 credit instead of 4).
3. **Enhanced Positions Aggregator**: `/api/v3/data/positions/enhanced` returns positions, dignities, joys, sect, and 9 Arabic lots in 1 call.
4. **L1 Natal Invariance Cache**: Hash birth data (`SHA-256`); natal charts never expire (0 repeated calls).

## Critical Workflows

1. **Defensive Throttling**: On Free Plan, enforce `sleep 2.0` between requests.
2. **Process Hygiene (CoHaLo)**: Maximum 10s execution timeouts (`timeout 10s`), `WaitMsBeforeAsync: 10000`, Zero Orphaned Tasks (`manage_task action="kill"`).
3. **Circuit Breaker**: Max 2 retries on 500/timeout before escalation; verify HTTP 200 and `status: "OK"`.
4. **Universal Client-Agnostic Schemas**: Standardize birth parameters (`YYYY`, `MM`, `DD`, `HH`, `MIN`, `LAT`, `LNG`, `TZ_NAME`). Zero PII.

## Quick Reference Table

| Module | REST Endpoint | Key Parameters |
|---|---|---|
| Western Natal | `POST /api/v3/western/natal-chart` | `birth_data`, `house_system` |
| Core Numerology | `POST /api/v3/numerology/core-numbers` | `birth_data`, `subject.name` |
| Hebrew Gematria | `POST /api/v3/kabbalah/gematria` | `text`, `system` |
| Timing Timeline | `POST /api/v3/timing/timeline` | `birth_data`, `techniques` |
| Vedic Drishti | `POST /api/v3/vedic/aspects` | `birth_data`, `ayanamsa` |
| Daily Horoscope | `GET /api/v3/horoscope/daily` | `sign`, `lang`, `format` |
| Relocation Report | `POST /api/v3/analysis/relocation-report` | `birth_data`, `candidate_cities` |
| Graphic Ephemeris | `POST /api/v3/render/graphic-ephemeris` | `birth_data`, `harmonic` |

## Output Contract

Parse JSON with `jq` or standard parsers. Verify `status: "OK"`. Results route downstream to diagnostic and branding modules.
