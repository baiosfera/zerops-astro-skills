---
name: freellmapi
description: "Trigger: freellmapi, free-llm-api, freellmapi gateway, multi-provider free llm, free tier inference, groq cerebras router, zerops freellmapi, bifrost freellmapi upstream. Aggregated free LLM proxy with 34+ providers, smart failover, rate tracking, and Bifrost upstream integration."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "1.3"
---

# `freellmapi` — Multi-Provider Free LLM Aggregation Gateway & Bridge (v1.3)

## Activation Contract
Deploying, configuring, or consuming FreeLLMAPI (`tashfeenahmed/freellmapi`), configuring free multi-provider inference pools (Groq, Cerebras, OpenCode, OpenRouter), setting up upstream routing for Bifrost, or registering the `/mcp` server on Zerops.

## Core Directives & Invariants
- **Encrypted Storage & Volume Permissions**: Stored provider keys are AES-256-GCM encrypted in SQLite (`freellmapi.db`). Mount `/app/server/data` to persistent local storage with `chmod -R 777`. Bind `PORT=3001` to `0.0.0.0`.
- **Zerops Env Precedence**: Inject production secrets via `zerops_env` using `FREEAPI_CONFIG_JSON`. Avoid baking dynamic secrets into `run.envVariables` inside `zerops.yaml`, which makes them immutable at service scope.
- **Declarative Admin Seeding**: Declare `admin: { email, password }` in the declarative configuration during headless deployments. FreeLLMAPI seeds this account on first boot (`userCount === 0`), permanently closing the unauthenticated `/api/auth/setup` window.
- **Fail-Fast & Anti-Cascade**: FreeLLMAPI acts as the zero-cost tier for non-transactional prompts behind Bifrost. Enforce fail-fast execution timeouts ($\le$ 2.5s) on upstream free providers. On HTTP 429, return deterministic 429 errors immediately without recursive multi-hop retries to let Bifrost circuit breakers trip to Pro Tier.
- **Monorepo Workspace Isolation**: Isolate the application directory before executing `npm ci` or `zcli push` to avoid `EUNSUPPORTEDPROTOCOL` from parent monorepo workspace references.

## Decision Gates & References
- **Drop-in Clients & CLI Generators**: [`usage.md`](file:///var/www/zerops-astro-skills/freellmapi/references/usage.md) — OpenAI/Python/TS drop-in client patterns and error catalog.
- **Zerops Topology & Lifecycle**: [`infra.md`](file:///var/www/zerops-astro-skills/freellmapi/references/infra.md) — Node.js 22 runtime, persistent mounts, and health probes.
- **Bifrost Upstream & MCP Bridge**: [`agy_bifrost_bridge.md`](file:///var/www/zerops-astro-skills/freellmapi/references/agy_bifrost_bridge.md) — Single Front Door topology and `/mcp` streaming.
- **Production Config Template**: [`freellmapi_production_template.json`](file:///var/www/zerops-astro-skills/freellmapi/assets/freellmapi_production_template.json) — Declarative JSON template.
- **Validation**: [`freellmapi-validate.sh`](file:///var/www/zerops-astro-skills/freellmapi/scripts/freellmapi-validate.sh) — Liveness sensor and token checker.

## Output Contract
Deterministic OpenAI-compatible responses from `/v1/chat/completions`, active health probe (HTTP 200 on `/api/ping`), and zero orphan daemon processes.
