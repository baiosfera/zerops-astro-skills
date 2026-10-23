---
name: nats
description: "Trigger: nats, nats server, jetstream, nats rpc, nats-py, nats kv store, nats object store, nats queue groups. Architect, deploy, and operate NATS Server 2.12, Core NATS RPC (<0.3ms P99), Queue Groups, and JetStream on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# NATS Server — Zerops Managed Messaging & Streaming Engine (v2.1)

## Activation Contract
Activate whenever architecting, configuring, connecting, or benchmarking NATS Server 2.12+, JetStream streaming, ultra-low latency Request-Reply RPC (<0.3ms P99), Subject Mappings, Key-Value stores, or queue groups in Zerops (`type: nats:single@2.12` or `type: nats:ha@2.12`).

## Hard Rules & Positive Guidance
- **Topology Selection**: Use `nats:single@2.12` for microservice meshes, dev and staging; use `nats:ha@2.12` (3-node RAFT JetStream cluster) for production financial events or zero-loss pipelines.
- **Port Routing Architecture**:
  - Port `4222`: Client communication (internal mesh, Request-Reply, JetStream pub/sub).
  - Port `6222`: Cluster routing (HA node sync, internal only).
  - Port `8222`: HTTP monitoring and metrics dashboard (`/varz`, `/connz`, `/healthz`).
- **Communication Pattern Separation**:
  - Request-Reply RPC: Use Core NATS subjects (`rpc.<service>.<action>`) with queue groups (`queue: "service.workers"`) for load balancing without JetStream storage overhead.
  - Durable Events: Use JetStream streams (`events.*`) with file storage for ordered, at-least-once transactional delivery.
- **Subject Namespace Standards**: Follow structured hierarchical naming (`<domain>.<entity>.<action>`, e.g., `orders.created`, `payments.confirmed`).
- **Connection Pooling**: Maintain a single long-lived connection per runtime process; multiplex subjects over lightweight subscriptions.

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Request-Reply RPC | Sub-millisecond synchronous microservice RPC | [`references/usage.md#nats-rpc`](file:///var/www/.agents/skills/nats/references/usage.md) |
| JetStream Streams | Persistent event queues, deduplication, ack | [`references/usage.md#jetstream-patterns`](file:///var/www/.agents/skills/nats/references/usage.md) |
| Single vs HA Cluster | Standalone lightweight vs 3-node RAFT cluster | [`references/infra.md#topology`](file:///var/www/.agents/skills/nats/references/infra.md) |
| Telemetry & Metrics | Health monitoring via port 8222 /varz | [`references/infra.md#monitoring`](file:///var/www/.agents/skills/nats/references/infra.md) |

## Critical Workflows
1. Provision NATS in `import.yaml` with `type: nats:single@2.12` or `nats:ha@2.12`.
2. Connect runtimes via `${nats_url}` on port `4222`.
3. Register RPC responders with queue groups for balanced service-to-service communication.
4. Verify server health via physical sensor (`curl -s http://nats:8222/healthz`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/nats/references/usage.md) — Core NATS RPC, JetStream stream creation, consumer configurations, and TypeScript/Python patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/nats/references/infra.md) — Single vs HA topologies, port architecture, sizing profiles, and monitoring.
