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

## 4. Module 3: Hebrew Kabbalistic Gematria (4 Systems)

Calculates numerical values and mystical letter vibrations for Hebrew and Latin words across 4 classical systems.

### A. Gematria Calculation Endpoint
`POST https://api.astrology-api.io/api/v3/kabbalah/gematria`

```bash
timeout 10s curl -s -X POST "https://api.astrology-api.io/api/v3/kabbalah/gematria" \
  -H "Authorization: Bearer $ASTROLOGY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bereshit",
    "language": "latin_translit"
  }'
```

### Supported Calculation Modes:
1. **Standard / Absolute (Ragil)**: Standard numerical value of letters ($1..400$).
2. **Ordinal (Siduri)**: Positional index ($1..22$).
3. **Reduced (Katan)**: Modulo 9 reduction of individual letter values.
4. **Integral (Kolel)**: Base value plus total letter count.

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
