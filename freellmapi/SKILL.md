---
name: freellmapi
description: "Trigger: freellmapi, free-llm-api, freellmapi gateway, multi-provider free llm, free tier inference, groq cerebras router, zerops freellmapi, bifrost freellmapi upstream. Aggregated free LLM proxy with smart bandit routing, cooldown escalation, keyless providers, and Bifrost upstream integration."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "2.2"
---

# `freellmapi` — Multi-Provider Free LLM Aggregation Gateway (v2.2)

## Activation Contract
Deploying, configuring, or consuming FreeLLMAPI (`tashfeenahmed/freellmapi`), provisioning multi-provider free pools (`cerebras`, `groq`, `ollama`, `openrouter` + built-in keyless `kilo`, `ovh`), or wiring FreeLLMAPI behind Bifrost on Zerops.

## Verified Core Directives & Invariants
1. **Declarative Env Precedence (`declarative-config.ts`)**: `FREEAPI_CONFIG_JSON` (`${FREEAPI_CONFIG_JSON_SECRET}`) takes strict precedence over `FREEAPI_CONFIG_PATH`. The schema uses Zod `.strict()` — only `admin`, `unifiedApiKey`, `license`, `keys`, `customProviders`, `models`, `fallback`, and `routing` are valid top-level keys.
2. **Built-In Keyless vs Keyed Pools (`providers/index.ts`)**: Built-in `keyless: true` platforms (`kilo`, `ovh`, `aihorde`) omit the `Authorization` header and require only `{ "platform": "kilo" }`. Conversely, `customProviders` entries require a non-empty `apiKey` (e.g., `"ollama"`).
3. **Bandit Routing & `least-remaining` (`01-routing-and-bandit-scoring.md`)**:
   - Chain priority: active profile (`profile_models`) $\to$ global `fallback_config` $\to$ sort alias (`auto:smart`, `auto:fast`, `auto:reliable`, `auto:balanced`) $\to$ named profile (`auto:<name>`).
   - Configure `routing.strategy: "smartest"` (`0.35 rel / 0.10 spd / 0.55 int`) and `routing.keySelectionStrategy: "least-remaining"`.
4. **Catalog Hygiene & Cooldown Engine**:
   - Disable safety-classifier/broken models (`openai/gpt-oss-safeguard-20b`, `allam-2-7b`, `meta-llama/llama-prompt-guard-*`, `ovh/Qwen3Guard-Gen-*`, `nvidia/*guard*`) and avoid inventing `tpmLimit` values (`learnLimitFromError()` automatically tightens real upstream caps; set `openai/gpt-oss-120b` `tpmLimit: 8000`).
   - Transient `429` cools down `90s`, then escalates (`2m` $\to$ `10m` $\to$ `1h` $\to$ `1d`); `402`/`403` cool down `24h`. Only `heuristic` cooldowns are cleared by the 60s background probe.
5. **Strict `$0` Upstream Behind Bifrost**: Serve on `http://freellmapi:3001` (`ubuntu/nodejs@24`, SQLite WAL at `/mnt/localstorage/freellmapi/data/freeapi.db`). Never force escalation to commercial Pro providers unless the caller explicitly opts in.
6. **Zerops Secret Seeding**: Provision keys idempotently via `scripts/seed-freellmapi-keys.sh` + `vault_env.py`. Keep `FREEAPI_CONFIG_JSON_SECRET` and `FREEAPI_ENCRYPTION_KEY` strictly service-scoped (`serviceHostname: "freellmapi"`, `sensitive: true`)—never in Project Shared Vault (`project: true`), where Zerops replicates every project variable across all services and build containers into `zcp`'s saved settings. Share only `FREELLMAPI_CLIENT_KEY` at project scope and never commit raw keys.

## Decision Gates & References
- **Client Wire & Routing**: [`usage.md`](file:///var/www/zerops-astro-skills/freellmapi/references/usage.md)
- **Zerops Storage & Env**: [`infra.md`](file:///var/www/zerops-astro-skills/freellmapi/references/infra.md)
- **Bifrost Bridge**: [`agy_bifrost_bridge.md`](file:///var/www/zerops-astro-skills/freellmapi/references/agy_bifrost_bridge.md)
- **Valid Declarative Template**: [`freellmapi_production_template.json`](file:///var/www/zerops-astro-skills/freellmapi/assets/freellmapi_production_template.json)
- **Validation**: `skills-suite-validate`

## Output Contract
HTTP 200 on `/api/ping`, `/v1/models?available=true` listing clean healthy models (0 guard/broken models), and zero plaintext keys in git.
