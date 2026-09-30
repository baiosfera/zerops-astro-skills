# Hermes-Agent Production Tools Bundle
# Standardized Pydantic v2 schemas and async tool handlers for Zerops multi-service mesh

import os
import json
import uuid
import time
import httpx
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

# ==============================================================================
# 1. ZCP / Antigravity Execution Bridge Tools
# ==============================================================================

class ZcpDeployInput(BaseModel):
    service: str = Field(..., description="Hostname of the target Zerops service (e.g. 'directus', 'astro')")
    branch: Optional[str] = Field("main", description="Git branch to deploy")

class ZcpStatusInput(BaseModel):
    service: Optional[str] = Field(None, description="Optional hostname of specific service to inspect")

async def tool_zcp_dispatch_deploy(service: str, branch: str = "main") -> Dict[str, Any]:
    nats_url = os.getenv("ZCP_NATS_URL", "nats://nats:4222")
    try:
        from nats.aio.client import Client as NATS
        nc = NATS()
        await nc.connect(nats_url)
        js = nc.jetstream()
        task_id = str(uuid.uuid4())
        payload = {
            "task_id": task_id,
            "action": "deploy",
            "target_service": service,
            "params": {"branch": branch},
            "timestamp": time.time()
        }
        await js.publish("zerops.ops.requests", json.dumps(payload).encode("utf-8"), headers={"Nats-Msg-Id": task_id})
        await nc.close()
        return {"status": "queued", "task_id": task_id, "service": service, "message": "Deployment dispatched to AGY."}
    except Exception as err:
        return {"status": "error", "message": f"NATS dispatch failed: {str(err)}"}

# ==============================================================================
# 2. Directus CMS Tools
# ==============================================================================

class DirectusQueryInput(BaseModel):
    collection: str = Field(..., description="Target Directus collection name")
    limit: int = Field(10, description="Max items to return")

async def tool_directus_query(collection: str, limit: int = 10) -> Dict[str, Any]:
    base_url = os.getenv("DIRECTUS_URL", "http://directus:8055")
    token = os.getenv("DIRECTUS_STATIC_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            res = await client.get(f"{base_url}/items/{collection}?limit={limit}", headers=headers)
            return {"status_code": res.status_code, "data": res.json()}
        except Exception as err:
            return {"status": "error", "message": str(err)}

# ==============================================================================
# 3. EvolutionGo WhatsApp Tools
# ==============================================================================

class EvolutionStatusInput(BaseModel):
    instance: Optional[str] = Field(None, description="Instance name, or None for all instances")

async def tool_evolution_status(instance: Optional[str] = None) -> Dict[str, Any]:
    base_url = os.getenv("EVOLUTION_URL", "http://evolution:8080")
    headers = {"apikey": os.getenv("EVOLUTION_APIKEY", "")}
    path = f"/instance/connectionState/{instance}" if instance else "/instance/fetchInstances"
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            res = await client.get(f"{base_url}{path}", headers=headers)
            return {"status_code": res.status_code, "data": res.json()}
        except Exception as err:
            return {"status": "error", "message": str(err)}

# ==============================================================================
# 4. Astro Frontend Health Tools
# ==============================================================================

async def tool_astro_health() -> Dict[str, Any]:
    url = os.getenv("ASTRO_URL", "http://astro:3000/healthz")
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            res = await client.get(url)
            return {"status": "ok" if res.status_code == 200 else "degraded", "http_code": res.status_code}
        except Exception as err:
            return {"status": "unreachable", "error": str(err)}

# ==============================================================================
# 5. Astrological Calculation & Oraculo Shards Tools
# ==============================================================================

class AstrologyCalculateChartInput(BaseModel):
    name: str = Field(..., description="Full legal or commercial name of the client")
    date_str: str = Field(..., description="Birth date in YYYY-MM-DD format")
    time_str: str = Field(..., description="Birth time in HH:MM format (24h)")
    lat: float = Field(..., description="Birth geographic latitude (-90.0 to 90.0)")
    lon: float = Field(..., description="Birth geographic longitude (-180.0 to 180.0)")
    city: str = Field("Unknown", description="City of birth")
    nation: str = Field("CO", description="Country code (ISO 3166-1 alpha-2)")
    dry_run: bool = Field(False, description="Simulate extraction without live API costs")

async def tool_astrology_calculate_chart(payload: AstrologyCalculateChartInput) -> Dict[str, Any]:
    """Dispatch astrological calculation across federated engines via NATS or direct HTTP"""
    nats_url = os.getenv("ZCP_NATS_URL", "nats://nats:4222")
    task_id = str(uuid.uuid4())
    message_data = {
        "task_id": task_id,
        "action": "astrology.calculate.v1",
        "client": payload.model_dump(),
        "timestamp": time.time()
    }
    try:
        from nats.aio.client import Client as NATS
        nc = NATS()
        await nc.connect(nats_url)
        js = nc.jetstream()
        await js.publish(
            "astrology.requests",
            json.dumps(message_data).encode("utf-8"),
            headers={"Nats-Msg-Id": task_id}
        )
        await nc.close()
        return {"status": "dispatched", "task_id": task_id, "message": "Astrological calculation queued on NATS."}
    except Exception as err:
        return {"status": "error", "message": f"NATS dispatch failed: {str(err)}"}

class AstrologyGetClientDumpsInput(BaseModel):
    client_id: str = Field(..., description="UUID of the client in PostgreSQL 18")
    shard_name: Optional[str] = Field(None, description="Optional specific shard name (e.g. 'shard_tropical', 'shard_dashas')")

async def tool_astrology_get_client_dumps(client_id: str, shard_name: Optional[str] = None) -> Dict[str, Any]:
    """Query 15-shard JSONB client dumps from PostgreSQL 18"""
    db_url = os.getenv("DATABASE_URL", "")
    if not db_url:
        return {"status": "error", "message": "DATABASE_URL not configured"}
    try:
        import asyncpg
        conn = await asyncpg.connect(db_url)
        if shard_name:
            row = await conn.fetchrow(f"SELECT {shard_name} FROM client_dumps WHERE client_id = $1", uuid.UUID(client_id))
            await conn.close()
            return {"status": "ok", "client_id": client_id, "shard": shard_name, "data": json.loads(row[0]) if row and row[0] else None}
        else:
            row = await conn.fetchrow("SELECT * FROM client_dumps WHERE client_id = $1", uuid.UUID(client_id))
            await conn.close()
            return {"status": "ok", "client_id": client_id, "data": dict(row) if row else None}
    except Exception as err:
        return {"status": "error", "message": f"PostgreSQL query failed: {str(err)}"}
