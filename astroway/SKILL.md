---
name: astroway
description: "Trigger: astroway, api.astroway.info, human design bodygraph, vargas d10, bazi ten gods, dashas 5 levels, acg lines, hellenistic zodiacal releasing. Massive Swiss Ephemeris REST engine with 760 endpoints across 59 domains."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---
# AstroWay REST Engine

High-precision astrological, metaphysical, and Human Design REST calculation engine powered by Swiss Ephemeris algorithms and NASA JPL DE440/DE441 planetary data (`https://api.astroway.info/v1/`).

## Architecture & Dual-RAG SSoT

AstroWay operates strictly via authenticated HTTP `POST` and `GET` requests with `X-Api-Key: $ASTROWAY_API_KEY`. The legacy local MCP server has been decommissioned to prevent double credit billing, eliminate context clutter, and ensure transparent credit accounting.

- **Complete API Catalog & Payloads**: [references/usage.md](file:///var/www/.agents/skills/astroway/references/usage.md) — Exhaustive documentation of all 760 endpoints across 59 domains, Pydantic input schemas, and return contracts.
- **Infrastructure & Environment Guide**: [references/infra.md](file:///var/www/.agents/skills/astroway/references/infra.md) — Indie PRO tier ($5/mo, 50k credits/mo, 30 req/min), credit compute tiers (1 to 7), audit headers, idempotency, and error recovery.

## Core Engines & Disciplines

1. **Western Natal & Wheel Rendering**: Classical/sidereal chart calculations, 7 house systems, aspect matrices, and SVG/PNG wheels (`POST /v1/chart`, `/render/wheel/*`).
2. **Vedic Jyotish & Vargas D1–D60**: 16 Shodashavargas, 6-factor Shadbala, Jaimini Karakas/Padas, Lal Kitab, and 10 Dasha systems down to Prana 5th level (`POST /v1/vedic/*`).
3. **Human Design Mechanics**: Complete BodyGraph, 9 Centers, 36 Channels, 64 Gates, Circuitry, Incarnation Cross, BG5 Penta, and PHS Sensitivity (`POST /v1/human-design`, `/hd/*`).
4. **Hellenistic & Traditional**: 15 Lots (Brennan), Zodiacal Releasing Spirit/Fortune, Antiscia (Greenbaum), Bounds/Decennials (Hand), and Stoic Elementhood (Schmidt) (`POST /v1/hellenistic/*`).
5. **Cosmobiology & Hamburg School**: 90° Dial, Midpoint Trees, 8 hypothetical Transneptunians, and Witte symmetry formulas (`POST /v1/cosmobiology/*`).
6. **Chinese Metaphysics**: BaZi Four Pillars, Day Master, Ten Gods, Luck Pillars Da Yun, Flying Stars Feng Shui, and Zi Wei Dou Shu 12 Palaces (`POST /v1/bazi/*`, `/chinese/*`, `/ziwei/*`).
7. **Astro-Geography & Relocation**: World ACG angular lines, thematic Best Places, Parans, and Local Space azimuths (`POST /v1/acg`, `/geo/*`).
8. **Modern Psychological & Evolutionary**: Liz Greene archetypes/shadow, Stephen Arroyo water house trauma, Dane Rudhyar lunation cycles, and evolutionary nodal axis (`POST /v1/psychological/*`, `/evolutionary/*`).
9. **Quadruple Numerology & Divination**: Pythagorean, Chaldean, Kabbalistic, and Vedic profiles; Rider-Waite/Marseille/Lenormand Tarot, Runes, and Geomancy (`POST /v1/numerology/*`, `/tarot/*`, `/geomancy/*`).
10. **AI Reports & Multilingual Localization**: Structured interpretations and publication-ready narratives localized in 21 languages (`POST /v1/ai/*`, `/reports/*`).

## Operational Directives

1. Consult [usage.md](file:///var/www/.agents/skills/astroway/references/usage.md) for endpoint paths and canonical `ChartInput` payloads before formulating calls.
2. In batch loops, apply `sleep 2.0` to respect the 30 req/min rate limit of the Indie PRO tier.
3. In unattended runs, inspect `X-Credits-Remaining` and `X-Credits-Used` headers on every response.
4. Bound all HTTP requests with `timeout 10s` and enforce safe retries with `Idempotency-Key: $(uuidgen)`.
