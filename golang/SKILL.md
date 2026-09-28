---
name: golang
description: "Trigger: golang, go, zerops go, go runtime, os alpine, os ubuntu, gomodcache, zsc execOnce. Native Go runtime architecture, base selection, GOMODCACHE caching, and deployment pipelines on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# Golang — Zerops Native Go Runtime Engine (v1.0)

## Activation Contract
Activate whenever authoring, building, deploying, or troubleshooting Go services on Zerops (`type: go@1.22`, `type: golang@latest`, or `build.base: go@...`), selecting between Alpine (`os: alpine`) and Ubuntu (`os: ubuntu`) bases, configuring `GOMODCACHE` snapshotting (`cache: true`), authoring atomic migrations (`zsc execOnce`), or connecting Go services to Zerops PostgreSQL (`pgx/v5`).

## Hard Rules
- **Rule 1 (Base OS Selection Invariant)**: Use `os: alpine` (default) with `CGO_ENABLED="0"` for 95% of standard web APIs and microservices. Switch to `os: ubuntu` ONLY when dynamic CGO bindings (`libvips`, `librdkafka`, `sqlite3` CGO) are strictly required.
- **Rule 2 (Minimal Deploy Artifacts)**: Production services MUST deploy compiled binaries only (`deployFiles: [./app, ./migrate]`). Never deploy full source code to production runtimes.
- **Rule 3 (Atomic Migrations)**: Always execute database migrations in `run.initCommands` using `zsc execOnce ${appVersionId} -- ./migrate` to prevent parallel execution race conditions across scaled containers.
- **Rule 4 (Zero-Guessing Scaling)**: Do NOT specify manual `verticalAutoscaling` blocks in `import.yaml`. Zerops manages vertical autoscaling natively out-of-the-box.
- **Rule 5 (Fractal CoHaLo Bounded Execution)**: All synchronous commands MUST enforce timeouts (`timeout 10s`), synchronous wait (`WaitMsBeforeAsync: 10000`), and terminate orphan background processes with `manage_task action="kill"`.

## Decision Gates

| Task / Scenario | Recommended Strategy | Reference / Asset |
|---|---|---|
| Pure Go APIs (`pgx`, `chi`, `nats`, `redis`) | `os: alpine`, `CGO_ENABLED: "0"`, `deployFiles: ./app` | [`references/usage.md`](file:///var/www/.agents/skills/golang/references/usage.md) |
| CGO Services (`libvips`, `librdkafka`) | `os: ubuntu`, `prepareCommands: apt-get install -y <pkg>` | [`references/usage.md`](file:///var/www/.agents/skills/golang/references/usage.md) |
| Zerops Lifecycle (`zerops.yaml` & Cache) | `cache: true` for `GOMODCACHE`, `deploy.readinessCheck` | [`references/infra.md`](file:///var/www/.agents/skills/golang/references/infra.md) |
| Development Workspaces | `deployFiles: ./`, `start: zsc noop --silent` | [`references/infra.md`](file:///var/www/.agents/skills/golang/references/infra.md) |
| Verified `zerops.yaml` Recipes | Copy-paste production and development setups | [`assets/go_production_recipes.json`](file:///var/www/.agents/skills/golang/assets/go_production_recipes.json) |

## Critical Workflows / Execution Steps
1. Define service topology in `import.yaml` using `type: go@1.22` or `type: golang@latest`.
2. Configure `zerops.yaml` with appropriate `os: alpine` or `os: ubuntu` and `cache: true`.
3. Author `deployFiles` to transfer only `./app` and `./migrate` to the run container.
4. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
5. **Circuit Breaker (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500 / timeout) before escalating.
6. **Sensor Attestation**: Verify physical sensor check (exit code 0 / HTTP 200) and format output deterministically.

## Output Contract
- Validated `zerops.yaml` and `import.yaml` targeting Zerops Managed Go Runtime.
- Verified build and compilation artifacts with zero orphaned tasks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/golang/references/usage.md) — Developer manual, `os: alpine` vs `os: ubuntu`, connection pooling (`pgx/v5`), and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/golang/references/infra.md) — Infrastructure manual, Incus LXC model, `GOMODCACHE` caching, atomic migrations, and CoHaLo process hygiene.
- [`assets/go_production_recipes.json`](file:///var/www/.agents/skills/golang/assets/go_production_recipes.json) — Production-ready `zerops.yaml` recipe catalog.
- [`scripts/golang-validate.sh`](file:///var/www/.agents/skills/golang/scripts/golang-validate.sh) — Physical integrity validator for the golang skill suite.
