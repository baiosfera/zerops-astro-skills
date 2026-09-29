---
name: "freellmapi"
description: "Trigger: freellmapi, free-llm-api, freellmapi gateway, multi-provider free llm, free tier inference, groq cerebras router, zerops freellmapi, bifrost freellmapi upstream. Aggregated free LLM proxy with 34+ providers, smart failover, rate tracking, and Bifrost upstream integration."
license: "MIT"
metadata:
  author: "gentleman-programming"
  version: "1.2"
---

# FreeLLMAPI — Multi-Provider Free LLM Aggregation Gateway & Bridge (v1.2)

## Activation Contract
Activate whenever deploying, configuring, or consuming FreeLLMAPI (`tashfeenahmed/freellmapi`), configuring free multi-provider inference pools (Groq, Cerebras, OpenCode, OpenRouter, HuggingFace, Ollama, Aisa), setting up FreeLLMAPI as an upstream provider for [`bifrost`](file:///var/www/.agents/skills/bifrost/SKILL.md), registering the `/mcp` server, or deploying on Zerops.

## Hard Rules
- **Rule 1 (Zero Deletion & High-Fidelity Invariant)**: Preserve complete method signatures, API endpoints, and provider mappings in full fidelity. Consult [`references/usage.md`](references/usage.md), [`references/infra.md`](references/infra.md), and [`references/agy_bifrost_bridge.md`](references/agy_bifrost_bridge.md) for complete exegesis.
- **Rule 2 (Encrypted Key & Zero-Loss Invariant)**: Stored provider keys are AES-256-GCM encrypted in SQLite (`freellmapi.db`). Execute `npm run rotate-encryption-key` prior to modifying `ENCRYPTION_KEY` to ensure seamless credential migration. Bind `PORT=3001` to `0.0.0.0` for inter-service container networking.
- **Rule 3 (Fractal CoHaLo Bounded Execution)**: Enforce execution timeouts (`timeout 10s`), `WaitMsBeforeAsync: 10000`, circuit breakers (maximum 2 retries on 5xx/timeout), and purge background tasks with `manage_task action="kill"`.
- **Rule 4 (Zerops Env Precedence & Secret Immutability)**: Inject production secrets via `zerops_env` using `FREEAPI_CONFIG_JSON`. Never declare dynamic secrets or provider keys in `run.envVariables` inside `zerops.yaml`, as yaml-baked keys become immutable at service scope and cannot be updated dynamically via platform tooling.
- **Rule 5 (Declarative Admin & Unauthenticated Setup Cloaking)**: When deploying headlessly or in automated blueprints, declare `admin: { email, password }` in the declarative configuration. FreeLLMAPI boots and seeds this account on first run (`userCount === 0`), permanently closing the unauthenticated `/api/auth/setup` window. Subsequent boots preserve the existing account and safely skip the block.
- **Rule 6 (Monorepo Workspace Isolation)**: When deploying FreeLLMAPI from a monorepo root, isolate the application directory before executing `npm ci` or `zcli push`. Scanning monorepo workspace references (e.g. `workspace:*`) causes npm to fail with `EUNSUPPORTEDPROTOCOL`. Purge container-side `.git` directories before packaging to prevent zcli archive failures.

## Decision Gates

| Use Case / Scenario | Action / Recommended Pattern | Primary Reference |
|---|---|---|
| OpenAI / Python / TypeScript Drop-in Client | Point `base_url` to `http://localhost:3001/v1` with unified token | [`references/usage.md`](file:///var/www/.agents/skills/freellmapi/references/usage.md#4-production-patterns--verified-code-recipes) |
| Coding Agent Auto-Setup | Run `npx freellmapi setup-*` or zero-persistence `launch` | [`references/usage.md`](file:///var/www/.agents/skills/freellmapi/references/usage.md#pattern-4-agent--tool-one-command-auto-configuration) |
| Bifrost Upstream Provider Integration | Register `freellmapi` in Bifrost `config.json` with fallback routing | [`references/agy_bifrost_bridge.md`](file:///var/www/.agents/skills/freellmapi/references/agy_bifrost_bridge.md#2-bifrost-configuration-for-freellmapi-upstream) |
| Model Context Protocol (MCP) Bridge | Register `/mcp` endpoint via HTTP/SSE | [`references/agy_bifrost_bridge.md`](file:///var/www/.agents/skills/freellmapi/references/agy_bifrost_bridge.md#method-a-model-context-protocol-mcp-server-registration) |
| Production Container Deploy on Zerops | Deploy on Node.js 22 or Docker VM with persistent `/app/server/data` | [`references/infra.md`](file:///var/www/.agents/skills/freellmapi/references/infra.md#4-lifecycle-commands--manifest-zeropsyaml) |
| Declarative Boot & Secret Synchronization | Apply `FREEAPI_CONFIG_JSON` seeded from ecosystem credentials | [`assets/freellmapi_production_template.json`](file:///var/www/.agents/skills/freellmapi/assets/freellmapi_production_template.json) |

## Critical Workflows / Execution Steps
1. **Validation & Discovery**: Check `freellmapi.db` volume permissions (`chmod -R 777`) and verify `ENCRYPTION_KEY` presence.
2. **Process Hygiene**: Probe server readiness with bounded timeout: `timeout 10s curl -s -f http://localhost:3001/api/ping`.
3. **Bifrost Wiring**: Ensure Bifrost `config.json` points to `http://freellmapi:3001/v1` with valid Virtual Key bindings.
4. **Sensor Attestation**: Verify liveness probe returns HTTP 200 and test inference carries `x-routed-via` header.

## Output Contract
- Deterministic response or OpenAI-compatible JSON payload from `/v1/chat/completions`.
- Active health probe metric (HTTP 200 on `/api/ping`) and zero orphan daemon processes.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/freellmapi/references/usage.md) — Full method matrix, 5 verified code recipes, CLI agent generators, and error catalog.
- [`references/infra.md`](file:///var/www/.agents/skills/freellmapi/references/infra.md) — Zerops manifest (`zerops.yaml`), `.env` dictionary, storage safeguards, and CoHaLo process hygiene.
- [`references/agy_bifrost_bridge.md`](file:///var/www/.agents/skills/freellmapi/references/agy_bifrost_bridge.md) — Single Front Door topology guide for Bifrost gateway and FreeLLMAPI upstream.
- [`assets/freellmapi_production_template.json`](file:///var/www/.agents/skills/freellmapi/assets/freellmapi_production_template.json) — Production declarative configuration template.
- [`assets/zerops_freellmapi_recipe.yaml`](file:///var/www/.agents/skills/freellmapi/assets/zerops_freellmapi_recipe.yaml) — Standalone Zerops import recipe.
- [`scripts/freellmapi-validate.sh`](file:///var/www/.agents/skills/freellmapi/scripts/freellmapi-validate.sh) — Deterministic physical sensor validation script.
