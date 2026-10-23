---
name: python
description: "Trigger: python, zerops python, python runtime, os alpine, os ubuntu, uv, granian, uvicorn, alembic, zsc execOnce. Native Python runtime architecture, base selection, vendoring, ASGI servers, and deployment pipelines on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# Python — Zerops Native Python Runtime Engine (v1.1)

## Activation Contract
Activate whenever architecting, configuring, caching, or deploying Python services (`runtime: ubuntu/python@3.12` or `alpine/python@3.12`), ASGI application servers, Alembic database migrations, or package management via `uv` or `pip` on Zerops.

## Hard Rules & Positive Guidance
- **Runtime Base Selection**:
  - `ubuntu/python@3.12`: Default for scientific computing, AI inference, C-extensions, and wheels requiring glibc.
  - `alpine/python@3.12`: Preferred for lightweight pure-Python microservices without native compilation.
- **Modern Package Management**: Use `uv` for lightning-fast dependency resolution and virtualenv management in build pipelines.
- **Build Caching**: Cache `~/.cache/uv` or `~/.cache/pip` in `zerops.yaml` to ensure fast subsequent builds.
- **Execution Boundary**: Run testing and migrations inside the runtime container via SSH (`ssh {hostname} "cd /var/www && pytest"`).
- **Process Supervision**: Run ASGI/WSGI servers in the foreground; do not background processes in `run.start`.

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Package Management | uv vs pip virtualenv workflows | [`references/usage.md#package-management`](file:///var/www/.agents/skills/python/references/usage.md) |
| ASGI/WSGI Servers | Granian, Uvicorn, Gunicorn selection | [`references/usage.md#server-selection`](file:///var/www/.agents/skills/python/references/usage.md) |
| zerops.yaml Configuration | Multi-stage build pipelines and caching | [`references/infra.md#zerops-pipeline`](file:///var/www/.agents/skills/python/references/infra.md) |
| Ubuntu vs Alpine Matrix | Base OS trade-offs and native libraries | [`references/infra.md#base-os`](file:///var/www/.agents/skills/python/references/infra.md) |

## Critical Workflows
1. Define Python runtime in `zerops.yaml` with explicit base image and version.
2. Install dependencies via `uv pip install -r requirements.txt` during `build`.
3. Launch server on `0.0.0.0` and verify with health check probe.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/python/references/usage.md) — uv workflows, ASGI server architectures, Alembic migrations, and virtual environments.
- [`references/infra.md`](file:///var/www/.agents/skills/python/references/infra.md) — Deployment pipelines on Zerops, dependency caching, base OS matrix, and process hygiene.
