# PostgreSQL — Infrastructure & Platform Lifecycle Manual on Zerops

This manual specifies the operational platform model, immutable deployment variants, scaling profiles, port architectures, extension installation flows, and bounded execution harnesses for **PostgreSQL 18** on Zerops.

---

## 1. Platform Topology & Deployment Variants

Zerops executes PostgreSQL inside unprivileged **Incus Linux Containers (LXC)** with NVMe block storage attached via private encrypted VXLAN networks.

```
+--------------------------------------------------------------------------+
| PostgreSQL Deployment Variants (Immutable after creation)               |
+------------------------------------+-------------------------------------+
| Variant A: postgresql:single@18    | Variant B: postgresql:ha@18         |
| - 1 dedicated Incus LXC node       | - 3 nodes on independent hosts      |
| - Ports: 5432 (RW), 6432 (TLS)     | - Ports: 5432 (RW), 5433 (RO), 6432 |
| - Profile: oltp-hobby / oltp-stage | - Patroni auto-failover (<1s)       |
| - Ideal for dev, stage, lean prod  | - Ideal for mission-critical HA prod|
+------------------------------------+-------------------------------------+
```

---

## 2. Scaling Profiles (`profile:`) & Zero-Guessing Scaling

PostgreSQL in Zerops takes a `profile:` property that automatically configures kernel parameters, buffer pools, and elastic vertical autoscaling tiers:

| Profile | Variant Compatibility | CPU Mode | Recommended Use Case |
|---|---|---|---|
| `oltp-hobby` | `:single` only | `SHARED` | Development, testing, and hobby tier. |
| `oltp-staging` | `:single` & `:ha` | `SHARED` | Staging environments and lean production workloads. |
| `oltp-production` | `:single` & `:ha` | `DEDICATED` | Mission-critical high-throughput production (dedicated CPU). |
| `oltp-enterprise` | `:ha` only | `DEDICATED` | Massive enterprise OLTP workloads with extreme concurrency. |
| `olap-production` | `:single` & `:ha` | `DEDICATED` | Analytics and heavy analytical scan queries. |
| `writeheavy-production` | `:single` & `:ha` | `DEDICATED` | High-frequency append-only write streams and time-series ingests. |

> **Zero-Guessing Scaling Invariant**:
> Do NOT author manual `verticalAutoscaling` min/max blocks. Specifying `profile: oltp-*` enables Zerops' native dynamic elastic scaling out-of-the-box.

---

## 3. Four-Way Architectural Comparison

| Dimensión Técnica | Managed PostgreSQL `:single` en Zerops | Managed PostgreSQL `:ha` en Zerops | Self-Hosted PostgreSQL en Generic Ubuntu LXC | Cliente en `os: alpine` vs `os: ubuntu` |
|---|---|---|---|---|
| **Aprovisionamiento** | **1 línea en `import.yaml` (`type: postgresql:single@18`)** | **1 línea en `import.yaml` (`type: postgresql:ha@18`)** | Manual con `apt-get install postgresql` | `os: alpine` (pure JS/TS/Go/Rust) / `ubuntu` (C-extensions) |
| **Topología** | 1 contenedor LXC con NVMe dedicado | 3 nodos en hosts físicos independientes | 1 contenedor genérico sin backups automáticos | N/A (conexión por red privada VXLAN) |
| **Failover / HA** | No (reinicio rápido en fallo de nodo) | **Automático sub-segundo** con Patroni | Manual / Requiere configurar clustering propio | Transparente al cliente vía DNS interno |
| **Puertos de Acceso** | 5432 (RW) + 6432 (pgBouncer TLS) | 5432 (RW) + 5433 (RO Replicas) + 6432 (TLS) | Solo 5432 (salvo instalar PgBouncer a mano) | Conexión interna directa a 5432 / 5433 |
| **Backups Gestionados** | Automáticos cifrados diarios | Automáticos cifrados diarios | Manual (scripts cron propios) | N/A |
| **Autoescalado** | **Automático según `profile: oltp-*`** | **Automático según `profile: oltp-*`** | Manual | Dinámico |
| **Casos de Uso** | Dev, Staging, Producción Lean | Producción crítica de misión alta | Necesidad de plugins de SO no soportados | Alpine para 95% web / Ubuntu para Python ML |

---

## 4. Port Architecture & Routing Rules

* **Port 5432 (RW Primary)**: Direct transactional read/write connection to the primary leader.
* **Port 5433 (Read Replicas - HA Only)**: Load-balanced connection across asynchronous read replicas.
* **Port 6432 (PgBouncer with TLS)**: External access via TLS pooling (`${db_portTls}`).

---

## 5. Superuser Extension Provisioning Flow

To install extensions (`vector`, `pg_stat_statements`, `pg_trgm`, `postgis`):
1. Execute `CREATE EXTENSION` using the `superUser` (`postgres`) credentials against `${db_dbName}`:
   ```bash
   psql "postgresql://$db_superUser:$db_superUserPassword@db:5432/$db_dbName" -c "CREATE EXTENSION IF NOT EXISTS vector;"
   ```
2. **Mandatory Service Restart**: Restart the service to initialize `shared_preload_libraries`:
   ```bash
   zerops_manage action="restart" serviceHostname="db"
   ```

---

## 6. Manifest Specifications (`import.yaml` & `zerops.yaml`)

### Production `import.yaml` Manifest
```yaml
project:
  name: production-app

services:
  # Managed PostgreSQL HA Cluster
  - hostname: db
    type: postgresql:ha@18
    profile: oltp-staging
    priority: 10

  # Managed Valkey Cache
  - hostname: cache
    type: valkey@7.2:single
    profile: staging

  # Application Runtime (Node.js/Bun)
  - hostname: api
    type: nodejs@22
    enableSubdomainAccess: true
```

### Application Cross-Service Wiring in `zerops.yaml`
```yaml
zerops:
  - setup: prod
    run:
      envVariables:
        DB_HOST: db
        DB_PORT: ${db_port}
        DB_NAME: ${db_dbName}
        DB_USER: ${db_user}
        DB_PASS: ${db_password}
        DATABASE_URL: postgresql://${db_user}:${db_password}@db:${db_port}/${db_dbName}
```

---

## 7. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

* **Strict Synchronous Timeouts**: All terminal queries and connectivity checks MUST execute with explicit timeouts:
  ```bash
  timeout 10s psql "$DATABASE_URL" -c "SELECT 1;"
  ```
* **Circuit Breaker (2-Attempt Limit)**: On consecutive connection failures or timeouts, halt execution and trigger human escalation.
* **Zero Orphaned Tasks Invariant**: Always terminate lingering background inspection tasks:
  ```typescript
  await manage_task({ Action: 'kill', TaskId: taskId });
  ```
