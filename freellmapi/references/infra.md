# FreeLLMAPI — Infrastructure, Ops & Zerops Deployment Manual (v2026.09)

## 1. Zerops & Container Specifications

FreeLLMAPI is deployed in Zerops ZCP as an autonomous internal inference engine servicing AI coding agents and upstream gateways like Bifrost.

### Architecture Specs
- **Service Type**: Native Linux container (`type: nodejs@22` or `type: ubuntu@24.04`) or Docker VM container running official image (`ghcr.io/tashfeenahmed/freellmapi:latest`).
- **Internal Listening Port**: `3001/TCP` (serves OpenAI `/v1`, Anthropic `/v1/messages`, Gemini `/v1beta`, MCP `/mcp`, dashboard, and `/api/ping`).
- **Network Scope**: Private Zerops network (`http://freellmapi:3001`) with optional external HTTP access via Zerops subdomain for admin dashboard inspection.
- **Health Check Probe**: `http://localhost:3001/api/ping` (returns HTTP 200 OK with zero auth).

---

## 2. Environment Variables (.env Dictionary)

| Variable Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `PORT` | Integer | Yes | `3001` | HTTP TCP listening port for all API surfaces and dashboard. |
| `NODE_ENV` | String | Yes | `production` | Runtime mode: `production` enforces strict secret encryption and security headers. |
| `ENCRYPTION_KEY` | String | Yes | — | 64-character hex string (32 bytes) used for AES-256-GCM encryption of stored provider keys. |
| `FREEAPI_DB_PATH` | String | No | `/app/server/data/freellmapi.db` | Absolute path to the persistent SQLite database file. |
| `FREEAPI_CONFIG_PATH` | String | No | — | Absolute file path to declarative JSON startup configuration file. |
| `FREEAPI_CONFIG_JSON` | String | No | — | Raw JSON string applied on startup to seed provider keys and routing declaratively. |
| `FREELLMAPI_CONTEXT_HANDOFF` | String | No | `on_model_switch` | Mode for injecting contextual session briefings upon model failover (`off` or `on_model_switch`). |
| `REQUEST_ANALYTICS_RETENTION_DAYS` | Integer | No | `90` | Rolling retention window for per-request latency and token usage metrics. |
| `REQUEST_ANALYTICS_MAX_ROWS` | Integer | No | `100000` | Hard cap on total logged request rows before automatic pruning. |
| `PROXY_URL` | String | Optional | — | SOCKS5 or HTTP outbound proxy URL for reaching upstream providers (`socks5h://...`). |

---

## 3. Storage Architecture & Permission Safeguards

FreeLLMAPI relies on SQLite (`better-sqlite3`) with WAL (Write-Ahead Logging) enabled.

### Persistent Storage Mount
- Mount a persistent Zerops storage volume at `/app/server/data/`.
- The database file `freellmapi.db` and its WAL logs (`freellmapi.db-wal`, `freellmapi.db-shm`) reside inside this directory.
- **Permission Safeguard**: Ensure proper permissions on mount initialization:
  ```bash
  mkdir -p /app/server/data
  chmod -R 777 /app/server/data
  ```

### Encrypted At-Rest Secret Security
- Provider keys in SQLite are encrypted with AES-256-GCM using keys derived from `ENCRYPTION_KEY`.
- If `ENCRYPTION_KEY` is modified without running the rotation script, all stored credentials will become permanently unreadable.
- To safely rotate encryption keys with zero data loss:
  ```bash
  cd server && ENCRYPTION_KEY=<old_key> npm run rotate-encryption-key -- --new-key <new_hex_32_bytes>
  ```

---

## 4. Lifecycle Commands & Manifest (`zerops.yaml`)

```yaml
zerops:
  - setup: freellmapi
    run:
      base: nodejs@22
      ports:
        - port: 3001
          httpSupport: true
      prepareCommands:
        - apt-get update && apt-get install -y --no-install-recommends python3 make g++ curl ca-certificates
        - npm ci --omit=dev
        - npm run build
        - mkdir -p /app/server/data
        - chmod -R 777 /app/server/data
      initCommands:
        - node server/dist/index.js &
        - sleep 3
        - curl -f http://localhost:3001/api/ping || exit 1
        - killall node
      start:
        exec: node server/dist/index.js
      healthCheck:
        httpGet:
          port: 3001
          path: /api/ping
      envVariables:
        PORT: "3001"
        NODE_ENV: "production"
        FREELLMAPI_CONTEXT_HANDOFF: "on_model_switch"
        FREEAPI_DB_PATH: "/app/server/data/freellmapi.db"
        ENCRYPTION_KEY: "generate-32-byte-hex-with-openssl-rand-hex-32"
```

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

When orchestrating or interacting with FreeLLMAPI in this Zerops container:

- **Bounded Execution**:
  - Always enforce execution timeouts on CLI commands:
    ```bash
    timeout 10s curl -s -f http://localhost:3001/api/ping
    ```
  - Maximum synchronous wait: `WaitMsBeforeAsync: 10000`.
- **Zero Orphaned Tasks**:
  - Terminate background server instances before starting new processes: `manage_task action="kill"` or `killall node`.
- **Circuit Breaker Policy**:
  - If health checks fail (HTTP 502/503 or timeout), limit consecutive retries to maximum **2 attempts** before triggering operator escalation.
- **Physical Sensor Attestation**:
  - Verify gateway liveness with:
    ```bash
    curl -s -o /dev/null -w "%{http_code}" http://localhost:3001/api/ping
    # MUST return 200
    ```
