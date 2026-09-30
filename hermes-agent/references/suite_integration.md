# Hermes-Agent Multi-Service Suite Orchestration Guide

This guide establishes the integration and orchestration patterns for **Hermes-Agent** across the full backend (`bknd`) and frontend (`frnt`) service topology deployed on Zerops.

---

## 1. Architectural Mesh Overview

Hermes-Agent acts as an intelligent administrative controller across the services deployed in the Zerops project:

```
                                    ┌──────────────────────┐
                                    │     TELEGRAM BOT     │
                                    └──────────┬───────────┘
                                               │
                                               ▼
                                    ┌──────────────────────┐
                                    │     HERMES-AGENT     │
                                    │    (Python 3.12)     │
                                    └──────────┬───────────┘
                                               │
                 ┌─────────────────────────────┼─────────────────────────────┐
                 │                             │                             │
                 ▼                             ▼                             ▼
      ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
      │   BACKEND SERVICES   │      │  FRONTEND & INGRESS  │      │  DATA & EVENT BUS    │
      │ • Directus (CMS)     │      │ • Astro (SSR / Edge) │      │ • PostgreSQL 18      │
      │ • ERPNext (Frappe)   │      │ • EvolutionGo (WA)   │      │ • Valkey 7.2 (Cache) │
      │                      │      │                      │      │ • NATS JetStream     │
      └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
```

---

## 2. Service-Specific Integration Protocols

### A. Directus Headless CMS
- **Role**: Content management, dynamic schemas, user profiles, and file storage.
- **Protocol**: Directus REST API (`http://directus:8055`) with Static Admin Token.
- **Hermes Tool Capabilities**:
  - `directus_get_items(collection, query)`: Fetch items with filtering and pagination.
  - `directus_create_item(collection, data)`: Insert new content item.
  - `directus_trigger_flow(flow_id, payload)`: Fire automated backend workflows.
- **Environment Ingestion**: Uses `$DIRECTUS_URL` and `$DIRECTUS_STATIC_TOKEN`.

### B. ERPNext & Frappe Framework
- **Role**: Business logic, inventory, accounting, and multi-tenant operations.
- **Protocol**: Frappe REST API (`http://erpnext:8000/api/method/`) using API Key & Secret.
- **Hermes Tool Capabilities**:
  - `erpnext_get_doc(doctype, name)`: Retrieve specific documents (e.g. Sales Invoice, Customer).
  - `erpnext_create_doc(doctype, data)`: Create business records.
  - `erpnext_get_status()`: Inspect background worker queue health and scheduler status.

### C. EvolutionGo (WhatsApp Engine)
- **Role**: WhatsApp multi-device messaging and webhook ingestion.
- **Protocol**: Evolution REST API (`http://evolution:8080`) with Global API Key.
- **Hermes Tool Capabilities**:
  - `evolution_get_instances()`: List all connected WhatsApp instances.
  - `evolution_send_message(instance, number, text)`: Transmit outbound WhatsApp messages.
  - `evolution_get_qr(instance)`: Retrieve base64 / PNG QR code for pairing sessions.

### D. Astro Frontend Engine
- **Role**: High-performance SSR and static web storefront.
- **Protocol**: HTTP health probes, webhooks, and rebuild signals via ZCP / AGY.
- **Hermes Tool Capabilities**:
  - `astro_health_check()`: Verify SSR endpoint responsiveness and response times.
  - `astro_trigger_rebuild()`: Trigger a clean build and deployment of the Astro service.

### E. Data Backbone: PostgreSQL, Valkey, and NATS
- **PostgreSQL**: Relational database queries executed via connection pooling (`asyncpg`). Hermes restricts ad-hoc queries to `SELECT` operations unless explicit override is confirmed.
- **Valkey**: In-memory caching, rate-limit counters, and active session states.
- **NATS**: Event distribution and asynchronous task queuing.

### F. Oráculo Astrological Calculation Engine & 15-Shard PostgreSQL 18 Mesh
- **Role**: Sovereign multi-tradition astrological calculation worker, generating 15 canonical JSONB shards and 11 feeds for each client.
- **Protocol**: NATS Request-Reply and JetStream pub/sub (`astrology.requests` -> `astrology.calculate.v1` -> `astrology.completed`).
- **Hermes Tool Capabilities**:
  - `tool_astrology_calculate_chart(payload)`: Dispatches client birth data to the federated extraction pipeline (AstroWay, VedAstro, FreeAstroAPI, AstrologyAPI, HebCal, BaZi-Lunar, Zmanim, Kundali).
  - `tool_astrology_get_client_dumps(client_id, shard_name)`: Reads client shard records (`shard_tropical`, `shard_sidereal`, `shard_vedic_kp`, `shard_dashas`, `shard_bazi`, `shard_ziwei`, `shard_kabbalah`, `shard_zmanim`, `shard_human_design`, `shard_cosmobiology`, `shard_nasa`, `shard_acg`, `shard_penta`, `shard_synastry`, `shard_timing`) directly from PostgreSQL 18 `client_dumps`.
- **Python MCP Engine**: In-process execution of BaZi (`zhdate`) and Zmanim (`kosherjava`/NOAA) algorithms, eliminating subprocess latency while preserving pure Python stdlib portability.

---

## 3. Tool Definition Bundle for Multi-Service Orchestration

```python
import os
import httpx
from pydantic import BaseModel, Field

# Directus Tools
class DirectusItemQuery(BaseModel):
    collection: str = Field(..., description="Name of the Directus collection")
    limit: int = Field(default=10, description="Max number of items to return")

async def tool_directus_list(collection: str, limit: int = 10) -> dict:
    url = f"{os.getenv('DIRECTUS_URL', 'http://directus:8055')}/items/{collection}?limit={limit}"
    headers = {"Authorization": f"Bearer {os.getenv('DIRECTUS_STATIC_TOKEN', '')}"}
    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.get(url, headers=headers)
        return res.json()

# EvolutionGo WhatsApp Tools
class WhatsAppMessageInput(BaseModel):
    instance: str = Field(..., description="WhatsApp instance name")
    phone_number: str = Field(..., description="Recipient phone number with country code")
    message: str = Field(..., description="Text content to deliver")

async def tool_evolution_send(instance: str, phone_number: str, message: str) -> dict:
    url = f"{os.getenv('EVOLUTION_URL', 'http://evolution:8080')}/message/sendText/{instance}"
    headers = {"apikey": os.getenv('EVOLUTION_APIKEY', '')}
    payload = {"number": phone_number, "options": {"delay": 1200}, "textMessage": {"text": message}}
    async with httpx.AsyncClient(timeout=10.0) as client:
        res = await client.post(url, json=payload, headers=headers)
        return res.json()

# Astro Health Tool
async def tool_astro_check() -> dict:
    url = os.getenv("ASTRO_URL", "http://astro:3000/healthz")
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            res = await client.get(url)
            return {"status": "ok" if res.status_code == 200 else "degraded", "code": res.status_code}
        except Exception as err:
            return {"status": "unreachable", "error": str(err)}
```

---

## 4. Cross-Service Deployment & Bootstrapping Sequence

When performing full-stack changes or cold boots, services must adhere to this topological sequence:

```
1. Infrastructure & Storage
   ├── storage (Object Storage S3)
   ├── postgres (PostgreSQL 18)
   ├── valkey (Valkey 7.2)
   └── nats (NATS JetStream)
         │
         ▼
2. Core Business Backends
   ├── directus (Ubuntu / Node.js 24)
   ├── erpnext (Python / Frappe)
   └── evolution (Alpine / Go 1.22)
         │
         ▼
3. Autonomous Agents & Frontends
   ├── hermes (Ubuntu / Python 3.12)
   └── astro (Alpine / Bun 1.3.9)
```

---

## 5. Security & Isolation Guidelines

- **Internal Hostnames**: Always use internal Docker/Zerops hostnames (`directus`, `postgres`, `valkey`, `nats`, `astro`, `evolution`) rather than external public routing to eliminate egress latency and protect endpoints.
- **Credential Hygiene**: Connection strings are injected via Zerops environment variables. Never write raw passwords, API keys, or tokens to configuration files or git repositories.
- **Read-Only Invariant**: Unless explicitly approved by an authorized administrator via Telegram inline keyboard, all database and schema inspections default to read-only semantics.
