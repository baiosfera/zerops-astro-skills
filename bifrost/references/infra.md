# Maxim AI Bifrost & Bifrost CLI — Infrastructure & Deployment Manual (v2.0.0 GA / Sept 2026)

## 1. Zerops & Container Specifications

Bifrost is deployed on Zerops as an ultra-fast, autonomous Linux service running the compiled native Go binary.

### Architecture Specs
- **Service Type**: Native Linux container (`alpine@3.21` base or `ubuntu@24.04`) or Docker VM container (`maximhq/bifrost:v2.0.0`).
- **Binary Target**: Official standalone Go release binary (`bifrost-linux-amd64` v2.0.0 GA).
- **Internal Listening Port**: `8080/TCP` (serves inference, management UI, health check, Prometheus `/metrics`, and MCP `/mcp`).
- **Public Routing**: HTTP routing on port `8080` with optional TLS terminated at Zerops load balancer.
- **Health Check Endpoint**: `http://localhost:8080/health` (HTTP 200 OK).

---

## 2. Environment Variables (.env Dictionary)

| Variable Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `APP_PORT` | Integer | Yes | `8080` | HTTP service TCP listening port for inference and admin API. |
| `APP_HOST` | String | Yes | `0.0.0.0` | Network interface address to bind HTTP listener. |
| `APP_DIR` | String | Yes | `/app/data` | Working directory housing `config.json` and persistent data. |
| `LOG_LEVEL` | String | No | `info` | Logging verbosity: `debug`, `info`, `warn`, `error`. |
| `LOG_STYLE` | String | No | `json` | Structured output formatting: `json` (production) or `pretty` (console). |
| `GOMEMLIMIT` | String | Recommended | Container RAM * 0.9 | Soft memory limit for Go runtime (e.g. `900MiB` on 1GB container) to prevent OOM kills. |
| `GOGC` | Integer | Recommended | `200` | Garbage collection trigger threshold. `200` doubles heap headroom for sub-100µs throughput. |
| `BIFROST_ENCRYPTION_KEY` | String | Yes | — | Secret passphrase used by Argon2id KDF to derive 32-byte AES-256 key for DB secret encryption. |
| `BIFROST_SETUP_TOKEN` | String | Conditional | — | Operator bootstrap token required to create the first admin user account. |
| `BIFROST_ENV_LABEL` | String | No | `PROD` | Visual environment tag (max 10 chars) rendered in the Bifrost UI header. |
| `BIFROST_DB_TYPE` | String | No | `sqlite` | Database engine backend: `sqlite` (single node) or `postgres` (HA cluster). |
| `BIFROST_DB_DSN` | String | Conditional | — | PostgreSQL connection string: `postgres://user:pass@host:5432/bifrost?sslmode=disable`. |
| `VALKEY_ADDR` | String | Optional | `valkey:6379` | Valkey/Redis instance address (`host:6379`) for exact & semantic caching. |
| `VALKEY_PASSWORD` | String | Optional | — | Valkey/Redis authentication password if required. |
| `FREELLMAPI_URL` | String | Optional | `http://freellmapi:4000/v1` | Upstream URL for FreeLLMAPI custom provider. |

---

## 3. Storage Architecture & Permission Safeguards

Bifrost supports two distinct storage modes depending on scale requirements:

### A. Dev / Single-Node Mode (SQLite)
- Mount a persistent Zerops volume at `/app/data/`.
- SQLite database files (`bifrost.db`, `logs.db`) reside directly inside `/app/data/`.
- **FUSE Permission Safeguard**: Ensure proper permissions on mount:
```bash
chmod -R 777 /app/data
```

### B. High-Availability Clustered Mode (PostgreSQL + Valkey)
- Fully stateless compute containers scaling horizontally (`min: 2, max: 10`).
- Backed by managed **PostgreSQL 16+** (`postgresql:single@18` or `postgresql:ha`) for configuration and audit logs.
- Backed by managed **Valkey 7.2+** (`valkey:single@7.2`) for direct key hashing and semantic vector cache storage.

---

## 4. Lifecycle Commands & Manifest (`zerops.yaml`)

```yaml
zerops:
  - setup: bifrost
    run:
      base: alpine@3.21
      ports:
        - port: 8080
          httpSupport: true
      prepareCommands:
        - apk add --no-cache curl ca-certificates tzdata
        - curl -fsSL -o /usr/local/bin/bifrost https://github.com/maximhq/bifrost/releases/download/v2.0.0/bifrost-linux-amd64
        - chmod +x /usr/local/bin/bifrost
        - mkdir -p /app/data
      initCommands:
        - /usr/local/bin/bifrost -app-dir /app/data -port 8080 -host 0.0.0.0 &
        - sleep 2
        - curl -f http://localhost:8080/health || exit 1
        - killall bifrost
      start:
        exec: /usr/local/bin/bifrost -app-dir /app/data -port 8080 -host 0.0.0.0 -log-level ${LOG_LEVEL:-info} -log-style ${LOG_STYLE:-json}
      healthCheck:
        httpGet:
          port: 8080
          path: /health
      envVariables:
        APP_PORT: "8080"
        APP_HOST: "0.0.0.0"
        APP_DIR: "/app/data"
        LOG_LEVEL: "info"
        LOG_STYLE: "json"
        GOMEMLIMIT: "900MiB"
        GOGC: "200"
        BIFROST_ENCRYPTION_KEY: "change-to-production-secret-argon2id-key"
```

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

When orchestrating or interacting with Bifrost in this ZCP environment:

- **Bounded Execution**:
  - Always enforce execution timeouts on CLI commands:
    ```bash
    timeout 10s curl -s -f http://localhost:8080/health
    ```
  - Maximum synchronous wait: `WaitMsBeforeAsync: 10000`.
- **Zero Orphaned Tasks**:
  - Never leave background daemon processes hanging in test loops. Terminate dangling instances via `manage_task action="kill"` or `killall bifrost`.
- **Circuit Breaker**:
  - If Bifrost fails health checks (HTTP 502/503 or timeout), limit consecutive retries to maximum **2 attempts** before triggering operator escalation.
- **Physical Sensor Attestation**:
  - Verify gateway readiness with:
    ```bash
    curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health
    # MUST return 200
    ```
