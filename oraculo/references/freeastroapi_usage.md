# FreeAstroAPI Canonical Reference Pointer

FreeAstroAPI is now maintained as a sovereign first-class Dual-RAG System Skill in the workspace.

## Primary Documentation Links

- **Main Router**: [.agents/skills/freeastroapi/SKILL.md](file:///var/www/.agents/skills/freeastroapi/SKILL.md)
- **Comprehensive Usage Manual (9 Modules)**: [.agents/skills/freeastroapi/references/usage.md](file:///var/www/.agents/skills/freeastroapi/references/usage.md)
- **Infrastructure & Environment Guide**: [.agents/skills/freeastroapi/references/infra.md](file:///var/www/.agents/skills/freeastroapi/references/infra.md)

## Integrated Modules Summary

1. **Western Natal & Sidereal**: `POST /api/v1/natal/calculate` (7 house systems, ayanamsas, dominants, stars, declination aspects, `time_known: false`).
2. **Visual Charts SVG/PNG**: `POST /api/v1/natal/chart/` (vector wheels).
3. **Chinese BaZi**: `POST /api/v1/chinese/bazi` (`time_standard: true_solar`, Ten Gods, Yong Shen, Shen Sha, Da Yun luck cycles).
4. **4-in-1 Numerology**: `POST /api/v1/numerology/profile` (Pythagorean, Chaldean, Kabbalah, Ank Jyotish).
5. **Vedic Jyotish & KP V2**: `POST /api/v2/vedic/kp` (12 Placidus cusps, 4-level Sub-Lords, significators).
6. **Astrocartography**: `POST /api/v1/western/astrocartography/lines` (GeoJSON WGS84 lines).
7. **Electional Timing**: `POST /api/v2/western/electional/<category>/search` (contracts, investments, litigation).
8. **Progressions**: `POST /api/v1/western/progressions/*` (secondary, converse, tertiary).
