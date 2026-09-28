---
name: bazi-lunar
description: "Trigger: bazi-lunar, bazi mcp, chinese lunar calendar, four pillars jiazi, true solar time bazi, ten gods shi shen, huangli almanac, lucky hours, lunar festivals, auspicious dates. Motor MCP nativo de BaZi, Astrologia China y Calendario Lunar."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---
# BaZi Four Pillars & Chinese Lunar MCP Engine

Deterministic, zero-latency Chinese metaphysics computation suite providing Four Pillars of Destiny (八字), BaZi compatibility, Huangli almanac (老黄历), lucky hours, moon phases, and traditional festivals.

## Core Architecture

BaZi-Lunar operates via native local stdio MCP server `lunar` (`/home/zerops/.local/bin/lunar-mcp-server`), running on Python 3.12 and `zhdate`. Calculations run 100% offline with sub-10ms latency and zero external token costs.

- **Primary Reference**: [references/usage.md](file:///var/www/.agents/skills/bazi-lunar/references/usage.md) — Tool parameters, request payloads, and JSON output schemas for all 20 tools.
- **Infrastructure Guide**: [references/infra.md](file:///var/www/.agents/skills/bazi-lunar/references/infra.md) — Local stdio runtime, resources (`lunar://...`), timezone offsets, and CoHaLo process hygiene.

## Available Functional Clusters (20 Tools)

1. **BaZi Four Pillars & Compatibility**: Core Four Pillars chart (`calculate_bazi`) and dual-chart synastry (`calculate_bazi_compatibility`).
2. **Auspicious Date Selection**: Date rating (`check_auspicious_date`), range search (`find_good_dates`), batch review (`batch_check_dates`), and comparison (`compare_dates`).
3. **Huangli Almanac & Lucky Hours**: Daily fortune (`get_daily_fortune`) and 12-branch lucky hours (`get_lucky_hours`).
4. **Zodiac Analysis**: Natal animal traits (`get_zodiac_info`) and zodiac compatibility (`check_zodiac_compatibility`).
5. **Calendar Conversion**: Bidirectional solar-to-lunar (`solar_to_lunar`) and lunar-to-solar (`lunar_to_solar`).
6. **Moon Phases & Astronomy**: Phase calculations (`get_moon_phase`, `get_moon_calendar`, `get_moon_influence`, `predict_moon_phases`).
7. **Traditional Festivals**: Cultural observances (`get_lunar_festivals`, `get_next_festival`, `get_festival_details`, `get_annual_festivals`).

## Critical Workflows

1. **Timezone Offset**: Default `timezone_offset` is `8` (CST / UTC+8). For other locations, supply signed UTC offset (e.g. `-5` EST, `1` CET).
2. **Deterministic Invocation**: Call via `call_mcp_tool(ServerName="lunar", ToolName="<tool>", Arguments={...})`.
3. **Process Hygiene (CoHaLo)**: Maximum 10s execution timeouts (`timeout 10s`), `WaitMsBeforeAsync: 10000`, Zero Orphaned Tasks (`manage_task action="kill"`).
4. **Circuit Breakers**: Max 2 retries on failure; verify required fields (`four_pillars`, `score`) before passing data downstream.

## Quick Reference Table

| Cluster | Key MCP Tool | Required Arguments | Output |
|---|---|---|---|
| Four Pillars | `calculate_bazi` | `birth_datetime` | `four_pillars`, `day_master`, `element_analysis` |
| Compatibility | `calculate_bazi_compatibility` | `birth_datetime1`, `birth_datetime2` | `compatibility_score`, `element_relationship_analysis` |
| Date Selection | `check_auspicious_date` | `date`, `activity` | `score`, `auspiciousness_level`, `good_for`, `avoid` |
| Almanac | `get_daily_fortune` | `date` | `lucky_directions`, `favorable_colors`, `yi`, `ji` |
| Lucky Hours | `get_lucky_hours` | `date` | 12 two-hour branch periods and ratings |
| Solar to Lunar | `solar_to_lunar` | `solar_date` | `lunar_year`, `lunar_month`, `lunar_day`, `zodiac_info` |
| Moon Phase | `get_moon_phase` | `date` | `phase_name`, `illumination`, `phase_angle` |
| Festivals | `get_annual_festivals` | `year` | Chronological list of traditional festivals |

## Output Contract

Parse JSON directly with `jq`. Validate `four_pillars` or `score` before forwarding data downstream.
