# NATS Server — Infrastructure & Platform Lifecycle Manual on Zerops

This manual specifies the operational platform model, immutable deployment variants, port architectures, double-auth prevention rules, and bounded execution harnesses for **NATS Server 2.12** on Zerops.

---

## 1. Platform Topology & Deployment Variants

Zerops executes NATS Server inside unprivileged **Incus Linux Containers (LXC)** attached to an isolated, encrypted VXLAN private network.

```
+--------------------------------------------------------------------------+
| NATS Server Deployment Variants (Immutable after creation)               |
+------------------------------------+-------------------------------------+
| Variant A: nats:single@2.12        | Variant B: nats:ha@2.12             |
| - 1 dedicated Incus LXC node       | - 3 nodes on independent hosts      |
| - Ports: 4222 (Client), 8222 (HTTP)| - Ports: 4222 (Client), 8222 (HTTP) |
| - JetStream: R1 local persistence  | - JetStream: R3 RAFT replication    |
| - Ideal for dev, stage, standard   | - Ideal for high-durability clusters|
+------------------------------------+-------------------------------------+
```

> **Automatic Vertical Autoscaling Invariant**:
> Do not author manual `verticalAutoscaling` min/max blocks. Zerops natively monitors CPU and memory usage and auto-scales vertically on demand with sub-second responsiveness.

---

## 2. Four-Way Architectural Comparison

| Dimensión Técnica | Managed NATS `:single` en Zerops | Managed NATS `:ha` en Zerops | Self-Hosted NATS en Generic Ubuntu LXC | Cliente en `os: alpine` vs `os: ubuntu` |
|---|---|---|---|---|
| **Aprovisionamiento** | **1 línea en `import.yaml` (`type: nats:single@2.12`)** | **1 línea en `import.yaml` (`type: nats:ha@2.12`)** | Manual vía `apt-get` o binario | `os: alpine` (pure Go/TS/Rust) / `ubuntu` (Python `nats-py`) |
| **Topología** | 1 contenedor Incus LXC (~6-15MB RAM idle) | 3 nodos en hosts físicos (RAFT Cluster) | 1 contenedor genérico | N/A (conexión por red privada VXLAN) |
| **Persistencia JetStream** | R1 (Almacenamiento en disco local / RAM) | **R3 (Replicación en 3 nodos con RAFT)** | Manual | Transparente al cliente |
| **Puertos de Acceso** | 4222 (Cliente) + 8222 (HTTP Metrics) | 4222 (Cliente) + 8222 (HTTP Metrics) | Solo los configurados a mano | Conexión interna directa a 4222 |
| **Rendimiento Request-Reply** | **<0.3ms P99** | **<0.5ms P99** | <0.3ms | Sub-milisegundo en ambos entornos |
| **Autoescalado Vertical** | **Elástico Automático Nativo (`min < max`)** | **Elástico Automático Nativo (`min < max`)** | Manual | Dinámico |
| **Casos de Uso** | Cola canónica para 95% de apps, microservicios | Cargas transaccionales críticas de alta durabilidad | Necesidad de flags o configuraciones custom | Alpine para Go/TS/Rust / Ubuntu para Python |

---

## 3. Port Architecture & Double-Auth Prevention

### Port Specifications
* **Port 4222**: NATS client connection port for TCP messaging over internal VXLAN.
* **Port 8222**: HTTP monitoring endpoint (`/healthz`, `/varz`, `/jsz`, `/connz`).

### Double-Auth Prevention Rules
Do **NOT** hand-compose connection URLs like `nats://${user}:${password}@${host}:4222`. Most NATS SDKs parse the URL credentials and simultaneously attempt SASL authentication, triggering an immediate `Authorization Violation` error.

**Supported Pattern A (Recommended)**:
```yaml
envVariables:
  NATS_HOST: ${queue_hostname}
  NATS_PORT: ${queue_port}
  NATS_USER: ${queue_user}
  NATS_PASS: ${queue_password}
```

**Supported Pattern B (Opaque Connection String)**:
```yaml
envVariables:
  NATS_URL: ${queue_connectionString}
```

---

## 4. Manifest Specifications (`import.yaml` & `zerops.yaml`)

### Production `import.yaml` Manifest
```yaml
project:
  name: distributed-app

services:
  # Managed NATS Broker Service (Canonical Hostname: queue)
  - hostname: queue
    type: nats:single@2.12
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
        NATS_HOST: queue
        NATS_PORT: ${queue_port}
        NATS_USER: ${queue_user}
        NATS_PASS: ${queue_password}
        NATS_URL: ${queue_connectionString}
```

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

* **Strict Synchronous Timeouts**: All terminal healthchecks and monitoring queries MUST execute with explicit timeouts:
  ```bash
  timeout 10s curl -s -f http://queue:8222/healthz
  ```
* **Circuit Breaker (2-Attempt Limit)**: On consecutive connection failures or timeouts, halt execution and trigger human escalation.
* **Zero Orphaned Tasks Invariant**: Always terminate lingering background inspection tasks:
  ```typescript
  await manage_task({ Action: 'kill', TaskId: taskId });
  ```
