---
name: python
description: "Trigger: python, zerops python, python runtime, os alpine, os ubuntu, uv, granian, uvicorn, alembic, zsc execOnce. Native Python runtime architecture, base selection, vendoring, ASGI servers, and deployment pipelines on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# Python — Zerops Native Python Runtime Engine (v1.0)

## Activation Contract
Activate whenever authoring, building, deploying, or troubleshooting Python services on Zerops (`type: python@3.12`, `type: python@latest`, or `build.base: python@...`), selecting between Alpine (`os: alpine`) and Ubuntu (`os: ubuntu`) bases, configuring package caching (`cache: [vendor]` or `.cache/uv`), configuring ASGI servers (Granian / Uvicorn), authoring atomic Alembic migrations (`zsc execOnce`), or connecting Python services to Zerops PostgreSQL (`asyncpg` / `SQLAlchemy`).

## Hard Rules
- **Rule 1 (Version Pinning Invariant)**: For production services, explicitly pin the target major/minor version (e.g. `python@3.12` or `python@3.11`). Avoid using bare `@latest` in production `zerops.yaml` to prevent upstream breaking changes.
- **Rule 2 (Base OS Selection Invariant)**: Use `os: alpine` (default) for pure Python web apps (FastAPI with asyncpg, Litestar, Flask). Switch to `os: ubuntu` ONLY when utilizing C-extension wheels (numpy, pandas, scipy, torch, opencv, psycopg2-binary, cryptography) to avoid source compilation failures on musl.
- **Rule 3 (Vendoring & PYTHONPATH)**: Install dependencies using `pip install --target=./vendor -r requirements.txt` and set `PYTHONPATH: /var/www/vendor` in `run.envVariables` to match `cache: [vendor]` and `deployFiles: [./vendor]`.
- **Rule 4 (Atomic Migrations)**: Always execute database migrations in `run.initCommands` using `zsc execOnce ${appVersionId} --retryUntilSuccessful -- alembic upgrade head` to prevent race conditions across scaled containers.
- **Rule 5 (Zero-Guessing Scaling)**: Do NOT specify manual `verticalAutoscaling` blocks in `import.yaml`. Zerops manages vertical autoscaling natively out-of-the-box.
- **Rule 6 (Fractal CoHaLo Bounded Execution)**: All synchronous commands MUST enforce timeouts (`timeout 10s`), synchronous wait (`WaitMsBeforeAsync: 10000`), and terminate orphan background processes with `manage_task action="kill"`.

## Decision Gates

| Task / Scenario | Recommended Strategy | Reference / Asset |
|---|---|---|
| Pure Async Web APIs (FastAPI, Litestar) | `os: alpine`, `granian --interface asgi`, `cache: [vendor]` | [`references/usage.md`](file:///var/www/.agents/skills/python/references/usage.md) |
| Data Science & ML (numpy, torch, pandas) | `os: ubuntu`, `prepareCommands: apt-get install -y <pkg>` | [`references/usage.md`](file:///var/www/.agents/skills/python/references/usage.md) |
| Zerops Lifecycle (`zerops.yaml` & Cache) | `cache: [vendor]`, `deploy.readinessCheck`, `zsc execOnce` | [`references/infra.md`](file:///var/www/.agents/skills/python/references/infra.md) |
| Managed vs Generic Ubuntu/Alpine Containers | Comparison of provisioning, toolchains, and maintenance | [`references/infra.md`](file:///var/www/.agents/skills/python/references/infra.md) |
| Verified `zerops.yaml` Recipes | Copy-paste production and development setups | [`assets/python_production_recipes.json`](file:///var/www/.agents/skills/python/assets/python_production_recipes.json) |

## Critical Workflows / Execution Steps
1. Define service topology in `import.yaml` using `type: python@3.12`.
2. Configure `zerops.yaml` with appropriate `os: alpine` or `os: ubuntu` and dependency vendoring.
3. Configure `run.start` with a production ASGI server (Granian or Uvicorn).
4. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
5. **Circuit Breaker (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500 / timeout) before escalating.
6. **Sensor Attestation**: Verify physical sensor check (exit code 0 / HTTP 200) and format output deterministically.

## Output Contract
- Validated `zerops.yaml` and `import.yaml` targeting Zerops Managed Python Runtime.
- Verified build and runtime execution with zero orphaned tasks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/python/references/usage.md) — Developer manual, `os: alpine` vs `os: ubuntu`, ASGI servers (Granian vs Uvicorn), `asyncpg` pooling, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/python/references/infra.md) — Infrastructure manual, Incus LXC model, Managed vs Generic containers, vendor caching, and CoHaLo process hygiene.
- [`assets/python_production_recipes.json`](file:///var/www/.agents/skills/python/assets/python_production_recipes.json) — Production-ready `zerops.yaml` recipe catalog.
- [`scripts/python-validate.sh`](file:///var/www/.agents/skills/python/scripts/python-validate.sh) — Physical integrity validator for the python skill suite.
