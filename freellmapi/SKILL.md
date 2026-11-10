---
name: freellmapi
description: "Trigger: freellmapi, free-llm-api, freellmapi gateway, multi-provider free llm, free tier inference, groq cerebras router, zerops freellmapi, bifrost freellmapi upstream. Aggregated free LLM proxy with 34+ providers, smart failover, rate tracking, and Bifrost upstream integration."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# `freellmapi` — Multi-Provider Free LLM Aggregation Gateway & Bridge (v2.1)

## Activation Contract
Deploying, configuring, or consuming FreeLLMAPI (`tashfeenahmed/freellmapi`), configuring free multi-provider inference pools (Groq, Cerebras, OpenRouter, Ollama), setting up upstream routing for Bifrost, or operating the dual-account quota mesh on Zerops.

## Core Directives & Invariants
- **8-Key Sovereign Mesh**: 8 verified free keys across 2 account layers (Cerebras, Groq, Ollama, OpenRouter). Purge platforms requiring paid credits (HuggingFace, OpenCode Zen, Aisa One).
- **9 Free-Tier Invariants**:
  1. *Provisional Leases*: Reserve estimated token budgets prior to streaming to prevent concurrency collapse.
  2. *4-Tier Cooldowns*: On HTTP 429, escalate cooldowns deterministically (2m $\to$ 10m $\to$ 1h $\to$ 24h) per key.
  3. *Recovery Probes*: Probe cooled providers asynchronously every 60s without stalling incoming inference.
  4. *Account-Level Quotas*: Aggregate rate limits across keys belonging to the same account boundary.
  5. *SQLite WAL & User-Model Guard*: Persist in SQLite WAL mode (`/mnt/localstorage/freellmapi/data/freeapi.db`). Models MUST use `source = 'user'` to prevent deletion during daily remote sync.
  6. *Dynamic Balanced Router*: Thompson-sampling Multi-Armed Bandit (MAB) weighting reliability, speed, and intelligence.
  7. *Bifrost Alias & 404 Shield*: Map consumer models (`qwen-3.8-27b`, `hermes-3-*`) to `auto` via Bifrost aliases.
  8. *Tool-Aware Token Estimation*: Sum serialized `tools` (`estimatedToolsTokens`) to prevent dispatching oversized schemas to low-TPM models.
  9. *Groq 7,000 ITPM Guard*: Enforce `tpm_limit = 7000` (not 70,000) for Groq on-demand models in `models` table.
- **Bifrost Tandem Invariant**: FreeLLMAPI listens on port 3001 as the $0 upstream for Bifrost (`http://freellmapi:3001/v1`). Clients connect through Bifrost (`http://bifrost:8080`).
- **Fail-Fast Anti-Cascade**: Return deterministic 429 errors within $\le$ 2.5s on upstream exhaustion to let Bifrost's 60s circuit breaker trip to Pro Tier without latency spikes.
- **Zerops Env Vault**: Inject credentials via `zerops_env` (`FREEAPI_ADMIN_EMAIL`, `FREEAPI_ADMIN_PASSWORD`, `FREEAPI_CONFIG_JSON_SECRET`) referenced in `zerops.yaml`.

## Decision Gates & References
- **Usage & Client Manual**: [`usage.md`](file:///var/www/zerops-astro-skills/freellmapi/references/usage.md) — Multi-tier architecture, client snippets, and cooldown catalog.
- **Zerops Topology & Storage**: [`infra.md`](file:///var/www/zerops-astro-skills/freellmapi/references/infra.md) — Node.js runtime, persistent volumes, and health probes.
- **Bifrost Tandem Bridge**: [`agy_bifrost_bridge.md`](file:///var/www/zerops-astro-skills/freellmapi/references/agy_bifrost_bridge.md) — Single Front Door upstream patterns.
- **Production Config Template**: [`freellmapi_production_template.json`](file:///var/www/zerops-astro-skills/freellmapi/assets/freellmapi_production_template.json) — 8-key declarative configuration.
- **Validation**: `skills-suite-validate` — Physical test sensor.

## Output Contract
Deterministic OpenAI-compatible responses from `/v1/chat/completions`, active health probe (HTTP 200 on `/api/ping`), and zero orphan daemon processes.
