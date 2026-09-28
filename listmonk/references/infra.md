# Listmonk Infrastructure, Zerops Topology & Lifecycle Manual (v1.0)

This manual provides production-grade infrastructure blueprints, multi-service `import.yaml` provisioning recipes (including **PostgreSQL**, **NATS**, and **Valkey**), `zerops.yaml` pipeline lifecycles, environment variable mapping, and the Fractal CoHaLo operational harness for Listmonk in Zerops.

---

## 1. Zerops Multi-Service Architecture & Topology

Listmonk operates within a secure, high-speed internal Zerops virtual network alongside PostgreSQL (storage), NATS (event messaging), and Valkey (caching/rate limiting):

```
┌────────────────────────────────────────────────────────────────────────┐
│ Zerops Project Topology                                                │
│                                                                        │
│   ┌────────────────────────┐          ┌────────────────────────────┐   │
│   │ Listmonk Service       │          │ Managed PostgreSQL (db)    │   │
│   │ (go@1.22 / os: alpine) │─────────▶│ (postgresql@16:single/:ha) │   │
│   │ Port 9000 (HTTP)       │          │ Port 5432 (Internal)       │   │
│   └───────────▲────────────┘          └────────────────────────────┘   │
│               │                                                        │
│               │ HTTP POST /api/tx                                      │
│               │                                                        │
│   ┌───────────┴────────────┐          ┌────────────────────────────┐   │
│   │ App / Email Worker     │─────────▶│ NATS JetStream (nats)      │   │
│   │ (nodejs / bun / go)    │          │ Port 4222 (Internal)       │   │
│   └───────────┬────────────┘          └────────────────────────────┘   │
│               │                                                        │
│               │ Rate-Limit & Locks                                     │
│               ▼                                                        │
│   ┌────────────────────────┐          ┌────────────────────────────┐   │
│   │ Valkey Cache (cache)   │          │ Shared Storage (NFS)       │   │
│   │ (valkey@7.2 / redis)   │          │ /mnt/baiostorage/listmonk/ │   │
│   │ Port 6379 (Internal)   │          │ (Persistent uploads)       │   │
│   └────────────────────────┘          └────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Service Provisioning Blueprint (`import.yaml`)

```yaml
services:
  # 1. Managed PostgreSQL for Listmonk SSoT Data & Subscribers
  - hostname: db
    type: postgresql@16:single
    mode: NON_HA

  # 2. Managed Valkey In-Memory Cache (Rate limiting & Idempotency)
  - hostname: cache
    type: valkey@7.2:single
    mode: NON_HA

  # 3. NATS JetStream Message Broker (Event-Driven Dispatch)
  - hostname: nats
    type: nats@2.10

  # 4. Listmonk Native Go / Web Application
  - hostname: listmonk
    type: go@1.22
    enableSubdomainAccess: true

  # 5. Shared Storage for Campaign Uploads & Attachments
  - hostname: baiostorage
    type: shared-storage
```

*Note: Zerops automatically scales CPU and RAM vertically and elastically according to live traffic across all managed services.*

---

## 3. Production Deployment Lifecycle (`zerops.yaml`)

```yaml
zerops:
  - setup: listmonk
    build:
      os: alpine
      prepareCommands:
        - sudo apk add --no-cache curl tar ca-certificates
        # Download official static Listmonk release binary for Linux amd64
        - curl -sSL https://github.com/knadh/listmonk/releases/download/v5.1.0/listmonk_5.1.0_linux_amd64.tar.gz -o listmonk.tar.gz
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
        - sudo apk add --no-cache ca-certificates tzdata curl
        # Ensure uploads storage directory permissions on FUSE mount
        - sudo mkdir -p /mnt/baiostorage/listmonk/uploads 2>/dev/null || true
        - sudo chmod -R 777 /mnt/baiostorage/listmonk/uploads 2>/dev/null || true

      initCommands:
        # Atomic, idempotent schema install and upgrade on every release
        - zsc execOnce ${appVersionId} -- ./listmonk --install --idempotent --yes --config=""
        - zsc execOnce ${appVersionId} -- ./listmonk --upgrade --yes --config=""

      start: ./listmonk --config=""

      ports:
        - port: 9000
          httpSupport: true

      envVariables:
        # Server listen address
        LISTMONK_app__address: "0.0.0.0:9000"
        
        # PostgreSQL dynamic connection string binding from Zerops
        LISTMONK_db__host: ${db_hostname}
        LISTMONK_db__port: ${db_port}
        LISTMONK_db__user: ${db_user}
        LISTMONK_db__password: ${db_password}
        LISTMONK_db__database: ${db_database}
        LISTMONK_db__ssl_mode: disable
        LISTMONK_db__max_open: 50
        LISTMONK_db__max_idle: 25
        LISTMONK_db__max_lifetime: "300s"

        # Admin initial bootstrap credentials
        LISTMONK_ADMIN_USER: "admin"
        LISTMONK_ADMIN_PASSWORD: "CHANGE_ME_IN_PRODUCTION"
```

---

## 4. Environment Variables Reference Dictionary

Listmonk parses any variable prefixed with `LISTMONK_` by converting double underscores (`__`) to nested TOML table fields:

| Environment Variable | Target Configuration Key | Description |
|---|---|---|
| `LISTMONK_app__address` | `app.address` | Binding host and port (default `"0.0.0.0:9000"`) |
| `LISTMONK_app__root_url` | `app.root_url` | Public canonical base URL for link tracking |
| `LISTMONK_app__logo_url` | `app.logo_url` | URL of the logo displayed in emails and login UI |
| `LISTMONK_db__host` | `db.host` | PostgreSQL server hostname (`${db_hostname}`) |
| `LISTMONK_db__port` | `db.port` | PostgreSQL server port (`${db_port}`) |
| `LISTMONK_db__user` | `db.user` | PostgreSQL username (`${db_user}`) |
| `LISTMONK_db__password` | `db.password` | PostgreSQL password (`${db_password}`) |
| `LISTMONK_db__database` | `db.database` | PostgreSQL database name (`${db_database}`) |
| `LISTMONK_db__ssl_mode` | `db.ssl_mode` | SSL connection mode (`disable`, `prefer`, `require`) |
| `LISTMONK_db__max_open` | `db.max_open` | Max open pool connections (recommended: `25–50`) |
| `LISTMONK_db__max_idle` | `db.max_idle` | Max idle pool connections (recommended: `10–25`) |
| `LISTMONK_ADMIN_USER` | CLI bootstrap env | Initial Super Admin username during `--install` |
| `LISTMONK_ADMIN_PASSWORD` | CLI bootstrap env | Initial Super Admin password during `--install` |

---

## 5. Storage & FUSE Volume Mounting

When persisting uploaded assets, media, and campaign images:

1. Create directory on shared storage: `/mnt/baiostorage/listmonk/uploads`
2. Apply permission shield: `sudo chmod -R 777 /mnt/baiostorage/listmonk/uploads`
3. In Listmonk Settings UI (`Settings -> Media`): Set upload provider to `Filesystem` with upload path `/mnt/baiostorage/listmonk/uploads`.

---

## 6. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with Listmonk must comply with the Fractal CoHaLo standards:

* **Bounded Timeouts**: All health check and API probe invocations must be wrapped with strict timeouts (`timeout 10s curl -f http://listmonk:9000/admin`).
* **Synchronous Wait Enforcement**: For CLI operations and API verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Always terminate background test servers and dangling workers via `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Health verification: `curl -s -o /dev/null -w "%{http_code}" http://listmonk:9000/admin` $\implies$ Expected: `200` or `302`.
  * Database connectivity: `psql "$db_connectionString" -c 'SELECT count(*) FROM subscribers;'`.
* **Circuit Breaker Policy**: If database migrations fail or return exit code $\ne 0$, retry a maximum of 2 times. If the second retry fails, trigger escalation and halt execution without muting errors.
