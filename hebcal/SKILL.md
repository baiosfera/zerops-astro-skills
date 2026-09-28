---
name: hebcal
description: "Trigger: hebcal, hebcal api, hebrew date converter, zmanim rest, shabbat havdalah, leyning torah, yahrzeit, assur melacha. Motor REST de calendario judio, conversion hebrea y festividades."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---
# HebCal Jewish Calendar & Zmanim REST Engine

Developer-first Jewish calendar, halachic timing, Torah reading, and Hebrew anniversary REST API suite providing sub-200ms responses with open CORS access.

## Core Architecture

HebCal operates via public high-speed JSON REST endpoints (`https://www.hebcal.com/`) with open CORS access and no API keys required. Requests must include a descriptive User-Agent (`GentleAI-Hebcal/1.0`).

- **Primary Reference**: [references/usage.md](file:///var/www/.agents/skills/hebcal/references/usage.md) — Comprehensive REST cURL templates across all 8 modules (including `/leyning` and `POST /yahrzeit`).
- **Infrastructure Guide**: [references/infra.md](file:///var/www/.agents/skills/hebcal/references/infra.md) — Base URLs, global geocoding, rate limits (90 req/10s), Cloudflare edge caching, and CoHaLo process hygiene.

## Available Engines & Modules

1. **Date Converter & Parashat HaShavua (`/converter`)**: Gregorian-Hebrew bidirectional conversion (single/range) with Torah portion, nikud, and gematria.
2. **Daily Zmanim & Assur Melacha (`/zmanim`)**: 34 halachic timestamps (Gr"a/MGA, seconds precision `sec=1`, elevation) and IoT work-forbidden status (`im=1`).
3. **Shabbat & Havdalah Engine (`/shabbat`)**: Candle lighting, Havdalah (8.5° / 42/50/72 min), Parasha, and Haftarah.
4. **Jewish Holidays & Sefirat HaOmer (`/hebcal`)**: Full holiday cycle, fast days, Rosh Chodesh, and 49-day Omer count (`o=on`).
5. **Daily Learning Schedules (`/hebcal`)**: 15 study tracks including Daf Yomi (`F=on`), Rambam 1/3 chapters (`dr1=on`, `dr3=on`), Mishna, and Tehilim.
6. **Leyning & Torah Reading API (`/leyning`)**: Full Kriyah aliyot 1–7 + Maftir, Haftarah breakdown, weekday readings, and triennial cycle.
7. **Yahrzeit & Hebrew Anniversaries (`/yahrzeit`)**: 20-year multi-person memorial, birthday, and anniversary calculation via HTTPS POST.

## Critical Workflows

1. **JSON Output Parameter**: Always supply `cfg=json` in every HebCal endpoint call.
2. **Descriptive User-Agent**: Pass `-A "GentleAI-Hebcal/1.0"` to avoid Cloudflare WAF scraping blocks.
3. **Seconds-Level Precision**: Pass `sec=1` to `/zmanim` for exact astronomical seconds precision.
4. **Process Hygiene (CoHaLo)**: Maximum 10s execution timeouts (`timeout 10s`), `WaitMsBeforeAsync: 10000`, Zero Orphaned Tasks (`manage_task action="kill"`).
5. **Circuit Breakers**: Max 2 retries on 500/timeout before escalation; verify HTTP 200 and structured fields.

## Quick Reference Table

| Module | Endpoint Route | Key Parameters |
|---|---|---|
| Date Converter | `GET /converter` | `cfg=json&date=<YYYY-MM-DD>&g2h=1` |
| Daily Zmanim | `GET /zmanim` | `cfg=json&latitude=<LAT>&longitude=<LNG>&tzid=<TZ>&sec=1` |
| Assur Melacha | `GET /zmanim?im=1` | `cfg=json&latitude=<LAT>&longitude=<LNG>&tzid=<TZ>` |
| Shabbat Times | `GET /shabbat` | `cfg=json&geonameid=<ID>&b=18&M=on` |
| Holidays & Omer | `GET /hebcal` | `v=1&cfg=json&maj=on&o=on&year=<YYYY>` |
| Daily Learning | `GET /hebcal` | `v=1&cfg=json&F=on&dr1=on&date=<YYYY-MM-DD>` |
| Torah Reading | `GET /leyning` | `cfg=json&date=<YYYY-MM-DD>` |
| Yahrzeit Memorial | `POST /yahrzeit` | `cfg=json&v=yahrzeit&y1=<YYYY>&m1=<MM>&d1=<DD>` |

## Output Contract

Parse JSON directly with `jq`. Verify `hy`, `times`, or `items` before forwarding results downstream.
