---
name: fastapi
description: "Trigger: fastapi, fastapi-zerops, pydantic v2, pydantic-settings, pgvector asyncpg, lifespan asynccontextmanager, annotated depends, granian fastapi. High-concurrency FastAPI microservices with Granian Rust ASGI, pgvector HNSW & Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# FastAPI — High-Concurrency Microservices on Zerops (v2.1)

## Activation Contract
Activate whenever developing, structuring, deploying, or tuning FastAPI microservices, Pydantic v2 schemas, Granian Rust ASGI servers, asyncpg connection pools, or `pgvector` HNSW endpoints on Zerops (`python@3.12` / `python@3.11`).

## Hard Rules & Positive Guidance
- **ASGI Production Server**: Deploy with Granian (Rust-based HTTP/1, HTTP/2 & WebSockets server) for maximum concurrency: `granian --interface asgi --host 0.0.0.0 --port 8000 main:app`.
- **Async Lifespan Management**: Use `lifespan` with `asynccontextmanager` to initialize and terminate database connection pools and client sessions.
- **Pydantic v2 Validation**: Use `pydantic-settings` for strongly-typed environment injection. Define schemas with Pydantic v2 `BaseModel` and `field_validator`.
- **Database Connection Pooling**: Connect to PostgreSQL 18 using `asyncpg` pools with explicit min/max connections. Reference connection strings by environment variable name (`$db_connectionString`).
- **Container Execution Boundary**: Run Python framework commands and migrations inside the service container via SSH (`ssh {hostname} "cd /var/www && uv run pytest"`).

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Granian ASGI Deployment | Multi-worker Rust ASGI configuration | [`references/usage.md#granian-asgi`](file:///var/www/.agents/skills/fastapi/references/usage.md) |
| asyncpg + pgvector | Async connection pooling and vector queries | [`references/usage.md#database-vector`](file:///var/www/.agents/skills/fastapi/references/usage.md) |
| zerops.yaml Lifecycle | Prepare, build, and run pipelines with uv | [`references/infra.md#zerops-pipeline`](file:///var/www/.agents/skills/fastapi/references/infra.md) |
| Sizing & Concurrency | Memory limits and worker tuning | [`references/infra.md#sizing-concurrency`](file:///var/www/.agents/skills/fastapi/references/infra.md) |

## Critical Workflows
1. Configure FastAPI service in `zerops.yaml` with Granian entrypoint.
2. Ingest environment variables via Pydantic Settings.
3. Validate service endpoints with physical sensor (`curl -s http://<service>:8000/health`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/fastapi/references/usage.md) — Granian ASGI setup, Pydantic v2, asyncpg pooling, and pgvector integrations.
- [`references/infra.md`](file:///var/www/.agents/skills/fastapi/references/infra.md) — Zerops deployment manifests, uv dependency caching, and concurrency optimization.
