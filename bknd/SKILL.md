---
name: bknd
description: "Trigger: bknd, backend, api stack, nats rpc, directus 12, postgresql 18, valkey 7, erpnext, devllm-telemetry, whatsapp-engine, payment-gateways, orders-fulfillment, ghcicd, local-storage, zcp, sales-enablement. Master Backend, Sovereign Data, RPC & Agentic Mesh Orchestrator in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.1"
---

# `bknd` — Master Backend, Sovereign Data & RPC Orchestrator (v3.1)

## Activation Contract
Activate when designing, architecting, building, or maintaining backend microservices, database schemas (PostgreSQL 18, `pgvector`), event-driven pipelines, NATS Request-Reply RPC, Directus 11/12+ BaaS, Frappe Cloud ERPNext connectors, shared storage backups, multi-carrier order fulfillment, or CI/CD delivery in Zerops.

## Hard Rules & Positive Guidance
- **Pre-Flight Epistemic Gate (MANDATORY)**: BEFORE authoring backend code, proposing architectural migrations, or modifying database schemas, the agent MUST evaluate the user request against the Active Sub-Skills Dispatch Table below. The agent MUST open and READ the matching sub-skill `SKILL.md` via its canonical `file:///` URI. Proceeding without inspecting the required sub-skills violates the architectural contract.
- **Brand SSoT Ingestion**: Ingest client business logic and brand guidelines directly from the local single-tenant path `/brand/fase0_system_prompt.md` and `/brand/brandbook.json`. Heavy binary media resides in S3 Object Storage (`storage`).
- **Strict Credential Protection**: Connection strings (`$db_connectionString`, `$cache_connectionString`, `$nats_url`) MUST ALWAYS be referenced as environment variable names. Never hardcode plaintext credentials.
- **Container Execution Boundary**: Runtime commands (build, test, framework execution, database migrations) MUST run inside containers via SSH (`ssh {hostname} "cd /var/www && <cmd>"`). Code editing happens on the host mount `/var/www/{hostname}/`.
- **Zero Deletion Invariant**: Preserve all existing database columns, Directus collections, and ERPNext DocTypes without destructive drop migrations. Consult [`references/usage.md`](file:///var/www/.agents/skills/bknd/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/bknd/references/infra.md) for full lossless APIs.
- **Dynamic Storage Mounting**: Mount Local Storage volumes via `run.volume: {hostname: <storageHostname>, mountPath: /mnt/<storageHostname>}` in `zerops.yaml`.
- **Fractal CoHaLo Execution**: Enforce hygiene (`timeout 10s`), wait limits (`WaitMsBeforeAsync: 10000`), zero orphan tasks (`manage_task action="kill"`), and physical sensors (NATS `:8222`, Valkey PING, PostgreSQL connection probes).

## Active Sub-Skills Dispatch Table

| Domain / Capability | Sub-Skill | Canonical SSoT Pointer | Role & Boundary |
|---|---|---|---|
| **Zerops LXC Platform** | `zcp` | [`zcp`](file:///var/www/.agents/skills/zcp/SKILL.md) | 22 MCP platform tools, `zerops.yaml` lifecycles, env variables & logs |
| **Persistent Storage** | `local-storage` | [`local-storage`](file:///var/www/.agents/skills/local-storage/SKILL.md) | POSIX persistent storage volumes (`run.volume: local-storage:single@1`) |
| **Relational BaaS** | `directus` | [`directus`](file:///var/www/.agents/skills/directus/SKILL.md) | Relational schema, CRM, PIM collections & REST/GraphQL BaaS |
| **RPC & Event Broker** | `nats` | [`nats`](file:///var/www/.agents/skills/nats/SKILL.md) | JetStream event broker (`events.*`) & ultra-low latency Request-Reply RPC (<0.3ms) |
| **Database & Vector RAG** | `postgresql` | [`postgresql`](file:///var/www/.agents/skills/postgresql/SKILL.md) | PostgreSQL 18 with `pgvector` HNSW vector embeddings & ACID relational stores |
| **Cache, Locks & Queues** | `valkey` | [`valkey`](file:///var/www/.agents/skills/valkey/SKILL.md) | High-throughput cache, BullMQ job queues & distributed concurrency locks |
| **Payment Gateways & Webhooks** | `payment-gateways` | [`payment-gateways`](file:///var/www/.agents/skills/payment-gateways/SKILL.md) | Server-to-Server webhooks, Wompi SHA-256 integrity, Stripe HMAC, Valkey idempotency locks |
| **Automation Engine** | `automation-engine` | [`automation-engine`](file:///var/www/.agents/skills/automation-engine/SKILL.md) | Asynchronous event-driven orchestrator, webhooks & worker pipelines |
| **ERP & Tax Invoicing** | `erpnext` | [`erpnext`](file:///var/www/.agents/skills/erpnext/SKILL.md) | Frappe Cloud REST client, `Sales Invoice`, `Delivery Note` & DIAN compliance |
| **Multicarrier Logistics** | `orders-fulfillment` | [`orders-fulfillment`](file:///var/www/.agents/skills/orders-fulfillment/SKILL.md) | Multi-carrier courier routing (Coordinadora, Servientrega), DANE Divipola & thermal labels |
| **Omnichannel Messaging** | `whatsapp-engine` | [`whatsapp-engine`](file:///var/www/.agents/skills/whatsapp-engine/SKILL.md) | Omnichannel messaging decoupling EvolutionGo with NATS and Bifrost gateway |
| **Enterprise AI Gateway** | `bifrost` | [`bifrost`](file:///var/www/.agents/skills/bifrost/SKILL.md) | Universal LLM proxy, sub-100us routing & drop-in OpenAI completions |
| **Executive Co-Pilot Bridge** | `hermes-agent` | [`hermes-agent`](file:///var/www/.agents/skills/hermes-agent/SKILL.md) | Telegram store-owner bot, Nous tool calling, NATS bridge & Directus/ERPNext control |
| **Continuous Delivery** | `ghcicd` | [`ghcicd`](file:///var/www/.agents/skills/ghcicd/SKILL.md) | 3-environment GitOps CI/CD delivery (`dev` -> `stage` -> `prod`) with GitHub Actions |
| **Telemetry & Metrics** | `devllm-telemetry` | [`devllm-telemetry`](file:///var/www/.agents/skills/devllm-telemetry/SKILL.md) | NATS telemetry, Valkey memory health & worker pipeline observability |
| **Sales Enablement AI** | `sales-enablement` | [`sales-enablement`](file:///var/www/.agents/skills/sales-enablement/SKILL.md) | BANT/CHAMP lead qualification engine and human advisor handoff protocols |

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 4D Matrix & RPC Protocols | NATS Request-Reply RPC (<0.3ms P99) vs HTTP, gRPC | [`references/usage.md#1-4d-comparative-architectural-matrix-backend-communication-protocols`](file:///var/www/.agents/skills/bknd/references/usage.md) |
| Sub-Skills Inventory | Direct pointers to Directus, NATS, FastAPI, Postgres | [`references/usage.md#2-sub-skills-inventory--direct-file-pointers`](file:///var/www/.agents/skills/bknd/references/usage.md) |
| Astro Actions + NATS RPC | Typed server actions with Zod and NATS request-reply | [`references/usage.md#3-typescript-contract-astro-actions--nats-rpc--directus-sdk`](file:///var/www/.agents/skills/bknd/references/usage.md) |
| FastAPI + pgvector | Python Granian microservice with pgvector HNSW search | [`references/usage.md#4-python-contract-fastapi-microservice--nats-rpc--pgvector`](file:///var/www/.agents/skills/bknd/references/usage.md) |
| Frappe Cloud REST Client | ERPNext sales invoice and inventory sync ($0 SaaS) | [`references/usage.md#5-frappe-cloud--erpnext-rest-client-0-saas-cost`](file:///var/www/.agents/skills/bknd/references/usage.md) |
| Automated pg_dump Backup | Database backups to SeaweedFS FUSE shared storage | [`references/usage.md#6-automated-pg_dump-backups-to-shared-storage`](file:///var/www/.agents/skills/bknd/references/usage.md) |
| Multi-Service Topology | Mesh architecture for Directus, FastAPI, Valkey, NATS | [`references/infra.md#1-multi-service-backend-mesh-topology-in-zerops`](file:///var/www/.agents/skills/bknd/references/infra.md) |
| Managed DB Profiles | Sizing profiles for PostgreSQL 18, Valkey 7.2 & NATS | [`references/infra.md#2-managed-database-sizing--immutability-rules`](file:///var/www/.agents/skills/bknd/references/infra.md) |
| Production Recipes JSON | NATS RPC handlers, Frappe client, backup scripts | [`assets/bknd_production_recipes.json`](file:///var/www/.agents/skills/bknd/assets/bknd_production_recipes.json) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/bknd-validate.sh`](file:///var/www/.agents/skills/bknd/scripts/bknd-validate.sh) |

## Execution Steps
1. Discover backend services and verify connection variables in Zerops environment.
2. Initialize database schemas and register `pgvector` codecs.
3. Configure NATS Request-Reply RPC handlers and JetStream streams.
4. Establish asynchronous BullMQ queues on Valkey for ERP and email sync.
5. Verify health of NATS, Valkey, and Postgres via physical sensors.

## Output Contract
- High-concurrency, resilient backend mesh running in Zerops Incus LXC.
- Sub-millisecond NATS RPC, automated pg_dump backups, and passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/bknd/references/usage.md) — 4D matrix, sub-skills inventory, TypeScript/Python contracts, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/bknd/references/infra.md) — Multi-service mesh topology, DB profiles, FUSE storage, and CoHaLo harness.
- [`assets/bknd_production_recipes.json`](file:///var/www/.agents/skills/bknd/assets/bknd_production_recipes.json) — Production RPC handlers and backup recipes.
- [`scripts/bknd-validate.sh`](file:///var/www/.agents/skills/bknd/scripts/bknd-validate.sh) — Deterministic quality & token validation sensor.
