---
name: automation-engine
description: "Trigger: automation-engine, nats jetstream, bullmq valkey, event driven architecture, cloudevents, dead letter queue, circuit breaker, background workers. Sovereign Event-Driven Orchestration, BullMQ Workers & NATS JetStream Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `automation-engine` — Universal Event-Driven Orchestration & Queuing (v2.0)

## Activation Contract
Activate when designing, building, or operating asynchronous pipelines, message queues (**BullMQ on Valkey 7.2**), domain event streaming (**NATS JetStream 2.12**), CNCF CloudEvents v1.0 envelopes, background worker pools, or Dead Letter Queues (DLQ) in Zerops.

## Hard Rules & Positive Guidance
- **Two-Tier Asynchronous Decoupling**: HTTP handlers and webhooks MUST acknowledge requests immediately (<100ms) with an event receipt. Heavy tasks (data sync, document generation, external API calls) MUST be dispatched to BullMQ queues or published to NATS JetStream.
- **At-Least-Once Delivery & Idempotency**: Workers consuming from NATS or BullMQ MUST acquire distributed locks in Valkey (`SET lock:job:${id} 1 NX EX 3600`) with unique owner tokens before mutation to prevent duplicate processing.
- **Dead Letter Queue (DLQ) & Circuit Breaker**: Transient failures MUST retry with exponential backoff and jitter. Unrecoverable failures route to DLQ streams (`events.dlq.>`), while failing downstreams trip a Tri-State Circuit Breaker (`CLOSED`, `OPEN`, `HALF_OPEN`).
- **Sub-Millisecond RPC**: Synchronous inter-service RPC MUST use Core NATS Request-Reply (`nc.request()`) maintaining P99 latencies < 0.3ms.
- **CNCF CloudEvents v1.0 Standard**: All cross-service events MUST conform to the CloudEvents v1.0 specification with W3C distributed tracing context (`traceparent`).
- **Hygiene & Sensors**: Strict timeouts (`timeout 10s`), wait limits (`WaitMsBeforeAsync: 10000`), zero orphan tasks, and sensor verification. Consult [`references/usage.md`](file:///var/www/.agents/skills/automation-engine/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/automation-engine/references/infra.md).

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Stream & RPC Architecture | NATS 2.12 JetStream pull consumers, Core RPC, and KV Store | [`references/usage.md#1-nats`](file:///var/www/.agents/skills/automation-engine/references/usage.md) |
| BullMQ Worker Queues | BullMQ on Valkey 7.2 with deduplication and DLQ routing | [`references/usage.md#2-bullmq`](file:///var/www/.agents/skills/automation-engine/references/usage.md) |
| CloudEvents v1.0 Schema | Standardized event schema with Zod validation | [`assets/automation_zod_schemas.ts`](file:///var/www/.agents/skills/automation-engine/assets/automation_zod_schemas.ts) |
| Circuit Breaker | Standalone Tri-State Circuit Breaker with exponential backoff | [`assets/circuit_breaker.ts`](file:///var/www/.agents/skills/automation-engine/assets/circuit_breaker.ts) |
| Cluster & Memory Config | NATS 2.12 clustering and Valkey memory tuning (`noeviction`) | [`references/infra.md#1-infra`](file:///var/www/.agents/skills/automation-engine/references/infra.md) |
| Production Recipes | Declarative streams, consumers, and worker definitions | [`assets/automation_engine_recipes.json`](file:///var/www/.agents/skills/automation-engine/assets/automation_engine_recipes.json) |
| Physical Sensor | Deterministic validator checking syntax, words, and schemas | [`scripts/automation-engine-validate.sh`](file:///var/www/.agents/skills/automation-engine/scripts/automation-engine-validate.sh) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/automation-engine/references/usage.md) — SOTA NATS JetStream, Core RPC, and BullMQ worker implementation guide.
- [`references/infra.md`](file:///var/www/.agents/skills/automation-engine/references/infra.md) — NATS 2.12 topology, Valkey memory tuning, and Zerops network routing.
- [`assets/automation_zod_schemas.ts`](file:///var/www/.agents/skills/automation-engine/assets/automation_zod_schemas.ts) — CNCF CloudEvents v1.0 and BullMQ schemas.
- [`assets/circuit_breaker.ts`](file:///var/www/.agents/skills/automation-engine/assets/circuit_breaker.ts) — Standalone Tri-State Circuit Breaker implementation.
- [`assets/nats_jetstream_client.ts`](file:///var/www/.agents/skills/automation-engine/assets/nats_jetstream_client.ts) — Agnostic connection singleton and publisher.
- [`assets/bullmq_worker.ts`](file:///var/www/.agents/skills/automation-engine/assets/bullmq_worker.ts) — Production BullMQ worker wrapper.
- [`assets/automation_engine_recipes.json`](file:///var/www/.agents/skills/automation-engine/assets/automation_engine_recipes.json) — Production stream declarations and recipes.
- [`scripts/automation-engine-validate.sh`](file:///var/www/.agents/skills/automation-engine/scripts/automation-engine-validate.sh) — Deterministic validation sensor.
