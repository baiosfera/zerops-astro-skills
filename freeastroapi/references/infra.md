# FreeAstroAPI Infrastructure & Environment Specification

Technical deployment, rate-limiting, environment variable configuration, tier boundaries, and error taxonomy for FreeAstroAPI (`https://api.freeastroapi.com/api/`).

---

## 1. Environment Variables & Secret Ingestion

FreeAstroAPI relies on a single master API key passed as the `x-api-key` header.

| Variable Name | Scope | Description | Default Fallback |
|---|---|---|---|
| `FREEASTRO_API_KEY` | Shell / Container | Master API key for FreeAstroAPI | Sourced from `unisetup` / `.env` |
| `freeastro_apiKey` | Zerops Project Env | Zerops managed environment key | Auto-injected in ZCP container |

### Safe Reference in Bash Scripts
```bash
# Always reference by variable name without printing to standard output
API_KEY="${FREEASTRO_API_KEY:-${freeastro_apiKey:-}}"
if [ -z "$API_KEY" ]; then
  echo "Error: FREEASTRO_API_KEY is not set in the environment." >&2
  exit 1
fi
```

---

## 2. Plan Tiers & Rate Limit Governance

| Plan Tier | Quota Allowance | Concurrency Limit | PDF Report Credits | Recommended Throttle |
|---|---|---|---|---|
| **Free Plan** | 80 requests / day | 1 request / second | 0 / month | `sleep 1.2` |
| **Entry Plan ($8/mo)** | 50,000 requests / month | 5 requests / second | 2 / month | `sleep 0.25` |
| **High Plan** | 500,000 requests / month | 10 requests / second | Included / Uncapped | `sleep 0.1` |

### Entry Tier ($8.00 USD / Month) Operational Bounds
- **Monthly Request Quota**: 50,000 requests per billing month.
- **RPS Limit**: 5 requests per second burst limit. Recommended loop throttle is `sleep 0.25` (4 requests/second, operating at 80% capacity to prevent burst 429 errors).
- **PDF Report Credits**: 2 branded comprehensive PDF reports (8,000–9,000 words each) included per month via `/api/v1/natal/report`. Check remaining credits at `/api/v1/natal/report-credits`. Additional reports require credit purchases or plan upgrade.
- **Astrocartography Crossings Boundary**: The `include_crossings` parameter MUST be set to `false`. Setting `include_crossings: true` triggers `403 high_plan_required`.

### Automated Script Discipline
Every batch loop invoking FreeAstroAPI (e.g. `omni_curl_dumper.sh`) MUST enforce rate limits:
```bash
# Invariant: Prevent 429 rate limit errors on Entry Tier (5 RPS max)
sleep 0.25
```

---

## 3. Idempotency & Safe Retry Protocol

Billable `POST` endpoints (specifically PDF report generation and compute-intensive operations) accept the `Idempotency-Key` header with a client-generated UUID:
```bash
-H "Idempotency-Key: $(uuidgen)"
```

- **Replay Behavior**: A retry with the exact same request body and idempotency key returns the original cached response with `Idempotency-Replayed: true` without consuming extra quota or report credits.
- **Key TTL**: Keys are retained in the server cache for ~24 hours.
- **Conflict Handling**: Reusing a key with a modified request body returns `409 idempotency_key_reused`. A duplicate request sent while the original is still computing returns `409 request_in_progress` with a `Retry-After` header.

---

## 4. HTTP Error Codes & Recovery Matrix

| HTTP Status | Error String | Diagnostic Cause | Automated Recovery Strategy |
|---|---|---|---|
| `400` | `bad_request` | Invalid coordinates, unresolved city name, or invalid date format | Verify date range; provide explicit `lat` and `lng` floats (-90 to 90, -180 to 180). |
| `401` | `unauthorized` | Missing or invalid `x-api-key` header | Verify `$FREEASTRO_API_KEY` in environment or container secrets. |
| `403` | `high_plan_required` | Feature requested exceeds Entry tier (e.g. `include_crossings: true` in ACG, or continuous `transits/timeline` and `transits/search`) | Enforce `include_crossings: false`, use `transits/calculate` with `current_city` for single-point snapshots, or upgrade tier. |
| `409` | `idempotency_conflict` | Idempotency key reused with different payload, or request in progress | Generate fresh UUID with `uuidgen`, or respect `Retry-After` header. |
| `422` | `validation_error` | Pydantic validation failure (missing required fields, invalid types, wrong nesting) | Inspect `detail` array in JSON error response. Common fixes: nest `location` inside `natal` and `solar_return`, provide `annual_profection: {year}`, add `current_city` in transits. |
| `429` | `too_many_requests` | Concurrency limit (5 RPS) or monthly quota exceeded | Respect `Retry-After` header; throttle loop with `sleep 0.25` or backoff to `sleep 1.0`. |
| `501` | `png_unavailable` | Native Cairo rendering library unavailable on server | Fall back to `format: "svg"` vector output. |

---

## 5. Network Resilience & Bounded Execution

All CLI and automated script invocations MUST use strict execution timeouts to satisfy CoHaLo process hygiene:

```bash
# Invariant: 10s maximum bounded execution for REST API calls
timeout 10s curl -s -f -X POST "https://api.freeastroapi.com/api/v1/natal/calculate" \
  -H "x-api-key: $FREEASTRO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "year": "<YYYY>",
    "month": "<MM>",
    "day": "<DD>",
    "hour": "<HH>",
    "minute": "<MIN>",
    "lat": "<FLOAT_LATITUDE>",
    "lng": "<FLOAT_LONGITUDE>",
    "tz_str": "<IANA_TIMEZONE>"
  }' || {
    echo "Request timed out or failed with non-2xx status." >&2
  }
```
