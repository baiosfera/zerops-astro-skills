# VedAstro PRO (REST & MCP) Canonical Reference Pointer

VedAstro is now maintained as a sovereign first-class Dual-RAG System Skill in the workspace.

## Primary Documentation Links

- **Main Router**: [.agents/skills/vedastro/SKILL.md](file:///var/www/.agents/skills/vedastro/SKILL.md)
- **Comprehensive Usage Manual (8 Modules)**: [.agents/skills/vedastro/references/usage.md](file:///var/www/.agents/skills/vedastro/references/usage.md)
- **Infrastructure, PRO Tier & CoHaLo Guide**: [.agents/skills/vedastro/references/infra.md](file:///var/www/.agents/skills/vedastro/references/infra.md)

## Integrated Domains Summary

1. **Horoscope Predictions (200+ Yogas & Doshas)**: `POST /api/Calculate/HoroscopePredictions`.
2. **All Planet Data & Ephemeris**: `POST /api/Calculate/AllPlanetData`.
3. **All Easy Astrology Summary**: `POST /api/Calculate/AllEasyAstrology`.
4. **Vimshottari Dashas at Range (5 Levels)**: `GET /api/Calculate/DasaAtRange/...` (Maha through PranaDasha).
5. **Match Report & 16 Kutas Compatibility**: `POST /api/Calculate/MatchReport`.
6. **Ashtakavarga Matrix**: `POST /api/Calculate/Ashtakvarga`.
7. **Classical Vedic Texts RAG Search**: `GET /api/Calculate/SearchSourceText/...` (BV Raman, BPHS).
8. **South & North Indian Kundli SVG Visuals**: `GET /api/Calculate/SouthIndianChart/...`, `NorthIndianChart/...`.
