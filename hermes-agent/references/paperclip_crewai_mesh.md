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
  {"type": "tool.call", "tool": "execute_query", "arguments": {"query": "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"}}
  ```
- **Tool Result (`tool.result`)**:
  ```json
  {"type": "tool.result", "tool": "execute_query", "status": "success", "output": "mentorships, bookings, clients"}
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

## 5. Dynamic Domain Agnosticism & Database Introspection

To prevent agentic hallucination, hardcoding of legacy project remnants (e.g. past e-commerce catalogs or specific brands), or rigid anti-commerce prohibitions, Hermes enforces **Dynamic Domain Introspection**:
1. **Zero Hardcoded Catalogs**: Hermes must never assume fixed products, services, or pricing models out-of-the-box.
2. **PostgreSQL 18 Live Introspection**: When asked about products, stock, bookings, or client sessions (e.g. Bioenka agroecology, Juan Damaren 1:1 mentorships, or consulting), Hermes queries `information_schema.tables` and live application tables via `execute_query`.
3. **Factual Adaptation**:
   - If tables exist (`mentorships`, `bookings`, `products`, `orders`), Hermes queries and mutates them factually.
   - If tables do not exist, Hermes accurately reports the live database state and offers to generate the schema DDL or coordinate with PiDev (`gentle-pi` in `/var/www/webdev`) for UI forms.

---

## 6. CrewAI 1.15.30+ and PydanticAI `output_pydantic` Bridge

Dynamic swarms orchestrated via `run_crew_ai` natively bridge CrewAI with Pydantic:
1. **Dynamic Schema Compilation**: If `output_schema` is supplied (e.g. `{"decision": "str", "score": "int", "items": "list[str]"}`), `pydantic.create_model` compiles a dynamic `BaseModel` schema.
2. **Strict Output Enforcement**: The generated schema is assigned to the terminal `Task(output_pydantic=DynamicModel)`.
3. **Typed Result Extraction**: `crew.kickoff()` produces structured JSON via `output.pydantic.model_dump_json()`, guaranteeing 100% type safety and eliminating markdown hallucination.

---

## 7. Bifrost Governance SSoT Invariant

When Bifrost runs with `config_store.enabled: true` backed by PostgreSQL (`config_store.type: "postgres"`):
1. **Database Is Exclusive Authority**: Bifrost reads, writes, and validates Virtual Keys strictly against the PostgreSQL table `governance_virtual_keys`.
2. **Static Config Ignored**: Keys in `config.json` are not dynamically watched or re-read after initial bootstrap.
3. **Key Sync Mandate**: Any provisioned or updated Virtual Key (`vk-production-main`, `vk-hermes-agent`, `vk-crewai`, `vk-pidev`, `vk-pydanticai`) must be upserted directly into PostgreSQL via `/api/governance/virtual-keys` or SQL `INSERT INTO governance_virtual_keys ... ON CONFLICT (name) DO UPDATE`.
