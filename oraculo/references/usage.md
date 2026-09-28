# Master Astrological APIs & MCP Systems Usage Guide (Dual-RAG SSoT V13.0)

Este manual documenta de forma exhaustiva los contratos técnicos, endpoints REST, servidores MCP y esquemas de payload para la extracción astrológica de alta precisión en Fase 0 bajo la arquitectura de **Sharding por Dominios (*Domain Sharding*)**, **Consenso Canónico**, y la **Tríada Sagrada de Ingestión** (Feed + NotebookLM RAG + Author Persona).

---

## 1. Principios de Gobernanza CoHaLo & Blindaje de Créditos
- **Zero-Waste Single-Pass (Extracción Atómica):** Fase 0 extrae el 100% de la matemática y textos interpretativos en un único pase concurrente al iniciar el diagnóstico.
- **Prohibición de Re-consumo Post-Fase 0:** A partir de la finalización de Fase 0, queda prohibido volver a realizar llamadas a APIs externas de pago (`FreeAstroAPI`, `AstroWay REST`, `Astrology-API.io V3`, `VedAstro PRO`).
- **SSoT Exclusivo en Disco:** Las fases 1 a 11 y todos los sub-oráculos (`oraculo-diag-a-psy` a `oraculo-diag-e-geo`) leen exclusivamente de `/var/www/baiosfera/ASTROLOGÍA/DIAG/<ID>/raw/`.
- **Cero Hardcoding de Claves:** Se leen desde las variables de entorno inyectadas por Zerops (`$FREEASTROAPI_KEY`, `$ASTROLOGY_API_KEY`, `$ASTROWAY_API_KEY`, `$VEDASTRO_API_KEY`, `$NASA_API_KEY`, etc.).
- **Rate-Limits & Circuit Breakers:** Concurrencia estructurada con `asyncio.TaskGroup`, token-bucket por proveedor, reintentos exponenciales acotados (máximo 2) y timeouts estrictos (`timeout 15s` red, `timeout 10s` local):
  - `FreeAstroAPI` (Astro Entry): 4.0 req/s (`sleep 0.25`).
  - `AstroWay REST` (Indie PRO): 0.5 req/s (`sleep 2.5`).
  - `Astrology-API.io V3`: 1.0 req/s (`sleep 1.0`).
  - `VedAstro PRO`: 1.5 req/s (`sleep 0.6`).
  - `HebCal REST`: 2.0 req/s (`sleep 0.5`).
  - `NASA JPL Horizons REST`: 2.0 req/s (`sleep 0.5`).

---

## 2. Arquitectura Unificada del Pipeline Asíncrono (`pipeline/`)

Toda la extracción, validación y consenso se ejecuta en un único proceso en memoria gobernado por [`scripts/omni_engine.py`](file:///var/www/.agents/skills/oraculo/scripts/omni_engine.py) y orquestado mediante [`pipeline/orchestrator.py`](file:///var/www/.agents/skills/oraculo/pipeline/orchestrator.py):

```
[scripts/omni_engine.py] (CLI Facade & Argument Parser)
       │
       ▼
[pipeline/orchestrator.py] (Async Concurrency Supervisor - asyncio.TaskGroup)
       ├──> [pipeline/clients/rest_client.py] (HTTP/2 Connection Pool)
       │      ├── FreeAstroAPI (19 endpoints: Tropical, Sidereal, KP V2, BaZi, Num, ACG, Elections)
       │      ├── AstroWay REST (26 endpoints: 16 Vargas D1-D60, 10 Dashas, Jaimini, Evolutionary)
       │      ├── Astrology-API.io V3 (Core Numerology, Gematria, Houses, Relocation)
       │      ├── VedAstro PRO (Predictions 200+ Yogas/Doshas, AllPlanetData, AllHouseData, DasaAtRange)
       │      ├── NASA JPL Horizons (Asteroides 1-4 Ceres/Pallas/Juno/Vesta, Centauros Chiron/Chariklo, TNOs Eris)
       │      └── HebCal REST (Converter, Zmanim 34 marcas solares, Shabbat, Festividades, Leyning)
       │
       ├──> [pipeline/clients/mcp_client.py] (Typed MCP Client)
       │      ├── lunar MCP (calculate_bazi con birth_datetime, solar_to_lunar, get_moon_phase, fortune)
       │      ├── kundali MCP (kundali con dasha_depth: 2, panchang, muhurat, festivals)
       │      └── zmanim MCP (daily_times: times + times_iso)
       │
       ├──> [pipeline/consensus/] (Canonical Delegations & Ontological Mapping)
       │      ├── chara_karakas.py (Ingestión canónica de AstroWay Jaimini Lahiri)
       │      ├── numerology.py (Consolidación FreeAstroAPI + Astrology-API.io)
       │      ├── tikkun.py (Síntesis Rav Berg enriquecida con Skipped Steps de AstroWay)
       │      └── sefer_yetzirah.py (Mapeo canónico sobre fecha hebrea y gematria)
       │
       └──> [pipeline/sharder/] (Deterministic File Generation)
              ├── 10 Domain Shards JSON (raw/json/dumps/)
              ├── 9 Feeds Quirúrgicos Markdown (raw/feeds/)
              └── 3 Reportes LLM SSoT (raw/llm/) + Astrobranding Semiotics
```

---

## 3. Catálogo de los 9 Motores Canónicos Auditados

### 1. FreeAstroAPI Engine (v1.2)
- **Tropical Placidus**: `/api/v1/natal/calculate` con declinaciones, estrellas fijas y dominantes.
- **Sideral Fagan-Bradley & Lahiri**: `/api/v1/natal/calculate` con Campanus y Whole Sign.
- **Vedic KP V2**: `/api/v2/vedic/kp` con significadores de 4 niveles y sub-lords.
- **BaZi True Solar**: `/api/v1/chinese/bazi` y `/api/v1/chinese/bazi/flow` (Da Yun 90 años).
- **Numerología Multidimensional**: `/api/v1/numerology/profile` (Pitagórica, Caldea, Ank Jyotish, Kabbalah).
- **Astrocartografía**: `/api/v1/western/astrocartography/lines` (`include_crossings: false`).
- **Progresiones**: Secundarias, Terciarias y Conversas.
- **10 Elecciones Comerciales**: `/api/v2/western/electional/*` (contratos, inversiones, alianzas, lanzamientos).

### 2. AstroWay Suite (v1.1)
- **16 Shodashavargas Completos**: `POST /v1/vedic/varga/d1` a `d60` (D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60).
- **10 Sistemas de Dashas**: `POST /v1/vedic/dashas/*` (Vimshottari a 5 niveles, Yogini, Chara, Kalachakra, etc.).
- **Jaimini Canónico**: `POST /v1/vedic/jaimini/chara-karakas` y `/karakas` (AK a DK con Rahu $30^\circ - \lambda$).
- **Astrología Evolutiva**: `POST /v1/evolutionary/nodal-axis-detail` y `/skipped-steps` (cuadraturas al eje nodal).
- **Human Design & Cosmobiología**: `POST /v1/human-design`, `/circuitry`, `/incarnation-cross`, `POST /v1/cosmobiology/dial-90`.
- **Helenística**: `POST /v1/hellenistic/lots-15`, `POST /v1/hellenistic/zr/peak-periods`.

### 3. Astrology-API.io Suite (v1.1)
- **Core Numerology**: `POST /api/v3/numerology/core-numbers` (Life Path, Expression, Soul Urge, Birthday, Personality, Maturity, Karmic Debt 13/14/16/19, Master Numbers 11/22/33).
- **Western Natal 23 Casas**: `POST /api/v3/western/natal-chart`.
- **Kabbalah Gematria**: `POST /api/v3/kabbalah/gematria` (Ragil, Siduri, Katan, Kolel).
- **Timing Timeline**: `POST /api/v3/timing/timeline`.
- **Relocalización**: `POST /api/v3/analysis/relocation`.

### 4. VedAstro PRO Suite (v1.2)
- **HoroscopePredictions**: `GET /api/Calculate/HoroscopePredictions` (200+ yogas y doshas natales con fuentes clásicas verbatim).
- **AllPlanetData & AllHouseData**: `GET /api/Calculate/AllPlanetData` (1.296 métricas) y `AllHouseData` (480 métricas).
- **DasaAtRange**: `GET /api/Calculate/DasaAtRange`.

### 5. NASA JPL Horizons & SBDB (v1.1)
- **Efemérides Geocéntricas**: `https://ssd.jpl.nasa.gov/api/horizons.api` con `EPHEM_TYPE=OBSERVER`, `CENTER=500@399`, `QUANTITIES=1,2,9,31,43`.
- **Catálogo de Cuerpos**:
  * Asteroides Clásicos: `1` (Ceres), `2` (Pallas), `3` (Juno), `4` (Vesta), `433` (Eros).
  * Centauros: `2060` (Chiron), `10199` (Chariklo).
  * TNOs: `136199` (Eris), `90377` (Sedna).

### 6. HebCal Jewish Calendar Suite (v1.1)
- **Conversor de Fechas**: `GET https://www.hebcal.com/converter?cfg=json&gy=<Y>&gm=<M>&gd=<D>&g2h=1`.
- **Zmanim Halájicos Solares**: `GET https://www.hebcal.com/zmanim?cfg=json&latitude=<LAT>&longitude=<LNG>&tzid=<TZ>&date=<DATE>&sec=1` (34 marcas solares NOAA).
- **Shabbat & Havdalah**: `GET https://www.hebcal.com/shabbat?cfg=json&latitude=<LAT>&longitude=<LNG>&tzid=<TZ>&m=on`.
- **Festividades & Omer**: `GET https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&min=on&mod=on&nx=on&mf=on&ss=on&c=on`.
- **Leyning (Lecturas de Torá)**: `GET https://www.hebcal.com/leyning?cfg=json&date=<DATE>`.

### 7. BaZi & Chinese Lunar Suite (v1.1)
- **calculate_bazi**: `birth_datetime` (`"YYYY-MM-DD HH:MM"`), `timezone_offset`.
- **solar_to_lunar**: `solar_date` (`"YYYY-MM-DD"`).
- **get_moon_phase**: `date`, `location`.
- **get_daily_fortune**: `date`, `zodiac`.

### 8. Kundali Jyotish Suite (v1.1)
- **kundali**: `birth_datetime`, `latitude`, `longitude`, `school=parashari`, `locale=en`, `ayanamsa=lahiri`, `dasha_depth: 2`.
- **panchang**: `date`, `latitude`, `longitude`, `timezone`.
- **muhurat**: `date`, `latitude`, `longitude`, `event_type=general_auspicious`.
- **festivals**: `start_date`, `end_date`.

### 9. Zmanim Halachic Solar Suite (v1.1)
- **zmanim_get_daily_times**: `location`, `latitude`, `longitude`, `time_zone`, `date`, `response_format=json`.
- Extrae ambos bloques: `times` (formato HH:MM:SS) y `times_iso` (marcas ISO 8601 con zona horaria).

---

## 4. Estructura de Salida SSoT (10 Shards & 9 Feeds)

### Los 10 Shards Canónicos (`raw/json/dumps/`):
1. `01_numerology_multi.json`: Pitagórica, Caldea, Ank Jyotish, Gematria (Astrology-API.io + FreeAstroAPI).
2. `02_western_tropical.json`: Placidus Tropical, 23 Casas, Sabian Symbols, Progresiones Sec/Ter/Converse.
3. `03_western_sidereal.json`: Fagan-Bradley Campanus, Casas Siderales de Astrology-API.io.
4. `04_vedic_jyotish_kp.json`: Lahiri Whole Sign, KP V2, Kundali MCP, VedAstro Predictions + AllPlanet + AllHouse, AstroWay 16 Vargas D1-D60 + Dashas.
5. `05_bazi_chinese_lunar.json`: BaZi True Solar, Da Yun Flow, AstroWay Four Pillars, Lunar MCP.
6. `06_human_design.json`: BodyGraph completo, Circuitry, Incarnation Cross, PHS Sensitivity.
7. `07_kabbalah_hermetic.json`: HebCal Converter, HebCal Zmanim, Zmanim MCP (`times` + `times_iso`), Gematria, Sefer Yetzirah, Tikkun Nodal enriquecido con Skipped Steps.
8. `08_timing_dashas_timelords.json`: Timeline Aggregator (Profecciones, Firdaria, Decennials, ZR), Vimshottari Dashas a 5 niveles, 10 Elecciones Comerciales.
9. `09_geo_acg_relocation.json`: ACG Lines (FreeAstroAPI + AstroWay), Best Places, Relocalización.
10. `10_cosmobiology_hellenistic_nasa.json`: Dial 90°, 15 Lots de Chris Brennan, ZR Peak Periods, Efemérides de Asteroides y Centauros de NASA Horizons (Ceres, Chiron, Pallas, Juno, Vesta, Eris).

### Los 9 Feeds Quirúrgicos Markdown (< 2.5 KB en `raw/feeds/`):
- `feed_fase1_num.md`: Matriz numerológica personal y comercial.
- `feed_fase2_occ.md`: Sol, Luna, ASC, MC y balance elemental tropical.
- `feed_fase3_sid.md`: Contraste ontológico Tropical vs. Sideral Fagan-Bradley.
- `feed_fase4_ved.md`: Lagna, Nakshatra, Deidad, Shakti, D9, D10 y Shadbala.
- `feed_fase5_bazi.md`: Cuatro Pilares (60 Jiazi), Day Master, Yong Shen y 5 Elementos.
- `feed_fase6_kab.md`: Calendario Hebreo, Sefer Yetzirah, Tikkun Nodal y Zmanim.
- `feed_fase7_voc.md`: Clímax de carrera (MC, D10, Human Design, roles comerciales).
- `feed_fase8_time.md`: Reloj temporal T0 (Pináculo activo, Da Yun activo, Dasha activa).
- `feed_fase9_end.md`: Horizontes estratégicos, 4 tracks de mentoría y sesión 1:1.

---

## 5. Mapeo de Dominios para Sub-Oráculos
- [`oraculo-diag-a-psy`](file:///var/www/.agents/skills/oraculo-diag-a-psy/SKILL.md): `02_western_tropical.json`, `06_human_design.json`, `10_cosmobiology_hellenistic_nasa.json`.
- [`oraculo-diag-b-voc`](file:///var/www/.agents/skills/oraculo-diag-b-voc/SKILL.md): `04_vedic_jyotish_kp.json`, `05_bazi_chinese_lunar.json`, `feed_fase7_voc.md`.
- [`oraculo-diag-c-mkt`](file:///var/www/.agents/skills/oraculo-diag-c-mkt/SKILL.md): `08_timing_dashas_timelords.json`, `feed_fase8_time.md`.
- [`oraculo-diag-d-leg`](file:///var/www/.agents/skills/oraculo-diag-d-leg/SKILL.md): `04_vedic_jyotish_kp.json` (D30/D60), `07_kabbalah_hermetic.json`.
- [`oraculo-diag-e-geo`](file:///var/www/.agents/skills/oraculo-diag-e-geo/SKILL.md): `09_geo_acg_relocation.json`.
- [`orchesbrand`](file:///var/www/.agents/skills/orchesbrand/SKILL.md): `brand/astrobranding_semiotics.md`, `01_numerology_multi.json`.
