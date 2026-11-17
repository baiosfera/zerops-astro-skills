---
name: bifrost
description: "Trigger: bifrost, bifrost-cli, maxim ai, ai gateway, llm proxy, llm router, semantic cache, mcp gateway, drop-in openai proxy. High-performance AI gateway with CEL routing, PostgreSQL config/logs store, chromem/qdrant cache, and MCP gateway."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.4"
---

# `bifrost` — Sovereign AI & MCP Gateway (v2.4)

## Activation Contract
Deploying, configuring, or calling Maxim AI Bifrost (`maximhq/bifrost`), configuring zero-cost CEL routing rules, managing PostgreSQL `config_store`/`logs_store`, or running `semantic_cache` (`chromem`/`qdrant`) on Zerops.

## Verified Core Directives & Invariants
1. **Schema Alignment (`config.schema.json`)**:
   - Omit legacy top-level `"version"` (use current v2 schema directly; `"version": 2` selects legacy backwards-compat mode).
   - `retry_backoff_initial` (default `500`, min `100`) and `retry_backoff_max` (default `5000`, min `100`) MUST be **integer milliseconds** (`300`, `1000`), never duration strings (`"300ms"`).
   - `custom_provider_config.allowed_requests`: omitting it enables all operations; a partial object defaults unlisted operations to `false`.
2. **Strict `$0` CEL Routing (Zero Auto-Drain)**:
   - Priority `0` (`rule-explicit-pro-override`): Route to `deepseek` **only** on `headers['x-force-deepseek'] == 'true' || headers['x-routing-tier'] == 'pro' || headers['x-tier'] == 'pro' || headers['x-tier'] == 'production' || model.startsWith('deepseek')`.
   - Priority `1` (`rule-freellm-opt-in-paid-fallback`): Route to `freellmapi` with `fallbacks: ["deepseek"]` **only** when `headers['x-allow-paid-fallback'] == 'true'`.
   - Priority `2` (`rule-freellm-zero-cost-strict`): Catch-all `true` routes strictly to `freellmapi` with `"fallbacks": []`.
   - Note: `circuit_breaker_config` is **Enterprise-only** (top-level); never place it inside `governance` on OSS builds.
3. **Env-Backed Virtual Keys & Encryption**: Declare a single env-backed Virtual Key (`vk-production-main` with `"value": "env.BIFROST_VIRTUAL_KEY"` wired from `${BIFROST_MASTER_VK}`), `"encryption_key": "env.BIFROST_ENCRYPTION_KEY"`, and `governance.auth_config` (`env.BIFROST_ADMIN_USERNAME` / `env.BIFROST_ADMIN_PASSWORD`). Never commit plaintext VKs.
4. **Allow-List & `PG18` Config Store**: Empty `[]` means DENY ALL (`["*"]` allows all). Once `PG18` `config_store` seeds rows (`routing_rules`, `config_keys`), subsequent `config.json` edits must reconcile PG or Governance API; encrypted empty aliases must stay SQL `NULL` (not `'{}'`).
5. **Storage & Semantic Cache**: Persist `config_store` + `logs_store` in PostgreSQL 18. Use `chromem` (single-node embedded with `path`, `compress`, `dimension: 1` for hash cache) or `qdrant` (`port: 6334` gRPC) — never `vector_store.type: redis` against vanilla Valkey 7.2.

## Decision Gates & References
- **Client Drop-in & CEL**: [`usage.md`](file:///var/www/zerops-astro-skills/bifrost/references/usage.md)
- **Zerops Storage & Env**: [`infra.md`](file:///var/www/zerops-astro-skills/bifrost/references/infra.md)
- **Hardened Config Template**: [`config_production_template.json`](file:///var/www/zerops-astro-skills/bifrost/assets/config_production_template.json)
- **Zerops Import Recipe**: [`zerops_bifrost_recipe.yaml`](file:///var/www/zerops-astro-skills/bifrost/assets/zerops_bifrost_recipe.yaml)
- **Validation**: `skills-suite-validate`

## Output Contract
HTTP 200 on `/health` (`db_pings: ok`), zero fatal startup schema errors, and verified `$0` routing on `freellmapi/auto` with `0` unrequested calls to DeepSeek.
