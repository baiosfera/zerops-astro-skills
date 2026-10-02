# Listmonk Infrastructure, Zerops Topology & Lifecycle Manual (v2.0)

This manual provides production-grade infrastructure blueprints, multi-service `import.yaml` provisioning recipes (including **PostgreSQL 18**, **NATS 2.12**, and **Valkey 7.2**), `zerops.yaml` pipeline lifecycles, environment variable mapping, horizontal multi-container scaling with the `--passive` flag, and the Fractal CoHaLo operational harness for Listmonk in Zerops.

---

## 1. Zerops Multi-Service Architecture & Topology

Listmonk operates within a secure, high-speed internal Zerops virtual network alongside PostgreSQL 18 (storage), NATS 2.12 (event messaging), Valkey 7.2 (caching/rate limiting), and Zerops Object Storage (S3):

```
┌────────────────────────────────────────────────────────────────────────┐
│ Zerops Project Topology                                                │
│                                                                        │
│   ┌────────────────────────┐          ┌────────────────────────────┐   │
│   │ Listmonk Primary       │          │ Managed PostgreSQL (db)    │   │
│   │ (go@1.22 / os: alpine) │─────────▶│ (postgresql:single@18)    │   │
│   │ Port 9000 (HTTP)       │          │ Port 5432 (Internal)       │   │
│   └───────────▲────────────┘          └────────────────────────────┘   │
│               │                                                        │
│               │ HTTP POST /api/tx                                      │
│               │                                                        │
│   ┌───────────┴────────────┐          ┌────────────────────────────┐   │
│   │ App / Astro 5 SSR      │─────────▶│ NATS JetStream (nats)      │   │
│   │ (bun@1.3 / webdev:3000)│          │ Port 4222 (Internal)       │   │
│   └───────────┬────────────┘          └────────────────────────────┘   │
│               │                                                        │
│               │ Rate-Limit & Locks                                     │
│               ▼                                                        │
│   ┌────────────────────────┐          ┌────────────────────────────┐   │
│   │ Valkey Cache (cache)   │          │ S3 Object Storage (object) │   │
│   │ (valkey:single@7.2)    │          │ Campaign Media & Assets    │   │
│   │ Port 6379 (Internal)   │          │ (Uploads Proxy Provider)   │   │
│   └────────────────────────┘          └────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Service Provisioning Blueprint (`import.yaml`)

```yaml
services:
  # 1. Managed PostgreSQL 18 for Listmonk SSoT Data & Subscribers
  - hostname: db
    type: postgresql:single@18
    mode: NON_HA

  # 2. Managed Valkey In-Memory Cache (Rate limiting & Idempotency)
  - hostname: cache
    type: valkey:single@7.2
    mode: NON_HA

  # 3. NATS JetStream Message Broker (Event-Driven Dispatch)
  - hostname: nats
    type: nats:single@2.12

  # 4. Listmonk Native Go / Web Application
  - hostname: listmonk
    type: go@1.22
    enableSubdomainAccess: true

  # 5. S3-Compatible Object Storage for Campaign Media Uploads
  - hostname: objectstorage
    type: object-storage
```

---

## 3. Production Deployment Lifecycle (`zerops.yaml`)

### Multi-Container Horizontal Scaling & `--passive` Flag
When running 2 or more containers of Listmonk to handle high API traffic, only **one** instance should execute the campaign scheduler. Auxiliary replica containers must pass the `--passive` flag to prevent duplicate email job execution across campaigns:

```yaml
zerops:
  - setup: listmonk
    build:
      os: alpine
      prepareCommands:
        - sudo apk add --no-cache curl tar ca-certificates
        - curl -sSL https://github.com/knadh/listmonk/releases/download/v6.2.0/listmonk_6.2.0_linux_amd64.tar.gz -o listmonk.tar.gz
        - tar -xzf listmonk.tar.gz
        - chmod +x listmonk
      deployFiles:
        - listmonk
        - static
        - i18n
      cache:
        - listmonk.tar.gz
    run:
      os: alpine
      prepareCommands:
        - sudo apk add --no-cache ca-certificates tzdata curl postgresql-client
      initCommands:
        # Pre-create schema in PostgreSQL 18 before running install
        - PGPASSWORD="${db_password}" psql -h "${db_hostname}" -U "${db_user}" -d "${db_database}" -c "CREATE SCHEMA IF NOT EXISTS listmonk;"
        # Idempotent database migrations wrapped in zsc execOnce
        - zsc execOnce ${appVersionId} -- ./listmonk --install --idempotent --yes --config=""
        - zsc execOnce ${appVersionId} -- ./listmonk --upgrade --yes --config=""
      # Primary container runs active scheduler; horizontal scaling replicas should run with --passive
      start: ./listmonk --config=""
      ports:
        - port: 9000
          httpSupport: true
      envVariables:
        LISTMONK_app__address: "0.0.0.0:9000"
        LISTMONK_db__host: ${db_hostname}
        LISTMONK_db__port: ${db_port}
        LISTMONK_db__user: ${db_user}
        LISTMONK_db__password: ${db_password}
        LISTMONK_db__database: ${db_database}
        LISTMONK_db__ssl_mode: disable
        LISTMONK_db__params: "search_path=listmonk,public"
        LISTMONK_db__max_open: "50"
        LISTMONK_db__max_idle: "25"
        LISTMONK_db__max_lifetime: "300s"
        # S3 Media Upload Provider
        LISTMONK_upload__provider: "s3"
        LISTMONK_upload__s3__url: ${objectstorage_apiUrl}
        LISTMONK_upload__s3__public_url: ${objectstorage_apiUrl}/${objectstorage_bucket}
        LISTMONK_upload__s3__aws_access_key_id: ${objectstorage_accessKeyId}
        LISTMONK_upload__s3__aws_secret_access_key: ${objectstorage_secretAccessKey}
        LISTMONK_upload__s3__aws_default_region: "us-east-1"
        LISTMONK_upload__s3__bucket: ${objectstorage_bucket}
```

---

## 4. Environment Variables Dictionary (Double Underscore Mapping)

| Variable | Zerops Source | Target Property | Description |
|---|---|---|---|
| `LISTMONK_app__address` | Literal | `app.address` | Bind interface and port (`0.0.0.0:9000`) |
| `LISTMONK_db__host` | `${db_hostname}` | `db.host` | PostgreSQL 18 internal host |
| `LISTMONK_db__port` | `${db_port}` | `db.port` | PostgreSQL port (5432) |
| `LISTMONK_db__user` | `${db_user}` | `db.user` | Database user |
| `LISTMONK_db__password` | `${db_password}` | `db.password` | Database password |
| `LISTMONK_db__database` | `${db_database}` | `db.database` | Database name |
| `LISTMONK_db__params` | Literal | `db.params` | Must include `search_path=listmonk,public` |
| `LISTMONK_upload__provider` | Literal | `upload.provider` | Set to `"s3"` for agnostic media storage |

---

## 5. PostgreSQL 18 Schema Pre-Creation & pgcrypto Resolution

In PostgreSQL 18, extension installation requires explicit schema placement. Running:
```sql
CREATE SCHEMA IF NOT EXISTS listmonk;
```
prior to `./listmonk --install` coupled with `search_path=listmonk,public` prevents:
- `ERROR: relation "settings" does not exist`
- `ERROR: function gen_random_uuid() does not exist`

The `zsc execOnce` wrapper ensures only the first container executes the migration step during multi-container rolling deployments.
