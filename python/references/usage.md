# Python — Developer & Agent Usage Manual on Zerops

This manual provides production-tested specifications, base OS selection rules, ASGI server tuning (Granian vs Uvicorn), database pooling patterns, and code recipes for developing with the **Zerops Managed Python Runtime** (`type: python@...` / `python@3.12`).

---

## 1. Base OS Selection Strategy in `zerops.yaml`

Within the Zerops Managed Python Runtime, the underlying OS base is configurable in `zerops.yaml`:

```
+-------------------------------------------------------------------------+
| Zerops Managed Python Runtime (type: python@3.12 / python@latest)       |
+------------------------------------+------------------------------------+
| Option A: os: alpine (Default)     | Option B: os: ubuntu               |
| - musl libc (~5MB base)            | - glibc 2.39 (~100MB base)         |
| - Ultra-lean RAM (~15-30MB)        | - Full glibc C-extension wheels    |
| - Pure Python & Async web apps     | - Instant numpy, torch, pandas     |
| - Ideal for FastAPI with asyncpg   | - Required for Data Science/ML     |
+------------------------------------+------------------------------------+
```

### When to Select `os: alpine` (Default)
* Asynchronous web APIs (`FastAPI`, `Litestar`, `Starlette`, `BlackSheep`).
* Pure Python database drivers (`asyncpg`, `redis-py`, `nats-py`).
* Web applications without heavy compiled C-extensions.

### When to Select `os: ubuntu`
* Data Science, Machine Learning, and Computer Vision (`torch`, `numpy`, `pandas`, `scipy`, `opencv-python`).
* Libraries requiring pre-compiled `manylinux_2_39` glibc wheels.
* Packages with complex C/C++ build requirements (`psycopg2-binary`, `cryptography`, `cffi`).

---

## 2. Environment Variables & Secret Ingestion

Zerops automatically generates and injects environment variables for managed services. Reference them in `zerops.yaml` using the `${hostname_key}` syntax:

```yaml
run:
  envVariables:
    PORT: "8000"
    PYTHONPATH: /var/www/vendor
    DB_HOST: ${db_hostname}
    DB_PORT: ${db_port}
    DB_USER: ${db_user}
    DB_PASS: ${db_password}
    DB_NAME: db
    CACHE_HOST: ${cache_hostname}
    CACHE_PORT: ${cache_port}
```

---

## 3. ASGI Production Servers: Granian vs Uvicorn

* **Granian (Recommended for High Throughput)**: Written in Rust on top of Hyper and Tokio. Outperforms Uvicorn by ~2x in concurrent I/O throughput and eliminates GIL contention on multi-core containers:
  ```bash
  /var/www/vendor/bin/granian --interface asgi --host 0.0.0.0 --port 8000 --workers 2 src.main:app
  ```
* **Uvicorn / Gunicorn with UvicornWorker**: Standard industry default for ASGI workloads:
  ```bash
  /var/www/vendor/bin/gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 2 src.main:app
  ```

---

## 4. Production Patterns & Verified Code Recipes

### Pattern 1: High-Performance FastAPI API with Granian
```python
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

class HealthResponse(BaseModel):
    status: str = Field(default="healthy")
    runtime: str = Field(default="zerops-python-managed")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (e.g. initialize connection pools)
    yield
    # Graceful shutdown logic

app = FastAPI(title="Zerops FastAPI Service", lifespan=lifespan)

@app.get("/healthz", response_model=HealthResponse)
async def health_check():
    return HealthResponse()

@app.get("/")
async def root():
    return {"message": "Welcome to Python on Zerops"}
```

### Pattern 2: Data Science / Machine Learning API (`os: ubuntu`)
```python
import os
import numpy as np
from fastapi import FastAPI

app = FastAPI(title="Data Science API on Zerops Ubuntu Base")

@app.get("/compute")
def compute_matrix():
    # Matrix operations utilizing glibc-optimized BLAS/LAPACK
    matrix_a = np.random.rand(500, 500)
    matrix_b = np.random.rand(500, 500)
    product = np.dot(matrix_a, matrix_b)
    trace_val = float(np.trace(product))
    return {
        "status": "computed",
        "matrix_shape": list(product.shape),
        "trace": trace_val
    }

@app.get("/healthz")
def health():
    return {"status": "healthy", "base": "ubuntu@24", "glibc": "2.39"}
```

### Pattern 3: Async PostgreSQL Pooling with `asyncpg` & SQLAlchemy 2.0
```python
import os
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME', 'db')}"
)

# Configured for Zerops elastic scaling
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def get_db_session():
    async with async_session_factory() as session:
        yield session
```

### Pattern 4: Atomic Alembic Migrations with `zsc execOnce`
In `zerops.yaml`:
```yaml
run:
  initCommands:
    - zsc execOnce ${appVersionId} --retryUntilSuccessful -- /var/www/vendor/bin/alembic upgrade head
```

Example migration script (`migrate.py` alternative):
```python
import os
import sys
from alembic.config import Config
from alembic import command

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    db_url = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME', 'db')}"
    )
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(alembic_cfg, "head")
    print("Alembic schema migration successfully completed via zsc execOnce")

if __name__ == "__main__":
    run_migrations()
```

### Pattern 5: Interactive SSH Development Setup with `noop`
```yaml
zerops:
  - setup: dev
    build:
      base: python@3.12
      buildCommands:
        - pip install --target=./vendor -r requirements.txt
      deployFiles:
        - ./
      cache:
        - vendor
    run:
      base: python@3.12
      ports:
        - port: 8000
          httpSupport: true
      envVariables:
        PYTHONPATH: /var/www/vendor
      start: zsc noop --silent
```

---

## 5. Anti-Patterns & Gotchas in Zerops

| Anti-Pattern | Why it Fails | Correct Solution |
|---|---|---|
| Installing torch/numpy on `os: alpine` | Builds from source; fails on musl headers or takes 30+ minutes | Set `os: ubuntu` in `build` and `run` to download pre-built wheels. |
| Forgetting `PYTHONPATH: /var/www/vendor` | Python cannot locate packages installed with `--target=./vendor` | Always set `PYTHONPATH: /var/www/vendor` in `run.envVariables`. |
| Running migrations in `buildCommands` | Migrations run against the build container, not the live database | Execute migrations in `run.initCommands` using `zsc execOnce`. |
| Omitting `cache: [vendor]` | Every build re-downloads all packages over the network | Add `cache: [vendor]` to reuse installed packages across builds. |
| Hardcoding `verticalAutoscaling` | Overrides Zerops' native dynamic elastic scaling | Omit `verticalAutoscaling` and allow Zerops to auto-scale. |
