# Astrology-API.io (V3) Technical Usage Manual

Comprehensive developer and agent reference manual for the Astrology-API.io calculation engine (`https://api.astrology-api.io/api/v3/`), powered by Swiss Ephemeris SE 2.10 across 100+ endpoints.

---

## 1. Authentication & Common Request Structure

### Authentication Header
Every request requires the `Authorization` header containing your Bearer API token (`$ASTROLOGY_API_IO` or `$ASTROLOGY_API_KEY`):

```bash
# Standard Authenticated Request Header
API_KEY="${ASTROLOGY_API_IO:-${ASTROLOGY_API_KEY:-${astrology_apiKey:-}}}"
-H "Authorization: Bearer ${API_KEY}" \
-H "Content-Type: application/json"
```

### Universal `birth_data` Schema
All endpoints calculating natal charts, timing, or numerology accept the standardized `birth_data` JSON object with canonical typed parameters:

```json
{
  "year": <YYYY>,
  "month": <MM>,
  "day": <DD>,
  "hour": <HH>,
  "minute": <MIN>,
  "latitude": <FLOAT_LATITUDE>,
  "longitude": <FLOAT_LONGITUDE>,
  "timezone": "<TIMEZONE_STR>"
}
```

---

## 2. Module 1: Western Natal & 23 House Systems

Calculates exact tropical/sidereal planet coordinates, 23 house system cusps (Placidus, Whole Sign, Koch, Equal, Regiomontanus, Campanus, Topocentric, Alcabitius, Porphyry, Morinus, etc.), and complete aspect tables.

### A. Calculate Full Natal Chart
`POST https://api.astrology-api.io/api/v3/western/natal-chart`

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/western/natal-chart" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "year": <YYYY>,
      "month": <MM>,
      "day": <DD>,
      "hour": <HH>,
      "minute": <MIN>,
      "latitude": <FLOAT_LATITUDE>,
      "longitude": <FLOAT_LONGITUDE>,
      "timezone": "<TIMEZONE_STR>"
    },
    "house_system": "placidus",
    "zodiac_type": "tropical",
    "include_aspects": true,
    "orb_profile": "tight"
  }'
```

---

## 3. Module 2: Multi-Name Core Numerology (5 Pillars)

Calculates the five core master numerology numbers for individuals and businesses with multi-name vibration analysis.

### A. Core Numbers Endpoint
`POST https://api.astrology-api.io/api/v3/numerology/core-numbers`

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/numerology/core-numbers" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": {
      "name": "<CONSULTANT_LEGAL_NAME>",
      "preferred_name": "<CONSULTANT_PREFERRED_NAME>",
      "birth_data": {
        "year": <YYYY>,
        "month": <MM>,
        "day": <DD>,
        "hour": <HH>,
        "minute": <MIN>,
        "latitude": <FLOAT_LATITUDE>,
        "longitude": <FLOAT_LONGITUDE>,
        "timezone": "<TIMEZONE_STR>"
      }
    }
  }'
```

### Returns 5 Core Pillars:
- **Life Path Number (Camino de Vida)**: From full birth date.
- **Expression / Destiny Number (Número de Destino)**: From full legal birth name.
- **Soul Urge / Heart's Desire (Deseo del Alma)**: From vowel vibrations.
- **Personality Number (Número de Personalidad)**: From consonant vibrations.
- **Birthday Number (Número de Nacimiento)**: Direct day reduction.

---

## 4. Module 3: Hebrew Kabbalistic Gematria (7 Methods & 72 Angels)

Calculates numerical values and mystical letter vibrations for Hebrew and Latin words across 7 classical calculation methods, plus the 72 Angels of Shem HaMephorash.

### A. Gematria Calculation Endpoint
`POST https://api.astrology-api.io/api/v3/kabbalah/gematria`

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/kabbalah/gematria" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bereshit",
    "language": "latin_translit",
    "method": "mispar_gadol"
  }'
```

### Supported Calculation Methods:
1. `mispar_hechrachi` (Ragil): Standard absolute numerical value ($1..400$).
2. `mispar_gadol`: Final letters (sofit) continue from 500 to 900 (Kaf Sofit=500, Mem=600, Nun=700, Pe=800, Tsade=900).
3. `mispar_katan`: Modulo 9 reduction of individual letter values (eliminates positional zeros).
4. `mispar_katan_mispari`: Integral word reduction to single digit.
5. `ordinal` (Siduri): Positional index in the 22-letter Hebrew alphabet ($1..22$).
6. `atbash`: Mirror substitution cipher (Aleph $\leftrightarrow$ Tav, Bet $\leftrightarrow$ Shin).
7. `albam`: Half-split substitution cipher (Aleph $\leftrightarrow$ Lamed).

### B. Birth Angels of Shem HaMephorash Endpoint
`POST https://api.astrology-api.io/api/v3/kabbalah/birth-angels`

Maps the 72 divine angels to exact 5° zodiacal quinances, providing the Physical, Emotional, and Intellectual guardian angels, along with Tree of Life pillar balancing (Mercy, Severity, Mildness):

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/kabbalah/birth-angels" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "year": <YYYY>,
      "month": <MM>,
      "day": <DD>,
      "hour": <HH>,
      "minute": <MIN>,
      "latitude": <FLOAT_LATITUDE>,
      "longitude": <FLOAT_LONGITUDE>,
      "timezone": "<TIMEZONE_STR>"
    }
  }'
```

---

## 5. Module 4: Hellenistic Timing Suite (11 Endpoints)

Comprehensive time-lord hub implementing classical Hellenistic and Persian timing techniques under `/api/v3/timing/*`.

### A. Timeline Aggregator (Flagship Endpoint)
Merges Annual Profections, Firdaria L1/L2, Decennials, and Zodiacal Releasing in parallel into a single chronological stream of active time-lords.

`POST https://api.astrology-api.io/api/v3/timing/timeline`

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/timing/timeline" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "year": <YYYY>,
      "month": <MM>,
      "day": <DD>,
      "hour": <HH>,
      "minute": <MIN>,
      "latitude": <FLOAT_LATITUDE>,
      "longitude": <FLOAT_LONGITUDE>,
      "timezone": "<TIMEZONE_STR>"
    },
    "target_date": "<TARGET_YYYY-MM-DD>",
    "techniques": ["profections", "firdaria", "decennials", "zodiacal_releasing"]
  }'
```

### B. Specific Timing Endpoints:
- **Annual Profections**: `POST /api/v3/timing/profections/annual` (Anchors: ASC, Fortune, Spirit, Sun, Moon, MC).
- **Firdaria**: `POST /api/v3/timing/firdaria` (Persian 75-year sect-aware cycle, L1 major and L2 sub-rulers).
- **Decennials**: `POST /api/v3/timing/decennials` (10-year Chaldean general planetary time-lords).
- **Zodiacal Releasing**: `POST /api/v3/timing/zodiacal-releasing` (Vettius Valens Lots of Fortune/Spirit down to L4).
- **Sun-Conjunctions**: `POST /api/v3/timing/sun-conjunctions` (Cazimi ~17', Combust ~8°30', Under the Beams ~17').

---

## 6. Module 5: Vedic Jyotish & Drishti Aspects

Sidereal Jyotish calculations matching traditional Parashara standards (BPHS) and Jagannatha Hora (JHora 8.0).

### A. Vedic Aspects & Drik Bala
`POST https://api.astrology-api.io/api/v3/vedic/aspects`

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/vedic/aspects" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "year": <YYYY>,
      "month": <MM>,
      "day": <DD>,
      "hour": <HH>,
      "minute": <MIN>,
      "latitude": <FLOAT_LATITUDE>,
      "longitude": <FLOAT_LONGITUDE>,
      "timezone": "<TIMEZONE_STR>"
    },
    "ayanamsa": "lahiri"
  }'
```

### Returns 6 Astrological Blocks:
- **Graha Drishti**: Planetary sight percentage per planet (BPHS Ch.27).
- **Drik Bala**: Exact aspectual strength matching JHora 8.0 (BPHS Ch.26).
- **Bhava Drishti**: Total aspect load on the 12 houses.
- **House-Lord Aspects**: Relationships between house dispositors.
- **Jaimini Rashi Drishti**: Sign-to-sign mutual aspects.

---

## 7. Module 6: Horoscope Engine (12 Life Areas, 17 Languages)

Deterministic daily, weekly, monthly, and yearly horoscope narratives localized in 17 languages.

### A. Daily Structured Horoscope
`GET https://api.astrology-api.io/api/v3/horoscope/daily`

```bash
timeout 10s curl -s -X GET "https://api.astrology-api.io/api/v3/horoscope/daily?sign=<ZODIAC_SIGN>&lang=<ISO_2_LANG>&format=structured" \
  -H "Authorization: Bearer ${API_KEY}"
```

### 12 Life Areas Breakdown:
`Identity`, `Health`, `Finance`, `Career`, `Love`, `Relationships`, `Creativity`, `Spirituality`, `Home`, `Learning`, `Communication`, `Travel`.

---

## 8. Module 7: Relocation & ACG World Analysis

Unified planetary relocation analysis integrating Astrocartography, Local Space azimuths, and parans.

### A. Relocation Report Endpoint
`POST https://api.astrology-api.io/api/v3/analysis/relocation-report`

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/analysis/relocation-report" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "year": <YYYY>,
      "month": <MM>,
      "day": <DD>,
      "hour": <HH>,
      "minute": <MIN>,
      "latitude": <FLOAT_LATITUDE>,
      "longitude": <FLOAT_LONGITUDE>,
      "timezone": "<TIMEZONE_STR>"
    },
    "candidate_cities": [
      {"name": "<CITY_NAME_1>", "latitude": <FLOAT_LAT_1>, "longitude": <FLOAT_LNG_1>},
      {"name": "<CITY_NAME_2>", "latitude": <FLOAT_LAT_2>, "longitude": <FLOAT_LNG_2>}
    ]
  }'
```

---

## 9. Module 8: Graphic Ephemeris & Harmonics SVG

Generates finished vector SVG visual ephemeris grids where planetary movements cross degree bands over selectable time windows.

### A. Graphic Ephemeris SVG Endpoint
`POST https://api.astrology-api.io/api/v3/render/graphic-ephemeris`

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/render/graphic-ephemeris" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "year": <YYYY>,
      "month": <MM>,
      "day": <DD>,
      "hour": <HH>,
      "minute": <MIN>,
      "latitude": <FLOAT_LATITUDE>,
      "longitude": <FLOAT_LONGITUDE>,
      "timezone": "<TIMEZONE_STR>"
    },
    "harmonic": 4,
    "window_months": 12,
    "planets": ["Sun", "Moon", "Mars", "Jupiter", "Saturn", "Uranus", "Pluto"]
  }' -o graphic_ephemeris.svg
```

---

## 10. Module 9: Quota-Optimized Multi-Aggregator Endpoints (Free Tier Stretching)

Architecture-grade aggregator endpoints designed to minimize API consumption under the 50 requests/month free tier:

### A. Enhanced Positions with Essential Dignities & Arabic Lots (1 Call vs 4)
`POST https://api.astrology-api.io/api/v3/data/positions/enhanced`

Returns in a single round-trip: planet positions, dignities (rulership, exaltation, triplicity, bounds, decans), debilities, sect condition, combustion/cazimi, houses of joy, dispositor chains, mutual receptions, and Arabic lots.

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/data/positions/enhanced" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "year": <YYYY>,
      "month": <MM>,
      "day": <DD>,
      "hour": <HH>,
      "minute": <MIN>,
      "latitude": <FLOAT_LATITUDE>,
      "longitude": <FLOAT_LONGITUDE>,
      "timezone": "<TIMEZONE_STR>"
    },
    "house_system": "P",
    "include_lots": true,
    "include_receptions": true
  }'
```

### B. Global Mundane Positions (24-Hour Cache Seed)
`POST https://api.astrology-api.io/api/v3/data/global-positions`

Calculates universal celestial positions independent of local coordinates. Seed once per day at 00:00 UTC and cache for 24h (`TTL: 86400`) to serve thousands of mundane transit requests consuming only 30 requests/month.

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/data/global-positions" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "<YYYY-MM-DD>",
    "time": "00:00:00",
    "zodiac_type": "tropical"
  }'
```

---

## 11. Module 10: Traditional Dignities & Almuten Figuris (Bonatti)

Calculates the Almuten Figuris (Ruler of the Chart) using Guido Bonatti's medieval weighted scoring system ($5/4/3/2/1$) over the 5 canonical Hyleg points (Sun, Moon, Ascendant, Part of Fortune, and Prenatal Syzygy solved via Brent's root-finding algorithm `brentq`).

### A. Almuten Figuris Calculation Endpoint
`POST https://api.astrology-api.io/api/v3/traditional/almuten`

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/traditional/almuten" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_data": {
      "year": <YYYY>,
      "month": <MM>,
      "day": <DD>,
      "hour": <HH>,
      "minute": <MIN>,
      "latitude": <FLOAT_LATITUDE>,
      "longitude": <FLOAT_LONGITUDE>,
      "timezone": "<TIMEZONE_STR>"
    },
    "scoring_system": "bonatti",
    "include_accidental": true,
    "syzygy_solver": "brent"
  }'
```

---

## 12. Canonical 3-Call Single-Pass Ingestion Basket (3 Credits / Consultant)

For Phase 0 extraction in the Data Lakehouse, execute exactly these 3 calls sequentially with `sleep 2.0` throttling. This guarantees 100% data coverage while consuming only 3 credits per client:

1. **Call 1 — Master Hellenistic Timeline (1 credit)**:
   - `POST /api/v3/timing/timeline`
   - Ingests Profections, Firdaria L1/L2, Decennials, and Zodiacal Releasing in parallel.
2. **Call 2 — Enhanced Positions & Dignities (1 credit)**:
   - `POST /api/v3/data/positions/enhanced`
   - Ingests tropical coordinates, essential dignities, debilities, joys, sect, and 9 Arabic lots.
3. **Call 3 — Core Numerology (1 credit)**:
   - `POST /api/v3/numerology/core-numbers`
   - Ingests Life Path, Expression, Soul Urge, Personality, and Birthday numbers.

Total Consumption: Exactly 3 API credits per client run. Allows up to 16 complete consultant audits per month on the 50 req/mo Free Tier.
