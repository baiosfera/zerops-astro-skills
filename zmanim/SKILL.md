---
name: zmanim
description: "Trigger: zmanim, zmanim mcp, jewish halachic times, shaot zmaniyot gra mga, shabbat times havdalah, plag hamincha, chatzot, shema tefila times. Motor MCP de calculo solar halajico y tiempos de oracion judia."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---
# Zmanim Halachic Solar & Jewish Calendar MCP Engine

Deterministic, high-precision astronomical and halachic prayer time calculator implementing Sha'ot Zmaniyot (proportional hours) according to Gr"a and Magen Avraham standards across 6 native MCP tools.

## Core Architecture

Zmanim operates via local stdio Python MCP server `zmanim` (`uvx zmanim-mcp-server` / `FastMCP("zmanim_mcp")`) backed by KosherJava, calculating NOAA solar transitions with zero network latency.

- **Primary Reference**: [references/usage.md](file:///var/www/.agents/skills/zmanim/references/usage.md) — Exact tool invocations, argument constraints, and two-block JSON outputs (`times` and `times_iso`) for all 6 tools.
- **Infrastructure Guide**: [references/infra.md](file:///var/www/.agents/skills/zmanim/references/infra.md) — Sha'ah Zmanit formulas (Gr"a vs MG"A 72-minute fixed offset), sea-level geometry, and CoHaLo process hygiene.

## Available Native Tools (6 Tools)

1. **Daily Zmanim Schedule (`zmanim_get_daily_times`)**: Complete daily prayer timeline (Alos 72, Sunrise, Shema Gr"a/MG"A, Tefila Gr"a/MG"A, Chatzos, Mincha, Sunset, Tzeis 72).
2. **Latest Shema Cutoff (`zmanim_get_shema_times`)**: 3 proportional hours according to Gr"a (Netz to Shkia) and Magen Avraham (Alos 72 to Tzeis 72).
3. **Latest Morning Prayer Cutoff (`zmanim_get_tefila_times`)**: 4 proportional hours according to Gr"a and MG"A.
4. **Mincha Afternoon Windows (`zmanim_get_mincha_times`)**: Mincha Gedola (6.5h), Mincha Ketana (9.5h), and Plag HaMincha (10.75h).
5. **Shabbat & Havdalah Times (`zmanim_get_shabbat_times`)**: Candle lighting (configurable offset) and Havdalah (Tzeis 72).
6. **Astronomical Solar Transitions (`zmanim_get_sunrise_sunset`)**: Geometric sea-level sunrise (HaNetz) and sunset (Shkiya).

## Critical Workflows

1. **Mandatory JSON Response Format**: Default `response_format` is `"markdown"`. Always pass `response_format: "json"` for programmatic parsing in downstream pipelines.
2. **Required Geographic Inputs**: Supply `location` (descriptive string), `latitude`, `longitude`, and IANA `time_zone` (e.g. `"Asia/Jerusalem"`, `"America/New_York"`).
3. **Process Hygiene (CoHaLo)**: Maximum 10s execution timeouts (`timeout 10s`), `WaitMsBeforeAsync: 10000`, Zero Orphaned Tasks (`manage_task action="kill"`).
4. **Circuit Breakers**: Max 2 retries on runtime failure before escalation; verify presence of `times` and `times_iso` blocks.

## Quick Reference Table

| Native MCP Tool | Required Arguments | Key Outputs |
|---|---|---|
| `zmanim_get_daily_times` | `location`, `latitude`, `longitude`, `time_zone` | Full day timeline (`times` & `times_iso`) |
| `zmanim_get_shema_times` | `location`, `latitude`, `longitude`, `time_zone` | `sof_zman_shema_gra`, `sof_zman_shema_mga` |
| `zmanim_get_tefila_times` | `location`, `latitude`, `longitude`, `time_zone` | `sof_zman_tefila_gra`, `sof_zman_tefila_mga` |
| `zmanim_get_mincha_times` | `location`, `latitude`, `longitude`, `time_zone` | `chatzos`, `mincha_gedola`, `plag_hamincha` |
| `zmanim_get_shabbat_times` | `location`, `latitude`, `longitude`, `time_zone` | `candle_lighting`, `havdalah_tzeis_72` |
| `zmanim_get_sunrise_sunset` | `location`, `latitude`, `longitude`, `time_zone` | `sunrise`, `sunset`, ISO timestamps |

## Output Contract

Parse JSON directly with `jq`. Use `times` for UI display and `times_iso` for programmatic calculations.
