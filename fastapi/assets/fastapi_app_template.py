from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator
import asyncpg
from fastapi import FastAPI, Depends, Request, HTTPException, status
from pgvector.asyncpg import register_vector
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Configuración Inmutable
class Settings(BaseSettings):
    ENVIRONMENT: str = Field(default="production", alias="ENVIRONMENT")
    DATABASE_URL: SecretStr = Field(..., alias="DATABASE_URL")
    DB_POOL_MIN_SIZE: int = Field(default=5, alias="DB_POOL_MIN_SIZE")
    DB_POOL_MAX_SIZE: int = Field(default=20, alias="DB_POOL_MAX_SIZE")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# 2. Lifespan Context Manager
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    async def init_connection(conn: asyncpg.Connection) -> None:
        await register_vector(conn)

    app.state.pg_pool = await asyncpg.create_pool(
        dsn=settings.DATABASE_URL.get_secret_value(),
        min_size=settings.DB_POOL_MIN_SIZE,
        max_size=settings.DB_POOL_MAX_SIZE,
        init=init_connection,
    )
    yield
    if getattr(app.state, "pg_pool", None):
        await app.state.pg_pool.close()

# 3. Inyección de Dependencias
def get_db_pool(request: Request) -> asyncpg.Pool:
    pool = getattr(request.app.state, "pg_pool", None)
    if not pool:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="DB Pool not ready")
    return pool

DbPool = Annotated[asyncpg.Pool, Depends(get_db_pool)]

async def get_db_connection(pool: DbPool) -> AsyncGenerator[asyncpg.Connection, None]:
    async with pool.acquire() as connection:
        yield connection

DbConnection = Annotated[asyncpg.Connection, Depends(get_db_connection)]

# 4. App Factory
app = FastAPI(title="FastAPI High-Concurrency Microservice", lifespan=lifespan)

@app.get("/healthz", tags=["Health"])
async def health_check(conn: DbConnection):
    val = await conn.fetchval("SELECT 1")
    return {"status": "healthy", "db": val == 1}
