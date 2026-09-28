# Valkey — Infrastructure & Platform Lifecycle Manual on Zerops

This manual specifies the operational platform model, immutable deployment variants, scaling profiles, port architectures, authentication requirements, and bounded execution harnesses for **Valkey 7.2** on Zerops.

---

## 1. Platform Topology & Deployment Variants

Zerops executes Valkey inside unprivileged **Incus Linux Containers (LXC)** with NVMe storage attached via private encrypted VXLAN networks.

```
+--------------------------------------------------------------------------+
| Valkey Deployment Variants (Immutable after creation)                    |
+------------------------------------+-------------------------------------+
| Variant A: valkey:single@7.2       | Variant B: valkey:ha@7.2            |
| - 1 dedicated Incus LXC node       | - 3 nodes (1 Primary + 2 Replicas)  |
| - Ports: 6379 (RW), 6380 (TLS)     | - Ports: 6379 (RW), 7000 (RO), 7001 |
| - Profile: hobby / staging         | - Auto-failover sub-second          |
| - Ideal for dev, stage, lean prod  | - Ideal for mission-critical cache  |
+------------------------------------+-------------------------------------+
```

---

## 2. Scaling Profiles (`profile:`) & Zero-Guessing Scaling

Valkey in Zerops takes a `profile:` property that automatically configures memory boundaries, eviction policies, and elastic vertical autoscaling tiers:

| Profile | Variant Compatibility | CPU Mode | Recommended Use Case |
|---|---|---|---|
| `hobby` | `:single` only | `SHARED` | Development, testing, and low-cost hobby tier. |
| `staging` | `:single` & `:ha` | `SHARED` | Staging environments and lean production workloads (Default). |
| `production` | `:single` & `:ha` | `DEDICATED` | Mission-critical high-throughput caching with guaranteed dedicated CPU. |

> **Zero-Guessing Scaling Invariant**:
> Do not author manual `verticalAutoscaling` min/max blocks. Specifying `profile: hobby/staging/production` enables Zerops' native dynamic elastic scaling out-of-the-box.

---

## 3. Four-Way Architectural Comparison

| Dimensión Técnica | Managed Valkey `:single` en Zerops | Managed Valkey `:ha` en Zerops | Self-Hosted Redis/Valkey en Generic Ubuntu LXC | Cliente en `os: alpine` vs `os: ubuntu` |
|---|---|---|---|---|
| **Aprovisionamiento** | **1 línea en `import.yaml` (`type: valkey:single@7.2`)** | **1 línea en `import.yaml` (`type: valkey:ha@7.2`)** | Manual vía `apt-get` | `os: alpine` (pure JS/TS/Go/Rust) / `ubuntu` (Python) |
| **Topología** | 1 contenedor Incus LXC (~15-30MB RAM idle) | 3 nodos (1 Master + 2 Réplicas) | 1 contenedor genérico | N/A (conexión por red privada VXLAN) |
| **Failover / HA** | No (reinicio rápido en fallo) | **Automático sub-segundo** con conmutación | Manual | Transparente al cliente vía DNS interno |
| **Puertos de Acceso** | 6379 (RW) + 6380 (TLS) | 6379 (RW) + 7000 (RO Replicas) + TLS | Solo 6379 | Conexión interna directa a 6379 / 7000 |
| **Autenticación** | `${cache_password}` requerida (`default` user) | `${cache_password}` requerida | Manual | Directa con `${cache_connectionString}` |
| **Autoescalado** | **Automático según `profile: hobby/staging`** | **Automático según `profile: staging/production`** | Manual | Dinámico |
| **Casos de Uso** | Cache, Sesiones, BullMQ, Rate Limiting | Cargas críticas de alto throughput en memoria | Necesidad de módulos C no soportados | Alpine para 95% web / Ubuntu para Python ML |

---

## 4. Port Architecture & Mandatory Authentication

### Port Specifications
* **Port 6379 (RW Primary)**: Standard TCP/RESP connection port for reads and writes.
* **Port 6380 (TLS External)**: Secure TLS-encrypted endpoint for external or VPN access (`${cache_portTls}`).
* **Port 7000 (Read Replicas - HA Only)**: Load-balanced endpoint across secondary read replicas (`${cache_portReplicas}`).
* **Port 7001 (Read Replicas TLS - HA Only)**: Encrypted read-replica endpoint.

### Mandatory Authentication Rule
Valkey enforces password authentication. The username is `default` and is not exposed as a variable. All connections MUST supply `${cache_password}` or use the pre-authenticated `${cache_connectionString}`.

---

## 5. Architectural Separation of Responsibilities

```
+--------------------------------------------------------------------------+
| Zerops Workload Distribution Strategy                                    |
+--------------------------------------------------------------------------+
| 1. Valkey (valkey@7.2): In-memory cache, sessions, BullMQ, rate limiting |
| 2. NATS (nats@2.12): Canonical distributed queue, RPC, global event bus   |
| 3. PostgreSQL (postgresql@18): ACID transactional outbox queues (pg-boss)|
| 4. Automation Engine: Workflow state machines & orchestration logic      |
+--------------------------------------------------------------------------+
```

---

## 6. Manifest Specifications (`import.yaml` & `zerops.yaml`)

### Production `import.yaml` Manifest
```yaml
project:
  name: cached-app

services:
  # Managed Valkey Cache Service (Canonical Hostname: cache)
  - hostname: cache
    type: valkey:single@7.2
    profile: staging
    priority: 10

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
        REDIS_HOST: cache
        REDIS_PORT: ${cache_port}
        REDIS_PASSWORD: ${cache_password}
        REDIS_URL: ${cache_connectionString}
```

---

## 7. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

* **Strict Synchronous Timeouts**: All terminal healthchecks and cache queries MUST execute with explicit timeouts:
  ```bash
  timeout 10s redis-cli -u "$REDIS_URL" PING
  ```
* **Circuit Breaker (2-Attempt Limit)**: On consecutive connection failures or timeouts, halt execution and trigger human escalation.
* **Zero Orphaned Tasks Invariant**: Always terminate lingering background inspection tasks:
  ```typescript
  await manage_task({ Action: 'kill', TaskId: taskId });
  ```
