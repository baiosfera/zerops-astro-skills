# FastAPI Microservices: Infrastructure, Granian ASGI & Zerops Deployment Manual (v2.0)

This manual provides production-grade infrastructure blueprints, Granian ASGI server configuration, Astral `uv` fast package installation, `zerops.yaml` lifecycle recipes, and the Fractal CoHaLo operational harness for `fastapi` running in Zerops.

---

## 1. Multi-Service Microservice Topology in Zerops

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Internal High-Speed Network                                                                     │
│                                                                                                        │
│   ┌──────────────────────────────────────────────────┐                                                 │
│   │ FastAPI Microservice (api:8000)                  │                                                 │
│   │ ├─ Base: python@3.12 (Incus LXC)                 │                                                 │
│   │ ├─ ASGI Server: Granian (Rust / uvloop)          │                                                 │
│   │ ├─ Lifespan: asyncpg, pgvector, Valkey, NATS     │                                                 │
│   │ └─ Ports: 8000 (HTTP)                            │                                                 │
│   └───────────────┬──────────────┬──────────────┬────┘                                                 │
│                   │              │              │                                                      │
│                   │ asyncpg TCP  │ RESP3 TCP    │ NATS TCP                                             │
│                   ▼              ▼              ▼                                                      │
│   ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐                                       │
│   │ PostgreSQL 18    │ │ Valkey 7.2 Cache │ │ NATS Server 2.12 │                                       │
│   │ ├─ pgvector Ext. │ │ ├─ Port: 6379    │ │ ├─ Port: 4222    │                                       │
│   │ └─ HNSW Index    │ │ └─ Rate Limiter  │ │ └─ JetStream     │                                       │
│   └──────────────────┘ └──────────────────┘ └──────────────────┘                                       │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Infrastructure Import Manifest (`import.yaml`)

```yaml
project:
  name: fastapi-ecosystem

services:
  # Managed PostgreSQL 18 with pgvector
  - hostname: db
    type: postgresql@18
    mode: NON_HA
    verticalAutoscaling:
      minCpu: 1
      maxCpu: 4
      minRam: 1
      maxRam: 8
      minDisk: 10
      maxDisk: 100

  # Valkey 7.2 In-Memory Cache & Queue
  - hostname: cache
    type: valkey@7.2
    mode: NON_HA
    verticalAutoscaling:
      minCpu: 1
      maxCpu: 2
      minRam: 0.5
      maxRam: 4
      minDisk: 5
      maxDisk: 20

  # FastAPI Microservice on Python 3.12
  - hostname: api
    type: python@3.12
    verticalAutoscaling:
      minCpu: 1
      maxCpu: 4
      minRam: 0.5
      maxRam: 4
      minDisk: 5
      maxDisk: 50
    minContainers: 1
    maxContainers: 4
```

---

## 3. Canonical Lifecycle Recipe (`zerops.yaml`)

```yaml
zerops:
  - setup: prod
    build:
      base: python@3.12
      prepareCommands:
        - sudo apk add --no-cache curl build-base libffi-dev postgresql-dev
      buildCommands:
        - curl -LsSf https://astral.sh/uv/install.sh | sh
        - export PATH="/root/.local/bin:$PATH"
        - uv pip install --target=./vendor -r requirements.txt
      deployFiles:
        - ./src
        - ./assets
        - ./vendor
      cache:
        - vendor

    deploy:
      readinessCheck:
        httpGet:
          port: 8000
          path: /healthz

    run:
      base: python@3.12
      ports:
        - port: 8000
          httpSupport: true
      envVariables:
        PYTHONPATH: /var/www/vendor
        PYTHONUNBUFFERED: "1"
        ENVIRONMENT: production
        DATABASE_URL: postgresql://${db_user}:${db_password}@${db_hostname}:${db_port}/${db_hostname}
        VALKEY_HOST: ${cache_hostname}
        VALKEY_PORT: ${cache_port}
        NATS_URL: nats://nats:4222
      start: >-
        /var/www/vendor/bin/granian
        --interface asgi
        --host 0.0.0.0
        --port 8000
        --workers 2
        --runtime-threads 1
        --blocking-threads 1
        --loop uvloop
        --http auto
        --no-ws
        --backlog 2048
        --backpressure 1024
        --log
        --log-level info
        --no-access-log
        src.main:app
```

---

## 4. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with `fastapi` must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All internal API calls and database probes must use explicit timeouts (`timeout 10s curl -f http://0.0.0.0:8000/healthz`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all lingering dev servers using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Healthz probe check: `curl -s http://0.0.0.0:8000/healthz | grep -q "status"` $\implies$ Exit 0.
* **Circuit Breaker Policy**: If PostgreSQL or Valkey is temporarily restarting during startup, the Lifespan handles connection retries with exponential backoff before failing readiness checks.
