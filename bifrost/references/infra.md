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
| `BIFROST_ADMIN_USERNAME` | String | Yes (v2.3+) | `admin` | Headless dashboard admin username referenced via `env.BIFROST_ADMIN_USERNAME` in `governance.auth_config`. |
| `BIFROST_ADMIN_PASSWORD` | String | Yes (v2.3+) | — | Strong admin password referenced via `env.BIFROST_ADMIN_PASSWORD` in `governance.auth_config` (unlocks `SetupLockMiddleware` without interactive setup). |
| `BIFROST_SETUP_TOKEN` | String | Conditional | — | Operator bootstrap token required only when `governance.auth_config.is_enabled` is false. |
| `BIFROST_ENV_LABEL` | String | No | `PROD` | Visual environment tag (max 10 chars) rendered in the Bifrost UI header. |
| `PG_HOST` | String | Required in Prod | `database` | PostgreSQL 18 host (${database_hostname}). |
| `PG_PORT` | Integer | Required in Prod | `5432` | PostgreSQL 18 port. |
| `PG_USER` | String | Required in Prod | — | PostgreSQL username (${database_user}). |
| `PG_PASSWORD` | String | Required in Prod | — | PostgreSQL password (${database_password}). |
| `PG_DATABASE` | String | Required in Prod | — | PostgreSQL database name (${database_dbName}). |
| `DATABASE_URL` | String | Recommended | — | Complete connection string (${database_connectionString}). |
| `VALKEY_ADDR` | String | Recommended | `valkey:6379` | Valkey 7.2 host:port for Redis-compatible vector cache. |
| `VALKEY_PASSWORD` | String | Recommended | — | Valkey 7.2 password (${valkey_password}). |
| `FREELLMAPI_URL` | String | Optional | `http://freellmapi:3001/v1` | Upstream URL for FreeLLMAPI custom provider (port 3001). |

---

## 3. Storage Architecture & Production Invariants

### Production Mode: PostgreSQL 18 + Valkey 7.2 + chromem Vector Store
Bifrost in Zerops persists its configuration and logs in managed PostgreSQL 18 (`config_store` and `logs_store`). Valkey 7.2 manages distributed locks and rate limits. For `semantic_cache`, `vector_store.type` MUST be `chromem` (embedded pure-Go vector engine) or `qdrant`. Setting `vector_store.type: redis` against standard Valkey 7.2 fails because vanilla Valkey lacks the proprietary RediSearch (`FT.*`) C-module.

In `config.json`:
```json
{
  "$schema": "https://www.getbifrost.ai/schema",
  "encryption_key": "env.BIFROST_ENCRYPTION_KEY",
  "config_store": {
    "enabled": true,
    "type": "postgres",
    "config": {
      "host": "env.PG_HOST",
      "port": "5432",
      "user": "env.PG_USER",
      "password": "env.PG_PASSWORD",
      "db_name": "env.PG_DATABASE",
      "ssl_mode": "disable"
    }
  },
  "logs_store": {
    "enabled": true,
    "type": "postgres",
    "config": {
      "host": "env.PG_HOST",
      "port": "5432",
      "user": "env.PG_USER",
      "password": "env.PG_PASSWORD",
      "db_name": "env.PG_DATABASE",
      "ssl_mode": "disable"
    }
  },
  "vector_store": {
    "enabled": true,
    "type": "chromem",
    "config": {
      "path": "/mnt/localstorage/bifrost/chromem",
      "compress": true
    }
  },
  "client": {
    "enforce_auth_on_inference": false
  },
  "governance": {
    "auth_config": {
      "is_enabled": true,
      "admin_username": "env.BIFROST_ADMIN_USERNAME",
      "admin_password": "env.BIFROST_ADMIN_PASSWORD",
      "disable_auth_on_inference": false
    }
  },
  "plugins": [
    {
      "enabled": true,
      "name": "semantic_cache",
      "config": {
        "dimension": 1,
        "ttl": 86400,
        "threshold": 0.8,
        "default_cache_key": "production-cache",
        "vector_store_namespace": "BifrostLocalCache",
        "cache_by_model": true,
        "cache_by_provider": true
      }
    }
  ]
}
```

---

## 4. Lifecycle Commands & Manifest (`zerops.yaml`)

```yaml
zerops:
  - setup: bifrost
    build:
      base: alpine/go@1.22
      buildCommands:
        - curl -fsSL -o bifrost https://downloads.getmaxim.ai/bifrost/v2.2.3/linux/amd64/bifrost-http
        - chmod +x bifrost
        - mkdir -p data
        - cp apps/bifrost/config.json data/config.json
      deployFiles: .
      cache:
        - bifrost
    run:
      base: alpine/go@1.22
      volume:
        hostname: localstorage
        mountPath: /mnt/localstorage
        readOnly: false
      ports:
        - port: 8080
          httpSupport: true
      prepareCommands:
        - sudo apk add --no-cache ca-certificates tzdata
        - sudo mkdir -p /mnt/localstorage/bifrost
        - sudo chown -R zerops:zerops /mnt/localstorage/bifrost
      initCommands:
        - cp /var/www/data/config.json /mnt/localstorage/bifrost/config.json
        - chmod +x /var/www/bifrost
      start: /var/www/bifrost -app-dir /mnt/localstorage/bifrost -port 8080 -host 0.0.0.0 -log-level info -log-style json
      healthCheck:
        httpGet:
          port: 8080
          path: /health
      envVariables:
        APP_PORT: "8080"
        APP_HOST: "0.0.0.0"
        APP_DIR: "/mnt/localstorage/bifrost"
        GOMEMLIMIT: "900MiB"
        GOGC: "200"
        PG_HOST: ${database_hostname}
        PG_PORT: "5432"
        PG_USER: ${database_user}
        PG_PASSWORD: ${database_password}
        PG_DATABASE: ${database_dbName}
        DATABASE_URL: ${database_connectionString}
        BIFROST_DB_TYPE: "postgres"
        BIFROST_DB_DSN: ${database_connectionString}
        VALKEY_ADDR: "valkey:6379"
        VALKEY_PASSWORD: ${valkey_password}
        FREELLMAPI_URL: "http://freellmapi:3001/v1"
        BIFROST_ENCRYPTION_KEY: "env.BIFROST_ENCRYPTION_KEY"
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

---

## 6. Ephemeral ZCP Control Plane Boundary vs Dedicated 24/7 Runtime Mesh

Zerops enforces a strict architectural boundary between the Control Plane (`zcp`) and Production Runtime Services:

1. **ZCP Lifecycle (Ephemeral & Demand-Driven)**:
   - The `zcp` container is active ONLY during interactive editing, auditing, SSoT synchronization, and deployment cycles. It is suspended/stopped during normal operations.
   - **Zero Production Dependents**: Never route WhatsApp webhooks, background workers, or public APIs through `zcp`.

2. **Dedicated Runtime Mesh (24/7 Invariant)**:
   - The production Bifrost gateway runs continuously in its dedicated `bifrost` container (`alpine/go@1.22` on internal port `8080`).
   - Configuration is persisted in managed PostgreSQL 18 (`config_store` & `logs_store`).
   - All runtime services (`whatsappbot`, `webprod`, `evolution`) connect directly to `http://bifrost:8080` over the Zerops private VXLAN mesh.

3. **Role of `bifrost-cli` in ZCP**:
   - `bifrost-cli` operates strictly as a development-time utility:
     - Synthetic smoke testing of `config.json` before applying changes.
     - TUI bridge for Coding Agents (Claude Code, OpenCode) running inside `zcp`.
---

## 7. Zerops Vault Self-Shadowing Prevention Invariant
When referencing environment variables or secrets stored in the Zerops Project Vault inside `zerops.yaml`:
- **The Self-Shadowing Trap**: Referencing a vault variable using the identical key name (e.g., `GROQ_API_KEY: ${GROQ_API_KEY}` or `OPENAI_API_KEY: ${OPENAI_API_KEY}`) triggers the Zerops preflight error:
  `service_env_self_shadow: Variable ... cannot reference itself`.
- **Enforced Naming Convention**: Secrets in the project vault must use explicit, distinct prefixes (e.g., `WHISPER_GROQ_API_KEY`, `VAULT_OPENAI_API_KEY`, `PROD_ANTHROPIC_KEY`).
- **Mapping in zerops.yaml**: Map the distinct vault secret to the standard runtime environment variable expected by the application:
  ```yaml
  envVariables:
    GROQ_API_KEY: ${WHISPER_GROQ_API_KEY}
    OPENAI_API_KEY: ${VAULT_OPENAI_API_KEY}
  ```

## 8. v2.3.0 Setup Lock & PostgreSQL 18 Connection Budget Invariants
- **SetupLockMiddleware (`v2.3.0+`)**: Bifrost locks all `/api/*` dashboard endpoints with `403` and redirects `/` to `/login` ("Finish setting up Bifrost") unless `governance.auth_config.is_enabled: true` is configured with `env.BIFROST_ADMIN_USERNAME` and `env.BIFROST_ADMIN_PASSWORD` (or `BIFROST_SETUP_TOKEN` is set for interactive setup).
- **Inference Auth Default**: `v2.3.0` defaults `client.enforce_auth_on_inference` to `true` on fresh deployments when omitted; set `"client": { "enforce_auth_on_inference": false }` explicitly if internal Zerops services call `/v1/*` without virtual keys.
- **No `-version` Flag**: `bifrost` v2.3.0 Go binary does not support `-version`/`--version`; query `GET /api/version` instead.
- **PostgreSQL 18 `max_connections=25` Budget**: Zerops `postgresql:single@18` defaults to 25 connections (22 non-superuser slots). Keep sibling service pools bounded (`paperclip` `DATABASE_POOL_MAX=4`, `whatsappbot` `PG_POOL_MAX=3`, `evolution` `CONNECTION LIMIT 4`) so Bifrost `config_store` + `logs_store` dashboard queries never hit `SQLSTATE 53300`.
