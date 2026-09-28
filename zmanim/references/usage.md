# Zmanim Halachic Solar & Jewish Calendar MCP Usage Manual

Comprehensive developer and agent reference manual for the Zmanim Model Context Protocol (MCP) server (`ServerName: "zmanim"`), covering all 6 native tools with verbatim JSON contracts, zero PII, strict parameterization, and CoHaLo bounded execution.

---

## 1. Primary Tool: `zmanim_get_daily_times` (Comprehensive Daily Schedule)

Calculates the complete schedule of halachic prayer times for any geographical coordinate and date. Returns both formatted strings in `"times"` and ISO-8601 timestamps with local offsets in `"times_iso"`.

### Input Parameters:
```json
{
  "ServerName": "zmanim",
  "ToolName": "zmanim_get_daily_times",
  "Arguments": {
    "location": "<LOCATION_NAME>",
    "latitude": "<LAT>",
    "longitude": "<LNG>",
    "time_zone": "<TIMEZONE_STR>",
    "date": "<YYYY-MM-DD>",
    "response_format": "json"
  }
}
```

### Argument Constraints:
| Parameter | Type | Required | Constraints / Default | Description |
|---|---|---|---|---|
| `location` | string | **Yes** | `1 <= length <= 100` | Human-readable location identifier (e.g. descriptive name). |
| `latitude` | number | **Yes** | `-90.0 <= lat <= 90.0` | Decimal latitude coordinate. |
| `longitude` | number | **Yes** | `-180.0 <= lng <= 180.0` | Decimal longitude coordinate. |
| `time_zone` | string | **Yes** | IANA identifier | Valid IANA timezone (e.g. `"Asia/Jerusalem"`, `"America/New_York"`). |
| `date` | string \| null | No | `YYYY-MM-DD` (default: null) | Target date. Defaults to current date if omitted. |
| `response_format` | string | No | Enum `["json", "markdown"]` | Output format. Defaults to `"markdown"`. Must be `"json"` for agents. |

### Verbatim Output JSON Schema:
```json
{
  "location": "<LOCATION_NAME>",
  "date": "<YYYY-MM-DD>",
  "timezone": "<TIMEZONE_STR>",
  "times": {
    "alos_hashachar_72": "<YYYY-MM-DD hh:mm AM/PM>",
    "sunrise": "<YYYY-MM-DD hh:mm AM/PM>",
    "sof_zman_shema_gra": "<YYYY-MM-DD hh:mm AM/PM>",
    "sof_zman_shema_mga": "<YYYY-MM-DD hh:mm AM/PM>",
    "sof_zman_tefila_gra": "<YYYY-MM-DD hh:mm AM/PM>",
    "sof_zman_tefila_mga": "<YYYY-MM-DD hh:mm AM/PM>",
    "chatzos": "<YYYY-MM-DD hh:mm AM/PM>",
    "mincha_gedola": "<YYYY-MM-DD hh:mm AM/PM>",
    "mincha_ketana": "<YYYY-MM-DD hh:mm AM/PM>",
    "plag_hamincha": "<YYYY-MM-DD hh:mm AM/PM>",
    "sunset": "<YYYY-MM-DD hh:mm AM/PM>",
    "tzeis_hakochavim_72": "<YYYY-MM-DD hh:mm AM/PM>"
  },
  "times_iso": {
    "alos_hashachar_72": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
    "sunrise": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
    "sof_zman_shema_gra": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
    "sof_zman_shema_mga": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
    "sof_zman_tefila_gra": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
    "sof_zman_tefila_mga": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
    "chatzos": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
    "mincha_gedola": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
    "mincha_ketana": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
    "plag_hamincha": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
    "sunset": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
    "tzeis_hakochavim_72": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>"
  }
}
```

---

## 2. Tool 2: `zmanim_get_shema_times` (Latest Shema Recitation)

Calculates the halachic deadline for reading the morning Shema (end of the 3rd proportional hour):
- **Gr"a**: 3 Sha'ot Zmaniyot after Sunrise (HaNetz).
- **Magen Avraham (MG"A)**: 3 Sha'ot Zmaniyot after Dawn (Alos 72 minutes before sunrise).

### Invocation:
```json
{
  "ServerName": "zmanim",
  "ToolName": "zmanim_get_shema_times",
  "Arguments": {
    "location": "<LOCATION_NAME>",
    "latitude": "<LAT>",
    "longitude": "<LNG>",
    "time_zone": "<TIMEZONE_STR>",
    "date": "<YYYY-MM-DD>",
    "response_format": "json"
  }
}
```

### Verbatim Output Schema:
```json
{
  "location": "<LOCATION_NAME>",
  "date": "<YYYY-MM-DD>",
  "timezone": "<TIMEZONE_STR>",
  "sof_zman_shema_gra": "<YYYY-MM-DD hh:mm AM/PM>",
  "sof_zman_shema_mga": "<YYYY-MM-DD hh:mm AM/PM>",
  "sof_zman_shema_gra_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
  "sof_zman_shema_mga_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>"
}
```

---

## 3. Tool 3: `zmanim_get_tefila_times` (Latest Morning Prayer / Shacharit)

Calculates the halachic cutoff for Shacharit prayer (end of the 4th proportional hour):
- **Gr"a**: 4 Sha'ot Zmaniyot after Sunrise.
- **MG"A**: 4 Sha'ot Zmaniyot after Alos 72.

### Invocation:
```json
{
  "ServerName": "zmanim",
  "ToolName": "zmanim_get_tefila_times",
  "Arguments": {
    "location": "<LOCATION_NAME>",
    "latitude": "<LAT>",
    "longitude": "<LNG>",
    "time_zone": "<TIMEZONE_STR>",
    "date": "<YYYY-MM-DD>",
    "response_format": "json"
  }
}
```

### Verbatim Output Schema:
```json
{
  "location": "<LOCATION_NAME>",
  "date": "<YYYY-MM-DD>",
  "timezone": "<TIMEZONE_STR>",
  "sof_zman_tefila_gra": "<YYYY-MM-DD hh:mm AM/PM>",
  "sof_zman_tefila_mga": "<YYYY-MM-DD hh:mm AM/PM>",
  "sof_zman_tefila_gra_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
  "sof_zman_tefila_mga_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>"
}
```

---

## 4. Tool 4: `zmanim_get_mincha_times` (Afternoon Prayer Windows)

Calculates the key afternoon prayer moments:
- **Chatzos**: Solar midday (astronomical zenith).
- **Mincha Gedola**: Earliest Mincha time (6.5 proportional hours after sunrise, 30 min after Chatzos).
- **Mincha Ketana**: Preferred Mincha time (9.5 proportional hours after sunrise).
- **Plag HaMincha**: Boundary window (10.75 proportional hours after sunrise, 1.25 hours before sunset).

### Invocation:
```json
{
  "ServerName": "zmanim",
  "ToolName": "zmanim_get_mincha_times",
  "Arguments": {
    "location": "<LOCATION_NAME>",
    "latitude": "<LAT>",
    "longitude": "<LNG>",
    "time_zone": "<TIMEZONE_STR>",
    "date": "<YYYY-MM-DD>",
    "response_format": "json"
  }
}
```

### Verbatim Output Schema:
```json
{
  "location": "<LOCATION_NAME>",
  "date": "<YYYY-MM-DD>",
  "timezone": "<TIMEZONE_STR>",
  "chatzos": "<YYYY-MM-DD hh:mm AM/PM>",
  "mincha_gedola": "<YYYY-MM-DD hh:mm AM/PM>",
  "mincha_ketana": "<YYYY-MM-DD hh:mm AM/PM>",
  "plag_hamincha": "<YYYY-MM-DD hh:mm AM/PM>",
  "chatzos_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
  "mincha_gedola_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
  "mincha_ketana_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
  "plag_hamincha_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>"
}
```

---

## 5. Tool 5: `zmanim_get_shabbat_times` (Shabbat Candle Lighting & Havdalah)

Calculates Friday candle lighting (Hadlakat Nerot) and Saturday night Havdalah (Tzeis HaKochavim 72 minutes post-sunset).

### Invocation:
```json
{
  "ServerName": "zmanim",
  "ToolName": "zmanim_get_shabbat_times",
  "Arguments": {
    "location": "<LOCATION_NAME>",
    "latitude": "<LAT>",
    "longitude": "<LNG>",
    "time_zone": "<TIMEZONE_STR>",
    "date": "<YYYY-MM-DD>",
    "candle_lighting_offset": 18,
    "response_format": "json"
  }
}
```
*Note*: `candle_lighting_offset` accepts integers between 1 and 60 minutes (standard: 18 min; Jerusalem: 40 min; Haifa: 30 min).

### Verbatim Output Schema:
```json
{
  "location": "<LOCATION_NAME>",
  "date": "<YYYY-MM-DD>",
  "timezone": "<TIMEZONE_STR>",
  "candle_lighting_offset_minutes": 18,
  "candle_lighting": "<YYYY-MM-DD hh:mm AM/PM>",
  "sunset": "<YYYY-MM-DD hh:mm AM/PM>",
  "havdalah_tzeis_72": "<YYYY-MM-DD hh:mm AM/PM>",
  "candle_lighting_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
  "sunset_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
  "havdalah_tzeis_72_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>"
}
```

---

## 6. Tool 6: `zmanim_get_sunrise_sunset` (Astronomical Solar Transitions)

Calculates geometric visible sunrise (HaNetz HaChama) and sunset (Shkiyat HaChama).

### Invocation:
```json
{
  "ServerName": "zmanim",
  "ToolName": "zmanim_get_sunrise_sunset",
  "Arguments": {
    "location": "<LOCATION_NAME>",
    "latitude": "<LAT>",
    "longitude": "<LNG>",
    "time_zone": "<TIMEZONE_STR>",
    "date": "<YYYY-MM-DD>",
    "response_format": "json"
  }
}
```

### Verbatim Output Schema:
```json
{
  "location": "<LOCATION_NAME>",
  "date": "<YYYY-MM-DD>",
  "timezone": "<TIMEZONE_STR>",
  "sunrise": "<YYYY-MM-DD hh:mm AM/PM>",
  "sunset": "<YYYY-MM-DD hh:mm AM/PM>",
  "sunrise_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>",
  "sunset_iso": "<YYYY-MM-DDTHH:MM:SS.ffffff+TZ:00>"
}
```

---

## 7. Halachic Timestamp Definitions Reference Catalog

| Output Timestamp Key | Halachic Concept | Calculation Methodology in Engine |
|---|---|---|
| `alos_hashachar_72` | Dawn (Alos) | Fixed 72 minutes before visible sunrise (`sunrise - 72 min`). |
| `sunrise` | Sunrise (HaNetz) | Sea-level refraction-adjusted solar upper limb appearance. |
| `sof_zman_shema_gra` | Latest Shema (Gr"a) | Sunrise + 3 Sha'ot Zmaniyot (proportional hours of Gr"a). |
| `sof_zman_shema_mga` | Latest Shema (MG"A) | Alos 72 + 3 Sha'ot Zmaniyot (proportional hours of MG"A). |
| `sof_zman_tefila_gra` | Latest Shacharit (Gr"a) | Sunrise + 4 Sha'ot Zmaniyot (Gr"a). |
| `sof_zman_tefila_mga` | Latest Shacharit (MG"A) | Alos 72 + 4 Sha'ot Zmaniyot (MG"A). |
| `chatzos` | Solar Midday | Exact astronomical transit (midpoint between sunrise and sunset). |
| `mincha_gedola` | Earliest Mincha | Sunrise + 6.5 Sha'ot Zmaniyot (Chatzos + 0.5 hour). |
| `mincha_ketana` | Standard Mincha | Sunrise + 9.5 Sha'ot Zmaniyot (Sunset - 2.5 hours). |
| `plag_hamincha` | Plag HaMincha | Sunrise + 10.75 Sha'ot Zmaniyot (Sunset - 1.25 hours). |
| `sunset` | Sunset (Shkiya) | Sea-level refraction-adjusted solar upper limb disappearance. |
| `tzeis_hakochavim_72` | Nightfall (Tzeis) | Fixed 72 minutes after visible sunset (`sunset + 72 min`). |
| `candle_lighting` | Candle Lighting | Sunset minus `candle_lighting_offset` minutes (default 18 min). |
| `havdalah_tzeis_72` | Havdalah | Tzeis HaKochavim at 72 minutes post-sunset. |

---

## 8. CoHaLo Execution & Process Hygiene Pattern

All calls to the `zmanim` MCP server execute synchronously over local stdio:
- Enforce a 10-second timeout on all agent tool executions (`timeout 10s`).
- Always pass `response_format: "json"` to bypass the default Markdown formatter.
- Validate the presence of both `times` and `times_iso` before forwarding results downstream.
