# `bknd`: Backend Infrastructure, Mesh Topology & Sovereign Storage Manual (v2.0)

This manual provides production-grade backend deployment architectures, database sizing blueprints, SeaweedFS POSIX FUSE storage configuration, and the Fractal CoHaLo operational harness in Zerops.

---

## 1. Multi-Service Backend Mesh Topology in Zerops

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Internal High-Speed Mesh Network (<0.3ms P99)                                                   │
│                                                                                                        │
│   ┌──────────────────────────────────┐ ┌──────────────────────────────────┐                            │
│   │ Directus 11+ (directus:8055)     │ │ FastAPI (fastapi:8000)           │                            │
│   │ ├─ Runtime: nodejs@24 (Ubuntu)   │ │ ├─ Runtime: python@3.12 (Granian)│                            │
│   │ ├─ Auth & Headless CRUD          │ │ ├─ pgvector HNSW Semantic Search │                            │
│   │ └─ Mount: /mnt/baiostorage/      │ │ └─ Mount: /mnt/baiostorage/      │                            │
│   └────────────────┬─────────────────┘ └────────────────┬─────────────────┘                            │
│                    │                                    │                                              │
│                    │ asyncpg / pg TCP                   │ NATS TCP                                     │
│                    ▼                                    ▼                                              │
│   ┌──────────────────────────────────┐ ┌──────────────────────────────────┐                            │
│   │ PostgreSQL 18 (db:5432)          │ │ NATS Server 2.12 (nats:4222)     │                            │
│   │ ├─ Extension: pgvector           │ │ ├─ Request-Reply RPC (<0.3ms P99)│                            │
│   │ ├─ Mode: NON_HA / Profile: oltp  │ │ ├─ JetStream Persistence         │                            │
│   │ └─ Daily pg_dump Backups         │ │ └─ HTTP Monitoring: :8222/varz   │                            │
│   └──────────────────────────────────┘ └──────────────────────────────────┘                            │
│                    │                                    │                                              │
│                    │ BullMQ Queues                      │ POSIX FUSE Mount                             │
│                    ▼                                    ▼                                              │
│   ┌──────────────────────────────────┐ ┌──────────────────────────────────┐                            │
│   │ Valkey 7.2 (cache:6379)          │ │ Shared Storage (baiostorage)     │                            │
│   │ ├─ In-Memory Cache & Sessions    │ │ ├─ Engine: SeaweedFS POSIX FUSE  │                            │
│   │ ├─ Rate Limiting Sliding Window  │ │ ├─ Mount: /mnt/baiostorage/      │                            │
│   │ └─ Queue: erpnext-sync, email    │ │ └─ Permissions: chmod -R 777     │                            │
│   └──────────────────────────────────┘ └──────────────────────────────────┘                            │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Managed Database Sizing & Immutability Rules

| Service | Single Node (`:single`) | High Availability (`:ha`) | Recommended Profiles |
|---|---|---|---|
| **PostgreSQL 18** | `postgresql:single@18` | `postgresql:ha@18` | `oltp-hobby`, `oltp-staging`, `oltp-production` |
| **Valkey 7.2** | `valkey:single@7.2` | `valkey:ha@7.2` | `hobby`, `staging`, `production` |
| **NATS 2.12** | `nats:single@2.12` | `nats:ha@2.12` | `hobby`, `staging`, `production` |
| **Shared Storage** | `shared-storage:single`| `shared-storage:ha` | Elastic Disk (`minDisk: 5`, `maxDisk: 100`) |

> **Immutability Invariant:** A database service provisioned as `:single` cannot be converted to `:ha` in-place. Promoting to High Availability requires the `launch-production` workflow.

---

## 3. POSIX Shared Storage Permissions Shield

Zerops shared storage uses SeaweedFS FUSE mounts mapped into unprivileged LXC containers:

1. **Mount Declaration**: Must be declared under `mount: [<storageHostname>]` in `import.yaml`.
2. **Permissions Shield**: Always run `chmod -R 777 /mnt/<storageHostname>/<serviceHostname>/` to allow cross-container read/write operations without UID mismatches.
3. **Strict Prohibition**: Never configure `run.mount` in `zerops.yaml`.

---

## 4. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with `bknd` must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All database queries and health probes must use explicit timeouts (`timeout 10s curl -f http://nats:8222/varz`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all lingering processes using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * NATS probe: `curl -s http://nats:8222/varz | grep -q "version"` $\implies$ Exit 0.
  * Valkey probe: `valkey-cli -u "$VALKEY_URL" ping | grep -q "PONG"` $\implies$ Exit 0.
  * Postgres probe: `psql "$DATABASE_URL" -c "SELECT 1;"` $\implies$ Exit 0.
* **Circuit Breaker Policy**: If database connections drop, enforce exponential retry backoff (max 3 attempts) in service Lifespans before marking instances degraded.
