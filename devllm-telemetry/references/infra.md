# `devllm-telemetry` Infrastructure, Observability & Zerops Manual (v2.0)

This manual provides production-grade infrastructure blueprints, NATS Server HTTP monitoring configuration (:8222), Valkey memory metrics extraction, database backup validation paths, and the Fractal CoHaLo operational harness for `devllm-telemetry`.

---

## 1. Multi-Service Observability Topology in Zerops

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Enterprise Project Topology                                                                     │
│                                                                                                        │
│   ┌──────────────────────────────┐              ┌──────────────────────────────────────────────────┐   │
│   │ AI Workers & Astro Frontend  │              │ Directus 11+ Unified BaaS (directus)             │   │
│   │ (trackLLMCall non-blocking)  │─────────────▶│ (nodejs@24 / os: ubuntu)                         │   │
│   └──────────────┬───────────────┘              │ - Native Directus Insights Telemetry Panels      │   │
│                  │                              │ - Collections: llm_telemetry_logs, system_health │   │
│                  │ Async Telemetry Stream       └────────────────────────┬─────────────────────────┘   │
│                  ▼                                                       ▲                             │
│   ┌──────────────────────────────┐                                       │ Writes health metrics       │
│   │ NATS Server 2.12 (nats)      │                                       │                             │
│   │ ├─ Port 4222: Core Messaging │              ┌────────────────────────┴─────────────────────────┐   │
│   │ └─ Port 8222: HTTP /varz     │◀─────────────│ System Health Daemon (aiworker / directus)       │   │
│   └──────────────┬───────────────┘              │ (bun@1.3 / nodejs@24)                            │   │
│                  │                              │ - Poller daemon every 60 seconds                 │   │
│                  │ Samples Memory & DLQ         │ - Ingests NATS, Valkey and Backup metrics        │   │
│                  ▼                              └────────────────────────┬─────────────────────────┘   │
│   ┌──────────────────────────────┐                                       │                             │
│   │ Valkey In-Memory Cache (cache│                                       ▼                             │
│   │ - Memory footprint info      │              ┌──────────────────────────────────────────────────┐   │
│   │ - DLQ depth inspection       │              │ Persistent Shared Storage (baiostorage)          │   │
│   └──────────────────────────────┘              │ /mnt/baiostorage/backups/postgresql/*.sql.gz     │   │
│                                                 └──────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. NATS Server HTTP Monitoring Configuration

Ensure NATS Server exposes HTTP monitoring endpoints on port `8222`:

* `http://nats:8222/varz` $\implies$ General server statistics (connections, in_msgs, out_msgs, memory, cpu).
* `http://nats:8222/connz` $\implies$ Connection details and active client IPs.
* `http://nats:8222/jsz` $\implies$ JetStream cluster and stream storage statistics.

---

## 3. Environment Variables Reference Dictionary

| Variable | Scope | Description |
|---|---|---|
| `DIRECTUS_URL` | Directus | Directus internal DNS endpoint (`http://directus:8055`) |
| `DIRECTUS_STATIC_TOKEN` | Directus | Admin token for seeder and telemetry logging |
| `VALKEY_URL` | Valkey | Valkey connection URI (`redis://cache:6379`) |
| `NATS_URL` | NATS | NATS core connection string (`nats://nats:4222`) |

---

## 4. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with `devllm-telemetry` must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All poller probes and API requests must use explicit timeouts (`timeout 10s curl -f http://nats:8222/varz`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all lingering workers using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Directus Telemetry Collection check: `curl -s http://directus:8055/items/system_health_logs?limit=1 | grep -q "sampled_at"` $\implies$ Exit 0.
  * NATS HTTP Health check: `curl -s -o /dev/null -w "%{http_code}" http://nats:8222/varz` $\implies$ Expected: `200`.
* **Circuit Breaker Policy**: If Directus is temporarily restarting or unreachable during telemetry logging, catch the error quietly in background (`setImmediate`) to never interrupt user-facing LLM responses.
