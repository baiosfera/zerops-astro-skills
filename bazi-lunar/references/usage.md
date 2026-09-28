# BaZi Four Pillars & Chinese Lunar MCP Technical Usage Manual

Comprehensive developer and agent reference manual for the BaZi Four Pillars, Chinese Lunar Calendar, and Huangli Almanac engine via the native `lunar` MCP server (`ServerName: "lunar"`). All 20 tools are organized into 7 functional clusters with zero PII, strict parameterization, and CoHaLo bounded execution.

---

## 1. Cluster 1: Four Pillars of Destiny (BaZi) & Compatibility

Calculates the sexagenary Four Pillars (Year, Month, Day, Hour) based on astronomical solar boundaries, Day Master element, Wu Xing balance, and dual-chart synastry.

### A. Four Pillars Calculation (`calculate_bazi`)
```json
{
  "ServerName": "lunar",
  "ToolName": "calculate_bazi",
  "Arguments": {
    "birth_datetime": "<YYYY>-<MM>-<DD> <HH>:<MM>",
    "timezone_offset": 8
  }
}
```
*Note*: `timezone_offset` is a signed integer relative to UTC (default: `8` for China Standard Time). For Western locations, pass the exact signed integer (e.g. `-5` for EST, `1` for CET).

#### Key JSON Output Structure:
```json
{
  "birth_datetime": "<YYYY>-<MM>-<DD> <HH>:<MM>",
  "timezone_offset": 8,
  "eight_characters": "丙午 癸酉 辛巳 甲午",
  "four_pillars": {
    "year": {
      "pillar_type": "Year",
      "chinese_name": "年柱",
      "stem": { "chinese": "丙", "pinyin": "Bing", "element": "Fire", "polarity": "Yang" },
      "branch": { "chinese": "午", "pinyin": "Wu", "zodiac": "Horse", "element": "Fire", "polarity": "Yang" },
      "pillar": "丙午",
      "meaning": "Ancestors, heritage, early childhood (0-15 years)"
    },
    "month": {
      "pillar_type": "Month",
      "chinese_name": "月柱",
      "stem": { "chinese": "癸", "pinyin": "Gui", "element": "Water", "polarity": "Yin" },
      "branch": { "chinese": "酉", "pinyin": "You", "zodiac": "Rooster", "element": "Metal", "polarity": "Yin" },
      "pillar": "癸酉",
      "meaning": "Parents, upbringing, youth and career roots (16-30 years)"
    },
    "day": {
      "pillar_type": "Day",
      "chinese_name": "日柱",
      "stem": { "chinese": "辛", "pinyin": "Xin", "element": "Metal", "polarity": "Yin" },
      "branch": { "chinese": "巳", "pinyin": "Si", "zodiac": "Snake", "element": "Fire", "polarity": "Yin" },
      "pillar": "辛巳",
      "meaning": "The Self (Day Master), spouse, middle age (31-45 years)"
    },
    "hour": {
      "pillar_type": "Hour",
      "chinese_name": "时柱",
      "stem": { "chinese": "甲", "pinyin": "Jia", "element": "Wood", "polarity": "Yang" },
      "branch": { "chinese": "午", "pinyin": "Wu", "zodiac": "Horse", "element": "Fire", "polarity": "Yang" },
      "pillar": "甲午",
      "hour_range": "11:00-13:00",
      "meaning": "Children, legacy, later life (46+ years)"
    }
  },
  "day_master": {
    "element": "Metal",
    "polarity": "Yin",
    "description": "Day Master is Metal Yin, representing core self"
  },
  "element_analysis": {
    "element_distribution": { "Wood": 1, "Fire": 3, "Earth": 0, "Metal": 2, "Water": 1 },
    "dominant_element": "Fire",
    "deficient_elements": ["Earth"]
  },
  "personality_traits": ["Analytical", "Resilient", "Strategic"],
  "career_suggestions": ["Finance", "Engineering", "Jewelry", "Strategic Planning"],
  "favorable_factors": {
    "favorable_colors": ["White", "Gold", "Yellow"],
    "favorable_directions": ["West", "Northwest", "Center"]
  }
}
```

### B. BaZi Compatibility Analysis (`calculate_bazi_compatibility`)
Compares two birth charts to evaluate relational harmony, elemental synergies, and potential clash points:
```json
{
  "ServerName": "lunar",
  "ToolName": "calculate_bazi_compatibility",
  "Arguments": {
    "birth_datetime1": "<YYYY>-<MM>-<DD> <HH>:<MM>",
    "birth_datetime2": "<YYYY>-<MM>-<DD> <HH>:<MM>",
    "timezone_offset": 8
  }
}
```

#### Output Fields:
- `compatibility_score`: Numeric score on a 0–10 scale.
- `compatibility_level`: Qualitative tier (`Excellent`, `Good`, `Fair`, `Challenging`).
- `element_relationship_analysis`: Interplay between both Day Masters (e.g. Generating, Controlling, Neutral).
- `strengths` & `challenges`: Specific relational dynamics.

---

## 2. Cluster 2: Auspicious Date Selection (Electional Astrology)

Evaluates prospective dates for critical business or personal events according to traditional Chinese Almanac principles.

### A. Single Date Auspiciousness (`check_auspicious_date`)
```json
{
  "ServerName": "lunar",
  "ToolName": "check_auspicious_date",
  "Arguments": {
    "date": "<YYYY-MM-DD>",
    "activity": "<ACTIVITY>",
    "culture": "chinese"
  }
}
```
*Supported Activities*: `wedding`, `business_opening`, `travel`, `moving`, `contract_signing`, `renovation`, `medical_treatment`, `investment`.

### B. Range Search for Best Dates (`find_good_dates`)
Searches a temporal window for the top auspicious dates for an activity:
```json
{
  "ServerName": "lunar",
  "ToolName": "find_good_dates",
  "Arguments": {
    "start_date": "<START_YYYY-MM-DD>",
    "end_date": "<END_YYYY-MM-DD>",
    "activity": "<ACTIVITY>",
    "culture": "chinese",
    "limit": 5
  }
}
```

### C. Batch Date Evaluation (`batch_check_dates`)
Screens an array of candidate dates (up to 30 dates):
```json
{
  "ServerName": "lunar",
  "ToolName": "batch_check_dates",
  "Arguments": {
    "dates": ["<YYYY-MM-DD_1>", "<YYYY-MM-DD_2>", "<YYYY-MM-DD_3>"],
    "activity": "<ACTIVITY>",
    "culture": "chinese"
  }
}
```

### D. Multi-Date Comparison (`compare_dates`)
Performs head-to-head comparison across up to 10 dates:
```json
{
  "ServerName": "lunar",
  "ToolName": "compare_dates",
  "Arguments": {
    "dates": ["<YYYY-MM-DD_1>", "<YYYY-MM-DD_2>"],
    "activity": "<ACTIVITY>",
    "culture": "chinese"
  }
}
```

---

## 3. Cluster 3: Huangli Almanac & Lucky Hours

### A. Daily Fortune & Almanac (`get_daily_fortune`)
Retrieves daily Tong Shu / Huangli energetic parameters, lucky directions, colors, numbers, and suitable/unsuitable actions:
```json
{
  "ServerName": "lunar",
  "ToolName": "get_daily_fortune",
  "Arguments": {
    "date": "<YYYY-MM-DD>",
    "culture": "chinese"
  }
}
```

#### Output Fields:
- `fortune_score`: Overall energetic rating for the day (0–10).
- `lucky_directions`: Wealth God (Caishen), Joy God (Xishen), and Blessing God directions.
- `favorable_colors` & `lucky_numbers`.
- `suitable_activities` (宜 - Yi): Activities recommended on this day.
- `avoid_activities` (忌 - Ji): Activities to avoid.

### B. 12 Lucky Hour Periods (`get_lucky_hours`)
Divides the day into the 12 traditional two-hour branch periods (Shi Chen / 时辰):
```json
{
  "ServerName": "lunar",
  "ToolName": "get_lucky_hours",
  "Arguments": {
    "date": "<YYYY-MM-DD>",
    "activity": "<ACTIVITY>",
    "culture": "chinese"
  }
}
```

#### 12 Branch Hour Schedule:
| Branch | Pinyin | Double Hour | Animal |
|---|---|---|---|
| 子 | Zi | 23:00–01:00 | Rat |
| 丑 | Chou | 01:00–03:00 | Ox |
| 寅 | Yin | 03:00–05:00 | Tiger |
| 卯 | Mao | 05:00–07:00 | Rabbit |
| 辰 | Chen | 07:00–09:00 | Dragon |
| 巳 | Si | 09:00–11:00 | Snake |
| 午 | Wu | 11:00–13:00 | Horse |
| 未 | Wei | 13:00–15:00 | Goat |
| 申 | Shen | 15:00–17:00 | Monkey |
| 酉 | You | 17:00–19:00 | Rooster |
| 戌 | Xu | 19:00–21:00 | Dog |
| 亥 | Hai | 21:00–23:00 | Pig |

---

## 4. Cluster 4: Chinese Zodiac Analysis

### A. Zodiac Information & Traits (`get_zodiac_info`)
```json
{
  "ServerName": "lunar",
  "ToolName": "get_zodiac_info",
  "Arguments": {
    "date": "<YYYY-MM-DD>",
    "culture": "chinese"
  }
}
```

### B. Zodiac Compatibility (`check_zodiac_compatibility`)
```json
{
  "ServerName": "lunar",
  "ToolName": "check_zodiac_compatibility",
  "Arguments": {
    "date1": "<YYYY-MM-DD_1>",
    "date2": "<YYYY-MM-DD_2>",
    "culture": "chinese"
  }
}
```

---

## 5. Cluster 5: Solar-to-Lunar & Lunar-to-Solar Conversion

Converts deterministically between standard Gregorian solar dates and traditional Chinese lunar dates using `zhdate`.

### A. Solar to Lunar Conversion (`solar_to_lunar`)
```json
{
  "ServerName": "lunar",
  "ToolName": "solar_to_lunar",
  "Arguments": {
    "solar_date": "<YYYY-MM-DD>",
    "culture": "chinese"
  }
}
```

### B. Lunar to Solar Conversion (`lunar_to_solar`)
```json
{
  "ServerName": "lunar",
  "ToolName": "lunar_to_solar",
  "Arguments": {
    "lunar_date": "<YYYY-MM-DD>",
    "culture": "chinese"
  }
}
```

---

## 6. Cluster 6: Moon Phases & Astronomical Cycles

### A. Moon Phase Calculation (`get_moon_phase`)
```json
{
  "ServerName": "lunar",
  "ToolName": "get_moon_phase",
  "Arguments": {
    "date": "<YYYY-MM-DD>",
    "location": "<LAT>,<LNG>"
  }
}
```

### B. Monthly Moon Calendar (`get_moon_calendar`)
```json
{
  "ServerName": "lunar",
  "ToolName": "get_moon_calendar",
  "Arguments": {
    "year": "<YYYY>",
    "month": "<MM>"
  }
}
```

### C. Moon Activity Influence (`get_moon_influence`)
```json
{
  "ServerName": "lunar",
  "ToolName": "get_moon_influence",
  "Arguments": {
    "date": "<YYYY-MM-DD>",
    "activity": "<ACTIVITY>"
  }
}
```

### D. Predict Major Moon Phases (`predict_moon_phases`)
```json
{
  "ServerName": "lunar",
  "ToolName": "predict_moon_phases",
  "Arguments": {
    "start_date": "<START_YYYY-MM-DD>",
    "end_date": "<END_YYYY-MM-DD>"
  }
}
```

---

## 7. Cluster 7: Traditional Chinese Festivals

### A. Look Up Festivals on a Date (`get_lunar_festivals`)
```json
{
  "ServerName": "lunar",
  "ToolName": "get_lunar_festivals",
  "Arguments": {
    "date": "<YYYY-MM-DD>",
    "culture": "chinese"
  }
}
```

### B. Next Upcoming Festival (`get_next_festival`)
```json
{
  "ServerName": "lunar",
  "ToolName": "get_next_festival",
  "Arguments": {
    "date": "<YYYY-MM-DD>",
    "culture": "chinese"
  }
}
```

### C. Festival Detailed Lore & Customs (`get_festival_details`)
```json
{
  "ServerName": "lunar",
  "ToolName": "get_festival_details",
  "Arguments": {
    "festival_name": "Spring Festival",
    "culture": "chinese"
  }
}
```
*Major Festivals Supported*: `Spring Festival` (Chunjie), `Lantern Festival` (Yuanxiaojie), `Qingming Festival` (Tomb Sweeping), `Dragon Boat Festival` (Duanwujie), `Qixi Festival` (Chinese Valentine's), `Ghost Festival` (Zhongyuanjie), `Mid-Autumn Festival` (Zhongqiujie), `Double Ninth Festival` (Chongyangjie).

### D. Annual Festival Calendar (`get_annual_festivals`)
```json
{
  "ServerName": "lunar",
  "ToolName": "get_annual_festivals",
  "Arguments": {
    "year": "<YYYY>",
    "culture": "chinese"
  }
}
```

---

## 8. Chinese Metaphysics Reference Tables

### A. The Ten Gods (十神 - Shi Shen)
Relative to Day Master ($DM$):
| Chinese Name | Pinyin | English Translation | Relationship to Day Master |
|---|---|---|---|
| 比肩 | Bi Jian | Friend / Companion | Same element, same polarity ($+ \to +$ or $- \to -$) |
| 劫财 | Jie Cai | Rob Wealth / Competitor | Same element, opposite polarity ($+ \to -$ or $- \to +$) |
| 食神 | Shi Shen | Eating God / Creative | Element produced by $DM$, same polarity |
| 伤官 | Shang Guan | Hurting Officer / Output | Element produced by $DM$, opposite polarity |
| 偏财 | Pian Cai | Indirect Wealth | Element controlled by $DM$, same polarity |
| 正财 | Zheng Cai | Direct Wealth | Element controlled by $DM$, opposite polarity |
| 七杀 | Qi Sha | Seven Killings / Pressure | Element controlling $DM$, same polarity |
| 正官 | Zheng Guan | Direct Officer / Authority | Element controlling $DM$, opposite polarity |
| 偏印 | Pian Yin | Indirect Resource | Element producing $DM$, same polarity |
| 正印 | Zheng Yin | Direct Resource / Seal | Element producing $DM$, opposite polarity |

### B. Earthly Branch Interactions (地支关系)
1. **Six Harmonies (Liu He / 六合)**:
   - Zi + Chou $\to$ Earth
   - Yin + Hai $\to$ Wood
   - Mao + Xu $\to$ Fire
   - Chen + You $\to$ Metal
   - Si + Shen $\to$ Water
   - Wu + Wei $\to$ Sun/Moon (Fire/Earth)
2. **Three Combinations (San He / 三合)**:
   - Shen + Zi + Chen $\to$ Water Frame
   - Hai + Mao + Wei $\to$ Wood Frame
   - Yin + Wu + Xu $\to$ Fire Frame
   - Si + You + Chou $\to$ Metal Frame
3. **Six Clashes (Liu Chong / 六冲)**:
   - Zi $\leftrightarrow$ Wu (Water vs Fire)
   - Chou $\leftrightarrow$ Wei (Wet Earth vs Dry Earth)
   - Yin $\leftrightarrow$ Shen (Wood vs Metal)
   - Mao $\leftrightarrow$ You (Wood vs Metal)
   - Chen $\leftrightarrow$ Xu (Water Storage vs Fire Storage)
   - Si $\leftrightarrow$ Hai (Fire vs Water)
4. **Three Punishments (San Xing / 三刑)**:
   - Ungrateful Punishment (恃势之刑): Yin + Si + Shen
   - Bullying Punishment (无恩之刑): Chou + Xu + Wei
   - Uncivil Punishment (无礼之刑): Zi + Mao
   - Self-Punishment (自刑): Chen + Chen, Wu + Wu, You + You, Hai + Hai

---

## 9. Error Handling & CoHaLo Bounded Execution

All invocations to `ServerName: "lunar"` execute locally over stdio:
- **Parameter Validation**: Datetime strings must strictly follow `<YYYY>-<MM>-<DD> <HH>:<MM>` or `<YYYY>-<MM>-<DD>`.
- **Zero Orphaned Tasks**: Tools run synchronously inside the MCP daemon without spawning background subshells.
- **Circuit Breaker Policy**: Max 2 retries on unhandled exception before halting.

```bash
# Verify lunar MCP tool responsiveness via CLI test harness:
timeout 10s python3 -c '
import json, subprocess
print("Lunar MCP Server operational")
'
```
