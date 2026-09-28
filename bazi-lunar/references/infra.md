# BaZi & Chinese Lunar Infrastructure, MCP Stdio Transports & Governance

Technical configuration guide, stdio MCP daemon architecture, resources, timezone standards, and CoHaLo process hygiene for the BaZi Four Pillars & Chinese Lunar engines.

---

## 1. Native MCP Stdio Daemon Architecture

BaZi and Chinese Lunar calculations operate entirely locally within the Antigravity container via the native stdio MCP server:
- **Server Name**: `lunar`
- **Binary Path**: `/home/zerops/.local/bin/lunar-mcp-server`
- **Underlying Runtime**: Python 3.12 virtualenv managed by `uv` (`/home/zerops/.local/share/uv/tools/lunar-mcp-server/`).
- **Core Libraries**: `lunar_mcp_server` (v1.2.1), `zhdate` (Chinese lunar calendar conversion), `lunardate`.
- **Latency & Performance**: Sub-10ms response times for all calculations.
- **Network & Secrets**: 100% offline, zero network egress required, zero external tokens, zero API keys.

---

## 2. Native MCP Resources (`list_resources`)

The `lunar` server exposes static reference resources via the `lunar://` URI scheme:

| Resource URI | Description & Contents |
|---|---|
| `lunar://zodiac/animals` | 12 Zodiac animals, Wu Xing element affiliations, Yin/Yang polarity, and personality traits |
| `lunar://elements/five` | Five Elements (Wood, Fire, Earth, Metal, Water), generating (Sheng) and controlling (Ke) cycles |
| `lunar://festivals/major` | The 8 major traditional Chinese festivals, solar term bounds, and cultural significances |
| `lunar://stems-branches/heavenly` | The 10 Heavenly Stems (Jia, Yi, Bing, Ding, Wu, Ji, Geng, Xin, Ren, Gui) |
| `lunar://stems-branches/earthly` | The 12 Earthly Branches (Zi, Chou, Yin, Mao, Chen, Si, Wu, Wei, Shen, You, Xu, Hai) |

Agents can read these directly via `read_resource(ServerName="lunar", Uri="...")` to ground astrological interpretations without consuming calculation tokens.

---

## 3. Timezone Standards & True Solar Time

### A. Timezone Offset (`timezone_offset`)
The `lunar` MCP server standardizes timezone calculation via signed integer offsets relative to UTC:
- **Default**: `8` (China Standard Time / UTC+8, Beijing time).
- **Western / Global Charts**: Supply the exact integer offset corresponding to the subject's birth location:
  - Eastern Standard Time (EST / New York): `-5` (or `-4` during EDT)
  - Central European Time (CET / Madrid, Paris): `1` (or `2` during CEST)
  - Greenwich Mean Time (GMT / London): `0` (or `1` during BST)
  - Japan Standard Time (JST / Tokyo): `9`

### B. True Solar Time Formula (真太阳时)
For precise natal charts near pillar transition boundaries, civil wall-clock time can be adjusted to physical True Solar Time:

$$T_{\text{true}} = T_{\text{std}} + 4 \times (\lambda - \lambda_{\text{std}}) + \text{EOT}$$

- $\lambda$: Longitude of birth location in decimal degrees (East positive, West negative).
- $\lambda_{\text{std}}$: Timezone reference meridian ($\text{Timezone Offset} \times 15^\circ$).
- $\text{EOT}$: Equation of Time in minutes.

---

## 4. Zi-Hour Day Rollover Policy (子时)

The Zi hour (子时, 23:00–01:00) represents the nocturnal transition between two consecutive days:
- **Early Zi (子初, 23:00–23:59)**: In WenZhen (问真) and modern standard Chinese metaphysics, the Day Pillar rolls over to the **next day** at 23:00.
- **Late Zi (子正, 00:00–00:59)**: Belongs fully to the new solar day.
- When querying `calculate_bazi` for birth moments between 23:00 and 23:59, the hour pillar is assigned the Zi branch with the stem derived from the subsequent day's Day Master.

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All invocations to the `lunar` MCP server MUST strictly adhere to the following CoHaLo harness constraints:

1. **Strict Execution Timeouts**:
   - Every MCP call is bounded by a 10s maximum timeout (`timeout 10s`).
2. **Circuit Breaker Policy (2-Attempt Limit)**:
   - If an MCP invocation encounters an unexpected daemon error, retry at most once with freshly validated arguments.
   - If the second attempt fails, trip the circuit breaker, preserve diagnostic logs, and escalate.
3. **Zero Orphaned Tasks**:
   - The MCP stdio server communicates over pipes managed by the supervisor. Never leave backgrounded shells or unmonitored async tasks.
4. **Sensor Attestation**:
   - Verify that output payloads contain non-null core keys (`four_pillars`, `day_master`, `score`, `lunar_year`) before accepting calculations as valid.
