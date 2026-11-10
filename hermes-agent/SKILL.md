---
name: "hermes-agent"
description: "Trigger: hermes-agent, hermes, nous hermes, telegram hermes, apotelos mesh, astrological worker, progressive tools, zerops 360, zero cost routing. Nous Research Hermes-Agent Dual-RAG orchestrator for Zerops Python, Telegram Gateway, Tri-Pillar Paperclip/CrewAI mesh, and Oráculo Astrological Worker."
version: "2.5"
---

# Hermes-Agent Engine, Telegram Gateway & Zerops 360 Orchestrator (v2.5)

Autonomous AI agent runtime powered by Nous Research Hermes models, featuring native function calling (`<tool_call>`), secure Telegram Gateway with anti-flood batching, Tri-Pillar mesh orchestration (Hermes + Paperclip + CrewAI/PydanticAI), Oráculo 15-shard astrological calculation worker on NATS JetStream, Zerops Python deployment, and bidirectional Antigravity bridge.

## Core Capabilities & Reference Map

| Domain | Scope & Capabilities | Authoritative Guide |
|---|---|---|
| **Zerops 360 Topology** | 10-service cluster awareness (`bifrost:8080`, `freellmapi:3001`, `paperclip:3100`, `pidev:3000`, `hermes:8000`, `nats:4222`, `database:5432`, `valkey:6379`, `/mnt/localstorage`, `zcp:8080`) | [`references/infra.md`](file:///var/www/.agents/skills/hermes-agent/references/infra.md) |
| **Calm Autodiscovery** | Sensor-First: verify physical disk (`read_file`, `list_directory`, `run_command --audit`) before asserting missing assets; proactive CLI execution | [`references/usage.md`](file:///var/www/.agents/skills/hermes-agent/references/usage.md) |
| **Universal Primitives** | 5 core primitives (`run_command`, POSIX files, `execute_query`, `mem_*`, `get_skill_docs`). Anti-Frankenstein: zero bespoke tools in `tools.py`; CLIs in `/usr/local/bin/` (`apotelos`, `orchesbrand`, `linear-cli`). | [`references/usage.md`](file:///var/www/.agents/skills/hermes-agent/references/usage.md) |
| **Smart Routing ($0)** | Priority 1 default to FreeLLMAPI ($0) via Bifrost (<100µs); DeepSeek Pro exclusively for explicit user override or 429 failover | [`references/paperclip_crewai_mesh.md`](file:///var/www/.agents/skills/hermes-agent/references/paperclip_crewai_mesh.md) |
| **Tri-Pillar Mesh** | Hermes Gateway v1, Paperclip OS governance, CrewAI/PydanticAI dual-engine, PostgreSQL 18 + LocalStorage SSoT | [`references/paperclip_crewai_mesh.md`](file:///var/www/.agents/skills/hermes-agent/references/paperclip_crewai_mesh.md) |
| **Apotelos Protocol** | Symmetric native `apotelos` CLI (`/usr/local/bin/apotelos`), reverse causality ($T_\text{final} \to T_0$), Blackboard manifest compilation | [`references/paperclip_crewai_mesh.md`](file:///var/www/.agents/skills/hermes-agent/references/paperclip_crewai_mesh.md) |
| **Progressive Disclosure** | `classify_query_intent`: prune 42 tools on chitchat (`x-freellm-task-type: chat`), saving ~5k tokens/turn | [`references/usage.md`](file:///var/www/.agents/skills/hermes-agent/references/usage.md) |
| **Astrological Worker** | Oráculo 15-shard computation, NATS RPC (`astrology.requests`), PostgreSQL 18 ingest | [`references/suite_integration.md`](file:///var/www/.agents/skills/hermes-agent/references/suite_integration.md) |
| **Runtime & Loop** | ChatML `<tool_call>`, scratchpad execution, Telegram Bot API 22.8, RBAC, anti-flood batching | [`references/usage.md`](file:///var/www/.agents/skills/hermes-agent/references/usage.md) |
| **Zero-CoT & Persona** | Deterministic `sanitize_model_output`, Rioplatense voseo standard, zero thinking leakage | [`references/usage.md`](file:///var/www/.agents/skills/hermes-agent/references/usage.md) |
| **Zerops Infra** | Python 3.12 Ubuntu invariant, vendor caching, persistent storage, systemd/supervisord daemon | [`references/infra.md`](file:///var/www/.agents/skills/hermes-agent/references/infra.md) |
| **AGY Bridge** | Telegram-to-AGY bridge: NATS JetStream, ZCP MCP client, bounded SSH, REST plugin | [`references/bridge_agy.md`](file:///var/www/.agents/skills/hermes-agent/references/bridge_agy.md) |

## Quick Reference Commands

```bash
# Validate installation & environment
skills-suite-validate

# Audit all brand verticals via canonical CLI
orchesbrand --vertical all --audit

# Inspect active NATS bridge status
nats stream info ZEROPS_OPS
```

## Bundled Assets & Recipes

- Production Configuration Template: [`assets/config_production_template.yaml`](file:///var/www/.agents/skills/hermes-agent/assets/config_production_template.yaml)
- Zerops Service Manifest Recipe: [`assets/zerops_hermes_recipe.yaml`](file:///var/www/.agents/skills/hermes-agent/assets/zerops_hermes_recipe.yaml)
- Production Tool Handlers Bundle: [`assets/hermes_tools_bundle.py`](file:///var/www/.agents/skills/hermes-agent/assets/hermes_tools_bundle.py)
