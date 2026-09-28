# NASA JPL Horizons & Open APIs Infrastructure & Governance

Technical deployment guide, endpoints, authentication, rate limits, error taxonomy, and CoHaLo process hygiene for the NASA JPL Horizons system, SBDB CAD API, and NASA Open APIs.

---

## 1. Endpoints & Rate Limits

| Service | Base URL | Auth Requirement | Rate Limit | Output Structure |
|---|---|---|---|---|
| **NASA JPL Horizons API** | `https://ssd.jpl.nasa.gov/api/horizons.api` | None (Public Open Access) | Generous batch limit (~hundreds/min) | JSON envelope with `.result` string |
| **NASA JPL SBDB CAD API** | `https://ssd-api.jpl.nasa.gov/cad.api` | None (Public Open Access) | Generous batch limit (~hundreds/min) | Native JSON with `fields` and `data` arrays |
| **NASA Open APIs** | `https://api.nasa.gov/` | `api_key=$NASA_API_KEY` | **1,000 requests / hour** | Native JSON (NeoWs, DONKI, APOD) |
| **NASA Open APIs (Demo)** | `https://api.nasa.gov/` | `api_key=DEMO_KEY` | 30 req / hour (50 req / day) | Native JSON |

*Rate Limit Headers on `api.nasa.gov`*: `X-RateLimit-Limit`, `X-RateLimit-Remaining`.

---

## 2. Environment Variables & Secret Ingestion

| Variable Name | Scope | Description | Default Source |
|---|---|---|---|
| `NASA_API_KEY` | Shell / System Env | Master NASA API Key | Sourced from `unisetup` / `/etc/environment` |
| `nasa_apiKey` | Zerops Project Env | Zerops managed platform variable | Auto-injected in ZCP container |

### Safe Reference in Shell Scripts
```bash
# Reference by variable name without standard output leakage
API_KEY="${NASA_API_KEY:-${nasa_apiKey:-DEMO_KEY}}"
```

---

## 3. HTTP Error Codes & In-Payload Diagnostics

| Status / Indicator | Root Cause | Recovery Action |
|---|---|---|
| `400` (Open APIs) | Malformed parameter or date range $> 7$ days in NeoWs | Restrict feed date ranges to $\le 7$ days. |
| `403` (Open APIs) | `api_key` expired or invalid for `api.nasa.gov` | Fall back to `${NASA_API_KEY:-${nasa_apiKey:-DEMO_KEY}}`. |
| `429` (Open APIs) | Hourly limit exceeded on `api.nasa.gov` (1,000 req/hr) | Throttle calls (`sleep 3.6`) or use keyless JPL Horizons/CAD endpoints. |
| `500` / `503` | Upstream NASA server timeout or orbital integrator fault | Retry with exponential backoff (circuit breaker max 2). |
| In-Payload Error (Horizons HTTP 200) | Missing `%3B` for asteroid or invalid date | Check `.error` field or verify presence of `$$SOE` before parsing. |

---

## 4. JPL Horizons Output Parsing (`$$SOE` and `$$EOE`)

Tabulated ephemeris data in JPL Horizons JSON responses is contained within the `.result` string between two standard demarcation markers:
- `$$SOE`: Start of Ephemeris.
- `$$EOE`: End of Ephemeris.

### Shell Extraction Snippet:
```bash
# Extract only CSV ephemeris rows between markers and verify validity
RESPONSE=$(curl -s "https://ssd.jpl.nasa.gov/api/horizons.api?format=json&...")
if echo "$RESPONSE" | jq -e '.error' >/dev/null 2>&1; then
  echo "Horizons Error: $(echo "$RESPONSE" | jq -r '.error')" >&2
  exit 1
fi
echo "$RESPONSE" | jq -r '.result' | awk '/\$\$SOE/{flag=1;next}/\$\$EOE/{flag=0}flag'
```

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All REST API invocations MUST strictly adhere to the following CoHaLo harness constraints:

1. **Strict Execution Timeouts**:
   ```bash
   # Invariant: 10s maximum bounded execution for REST API calls
   timeout 10s curl -s "https://ssd.jpl.nasa.gov/api/horizons.api?..."
   ```
2. **Circuit Breaker Policy (2-Attempt Limit)**:
   - If an API call fails with HTTP `500` or network timeout, the harness permits at most **2 autonomous retry attempts** with backoff (`sleep 5.0`).
   - If the second attempt fails, the circuit opens: execution halts immediately, error logs are preserved, and human escalation is triggered without entering infinite loops.
3. **Zero Orphaned Tasks**:
   - Any background process or detached subshell must be audited and terminated via `manage_task action="kill"` before concluding an execution turn.
