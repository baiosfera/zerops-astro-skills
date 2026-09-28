---
name: bifrost
description: "Trigger: bifrost, bifrost-cli, maxim ai, ai gateway, llm proxy, llm router, semantic cache, mcp gateway, drop-in openai proxy. High-performance enterprise AI gateway with sub-100us latency, adaptive CEL routing, and agent CLI integration."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# Bifrost — Enterprise AI Gateway & CLI Orchestrator (v2.1)

## Activation Contract
Activate whenever deploying, configuring, or interacting with Maxim AI Bifrost (`maximhq/bifrost`), running `@maximhq/bifrost-cli`, setting up OpenAI/Anthropic/MCP compatible drop-in proxies, configuring adaptive multi-LLM failover, or deploying semantic caching on Zerops.

## Hard Rules
- **Rule 1 (Zero Deletion & High-Fidelity Invariant)**: Preserve complete method signatures, configuration parameters, and error codes in full fidelity. Consult [`references/usage.md`](file:///var/www/.agents/skills/bifrost/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/bifrost/references/infra.md) for full exegesis.
- **Rule 2 (2026 Allow-List Invariant)**: In `config.json`, empty arrays `[]` strictly mean **DENY ALL**. Use `["*"]` to allow all models or keys. Use `key_ids` instead of deprecated `allowed_keys`.
- **Rule 3 (Fractal CoHaLo Bounded Execution)**: Enforce `timeout 10s`, `WaitMsBeforeAsync: 10000`, circuit breakers (maximum 2 retries on HTTP 5xx/timeout), and terminate background tasks via `manage_task action="kill"`.

## Decision Gates

| Use Case / Scenario | Action / Recommended Pattern | Primary Reference |
|---|---|---|
| Client Drop-in Proxy (OpenAI / Anthropic) | Override `baseURL` to `http://localhost:8080/v1` or `/anthropic/v1` with Virtual Key | [`references/usage.md`](file:///var/www/.agents/skills/bifrost/references/usage.md#4-production-patterns--verified-code-recipes) |
| Autonomous MCP Gateway & Tool Calling | Route `/mcp` traffic through Bifrost daemon with tool allowlist | [`references/usage.md`](file:///var/www/.agents/skills/bifrost/references/usage.md#pattern-3-mcp-model-context-protocol-gateway) |
| Coding Agent Integration | Launch `@maximhq/bifrost-cli` TUI or export drop-in proxy environment variables | [`references/usage.md`](file:///var/www/.agents/skills/bifrost/references/usage.md#pattern-5-bifrost-cli-maximhqbifrost-cli-coding-agent-bridge) |
| Production Container Deploy | Deploy standalone Go binary on Alpine 3.21 via `zerops.yaml` | [`references/infra.md`](file:///var/www/.agents/skills/bifrost/references/infra.md#4-lifecycle-commands--manifest-zeropsyaml) |
| Semantic & Direct Caching | Connect Valkey/Redis with `dimension: 1` or cosine embeddings | [`references/infra.md`](file:///var/www/.agents/skills/bifrost/references/infra.md#3-storage-architecture--permission-safeguards) |
| Declarative Routing & Fallbacks | Configure CEL expressions and weighted targets in `config.json` | [`assets/config_production_template.json`](file:///var/www/.agents/skills/bifrost/assets/config_production_template.json) |

## Critical Workflows / Execution Steps
1. **Validation & Discovery**: Check `config.json` syntax and verify required environment variables (`BIFROST_ENCRYPTION_KEY`, provider keys).
2. **Process Hygiene**: Start or probe daemon with bounded timeout: `timeout 10s curl -s -f http://localhost:8080/health`.
3. **Circuit Breakers**: Halt execution after 2 consecutive failed attempts and inspect `/metrics` or server logs.
4. **Sensor Attestation**: Verify liveness probe returns HTTP 200 before routing live inference traffic.

## Output Contract
- Deterministic response or JSON configuration matching [`https://www.getbifrost.ai/schema`](https://www.getbifrost.ai/schema).
- Verified health probe metric (HTTP 200) and clean process state.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/bifrost/references/usage.md) — Method matrix, 5+ code recipes, CLI guide, error catalog, and 2026 breaking changes.
- [`references/infra.md`](file:///var/www/.agents/skills/bifrost/references/infra.md) — Zerops deployment specs, .env dictionary, storage safeguards, and CoHaLo process hygiene.
- [`assets/config_production_template.json`](file:///var/www/.agents/skills/bifrost/assets/config_production_template.json) — Production declarative configuration template.
- [`assets/zerops_bifrost_recipe.yaml`](file:///var/www/.agents/skills/bifrost/assets/zerops_bifrost_recipe.yaml) — Standalone Zerops import recipe.
- [`scripts/bifrost-validate.sh`](file:///var/www/.agents/skills/bifrost/scripts/bifrost-validate.sh) — Deterministic physical sensor validation script.
