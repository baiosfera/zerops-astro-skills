---
name: valkey
description: "Trigger: valkey, redis, valkey@7.2, ioredis, bullmq, valkey-glide, cache-aside, sliding window rate limit, valkey:single, valkey:ha. Architect, optimize, connect, and manage Valkey 7.2 in-memory caching and session engines on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# Valkey — Zerops Managed In-Memory Engine & Cache (v2.0)

## Activation Contract
Activate whenever architecting, querying, tuning, provisioning, or connecting to Valkey 7.2, Redis-compatible caches, RESP3 protocols, BullMQ background queues, sliding-window rate limiters, or managing Zerops semi-managed services (`type: valkey:single@7.2` or `type: valkey:ha@7.2`).

## Hard Rules
- **Rule 1 (Version Pinning Invariant)**: MUST use `valkey:single@7.2` or `valkey:ha@7.2`. `valkey@8` is strictly prohibited (fails platform import).
- **Rule 2 (Scaling Profile Invariant)**: Always assign an explicit `profile:` (`hobby` for dev :single, `staging` for production lean, `production` for dedicated CPU mission-critical). Do NOT author manual `verticalAutoscaling` blocks.
- **Rule 3 (Mandatory Authentication)**: Always authenticate using `${cache_password}` or `${cache_connectionString}`. There is no separate `${cache_user}` variable (user is `default`). Unauthenticated connections throw `NOAUTH`.
- **Rule 4 (Port Routing Architecture)**:
  - Port `6379`: Primary Read/Write node (TCP/RESP over private VXLAN).
  - Port `6380`: External TLS access (`${cache_portTls}`).
  - Port `7000`: Balanced Read Replicas (available exclusively in `:ha`).
  - Port `7001`: Read Replicas TLS (available exclusively in `:ha`).
- **Rule 5 (Architectural Scope Boundaries)**: Valkey is strictly for **In-Memory Caching + Sessions + Redis-bound Queues (BullMQ, Celery, Sidekiq)**. For general distributed message brokering, use `nats@2.12`.
- **Rule 6 (Fractal CoHaLo Bounded Execution)**: All synchronous commands MUST enforce timeouts (`timeout 10s`), wait limit (`WaitMsBeforeAsync: 10000`), and terminate orphan background processes with `manage_task action="kill"`.

## Decision Gates

| Task / Scenario | Recommended Strategy | Reference / Asset |
|---|---|---|
| In-Memory Cache-Aside & Sessions | TTL expiration, pipeline batching, `ioredis` / `redis-py` | [`references/usage.md`](file:///var/www/.agents/skills/valkey/references/usage.md) |
| Sliding-Window Rate Limiting | Atomic Lua scripts with Redis sorted sets (`ZADD`, `ZRANGEBYSCORE`) | [`references/usage.md`](file:///var/www/.agents/skills/valkey/references/usage.md) |
| BullMQ / Celery Queue Engine | Worker & Queue initialization with connection options | [`references/usage.md`](file:///var/www/.agents/skills/valkey/references/usage.md) |
| Zerops Infrastructure (:single vs :ha) | `hobby` vs `staging` vs `production`, Ports 6379/7000, 4-Way Comparison | [`references/infra.md`](file:///var/www/.agents/skills/valkey/references/infra.md) |
| Verified Client Recipes | Production TypeScript, Python, and Go implementations | [`assets/valkey_production_recipes.json`](file:///var/www/.agents/skills/valkey/assets/valkey_production_recipes.json) |

## Critical Workflows / Execution Steps
1. Define cache topology in `import.yaml` using `type: valkey:single@7.2` or `type: valkey:ha@7.2` with explicit `profile:`.
2. Connect from runtime services via `6379` using `${cache_connectionString}` or `${cache_password}`.
3. Configure cache TTLs and eviction policies appropriate for application memory bounds.
4. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
5. **Circuit Breaker (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500 / timeout) before escalating.
6. **Sensor Attestation**: Verify physical sensor check (exit code 0 on `redis-cli PING` returning `PONG`).

## Output Contract
- Validated `import.yaml` and `zerops.yaml` manifests targeting Valkey on Zerops.
- Verified cache and BullMQ connectivity with zero orphaned tasks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/valkey/references/usage.md) — Developer manual, Valkey 7.2 RESP3, Cache-Aside, sliding-window rate limiting Lua, and BullMQ queue patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/valkey/references/infra.md) — Infrastructure manual, :single vs :ha topology, profiles, ports, mandatory auth, Four-Way comparison, and CoHaLo process hygiene.
- [`assets/valkey_production_recipes.json`](file:///var/www/.agents/skills/valkey/assets/valkey_production_recipes.json) — Production-ready recipes for Cache-Aside, Lua rate limiting, and BullMQ.
- [`assets/import_template.yaml`](file:///var/www/.agents/skills/valkey/assets/import_template.yaml) — Clean `import.yaml` template with native elastic autoscaling.
- [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/valkey/assets/zerops_template.yaml) — Application lifecycle `zerops.yaml` template with Valkey wiring.
- [`scripts/valkey-validate.sh`](file:///var/www/.agents/skills/valkey/scripts/valkey-validate.sh) — Physical integrity validator for the valkey skill suite.
