---
name: astroway
description: "Trigger: astroway, api.astroway.info, human design bodygraph, bg5 penta, vargas d10, bazi ten gods, dashas 5 levels, acg lines, hellenistic zodiacal releasing, cosmobiology dial 90, uranian tnps. Massive Swiss Ephemeris REST engine with 777 operations across 59 domains."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.3"
---
# AstroWay REST Engine (v1.3)

High-precision astrological, metaphysical, and Human Design REST calculation engine powered by Swiss Ephemeris algorithms and NASA JPL DE440/DE441 planetary data (`https://api.astroway.info/v1/`).

## Architecture & Dual-RAG SSoT

AstroWay operates via authenticated HTTP `POST` and `GET` requests with `X-Api-Key: $ASTROWAY_API_KEY`. The canonical OpenAPI 3.1 specification documents 775 routes (777 operations) across 59 domains:

- **Complete API Catalog & Payloads**: [`references/usage.md`](file:///var/www/.agents/skills/astroway/references/usage.md) — Exhaustive documentation of all 777 operations, Pydantic schemas, 30-endpoint basket (740 credits), and return contracts.
- **Infrastructure & Environment Guide**: [`references/infra.md`](file:///var/www/.agents/skills/astroway/references/infra.md) — Indie PRO tier ($5/mo, 50k credits/mo, 30 req/min), compute tiers (1 to 7), and rate limits.

## Core Engines & Disciplines

1. **Western Natal & Wheel Rendering**: Classical/sidereal chart calculations, 7 house systems, and SVG/PNG wheels (`POST /v1/chart`, `/render/wheel/*`).
2. **Vedic Jyotish & Vargas D1–D60**: 16 Shodashavargas, 6-factor Shadbala in Rupas, Jaimini Karakas, and 10 Dasha systems down to Prana 5th level (`POST /v1/vedic/*`).
3. **Human Design Mechanics**: Complete BodyGraph, 9 Centers, 36 Channels, 64 Gates (conscious/unconscious 88° arc), Incarnation Cross, BG5 Penta, and PHS (`POST /v1/human-design`, `/hd/*`).
4. **Hellenistic & Traditional**: 15 Lots and Zodiacal Releasing (Brennan), Antiscia (Greenbaum), Bounds/Decennials (Hand), and Stoic Elementhood (Schmidt) (`POST /v1/hellenistic/*`).
5. **Cosmobiology & Hamburg School**: 90° Dial, Midpoint Trees, 8 Transneptunians (TNPs), and Witte symmetry formulas (`POST /v1/cosmobiology/*`).
6. **Chinese Metaphysics**: BaZi Four Pillars, Day Master, Ten Gods, Luck Pillars Da Yun, and Zi Wei Dou Shu 12 Palaces (`POST /v1/bazi/*`, `/chinese/*`, `/ziwei/*`).
7. **Astro-Geography & Relocation**: World ACG angular lines, Best Places ranking (34,028 GeoNames cities), Brady Star Parans, and Local Space (`POST /v1/acg`, `/v1/acg/best-places`).
8. **Modern Psychological & Evolutionary**: Liz Greene archetypes/shadow, Stephen Arroyo water house trauma, and Rudhyar lunation cycles (`POST /v1/modern/*`, `/evolutionary/*`).
9. **Numerology & Divination**: Pythagorean, Chaldean, Kabbalistic, and Vedic profiles; Tarot, Runes, and Geomancy (`POST /v1/numerology/*`, `/tarot/*`).

## Operational Directives (CoHaLo)

1. **Single-Character House Codes**: Pass single-letter codes (`P` = Placidus, `W` = Whole Sign, `K` = Koch, `C` = Campanus).
2. **Optimal Phase 0 Basket (740 credits)**: Extract 30 JSON endpoints (Tiers 1-3). VETO Tier 7 PDF reports (`/v1/reports/*` = 5,000 credits).
3. **Rate Limiting**: Enforce `sleep 2.0` between requests in batch loops (30 req/min in Indie PRO).
4. **Credit Audit & Idempotency**: Inspect `X-Credits-Remaining` header. Pass `Idempotency-Key: $(uuidgen)`.
