---
name: bun
description: "Trigger: bun, bun.serve, bun.sql, bun.build, bun:test, bunx, runtime bun@1.3.9, elysia, hono, fast http server, typescript nativo. Architect, develop, test, and deploy high-performance TypeScript/JavaScript services on native Bun and Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# Bun — Zerops Native Bun Runtime Engine (v2.0)

## Activation Contract
Activate whenever authoring, building, deploying, or troubleshooting workloads on the Zerops Managed Bun Runtime (`type: bun@1.3.9` or `build.base: bun@...`), choosing between Alpine (`os: alpine`) and Ubuntu (`os: ubuntu`), applying the Bundling Bifurcation Law (`bun build --target bun` vs full deploy), configuring `BUN_INSTALL: ./.bun` build caching, using `Bun.serve`/`Bun.sql`, or running atomic database migrations (`zsc execOnce`).

## Hard Rules
- **Rule 1 (Version Pinning)**: Pin target version in production `zerops.yaml` (e.g. `bun@1.3.9` or `bun@1.2.2`). Avoid unpinned `@latest`.
- **Rule 2 (Bundling Bifurcation Law)**:
  - **Pure JS/TS (Elysia, Hono, Fastify, Astro)**: Execute `bun build src/index.ts --outfile dist/index.js --target bun` and deploy only `./dist` (`deployFiles: [dist]`), producing an ultra-lean ~150KB bundle with zero runtime `node_modules`.
  - **Native C++ Addons (`sharp`, `canvas`, `bcrypt`, `mysql2`)**: Skip bundling. Deploy the full tree (`deployFiles: [./]`) with `start: bun src/index.ts` on `os: ubuntu`.
- **Rule 3 (Build Cache Redirect)**: MUST set `BUN_INSTALL: ./.bun` in `build.envVariables` and cache `node_modules` and `.bun/install/cache`.
- **Rule 4 (CLI Invariant)**: Always execute tool commands using `bunx` instead of `npx`.
- **Rule 5 (Atomic Migrations)**: Execute database migrations in `run.initCommands` using `zsc execOnce ${appVersionId} --retryUntilSuccessful -- bun dist/migrate.js`.
- **Rule 6 (Zero-Guessing Scaling)**: Do NOT author manual `verticalAutoscaling` blocks in `import.yaml`. Zerops manages elastic autoscaling natively.
- **Rule 7 (Fractal CoHaLo Bounded Execution)**: All synchronous commands MUST enforce timeouts (`timeout 10s`), wait limit (`WaitMsBeforeAsync: 10000`), and kill orphan background processes with `manage_task action="kill"`.

## Decision Gates

| Task / Scenario | Recommended Strategy | Reference / Asset |
|---|---|---|
| Pure TS/JS APIs (Elysia, Hono) | `bun build --target bun`, `deployFiles: [dist]`, `os: alpine` | [`references/usage.md`](file:///var/www/.agents/skills/bun/references/usage.md) |
| Native C++ Addons (`sharp`) | Skip bundling, `deployFiles: [./]`, `os: ubuntu` | [`references/usage.md`](file:///var/www/.agents/skills/bun/references/usage.md) |
| Zerops Lifecycle & Cache (`zerops.yaml`) | `BUN_INSTALL: ./.bun`, `deploy.readinessCheck` | [`references/infra.md`](file:///var/www/.agents/skills/bun/references/infra.md) |
| Four-Way Architecture Comparison | Managed Alpine vs Managed Ubuntu vs Generic LXC | [`references/infra.md`](file:///var/www/.agents/skills/bun/references/infra.md) |
| Verified `zerops.yaml` Recipes | Production Elysia Standalone, Sharp C++, and Dev setups | [`assets/bun_production_recipes.json`](file:///var/www/.agents/skills/bun/assets/bun_production_recipes.json) |

## Critical Workflows / Execution Steps
1. Define service topology in `import.yaml` using `type: bun@1.3.9`.
2. Apply the Bundling Bifurcation Law based on dependency type (Pure JS/TS vs Native C++).
3. Set `BUN_INSTALL: ./.bun` in `zerops.yaml` with `.bun/install/cache` in `cache`.
4. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
5. **Circuit Breaker (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500 / timeout) before escalating.
6. **Sensor Attestation**: Verify physical sensor check (exit code 0 / HTTP 200) and format output deterministically.

## Output Contract
- Validated `zerops.yaml` and `import.yaml` targeting Zerops Managed Bun Runtime.
- Verified build and runtime execution with zero orphaned tasks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/bun/references/usage.md) — Developer manual, `Bun.serve`, `Bun.sql`, `bun:sqlite`, `bun:test`, Elysia/Hono patterns, and 5 production recipes.
- [`references/infra.md`](file:///var/www/.agents/skills/bun/references/infra.md) — Infrastructure manual, Incus LXC model, Four-Way comparison matrix, build caching, and CoHaLo process hygiene.
- [`assets/bun_production_recipes.json`](file:///var/www/.agents/skills/bun/assets/bun_production_recipes.json) — Production-ready `zerops.yaml` recipe catalog.
- [`assets/import_template.yaml`](file:///var/www/.agents/skills/bun/assets/import_template.yaml) — Clean `import.yaml` template with native elastic autoscaling.
- [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/bun/assets/zerops_template.yaml) — Dual-setup `zerops.yaml` (Prod & Dev).
- [`scripts/bun-validate.sh`](file:///var/www/.agents/skills/bun/scripts/bun-validate.sh) — Physical integrity validator for the bun skill suite.
