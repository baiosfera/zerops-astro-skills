---
name: freellmapi
description: "Trigger: freellmapi, free-llm-api, freellmapi gateway, multi-provider free llm, free tier inference, groq cerebras router, zerops freellmapi, bifrost freellmapi upstream. Aggregated free LLM proxy with 34+ providers, smart failover, rate tracking, and Bifrost upstream integration."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `freellmapi` — Multi-Provider Free LLM Aggregation Gateway & Bridge (v2.0)

## Activation Contract
Deploying, configuring, or consuming FreeLLMAPI (`tashfeenahmed/freellmapi`), configuring free multi-provider inference pools (Groq, Cerebras, OpenCode, GitHub Models, OpenRouter), setting up upstream routing for Bifrost, or operating the 12-key dual-layer quota pool on Zerops.

## Core Directives & Invariants
- **12-Key Sovereign Dual-Layer Pool**: Coalesce 12 free API keys distributed across 2 independent account layers (6 providers per layer: Groq, Cerebras, OpenCode Zen, GitHub Models, OpenRouter Free, HuggingFace/Ollama) to maximize free concurrency headroom without paying commercial egress.
- **7 Free-Tier Invariants**:
  1. *Provisional Token Leases*: Reserve estimated token budgets prior to streaming to prevent concurrency collapse.
  2. *4-Tier Escalating Cooldowns*: On HTTP 429, escalate cooldowns deterministically (2m $\to$ 10m $\to$ 1h $\to$ 24h) per key.
  3. *Background 60s Recovery Probes*: Probe cooled providers asynchronously every 60s without stalling incoming inference.
  4. *Account-Level Shared Quotas*: Aggregate rate limits across keys belonging to the same account boundary.
  5. *SQLite WAL Persistence*: Persist state in SQLite WAL mode (`/app/server/data/freellmapi.db`) mounted to persistent local storage with `chmod -R 777`.
  6. *Thompson Sampling Bandit Router*: Select providers via multi-armed bandit dynamically weighting latency, quality, and remaining quota.
  7. *Signed Catalog Synchronization*: Validate model metadata against verified provider manifests.
- **Bifrost Tandem Invariant**: FreeLLMAPI listens on port 3001 as the internal $0 upstream for Bifrost (`http://freellmapi:3001/v1`). Clients connect through Bifrost (`http://bifrost:8080`); runtime inference never exposes raw FreeLLMAPI keys publicly.
- **Fail-Fast Anti-Cascade**: Return deterministic 429 errors within $\le$ 2.5s on upstream exhaustion to let Bifrost's 60s circuit breaker trip to Pro Tier without cascading latency spikes.
- **Zerops Env & Login Vault Contract**: Always inject admin credentials via `zerops_env action="set" sensitive=true` using keys `FREEAPI_ADMIN_EMAIL`, `FREEAPI_ADMIN_PASSWORD`, and `FREEAPI_CONFIG_JSON` containing `{ "admin": { "email", "password" } }`. Reference all three in `run.envVariables` in `zerops.yaml` to permanently lock the setup window and guarantee persistent login access.

## Decision Gates & References
- **Drop-in Clients & Quota Manual**: [`usage.md`](file:///var/www/zerops-astro-skills/freellmapi/references/usage.md) — 12-key architecture, client snippets, and cooldown catalog.
- **Zerops Topology & Storage**: [`infra.md`](file:///var/www/zerops-astro-skills/freellmapi/references/infra.md) — Node.js runtime, persistent volumes, and health probes.
- **Bifrost Tandem Bridge**: [`agy_bifrost_bridge.md`](file:///var/www/zerops-astro-skills/freellmapi/references/agy_bifrost_bridge.md) — Single Front Door upstream patterns.
- **Production Config Template**: [`freellmapi_production_template.json`](file:///var/www/zerops-astro-skills/freellmapi/assets/freellmapi_production_template.json) — 12-key declarative configuration.
- **Validation**: `skills-suite-validate` — Physical test sensor.

## Output Contract
Deterministic OpenAI-compatible responses from `/v1/chat/completions`, active health probe (HTTP 200 on `/api/ping` and `/`), and zero orphan daemon processes.
