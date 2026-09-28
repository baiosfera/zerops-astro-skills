# FreeAstroAPI Comprehensive Technical Usage Manual (v1.3)

Unified reference manual for all calculation, metaphysical, chart rendering, astrocartography, progressions, and electional timing endpoints provided by FreeAstroAPI (`https://api.freeastroapi.com/api/`).

---

## 1. Global Authentication, Headers & Network Discipline

All requests require authentication via the `x-api-key` HTTP header. Authenticated mutation/calculation requests accept the optional `Idempotency-Key` header with a client-generated UUID to prevent duplicate quota consumption during retries.

```bash
# Standard Request Headers Template
curl -s -X POST "https://api.freeastroapi.com/api/v1/natal/calculate" \
  -H "x-api-key: $FREEASTRO_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept-Encoding: br, gzip" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{ ... }'
```

### Rate Limit Policy & Account Tier
- **Free Tier**: 80 requests/day, 1 req/sec (`sleep 1.2` throttle).
- **Astro Entry Plan ($8 USD/mo)**: 50,000 requests/month, 5 req/sec concurrency. Automated batch scripts MUST enforce `sleep 0.25` between consecutive requests (4 req/s = 80% capacity limit for zero 429 risk). Includes 2 full branded PDF report credits (8,000–9,000 words).
- **High Plan ($40 USD/mo)**: 500,000 requests/month, 10 req/sec concurrency (`sleep 0.1` throttle). Required for Astrocartography latitude crossings (`include_crossings: true`).

### Two-Tier Storage & Token Economy Architecture (CoHaLo)
- **Tier 1 (Raw Persistence)**: Full-depth JSON responses from API calls are persisted to disk at `raw/json/dumps/` for offline auditability and multi-model downstream tasks.
- **Tier 2 (Agent Feed Extraction)**: Only extracted, domain-specific metrics are curated into typed XML snippets (<2.5 KB) in `raw/feeds/`, strictly preserving LLM context window tokens and preventing cache thrashing.

---

## 2. Module 1: Western Natal & Deep Insights (`/api/v1/natal/calculate`)

Calculates exact planetary positions, house cusps, major/minor aspects, declination parallels, dominants profile, fixed stars, and chart signatures.

### Endpoint
`POST https://api.freeastroapi.com/api/v1/natal/calculate`

### Canonical Client-Agnostic Request
```json
{
  "name": "<CONSULTANT_NAME>",
  "year": <YYYY>,
  "month": <MM>,
  "day": <DD>,
  "hour": <HH>,
  "minute": <MN>,
  "lat": <FLOAT_LATITUDE>,
  "lng": <FLOAT_LONGITUDE>,
  "tz_str": "<IANA_TIMEZONE>",
  "house_system": "placidus",
  "zodiac_type": "tropical",
  "fixed_stars": ["royal_4", "behenian_20"],
  "dominants_method": "modern",
  "include_declination_aspects": true,
  "time_known": true
}
```

### Zero-Hour Failsafe (Untimed Birth Mode)
When the exact birth time is unknown, pass `"time_known": false`. Houses and angles are safely omitted to prevent false ascendant/cusp derivations:
```json
{
  "name": "<CONSULTANT_NAME>",
  "year": <YYYY>,
  "month": <MM>,
  "day": <DD>,
  "time_known": false,
  "lat": <FLOAT_LATITUDE>,
  "lng": <FLOAT_LONGITUDE>,
  "tz_str": "<IANA_TIMEZONE>",
  "zodiac_type": "tropical"
}
```

### Key Parameters Table
| Parameter | Type | Default | Description |
|---|---|---|---|
| `house_system` | `string` | `"placidus"` | `"placidus"`, `"whole_sign"`, `"equal"`, `"koch"`, `"regiomontanus"`, `"porphyry"`, `"campanus"` |
| `zodiac_type` | `string` | `"tropical"` | `"tropical"` or `"sidereal"` (combined with `sidereal_ayanamsa`) |
| `sidereal_ayanamsa` | `string` | `"lahiri"` | `"lahiri"`, `"fagan_bradley"`, `"raman"`, `"krishnamurti"`, `"deluce"`, `"true_citra"` |
| `fixed_stars` | `array[str]`| `[]` | Pack IDs (`"royal_4"`, `"behenian_20"`), individual names (`"Spica"`), or `["all"]` |
| `dominants_method` | `string` | `null` | `"modern"` or `"traditional"`. Returns weighted element, mode, and planet dominance |
| `include_declination_aspects` | `boolean` | `false` | Returns parallels and contra-parallels with orb <= 1.0° |

### Specialized Psychological Insights & Sign Endpoints
- `POST /api/v1/western/natal/insights`: Deep archetypal interpretations grouped by life sectors.
- `POST /api/v1/western/signs/sun`: Solar identity and archetype analysis.
- `POST /api/v1/western/signs/moon`: Lunar emotional core and subconscious security needs.
- `POST /api/v1/western/signs/rising`: Ascendant physical persona, style, and interface to the world.
- `POST /api/v1/western/signs/midheaven`: Midheaven (MC) vocation, public reputation, and legacy.

---

## 3. Module 2: Visual Vector Charts SVG/PNG

Renders crisp, publication-ready SVG and PNG chart wheels directly from ephemeris data.

### Endpoints
- **Natal Chart Wheel**: `POST https://api.freeastroapi.com/api/v1/natal/chart/`
- **Composite Chart Wheel**: `POST https://api.freeastroapi.com/api/v1/natal/chart/composite`
- **Solar Return Wheel**: `POST https://api.freeastroapi.com/api/v1/natal/chart/solar-return`
- **Synastry Bi-Wheel**: `POST https://api.freeastroapi.com/api/v1/natal/chart/synastry`
- **Transits Bi-Wheel**: `POST https://api.freeastroapi.com/api/v1/natal/chart/transits`
- **Kerykeion Classic Style**: `POST https://api.freeastroapi.com/api/v1/svg/kerykeion`
- **Vedic Regional Visual Chart**: `POST https://api.freeastroapi.com/api/v2/vedic/visual/chart`
- **Vedic KP Wheel & Tables**: `POST https://api.freeastroapi.com/api/v2/vedic/kp/render`

### Curl Example (Natal SVG Wheel)
```bash
curl -s -X POST "https://api.freeastroapi.com/api/v1/natal/chart/" \
  -H "x-api-key: $FREEASTRO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "year": <YYYY>,
    "month": <MM>,
    "day": <DD>,
    "hour": <HH>,
    "minute": <MN>,
    "lat": <FLOAT_LATITUDE>,
    "lng": <FLOAT_LONGITUDE>,
    "tz_str": "<IANA_TIMEZONE>",
    "theme": "dark",
    "format": "svg",
    "chart_type": "natal",
    "custom_width": 1000
  }' > chart.svg
```

---

## 4. Module 3: Western Synastry & Relationship Dynamics

Comprehensive relationship affinity, cross-aspect matrices, house overlays, and celebrity comparisons.

### Endpoints
- `POST /api/v1/western/synastry` & `POST /api/v2/western/synastry`: Core aspect grid and house overlays.
- `POST /api/v1/western/synastry/horoscope` & `POST /api/v2/western/synastry/horoscope`: Relational forecast.
- `POST /api/v1/western/synastry/simplified`: High-level compatibility indicators.
- `POST /api/v1/western/synastry/summary`: Executive psychological and elemental harmony scores.
- `POST /api/v1/western/synastrycards`: Formatted synastry summary cards.
- `POST /api/v2/western/chart-similarity/famous-people`: Harmonic natal resonance with historical figures.

### Canonical Request Payload
```json
{
  "chart1": {
    "name": "<PERSON_A>",
    "year": <YYYY_A>,
    "month": <MM_A>,
    "day": <DD_A>,
    "hour": <HH_A>,
    "minute": <MN_A>,
    "lat": <LAT_A>,
    "lng": <LNG_A>,
    "tz_str": "<TZ_A>"
  },
  "chart2": {
    "name": "<PERSON_B>",
    "year": <YYYY_B>,
    "month": <MM_B>,
    "day": <DD_B>,
    "hour": <HH_B>,
    "minute": <MN_B>,
    "lat": <LAT_B>,
    "lng": <LNG_B>,
    "tz_str": "<TZ_B>"
  },
  "house_system": "placidus"
}
```

---

## 5. Module 4: Western Transits, Returns & Solar Cycles

Temporal unfolded planetary movements and exact planetary return moments.

> **Tier Boundary Notice**: Continuous timeline endpoints (`/api/v1/western/transits/timeline` and `/transits/search`) scan long windows and require the High plan ($40/mo). On the **Entry plan ($8/mo)**, use instant snapshot calculations via `POST /api/v1/transits/calculate` (requires `current_city`) or Solar/Planetary Returns.

### Endpoints
- `POST /api/v1/transits/calculate`: Active transits to natal positions on a specific date (Entry compliant).
- `POST /api/v1/western/transits/insights`: Narrative interpretation of current transit activations.
- `POST /api/v1/western/transits/search`: Scans a date window for exact aspect hits (High plan required).
- `POST /api/v1/western/transits/timeline`: Chronological transit aspect timeline (High plan required).
- `POST /api/v1/western/returns/calculate`: Returns for any planet (Solar, Lunar, Saturn Return, Jupiter Return, etc.).
- `POST /api/v1/western/solar/calculate`: Solar return chart with exact relocation coordinates.

### Canonical Transits Calculate Request (Entry Plan Compliant)
```json
{
  "natal": {
    "year": <YYYY>,
    "month": <MM>,
    "day": <DD>,
    "hour": <HH>,
    "minute": <MN>,
    "lat": <BIRTH_LAT>,
    "lng": <BIRTH_LNG>,
    "tz_str": "<BIRTH_TZ>"
  },
  "current_city": "<CURRENT_LOCATION_CITY>",
  "transit_datetime": "<YYYY-MM-DDTHH:MM:SSZ>"
}
```

### Canonical Solar Return Request (Strict Pydantic Nested Schema)
```json
{
  "natal": {
    "name": "<CONSULTANT_NAME>",
    "datetime": "<YYYY-MM-DDTHH:MM:SS-05:00>",
    "location": {
      "city": "<BIRTH_CITY>",
      "latitude": <BIRTH_LAT>,
      "longitude": <BIRTH_LNG>,
      "timezone": "<BIRTH_TZ>"
    }
  },
  "solar_return": {
    "year": <TARGET_RETURN_YEAR>,
    "location": {
      "city": "<RELOCATED_CITY>",
      "latitude": <RELOCATED_LAT>,
      "longitude": <RELOCATED_LNG>,
      "timezone": "<RELOCATED_TZ>"
    }
  }
}
```

---

## 6. Module 5: Western Primary Directions & Annual Profections

Classical predictive astrology and traditional time lords.

### Endpoints
- `POST /api/v1/western/directions/primary`: Primary directions using Ptolemaic, Naibod, or Placidean keys.
- `POST /api/v1/western/directions/primary/calendar`: Calendar of directional arc completions.
- `POST /api/v1/western/directions/primary/exact-aspects`: Exact promisor-significator contacts.
- `POST /api/v1/western/directions/primary/search`: Directional aspect scanning.
- `POST /api/v1/western/profections/annual`: Hellenistic annual profections identifying the Lord of the Year, profected house, and activated natal planets.

### Canonical Annual Profections Request (Pydantic-Strict)
```json
{
  "year": <YYYY>,
  "month": <MM>,
  "day": <DD>,
  "hour": <HH>,
  "minute": <MN>,
  "city": "<BIRTH_CITY>",
  "annual_profection": {
    "year": <TARGET_PROFECTION_YEAR>
  }
}
```

---

## 7. Module 6: Western Progressions — 5 Distinct Systems (20 Endpoints)

Full progression unfolding across 5 classical and modern progression frameworks:
1. **Secondary Progressions** (Major progression: 1 solar day = 1 solar year):
   - `POST /api/v1/western/progressions/secondary`
   - `POST /api/v1/western/progressions/secondary/calendar`
   - `POST /api/v1/western/progressions/secondary/exact-aspects`
   - `POST /api/v1/western/progressions/secondary/exact-ingresses`
2. **Tertiary Progressions** (1 solar day = 1 tropical lunar month):
   - `POST /api/v1/western/progressions/tertiary`
   - `POST /api/v1/western/progressions/tertiary/calendar`
   - `POST /api/v1/western/progressions/tertiary/exact-aspects`
   - `POST /api/v1/western/progressions/tertiary/exact-ingresses`
3. **Converse Secondary Progressions** (Regressive progression backwards in time):
   - `POST /api/v1/western/progressions/converse-secondary`
   - `POST /api/v1/western/progressions/converse-secondary/calendar`
   - `POST /api/v1/western/progressions/converse-secondary/exact-aspects`
   - `POST /api/v1/western/progressions/converse-secondary/exact-ingresses`
4. **Quaternary Progressions** (Minor progression: 1 sidereal day = 1 sidereal year):
   - `POST /api/v1/western/progressions/quaternary`
   - `POST /api/v1/western/progressions/quaternary/calendar`
   - `POST /api/v1/western/progressions/quaternary/exact-aspects`
   - `POST /api/v1/western/progressions/quaternary/exact-ingresses`
5. **Quotidian Progressions** (Daily rotated house cusps based on secondary sun):
   - `POST /api/v1/western/progressions/quotidian`
   - `POST /api/v1/western/progressions/quotidian/calendar`
   - `POST /api/v1/western/progressions/quotidian/exact-aspects`
   - `POST /api/v1/western/progressions/quotidian/exact-ingresses`

### Canonical Progression Payload
> **Pydantic Validation Requirement**: `natal.location.city` is strictly required. Each system expects its own target block (`secondary_progression`, `tertiary_progression`, etc.).

```json
{
  "natal": {
    "name": "<CONSULTANT_NAME>",
    "datetime": "<ISO_DATETIME_WITH_OFFSET>",
    "time_known": true,
    "location": {
      "city": "<BIRTH_CITY>",
      "latitude": <FLOAT_LATITUDE>,
      "longitude": <FLOAT_LONGITUDE>,
      "timezone": "<IANA_TIMEZONE>"
    }
  },
  "secondary_progression": {
    "target_date": "<TARGET_YYYY-MM-DD>"
  }
}
```

---

## 8. Module 7: Western Astrocartography & Relocation

World cartography of planetary angular lines and geographical relocation.

### Endpoints
- `POST /api/v1/western/astrocartography/lines`: Global GeoJSON `LineString`/`MultiLineString` angular paths.
- `POST /api/v1/western/astrocartography/city-check`: Distance and orb assessment to planetary lines for a specific city.
- `POST /api/v1/western/astrocartography/parans`: Latitudinal intersection points (parans) across the globe.
- `POST /api/v1/western/astrocartography/recommendations`: Algorithmic suggestion of best world cities by theme.
- `POST /api/v1/western/astrocartography/relocation`: Relocated chart calculation.

### Canonical ACG Request (Entry Tier Compliant)
> **Account Tier Hard Boundary**: `include_crossings: false` is strictly required on Entry ($8 USD) and Free plans. Setting `include_crossings: true` produces `HTTP 403 high_plan_required`.

```json
{
  "natal": {
    "year": <YYYY>,
    "month": <MM>,
    "day": <DD>,
    "hour": <HH>,
    "minute": <MN>,
    "lat": <FLOAT_LATITUDE>,
    "lng": <FLOAT_LONGITUDE>,
    "tz_str": "<IANA_TIMEZONE>"
  },
  "mode": "in_mundo",
  "bodies": ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"],
  "angles": ["asc", "dsc", "mc", "ic"],
  "include_crossings": false
}
```

---

## 9. Module 8: Western Commercial Electional Astrology (10 Categories)

Scans continuous search windows to discover optimal planetary configurations for commercial and personal endeavors.

### Complete Category Routes
1. `POST /api/v2/western/electional/making-contracts/search`: Corporate agreements, commercial contracts, partnerships.
2. `POST /api/v2/western/electional/invest-money/search`: Capital allocation, stock purchases, investments.
3. `POST /api/v2/western/electional/legal-proceedings/search`: Filing lawsuits, legal negotiations, arbitration.
4. `POST /api/v2/western/electional/job-audition/search`: Job interviews, pitches, career auditions.
5. `POST /api/v2/western/electional/purchase-property/search`: Real estate acquisitions, land deeds.
6. `POST /api/v2/western/electional/purchase-car/search`: Vehicle purchases, transport machinery.
7. `POST /api/v2/western/electional/move-into-new-home/search`: Relocation, home moves, domestic changes.
8. `POST /api/v2/western/electional/wedding/search`: Marriage ceremonies, civil unions.
9. `POST /api/v2/western/electional/starting-journey/search`: Travel departures, international expeditions.
10. `POST /api/v2/western/electional/physical-examination/search`: Elective health checkups and procedures.

### Canonical Electional Request
> **Pydantic Validation Requirement**: Root `lat`, `lng`, `tz_str`, `search_window: {start, end, step_minutes}`, and `principal_natal` (flat year, month, day, hour, minute, lat, lng, tz_str) are mandatory. Passing `natal: {datetime}` triggers `HTTP 422 Unprocessable Entity`.

```json
{
  "search_window": {
    "start": "<START_ISO_DATETIME_Z>",
    "end": "<END_ISO_DATETIME_Z>",
    "step_minutes": 60
  },
  "lat": <FLOAT_LATITUDE>,
  "lng": <FLOAT_LONGITUDE>,
  "tz_str": "<IANA_TIMEZONE>",
  "principal_natal": {
    "year": <YYYY>,
    "month": <MM>,
    "day": <DD>,
    "hour": <HH>,
    "minute": <MN>,
    "lat": <FLOAT_LATITUDE>,
    "lng": <FLOAT_LONGITUDE>,
    "tz_str": "<IANA_TIMEZONE>"
  },
  "max_results": 5
}
```

---

## 10. Module 9: Chinese BaZi & Four Pillars Engine

Four Pillars metaphysics, 10-year Da Yun luck cycles, and classical TCM Huangdi Neijing analysis.

### Endpoints
- `POST /api/v1/chinese/bazi`: Four Pillars calculation with mandatory True Solar Time.
- `POST /api/v1/chinese/bazi/flow`: Da Yun 10-year luck cycles (ages 0 to 90), annual and monthly pillars.
- `POST /api/v1/chinese/bazi/health`: TCM 5 elements organ constitution, temperature/moisture indexes, and health tendencies.
- `POST /api/v1/chinese/bazi/lifespan`: Neijing life curve (balance of Jing, Qi, and Shen) with cultivation factor.
- `POST /api/v1/chinese/bazi/synastry`: BaZi 5-layer relationship compatibility and element balance.
- `POST /api/v1/chinese/bazi/time-correction`: Solar time offset and equation of time calculator.
- `GET /api/v1/chinese/bazi/dictionary`: Dictionary of 10 Gods, stars, clashes, and combinations.
- `GET /api/v1/chinese/calendar/{date}`: Traditional Chinese lunar calendar (Huangli) for any date.
- `GET /api/v1/chinese/today`: Daily pillars, lunar mansion, and lucky hours.

### Canonical Professional BaZi Request
```json
{
  "year": <YYYY>,
  "month": <MM>,
  "day": <DD>,
  "hour": <HH>,
  "minute": <MN>,
  "lat": <FLOAT_LATITUDE>,
  "lng": <FLOAT_LONGITUDE>,
  "tz_str": "<IANA_TIMEZONE>",
  "sex": "<M_OR_F>",
  "time_standard": "true_solar",
  "include_ten_gods": true,
  "include_pinyin": true,
  "include_stars": true,
  "include_interactions": true,
  "include_professional": true,
  "include_current_flow": true
}
```

### TCM Health Analysis Request (`POST /api/v1/chinese/bazi/health`)
Evaluates constitutional organ balance according to the *Huangdi Neijing* (黄帝内经):
```json
{
  "year": 1990,
  "month": 5,
  "day": 15,
  "hour": 12,
  "minute": 0,
  "lat": 6.25,
  "lng": -75.56,
  "tz_str": "America/Bogota",
  "sex": "M",
  "time_standard": "true_solar",
  "include_timing": true,
  "timing_years_ahead": 10
}
```
**Scoring Architecture:**
- **Raw Base (200 pts):** Celestial Stems (20 pts), Earthly Branches (20 pts), Hidden Stems (*Cang Gan* weighted 60-100%, 30%, 10% up to 10 pts).
- **Seasonal Multipliers:** Modulated by birth month branch (e.g. Summer: Fire ×1.2–1.5, Metal ×0.5–0.7; Winter: Water ×1.2–1.5, Fire ×0.4–0.5).
- **Thermal Index (-1.0 to +1.0):** Fire (+1.0), Wood (+0.2), Earth (0.0), Metal (-0.3), Water (-0.8). $>+0.25 \to$ Hot; $<-0.25 \to$ Cold.
- **Moisture Index (-1.0 to +1.0):** Water (+0.8), Earth (+0.5), Wood (+0.3), Metal (-0.5), Fire (-0.8). $>+0.20 \to$ Damp; $<-0.20 \to$ Dry.
- **Strain Index (Da Yun):** Tracks stress risk on vulnerable organs during unfavorable 10-year luck pillars.

### Neijing Lifespan Simulation Request (`POST /api/v1/chinese/bazi/lifespan`)
Stochastic annual simulation (0 to `max_age` years) based on Jing-Qi-Shen bioenergetics:
```json
{
  "year": 1990,
  "month": 5,
  "day": 15,
  "hour": 12,
  "minute": 0,
  "lat": 6.25,
  "lng": -75.56,
  "tz_str": "America/Bogota",
  "sex": "M",
  "time_standard": "true_solar",
  "max_age": 100,
  "cultivation_factor": 0.75
}
```
- `cultivation_factor` (0.0 to 1.0): Internal alchemy / Neigong preservation factor.
- Returns: `j0`/`j_final` (Jing vitality), `jing_prenatal` vs `jing_postnatal`, `qi_pre_heaven`, `qi_post_heaven`, `shen` spirit balance, and biometrics: S (Stability), D (Depletion), V (Vitality), H (Harmony).

### BaZi Synastry 5-Layer Weighting (`POST /api/v1/chinese/bazi/synastry`)
1. **Day Master Reciprocity (25%):** Stem combination *He* (+95 pts), Production *Sheng* (+85 pts), Clash *Chong* (40 pts).
2. **Spouse Palace / Ri Zhi (20%):** Six Harmonies *Liu He* (+15 pts), Penalty *Xing* (-12 pts), Clash *Chong* (-15 pts).
3. **Four Pillars Alignment (30%):** Day (40%), Month (30%), Hour (20%), Year (10%).
4. **Useful God / Yong Shen Complementarity (15%):** Fills missing elements (+15 pts).
5. **Hidden Stems / Cang Gan Karmic Bonds (10%):** Magnetic attraction between hidden roots.

### Professional Response Structure
When `"include_professional": true` is passed, the response includes the `professional` object:
- `dm_strength`: `"Weak"` or `"Strong"`, with `dm_strength_score` and `balance_ratio`.
- `structure`: Main BaZi structure (e.g. `"Direct Officer Structure"`, `"Indirect Wealth"`).
- `yong_shen_candidates`: Recommended Useful God elements (e.g. `["Water", "Metal"]`).
- `favorable_elements` & `unfavorable_elements`.
- `season_reason`: Seasonal rationale based on birth month branch.
- `stars`: Shen Sha stars with `xun_kong` (empty branch / Kong Wang detection).
- `current_year_triggers`: Real-time interactions with the current year pillar (clashes, combinations, harms).

---

## 11. Module 10: Vedic Jyotish Classical & KP V2 (38 Endpoints)

High-precision Vedic astrology covering classical Parashara and Krishnamurti Paddhati (KP).

### Key Endpoints
- **KP V2 Engine**: `POST /api/v2/vedic/kp`
- **KP Visual Chart**: `POST /api/v2/vedic/kp/render`
- **Parashari Full Chart**: `POST /api/v1/vedic/calculate` & `POST /api/v2/vedic/calculate`
- **Divisional Charts (Vargas D1-D60)**: `POST /api/v1/vedic/vargas` & `POST /api/v2/vedic/vargas`
- **Vimshottari Dashas**: `POST /api/v1/vedic/dasha` & `POST /api/v2/vedic/dasha`
- **Shadbala & Strengths**: `POST /api/v1/vedic/strength` & `POST /api/v2/vedic/strength` (6-factor Shadbala and Bhavabala)
- **Classical Yogas**: `POST /api/v1/vedic/yogas` & `POST /api/v2/vedic/yogas` (Raja, Dhana, Gajakesari, etc.)
- **Gochar Transits**: `POST /api/v1/vedic/gochar/timeline` & `/insights`
- **Compatibility**: `POST /api/v1/vedic/match` & `POST /api/v2/vedic/match` (Ashtakoota 36 Gunas, Manglik Dosha)
- **Panchang**: `POST /api/v1/vedic/panchang` & `POST /api/v2/vedic/panchang` (Tithi, Vara, Nakshatra, Yoga, Karana)
- **Muhurat Search**: `POST /api/v2/vedic/muhurat/search` & `POST /api/v2/vedic/muhurat/personalized-search`

### Shodashavarga Divisional Charts Request (`POST /api/v1/vedic/vargas`)
```json
{
  "year": 1990,
  "month": 5,
  "day": 15,
  "hour": 12,
  "minute": 0,
  "lat": 6.25,
  "lng": -75.56,
  "tz_str": "America/Bogota",
  "ayanamsha": "lahiri",
  "divisions": [1, 2, 3, 4, 5, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60]
}
```

### Muhurat Window Search Request (`POST /api/v2/vedic/muhurat/search`)
Algorithmic electional window search evaluating Tithi, Nakshatra, Yoga, Karana, and Lagna while auditing **Rahu Kaal**, **Bhadra**, and **Panchak** restrictions:
```json
{
  "purpose": "vehicle_purchase",
  "start_date": "2026-10-01",
  "end_date": "2026-10-31",
  "lat": 6.25,
  "lng": -75.56,
  "ayanamsha": "lahiri",
  "limit": 5
}
```
*Supported purposes:* `general_work`, `vehicle_purchase`, `property_purchase`, `griha_pravesh` (new home), `namkaran` (naming/brand launch), `mundan` (first haircut).

### Canonical KP V2 Request
```json
{
  "year": <YYYY>,
  "month": <MM>,
  "day": <DD>,
  "hour": <HH>,
  "minute": <MN>,
  "second": 0,
  "lat": <FLOAT_LATITUDE>,
  "lng": <FLOAT_LONGITUDE>,
  "tz_str": "<IANA_TIMEZONE>",
  "ayanamsha": "kp",
  "house_system": "placidus",
  "node_type": "mean",
  "reference_date": "<REFERENCE_YYYY-MM-DD>",
  "dasha_levels": 3
}
```

### KP Four-Level Significator Hierarchy
1. **Level 1 (Strongest)**: House occupied by the planet's Star Lord.
2. **Level 2**: House occupied by the planet itself.
3. **Level 3**: Houses whose cusp signs are ruled by the planet's Star Lord.
4. **Level 4**: Houses whose cusp signs are ruled by the planet itself.

---

## 12. Module 11: 4-in-1 Unified Numerology

Comprehensive archetypal numerology profile supporting Pythagorean, Chaldean, Kabbalah, and Ank Jyotish.

### Endpoints
- `POST /api/v1/numerology/profile`: Core profile calculation.
- `GET /api/v1/numerology/alphabets`: Tables of letter-to-number assignments.
- `GET /api/v1/numerology/methods`: List of active numerology profiles and calculation policies.

### Canonical Pythagorean Request with Karmic Debts & Interpretations
```json
{
  "method": {
    "system": "pythagorean",
    "profile": "standard",
    "compound_policy": "compound_and_root"
  },
  "subject": {
    "birth_date": "<YYYY-MM-DD>",
    "name": {
      "birth": "<FULL_BIRTH_NAME>",
      "current": "<PREFERRED_CURRENT_NAME>"
    },
    "tz_str": "<IANA_TIMEZONE>"
  },
  "date_context": {
    "reference_date": "<REFERENCE_YYYY-MM-DD>"
  },
  "include_interpretations": true
}
```

### Karmic Debts & Master Numbers Structure
The response populates `.data.core` with compound values:
- Compound numbers (e.g. 16/7, 19/1, 14/5, 13/4).
- Karmic debt array in `.data.core.life_path.karmic_debts`.
- Master numbers (11, 22, 33) preserved without reduction.
- Rich narrative interpretations in `.data.interpretations`.

---

## 13. Module 12: Horoscopes, Ephemeris & Moon Pulse

- **Personalized Daily Horoscopes**: `POST /api/v1/horoscope/daily/personal`, `POST /api/v2/horoscope/daily/personal`, `POST /api/v3/horoscope/daily/personal`
- **Sign Daily Horoscopes**: `GET /api/v1/horoscope/daily/sign?sign=aries`
- **Weekly Horoscope**: `POST /api/v3/horoscope/weekly/personal`
- **Ephemeris Calculation**: `POST /api/v1/ephemeris/calculate`
- **Moon Phases**: `GET /api/v1/moon/phase`
- **Moon Month Calendar**: `GET /api/v1/moon/month?year=<YYYY>&month=<MM>`
- **Garmin-Safe Moon Pulse**: `GET /moon-pulse/v1/moon`
- **Sky Events**: `GET /api/v1/sky-events`

---

## 14. Module 13: Hosted MCP Server & PDF Reports

- **Hosted MCP Server**: `https://api.freeastroapi.com/mcp` (Connect LLM agents directly with `x-api-key`).
- **Report Branding**: `POST /api/v1/auth/report-branding` (Upload logo, primary/secondary colors, and custom typography).
- **Report Credits**: `GET /api/v1/natal/report-credits` (Entry plan includes 2 monthly credits).
- **Report Polling & Retrieval**: `GET /api/v1/natal/report/{job_id}` (Retrieves 8,000–9,000 word publication-ready PDF).
- **City Search & Geo Resolution**: `GET /api/v1/geo/search?q=<CITY_NAME>` and `GET /api/v2/geo/search?q=<CITY_NAME>`.
