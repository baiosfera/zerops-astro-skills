---
name: valkey
description: "Trigger: valkey, redis, valkey@7.2, ioredis, bullmq, valkey-glide, cache-aside, sliding window rate limit, valkey:single, valkey:ha. Architect, optimize, connect, and manage Valkey 7.2 in-memory caching and session engines on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# Valkey — Zerops Managed In-Memory Engine & Cache (v2.1)

## Activation Contract
Activate whenever architecting, connecting, provisioning, or tuning Valkey 7.2 in-memory stores, BullMQ job queues, cache-aside patterns, distributed locks, or rate limiters on Zerops (`type: valkey:single@7.2` or `type: valkey:ha@7.2`).

## Hard Rules & Positive Guidance
- **Topology Selection**: Deploy `valkey:single@7.2` for dev/staging and ephemeral caching; deploy `valkey:ha@7.2` (multi-node with Sentinel auto-failover) for production queues and session state.
- **Resource Sizing Profiles**: Assign explicit sizing profiles (`cache-hobby` for dev, `cache-staging` for preview, `cache-production` for dedicated high-throughput).
- **Port Routing Architecture**:
  - Port `6379`: Primary Read/Write internal mesh connection (unencrypted internal network, high throughput).
  - Port `26379`: Sentinel quorum monitoring port (available in `:ha`).
- **Memory Eviction Policy**: Set `maxmemory-policy volatile-lru` for mixed caching/queue workloads; set `noeviction` for strictly durable BullMQ queues to prevent silent job loss.
- **Connection Hygiene**: Use connection pooling with heartbeat ping. Set `tcp-keepalive 60` to prevent stale socket accumulation.
- **Zero Plaintext Secrets**: Wire connections using platform variables `${cache_connectionString}`, `${cache_hostname}`, `${cache_port}`.

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Cache-Aside & Rate Limiting | Sliding window counters, TTL caching | [`references/usage.md#cache-patterns`](file:///var/www/.agents/skills/valkey/references/usage.md) |
| BullMQ Worker Queues | Durable queue workers, dead-letter routing | [`references/usage.md#bullmq-queues`](file:///var/www/.agents/skills/valkey/references/usage.md) |
| Single vs HA Sentinel | Ephemeral cache vs durable state clusters | [`references/infra.md#topology-comparison`](file:///var/www/.agents/skills/valkey/references/infra.md) |
| Valkey Scaling Profiles | Sizing guidelines and memory limits | [`references/infra.md#sizing-profiles`](file:///var/www/.agents/skills/valkey/references/infra.md) |

## Critical Workflows
1. Define Valkey in `import.yaml` with `type: valkey:single@7.2` or `valkey:ha@7.2` and explicit profile.
2. Connect runtimes via internal mesh on port `6379` using `${cache_connectionString}`.
3. Configure BullMQ and cache-aside layers with explicit TTL and eviction policies.
4. Verify connection with physical sensor (`redis-cli -u "$cache_connectionString" PING`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/valkey/references/usage.md) — Valkey 7.2 client drivers, BullMQ queue patterns, cache-aside, and distributed locking.
- [`references/infra.md`](file:///var/www/.agents/skills/valkey/references/infra.md) — Single vs HA Sentinel architecture, sizing profiles, eviction policies, and connection tuning.
