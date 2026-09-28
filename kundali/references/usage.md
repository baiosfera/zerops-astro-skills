# Kundali Jyotish & Shodashavarga MCP Usage Manual

Comprehensive developer and agent reference manual for the Kundali Model Context Protocol (MCP) calculation server (`https://mcp.kundalimcp.com/mcp` / Vedākṣha Engine v15.0.0), covering all 10 native tools across 9 functional modules.

---

## 1. Primary Tool: `kundali` (Vedic Birth Chart Engine)

Computes the core Vedic birth chart, planetary coordinates, houses (Bhavas), active Yogas, Sade Sati windows, and Vimshottari dasha hierarchy.

### Input Arguments:
```json
{
  "birth_datetime": "<YYYY>-<MM>-<DD>T<HH>:<mm>:<ss>",
  "latitude": <LAT>,
  "longitude": <LNG>,
  "school": "parashari",
  "locale": "en",
  "ayanamsa": "lahiri",
  "gender": "male",
  "include": "vargas,classical_rules,events",
  "vargas": ["D1", "D9", "D10", "D60"],
  "dasha_depth": 2
}
```

### Argument Taxonomy:
| Argument | Type | Required | Description |
|---|---|---|---|
| `birth_datetime` | string | Yes | Local naive clock time (`<YYYY>-<MM>-<DD>T<HH>:<mm>:<ss>`). No 'Z', no timezone offset. |
| `latitude` | number | Yes | Decimal latitude in range `[-90.0, 90.0]`. |
| `longitude` | number | Yes | Decimal longitude in range `[-180.0, 180.0]`. |
| `school` | string | Yes | Jyotish school: `"parashari"`, `"jaimini"`, or `"kp"`. |
| `locale` | string | Yes | Language: `"en"`, `"hi"`, `"sa"`, `"ta"`, `"te"`, `"kn"`, `"bn"`. |
| `ayanamsa` | string | No | Sideral ayanamsa: `"lahiri"` (default), `"raman"`, `"kp"`. |
| `gender` | string | No | `"male"` or `"female"`. Unlocks BPHS Ch. 80 Stri-Jataka rules and Beeja/Kshetra tests. |
| `house_system` | string | No | House division system (e.g. `"placidus"`, `"equal"`, `"sripati"`). |
| `domain` | string | No | Target domain (career, marriage, health, wealth, spirituality, etc.). Requires `include=narrative`. |
| `eval_date` | string | No | Target evaluation date (`<YYYY>-<MM>-<DD>`). |
| `transit_date` | string | No | Evaluation moment for transit calculations. |
| `transit_start` / `transit_end` | string | No | Range for transit scans (`<YYYY>-<MM>-<DD>`). Requires `include=transit_events`. |
| `include` | string | No | Comma-separated sections: `vargas`, `classical_rules`, `events`, `transit_events`, `narrative`, `reasoning`, `idl`. |
| `vargas` | array | No | Divisional charts array, e.g. `["D9", "D10", "D60"]`. Requires `include=vargas`. |
| `dasha_depth` | integer | No | Levels 1 to 5 (default 2). Levels $>2$ require `dasha_branch`. |
| `dasha_branch` | string | Conditional | Target branch, e.g. `"shani/budha"`. Required when `dasha_depth > 2`. |
| `dasha_max_level` | integer | No | Highest dasha level to return (0..4). |
| `cache` | string | No | Set to `"skip"` to bypass server cache. |

---

## 2. Module 2: 16 Shodashavarga Divisional Charts

Computes the classical 16 divisional charts of Maharishi Parashara:

| Varga | Sanskrit Name | Primary Analytical Domain |
|---|---|---|
| **D1** | Rashi | Physical body, general vitality, overall destiny |
| **D2** | Hora | Wealth, liquid assets, financial prosperity |
| **D3** | Drekkana | Siblings, courage, motivation, energy |
| **D4** | Chaturthamsha | Fixed assets, property, home, happiness |
| **D7** | Saptamsha | Children, progeny, creative lineage |
| **D9** | **Navamsha** | **Dharma, spouse, inner potential, soul evolution** |
| **D10** | **Dasamsha** | **Career, profession, social status, executive power** |
| **D12** | Dvadasamsha | Parents, lineage, ancestral karma |
| **D16** | Shodashamsha | Vehicles, conveyances, general comforts |
| **D20** | Vimshamsha | Spiritual pursuits, upasana, religious inclinations |
| **D24** | Chaturvimshamsha | Higher learning, academic knowledge, intellect |
| **D27** | Saptavimshamsha | Strengths and weaknesses, subconscious fears |
| **D30** | Trimshamsha | Misfortunes, evils, psychological imbalances |
| **D40** | Khavedamsha | Auspicious and inauspicious karmic effects |
| **D45** | Akshavedamsha | General well-being, character purity |
| **D60** | **Shashtiamsha** | **Ultimate karmic root, past-life momentum** |

---

## 3. Module 3: 6-Factor Shadbala Strength

Evaluates planetary potency across 6 classical components:
1. **Sthana Bala (Positional Strength)**: Uccha (Exaltation), Saptavargiya, Ojhayugma, Kendradi, Drekkana Bala.
2. **Dig Bala (Directional Strength)**: Jupiter/Mercury in 1st, Sun/Mars in 10th, Saturn in 7th, Moon/Venus in 4th.
3. **Kala Bala (Temporal Strength)**: Natonnata, Paksha, Tribhaga, Varsha-Masa-Dina-Hora lords, Ayana, Yuddha Bala.
4. **Chesta Bala (Motional Strength)**: Planetary velocity and retrograde status.
5. **Naisargika Bala (Natural Inherent Strength)**: Sun > Moon > Venus > Jupiter > Mercury > Mars > Saturn.
6. **Drik Bala (Aspectual Strength)**: Aspect load from benefic and malefic grahas.

---

## 4. Module 4: Ashtakoota Milan Tool (`kundali_milan`)

Calculates 36 Gunas relationship and business partnership compatibility using structured partner objects:

### Input Arguments:
```json
{
  "groom": {
    "birth_datetime": "<YYYY>-<MM>-<DD>T<HH>:<mm>:<ss>",
    "latitude": <LAT>,
    "longitude": <LNG>
  },
  "bride": {
    "birth_datetime": "<YYYY>-<MM>-<DD>T<HH>:<mm>:<ss>",
    "latitude": <LAT>,
    "longitude": <LNG>
  },
  "school": "parashari",
  "locale": "en",
  "include_provenance": false,
  "eval_date": "<YYYY>-<MM>-<DD>"
}
```

### 8 Kutas Scoring Matrix (36 Max Points):
- **Varna (1 pt)**: Spiritual and ego compatibility.
- **Vashya (2 pts)**: Mutual attraction and dominance balance.
- **Tara (3 pts)**: Destiny, luck, and longevity harmony.
- **Yoni (4 pts)**: Physical, intimate, and biological affinity.
- **Graha Maitri (5 pts)**: Psychological harmony and mental friendship.
- **Gana (6 pts)**: Temperament (Deva, Manushya, Rakshasa).
- **Bhakoot (7 pts)**: Family growth, health, and financial alignment.
- **Nadi (8 pts)**: Genetic, physiological, and neurological compatibility.

*Doshas Evaluated*: Mangal Dosha (with cancellation rules), Nadi Dosha, Bhakoot Dosha.

---

## 5. Module 5: Life Timeline Tool (`lifemap`)

Maps multi-year life trends, Vimshottari Mahadashas/Antardashas, planetary return cycles, and Sade Sati periods.

### Input Arguments:
```json
{
  "birth_datetime": "<YYYY>-<MM>-<DD>T<HH>:<mm>:<ss>",
  "latitude": <LAT>,
  "longitude": <LNG>,
  "school": "parashari",
  "locale": "en",
  "sample_step": 0.8,
  "include": "life_events"
}
```

### Output Fields:
- `facts.current`: Active Mahadasha, Antardasha, and Pratyantardasha.
- `facts.next_mahadashas`: Timeline of upcoming major cycles.
- `facts.sade_sati`: Exact start, peak, and release dates of Saturn transits over Moon.
- `facts.returns`: Saturn returns (29.5y), Jupiter returns (12y), Rahu/Ketu nodal reversals (18.6y).
- `facts.key_events`: Top 10 projected life milestones.

---

## 6. Module 6: Panchanga Engine (`panchang`)

Returns the five limbs of time for any moment and location:

### Input Arguments:
```json
{
  "datetime": "<YYYY>-<MM>-<DD>T<HH>:<mm>:<ss>",
  "latitude": <LAT>,
  "longitude": <LNG>,
  "locale": "en",
  "include": "windows,timeline"
}
```

### Computed Attributes:
- **5 Extremities**:
  - `tithi`: Lunar day, paksha (Shukla/Krishna), completion percentage, end time.
  - `vara`: Solar weekday and planetary day ruler.
  - `nakshatra`: Lunar mansion (1..27), Pada (1..4), degree span, end time.
  - `yoga`: 27 Solar-Lunar angular combinations (Vishkumbha to Vaidhriti).
  - `karana`: Half-tithi period (Bava to Kimstughna).
- **Inauspicious Windows**: Rahu Kaal, Gulika Kaal, Yamaganda, Dur Muhurtas, Varjya.
- **Auspicious Windows**: Abhijit Muhurta, Brahma Muhurta, Amrita Kaal, Choghadiya (16 periods), Hora (24 planetary hours).
- **Daily Yogas**: Sarvartha Siddhi, Amrita Siddhi, Ravi Yoga, Dagdha Yoga.

---

## 7. Module 7: Observances & Festivals (`festivals`)

Scans solar and lunar tithi observances over a date range up to 400 days following the classical sunrise rule (Muhurta Chintamani).

### Input Arguments:
```json
{
  "start_date": "<YYYY>-<MM>-<DD>",
  "end_date": "<YYYY>-<MM>-<DD>",
  "latitude": <LAT>,
  "longitude": <LNG>,
  "locale": "en",
  "masa_scheme": "amanta",
  "include": "astronomy"
}
```

*Covered Observances*: Ekadashi, Purnima, Amavasya (Somavati, Bhaumavati, Shani Amavasya), Sankashti Chaturthi, Masik Shivaratri, Pradosha Trayodashi, and Surya Sankrantis.

---

## 8. Module 8: Auspicious Electional Timing (`muhurat`) & Scriptural Proofs (`pramaan`)

### A. Auspicious Timing (`muhurat`):
Calculates optimal electional windows for 24 specific activities in either single-moment evaluation or temporal scan mode ($\le$ 31 days).

```json
{
  "datetime": "<YYYY>-<MM>-<DD>T<HH>:<mm>:<ss>",
  "latitude": <LAT>,
  "longitude": <LNG>,
  "event_type": "business_opening",
  "school": "parashari",
  "locale": "en",
  "scan_end": "<YYYY>-<MM>-<DD>",
  "max_windows": 10,
  "native": {
    "birth_datetime": "<YYYY>-<MM>-<DD>T<HH>:<mm>:<ss>",
    "latitude": <LAT>,
    "longitude": <LNG>
  }
}
```

*Supported 24 `event_type` Values*:
`"annaprashan"`, `"bhoomi_pujan"`, `"business_opening"`, `"contract_signing"`, `"convocation"`, `"engagement"`, `"exam_start"`, `"general_auspicious"`, `"griha_pravesh"`, `"journey_start"`, `"loan_repayment"`, `"marriage_ceremony"`, `"medicine_start"`, `"mundana"`, `"name_ceremony"`, `"partnership"`, `"pilgrimage"`, `"property_purchase"`, `"puja"`, `"surgery"`, `"treatment_start"`, `"upanayana"`, `"vehicle_purchase"`, `"vidyarambha"`.

### B. Scriptural Proofs (`pramaan`):
Provides causal verification and classical citations (Brihat Parashara Hora Shastra, Jaimini Upadesha Sutras, Phaladeepika, Saravali) for any astrological claim or placement.

```json
{
  "chart_ref": {
    "birth_datetime": "<YYYY>-<MM>-<DD>T<HH>:<mm>:<ss>",
    "latitude": <LAT>,
    "longitude": <LNG>
  },
  "claim_id": "concept:yoga/gajakesari",
  "school": "parashari",
  "locale": "en",
  "include": "trace,detail,metrics"
}
```

---

## 9. Module 9: Interactive Vedic AI Chat & Engine Status (`chat`, `get_version`, `submit_feedback`)

### A. Classical Vedic Chat (`chat`):
Interactive natural language conversation grounded in classical scriptural rules, with optional natal chart anchoring and transit awareness.

```json
{
  "message": "Analyze career prospects during Jupiter Mahadasha based on 10th house placements.",
  "locale": "en",
  "birth_datetime": "<YYYY>-<MM>-<DD>T<HH>:<mm>:<ss>",
  "latitude": <LAT>,
  "longitude": <LNG>
}
```

### B. Engine Version Status (`get_version`):
Unauthenticated status check returning active engine and protocol version metadata.

```json
{}
```

### C. Feedback Calibration (`submit_feedback`):
Submits structured feedback to the Calibratable Interpretive Layer (CIL) for algorithmic improvement.

```json
{
  "feedback_type": "accuracy",
  "rating": 5,
  "claim_id": "concept:yoga/gajakesari",
  "notes": "Classical rule verified against BPHS Chapter 35 Shloka 12."
}
```
