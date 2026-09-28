# Astrology-API.io Infrastructure, Plan Tiers & Governance

Technical deployment guide, pricing plans, authentication, rate limits, error taxonomy, and CoHaLo process hygiene for the Astrology-API.io engine (`https://api.astrology-api.io/api/v3/`).

---

## 1. Plan Tiers & Rate Limits

| Dimension | Forever Free | Starter / Pro | Pro Plus | Ultra / Professional | Business |
|---|---|---|---|---|---|
| **Price** | $0 / month | $11 / month | $21 / month | $37 / month | $99 / month |
| **Monthly Quota** | **50 requests** | 1,000 requests | 7,000 requests | 55,000 requests | 220,000 requests |
| **House Systems** | 12 systems | 12 systems | 12 systems | **23 systems** | 23 systems |
| **Endpoints** | Standard endpoints | Standard endpoints | Standard endpoints | Premium endpoints | **All 100+ endpoints** |
| **Throttling Policy** | Strict (`sleep 2.0`) | `sleep 0.5` | `sleep 0.2` | `sleep 0.1` | No artificial delay |
| **Overage Cost** | Requests blocked (`429`) | $10 / 1,000 extra | $10 / 1,000 extra | $10 / 1,000 extra | $10 / 1,000 extra |

---

## 2. Environment Variables & Secret Ingestion

| Variable Name | Scope | Description | Default Source |
|---|---|---|---|
| `ASTROLOGY_API_IO` | Container / System Env | Primary Bearer API Token (`ask_...`) | Injected in Zerops ZCP by `setup-astrokey.sh` |
| `ASTROLOGY_API_KEY` | Shell / System Env | Legacy Bearer API Token fallback | Fallback source |
| `astrology_apiKey` | Zerops Project Env | Zerops managed platform variable | Managed environment fallback |

### Safe Reference in Bash Scripts
```bash
# SOTA resolution cascade: primary ASTROLOGY_API_IO > ASTROLOGY_API_KEY > platform variable
API_KEY="${ASTROLOGY_API_IO:-${ASTROLOGY_API_KEY:-${astrology_apiKey:-}}}"
if [ -z "$API_KEY" ]; then
  echo "Error: Neither ASTROLOGY_API_IO nor ASTROLOGY_API_KEY is set in the environment." >&2
  exit 1
fi
```

---

## 3. Free Tier Optimization & Quota Stretching (4 Architectural Patterns)

With the **Forever Free Plan** providing 50 requests/month, applications must adhere to the following 4 architectural maximization patterns:

1. **Pattern 1 (Daily Global Ephemeris Caching - 90% Savings)**:
   - Mundane transit positions are globally identical across the Earth.
   - Run a single scheduled call at 00:00 UTC to `POST /api/v3/data/global-positions` (or universal parameters on `/data/positions`).
   - Cache the JSON payload in memory (Valkey/Redis/SQLite) for 24 hours (`TTL: 86400`).
   - Consumes exactly 30 requests/month, providing unlimited planetary transit calculations for thousands of user queries.
2. **Pattern 2 (Master Timing Aggregator - 75% Savings)**:
   - Never invoke separate endpoints for Profections, Firdaria, Decennials, and Zodiacal Releasing.
   - Invoke `POST /api/v3/timing/timeline` passing `techniques: ["profections", "firdaria", "decennials", "zodiacal_releasing"]`.
   - Returns all 4 Hellenistic timing systems in parallel inside **1 single API credit** (saving 3 calls per reading).
3. **Pattern 3 (Enhanced Positions & Dignities Aggregation)**:
   - Call `POST /api/v3/data/positions/enhanced` instead of multiple separate calls.
   - A single response provides: planetary positions, essential dignities (rulership, exaltation, triplicity, bound, decan), debilities (detriment, fall), sect condition, combustion/cazimi, houses of joy, dispositor chains, mutual receptions, and 9 Arabic lots.
4. **Pattern 4 (L1 Natal Invariance Caching)**:
   - Natal charts never change over time. Cache the raw natal response forever indexed by `sha256(YYYY-MM-DD-HH-MM-LAT-LNG)`.
   - Repeated lookups for the same consultant consume **0 API credits**.

### Canonical Single-Pass Ingestion Basket (3 Credits / Consultant)
For Phase 0 extraction in the Data Lakehouse, use the 3-endpoint basket cataloged in [usage.md](file:///var/www/.agents/skills/astrologyapi/references/usage.md#12-canonical-3-call-single-pass-ingestion-basket-3-credits--consultant):
- `POST /api/v3/timing/timeline` (1 credit)
- `POST /api/v3/data/positions/enhanced` (1 credit)
- `POST /api/v3/numerology/core-numbers` (1 credit)
- Total compute cost: exactly 3 credits per consultant run.
- Capacity: 16 full client profiles per month on the 50 req/mo Free Tier.
- Throttling: `sleep 2.0` between calls.

---

## 4. Request Header Standards

```http
Authorization: Bearer ${API_KEY}
Content-Type: application/json
Accept: application/json
```

---

## 5. HTTP Error Codes & Recovery Matrix

| HTTP Status | Error String | Cause | Recovery Action |
|---|---|---|---|
| `400` | `BAD_REQUEST` | Malformed parameters or invalid date/time coordinates | Verify `birth_data` schema in [usage.md](file:///var/www/.agents/skills/astrologyapi/references/usage.md). |
| `401` | `UNAUTHORIZED` | Missing or invalid Bearer token | Verify `$ASTROLOGY_API_IO` or `$ASTROLOGY_API_KEY` token. |
| `403` | `FORBIDDEN` | Endpoint requires a higher plan (e.g. Ultra for AI Horary) | Switch to standard endpoint or fallback engine (e.g. AstroWay). |
| `429` | `TOO_MANY_REQUESTS` / `QUOTA_EXCEEDED` | Monthly request quota exhausted (50/mo on Free) | Circuit breaker opens: halt calls, trigger email notification, switch to local ephemeris. |
| `500` | `INTERNAL_SERVER_ERROR` | Upstream calculation exception | Retry with exponential backoff (circuit breaker max 2). |

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All REST API invocations MUST strictly adhere to the following CoHaLo harness constraints:

1. **Strict Execution Timeouts**:
   ```bash
   # Invariant: 10s maximum bounded execution for REST API calls
   timeout 10s curl -s -f -X POST "https://api.astrology-api.io/api/v3/western/natal-chart" \
     -H "Authorization: Bearer $ASTROLOGY_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{ ... }'
   ```
2. **Circuit Breaker Policy (2-Attempt Limit)**:
   - If an API call fails with HTTP `500` or network timeout, the harness permits at most **2 autonomous retry attempts** with exponential backoff (`sleep 5.0`).
   - If the second attempt fails, the circuit opens: execution halts immediately, error logs are preserved, and human escalation is triggered without entering infinite loops.
3. **Zero Orphaned Tasks**:
   - Any background process or detached task must be audited and terminated via `manage_task action="kill"` before concluding an execution turn.
