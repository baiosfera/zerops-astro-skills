# Zmanim MCP Infrastructure, Mathematical Formulas & Governance

Technical configuration guide, FastMCP stdio daemon architecture, KosherJava mathematical algorithms, and CoHaLo process hygiene for the Zmanim Halachic Solar calculation engine.

---

## 1. FastMCP Daemon Architecture

The Zmanim MCP server runs locally within the Antigravity container as a dedicated stdio daemon:
- **Server Name**: `zmanim`
- **MCP Framework**: `FastMCP("zmanim_mcp")`
- **Launcher**: `uvx zmanim-mcp-server`
- **Core Library**: `zmanim` (Python port of the canonical `KosherJava/zmanim` library).
- **Core Classes**: `zmanim.zmanim_calendar.ZmanimCalendar`, `zmanim.util.geo_location.GeoLocation`, `zmanim.astronomical_calendar.AstronomicalCalendar`, `NOAACalculator`.
- **Latency & Performance**: Sub-10ms response times for all calculations.
- **Network & Secrets**: 100% offline local computation, zero network dependencies, zero API keys.

---

## 2. Astronomical & Geometric Constraints

### A. Sea-Level Horizon Reference (`use_elevation = False`)
In `ZmanimCalendar.__init__`, the elevation correction flag is set to:
```python
self.use_elevation = False
```
All solar depression and transit calculations are computed relative to the geometric sea-level horizon ($0\text{ m}$ elevation). Atmospheric refraction is adjusted using the standard NOAA astronomical refraction formula ($34\text{ arcminutes}$ of refraction plus $16\text{ arcminutes}$ of solar semi-diameter, totaling $50\text{ arcminutes}$ / $0.833^\circ$ at the horizon).

### B. Timezone Resolution
The server requires an explicit IANA timezone identifier (e.g. `"Asia/Jerusalem"`, `"America/New_York"`, `"Europe/London"`). The underlying engine converts the target calendar date and geographical coordinates into localized UTC timestamps.

---

## 3. Mathematical Engine: Sha'ot Zmaniyot (Proportional Hours)

Halachic daytime is partitioned into 12 proportional hours (**Sha'ot Zmaniyot**):
$$\text{Sha'ah Zmanit} = \frac{\text{Day End} - \text{Day Start}}{12}$$

### A. Opinion of the Gr"a (Vilna Gaon)
- **Day Definition**: From visible sunrise (**HaNetz**, upper limb) to visible sunset (**Shkiya**, upper limb).
- **Proportional Hour Formula**:
  $$\text{Sha'ah Zmanit}_{\text{Gra}} = \frac{\text{Sunset} - \text{Sunrise}}{12}$$
- **Halachic Deadlines**:
  - **Sof Zman Shema (Gr"a)**: $\text{Sunrise} + 3 \times \text{Sha'ah Zmanit}_{\text{Gra}}$
  - **Sof Zman Tefila (Gr"a)**: $\text{Sunrise} + 4 \times \text{Sha'ah Zmanit}_{\text{Gra}}$
  - **Chatzos (Solar Noon)**: $\text{Sunrise} + 6 \times \text{Sha'ah Zmanit}_{\text{Gra}}$ (Exact NOAA solar transit)
  - **Mincha Gedola**: $\text{Sunrise} + 6.5 \times \text{Sha'ah Zmanit}_{\text{Gra}} = \text{Chatzos} + 0.5 \times \text{Sha'ah Zmanit}_{\text{Gra}}$
  - **Mincha Ketana**: $\text{Sunrise} + 9.5 \times \text{Sha'ah Zmanit}_{\text{Gra}} = \text{Sunset} - 2.5 \times \text{Sha'ah Zmanit}_{\text{Gra}}$
  - **Plag HaMincha**: $\text{Sunrise} + 10.75 \times \text{Sha'ah Zmanit}_{\text{Gra}} = \text{Sunset} - 1.25 \times \text{Sha'ah Zmanit}_{\text{Gra}}$

### B. Opinion of Magen Avraham (MG"A - 72-Minute Fixed Offset)
- **Day Definition**: From dawn (**Alos**) to nightfall (**Tzeis**).
- **Engine Implementation**: This server implements the classical fixed 72-minute temporal offset:
  $$\text{Alos}_{72} = \text{Sunrise} - 72\text{ minutes}$$
  $$\text{Tzeis}_{72} = \text{Sunset} + 72\text{ minutes}$$
  $$\text{Total Duration}_{\text{MGA}} = (\text{Sunset} + 72) - (\text{Sunrise} - 72) = (\text{Sunset} - \text{Sunrise}) + 144\text{ minutes}$$
  $$\text{Sha'ah Zmanit}_{\text{MGA}} = \text{Sha'ah Zmanit}_{\text{Gra}} + \frac{144}{12} = \text{Sha'ah Zmanit}_{\text{Gra}} + 12\text{ minutes}$$
- **Halachic Deadlines**:
  - **Sof Zman Shema (MG"A)**: $\text{Alos}_{72} + 3 \times \text{Sha'ah Zmanit}_{\text{MGA}}$
  - **Sof Zman Tefila (MG"A)**: $\text{Alos}_{72} + 4 \times \text{Sha'ah Zmanit}_{\text{MGA}}$

---

## 4. Response Formatting Policy

The server provides two serialization options:
- `"markdown"` (Default): Formatted text tables intended for human viewing.
- `"json"`: Structured JSON object containing both human-friendly strings (`times`) and machine-readable ISO-8601 timestamps (`times_iso`).
- **Rule of Engagement**: All automated agents, orchestrators, and programmatic consumers MUST pass `"response_format": "json"`.

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All invocations to the `zmanim` MCP server MUST adhere to the following constraints:

1. **Strict Execution Timeouts**:
   - Every MCP call is bounded by a 10s maximum timeout (`timeout 10s`).
2. **Circuit Breakers (2-Attempt Limit)**:
   - If an invocation fails due to parameter errors or subprocess crash, retry once with verified arguments.
   - If the second attempt fails, trip the circuit breaker, log the trace, and halt.
3. **Zero Orphaned Tasks**:
   - Clean up any background tasks via `manage_task action="kill"`.
4. **Sensor Attestation**:
   - Verify that `times` contains all 12 halachic timestamps and `times_iso` contains valid ISO-8601 strings.
