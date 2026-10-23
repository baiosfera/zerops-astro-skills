---
name: bifrost
description: "Trigger: bifrost, bifrost-cli, maxim ai, ai gateway, llm proxy, llm router, semantic cache, mcp gateway, drop-in openai proxy. High-performance enterprise AI gateway with sub-100us latency, adaptive CEL routing, and agent CLI integration."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.2"
---

# `bifrost` — Enterprise AI Gateway & CLI Orchestrator (v2.2)

## Activation Contract
Deploying, configuring, or calling Maxim AI Bifrost (`maximhq/bifrost`), running `@maximhq/bifrost-cli`, setting up OpenAI/Anthropic/MCP proxies, configuring CEL routing, or deploying semantic caching on Zerops.

## Core Directives & Invariants
- **Allow-List Invariant**: In `config.json`, empty arrays `[]` mean **DENY ALL**. Use `["*"]` to permit all models or keys. Use `key_ids` instead of deprecated `allowed_keys`.
- **PostgreSQL 18 & Storage**: Persist `config_store` and `logs_store` in managed PostgreSQL 18. Valkey 7.2 serves distributed locks. For `semantic_cache`, use `vector_store.type: chromem` or `qdrant`. SQLite is strictly prohibited in production.
- **Ephemeral ZCP & Production Mesh**: Production Bifrost runs in dedicated Zerops container `alpine/go@1.22` on port 8080 (`http://bifrost:8080`). FreeLLMAPI connects at `http://freellmapi:3001`. The `zcp` container is strictly an ephemeral control plane for editing and auditing; runtime inference never routes through `zcp`.
- **Dual-Tier Predictive Intent Routing**: Classify intent before dispatch to eliminate cascading failover latency. Route transactional, revenue, tool-calling, and reasoning intents directly to Pro Tier (`DeepSeek V4/V3`) via header `x-tier: production` or `x-routing-tier: pro`. Route lightweight FAQs to Free Tier (`FreeLLMAPI`) with strict timeout ($\le$ 3s) and 1 retry.
- **Circuit Breaker Cooldown**: Trip the circuit breaker to OPEN for 120s cooldown when FreeLLMAPI triggers 3 consecutive HTTP 429 errors within 60s, bypassing FreeLLMAPI to preserve conversational latency.
- **Agnostic Gateway & Brand Decoupling**: Bifrost remains an agnostic transport gateway. It never stores brand guidelines, personas, copy or tokens. Identity control belongs exclusively to client workers, which ingest Brandbook SSoT dynamically.

## Decision Gates & References
- **Client Drop-in & Patterns**: [`usage.md`](file:///var/www/zerops-astro-skills/bifrost/references/usage.md) — OpenAI/Anthropic proxies, MCP streaming, and `@maximhq/bifrost-cli`.
- **Zerops Topology & Lifecycle**: [`infra.md`](file:///var/www/zerops-astro-skills/bifrost/references/infra.md) — Alpine deployment specs, storage safeguards, and env mapping.
- **Production Config Template**: [`config_production_template.json`](file:///var/www/zerops-astro-skills/bifrost/assets/config_production_template.json) — Declarative CEL routing and fallbacks.
- **Zerops Import Recipe**: [`zerops_bifrost_recipe.yaml`](file:///var/www/zerops-astro-skills/bifrost/assets/zerops_bifrost_recipe.yaml) — Standalone Zerops import recipe.
- **Validation**: [`bifrost-validate.sh``skills-suite-validate` — Liveness probe and config sensor.

## Output Contract
Deterministic response matching schema, verified health probe (HTTP 200 on port 8080), and clean process state.
