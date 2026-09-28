---
name: fastapi
description: "Trigger: fastapi, fastapi-zerops, pydantic v2, pydantic-settings, pgvector asyncpg, lifespan asynccontextmanager, annotated depends, granian fastapi, nats-py, valkey python. High-concurrency FastAPI microservices with Granian Rust ASGI, pgvector HNSW, NATS JetStream & Valkey in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `fastapi` — High-Concurrency Microservices & AI Engine on Zerops (v2.0)

## Activation Contract
Activate when architecting, building, optimizing, or deploying asynchronous REST APIs, semantic vector search endpoints (`pgvector`), AI inference/scoring services, or background processing pipelines with FastAPI (0.115+) on native Zerops Incus LXC containers (`python@3.12`, `python@3.14`).

## Hard Rules
- **Lifespan Exclusivity**: Never use deprecated `@app.on_event("startup")` or `@app.on_event("shutdown")`. All pool (`asyncpg`), cache (`redis.asyncio`), and NATS client lifecycles MUST be managed in `@asynccontextmanager lifespan(app: FastAPI)`.
- **Binary Vector Codec**: PostgreSQL pools with `pgvector` MUST register binary codecs via `await register_vector(conn)` in pool init.
- **Non-Blocking AI Inference**: Synchronous ML models (Scikit-Learn, XGBoost) MUST execute within `await asyncio.to_thread(_run_inference)` to prevent blocking the ASGI loop.
- **Dependency Typing (PEP 593)**: All dependency injections MUST use `Annotated[T, Depends(func)]`.
- **Pydantic v2 Settings**: Environment variables MUST be managed via `pydantic-settings` with `@lru_cache(maxsize=1)`.
- **Fractal CoHaLo**: Enforce strict hygiene (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans (`manage_task action="kill"`), sensor (healthz probe).
- **Zero Deletion**: Consult [`references/usage.md`](file:///var/www/.agents/skills/fastapi/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/fastapi/references/infra.md) for full lossless APIs.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 4D Matrix & ASGI Servers | Granian (Rust) vs Uvicorn, Gunicorn, Flask/Django | [`references/usage.md#1-4d-comparative-architectural-matrix-python-asgi-servers--frameworks`](file:///var/www/.agents/skills/fastapi/references/usage.md) |
| Lifespan Management | Initialize asyncpg, pgvector, Valkey, and NATS | [`references/usage.md#2-lifespan-lifecycle-management-with-asynccontextmanager`](file:///var/www/.agents/skills/fastapi/references/usage.md) |
| Modern DI (PEP 593) | Type-safe pool and connection injection with auto-release | [`references/usage.md#3-modern-dependency-injection-annotated-depends`](file:///var/www/.agents/skills/fastapi/references/usage.md) |
| pgvector Semantic Search | HNSW index creation and cosine similarity search | [`references/usage.md#4-semantic-vector-search-with-pgvector--hnsw-indexing`](file:///var/www/.agents/skills/fastapi/references/usage.md) |
| Non-Blocking AI Endpoints | Churn & Lead Scoring inference via asyncio.to_thread | [`references/usage.md#6-non-blocking-ai-endpoints-lead-scoring--churn-prediction`](file:///var/www/.agents/skills/fastapi/references/usage.md) |
| Incus LXC Topology | Granian, PostgreSQL 18, Valkey 7.2, and NATS setup | [`references/infra.md#1-multi-service-microservice-topology-in-zerops`](file:///var/www/.agents/skills/fastapi/references/infra.md) |
| zerops.yaml Configuration | Astral uv fast package installation & Granian launcher | [`references/infra.md#3-canonical-lifecycle-recipe-zeropsyaml`](file:///var/www/.agents/skills/fastapi/references/infra.md) |
| FastAPI App Template | Canonical modular FastAPI application template | [`assets/fastapi_app_template.py`](file:///var/www/.agents/skills/fastapi/assets/fastapi_app_template.py) |
| Production Recipes JSON | Lifespan and Granian launcher recipes | [`assets/fastapi_production_recipes.json`](file:///var/www/.agents/skills/fastapi/assets/fastapi_production_recipes.json) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/fastapi-validate.sh`](file:///var/www/.agents/skills/fastapi/scripts/fastapi-validate.sh) |

## Execution Steps
1. Verify database and cache connection variables in Zerops environment.
2. Build FastAPI microservice using Astral `uv` in `zerops.yaml`.
3. Launch with Granian ASGI server on port `8000`.
4. Register `pgvector` codecs and Valkey clients in Lifespan.
5. Verify `/healthz` endpoint via physical sensor check.

## Output Contract
- High-concurrency FastAPI microservice running under Granian (Rust ASGI) in Zerops.
- Non-blocking ML inference, sub-millisecond vector search, and passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/fastapi/references/usage.md) — 4D matrix, Lifespan, asyncpg + pgvector HNSW, DI, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/fastapi/references/infra.md) — Incus LXC topology, Granian flags, zerops.yaml, and CoHaLo harness.
- [`assets/fastapi_production_recipes.json`](file:///var/www/.agents/skills/fastapi/assets/fastapi_production_recipes.json) — Production lifespan and launcher recipes.
- [`assets/fastapi_app_template.py`](file:///var/www/.agents/skills/fastapi/assets/fastapi_app_template.py) — Modular FastAPI application template.
- [`assets/pgvector_search_template.py`](file:///var/www/.agents/skills/fastapi/assets/pgvector_search_template.py) — High-speed semantic vector search module.
- [`assets/churn_scoring_template.py`](file:///var/www/.agents/skills/fastapi/assets/churn_scoring_template.py) — Non-blocking AI scoring endpoint.
- [`assets/zerops_fastapi_template.yaml`](file:///var/www/.agents/skills/fastapi/assets/zerops_fastapi_template.yaml) — Optimized zerops.yaml for Granian & uv.
- [`scripts/fastapi-validate.sh`](file:///var/www/.agents/skills/fastapi/scripts/fastapi-validate.sh) — Deterministic quality & token validation sensor.
