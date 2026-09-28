# HebCal Infrastructure, Geocoding & Governance

Technical deployment guide, endpoints, geocoding parameters, rate limits, caching strategy, error taxonomy, and CoHaLo process hygiene for the HebCal REST API engine (`https://www.hebcal.com/`).

---

## 1. Endpoints & Base URLs

| Module | Endpoint URL | HTTP Method | Auth Requirement | Typical Latency |
|---|---|---|---|---|
| **Date Converter** | `https://www.hebcal.com/converter` | `GET` | None (Public CORS) | < 150 ms |
| **Zmanim API** | `https://www.hebcal.com/zmanim` | `GET` | None (Public CORS) | < 200 ms |
| **Assur Melacha (IoT)** | `https://www.hebcal.com/zmanim?im=1` | `GET` | None (Public CORS) | < 200 ms |
| **Shabbat Times** | `https://www.hebcal.com/shabbat` | `GET` | None (Public CORS) | < 200 ms |
| **Jewish Calendar & Yomi** | `https://www.hebcal.com/hebcal` | `GET` | None (Public CORS) | < 250 ms |
| **Torah Reading (Leyning)** | `https://www.hebcal.com/leyning` | `GET` | None (Public CORS) | < 200 ms |
| **Yahrzeit Memorials** | `https://www.hebcal.com/yahrzeit` | `POST` | None (Public HTTPS) | < 300 ms |

---

## 2. Geocoding & Location Parameters

HebCal accepts flexible location identifiers:
- **Coordinates + Timezone**: `latitude=<DECIMAL>&longitude=<DECIMAL>&tzid=<IANA_TZ>`. *(Note: `tzid` is mandatory when using coordinates)*.
- **GeoNames ID**: `geonameid=<ID>` (e.g. `3448439` for São Paulo, `5128581` for New York, `281184` for Jerusalem, `3117735` for Madrid).
- **US ZIP Code**: `zip=<ZIP5>` (e.g. `90210`).
- **Elevation Adjustment**: Optional `elev=<METERS>&ue=on` (1 to 9000 m) for elevation-adjusted sunset and sunrise.

---

## 3. Rate Limits, User-Agent & Caching Strategy

- **Rate Limit Policy (HTTP 429)**:
  - HebCal enforces a sliding rate limit of **90 requests per 10-second window** per client IP.
  - If exceeded, the server answers `429 Too Many Requests`.
- **Descriptive User-Agent**:
  - Requests should supply a descriptive User-Agent header (e.g. `-A "GentleAI-Hebcal/1.0"`) to prevent generic scraping bans by Cloudflare WAF.
- **Cloudflare Edge Caching**:
  - Responses for static dates (`date=YYYY-MM-DD`, `gy=YYYY`) are aggressively cached on the Cloudflare edge network. Always supply explicit dates when possible to maximize cache hit rates.

---

## 4. HTTP Error Codes & Recovery Matrix

| HTTP Status | Root Cause | Recovery Action |
|---|---|---|
| `400` | Malformed parameters, invalid date string, or date out of range | Supply valid date (`YYYY-MM-DD`) and ensure `cfg=json`. |
| `404` | Non-existent route or invalid location ID | Verify route in [usage.md](file:///var/www/.agents/skills/hebcal/references/usage.md) or switch to coordinates. |
| `429` | Sliding window rate limit exceeded (>90 req / 10s) | Throttle requests (`sleep 0.2`) or use cached responses. |
| `500` / `502` | Upstream HebCal server timeout or Cloudflare error | Retry with exponential backoff (circuit breaker max 2). |

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All REST API invocations MUST strictly adhere to the following CoHaLo harness constraints:

1. **Strict Execution Timeouts**:
   ```bash
   # Invariant: 10s maximum bounded execution for REST API calls
   timeout 10s curl -s -A "GentleAI-Hebcal/1.0" "https://www.hebcal.com/zmanim?cfg=json&..."
   ```
2. **Circuit Breaker Policy (2-Attempt Limit)**:
   - If an API call fails with HTTP `500` or network timeout, the harness permits at most **2 autonomous retry attempts** with backoff (`sleep 5.0`).
   - If the second attempt fails, the circuit opens: execution halts immediately, error logs are preserved, and human escalation is triggered without entering infinite loops.
3. **Zero Orphaned Tasks**:
   - Any background process or detached subshell must be audited and terminated via `manage_task action="kill"` before concluding an execution turn.
