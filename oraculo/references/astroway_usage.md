# AstroWay REST Engine Canonical Reference Pointer (SOTA 2026)

AstroWay is maintained as a sovereign first-class Dual-RAG System Skill in the workspace (`.agents/skills/astroway/`). Under the unified architectural governance of Oráculo v12.0, AstroWay is utilized exclusively through its high-performance **REST API** (`https://api.astroway.info/v1/`) under the **Indie PRO** plan (50,000 credits/month quota).

## Primary Documentation Links

- **Main Router**: [.agents/skills/astroway/SKILL.md](file:///var/www/.agents/skills/astroway/SKILL.md)
- **Comprehensive Usage Manual**: [.agents/skills/astroway/references/usage.md](file:///var/www/.agents/skills/astroway/references/usage.md)
- **Infrastructure, Plan Tiers & Rate Limits Guide**: [.agents/skills/astroway/references/infra.md](file:///var/www/.agents/skills/astroway/references/infra.md)
- **Epistemic Integration Reference**: [.agents/skills/astroway/references/usage.md](file:///var/www/.agents/skills/astroway/references/usage.md)

## Integrated REST Endpoints in Oráculo

1. **Western Natal Chart**: `POST /v1/chart` (Swiss Ephemeris topocentric positions).
2. **Sabian Symbols (Rudhyar 360°)**: `POST /v1/aspects/sabian-symbols` (Degree-by-degree archetypal symbols).
3. **Founder Business Archetypes**: `POST /v1/business/founder-personality` & `POST /v1/business/leadership-style`.
4. **Human Design System**: `POST /v1/human-design`, `POST /v1/hd/circuitry`, `POST /v1/hd/incarnation-cross`.
5. **Chinese BaZi**: `POST /v1/bazi/four-pillars` (Four Pillars sexagesimal 60-Jiazi).
6. **Vedic Vargas**: `POST /v1/vedic/varga/d1`, `/d9`, `/d10`, `/d60`.
7. **Shadbala (6-Factor Total)**: `POST /v1/vedic/shadbala/full`.
8. **Vimshottari Dashas**: `POST /v1/vedic/dashas/vimshottari/maha`.
9. **Astrocartography**: `POST /v1/acg` & `POST /v1/acg/best-places`.
10. **Cosmobiology & Hellenistic**: `POST /v1/cosmobiology/dial-90`, `POST /v1/hellenistic/lots-15`, `POST /v1/hellenistic/zr/peak-periods`.

## Financial Audit & Rate Limit Shield

- **Authentication**: `X-Api-Key: $ASTROWAY_API_KEY`
- **Rate Limit**: 30 requests/minute (`sleep 2.5` throttle).
- **Quota Tracking**: Headers `X-Credits-Used` and `X-Credits-Remaining` captured in real time by `omni_curl_dumper.sh`.
