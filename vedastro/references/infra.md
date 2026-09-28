# VedAstro Infrastructure, PRO Tiers & Governance

Technical deployment guide, pricing tiers, authentication, REST data lake architecture, error taxonomy, and CoHaLo process hygiene for the VedAstro engine (`https://api.vedastro.org/api/`).

---

## 1. Plan Tiers & Rate Limit Architecture

| Dimension | Free Tier | PRO Unlimited Tier (Active User Plan) |
|---|---|---|
| **Price** | $0 / month | **$1 / month** (or $9 / year) |
| **Monthly Calls** | Rate-limited (5 req / min) | **UNLIMITED Calls** (No per-request cost) |
| **Calculation Scope** | All 600+ calculators | **All 600+ calculators + Priority Queue** |
| **Throttling Policy** | Strict `sleep 12.0` | **No artificial delay** (Immediate execution) |
| **Accuracy Engine** | Swiss Ephemeris (NASA JPL) | Swiss Ephemeris (NASA JPL) |
| **Support** | Community / GitHub | Priority Developer Support |

---

## 2. Environment Variables & Secret Ingestion

| Variable Name | Scope | Description | Default Source |
|---|---|---|---|
| `VEDASTRO_API_KEY` | Shell / System Env | Master Subscriber API Key | Sourced from `unisetup` / `/etc/environment` |
| `vedastro_apiKey` | Zerops Project Env | Zerops managed platform variable | Auto-injected in ZCP container |

### Safe Reference in Bash Scripts
```bash
# Reference by variable name without standard output leakage
API_KEY="${VEDASTRO_API_KEY:-${vedastro_apiKey:-}}"
if [ -z "$API_KEY" ]; then
  echo "Error: VEDASTRO_API_KEY is not set in the environment." >&2
  exit 1
fi
```

---

## 3. Date Syntax Rules: POST vs. GET Discrepancy

> [!IMPORTANT]
> VedAstro enforces different date delimiters depending on HTTP method:
> - **POST Requests:** Use forward slash `/` in `StdTime` (`"HH:mm DD/MM/YYYY +ZZ:ZZ"`).
> - **GET Requests:** Use hyphen `-` in URL segments (`.../Time/<HH:mm>/<DD-MM-YYYY>/<+/-ZZ:ZZ>/...`).

---

## 4. Integration Architecture: Direct REST cURL Pipeline

VedAstro is integrated into the multi-agent ecosystem (Oráculo Maestro and diagnostic agents) as a direct REST cURL data lake. This architecture prevents token duplication and context bloat:

1. **Direct Transport**: REST cURL calls execute with bounded execution (`timeout 10s`) and transparent audit headers.
2. **Offline Data Lake**: Raw full-depth JSON payloads are persisted to disk at `raw/json/dumps/` for downstream multi-modal analysis.
3. **Lean Context Feeds**: Extracted domain metrics are saved as typed XML snippets (<2.5 KB) in `raw/feeds/`, strictly preserving context window tokens.

---

## 5. HTTP Error Codes & Recovery Matrix

| HTTP Status | Error String / Status | Cause | Recovery Action |
|---|---|---|---|
| `400` | `Status: "Fail"` | Malformed `StdTime` or missing coordinate fields | Format `StdTime` as `"HH:mm DD/MM/YYYY +ZZ:ZZ"` in [usage.md](file:///var/www/.agents/skills/vedastro/references/usage.md). |
| `401` | `UNAUTHORIZED` | Missing or invalid `x-api-key` | Verify `$VEDASTRO_API_KEY` in environment. |
| `429` | `TOO_MANY_REQUESTS` | Free tier quota exceeded (>5 req/min) | Supply valid PRO `$VEDASTRO_API_KEY` to unlock unlimited requests. |
| `500` | `INTERNAL_SERVER_ERROR` | Upstream computation exception | Retry with exponential backoff (circuit breaker max 2). |

---

## 6. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All REST API invocations MUST strictly adhere to the following CoHaLo harness constraints:

1. **Strict Execution Timeouts**:
   ```bash
   # Invariant: 10s maximum bounded execution for REST API calls
   timeout 10s curl -s -f -X POST "https://api.vedastro.org/api/Calculate/HoroscopePredictions" \
     -H "x-api-key: $VEDASTRO_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{ ... }'
   ```
2. **Circuit Breaker Policy (2-Attempt Limit)**:
   - If an API call fails with HTTP `500` or network timeout, the harness permits at most **2 autonomous retry attempts** with exponential backoff (`sleep 5.0`).
   - If the second attempt fails, the circuit opens: execution halts immediately, error logs are preserved, and human escalation is triggered without entering infinite loops.
3. **Zero Orphaned Tasks**:
   - Any background process or detached task must be audited and terminated via `manage_task action="kill"` before concluding an execution turn.
4. **Calculators Catalog SSoT**:
   - Complete schema mapping for all 677 advanced calculators is located at [`assets/advanced_calculators_catalog.json`](file:///var/www/.agents/skills/vedastro/assets/advanced_calculators_catalog.json) (with backward-compatible symlink at [`references/advanced_calculators_catalog.json`](file:///var/www/.agents/skills/vedastro/references/advanced_calculators_catalog.json)).
