---
name: bknd
description: "Trigger: bknd, backend architecture, decoupled lego backend, backend stack, backend mesh, rpc architecture, zerops backend. Master Backend, Sovereign Data, RPC & Agentic Mesh Orchestrator in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.2"
---

# `bknd` — Master Backend, Sovereign Data & RPC Orchestrator (v3.2)

## Activation Contract
Activate when designing, architecting, building, or orchestrating backend microservices, event-driven pipelines, NATS Request-Reply RPC, Directus BaaS, database topologies, or multi-service mesh in Zerops. Atomic tasks on a single runtime execute directly with domain skills.

## Hard Rules & Positive Guidance
- **Pre-Flight Epistemic Gate**: Evaluate backend requests against the domain sub-skills table. Inspect the matching sub-skill `SKILL.md` before coding.
- **Brand SSoT Ingestion**: Ingest client business logic and brand tokens from `/brand/fase0_system_prompt.md` and `/brand/brandbook.json`. Store binary assets in S3 Object Storage (`storage`).
- **Strict Credential Protection**: Reference connection strings exclusively via environment variable names (`$db_connectionString`, `$cache_connectionString`, `$nats_url`). Zero plaintext secrets.
- **Container Execution Boundary**: Execute runtime commands inside containers via SSH (`ssh {hostname} "cd /var/www && <cmd>"`). Edit code on host mounts `/var/www/{hostname}/`.
- **Zero Deletion Invariant**: Preserve database columns, Directus collections, and DocTypes without destructive drop migrations. Consult [`references/usage.md`](file:///var/www/.agents/skills/bknd/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/bknd/references/infra.md) for full lossless patterns.
- **Decoupled Lego Mesh**: Route inter-service traffic via Zerops internal DNS (`http://<service>:<port>`). Mount Local Storage persistent volumes via `run.volume` in `zerops.yaml`.
- **Fractal CoHaLo Bounded Execution**: Run synchronous commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks. Verify health via physical sensors (NATS `:8222`, Valkey PING, PostgreSQL connection probes).

## Active Sub-Skills Dispatch Table

| Capability | Sub-Skill | Role & Boundary |
|---|---|---|
| **LXC Platform** | `zcp` ([`SKILL.md`](file:///var/www/.agents/skills/zcp/SKILL.md)) | Platform lifecycle, env vars, scale & logs |
| **Persistent Storage** | `local-storage` ([`SKILL.md`](file:///var/www/.agents/skills/local-storage/SKILL.md)) | POSIX persistent disk volumes (`run.volume`) |
| **RPC & Event Broker** | `nats` ([`SKILL.md`](file:///var/www/.agents/skills/nats/SKILL.md)) | JetStream events & Request-Reply RPC (<0.3ms) |
| **Database & Vector** | `postgresql` ([`SKILL.md`](file:///var/www/.agents/skills/postgresql/SKILL.md)) | PostgreSQL 18 with `pgvector` HNSW |
| **Cache & Queues** | `valkey` ([`SKILL.md`](file:///var/www/.agents/skills/valkey/SKILL.md)) | Valkey 7.2, BullMQ queues & concurrency locks |
| **Gateways & Logistics**| `payment-gateways` ([`SKILL.md`](file:///var/www/.agents/skills/payment-gateways/SKILL.md)) | Multi-gateway webhooks & order fulfillment |

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Communication Protocols | NATS Request-Reply RPC vs HTTP/gRPC | [`references/usage.md#1-4d-comparative-architectural-matrix`](file:///var/www/.agents/skills/bknd/references/usage.md) |
| Sub-Skills Inventory | Direct pointers to Directus, NATS, Postgres | [`references/usage.md#2-sub-skills-inventory`](file:///var/www/.agents/skills/bknd/references/usage.md) |
| Multi-Service Topology | Mesh architecture in Zerops Incus LXC | [`references/infra.md#1-multi-service-backend-mesh`](file:///var/www/.agents/skills/bknd/references/infra.md) |
| Database Profiles | Sizing profiles for PostgreSQL, Valkey, NATS | [`references/infra.md#2-managed-database-sizing`](file:///var/www/.agents/skills/bknd/references/infra.md) |

## Output Contract
- High-concurrency, resilient backend mesh running in Zerops Incus LXC.
- Sub-millisecond NATS RPC, automated backups, and passing physical sensors (`skills-suite-validate`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/bknd/references/usage.md) — Architectural matrix, TypeScript/Python contracts, and production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/bknd/references/infra.md) — Multi-service mesh topology, database sizing, FUSE storage, and harness.
