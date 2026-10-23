---
name: devllm-telemetry
description: "Trigger: devllm-telemetry, llm telemetry, ai costs, nats health, valkey health, postgres backups, token tracking, llmops directus. Master DevOps, LLMOps & Infrastructure Telemetry Orchestrator with Directus Insights, NATS :8222 & Valkey in Zerops."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# `devllm-telemetry` — DevOps, LLMOps & Infrastructure Health Orchestrator (v2.1)

## Activation Contract
Tracking AI token spend and costs in USD (`llm_telemetry_logs`), monitoring NATS Server 2.12 HTTP stats (`:8222/varz`), inspecting Valkey memory and BullMQ DLQ depth, or verifying PostgreSQL backup snapshots in Directus Insights.

## Core Directives & Invariants
- **Non-Blocking Telemetry**: Ingesting LLM metrics or health logs must never block user requests. Use asynchronous background promises (`setImmediate`) or NATS events.
- **Zero Memory Bloat**: Never deploy heavy observability stacks (Prometheus, Grafana, Datadog). All technical dashboards and metrics reside natively inside Directus 11+ Insights (~0 MB extra RAM).
- **Backup Verification**: Health pollers must verify that `.sql.gz` backups exist in `/mnt/localstorage/backups/postgresql/` and are under 26 hours old.
- **Process Hygiene**: Enforce strict timeouts (`timeout 10s`), `WaitMsBeforeAsync: 10000`, and clean termination of background tasks.

## Decision Gates & References
- **Matrix & Tracker Wrapper**: [`usage.md`](file:///var/www/zerops-astro-skills/devllm-telemetry/references/usage.md) — Directus Telemetry comparison, LLMOps token wrapper, and health daemon.
- **Multi-Service Topology**: [`infra.md`](file:///var/www/zerops-astro-skills/devllm-telemetry/references/infra.md) — NATS port 8222 monitoring and storage configuration.
- **Production Recipes**: [`devllm_telemetry_production_recipes.json`](file:///var/www/zerops-astro-skills/devllm-telemetry/assets/devllm_telemetry_production_recipes.json) — Tracker schemas and poller scripts.
- **Validation**: [`devllm-telemetry-validate.sh``skills-suite-validate` — Liveness and metric sensor.

## Output Contract
Zero-bloat DevOps & LLMOps control plane in Directus 11+ Insights with 60s health monitoring and passing validation sensors.
