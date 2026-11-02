---
name: bifrost
description: "Trigger: bifrost, bifrost-cli, maxim ai, ai gateway, llm proxy, llm router, semantic cache, mcp gateway, drop-in openai proxy. High-performance enterprise AI gateway with sub-100us latency, adaptive CEL routing, and agent CLI integration."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.3"
---

# `bifrost` — Enterprise AI Gateway & CLI Orchestrator (v2.3)

## Activation Contract
Deploying, configuring, or calling Maxim AI Bifrost (`maximhq/bifrost`), running `@maximhq/bifrost-cli`, setting up OpenAI/Anthropic/MCP proxies, configuring CEL routing, or deploying semantic caching on Zerops.

## Core Directives & Invariants
- **Inverted Zero-Leak CEL Routing ($0 Primary)**: Default 100% of base inference to FreeLLMAPI ($0 tier, 12 keys across 2 account layers) via Priority 1 rule (`true`). Pro Tier (`deepseek`) is strictly restricted to Priority 0 explicit bypass (`headers['x-force-deepseek'] == 'true' || headers['x-tier'] == 'pro' || headers['x-routing-tier'] == 'pro'`) or automatic fallback on downstream FreeLLMAPI exhaustion.
- **Circuit Breaker Cooldown**: Trip the circuit breaker to OPEN for 60s cooldown when FreeLLMAPI returns HTTP 429 or exhausted rate limits, temporarily failing over to Pro Tier without cascading latency spikes.
- **Bifrost-CLI Integration**: `@maximhq/bifrost-cli` (v1.0.1) is globally accessible at `/usr/local/bin/bifrost` and `/usr/local/bin/bifrost-cli`. The bootstrap npm script downloads the compiled Go binary into `~/.bifrost/bin/bifrost` on first run; symlinks point directly to this native binary.
- **Allow-List Invariant**: In `config.json`, empty arrays `[]` strictly mean **DENY ALL**. Use `["*"]` to permit all models or keys. Use `key_ids` instead of deprecated `allowed_keys`.
- **PostgreSQL 18 & Storage**: Persist `config_store` and `logs_store` in managed PostgreSQL 18. Valkey 7.2 serves distributed locks. For `semantic_cache`, use `vector_store.type: chromem` or `qdrant` (Valkey 7.2 lacks RediSearch `FT.*`). SQLite is strictly prohibited in production.
- **Ephemeral ZCP & Production Mesh**: Production Bifrost runs in dedicated Zerops container `alpine/go@1.22` on port 8080 (`http://bifrost:8080`). FreeLLMAPI connects at `http://freellmapi:3001`. The `zcp` container is an ephemeral control plane; runtime inference never routes through `zcp`.
- **Agnostic Gateway & Brand Decoupling**: Bifrost is an agnostic transport gateway. It never stores brand personas or copy. Workers ingest Brandbook SSoT dynamically.

## Decision Gates & References
- **Client Drop-in & CLI**: [`usage.md`](file:///var/www/zerops-astro-skills/bifrost/references/usage.md) — Zero-leak CEL rules, `@maximhq/bifrost-cli`, and OpenAI/Anthropic proxies.
- **Zerops Topology & Storage**: [`infra.md`](file:///var/www/zerops-astro-skills/bifrost/references/infra.md) — Alpine deployment specs, PostgreSQL 18, and env mapping.
- **Production Config Template**: [`config_production_template.json`](file:///var/www/zerops-astro-skills/bifrost/assets/config_production_template.json) — Zero-leak CEL routing with circuit breaker.
- **Zerops Import Recipe**: [`zerops_bifrost_recipe.yaml`](file:///var/www/zerops-astro-skills/bifrost/assets/zerops_bifrost_recipe.yaml) — Standalone Zerops import recipe.
- **Validation**: `skills-suite-validate` — Physical test sensor.

## Output Contract
Deterministic response matching schema, verified health probe (HTTP 200 on port 8080), and clean process state.
