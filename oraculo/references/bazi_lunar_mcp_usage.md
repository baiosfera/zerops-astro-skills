# BaZi Four Pillars & Chinese Lunar MCP Reference Pointer

BaZi & Chinese Lunar calculation engines are now maintained as a sovereign first-class Dual-RAG System Skill in the workspace.

## Primary Documentation Links

- **Main Router**: [.agents/skills/bazi-lunar/SKILL.md](file:///var/www/.agents/skills/bazi-lunar/SKILL.md)
- **Comprehensive Usage Manual (8 Modules)**: [.agents/skills/bazi-lunar/references/usage.md](file:///var/www/.agents/skills/bazi-lunar/references/usage.md)
- **Infrastructure, MCP Connectors & CoHaLo Guide**: [.agents/skills/bazi-lunar/references/infra.md](file:///var/www/.agents/skills/bazi-lunar/references/infra.md)

## Integrated Domains Summary

1. **Four Pillars Structure (四柱八字)**: `getBaziChart`, `calculate_bazi_chart` (60 Jiazi).
2. **True Solar Time Correction (真太阳时)**: Longitude delta + Equation of Time (EOT).
3. **Day Master & Five Elements (日主 & 五行)**: 12 Growth Stages, Wu Xing percentage balance.
4. **Ten Gods & Hidden Stems (十神 & 藏干)**: Main stars, sub-stars, stem allocations.
5. **Earthly Branch Interactions (刑冲合会)**: Liu He, San He, Liu Chong, San Xing, Liu Hai, Liu Po.
6. **10-Year Major Luck Cycles (大运 & 起运)**: Decade pillars and timeline progression.
7. **24 Solar Terms (二十四节气)**: Solar astronomical boundaries for month pillars.
8. **Chinese Almanac & Huangli (老黄历 & 神煞)**: `getHuangli` (Yi/Ji auspicious/inauspicious actions, 28 Mansions, Shen Sha).
