# Qdrant — Infrastructure & Platform Lifecycle Manual on Zerops

This manual specifies the operational platform model, immutable deployment variants, port architectures, vector database decision criteria, authentication requirements, and bounded execution harnesses for **Qdrant 1.12** on Zerops.

---

## 1. Platform Topology & Deployment Variants

Zerops executes Qdrant inside unprivileged **Incus Linux Containers (LXC)** with dedicated NVMe block storage attached via private encrypted VXLAN networks.

```
+--------------------------------------------------------------------------+
| Qdrant Deployment Variants (Immutable after creation)                     |
+------------------------------------+-------------------------------------+
| Variant A: qdrant:single@1.12      | Variant B: qdrant:ha@1.12           |
| - 1 dedicated Incus LXC node       | - 3 nodes with auto-clustering      |
| - Ports: 6333 (HTTP), 6334 (gRPC)  | - Ports: 6333 (HTTP), 6334 (gRPC)   |
| - Automatic NVMe disk expansion    | - automaticClusterReplication=true  |
| - Ideal for standard RAG & search  | - Ideal for enterprise HA workloads |
+------------------------------------+-------------------------------------+
```

> **Automatic Vertical Autoscaling Invariant**:
> Do not author manual `verticalAutoscaling` min/max blocks. Zerops natively monitors CPU and memory usage and auto-scales vertically on demand with sub-second responsiveness.

---

## 2. Vector DB Selection: Qdrant vs PostgreSQL 18 `pgvector`

| Technical Dimension | Qdrant Dedicated Vector DB (`type: qdrant:single@1.12`) | PostgreSQL 18 + `pgvector` (`type: postgresql:single@18`) |
|---|---|---|
| **Core Architecture** | **100% Rust-native Vector Search Engine** | Relational ACID database with vector extension |
| **Throughput (1M vectors)**| **~4,200 QPS (p99 18ms)** | ~850 QPS (p99 89ms) |
| **High-Speed Protocol** | **Native binary gRPC (Port 6334)** | PostgreSQL wire protocol (Port 5432) |
| **Hybrid Search** | **Native Dense + Sparse (SPLADE) + Server RRF** | Complex SQL combining Full-Text search and `<=>` |
| **Multi-Tenancy** | Payload pre-filtering for 10M+ tenants | Partitioned tables or `WHERE tenant_id = ...` |
| **Quantization** | Scalar int8 and binary quantization | `halfvec` (float16) and `bit` (binary quantization) |
| **Recommended Choice** | **Large-scale RAG, embeddings >500k, gRPC microservices** | **Transactional business entities sharing ACID guarantees** |

---

## 3. Four-Way Architectural Comparison

| Dimensión Técnica | Managed Qdrant `:single` en Zerops | Managed Qdrant `:ha` en Zerops | Self-Hosted Qdrant en Generic Ubuntu LXC | Cliente en `os: alpine` vs `os: ubuntu` |
|---|---|---|---|---|
| **Aprovisionamiento** | **1 línea en `import.yaml` (`type: qdrant:single@1.12`)** | **1 línea en `import.yaml` (`type: qdrant:ha@1.12`)** | Manual vía binario/apt | `os: alpine` (pure JS/TS/Go/Rust) / `ubuntu` (Python ML) |
| **Topología** | 1 contenedor Incus LXC con NVMe dedicado | 3 nodos distribuidos con auto-clustering | 1 contenedor genérico | N/A (conexión por red privada VXLAN) |
| **Puertos de Acceso** | 6333 (REST/UI) + 6334 (gRPC) | 6333 (REST/UI) + 6334 (gRPC) | Solo los configurados a mano | Conexión interna directa a 6333 / 6334 |
| **Autenticación** | `${qdrant_apiKey}` (Full) + `${qdrant_readOnlyApiKey}` | `${qdrant_apiKey}` + `${qdrant_readOnlyApiKey}` | Manual | Cabecera `api-key` requerida |
| **Backups Gestionados** | Automáticos cifrados diarios | Automáticos cifrados diarios | Manual | N/A |
| **Autoescalado Vertical** | **Elástico Automático Nativo (`min < max`)** | **Elástico Automático Nativo (`min < max`)** | Manual | Dinámico |
| **Casos de Uso** | RAG semántico, búsqueda híbrida de productos | Sistemas corporativos RAG de alta disponibilidad | Necesidad de plugins no soportados | Alpine para TypeScript/Go / Ubuntu para Python |

---

## 4. Port Architecture & Mandatory Authentication

### Port Specifications
* **Port 6333 (HTTP REST / UI)**: REST API and built-in Qdrant Web Dashboard (`http://qdrant:6333/dashboard`).
* **Port 6334 (gRPC Protocol)**: High-speed binary protocol for high-throughput batch vector indexing and querying.

### Mandatory Authentication Rules
Qdrant in Zerops strictly enforces API Key authentication on all requests:
* Pass `${qdrant_apiKey}` in the `api-key` HTTP header (or via the client SDK's `apiKey` option).
* Use `${qdrant_readOnlyApiKey}` for read-only query surfaces exposed to public frontend clients.

---

## 5. Storage Growth Law & Backups

* **Dynamic NVMe Storage Expansion**: Zerops automatically scales the underlying NVMe storage as collections grow.
* **Storage Non-Shrink Law**: Once allocated, vector disk storage **never shrinks**.
* **Automated Platform Backups**: Daily encrypted backups (00:00–01:00 UTC) are enabled out-of-the-box.

---

## 6. Manifest Specifications (`import.yaml` & `zerops.yaml`)

### Production `import.yaml` Manifest
```yaml
project:
  name: rag-app

services:
  # Managed Qdrant Vector Search Service (Canonical Hostname: qdrant)
  - hostname: qdrant
    type: qdrant:single@1.12
    priority: 10

  # Application Runtime (Node.js/Bun/Python)
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
        QDRANT_HOST: qdrant
        QDRANT_PORT: ${qdrant_port}
        QDRANT_GRPC: ${qdrant_grpcPort}
        QDRANT_API_KEY: ${qdrant_apiKey}
        QDRANT_READ_ONLY_KEY: ${qdrant_readOnlyApiKey}
```

---

## 7. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

* **Strict Synchronous Timeouts**: All healthchecks and vector diagnostics MUST execute with explicit timeouts:
  ```bash
  timeout 10s curl -s -f -H "api-key: $QDRANT_API_KEY" http://qdrant:6333/healthz
  ```
* **Circuit Breaker (2-Attempt Limit)**: On consecutive connection failures or timeouts, halt execution and trigger human escalation.
* **Zero Orphaned Tasks Invariant**: Always terminate lingering background inspection tasks:
  ```typescript
  await manage_task({ Action: 'kill', TaskId: taskId });
  ```
