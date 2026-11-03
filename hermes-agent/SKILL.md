---
name: "hermes-agent"
description: "Nous Research Hermes-Agent (CalVer 2026.8+) Dual-RAG orchestrator for Zerops Python (Ubuntu invariant), Telegram Bot Gateway, Tri-Pillar Paperclip/CrewAI mesh, Oráculo Astrological Worker, and Antigravity (AGY) bridge."
version: "2.2"
---

# Hermes-Agent Engine, Telegram-to-AGY Gateway & Astrological Worker (v2.2)

Autonomous AI agent runtime powered by Nous Research Hermes models, featuring native function calling (`<tool_call>`), secure Telegram Gateway with anti-flood batching, Tri-Pillar mesh orchestration (Hermes + Paperclip + CrewAI/PydanticAI), Oráculo 15-shard astrological calculation worker on NATS JetStream, Zerops Python deployment, and bidirectional Antigravity (AGY) bridge.

## Core Capabilities & Reference Map

| Domain | Scope & Capabilities | Authoritative Guide |
|---|---|---|
| **Tri-Pillar Mesh** | Hermes Gateway v1, Paperclip OS governance, CrewAI/PydanticAI dual-engine, PostgreSQL 18 + LocalStorage SSoT | [`references/paperclip_crewai_mesh.md`](file:///var/www/.agents/skills/hermes-agent/references/paperclip_crewai_mesh.md) |
| **Astrological Worker** | Oráculo 15-shard computation, NATS RPC (`astrology.requests`), 11 XML gold feeds, PostgreSQL 18 ingest | [`references/suite_integration.md`](file:///var/www/.agents/skills/hermes-agent/references/suite_integration.md) |
| **Runtime & Loop** | ChatML `<tool_call>`, scratchpad execution, Telegram Bot API 22.8, RBAC, anti-flood batching | [`references/usage.md`](file:///var/www/.agents/skills/hermes-agent/references/usage.md) |
| **Zerops Infra** | Python 3.12 Ubuntu invariant, vendor caching, persistent storage, systemd/supervisord daemon | [`references/infra.md`](file:///var/www/.agents/skills/hermes-agent/references/infra.md) |
| **AGY Bridge** | Telegram-to-AGY bridge: NATS JetStream (recommended), ZCP MCP client, bounded SSH, REST plugin | [`references/bridge_agy.md`](file:///var/www/.agents/skills/hermes-agent/references/bridge_agy.md) |
| **Suite Integration** | Directus, ERPNext, EvolutionGo, Astro, PostgreSQL 18, Valkey 7.2, NATS cluster orchestration | [`references/suite_integration.md`](file:///var/www/.agents/skills/hermes-agent/references/suite_integration.md) |

## Operational State Machine (CoHaLo Protocol)

```
[Inflow: Telegram / Paperclip Gateway v1] ──> [Gate 0: Epistemic Whitelist & RBAC]
                                                     │
                                                     ▼
[Gate 1: Intent & Safety] ──────────────────> [Gate 2: Tool / Swarm Resolution]
                                                     │
                                                     ▼
[Gate 3: Execution Sensor] ─────────────────> [Outflow: Verified Result / SSE Events]
```

## Quick Reference Commands

- **Validate Installation & Environment**:
  ```bash
  skills-suite-validate
  ```
- **Start Gateway Daemon (Local / Container)**:
  ```bash
  python -m hermes.cli gateway --config config.yaml
  ```
- **Inspect Active NATS Bridge Status**:
  ```bash
  nats stream info ZEROPS_OPS
  ```

## Bundled Assets & Recipes

- Production Configuration Template: [`assets/config_production_template.yaml`](file:///var/www/.agents/skills/hermes-agent/assets/config_production_template.yaml)
- Zerops Service Manifest Recipe: [`assets/zerops_hermes_recipe.yaml`](file:///var/www/.agents/skills/hermes-agent/assets/zerops_hermes_recipe.yaml)
- Production Tool Handlers Bundle: [`assets/hermes_tools_bundle.py`](file:///var/www/.agents/skills/hermes-agent/assets/hermes_tools_bundle.py)
