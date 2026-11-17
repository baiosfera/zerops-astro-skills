---
name: hermes-agent
description: "Trigger: hermes-agent, hermes, nous hermes, telegram hermes, apotelos mesh, astrological worker, progressive tools, zerops 360, zero cost routing. Nous Research Hermes-Agent Dual-RAG orchestrator for Zerops Python, Telegram Gateway, Tri-Pillar Paperclip/CrewAI mesh, and Oráculo Astrological Worker."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "2.6"
---

# Hermes-Agent Engine, Telegram Gateway & Zerops Orchestrator (v2.6)

Autonomous AI agent runtime powered by Nous Research Hermes (`NousResearch/hermes-agent`), native tool calling, fail-closed Telegram Gateway, embedded CrewAI SwarmCompiler, and ZCP/NATS/PostgreSQL 18 integration.

## Verified Core Invariants
1. **Prompt & Context Precedence (`prompt-assembly.md`)**: 3-tier cached prompt (`stable` $\to$ `context` $\to$ `volatile`); `~/.hermes/SOUL.md` loads first, and project context resolves first-match-wins (`.hermes.md` $\to$ `AGENTS.override.md` $\to$ `AGENTS.md` $\to$ `CLAUDE.md`).
2. **Minimum Context Floor & Provider Wiring**: Official Hermes enforces a **64,000-token minimum context window** for tool-enabled OpenAI-compatible `provider: custom` runs (`http://bifrost:8080/v1`, `model: auto`). Keep FreeLLMAPI catalog `contextWindow >= 65536`.
3. **Strict `$0` Routing & No Unrequested Paid Failover**: Wire `BIFROST_VIRTUAL_KEY: ${BIFROST_MASTER_VK}` (never hardcoded `vk-hermes-agent`) and `ALLOW_PAID_FALLBACK: "false"`. Escalate to DeepSeek only when the caller explicitly sets `x-force-deepseek: true` or `x-routing-tier: pro`.
4. **3-Level Skill & Paginated Playbook Access**: Consume skills via progressive disclosure (`skills_list` $\to$ `skill_view` $\to$ `references/*.md`), and read large playbooks via `get_playbook(playbook_slug, section, offset, limit)` without silent truncation.
5. **Memory & Storage (`hermes-agent` docs)**: `~/.hermes` (`HERMES_HOME=/mnt/localstorage/hermes/.hermes`) and `CREWAI_STORAGE_DIR=/mnt/localstorage/hermes/crewai` persist across Zerops deploys.

## Core Reference Map
- **Zerops Infra & Python 3.12**: [`references/infra.md`](file:///var/www/zerops-astro-skills/hermes-agent/references/infra.md)
- **Runtime Loops, Tools & Telegram**: [`references/usage.md`](file:///var/www/zerops-astro-skills/hermes-agent/references/usage.md)
- **Paperclip, CrewAI & Bifrost Mesh**: [`references/paperclip_crewai_mesh.md`](file:///var/www/zerops-astro-skills/hermes-agent/references/paperclip_crewai_mesh.md)
- **Astrological & Suite Integration**: [`references/suite_integration.md`](file:///var/www/zerops-astro-skills/hermes-agent/references/suite_integration.md)
- **AGY Bidirectional Bridge**: [`references/bridge_agy.md`](file:///var/www/zerops-astro-skills/hermes-agent/references/bridge_agy.md)
- **Assets**: [`config_production_template.yaml`](file:///var/www/zerops-astro-skills/hermes-agent/assets/config_production_template.yaml), [`zerops_hermes_recipe.yaml`](file:///var/www/zerops-astro-skills/hermes-agent/assets/zerops_hermes_recipe.yaml), [`hermes_tools_bundle.py`](file:///var/www/zerops-astro-skills/hermes-agent/assets/hermes_tools_bundle.py)

## Validation & Output Contract
Run `python3 -B -m unittest discover -s tests -v` and `skills-suite-validate`; report HTTP 200 on `/healthz`, fail-closed Telegram RBAC, and zero automatic paid escalation.
