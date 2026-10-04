---
name: devllm-telemetry
description: "Trigger: devllm-telemetry, llm telemetry, ai costs, nats health, valkey health, postgres backups, token tracking, llmops directus. Master DevOps, LLMOps & Infrastructure Telemetry Orchestrator with Directus Insights, NATS :8222 & Valkey in Zerops."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `devllm-telemetry` — DevOps, LLMOps & Infrastructure Health Orchestrator (v2.0)

## Activation Contract
Activate when tracking AI model token expenditures and costs in USD (`llm_telemetry_logs`), monitoring NATS Server 2.12 HTTP statistics (`:8222/varz`), inspecting Valkey 7.2 memory footprint and BullMQ Dead Letter Queue (DLQ) depth, or verifying automated PostgreSQL 18 `pg_dump` snapshots in Directus 11+ Insights on Zerops.

## Hard Rules
- **Non-Blocking Telemetry**: Ingesting LLM metrics or system health logs must NEVER block the main request/response lifecycle. Always use background promises (`setImmediate`) or NATS events.
- **Zero Memory Bloat**: Never deploy heavy standalone observability containers (Prometheus, Grafana, Datadog). All technical dashboards and metrics reside natively inside Directus 11+ Insights (~0 MB extra RAM).
- **Backup Verification**: Health pollers must verify that `.sql.gz` backups exist in `/mnt/localstorage/backups/postgresql/` and are under 26 hours old.
- **Fractal CoHaLo**: Enforce strict hygiene (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans (`manage_task action="kill"`), sensor (Directus telemetry record probe).
- **Zero Deletion**: Consult [`references/usage.md`](file:///var/www/.agents/skills/devllm-telemetry/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/devllm-telemetry/references/infra.md) for full lossless APIs.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 4D Matrix & Comparison | Directus Telemetry vs Prometheus, Grafana, Datadog | [`references/usage.md#1-4d-comparative-architectural-matrix`](file:///var/www/.agents/skills/devllm-telemetry/references/usage.md) |
| LLMOps Token & Cost Tracker | Intercept model calls and calculate USD costs | [`references/usage.md#3-typescript-contract-llmops-telemetry-tracker-wrapper`](file:///var/www/.agents/skills/devllm-telemetry/references/usage.md) |
| System Health Daemon Poller | Sample NATS :8222, Valkey memory, DLQ & backups | [`references/usage.md#4-system-health-daemon-poller-nats-valkey--backups`](file:///var/www/.agents/skills/devllm-telemetry/references/usage.md) |
| Ops Dashboard Seeder Script | Provision AI spend and latency panels in Directus | [`references/usage.md#5-declarative-directus-insights-panel-seeder-for-devops--llmops`](file:///var/www/.agents/skills/devllm-telemetry/references/usage.md) |
| Multi-Service Topology | Connect Directus, NATS, Valkey, AI Workers & Storage | [`references/infra.md#1-multi-service-observability-topology-in-zerops`](file:///var/www/.agents/skills/devllm-telemetry/references/infra.md) |
| NATS HTTP Monitoring Setup | Configure and verify port 8222 /varz and /connz | [`references/infra.md#2-nats-server-http-monitoring-configuration`](file:///var/www/.agents/skills/devllm-telemetry/references/infra.md) |
| Production Recipes JSON | LLM tracker wrapper, poller code, and schemas | [`assets/devllm_telemetry_production_recipes.json`](file:///var/www/.agents/skills/devllm-telemetry/assets/devllm_telemetry_production_recipes.json) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/devllm-telemetry-validate.sh`](file:///var/www/.agents/skills/devllm-telemetry/scripts/devllm-telemetry-validate.sh) |

## Execution Steps
1. Verify `DIRECTUS_URL` and `VALKEY_URL` in Zerops environment variables.
2. Enable NATS Server HTTP monitoring on port `8222`.
3. Execute `seedOpsDashboard()` to provision technical telemetry panels in Directus Insights.
4. Launch the 60-second system health poller daemon in background.
5. Verify health collection logging via physical sensor probe.

## Output Contract
- Zero-bloat DevOps & LLMOps observability control plane running inside Directus 11+ Insights on Zerops.
- Continuous 60s health monitoring of NATS, Valkey, backups, and passing physical validation sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/devllm-telemetry/references/usage.md) — 4D matrix, LLM tracker wrapper, health poller, dashboard seeder, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/devllm-telemetry/references/infra.md) — Multi-service topology, NATS :8222 setup, and CoHaLo harness.
- [`assets/devllm_telemetry_production_recipes.json`](file:///var/www/.agents/skills/devllm-telemetry/assets/devllm_telemetry_production_recipes.json) — Production tracker wrappers and health poller recipes.
- [`scripts/devllm-telemetry-validate.sh`](file:///var/www/.agents/skills/devllm-telemetry/scripts/devllm-telemetry-validate.sh) — Deterministic quality & token validation sensor.
