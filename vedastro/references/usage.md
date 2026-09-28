# VedAstro PRO API Technical Usage Manual (REST Engine)

Unified developer and agent reference manual for the VedAstro calculation engine (`https://api.vedastro.org/api/`), powered by Swiss Ephemeris NASA JPL algorithms across 6 macro aggregators and 677 atomic calculators.

---

## 1. Authentication & Common Request Schema

### Authentication Headers
Authentication is handled via the `x-api-key` header (or `APIKey` / `Authorization: Bearer`):

```bash
# Standard Authenticated cURL Template
timeout 10s curl -s -X POST "https://api.vedastro.org/api/Calculate/HoroscopePredictions" \
  -H "x-api-key: $VEDASTRO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

### Standard Time & Location JSON Schema
VedAstro uses a standardized time representation where `StdTime` is formatted as `"HH:mm DD/MM/YYYY +ZZ:ZZ"`:

```json
{
  "Location": {
    "Latitude": <FLOAT_LATITUDE>,
    "Longitude": <FLOAT_LONGITUDE>,
    "Name": "<BIRTH_CITY>"
  },
  "Time": {
    "StdTime": "<HH:mm> <DD/MM/YYYY> <+/-ZZ:ZZ>"
  },
  "Ayanamsa": "<RAMAN|LAHIRI|KP|FAGAN_BRADLEY>"
}
```

> [!IMPORTANT]
> **Delimitation Rules for Dates**:
> - `POST` endpoints require dates with slash `/` in `StdTime` (`"HH:mm DD/MM/YYYY +ZZ:ZZ"`).
> - `GET` endpoints require dates with hyphen `-` in URL path segments (`.../Time/<HH:mm>/<DD-MM-YYYY>/<+/-ZZ:ZZ>/...`).

---

## 2. Architectural Structure: 6 Macro Endpoints vs. 677 Advanced Calculators

The official VedAstro API architecture is bifurcated into two computational tiers:

1. **Macro Endpoints (High-Level Aggregators):**
   - `HoroscopePredictions`: 1,077 combinations and 200+ classical yogas, doshas, and predictions with verbatim citations.
   - `AllPlanetData`: Batch-calculates 144 astronomical, astrological, and strength factors for all 9 planets (1,296 calculations in 1 call).
   - `AllHouseData`: Batch-calculates 40 factors for all 12 houses (480 calculations in 1 call).
   - `DasaAtRange`: Computes 5 levels of Vimshottari Dashas across specified date ranges.
   - `MatchReport`: Traditional 16 Kutas (36 Gunas) synastry compatibility.
   - `SouthIndianChart` / `NorthIndianChart`: Vector SVG chart rendering.
2. **Advanced Calculators (677 Atomic Methods):**
   - Granular methods for individual calculations (e.g. `LagnaSignName`, `MoonConstellation`, `PlanetShadbalaPinda`, `KalaSarpaYoga`, `PanchangaTable`).
   - The complete machine-readable catalog with signatures and parameters is indexed in:  
     [`assets/advanced_calculators_catalog.json`](file:///var/www/.agents/skills/vedastro/assets/advanced_calculators_catalog.json).

---

## 3. Module 1: Horoscope Predictions (Yogas & Doshas)

Evaluates over 200 classical Parashari, Jaimini, and medical yogas, doshas (Kala Sarpa, Manglik, Kemadruma), and behavioral archetypes with canonical literature citations.

### A. POST Method: Complete Predictions
`POST https://api.vedastro.org/api/Calculate/HoroscopePredictions`

```bash
timeout 10s curl -s -X POST "https://api.vedastro.org/api/Calculate/HoroscopePredictions" \
  -H "x-api-key: $VEDASTRO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "birthTime": {
      "StdTime": "<HH:mm> <DD/MM/YYYY> <+/-ZZ:ZZ>",
      "Location": {
        "Latitude": <FLOAT_LATITUDE>,
        "Longitude": <FLOAT_LONGITUDE>,
        "Name": "<BIRTH_CITY>"
      }
    },
    "Ayanamsa": "LAHIRI"
  }'
```

### Response Schema:
```json
{
  "Status": "Pass",
  "Payload": [
    {
      "Name": "Gajakesari Yoga",
      "Description": "Jupiter is in a kendra from the Moon. The native will be illustrious...",
      "RelatedBody": {
        "Planets": ["Jupiter", "Moon"],
        "Houses": [1, 4, 7, 10]
      },
      "Tags": ["Wealth", "Reputation", "Virtue"]
    }
  ]
}
```

---

## 4. Module 2: Complete Natal Planetary Positions & Strengths (`AllPlanetData`)

Calculates coordinates, speeds, avasthas (Lajjita, Garvita, Kshudita, Trashita, Mudita), dignities, aspects, Shadbala breakdowns, and Ashtakavarga points for all 9 planets in a single call.

### A. All Planet Data Endpoint
`POST https://api.vedastro.org/api/Calculate/AllPlanetData`

```bash
timeout 10s curl -s -X POST "https://api.vedastro.org/api/Calculate/AllPlanetData" \
  -H "x-api-key: $VEDASTRO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "PlanetName": "All",
    "Time": {
      "StdTime": "<HH:mm> <DD/MM/YYYY> <+/-ZZ:ZZ>",
      "Location": {
        "Latitude": <FLOAT_LATITUDE>,
        "Longitude": <FLOAT_LONGITUDE>,
        "Name": "<BIRTH_CITY>"
      }
    },
    "Ayanamsa": "LAHIRI"
  }'
```

---

## 5. Module 3: Complete House Analytics (`AllHouseData`)

Calculates cusps, signs, lords, occupants, and aspects for all 12 houses (Bhava Chalit and Rasi) across 40 parameters per house.

### A. All House Data Endpoint
`POST https://api.vedastro.org/api/Calculate/AllHouseData`

```bash
timeout 10s curl -s -X POST "https://api.vedastro.org/api/Calculate/AllHouseData" \
  -H "x-api-key: $VEDASTRO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "HouseName": "All",
    "Time": {
      "StdTime": "<HH:mm> <DD/MM/YYYY> <+/-ZZ:ZZ>",
      "Location": {
        "Latitude": <FLOAT_LATITUDE>,
        "Longitude": <FLOAT_LONGITUDE>,
        "Name": "<BIRTH_CITY>"
      }
    },
    "Ayanamsa": "LAHIRI"
  }'
```

---

## 6. Module 4: Multi-Level Vimshottari Dashas (5 Computational Levels)

Calculates the temporal unfolding of life periods across 5 hierarchical levels: Mahadasha (L1), Antardasha (L2), Pratyantardasha (L3), Sookshmadasha (L4), and Pranadasha (L5).

### A. POST Method (`DasaAtRange`)
`POST https://api.vedastro.org/api/Calculate/DasaAtRange`

```bash
timeout 10s curl -s -X POST "https://api.vedastro.org/api/Calculate/DasaAtRange" \
  -H "x-api-key: $VEDASTRO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "birthTime": {
      "StdTime": "<HH:mm> <DD/MM/YYYY> <+/-ZZ:ZZ>",
      "Location": {
        "Latitude": <FLOAT_LATITUDE>,
        "Longitude": <FLOAT_LONGITUDE>,
        "Name": "<BIRTH_CITY>"
      }
    },
    "startTime": {
      "StdTime": "<HH:mm> <DD/MM/YYYY> <+/-ZZ:ZZ>",
      "Location": {"Latitude": <FLOAT_LATITUDE>, "Longitude": <FLOAT_LONGITUDE>, "Name": "<BIRTH_CITY>"}
    },
    "endTime": {
      "StdTime": "<HH:mm> <DD/MM/YYYY> <+/-ZZ:ZZ>",
      "Location": {"Latitude": <FLOAT_LATITUDE>, "Longitude": <FLOAT_LONGITUDE>, "Name": "<BIRTH_CITY>"}
    },
    "ayanamsa": "LAHIRI",
    "levels": 3
  }'
```

### B. GET Method Equivalent:
```bash
timeout 10s curl -s "https://api.vedastro.org/api/Calculate/DasaAtRange/Location/<FLOAT_LATITUDE>,<FLOAT_LONGITUDE>/Time/<HH:mm>/<DD-MM-YYYY>/<+/-ZZ:ZZ>/StartTime/<HH:mm>/<DD-MM-YYYY>/<+/-ZZ:ZZ>/EndTime/<HH:mm>/<DD-MM-YYYY>/<+/-ZZ:ZZ>/Levels/3/PrecisionHours/24/Ayanamsa/LAHIRI" \
  -H "x-api-key: $VEDASTRO_API_KEY"
```

---

## 7. Module 5: Ashtakoota Match Making Compatibility (16 Kutas)

Calculates relationship and business partnership compatibility using the traditional 16 Kutas and 36 Gunas system.

### A. Match Report Endpoint
`POST https://api.vedastro.org/api/Calculate/MatchReport`

```bash
timeout 10s curl -s -X POST "https://api.vedastro.org/api/Calculate/MatchReport" \
  -H "x-api-key: $VEDASTRO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "maleTime": {
      "Location": {"Latitude": <FLOAT_LATITUDE_M>, "Longitude": <FLOAT_LONGITUDE_M>, "Name": "<CITY_M>"},
      "Time": {"StdTime": "<HH:mm> <DD/MM/YYYY> <+/-ZZ:ZZ>"}
    },
    "femaleTime": {
      "Location": {"Latitude": <FLOAT_LATITUDE_F>, "Longitude": <FLOAT_LONGITUDE_F>, "Name": "<CITY_F>"},
      "Time": {"StdTime": "<HH:mm> <DD/MM/YYYY> <+/-ZZ:ZZ>"}
    },
    "ayanamsa": "RAMAN"
  }'
```

---

## 8. Module 6: Classical Vedic Texts RAG Vector Search

Semantic search engine querying foundational classical textbooks with vector embeddings.

### A. Search Source Text Endpoint
`GET https://api.vedastro.org/api/Calculate/SearchSourceText/...`

```bash
timeout 10s curl -s "https://api.vedastro.org/api/Calculate/SearchSourceText/Query/<ENCODED_SEARCH_QUERY>/TopK/5/SourceName/Hindu-Predictive-Astrology" \
  -H "x-api-key: $VEDASTRO_API_KEY"
```

### Available Source Names:
- `Hindu-Predictive-Astrology` (B.V. Raman)
- `Brihat-Parashara-Hora-Shastra` (Maharishi Parashara)
- `Jaimini-Sutras` (Maharishi Jaimini)

---

## 9. Module 7: South & North Indian Kundli SVG Visual Charts

Generates clean vector SVG birth chart diagrams in authentic regional formats.

### A. South Indian Diamond Chart SVG
```bash
timeout 10s curl -s "https://api.vedastro.org/api/Calculate/SouthIndianChart/Location/<FLOAT_LATITUDE>,<FLOAT_LONGITUDE>/Time/<HH:mm>/<DD-MM-YYYY>/<+/-ZZ:ZZ>/Ayanamsa/RAMAN" \
  -H "x-api-key: $VEDASTRO_API_KEY" -o south_indian_chart.svg
```

### B. North Indian Square Chart SVG
```bash
timeout 10s curl -s "https://api.vedastro.org/api/Calculate/NorthIndianChart/Location/<FLOAT_LATITUDE>,<FLOAT_LONGITUDE>/Time/<HH:mm>/<DD-MM-YYYY>/<+/-ZZ:ZZ>/Ayanamsa/RAMAN" \
  -H "x-api-key: $VEDASTRO_API_KEY" -o north_indian_chart.svg
```

---

## 10. CoHaLo Context Engineering & Token Economy

A complete raw extraction of VedAstro yields ~177 KB of JSON (~45,000 tokens). Dumping this directly into an LLM context window causes cognitive degradation and token waste.

### The Two-Tier Compression Architecture:
1. **Tier 1 — Exhaustive Data Lake (SSoT Disk):**  
   Save full raw JSON dumps in `raw/json/dumps/04_vedic_jyotish_kp.json`. Accessible offline by specialized diagnostic subskills (`oraculo-diag-b-voc`, `oraculo-diag-d-leg`).
2. **Tier 2 — Surgical Phase Feeds (CoHaLo XML):**  
   `omni_consensus_engine.py` filters the data into structured, typed XML feeds (`<feed_input phase="4">`) containing exclusively the **Vedic Trinity** (Lagna, Surya Lagna, Chandra Lagna/AK) and 2-3 karmic challenge yogas (<2.5 KB XML, >95% token savings).
