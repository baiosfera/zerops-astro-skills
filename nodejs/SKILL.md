---
name: nodejs
description: "Trigger: nodejs, node, nodejs@24, nodejs@22, type stripping, node:test, node:sqlite, fastify, express, nestjs, zerops nodejs runtime. Architect, develop, test, and deploy high-performance TypeScript/JavaScript services on native Node.js and Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# Node.js — Zerops Native Node.js Runtime Engine (v2.0)

## Activation Contract
Activate whenever authoring, building, deploying, or troubleshooting Node.js services on Zerops (`type: nodejs@22`, `type: nodejs@24`, or `build.base: nodejs@...`), selecting between Alpine (`os: alpine`) and Ubuntu (`os: ubuntu`) bases, configuring `npm_config_cache` build caching, compiling C++ native addons via `node-gyp`, executing native TypeScript type stripping (`--experimental-strip-types`), or authoring atomic database migrations (`zsc execOnce`).

## Hard Rules
- **Rule 1 (Version Pinning Invariant)**: For production services, explicitly pin the target LTS version (e.g. `nodejs@22` or `nodejs@24`). Avoid using bare `@latest` in production `zerops.yaml` to prevent unexpected upstream breaking changes.
- **Rule 2 (Base OS Selection Invariant)**: Use `os: alpine` (default) for 95% of standard web applications (Fastify, Express, NestJS, Astro, Remix, Hono). Switch to `os: ubuntu` ONLY when native C++ addons (`sharp`, `canvas`, `bcrypt`, `better-sqlite3`, `libvips-dev`) require `glibc` compilation via `node-gyp`.
- **Rule 3 (Build Cache & Production Prune)**: Set `npm_config_cache: .npm-cache` in `build.envVariables` and cache `node_modules` and `.npm-cache`. Always run `npm prune --omit=dev` before packaging to ensure only production dependencies enter `deployFiles`.
- **Rule 4 (Atomic Migrations)**: Always execute database migrations in `run.initCommands` using `zsc execOnce ${appVersionId} --retryUntilSuccessful -- node dist/migrate.js` to prevent parallel execution race conditions across scaled containers.
- **Rule 5 (Zero-Guessing Scaling)**: Do NOT specify manual `verticalAutoscaling` blocks in `import.yaml`. Zerops manages vertical autoscaling natively out-of-the-box.
- **Rule 6 (Fractal CoHaLo Bounded Execution)**: All synchronous commands MUST enforce timeouts (`timeout 10s`), synchronous wait (`WaitMsBeforeAsync: 10000`), and terminate orphan background processes with `manage_task action="kill"`.

## Decision Gates

| Task / Scenario | Recommended Strategy | Reference / Asset |
|---|---|---|
| Pure TypeScript/JS Web APIs (Fastify, Express) | `os: alpine`, `npm ci`, `npm prune --omit=dev` | [`references/usage.md`](file:///var/www/.agents/skills/nodejs/references/usage.md) |
| C++ Native Addons (`sharp`, `node-gyp`) | `os: ubuntu`, `prepareCommands: apt-get install -y build-essential` | [`references/usage.md`](file:///var/www/.agents/skills/nodejs/references/usage.md) |
| Zerops Lifecycle (`zerops.yaml` & Cache) | `npm_config_cache: .npm-cache`, `deploy.readinessCheck` | [`references/infra.md`](file:///var/www/.agents/skills/nodejs/references/infra.md) |
| Four-Way Architecture Comparison | Managed Alpine vs Managed Ubuntu vs Generic LXC | [`references/infra.md`](file:///var/www/.agents/skills/nodejs/references/infra.md) |
| Verified `zerops.yaml` Recipes | Production Fastify, NestJS, Sharp, and Dev setups | [`assets/nodejs_production_recipes.json`](file:///var/www/.agents/skills/nodejs/assets/nodejs_production_recipes.json) |

## Critical Workflows / Execution Steps
1. Define service topology in `import.yaml` using `type: nodejs@22` or `type: nodejs@24`.
2. Configure `zerops.yaml` with appropriate `os: alpine` or `os: ubuntu` and `npm_config_cache`.
3. Author `deployFiles` to transfer only `./dist`, `./node_modules`, and `./package.json` to the run container.
4. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
5. **Circuit Breaker (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500 / timeout) before escalating.
6. **Sensor Attestation**: Verify physical sensor check (exit code 0 / HTTP 200) and format output deterministically.

## Output Contract
- Validated `zerops.yaml` and `import.yaml` targeting Zerops Managed Node.js Runtime.
- Verified build and runtime execution with zero orphaned tasks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/nodejs/references/usage.md) — Developer manual, `node:sqlite`, `node:test`, Type Stripping, Fastify/NestJS patterns, and 5 production recipes.
- [`references/infra.md`](file:///var/www/.agents/skills/nodejs/references/infra.md) — Infrastructure manual, Incus LXC model, Four-Way comparison matrix, build caching, and CoHaLo process hygiene.
- [`assets/nodejs_production_recipes.json`](file:///var/www/.agents/skills/nodejs/assets/nodejs_production_recipes.json) — Production-ready `zerops.yaml` recipe catalog.
- [`assets/import_template.yaml`](file:///var/www/.agents/skills/nodejs/assets/import_template.yaml) — Clean `import.yaml` template with native elastic autoscaling.
- [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/nodejs/assets/zerops_template.yaml) — Dual-setup `zerops.yaml` (Prod & Dev).
- [`scripts/nodejs-validate.sh`](file:///var/www/.agents/skills/nodejs/scripts/nodejs-validate.sh) — Physical integrity validator for the nodejs skill suite.
