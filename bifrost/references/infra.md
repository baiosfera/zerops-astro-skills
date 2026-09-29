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

### Production Mode: PostgreSQL 18 + Valkey 7.2 (Mandatory)
Bifrost in Zerops must persist its configuration and logs in managed PostgreSQL 18 (`type: postgresql:single@18` or `postgresql:ha@18`) and cache via Valkey 7.2 (`valkey:single@7.2`).

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
    "type": "redis",
    "config": {
      "addr": "env.VALKEY_ADDR",
      "password": "env.VALKEY_PASSWORD",
      "db": 0,
      "use_tls": false,
      "cluster_mode": false
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
        "default_cache_key": "elplacerdc-production-cache",
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
