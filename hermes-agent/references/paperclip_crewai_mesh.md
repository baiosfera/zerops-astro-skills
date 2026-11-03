# Tri-Pillar Multi-Agent Mesh Specification (Hermes + Paperclip + CrewAI/PydanticAI)

Authoritative specification for the sovereign, frugal, and persistent multi-agent architecture in Zerops Astrobranding.

---

## 1. Architectural Model & Responsibilities

The mesh decouples responsibilities across three autonomous tiers:

1. **Pillar 1: Hermes Copilot (Chief of Staff & Execution Gateway)**
   - **Runtime**: Ubuntu Python 3.12 (`hermes`).
   - **Primary Surface**: Telegram Bot with auto-recovery watchdog and Paperclip HTTP Gateway v1 (`ThreadingHTTPServer` on port 8000).
   - **Capabilities**: Universal tool dispatch (`TOOL_DISPATCH`), dynamic ephemeral worker discovery (`list_zerops_services`), and bidirectional communication.

2. **Pillar 2: Paperclip OS (Governance, Spend Caps & Org Chart)**
   - **Runtime**: Ubuntu Node.js 26 (`paperclip` / `agentdev` on port 3100).
   - **Responsibilities**: Budget allocation, spend caps watchdog, issue queues, agent hiring, and organizational delegation.
   - **Persistence SSoT**: Managed PostgreSQL 18 cluster + POSIX LocalStorage NVMe volume (`/mnt/localstorage/paperclip`).

3. **Pillar 3: Dual-Engine Swarm Mesh**
   - **PydanticAI Micro-Agents (<35MB RAM, <100ms)**: Sub-second deterministic schema parsing, classification, and parameter extraction (`extract_structured_data`).
   - **CrewAI Macro-Swarms (1.15.30+)**: Collaborative multi-agent teams for deep research, SEO/AEO/GEO audits, and complex reasoning pipelines (`run_crew_ai`).
   - **Ephemeral Video Workers (`videoworker`)**: On-demand Chromium/Playwright and FFmpeg rendering spun up via Recipe 08 and torn down when idle.

---

## 2. Paperclip HTTP Gateway v1 Protocol

Hermes implements the official Paperclip agent integration API:

### 2.1 Route Definitions

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| `POST` | `/v1/runs` | Submits a task execution run | `202 Accepted` |
| `GET` | `/v1/runs/:id` | Polls current run status and metrics | `200 OK` |
| `GET` | `/v1/runs/:id/events` | SSE real-time event stream | `200 OK` (`text/event-stream`) |
| `GET` | `/health` | Health check probe | `200 OK` |

### 2.2 Event Payloads (SSE Format)

Every event is formatted as `event: <type>\ndata: <json>\n\n`:

- **Run Started (`run.started`)**:
  ```json
  {"type": "run.started", "run_id": "run_1730598000_a1b2", "task": "Auditar inventario"}
  ```
- **Tool Invocation (`tool.call`)**:
  ```json
  {"type": "tool.call", "tool": "get_store_products", "arguments": {"category": "activewear"}}
  ```
- **Tool Result (`tool.result`)**:
  ```json
  {"type": "tool.result", "tool": "get_store_products", "status": "success", "output": "..."}
  ```
- **Token Delta (`token.delta`)**:
  ```json
  {"type": "token.delta", "content": "Se encontraron 12 productos activos."}
  ```
- **Run Completed (`run.completed`)**:
  ```json
  {
    "type": "run.completed",
    "result": "Auditoría completada exitosamente.",
    "usage": {
      "prompt_tokens": 1240,
      "completion_tokens": 380,
      "total_tokens": 1620,
      "cost_cents": 0
    }
  }
  ```

---

## 3. Indestructible SSoT Persistence Contract

Paperclip AI must be operated with managed infrastructure to guarantee zero data loss:

1. **Managed PostgreSQL 18**:
   - `DATABASE_URL: ${database_connectionString}`.
   - Automatically bypasses `@embedded-postgres`, saving ~400 MB of container RAM and preventing swap starvation.
   - All migrations, company entities, tasks, and issues persist in the relational lakehouse.

2. **POSIX LocalStorage NVMe Volume**:
   - Volume `localstorage` mounted at `/mnt/localstorage` in `zerops.yaml`.
   - Dedicated paths:
     * `PAPERCLIP_HOME: "/mnt/localstorage/paperclip"`
     * `PAPERCLIP_STORAGE_PROVIDER: "local_disk"`
     * `PAPERCLIP_STORAGE_LOCAL_DIR: "/mnt/localstorage/paperclip/storage"`
     * `PAPERCLIP_SECRETS_MASTER_KEY_FILE: "/mnt/localstorage/paperclip/secrets/master.key"`
   - Daily automated `.tar.gz` snapshots provided by Zerops platform.
   - Container redeployments (`zerops_deploy`) do not touch `/mnt/localstorage`.

---

## 4. Spend Caps & Frugal Zero-Leak Policy

To prevent runaway API costs, the mesh enforces:

1. **Inference Hierarchy**:
   - Priority 0: Explicit pro overrides (`x-force-deepseek: true`) routed to DeepSeek V3.
   - Priority 1: FreeLLMAPI ($0 default across 34+ providers) with automated failover.
2. **Paperclip Budget Policies**:
   - Every agent is bound to a strict spend limit (e.g. $10/month or $0.50/run).
   - If a run attempts to exceed its allocated budget, Hermes marks the run failed with `BUDGET_EXCEEDED` and returns an incident event to Paperclip.
