# AstroWay Infrastructure & Environment Specification

Technical deployment, rate-limiting, compute tiers, audit headers, idempotency, and error recovery for the AstroWay REST engine (`https://api.astroway.info/v1/`).

---

## 1. Environment Variables & Secret Ingestion

AstroWay authenticates via the `X-Api-Key` header using an active API key (`aw_live_...`).

| Variable Name | Scope | Description | Default Fallback |
|---|---|---|---|
| `ASTROWAY_API_KEY` | Shell / Container | Production API key for AstroWay | Sourced from `unisetup` / `.env` |
| `astroway_apiKey` | Zerops Project Env | Zerops managed environment key | Auto-injected in ZCP container |

### Safe Reference in Bash Scripts
```bash
# Reference by variable name without printing secret to stdout
API_KEY="${ASTROWAY_API_KEY:-${astroway_apiKey:-}}"
if [ -z "$API_KEY" ]; then
  echo "Error: ASTROWAY_API_KEY is not set in the environment." >&2
  exit 1
fi
```

---

## 2. Plan Tiers & Operational Bounds

| Plan Tier | Monthly Quota | Concurrency Limit | Endpoint Access | Inter-Request Delay |
|---|---|---|---|---|
| **Free Plan** | 500 credits / month | 10 requests / minute | 716 / 758 routes (42 routes blocked) | `sleep 7.0` |
| **Indie PRO ($5/mo)** | **50,000 credits / month** | **30 requests / minute** | **100% Unlocked (All 758 routes)** | **`sleep 2.0`** (or `0.5s` burst) |
| **Pro Plan ($25/mo)** | 300,000 credits / month | 120 requests / minute | 100% Unlocked | `sleep 0.5` |
| **Lifetime License** | 50,000 credits / month | 30 requests / minute | 100% Unlocked | `sleep 2.0` |

### Indie PRO Tier ($5.00 USD / Month) Operational Bounds
- **Monthly Quota**: 50,000 credits per billing month.
- **Overage**: Billed at $5.00 USD per 10,000 additional credits.
- **Concurrency Rate Limit**: 30 requests per minute burst limit. Recommended loop delay is `sleep 2.0` (tolerating bursts of `sleep 0.5` for batches under 5 calls).
- **Architecture**: 100% REST-ONLY. The local `@astroway/mcp` server has been decommissioned to prevent double credit billing, eliminate 717 schema files from the agent context, and ensure transparent header auditing.

### Credit Cost by Compute Tiers
Calculations are charged per call based on server compute complexity:
- **Tier 1 (10 credits, <50ms)**: Simple lookups, transit snapshots, Sabian symbols, I Ching, Tarot single draw.
- **Tier 2 (20 credits, 50–200ms)**: Individual natal charts (`/chart`), D10 Dasamsa, D60 Shashtiamsa, BaZi Four Pillars, fixed stars, ACG line reports.
- **Tier 3 (50 credits, 200–500ms)**: Dual charts, synastry, full Human Design BodyGraph, ACG best places.
- **Tier 4 (100 credits, >500ms)**: Multi-day temporal scans, AI interpretations (`/ai/interpret/natal`).
- **Tier 5 (250 credits, 2–5s)**: Hermetic Trutine rectification, AI long-form narratives (`/reports/ai-natal-narrative`).
- **Tier 6 (500 credits, 10–120s)**: Deep biographical multi-event rectification.
- **Tier 7 (5,000 credits, 3–8s) — STRICTLY VETOED**: 40+ page publication-grade PDF report compiler (`/v1/reports/*`). Consumes 10% of total monthly Indie PRO quota in a single request. Vetoed in automated extraction.

### Canonical Single-Pass Ingestion Basket (740 Credits / Consultant)
For Phase 0 extraction in the Data Lakehouse, use the 30 JSON endpoints cataloged in [usage.md](file:///var/www/.agents/skills/astroway/references/usage.md#14-the-30-endpoint-single-pass-basket-740-credits).
- Total compute cost: exactly 740 credits per consultant run.
- Throughput capacity: 67 complete client runs per month on Indie PRO ($5/mo, 50,000 credits).
- Mandatory pacing: `sleep 2.0` between sequential requests to respect the 30 req/min rate limit.

---

## 3. Audit Headers for Consumption Tracking

Every successful response includes headers that MUST be audited in automated scripts:
- `X-Credits-Used`: Exact credits deducted for the transaction.
- `X-Credits-Remaining`: Remaining credit balance in your account.
- `X-Credits-Limit`: Account ceiling (50,000 on Indie PRO).

### Automated Inspection in Bash
```bash
# Capture and inspect remaining balance
REMAINING=$(grep -i "x-credits-remaining" headers.txt | tr -d '\r' | awk '{print $2}')
if [ -n "$REMAINING" ] && [ "$REMAINING" -lt 500 ]; then
  echo "⚠️ Warning: AstroWay credit balance critically low: $REMAINING credits left." >&2
fi
```

---

## 4. Idempotency & Safe Retry Protocol

Compute-intensive endpoints accept the `Idempotency-Key` header with a client UUID:
```bash
-H "Idempotency-Key: $(uuidgen)"
```

- **Replay Behavior**: Repeating a request with the same body and idempotency key returns the cached response with `Idempotency-Replayed: true` without deducting additional credits.
- **TTL**: Keys persist in the server cache for ~24 hours.
- **Conflict Handling**: Reusing an existing key with a modified payload returns `409 Conflict`. A duplicate request sent while the initial calculation is processing returns `409 In Progress` with a `Retry-After` header.

---

## 5. HTTP Error Codes & Recovery Matrix

| HTTP Status | Error String | Diagnostic Cause | Automated Recovery Strategy |
|---|---|---|---|
| `400` | `bad_request` | Invalid coordinates, missing required fields, or malformed date/time strings | Ensure `date` is `YYYY-MM-DD`, `time` is `HH:MM:SS`, and `latitude`/`longitude` are numeric floats. |
| `401` | `unauthorized` | Missing, expired, or invalid `X-Api-Key` | Verify `$ASTROWAY_API_KEY` in environment. |
| `403` | `forbidden` | Feature requested is locked on Free tier (e.g. `/reports/*`) | Upgrade to Indie PRO ($5/mo) or check account standing. |
| `409` | `conflict` | Idempotency key conflict or duplicate concurrent request | Generate a new UUID with `uuidgen` or wait for `Retry-After`. |
| `422` | `validation_error` | Enum out of bounds (e.g. invalid `houseSystem` code or negative time) | Check [usage.md](file:///var/www/.agents/skills/astroway/references/usage.md) for valid enums (`P`, `W`, `K`, `C`). |
| `429` | `too_many_requests` | Rate limit breached (>30 req/min) or monthly 50k quota exhausted | Throttle loop to `sleep 2.0`; check `X-Credits-Remaining`. |
| `500` | `internal_server_error` | Ephemeris calculation fault or upstream failure | Retry once with `sleep 3.0` exponential backoff; escalate on repeat. |

---

## 6. Network Resilience & Bounded Execution (CoHaLo)

All automated calls MUST use strict timeouts:

```bash
# Invariant: 10s maximum bounded execution for REST API calls
timeout 10s curl -s -f -X POST "https://api.astroway.info/v1/chart" \
  -H "X-Api-Key: $ASTROWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept-Encoding: br, gzip" \
  -d '{
    "date": "1990-05-15",
    "time": "14:30:00",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timezoneOffset": -4
  }' || {
    echo "Request timed out or failed with non-2xx status." >&2
  }
```
