---
name: nats
description: "Trigger: nats, nats server, jetstream, nats rpc, nats-py, nats kv store, nats object store, nats queue groups. Architect, deploy, and operate NATS Server 2.12, Core NATS RPC (<0.3ms P99), Queue Groups, and JetStream on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# NATS Server — Zerops Managed Messaging & Streaming Engine (v2.0)

## Activation Contract
Activate whenever architecting, deploying, configuring, or connecting to NATS Server 2.12, Core NATS Pub/Sub, Microservices Request-Reply (RPC) (<0.3ms P99 latency), Queue Groups load balancing, JetStream 2.12 streams & pull consumers, NATS Key-Value (KV) Store, NATS Object Store, or managing Zerops semi-managed services (`type: nats:single@2.12` or `type: nats:ha@2.12`).

## Hard Rules
- **Rule 1 (Request-Reply RPC Timeout)**: All synchronous RPC calls via `nc.request()` MUST specify an explicit timeout (e.g. `timeout: 2000`) to prevent thread starvation during service degradation.
- **Rule 2 (Poison Pill Termination)**: When a message in a JetStream Pull Consumer exceeds its maximum delivery attempts (`max_deliver`), the consumer MUST invoke `msg.term()` to prevent infinite delivery cycles.
- **Rule 3 (Atomic Msg-Id Deduplication)**: All JetStream publishing events MUST supply the `Nats-Msg-Id` header with a unique idempotency key for hardware-level deduplication without database lookups.
- **Rule 4 (Double-Auth Prevention)**: Do NOT hand-compose URLs like `nats://${user}:${password}@host:4222`. Pass `servers`, `user`, and `pass` as connection options, or supply `${queue_connectionString}` directly.
- **Rule 5 (Zero-Guessing Scaling)**: Do NOT author manual `verticalAutoscaling` blocks in `import.yaml`. Zerops manages elastic autoscaling natively on Incus LXC.
- **Rule 6 (Fractal CoHaLo Bounded Execution)**: All synchronous commands MUST enforce timeouts (`timeout 10s`), wait limit (`WaitMsBeforeAsync: 10000`), and terminate orphan background processes with `manage_task action="kill"`.

## Decision Gates

| Task / Scenario | Recommended Strategy | Reference / Asset |
|---|---|---|
| Core Pub/Sub & Sub-ms RPC | `nc.subscribe('subject', { queue: 'workers' })`, `nc.request()` | [`references/usage.md`](file:///var/www/.agents/skills/nats/references/usage.md) |
| JetStream 2.12 Streams & Pull Consumers | `Nats-Msg-Id`, batch pull, `msg.term()`, priority | [`references/usage.md`](file:///var/www/.agents/skills/nats/references/usage.md) |
| KV Store & Object Store | `nats.kv('bucket')`, `nats.objectStore('bucket')` | [`references/usage.md`](file:///var/www/.agents/skills/nats/references/usage.md) |
| Zerops Infrastructure (:single vs :ha) | Port 4222 / 8222, Double-Auth Prevention, 4-Way Comparison | [`references/infra.md`](file:///var/www/.agents/skills/nats/references/infra.md) |
| Verified Client & Server Recipes | Production TypeScript, Python, and Go implementations | [`assets/nats_production_recipes.json`](file:///var/www/.agents/skills/nats/assets/nats_production_recipes.json) |

## Critical Workflows / Execution Steps
1. Define queue topology in `import.yaml` using `type: nats:single@2.12` or `type: nats:ha@2.12`.
2. Connect from runtime services via `4222` using `${queue_hostname}` or `${queue_connectionString}`.
3. Configure JetStream streams with appropriate storage (`File` for durability or `Memory` for speed).
4. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
5. **Circuit Breaker (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500 / timeout) before escalating.
6. **Sensor Attestation**: Verify physical sensor check (HTTP 200 on `:8222/healthz` or client connect exit code 0).

## Output Contract
- Validated `import.yaml` and `zerops.yaml` manifests targeting NATS on Zerops.
- Verified NATS connectivity and stream initialization with zero orphaned tasks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/nats/references/usage.md) — Developer manual, Core RPC `<0.3ms`, JetStream 2.12, KV Store, Object Store, TypeScript `nats.js`, Python `nats-py`, and Go `nats.go`.
- [`references/infra.md`](file:///var/www/.agents/skills/nats/references/infra.md) — Infrastructure manual, :single vs :ha RAFT cluster, ports 4222/8222, double-auth prevention, Four-Way comparison, and CoHaLo process hygiene.
- [`assets/nats_production_recipes.json`](file:///var/www/.agents/skills/nats/assets/nats_production_recipes.json) — Production-ready recipes for JetStream, KV store, and RPC.
- [`assets/import_template.yaml`](file:///var/www/.agents/skills/nats/assets/import_template.yaml) — Clean `import.yaml` template with native elastic autoscaling.
- [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/nats/assets/zerops_template.yaml) — Application lifecycle `zerops.yaml` template with NATS wiring.
- [`scripts/nats-validate.sh`](file:///var/www/.agents/skills/nats/scripts/nats-validate.sh) — Physical integrity validator for the nats skill suite.
