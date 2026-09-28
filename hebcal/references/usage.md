# HebCal Jewish Calendar & Zmanim REST Technical Usage Manual

Comprehensive developer and agent reference manual for the HebCal calculation engine (`https://www.hebcal.com/`), covering all 8 canonical modules with zero PII, strict parameterization, and CoHaLo bounded execution.

---

## 1. Module 1: Date Converter & Parashat HaShavua (`/converter`)

Converts bidirectionally between Gregorian and Hebrew calendar dates and identifies the active weekly Torah portion or holiday events.

### A. Gregorian to Hebrew Date Conversion (Single Day)
```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/converter?cfg=json&date=<YYYY-MM-DD>&g2h=1&strict=1" | jq '.'
```
*Note*: Append `&gs=on` if the event occurred after sunset (initiating the next Hebrew day).

### JSON Response Schema:
```json
{
  "gy": "<YYYY>",
  "gm": "<MM>",
  "gd": "<DD>",
  "hy": "<HEBREW_YEAR>",
  "hm": "<HEBREW_MONTH>",
  "hd": "<HEBREW_DAY>",
  "hebrew": "כ״ב בְּתַמּוּז תש״ן",
  "heDateParts": {
    "y": "תש״ן",
    "m": "תמוז",
    "d": "כ״ב"
  },
  "events": [
    "Parashat Pinchas"
  ]
}
```

### B. Gregorian to Hebrew Date Conversion (Continuous Range, Max 180 Days)
```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/converter?cfg=json&start=<START_YYYY-MM-DD>&end=<END_YYYY-MM-DD>&g2h=1&strict=1" | jq '.hdates'
```

### C. Hebrew to Gregorian Date Conversion (Single Day)
```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/converter?cfg=json&hy=<HEBREW_YEAR>&hm=<HEBREW_MONTH>&hd=<HEBREW_DAY>&h2g=1&strict=1" | jq '.'
```
*Valid Hebrew months*: `Nisan`, `Iyyar`, `Sivan`, `Tamuz`, `Av`, `Elul`, `Tishrei`, `Cheshvan`, `Kislev`, `Tevet`, `Sh'vat`, `Adar`, `Adar1`, `Adar2`.

### D. Hebrew to Gregorian Date Conversion (Range, 2–180 Days)
```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/converter?cfg=json&hy=<HEBREW_YEAR>&hm=<HEBREW_MONTH>&hd=<HEBREW_DAY>&h2g=1&ndays=<N>&strict=1" | jq '.hdates'
```

---

## 2. Module 2: Daily Zmanim REST Engine (`/zmanim`)

Calculates 34 classical halachic prayer timestamps with seconds precision based on NOAA solar algorithms and Jean Meeus astronomical equations.

### A. Daily Halachic Times (Coordinates Mode)
```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/zmanim?cfg=json&latitude=<LAT>&longitude=<LNG>&tzid=<TIMEZONE_STR>&date=<YYYY-MM-DD>&sec=1" | jq '.times'
```

### B. Daily Halachic Times (GeoNames ID with Topographical Elevation)
```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/zmanim?cfg=json&geonameid=<GEONAMEID>&date=<YYYY-MM-DD>&elev=<METERS>&ue=on&sec=1" | jq '.times'
```

### C. Multi-Day Zmanim Range (Up to 180 Days)
```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/zmanim?cfg=json&latitude=<LAT>&longitude=<LNG>&tzid=<TIMEZONE_STR>&start=<START_YYYY-MM-DD>&end=<END_YYYY-MM-DD>&sec=1" | jq '.times'
```

### Catalog of 34 Halachic Marks (`times`):
| Timestamp Key | Definition & Halachic Authority |
|---|---|
| `chatzotNight` | Solar midnight (sunset + 6 halachic hours) |
| `alotHaShachar` | Astronomical dawn (Sun 16.1° below horizon) |
| `alosBaalHatanya` | Dawn according to Baal HaTanya (16.9° / 72 min at equinox) |
| `misheyakir` | Earliest tzitzit recognition (Sun 11.5° below horizon) |
| `misheyakirMachmir` | Strict tzitzit recognition (Sun 10.2° below horizon) |
| `dawn` | Civil dawn (Sun 6.0° below horizon) |
| `sunrise` | Refraction-adjusted visible sunrise |
| `seaLevelSunrise` | Sunrise at sea-level horizon without elevation correction |
| `sofZmanShma` | Latest Shema cutoff according to Gr"a (sunrise + 3 halachic hours) |
| `sofZmanShmaMGA` | Latest Shema according to Magen Avraham (dawn to nightfall basis) |
| `sofZmanShmaMGA16Point1` | Shema MGA with 16.1° dawn |
| `sofZmanShmaMGA19Point8` | Shema MGA with 19.8° dawn (90 min at equinox) |
| `sofZmanShmaBaalHatanya` | Shema according to Baal HaTanya |
| `sofZmanTfilla` | Latest Shacharit prayer cutoff according to Gr"a (sunrise + 4 halachic hours) |
| `sofZmanTfillaMGA` | Latest Shacharit cutoff according to MGA |
| `sofZmanTfillaMGA16Point1` | Shacharit MGA with 16.1° dawn |
| `sofZmanTfillaMGA19Point8` | Shacharit MGA with 19.8° dawn |
| `sofZmanTfillaBaalHatanya` | Shacharit cutoff according to Baal HaTanya |
| `chatzot` | Midday solar noon (astronomical zenith) |
| `minchaGedola` | Earliest Mincha time according to Gr"a (sunrise + 6.5 halachic hours) |
| `minchaGedolaMGA` | Earliest Mincha according to MGA |
| `minchaGedolaBaalHatanya` | Earliest Mincha according to Baal HaTanya |
| `minchaKetana` | Standard Mincha time according to Gr"a (sunrise + 9.5 halachic hours) |
| `minchaKetanaMGA` | Standard Mincha according to MGA |
| `minchaKetanaBaalHatanya` | Standard Mincha according to Baal HaTanya |
| `plagHaMincha` | Plag HaMincha window according to Gr"a (sunrise + 10.75 halachic hours) |
| `plagHaMinchaBaalHatanya` | Plag HaMincha according to Baal HaTanya |
| `sunset` | Refraction-adjusted visible sunset (Shkiya) |
| `seaLevelSunset` | Sunset at sea level |
| `beinHaShmashos` | Twilight window (13.5 minutes before Tzeit 7.083°) |
| `dusk` | Civil dusk (Sun 6.0° below horizon) |
| `tzeit7083deg` | Nightfall with 3 medium stars (Sun 7.083° below horizon) |
| `tzeit85deg` | Strict nightfall with 3 small stars (Sun 8.5° below horizon) |
| `tzeit42min` / `tzeit50min` | Nightfall at fixed minutes after visible sunset |
| `tzeit72min` | Nightfall of Rabbeinu Tam (72 fixed minutes post-sunset) |
| `tzaisBaalHatanya` | Nightfall according to Baal HaTanya |

---

## 3. Module 3: Assur Melacha IoT Mode (`/zmanim?im=1`)

Designed for IoT automation, smart-home relays, and Sabbath mode switches. Evaluates whether work is forbidden at a specific target instant.

```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/zmanim?cfg=json&latitude=<LAT>&longitude=<LNG>&tzid=<TIMEZONE_STR>&im=1&dt=<YYYY-MM-DDTHH:mm:ssZ>" | jq '.status'
```

### JSON Response Schema:
```json
{
  "status": {
    "localTime": "<YYYY-MM-DDTHH:mm:ss-OFFSET>",
    "isAssurBemlacha": true
  }
}
```
*Note*: `isAssurBemlacha` is `true` from candle lighting (default 18 min before sunset) through nightfall (3 small stars, 8.5° solar depression) on Shabbat and Biblical Yom Tov days.

---

## 4. Module 4: Shabbat & Havdalah Fast Shortcut (`/shabbat`)

Optimized weekly endpoint returning candle lighting times, Havdalah, and weekly Parashat HaShavua for a given location.

```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/shabbat?cfg=json&latitude=<LAT>&longitude=<LNG>&tzid=<TIMEZONE_STR>&b=18&M=on&leyning=off" | jq '.items'
```

### Key Parameters:
- `b=<MINUTES>`: Candle lighting offset before sunset (default: 18; Jerusalem: 40; Haifa: 30).
- `M=on`: Havdalah calculated astronomically at 8.5° solar depression (3 small stars).
- `m=<MINUTES>`: Alternative fixed-minute Havdalah (e.g. `m=42`, `m=50`, `m=72`; `m=0` disables Havdalah).
- `leyning=off`: Suppresses verbose Torah reading aliyot payload for fast lightweight responses.
- `lg=<LANG>`: Language/transliteration (`s` Sephardic, `a` Ashkenazic, `he` Hebrew).

---

## 5. Module 5: Jewish Holidays & Fast Days Calendar (`/hebcal`)

Retrieves the complete annual or monthly calendar of Jewish holidays, fasts, and special observances, including Sefirat HaOmer.

### A. Annual Major & Minor Holidays with Fast Days
```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&min=on&mod=on&nx=on&mf=on&ss=on&year=<YYYY>&month=x" | jq '.items'
```

### B. Sefirat HaOmer (49-Day Count with Kabbalistic Sefirot)
To query the Omer count in JSON format, query `/hebcal` with the `o=on` flag:
```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/hebcal?v=1&cfg=json&o=on&year=<YYYY>&yt=G" | jq '[.items[] | select(.category == "omer")]'
```

### Event Flags Reference:
| Flag | Observance Category |
|---|---|
| `maj=on` | Major Biblical Holidays (Pesach, Shavuot, Sukkot, Rosh Hashana, Yom Kippur) |
| `yto=on` | Yom Tov Only (work-forbidden holidays) |
| `min=on` | Minor Holidays (Purim, Chanukah, Tu BiShvat, Lag BaOmer) |
| `mod=on` | Modern Holidays (Yom HaShoah, Yom HaZikaron, Yom HaAtzma'ut, Yom Yerushalayim) |
| `nx=on` | Rosh Chodesh (New Month) |
| `mf=on` | Minor Fasts (Tzom Gedaliah, 10th of Tevet, Ta'anit Esther, 17th of Tammuz) |
| `ss=on` | Special Shabbatot (Shekalim, Zachor, Parah, HaChodesh, HaGadol, Chazon, Nachamu) |
| `s=on` | Weekly Parashat HaShavua |
| `o=on` | Days of the Omer count |
| `molad=on` | Exact astronomical Molad (New Moon announcement) |
| `yzkr=on` | Yizkor memorial prayer dates |
| `mvch=on` | Shabbat Mevarchim |
| `i=on` / `i=off` | Israel schedule (1-day Yom Tov) vs Diaspora schedule (2-day Yom Tov) |

---

## 6. Module 6: Daily Learning Schedules (Yomi — 15 Channels)

Retrieves daily Torah, Talmud, and Halacha study tracks via the `/hebcal` engine.

### A. Daily Daf Yomi (Talmud Bavli) & Rambam
```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/hebcal?v=1&cfg=json&F=on&dr1=on&start=<YYYY-MM-DD>&end=<YYYY-MM-DD>" | jq '.items'
```

### 15 Canonical Yomi Channel Flags:
| Flag | Study Track | Content Description |
|---|---|---|
| `F=on` | Daf Yomi (Bavli) | Daily folio of Babylonian Talmud |
| `dw=on` | Daf-a-Week | Slower-paced Daf study program |
| `yyomi=on` | Yerushalmi Yomi | Jerusalem Talmud (Vilna edition) |
| `yys=on` | Yerushalmi Yomi | Jerusalem Talmud (Schottenstein edition) |
| `myomi=on` | Mishna Yomi | Two daily mishnayot |
| `nyomi=on` | Nach Yomi | Daily chapter of Prophets and Writings |
| `dty=on` | Tanakh Yomi | Daily section of Tanakh |
| `dps=on` | Daily Psalms | Daily Tehillim according to monthly/weekly division |
| `dr1=on` | Rambam (1 Chapter) | Mishneh Torah 1 chapter per day cycle |
| `dr3=on` | Rambam (3 Chapters) | Mishneh Torah 3 chapters per day cycle |
| `dsm=on` | Sefer HaMitzvot | Daily study of Rambam's Sefer HaMitzvot |
| `dksa=on` | Kitzur Shulchan Aruch | Daily code of Jewish law |
| `ahsy=on` | Aruch HaShulchan Yomi | Daily Halachic code study |
| `dcc=on` | Chofetz Chaim | Daily laws of proper speech |
| `dshl=on` | Shemirat HaLashon | Daily ethical treatise on speech |
| `dpa=on` | Pirkei Avot | Summer Sabbath afternoon ethics chapters |

---

## 7. Module 7: Leyning & Torah Reading API (`/leyning`)

Specialized endpoint returning the complete liturgical breakdown of Torah and Haftarah readings for any date, including aliyot 1–7, Maftir, triennial portions, and Monday/Thursday weekday readings.

### A. Shabbat and Holiday Torah Reading
```bash
timeout 10s curl -s -A "GentleAI-Hebcal/1.0" \
  "https://www.hebcal.com/leyning?cfg=json&date=<YYYY-MM-DD>&triennial=on" | jq '.'
```

### JSON Response Schema:
```json
{
  "name": {
    "en": "Parashat Bereshit",
    "he": "פרשת בראשית"
  },
  "summary": "Genesis 1:1-6:8",
  "fullkriyah": {
    "1": { "k": "Genesis", "b": "1:1", "e": "1:5", "v": 5, "p": 1 },
    "2": { "k": "Genesis", "b": "1:6", "e": "1:8", "v": 3, "p": 1 },
    "3": { "k": "Genesis", "b": "1:9", "e": "1:13", "v": 5, "p": 1 },
    "4": { "k": "Genesis", "b": "1:14", "e": "1:19", "v": 6, "p": 1 },
    "5": { "k": "Genesis", "b": "1:20", "e": "1:23", "v": 4, "p": 1 },
    "6": { "k": "Genesis", "b": "1:24", "e": "1:31", "v": 8, "p": 1 },
    "7": { "k": "Genesis", "b": "2:1", "e": "2:3", "v": 3, "p": 1 },
    "M": { "k": "Genesis", "b": "2:1", "e": "2:3", "v": 3, "p": 1 }
  },
  "haftara": "Isaiah 42:5-43:10",
  "weekday": {
    "1": { "k": "Genesis", "b": "1:1", "e": "1:5", "v": 5 },
    "2": { "k": "Genesis", "b": "1:6", "e": "1:8", "v": 3 },
    "3": { "k": "Genesis", "b": "1:9", "e": "1:13", "v": 5 }
  },
  "triennial": {
    "yearNum": 1,
    "1": { "k": "Genesis", "b": "1:1", "e": "1:5", "v": 5 }
  }
}
```

---

## 8. Module 8: Yahrzeit & Hebrew Anniversaries (`POST /yahrzeit`)

Calculates up to 20 years of future Yahrzeit dates, Hebrew birthdays, or wedding anniversaries.

- **Protocol**: Strictly HTTPS POST.
- **Content-Type**: `application/x-www-form-urlencoded`.

```bash
timeout 10s curl -s -X POST -A "GentleAI-Hebcal/1.0" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "cfg=json&v=yahrzeit&years=20&n1=<PERSON_NAME>&t1=Yahrzeit&y1=<YYYY>&m1=<MM>&d1=<DD>&s1=off&yizkor=on" \
  "https://www.hebcal.com/yahrzeit" | jq '.items'
```

### Form Parameters:
| Parameter | Value / Description |
|---|---|
| `cfg=json` | Output JSON response format |
| `v=yahrzeit` | Calculation target type |
| `years=<N>` | Number of future years to calculate (1–20, default 20) |
| `start=<HEBREW_YEAR>` | Starting Hebrew year (optional) |
| `end=<HEBREW_YEAR>` | Ending Hebrew year (optional) |
| `yizkor=on` | Include dates of Yizkor prayer recitations (Yom Kippur, Shemini Atzeret, Pesach, Shavuot) |
| `hebdate=on` | Include Hebrew date formatted strings in output |
| `nX` | Name of person for record index $X$ ($X=1, 2, 3...$) |
| `tX` | Event type: `Yahrzeit` \| `Birthday` \| `Anniversary` \| `Other` |
| `yX`, `mX`, `dX` | Gregorian year, month, day of event |
| `sX=on` | Event occurred after sunset (advances Hebrew day by +1) |
| `hyX`, `hmX`, `hdX` | Alternative Hebrew date of event (if Gregorian is unknown) |

---

## 9. Error Handling & CoHaLo Bounded Execution

HebCal APIs return deterministic HTTP error codes:
- **HTTP 400 Bad Request**: Invalid parameters (e.g. invalid date format with `strict=1`, missing `tzid` when coordinates are supplied, invalid month name).
- **HTTP 404 Not Found**: Deprecated or invalid URL paths (e.g. `/yomi` or `/omer`).
- **HTTP 429 Too Many Requests**: Client exceeded 90 requests per 10-second rolling window. Backoff with exponential jitter before retrying.

### Production Execution Pattern:
```bash
#!/usr/bin/env bash
set -euo pipefail

URL="https://www.hebcal.com/zmanim?cfg=json&latitude=${LAT}&longitude=${LNG}&tzid=${TIMEZONE_STR}&date=${TARGET_DATE}&sec=1"

RESPONSE=$(timeout 10s curl -s -w "\n%{http_code}" -A "GentleAI-Hebcal/1.0" "$URL")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
  echo "$BODY" | jq '.times'
else
  echo "HebCal API request failed with HTTP status $HTTP_CODE" >&2
  exit 1
fi
```
