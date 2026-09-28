# Kundali MCP Infrastructure, Connectors & Governance

Technical deployment guide, remote Streamable HTTP MCP connection, authentication, timezone resolution, error taxonomy, and CoHaLo process hygiene for the Kundali Jyotish engine (`https://mcp.kundalimcp.com/mcp`).

---

## 1. Remote MCP Connector Configuration

Kundali operates via a remote Streamable HTTP MCP endpoint. Configure your MCP client as follows:

### MCP Configuration Template (`mcp_config.json`):
```json
{
  "mcpServers": {
    "kundali": {
      "url": "https://mcp.kundalimcp.com/mcp",
      "headers": {
        "Authorization": "Bearer ${KUNDALI_MCP_KEY}"
      }
    }
  }
}
```

---

## 2. Environment Variables & Secret Ingestion

| Variable Name | Scope | Description | Default Source |
|---|---|---|---|
| `KUNDALI_MCP_KEY` | Shell / System Env | Master Bearer API Key | Sourced from `unisetup` / `/etc/environment` |
| `kundali_mcpKey` | Zerops Project Env | Zerops managed platform variable | Auto-injected in ZCP container |

### Safe Reference in Shell Scripts
```bash
# Reference by variable name without standard output leakage
API_KEY="${KUNDALI_MCP_KEY:-${kundali_mcpKey:-}}"
if [ -z "$API_KEY" ]; then
  echo "Error: KUNDALI_MCP_KEY is not set in the environment." >&2
  exit 1
fi
```

---

## 3. Historical Timezone Resolution (`chrono-tz`)

The Kundali server integrates a full `chrono-tz` IANA timezone database covering all historical boundary shifts:
- **India 1955**: Consolidation into standard UTC+05:30.
- **USA 1966**: Uniform Time Act standardization.
- **Russia 2011**: Permanent daylight saving transition and subsequent adjustments.
- **DST Regimes**: Full historical forward and fall-back transition handling.

---

## 4. Rate Limits & Tier Capacities

| Tier | Rate Limit (RPS / RPM) | Monthly Quota | Caching Strategy |
|---|---|---|---|
| **Free Forever** | 2 RPS / 120 RPM | 5,000 tool calls/mo | Default 30-day encrypted cache |
| **Standard** | 10 RPS / 600 RPM | 50,000 tool calls/mo | Operator-blind encrypted cache |
| **Enterprise** | 30 RPS / 1800 RPM | Unlimited | Custom retention / `cache: "skip"` |

*Note: Unauthenticated tool `get_version` does not consume quota. Computational calls require Bearer token `sutra_<32 hex chars>`.*

---

## 5. Boundary Sensitivity Protocol (`boundary_sensitive`)

The Vedākṣha engine evaluates positional margins against zodiacal signs, nakshatras, and padas:
- The server returns `facts.boundary_margins` / `idl.boundary_margins`.
- If any graha has `boundary_sensitive: true`, the physical position lies within $0.05^\circ$ of a boundary.
- **Agent Protocol**: When `boundary_sensitive: true` is reported on Lagna or Chandra, the agent MUST flag boundary sensitivity before deriving high-precision D9 (Navamsha) or D60 (Shashtiamsha) predictions, noting that birth time accuracy within $\pm 2$ minutes is mandatory.

---

## 6. Canonical JSON-RPC 2.0 Error Taxonomy & Recovery Matrix

| Status / Error Code | Error Type | Root Cause | Machine Recovery Action (`data.hint`) |
|---|---|---|---|
| `-32602` | `InvalidParams` | Unknown tool name (e.g. `shubh_muhurat`) or DST spring-forward gap | Use canonical name `muhurat`; adjust clock time $\pm 1$ hour if gap. |
| `-32601` | `MethodNotFound` | Tool method not registered | Re-verify tool name against `get_version` or schema catalog. |
| `-32029` | `RateLimitExceeded` | Concurrency limit (>120 RPM) or monthly cap hit | Enforce `sleep 2.0` throttling or use cached responses (`cache: "default"`). |
| `-32603` | `Internal` | Infrastructure error or tier permission denial | Retry with circuit breaker (max 2 attempts with `sleep 5.0`). |
| `-32000` | `ComputationError` | Birth datetime outside ephemeris range (-2000 BC to 3000 AD) | Bound calculation queries to supported astronomical epoch. |

*Agent Guidance*: Inspect `error.data.hint` in all JSON-RPC error responses for dynamic remediation directives.

---

## 7. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All MCP invocations MUST strictly adhere to the following CoHaLo harness constraints:

1. **Strict Execution Timeouts**:
   - Every MCP tool call must be bounded by a 10s maximum execution timeout (`timeout 10s`).
2. **Circuit Breaker Policy (2-Attempt Limit)**:
   - If an MCP call fails with JSON-RPC `-32603` or network timeout, the harness permits at most **2 autonomous retry attempts** with exponential backoff (`sleep 5.0`).
   - If the second attempt fails, the circuit opens: execution halts immediately, error logs are preserved, and human escalation is triggered without entering infinite loops.
3. **Zero Orphaned Tasks**:
   - Any background process or detached MCP subshell must be audited and terminated via `manage_task action="kill"` before concluding an execution turn.
