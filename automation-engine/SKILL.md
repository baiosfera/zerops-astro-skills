---
name: automation-engine
description: "Trigger: automation-engine, nats jetstream, directus flows, bullmq valkey, event driven architecture, cloudevents, dead letter queue, post payment pipeline. Sovereign Event-Driven Orchestration, BullMQ Workers & NATS JetStream Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `automation-engine` — Sovereign Event-Driven Orchestration & Queuing (v2.0)

## Activation Contract
Activate when designing, building, or operating asynchronous background pipelines, message queues (**BullMQ on Valkey 7.2**), domain event streaming (**NATS JetStream 2.12**), automated post-payment settlement workflows, scheduled cron routines, or Dead Letter Queues (DLQ) in Zerops.

## Hard Rules & Positive Guidance
- **Two-Tier Asynchronous Decoupling**: Endpoints handling payments or webhooks MUST respond immediately (<200ms) after locking and updating local order state in Directus. Heavy tasks (ERP posting, PDF generation, email/WhatsApp delivery) MUST be enqueued to BullMQ or published to NATS JetStream.
- **At-Least-Once Delivery & Idempotency**: Every worker consuming from NATS or BullMQ MUST check transaction status in Valkey (`SET lock:worker:${jobId} 1 EX 60 NX`) before executing external mutations to prevent double delivery.
- **Dead Letter Queue (DLQ) & Exponential Backoff**: Transient failures in external APIs (Frappe Cloud, email gateways) MUST retry 3 times with exponential backoff before routing to a DLQ stream for operator inspection.
- **Sub-Millisecond RPC**: Synchronous microservice communication MUST use Core NATS Request-Reply (`nc.request()`) maintaining P99 latencies < 0.3ms.
- **Zero SaaS Bloat**: Operates with <250 MB RAM total footprint across Valkey and NATS, avoiding costly third-party webhook relays.
- **Fractal CoHaLo Execution**: Enforce command timeouts (`timeout 10s`), wait limits (`WaitMsBeforeAsync: 10000`), zero orphan tasks, and sensor verification.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Stream & Flow Architecture | NATS JetStream setup, Directus webhook flows, and core usage | [`references/usage.md`](file:///var/www/.agents/skills/automation-engine/references/usage.md) |
| BullMQ Worker Queues | Canonical BullMQ queue configuration on Valkey with retries | [`references/bullmq_valkey.md`](file:///var/www/.agents/skills/automation-engine/references/bullmq_valkey.md) |
| NATS Event Hierarchy | Domain event subjects, schemas, and stream declarations | [`references/nats_jetstream.md`](file:///var/www/.agents/skills/automation-engine/references/nats_jetstream.md) |
| Scheduled Crons | Periodic cart reservation cleanup and gateway watchdogs | [`references/scheduled_crons.md`](file:///var/www/.agents/skills/automation-engine/references/scheduled_crons.md) |
| Environment & Cluster Config | NATS 2.12 topology, Valkey memory tuning, and network routing | [`references/infra.md`](file:///var/www/.agents/skills/automation-engine/references/infra.md) |
| Production Recipes JSON | Post-payment worker and JetStream stream declarations | [`assets/automation_engine_recipes.json`](file:///var/www/.agents/skills/automation-engine/assets/automation_engine_recipes.json) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/automation-engine-validate.sh`](file:///var/www/.agents/skills/automation-engine/scripts/automation-engine-validate.sh) |

## Execution Steps
1. Declare NATS JetStream streams (`ORDERS`, `EVENTS`) using the management client.
2. Initialize BullMQ queues on Valkey (`orders:post-settlement`).
3. Deploy worker handling ERPNext posting, email generation, and WhatsApp dispatch.
4. Configure scheduled cron tasks for stock reservation sweeps.
5. Verify health via physical sensor (`scripts/automation-engine-validate.sh`).

## Output Contract
- High-throughput asynchronous event fabric with zero HTTP request blocking.
- Resilient background task execution with automatic retries and passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/automation-engine/references/usage.md) — JetStream consumer setup, Directus Flows, and BullMQ bridges.
- [`references/infra.md`](file:///var/www/.agents/skills/automation-engine/references/infra.md) — NATS Server cluster configuration and Valkey memory tuning.
- [`references/bullmq_valkey.md`](file:///var/www/.agents/skills/automation-engine/references/bullmq_valkey.md) — BullMQ on Valkey configuration and worker examples.
- [`references/nats_jetstream.md`](file:///var/www/.agents/skills/automation-engine/references/nats_jetstream.md) — NATS JetStream domain event streaming specifications.
- [`references/scheduled_crons.md`](file:///var/www/.agents/skills/automation-engine/references/scheduled_crons.md) — Scheduled cron tasks and maintenance routines.
- [`assets/automation_engine_recipes.json`](file:///var/www/.agents/skills/automation-engine/assets/automation_engine_recipes.json) — Production worker definitions and stream declarations.
- [`scripts/automation-engine-validate.sh`](file:///var/www/.agents/skills/automation-engine/scripts/automation-engine-validate.sh) — Deterministic quality & token validation sensor.
