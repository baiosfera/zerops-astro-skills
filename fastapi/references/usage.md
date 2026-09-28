# FastAPI Microservices, Granian ASGI & AI Ingestion Engine Manual (v2.0)

`fastapi` is the sovereign high-concurrency microservice, semantic vector search, non-blocking AI inference, and real-time streaming engine for the Zerops stack. Executing on native **Zerops Incus LXC containers (`python@3.12`, `python@3.14`)** powered by **Granian (Rust ASGI server)** and **Astral `uv`**, it achieves sub-millisecond baseline latencies with zero event loop blocking.

---

## 1. 4D Comparative Architectural Matrix: Python ASGI Servers & Frameworks

| Framework / Server | Core Engine | Baseline Throughput (RPS) | Memory Footprint (Base) | Zerops Suitability |
|---|---|---|---|---|
| **FastAPI + Granian (Target)** | **Python + Rust (uvloop)** | **~75,000+ RPS** | **~45 MB RAM** | **SSoT for High Concurrency** |
| **FastAPI + Uvicorn Standard** | Python + Cython (uvloop) | ~45,000 RPS | ~65 MB RAM | Standard reliable runner |
| **FastAPI + Gunicorn + Uvicorn**| Python Multi-Process | ~50,000 RPS | ~120 MB RAM | Traditional enterprise worker |
| **Flask / Django WSGI** | Synchronous Python | ~8,000 RPS | ~90 MB RAM | Unsuitable for async/vector search |

---

## 2. Lifespan Lifecycle Management with `@asynccontextmanager`

In FastAPI 0.115+, the unified ASGI Lifespan protocol replaces legacy `@app.on_event("startup")` and `@app.on_event("shutdown")`:

```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncpg
import joblib
from fastapi import FastAPI
from pgvector.asyncpg import register_vector
import redis.asyncio as aioredis
from nats.aio.client import Client as NATS

from app.core.config import get_settings

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()
    
    # 1. STARTUP: PostgreSQL asyncpg Pool with pgvector binary codec
    async def init_connection(conn: asyncpg.Connection) -> None:
        await register_vector(conn)

    app.state.pg_pool = await asyncpg.create_pool(
        dsn=settings.DATABASE_URL.get_secret_value(),
        min_size=settings.DB_POOL_MIN_SIZE,
        max_size=settings.DB_POOL_MAX_SIZE,
        max_queries=50_000,
        max_inactive_connection_lifetime=300.0,
        command_timeout=30.0,
        init=init_connection,
    )

    # 2. STARTUP: Valkey In-Memory Cache Connection
    app.state.redis = aioredis.from_url(
        f"redis://{settings.VALKEY_HOST}:{settings.VALKEY_PORT}",
        decode_responses=True
    )

    # 3. STARTUP: NATS Client Connection
    try:
        app.state.nats = NATS()
        await app.state.nats.connect(servers=[settings.NATS_URL])
    except Exception as e:
        app.state.nats = None

    # 4. STARTUP: Load Predictive ML Models into Memory
    try:
        app.state.churn_classifier = joblib.load(settings.CHURN_MODEL_PATH)
    except Exception:
        app.state.churn_classifier = None

    yield  # --- APPLICATION SERVING TRAFFIC ---

    # 5. SHUTDOWN: Graceful teardown of connections and sockets
    if getattr(app.state, "pg_pool", None):
        await app.state.pg_pool.close()
    if getattr(app.state, "redis", None):
        await app.state.redis.aclose()
    if getattr(app.state, "nats", None):
        await app.state.nats.drain()
```

---

## 3. Modern Dependency Injection: `Annotated[..., Depends(...)]`

```python
from typing import Annotated, AsyncGenerator
import asyncpg
from fastapi import Depends, Request, HTTPException, status

def get_db_pool(request: Request) -> asyncpg.Pool:
    pool: asyncpg.Pool = getattr(request.app.state, "pg_pool", None)
    if pool is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection pool is not initialized"
        )
    return pool

DbPool = Annotated[asyncpg.Pool, Depends(get_db_pool)]

async def get_db_connection(pool: DbPool) -> AsyncGenerator[asyncpg.Connection, None]:
    async with pool.acquire() as connection:
        yield connection

DbConnection = Annotated[asyncpg.Connection, Depends(get_db_connection)]
```

---

## 4. Semantic Vector Search with `pgvector` & HNSW Indexing

### PostgreSQL 18 Schema DDL:
```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS customer_embeddings (
    customer_id VARCHAR(64) PRIMARY KEY,
    features_vector vector(1536) NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    updated_at TIMESTAMPTZ DEFAULT clock_timestamp()
);

-- HNSW Cosine Index for ultra-fast vector search
CREATE INDEX IF NOT EXISTS idx_customer_embeddings_hnsw_cosine
ON customer_embeddings
USING hnsw (features_vector vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

### Asynchronous Vector Search Function:
```python
from pgvector import Vector
import asyncpg

async def search_similar_customers(
    conn: asyncpg.Connection,
    query_embedding: list[float],
    top_k: int = 10,
    similarity_threshold: float = 0.75
) -> list[dict]:
    vec = Vector(query_embedding)
    query = """
        SELECT 
            customer_id,
            metadata,
            1 - (features_vector <=> $1) AS cosine_similarity
        FROM customer_embeddings
        WHERE 1 - (features_vector <=> $1) >= $2
        ORDER BY features_vector <=> $1 ASC
        LIMIT $3;
    """
    rows = await conn.fetch(query, vec, similarity_threshold, top_k)
    return [dict(row) for row in rows]
```

---

## 5. Immutable Configuration with `pydantic-settings` (Pydantic v2)

```python
from functools import lru_cache
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    ENVIRONMENT: str = Field(default="production", alias="ENVIRONMENT")
    DATABASE_URL: SecretStr = Field(..., alias="DATABASE_URL")
    VALKEY_HOST: str = Field(default="cache", alias="VALKEY_HOST")
    VALKEY_PORT: int = Field(default=6379, alias="VALKEY_PORT")
    NATS_URL: str = Field(default="nats://nats:4222", alias="NATS_URL")
    
    DB_POOL_MIN_SIZE: int = Field(default=5, alias="DB_POOL_MIN_SIZE")
    DB_POOL_MAX_SIZE: int = Field(default=20, alias="DB_POOL_MAX_SIZE")
    CHURN_MODEL_PATH: str = Field(default="assets/models/churn_xgb_v2.joblib", alias="CHURN_MODEL_PATH")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()
```

---

## 6. Non-Blocking AI Endpoints: Lead Scoring & Churn Prediction

```python
import asyncio
from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel, Field, ConfigDict

router = APIRouter(prefix="/api/v1/predict", tags=["AI Inference"])

class ChurnFeatureInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_id: str = Field(..., description="Unique customer identifier")
    tenure_months: int = Field(..., ge=0, le=120)
    monthly_charges: float = Field(..., ge=0.0)
    total_support_tickets: int = Field(..., ge=0)
    contract_type_annual: bool = Field(...)

class ChurnPredictionOutput(BaseModel):
    customer_id: str
    churn_probability: float = Field(..., ge=0.0, le=1.0)
    is_high_risk: bool
    recommended_action: str

@router.post("/churn", response_model=ChurnPredictionOutput, status_code=status.HTTP_200_OK)
async def predict_customer_churn(payload: ChurnFeatureInput, request: Request) -> ChurnPredictionOutput:
    model = getattr(request.app.state, "churn_classifier", None)
    if model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="AI Model not loaded")
        
    features = [[payload.tenure_months, payload.monthly_charges, payload.total_support_tickets, 1 if payload.contract_type_annual else 0]]
    
    # Execute CPU-bound inference in separate thread pool
    def _run_inference() -> float:
        probabilities = model.predict_proba(features)
        return float(probabilities[0][1])
        
    churn_prob = await asyncio.to_thread(_run_inference)
    high_risk = churn_prob >= 0.65
    action = "Immediate Retention Offer" if high_risk else "Standard Monitoring"
    
    return ChurnPredictionOutput(
        customer_id=payload.customer_id,
        churn_probability=round(churn_prob, 4),
        is_high_risk=high_risk,
        recommended_action=action
    )
```

---

## 7. 5 Production Patterns in Zerops

### Pattern 1: High-Performance Async Lifespan with Pools & NATS
Initializes `asyncpg`, `pgvector` codecs, Valkey, and NATS JetStream within `@asynccontextmanager lifespan`.

### Pattern 2: Sub-Millisecond pgvector HNSW Vector Search
Executes cosine distance search against 1536-dimensional embeddings with HNSW indexing in `<1.5ms P99`.

### Pattern 3: Non-Blocking CPU ML Inference via Thread Pooling
Wraps heavy Scikit-Learn or XGBoost model predictions in `asyncio.to_thread()` to prevent stalling the ASGI event loop.

### Pattern 4: Sliding-Window Rate Limiting with Valkey
Enforces IP-based rate limiting using Valkey pipelines inside reusable FastAPI `Depends` functions.

### Pattern 5: Granian ASGI Rust Deployment with Astral uv
Leverages Granian with uvloop and `uv pip install` in `zerops.yaml` for sub-5 second deployment cycles and 75,000+ RPS throughput.

---

## 8. Anti-Patterns & Common Gotchas

1. **Using Deprecated `@app.on_event`**: Never use `@app.on_event("startup")`; always use `@asynccontextmanager lifespan(app: FastAPI)`.
2. **Blocking the ASGI Event Loop**: Running heavy synchronous CPU tasks directly inside `async def` endpoints blocks all incoming HTTP traffic. Always use `await asyncio.to_thread()`.
3. **Missing pgvector Codec Registration**: Failing to call `await register_vector(conn)` causes type conversion errors on vector columns.
