# Evolution Go Infrastructure, Zerops Topology & Lifecycle Manual (v1.0)

This manual provides the production-grade infrastructure blueprints, multi-service `import.yaml` provisioning recipes (including **Astro**, **Directus**, **Evolution Go**, **AI Worker**, **PostgreSQL**, **NATS**, and **Valkey**), `zerops.yaml` pipeline lifecycles, environment variable mapping, and the Fractal CoHaLo operational harness for Evolution Go running in Zerops.

---

## 1. Multi-Service Zerops Ecosystem Topology

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Enterprise Project Topology                                                                     │
│                                                                                                        │
│   ┌──────────────────────────────┐              ┌──────────────────────────────────────────────────┐   │
│   │ Astro Frontend UI (astro)    │              │ Directus Backend CMS / CRM (directus)            │   │
│   │ (bun@1.3 / nodejs@20)        │─────────────▶│ (nodejs@20 / os: alpine)                         │   │
│   │ Port 3000 (HTTP Subdomain)   │              │ Port 8055 (HTTP Subdomain)                       │   │
│   └──────────────────────────────┘              └────────────────────────┬─────────────────────────┘   │
│                                                                          │                             │
│   ┌──────────────────────────────┐              ┌────────────────────────▼─────────────────────────┐   │
│   │ Evolution Go Gateway (evogo) │              │ NATS JetStream Message Broker (nats)             │   │
│   │ (go@1.22 / os: alpine)       │◀────────────▶│ (nats@2.10)                                      │   │
│   │ Port 8080 (Internal / Sub)   │              │ Port 4222 (Internal Zerops DNS)                  │   │
│   └──────────────┬───────────────┘              └────────────────────────┬─────────────────────────┘   │
│                  │                                                       │                             │
│                  │ Media uploads                                         ▼                             │
│                  ▼                              ┌──────────────────────────────────────────────────┐   │
│   ┌──────────────────────────────┐              │ Intelligent AI / LLM Agent Worker (aiworker)     │   │
│   │ Shared Storage (baiostorage) │              │ (python@3.12 / nodejs@20)                        │   │
│   │ /mnt/baiostorage/evolutiongo │              │ - Consumes NATS events & executes OpenAI/Whisper │   │
│   └──────────────────────────────┘              └────────────────────────┬─────────────────────────┘   │
│                                                                          │                             │
│                  ┌───────────────────────────────────────────────────────┴─────────┐                   │
│                  ▼                                                                 ▼                   │
│   ┌──────────────────────────────────────────┐  ┌──────────────────────────────────────────────────┐   │
│   │ Valkey In-Memory Cache (cache)           │  │ Managed PostgreSQL Cluster (db)                  │   │
│   │ (valkey@7.2:single / HA)                 │  │ (postgresql@16:single / HA)                      │   │
│   │ Port 6379 (Internal Zerops DNS)          │  │ Port 5432 (Internal Zerops DNS)                  │   │
│   └──────────────────────────────────────────┘  └──────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Service Provisioning Blueprint (`import.yaml`)

```yaml
services:
  # 1. Managed PostgreSQL for Evolution Go (Auth + Users) & Directus
  - hostname: db
    type: postgresql@16:single
    mode: NON_HA

  # 2. Managed Valkey In-Memory Cache (Chat memory & Idempotency)
  - hostname: cache
    type: valkey@7.2:single
    mode: NON_HA

  # 3. NATS JetStream Event Broker
  - hostname: nats
    type: nats@2.10

  # 4. Evolution Go Native Gateway
  - hostname: evolutiongo
    type: go@1.22
    enableSubdomainAccess: true

  # 5. Directus Headless CMS & CRM Engine
  - hostname: directus
    type: nodejs@20
    enableSubdomainAccess: true

  # 6. Intelligent AI / LLM Worker
  - hostname: aiworker
    type: nodejs@20

  # 7. Astro Frontend Webapp
  - hostname: astro
    type: nodejs@20
    enableSubdomainAccess: true

  # 8. Persistent Shared Storage for Media & Attachments
  - hostname: baiostorage
    type: shared-storage
```

---

## 3. Production Deployment Lifecycle (`zerops.yaml`)

```yaml
zerops:
  - setup: evolutiongo
    build:
      os: alpine
      prepareCommands:
        - sudo apk add --no-cache curl tar git ca-certificates
        # Build from official evolution-foundation repository
        - git clone --depth 1 https://github.com/evolution-foundation/evolution-go.git .
        - go mod download
        - CGO_ENABLED=0 go build -ldflags="-s -w" -o evolution-go cmd/server/main.go
      deployFiles:
        - evolution-go
      cache:
        - /go/pkg/mod

    run:
      os: alpine
      prepareCommands:
        - sudo apk add --no-cache ca-certificates tzdata curl
        # Prepare persistent media directory on NFS mount
        - sudo mkdir -p /mnt/baiostorage/evolutiongo/media 2>/dev/null || true
        - sudo chmod -R 777 /mnt/baiostorage/evolutiongo/media 2>/dev/null || true

      initCommands:
        # Ensure database schemas exist before starting service
        - zsc execOnce ${appVersionId} -- psql "$db_connectionString" -c 'CREATE DATABASE evogo_auth;' 2>/dev/null || true
        - zsc execOnce ${appVersionId} -- psql "$db_connectionString" -c 'CREATE DATABASE evogo_users;' 2>/dev/null || true

      start: ./evolution-go

      ports:
        - port: 8080
          httpSupport: true

      envVariables:
        SERVER_PORT: "8080"
        CLIENT_NAME: "evolution"
        GLOBAL_API_KEY: "CHANGE_ME_IN_PRODUCTION_SUPER_SECRET_KEY"
        
        # Dual PostgreSQL database wiring via Zerops dynamic variables
        POSTGRES_AUTH_DB: "postgresql://${db_user}:${db_password}@${db_hostname}:${db_port}/evogo_auth?sslmode=disable"
        POSTGRES_USERS_DB: "postgresql://${db_user}:${db_password}@${db_hostname}:${db_port}/evogo_users?sslmode=disable"
        DATABASE_SAVE_MESSAGES: "true"

        # Event stream binding to Zerops NATS JetStream
        NATS_URL: "nats://${nats_hostname}:${nats_port}"

        # Logging & Debugging
        WADEBUG: "INFO"
        LOGTYPE: "console"

        # Webhook fallback URL
        WEBHOOK_URL: "http://aiworker:3000/webhook"
        WEBHOOK_BY_EVENTS: "true"
```

---

## 4. Environment Variables Reference Dictionary

| Variable | Description | Default / Example Value |
|---|---|---|
| `SERVER_PORT` | HTTP Server port | `"8080"` |
| `CLIENT_NAME` | WhatsApp client identifier | `"evolution"` |
| `GLOBAL_API_KEY` | Super Admin secret for authentication | Required in production |
| `POSTGRES_AUTH_DB` | Connection URI for authentication and session keys | `postgresql://${db_user}:${db_password}@${db_hostname}:${db_port}/evogo_auth?sslmode=disable` |
| `POSTGRES_USERS_DB` | Connection URI for messages, chats, and contacts | `postgresql://${db_user}:${db_password}@${db_hostname}:${db_port}/evogo_users?sslmode=disable` |
| `DATABASE_SAVE_MESSAGES` | Persist incoming/outgoing messages in PostgreSQL | `"true"` or `"false"` |
| `NATS_URL` | NATS JetStream server URI for event distribution | `nats://${nats_hostname}:${nats_port}` |
| `AMQP_URL` | RabbitMQ server URI (optional alternative to NATS) | `amqp://user:pass@host:5672/` |
| `WEBHOOK_URL` | HTTP endpoint receiving instance events | `http://aiworker:3000/webhook` |
| `WEBHOOK_BY_EVENTS` | Split webhook events into granular subscriptions | `"true"` |
| `PASSKEY_PUBLIC_URL` | Public API URL used during WebAuthn Passkey pairing | `https://whatsapp-api.yourdomain.com` |
| `EVOLUTION_OPERATOR_EMAIL`| Auto-registration email for headless license check | `operator@company.com` |
| `WADEBUG` | whatsmeow log level | `"DEBUG"`, `"INFO"`, `"ERROR"` |

---

## 5. Storage & FUSE Volume Mounting

When handling incoming audio notes, PDFs, images, and stickers:

1. Mount shared storage volume: `/mnt/baiostorage/evolutiongo/media`
2. Apply permission shield: `sudo chmod -R 777 /mnt/baiostorage/evolutiongo`
3. If using S3/MinIO compatible object store, set:
   - `MINIO_ENABLED: "true"`
   - `MINIO_ENDPOINT: "storage.yourdomain.com"`
   - `MINIO_ACCESS_KEY: "${storage_accessKey}"`
   - `MINIO_SECRET_KEY: "${storage_secretKey}"`

---

## 6. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with Evolution Go must strictly follow the Fractal CoHaLo standard:

* **Bounded Timeouts**: All health check probes and API inquiries must use explicit timeouts (`timeout 10s curl -f http://evolutiongo:8080/health`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all lingering workers and background monitoring scripts using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Gateway health check: `curl -s -o /dev/null -w "%{http_code}" http://evolutiongo:8080/health` $\implies$ Expected: `200`.
  * Database connectivity: `psql "$db_connectionString" -c 'SELECT count(*) FROM whatsmeow_device;'`.
* **Circuit Breaker Policy**: If instance pairing fails 2 consecutive times due to socket drop, initiate automatic logout via `DELETE /instance/logout/{instance}` and restart instance socket cleanly.
