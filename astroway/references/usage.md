# AstroWay Comprehensive Technical Usage Manual (REST Engine)

Unified technical reference manual for the AstroWay Swiss Ephemeris calculation engine (`https://api.astroway.info/v1/`), powered by NASA JPL DE440/DE441 high-precision ephemerides across **758 unique routes** and **760 HTTP operations** categorized under **59 functional domain tags**.

---

## 1. Global Authentication & Request Architecture

### REST API Authentication
Authentication uses the HTTP header `X-Api-Key` with your active API key.

```bash
# Standard REST Request Execution Template
curl -s -X POST "https://api.astroway.info/v1/chart" \
  -H "X-Api-Key: $ASTROWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept-Encoding: br, gzip" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{
    "date": "<YYYY-MM-DD>",
    "time": "<HH:MM:SS>",
    "timezoneOffset": <FLOAT_HOURS_UTC>,
    "latitude": <FLOAT_LATITUDE>,
    "longitude": <FLOAT_LONGITUDE>,
    "houseSystem": "P",
    "zodiacType": "tropical"
  }'
```

### Real-Time Credit Audit Headers
Every HTTP response returns deterministic audit headers:
- `X-Credits-Used`: Number of credits charged for the specific call.
- `X-Credits-Remaining`: Remaining credit balance in your monthly quota.
- `X-Credits-Limit`: Total monthly credit allocation (50,000 credits on Indie PRO).

---

## 2. Canonical Input Schemas (100% Client-Agnostic & Zero-PII)

All requests conform strictly to Pydantic models with generic typed variables.

### A. Standard Natal Chart Model (`ChartInput`)
Root model for Western, Hellenistic, ACG, Human Design, and Cosmobiology:
```json
{
  "date": "<YYYY-MM-DD>",
  "time": "<HH:MM:SS>",
  "timezoneOffset": <FLOAT_HOURS_UTC>,
  "latitude": <FLOAT_LATITUDE>,
  "longitude": <FLOAT_LONGITUDE>,
  "houseSystem": "<P|W|K|C|R|O|E>",
  "name": "<CONSULTANT_NAME>",
  "city": "<BIRTH_CITY>",
  "zodiacType": "<tropical|sidereal>",
  "ayanamsa": "<lahiri|fagan_bradley|raman|krishnamurti>"
}
```
*Valid `houseSystem` codes*: `P` (Placidus), `W` (Whole Sign), `K` (Koch), `C` (Campanus), `R` (Regiomontanus), `O` (Porphyry), `E` (Equal). Default: `"P"`.

### B. Untimed Birth Model (`ChartInputUnknownTime`)
Used when exact birth hour is unavailable:
```json
{
  "date": "<YYYY-MM-DD>",
  "timeUnknown": true,
  "timezoneOffset": <FLOAT_HOURS_UTC>,
  "latitude": <FLOAT_LATITUDE>,
  "longitude": <FLOAT_LONGITUDE>,
  "houseSystem": "W"
}
```

### C. Chinese BaZi Four Pillars Model (`BaziFourPillarsInput`)
Used by `/bazi/*` endpoints:
```json
{
  "date": "<YYYY-MM-DD>",
  "time": "<HH:MM:SS>",
  "timezoneOffset": <FLOAT_HOURS_UTC>
}
```

### D. Cosmobiology 90° Dial Model (`ChartWithTnp`)
Used by `/cosmobiology/*` endpoints:
```json
{
  "date": "<YYYY-MM-DD>",
  "time": "<HH:MM:SS>",
  "timezoneOffset": <FLOAT_HOURS_UTC>,
  "latitude": <FLOAT_LATITUDE>,
  "longitude": <FLOAT_LONGITUDE>,
  "withTnp": true
}
```

---

## 3. Module 1: Vedic Jyotish & Classical Metaphysics (174 Endpoints)

High-precision Vedic calculation engine supporting Parashara, Jaimini, and Lal Kitab.

### Key Endpoints:
- **16 Shodashavargas (D1 to D60)**:
  - `POST /v1/vedic/varga/d1` (Rasi: Physical constitution, general life path)
  - `POST /v1/vedic/varga/d2` (Hora: Wealth, assets, liquid finances)
  - `POST /v1/vedic/varga/d3` (Drekkana: Siblings, courage, vitality)
  - `POST /v1/vedic/varga/d4` (Chaturthamsa: Real estate, immovable property, home)
  - `POST /v1/vedic/varga/d7` (Saptamsa: Children, progeny, creative lineage)
  - `POST /v1/vedic/varga/d9` (Navamsa: Dharma, marriage, spiritual maturity, inner soul)
  - `POST /v1/vedic/varga/d10` (Dasamsa: Career, profession, status, public reputation)
  - `POST /v1/vedic/varga/d12` (Dwadasamsa: Parents, ancestral heritage, past-life lineage)
  - `POST /v1/vedic/varga/d16` (Shodasamsa: Vehicles, conveyances, general luxuries)
  - `POST /v1/vedic/varga/d20` (Vimsamsa: Spiritual pursuits, devotion, upasana)
  - `POST /v1/vedic/varga/d24` (Chaturvimsamsa: Higher learning, knowledge, intellect)
  - `POST /v1/vedic/varga/d27` (Saptavimsamsa: Strengths, weaknesses, subconscious resilience)
  - `POST /v1/vedic/varga/d30` (Trimsamsa: Evils, misfortunes, subconscious miseries)
  - `POST /v1/vedic/varga/d40` (Khavedamsa: Auspicious and inauspicious karmic effects)
  - `POST /v1/vedic/varga/d45` (Akshavedamsa: Character, purity, general wellbeing)
  - `POST /v1/vedic/varga/d60` (Shashtiamsa: Fine-grained past-life karma, highest root weight)
- **10 Distinct Dasha Systems (Up to 5 Levels: Maha, Antar, Pratyantar, Sookshma, Prana)**:
  - `POST /v1/vedic/dashas/vimshottari/*` (Standard 120-year cycle)
  - `POST /v1/vedic/dashas/yogini/*` (8 Yoginis 36-year cycle)
  - `POST /v1/vedic/dashas/chara/*` (Jaimini sign-based progression)
  - `POST /v1/vedic/dashas/kalachakra/*` (Constellational wheel progression)
  - `POST /v1/vedic/dashas/ashtottari/*` (108-year Rahu-excluded system)
  - `POST /v1/vedic/dashas/shatabdika/*` (100-year cycle)
  - `POST /v1/vedic/dashas/shodashottari/*` (116-year cycle)
  - `POST /v1/vedic/dashas/shoola/*` (Longevity and timing of crisis)
  - `POST /v1/vedic/dashas/sthira/*` (Fixed sign dasha)
  - `POST /v1/vedic/dashas/tribhagi/*` (Accelerated 80-year cycle)
- **6-Factor Shadbala & Planetary Strengths**:
  - `POST /v1/vedic/shadbala/full` (Combined 6-factor strength in Rupas)
  - `POST /v1/vedic/shadbala/sthana` (Positional strength)
  - `POST /v1/vedic/shadbala/dig` (Directional strength)
  - `POST /v1/vedic/shadbala/kala` (Temporal strength)
  - `POST /v1/vedic/shadbala/cheshta` (Motional strength)
  - `POST /v1/vedic/shadbala/naisargika` (Natural strength)
  - `POST /v1/vedic/shadbala/drik` (Aspectual strength)
  - `POST /v1/vedic/bhavabala` (12 House cusp strengths)
- **Jaimini Astrology**:
  - `POST /v1/vedic/jaimini/chara-karakas` (7 and 8 Karakas: Atmakaraka, Amatyakaraka, Bhratri, Matri, Pitri, Putra, Gnati, Dara)
  - `POST /v1/vedic/jaimini/atmakaraka-navamsa` (Karakamsa placement and spiritual orientation)
  - `POST /v1/vedic/jaimini/padas` (Arudha Padas: AL, A1 to A12, UL Upapada)
  - `POST /v1/vedic/jaimini/argala-analysis` (Intervention and obstruction analysis)
  - `POST /v1/vedic/jaimini/yogas` (Raja Yogas and Dhana Yogas in Jaimini)
- **Lal Kitab System**:
  - `POST /v1/vedic/lal-kitab/teva` (Lal Kitab birth chart conversion)
  - `POST /v1/vedic/lal-kitab/debts` (Ancestral and karmic debts: Pitra, Matri, etc.)
  - `POST /v1/vedic/lal-kitab/remedies` (Prescriptive planetary pacifications)
  - `POST /v1/vedic/lal-kitab/varshphal` (Annual solar return according to Lal Kitab)
- **Panchang & Muhurta**:
  - `POST /v1/vedic/panchang/full` (Tithi, Vara, Nakshatra, Yoga, Karana, Rahu Kaal, Choghadia)
  - `POST /v1/vedic/muhurat/*` (Marriage, property purchase, travel, vehicle, surgery, business start)

---

## 4. Module 2: Human Design Mechanics (12 Endpoints)

Calculates the complete BodyGraph mechanics founded by Ra Uru Hu.

### Key Endpoints:
- `POST /v1/human-design`: Full BodyGraph calculation. Returns Type (Generator, Manifesting Generator, Projector, Manifestor, Reflector), Strategy, Not-Self Theme, Authority (Solar Plexus, Sacral, Splenic, Ego, Self-Projected, None/Lunar), Profile (1/3 to 6/3), Definition (Single, Split, Triple, Quadruple), 9 Centers, 36 Channels, and 64 Gates across conscious (Personality) and unconscious (Design, 88° solar arc previous) activations.
- `POST /v1/hd/circuitry`: Individual (Knowing, Centering), Collective (Understanding, Sensing), Tribal (Ego, Defense), and Integration sub-circuit mapping.
- `POST /v1/hd/incarnation-cross`: Incarnation Cross orientation (Right Angle, Left Angle, Juxtaposition) with solar/earth gate coordinates.
- `POST /v1/hd/dream-rave`: Sleep matrix analyzing night astral body and dormant centers.
- `POST /v1/hd/penta`: BG5 small group analysis (3 to 5 members) and functional organizational channels.
- `POST /v1/hd/sensitivity`: Primary Health System (PHS) determination: Digestion, Environment, and Primary Cognition (Color, Tone, Base).

---

## 5. Module 3: Hellenistic & Traditional Astrology (40 Endpoints)

Exposes the core traditions of classical Hellenistic and Medieval predictive astrology.

### Traditions & Endpoints:
- **Chris Brennan Tradition (10 Endpoints)**:
  - `POST /v1/hellenistic/brennan/lots-15`: 15 Hellenistic Lots (Fortune, Spirit, Eros, Necessity, Courage, Victory, Nemesis, etc.).
  - `POST /v1/hellenistic/brennan/zodiacal-releasing/spirit`: Zodiacal Releasing from Lot of Spirit (career, peak action periods L1–L4).
  - `POST /v1/hellenistic/brennan/zodiacal-releasing/fortune`: Zodiacal Releasing from Lot of Fortune (physical body, health, material circumstances).
  - `POST /v1/hellenistic/brennan/zr/peak-periods`: Angular peak periods and Loosing of the Bond detection.
  - `POST /v1/hellenistic/brennan/profections-detail`: Annual, monthly, and daily profections with lord of the year.
  - `POST /v1/hellenistic/brennan/time-lord-stack`: Comprehensive multi-system time-lord hierarchy.
  - `POST /v1/hellenistic/brennan/joys-of-planets`: Planetary joys in the 12 traditional houses.
- **Dorian Greenbaum Tradition (10 Endpoints)**:
  - `POST /v1/hellenistic/greenbaum/antiscia-hellenistic` & `_contra_antiscia`: Solstitial mirror points and shadow activations.
  - `POST /v1/hellenistic/greenbaum/dodekatemoria`: 2.5° micro-twelfth harmonic sign subdivisions.
  - `POST /v1/hellenistic/greenbaum/daimon-tyche-axis`: Daimon vs. Tyche spiritual-material polarities.
  - `POST /v1/hellenistic/greenbaum/quality-of-time`: Qualitative climate and atmospheric temperament assessment.
  - `POST /v1/hellenistic/greenbaum/temple-doctrine`: Planetary temple and sanctuary doctrines.
- **Robert Hand Tradition (10 Endpoints)**:
  - `POST /v1/hellenistic/hand/bounds`: Egyptian and Chaldean terms/bounds.
  - `POST /v1/hellenistic/hand/decennials`: Major and minor decennial time-lords (10-year and 7-month periods).
  - `POST /v1/hellenistic/hand/sect-strength`: Diurnal vs. nocturnal sect calculations (Hayz and Halbfass status).
- **Robert Schmidt Tradition (10 Endpoints)**:
  - `POST /v1/hellenistic/schmidt/aspectual-typology`: Greek aspectual testimonies (witnessing, adherence, contraposition).
  - `POST /v1/hellenistic/schmidt/lord-of-prediction`: Predominating lord and natal governor.

---

## 6. Module 4: Cosmobiology & Hamburg School (10 Endpoints)

Reinhold Ebertin and Alfred Witte's symmetrical 90° dial astrology.

### Endpoints:
- `POST /v1/cosmobiology/dial-90`: 90° dial projection calculating hard aspects (conjunction, square, opposition, semi-square, sesquiquadrate) within tight orbs (<1.5°).
- `POST /v1/aspects/midpoint-trees`: Complete planetary midpoint trees (e.g. Sun/Moon = Jupiter, Ascendant/Midheaven midpoints).
- `POST /v1/cosmobiology/uranian-tnps`: Coordinates for the 8 hypothetical Transneptunian points (Cupido, Hades, Zeus, Kronos, Apollon, Admetos, Vulkanus, Poseidon).
- `POST /v1/cosmobiology/witte-formulas`: Three- and four-factor planetary symmetry formulas ($A + B - C$).

---

## 7. Module 5: Chinese Metaphysics (39 Endpoints)

Comprehensive traditional Chinese metaphysical systems.

### Key Sub-Domains:
- **BaZi (Four Pillars - 11 Endpoints)**:
  - `POST /v1/bazi/four-pillars`: Year, Month, Day, and Hour pillars anchored on the 60-Jiazi sexagesimal cycle.
  - `POST /v1/bazi/day-master`: Day Master stem, Yin/Yang polarity, seasonal strength, and root balance.
  - `POST /v1/bazi/ten-gods`: Shi Shen (Ten Gods) relationships for all heavenly stems and hidden earthly branches.
  - `POST /v1/bazi/element-balance`: Quantitative percentage balance of the Five Elements (Wood, Fire, Earth, Metal, Water).
  - `POST /v1/bazi/luck-pillars`: Da Yun 10-year luck pillars from age 0 to 90.
- **Feng Shui (14 Endpoints)**:
  - `POST /v1/chinese/feng-shui/flying-star`: Xuan Kong Fei Xing 9-palace annual and natal star grid.
  - `POST /v1/chinese/feng-shui/bagua`: Trigram alignment and spatial energetic sectors.
  - `POST /v1/chinese/feng-shui/kua`: Personal Gua/Kua number calculation and favorable directions.
- **Zi Wei Dou Shu (Purple Star - 13 Endpoints)**:
  - `POST /v1/ziwei/full-chart`: 12 Palaces (Destiny, Wealth, Career, Siblings, Spouse, Children, Health, Travel, Friends, Property, Karma, Parents).
  - `POST /v1/ziwei/main-stars`: 14 Major Stars (Zi Wei, Tian Ji, Tai Yang, etc.).
  - `POST /v1/ziwei/four-transformations`: Si Hua transformations (Lu, Quan, Ke, Ji).

---

## 8. Module 6: Astro-Geography & Relocation (18 Endpoints)

Calculates planetary lines and angular influences projected across the globe.

### Endpoints:
- `POST /v1/acg`: Full world Astrocartography lines for ASC, DSC, MC, and IC across all 10 major planetary bodies.
- `POST /v1/geo/acg/best-places`: Algorithmic ranking of optimal world cities filtered by category (Career, Love, Spirituality, Creativity).
- `POST /v1/geo/parans`: Latitudinal crossing points (parans) where two planetary lines intersect.
- `POST /v1/geo/relocation`: Relocated chart recalculation for candidate geographical destinations.
- `POST /v1/geo/local-space`: Local space horizon azimuths projected from the birth location.

---

## 9. Module 7: Modern Psychological & Evolutionary Astrology (20 Endpoints)

Archetypal and psychological models of deep personality integration.

### Endpoints:
- **Stephen Arroyo (5 Endpoints)**:
  - `POST /v1/psychological/modern/arroyo/element-integration`: Psycho-dynamic elemental integration and deficient element compensation.
  - `POST /v1/psychological/modern/arroyo/water-houses-trauma`: Analysis of 4th, 8th, and 12th houses (emotional complexes and psychic trauma).
- **Liz Greene (5 Endpoints)**:
  - `POST /v1/psychological/modern/greene/archetypal-figures`: Shadow, Anima/Animus, and heroic archetypal figures.
  - `POST /v1/psychological/modern/greene/saturn-shadow`: Saturnine defense mechanisms, inferiority complexes, and authority projection.
- **Dane Rudhyar (5 Endpoints)**:
  - `POST /v1/psychological/modern/rudhyar/lunation-phase`: 8-phase lunation cycle (New Moon, Crescent, First Quarter, Gibbous, Full, Disseminating, Last Quarter, Balsamic).
  - `POST /v1/psychological/modern/rudhyar/symbolic-degrees`: Sabian symbol degree-by-degree keynote synthesis.
- **Evolutionary Astrology (5 Endpoints)**:
  - `POST /v1/evolutionary/nodal-axis-detail`: Lunar nodal axis karmic orientation (South Node comfort zone vs. North Node evolutionary imperative).
  - `POST /v1/evolutionary/pluto-natal-condition`: Pluto's house and sign condition as root soul desire.

---

## 10. Module 8: Business, Financial & Family Astrology (27 Endpoints)

Corporate timing, wealth generation, and systemic family dynamics.

### Endpoints:
- **Business Astrology (12 Endpoints)**:
  - `POST /v1/business/founder-personality`: Founder archetypal profile and corporate leadership style.
  - `POST /v1/business/ideal-industry`: Recommended economic sectors and enterprise verticals.
  - `POST /v1/business/electional-day`: Auspicious launch date screening for commercial registration.
- **Financial Astrology (10 Endpoints)**:
  - `POST /v1/financial/market-timing`: Planetary market timing and sector cycles.
  - `POST /v1/financial/wealth-house`: Condition of 2nd (liquid assets), 8th (investments/debt), and 11th (gains) houses.
  - `POST /v1/financial/investor-archetype`: Risk profile, spending psychology, and capital allocation archetype.
- **Family Astrology (5 Endpoints)**:
  - `POST /v1/family/genogram`: Intergenerational synastry and astrological genogram mapping.
  - `POST /v1/family/saturn-return-cycles`: Generational Saturn return timing and structural milestones.

---

## 11. Module 9: Quadruple Numerology (50 Endpoints)

Complete numerological profiles across 4 world traditions (10 endpoints per tradition).

### Traditions & Routes:
- `POST /v1/numerology/pythagorean/*`: Life Path, Expression, Soul Urge, Birthday, Personality, Maturity, Personal Year, Pinnacles, Challenges, Balance.
- `POST /v1/numerology/chaldean/*`: Cheiro 1–8 vibration system with compound and root number synthesis.
- `POST /v1/numerology/kabbalistic/*`: Hebrew phonetic Gematria vibration profile.
- `POST /v1/numerology/vedic/*`: Ank Jyotish Navagraha planetary number connections.

---

## 12. Module 10: Tarot, Divination, Esoteric & Wellness (114 Endpoints)

Comprehensive symbolic divination engines.

### Key Systems:
- **Tarot (66 Endpoints)**:
  - Rider-Waite-Smith (35): Spreads (Celtic Cross, Horseshoe, Decision, Relationship, Year Ahead, Shadow Work), card draws, keywords, advice.
  - Marseille (21): Spreads (Cross, Decision, Hero, Spiritual), major arcana keys, timing calculations.
  - Lenormand (10): Grand Tableau (36 houses), Line of Five, 9-Card Square, daily card.
- **Elder Futhark Runes (5 Endpoints)**: Single, Three-Rune, Nine-Rune cast, and zodiacal correlations.
- **Agrippa Geomancy (16 Endpoints)**: Calculations for all 16 classical geomantic figures (Fortuna Major, Fortuna Minor, Puella, Puer, etc.).
- **Esoteric & Wellness (27 Endpoints)**: Angel numbers, dream decode, crystal prescriptions, medical astrology organ rulerships, biorhythms.

---

## 13. Module 11: AI Reports, Interpretations & Localization (34 Endpoints)

Structured generative intelligence and multilingual synthesis.

### Key Endpoints:
- `POST /v1/ai/interpret/natal`: Structured psychological and vocational synthesis of natal chart.
- `POST /v1/ai/interpret/synastry`: Relationship dynamics and tension points synthesis.
- `POST /v1/reports/ai-natal-narrative`: Long-form 5,000–8,000 word publication-ready narrative report.
- `POST /v1/content-localization/translate-astro`: Astrological translation maintaining technical terms across 21 supported languages.
