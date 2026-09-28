# Astrology-API.io (V3) Canonical Reference Pointer

Astrology-API.io is now maintained as a sovereign first-class Dual-RAG System Skill in the workspace.

## Primary Documentation Links

- **Main Router**: [.agents/skills/astrologyapi/SKILL.md](file:///var/www/.agents/skills/astrologyapi/SKILL.md)
- **Comprehensive Usage Manual (9 Modules)**: [.agents/skills/astrologyapi/references/usage.md](file:///var/www/.agents/skills/astrologyapi/references/usage.md)
- **Infrastructure, Plan Tiers & CoHaLo Guide**: [.agents/skills/astrologyapi/references/infra.md](file:///var/www/.agents/skills/astrologyapi/references/infra.md)

## Integrated Domains Summary

1. **Western Natal & 23 Houses**: `POST /api/v3/western/natal-chart`, `/aspects`.
2. **Multi-Name Core Numerology**: `POST /api/v3/numerology/core-numbers` (5 master pillars).
3. **Hebrew Kabbalah Gematria**: `POST /api/v3/kabbalah/gematria` (4 classical systems).
4. **Hellenistic Timing Suite**: `/api/v3/timing/*` (Profections, Firdaria, Decennials, Zodiacal Releasing, Cazimi, Timeline).
5. **Vedic Jyotish & Drishti**: `POST /api/v3/vedic/birth-details`, `POST /api/v3/vedic/aspects` (Drik Bala matching JHora 8.0).
6. **Horoscope Engine**: `GET /api/v3/horoscope/daily` (12 life areas, 17 languages).
7. **Relocation & ACG Report**: `POST /api/v3/analysis/relocation-report` (World map, parans, Local Space).
8. **Graphic Ephemeris SVG**: `POST /api/v3/render/graphic-ephemeris` (Harmonics 1, 2, 4, 8, 16).
9. **Astrology AI Chat & Horary**: `POST /api/v3/chat`, `/horary/ask`.
