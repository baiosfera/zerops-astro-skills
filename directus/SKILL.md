---
name: directus
description: "Trigger: directus, directus 11, directus bootstrap, directus flows, directus extensions, directus hooks, directus rag, devllm-telemetry, business-insights, google oauth directus, directus valkey, directus nats. Enterprise Directus 11+ Headless CMS, BaaS & Data Engine with RAG, Flows, Valkey, NATS & Astro in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# Directus 11+ — Headless CMS, Unified BaaS & Data Engine (v2.0)

## Activation Contract
Activate when architecting, provisioning, configuring, extending, or deploying Directus 11+ on Zerops, managing PostgreSQL schemas, Valkey cache sync, Google OAuth 2.0, Flows, RAG (`pgvector`), or backend pipelines for **`bknd`**, **`devllm-telemetry`**, **`business-insights`**, **Astro**, and WhatsApp engines ([`whatsapp-engine`](file:///var/www/.agents/skills/whatsapp-engine/SKILL.md)).

## Hard Rules
- **Atomic Bootstrap**: Must run `zsc execOnce ${appVersionId} --retryUntilSuccessful -- npx directus bootstrap` in `run.initCommands`.
- **Ubuntu Baseline**: Must run on `os: ubuntu` (Debian glibc) for native `sharp` (libvips) image processing.
- **Persistent Media**: Uploads map to `/mnt/baiostorage/directus/uploads/` with `chmod -R 777`.
- **Valkey Sync**: Multi-node clusters set `CACHE_STORE="redis"`, `SYNCHRONIZATION_STORE="redis"`, and `MESSENGER_STORE="redis"` to `${cache_connectionString}`.
- **Non-Blocking Telemetry**: `llm_telemetry_logs` and ERP sync use non-blocking async calls or NATS events.
- **Fractal CoHaLo**: Enforce hygiene (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans (`manage_task action="kill"`), sensor (HTTP `200` on `/server/health`).
- **Zero Deletion**: Consult [`references/usage.md`](file:///var/www/.agents/skills/directus/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/directus/references/infra.md) for full lossless APIs.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 4D Matrix & Comparison | Directus 11+ vs Strapi, Supabase, Payload | [`references/usage.md#1-4d-comparative-architectural-matrix`](file:///var/www/.agents/skills/directus/references/usage.md) |
| Schema Migrations | Declarative CLI snapshot, diff, apply on PostgreSQL 18 | [`references/usage.md#2-data-engine--schema-management-on-postgresql-18`](file:///var/www/.agents/skills/directus/references/usage.md) |
| Composable `@directus/sdk` | TypeScript client with REST, GraphQL, Auth & WebSockets | [`references/usage.md#3-composable-directussdk-client-typescript`](file:///var/www/.agents/skills/directus/references/usage.md) |
| LLMOps Telemetry Backend | Directus Insights dashboards & `llm_telemetry_logs` | [`references/usage.md#4-backend-engine-for-devllm-telemetry-zero-ram-llmops-observability`](file:///var/www/.agents/skills/directus/references/usage.md) |
| Business Insights Backend | GMV, AOV, Funnel conversion & ERPNext sync | [`references/usage.md#5-backend-engine-for-business-insights-commercial--financial-analytics`](file:///var/www/.agents/skills/directus/references/usage.md) |
| Astro Actions & NATS Triad | Typed mutations, NATS RPC inventory lock & Directus | [`references/usage.md#6-backend-engine-for-bknd-astro-actions--nats-rpc-triad`](file:///var/www/.agents/skills/directus/references/usage.md) |
| Directus Flows & Automations | Event hooks, webhooks, cron schedules (`0 9 * * 1-5`) | [`references/usage.md#7-directus-flows--automation-engine`](file:///var/www/.agents/skills/directus/references/usage.md) |
| RAG Vector Search (`pgvector`) | Extension Hook auto-embedding & cosine search | [`references/usage.md#8-rag--semantic-vector-search-with-postgresql-pgvector`](file:///var/www/.agents/skills/directus/references/usage.md) |
| Multi-Service `import.yaml` | Node.js 24, Astro, NATS, Valkey & PostgreSQL 18 | [`references/infra.md#2-multi-service-provisioning-blueprint-importyaml`](file:///var/www/.agents/skills/directus/references/infra.md) |
| Google OAuth 2.0 Runbook | Onboarding guide for Google Cloud Console OAuth 2.0 | [`references/infra.md#5-google-cloud-console-oauth-20-runbook`](file:///var/www/.agents/skills/directus/references/infra.md) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/directus-validate.sh`](file:///var/www/.agents/skills/directus/scripts/directus-validate.sh) |

## Execution Steps
1. Provision multi-service stack via Zerops `import.yaml`.
2. Configure `zerops.yaml` with Node.js 24 on `os: ubuntu` with `sharp` support and `zsc execOnce` bootstrap.
3. Wire cache and synchronization to Valkey (`CACHE_REDIS: ${cache_connectionString}`) and database to PostgreSQL 18.
4. Mount persistent storage to `/mnt/baiostorage/directus/uploads` with `chmod -R 777`.
5. Connect Directus Flows for NATS event dispatching and deploy RAG extension hooks for `pgvector`.
6. Verify gateway health via physical sensor probe (`curl -f http://directus:8055/server/health`).

## Output Contract
- Production Directus 11+ instance on Zerops Incus LXC (`os: ubuntu`) with Valkey sync.
- Fully wired backend supporting `bknd`, `devllm-telemetry`, `business-insights`, RAG `pgvector`, and passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/directus/references/usage.md) — 4D matrix, `@directus/sdk`, telemetry, business KPIs, Flows, RAG `pgvector` hooks.
- [`references/infra.md`](file:///var/www/.agents/skills/directus/references/infra.md) — Multi-service topology, `import.yaml`, `zerops.yaml`, Google OAuth 2.0, CoHaLo harness.
- [`assets/directus_production_recipes.json`](file:///var/www/.agents/skills/directus/assets/directus_production_recipes.json) — Production recipes, RAG hook code, telemetry schemas.
- [`assets/import_template.yaml`](file:///var/www/.agents/skills/directus/assets/import_template.yaml) — Production import template for Directus 11+ stack.
- [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/directus/assets/zerops_template.yaml) — Full zerops.yaml template for Directus 11+.
- [`scripts/directus-validate.sh`](file:///var/www/.agents/skills/directus/scripts/directus-validate.sh) — Deterministic quality & token validation sensor.
