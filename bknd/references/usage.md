# `bknd`: Universal Backend, Sovereign Data & Edge Ingress Manual (v2.0)

`bknd` is the master backend orchestrator commanding all backend services, database engines, event brokers, asynchronous microservices, external enterprise ERP connectors, and Cloudflare Edge ingress routing. It guarantees high concurrency, sub-millisecond inter-service communication, and $0 recurring SaaS licensing costs.

---

## 1. 4D Comparative Architectural Matrix: Backend Communication Protocols

| Protocol / Mechanism | Core Engine | Baseline Latency (P99) | Resource Consumption | Zerops Suitability |
|---|---|---|---|---|
| **NATS Request-Reply RPC (Target)** | **NATS 2.12 Binary TCP** | **<0.3ms P99** | **~25 MB RAM total** | **SSoT for Inter-Service RPC** |
| **Direct Internal HTTP/REST** | HTTP 1.1 JSON | ~2.5–5.0ms | HTTP socket overhead | Standard for public APIs |
| **gRPC over HTTP/2** | HTTP/2 Protobuf | ~1.0–1.8ms | Requires proto compilation | High maintenance overhead |
| **Database Polling** | SQL Query Loop | >100ms | High DB I/O load | Prohibited for real-time |

---

## 2. Sub-Skills Inventory & Direct File Pointers

| Sub-Skill | Role in Backend Ecosystem | Direct SSoT Pointer |
|---|---|---|
| **`directus`** | Headless CMS, CRM, auto-generated REST/GraphQL API, user permissions | [`directus`](file:///var/www/.agents/skills/directus/SKILL.md) |
| **`nats`** | NATS Server 2.12 Request-Reply RPC (<0.3ms P99), JetStream, :8222/varz | [`nats`](file:///var/www/.agents/skills/nats/SKILL.md) |
| **`fastapi`** | High-performance Python microservices, pgvector HNSW search, ML inference | [`fastapi`](file:///var/www/.agents/skills/fastapi/SKILL.md) |
| **`erpnext`** | Frappe Cloud REST API ($0 SaaS tier, legal DIAN billing & inventory sync) | [`erpnext`](file:///var/www/.agents/skills/erpnext/SKILL.md) |
| **`devllm-telemetry`**| LLM token/cost tracking in USD, NATS/Valkey metrics, backup verification | [`devllm-telemetry`](file:///var/www/.agents/skills/devllm-telemetry/SKILL.md) |
| **`business-insights`**| GMV, AOV, financial balances in Directus Insights (~0 MB RAM extra) | [`business-insights`](file:///var/www/.agents/skills/business-insights/SKILL.md) |
| **`postgresql`** | PostgreSQL 18 relational engine, HNSW vector indexing, UUIDv7, JSON table | [`postgresql`](file:///var/www/.agents/skills/postgresql/SKILL.md) |
| **`valkey`** | Valkey 7.2 in-memory caching, sliding window rate limiter, BullMQ queues | [`valkey`](file:///var/www/.agents/skills/valkey/SKILL.md) |
| **`local-storage`** | Persistent POSIX shared storage volumes (`/mnt/storage/`), pg_dump backups | [`local-storage`](file:///var/www/.agents/skills/local-storage/SKILL.md) |
| **`whatsapp-engine`** | Sovereign Golang WhatsApp gateway decoupled via NATS & Bifrost | [`whatsapp-engine`](file:///var/www/.agents/skills/whatsapp-engine/SKILL.md) |
| **`payment-gateways`** | Cryptographic webhook validation, Wompi SHA-256, Stripe HMAC, Valkey locks | [`payment-gateways`](file:///var/www/.agents/skills/payment-gateways/SKILL.md) |
| **`cloudflare`** | API Subdomains (`api.domain.com`), WAF ACME bypass, SSL Full Strict | [`cloudflare`](file:///var/www/.agents/skills/cloudflare/SKILL.md) |

---

## 3. TypeScript Contract: Astro Actions + NATS RPC + Directus SDK

```typescript
// src/actions/checkout.ts
import { defineAction, ActionError } from 'astro:actions';
import { z } from 'astro:schema';
import { connect, JSONCodec } from 'nats';
import { createDirectus, rest, createItem, staticToken } from '@directus/sdk';

const jc = JSONCodec();

let natsConn: any = null;
async function getNats() {
  if (!natsConn || natsConn.isClosed()) {
    natsConn = await connect({ servers: process.env.NATS_URL || 'nats://nats:4222' });
  }
  return natsConn;
}

const directus = createDirectus(process.env.DIRECTUS_URL || 'http://directus:8055')
  .with(staticToken(process.env.DIRECTUS_STATIC_TOKEN || ''))
  .with(rest());

export const server = {
  processOrder: defineAction({
    accept: 'json',
    input: z.object({
      customerEmail: z.string().email(),
      customerName: z.string().min(2),
      customerPhone: z.string().min(10),
      cityDaneCode: z.string().length(8),
      items: z.array(z.object({
        productId: z.string().uuid(),
        quantity: z.number().int().positive(),
        unitPrice: z.number().positive(),
      })),
      paymentMethod: z.enum(['WOMPI_PSE', 'WOMPI_NEQUI', 'WOMPI_CARD', 'COD']),
    }),
    handler: async (input) => {
      try {
        const nc = await getNats();

        // 1. Invoke atomic inventory lock RPC via NATS (<0.3ms P99)
        const rpcPayload = { items: input.items, lockTimeoutSeconds: 900 };
        const inventoryRes = await nc.request(
          'inventory.lock',
          jc.encode(rpcPayload),
          { timeout: 2000 }
        );
        const lockResult = jc.decode(inventoryRes.data) as { success: boolean; lockId?: string; reason?: string };

        if (!lockResult.success) {
          throw new ActionError({
            code: 'PRECONDITION_FAILED',
            message: lockResult.reason || 'Inventory unavailable for one or more selected items.',
          });
        }

        // 2. Persist preliminary order in Directus 11+
        const totalAmount = input.items.reduce((acc, it) => acc + it.unitPrice * it.quantity, 0);
        const orderRecord = await directus.request(
          createItem('orders', {
            customer_email: input.customerEmail,
            customer_name: input.customerName,
            customer_phone: input.customerPhone,
            dane_code: input.cityDaneCode,
            total_amount: totalAmount,
            status: 'pending_payment',
            payment_gateway: input.paymentMethod,
            inventory_lock_id: lockResult.lockId,
          })
        );

        return {
          success: true,
          orderId: orderRecord.id,
          totalAmount,
          lockId: lockResult.lockId,
        };
      } catch (err: any) {
        if (err instanceof ActionError) throw err;
        throw new ActionError({
          code: 'INTERNAL_SERVER_ERROR',
          message: `Error processing order: ${err.message}`,
        });
      }
    },
  }),
};
```

---

## 4. Python Contract: FastAPI Microservice + NATS RPC + pgvector

```python
# services/inventory_rpc.py
import asyncio
import json
import os
import asyncpg
from contextlib import asynccontextmanager
from fastapi import FastAPI
import nats

DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgresql:5432/app_db")
NATS_URL = os.getenv("NATS_URL", "nats://nats:4222")

class AppState:
    db_pool: asyncpg.Pool = None
    nc = None

state = AppState()

@asynccontextmanager
async def lifespan(app: FastAPI):
    state.db_pool = await asyncpg.create_pool(dsn=DB_URL, min_size=5, max_size=20)
    state.nc = await nats.connect(NATS_URL)

    async def handle_inventory_lock(msg):
        try:
            data = json.loads(msg.data.decode())
            items = data.get("items", [])
            
            async with state.db_pool.acquire() as conn:
                async with conn.transaction():
                    for it in items:
                        row = await conn.fetchrow(
                            "SELECT stock_quantity FROM products WHERE id = $1 FOR UPDATE",
                            it["productId"]
                        )
                        if not row or row["stock_quantity"] < it["quantity"]:
                            res = {"success": False, "reason": f"Insufficient stock for {it['productId']}"}
                            await msg.respond(json.dumps(res).encode())
                            return
                    
                    for it in items:
                        await conn.execute(
                            "UPDATE products SET stock_quantity = stock_quantity - $1 WHERE id = $2",
                            it["quantity"], it["productId"]
                        )
                    
                    lock_id = f"lock_{asyncio.get_event_loop().time()}"
                    res = {"success": True, "lockId": lock_id}
                    await msg.respond(json.dumps(res).encode())
        except Exception as e:
            res = {"success": False, "reason": str(e)}
            await msg.respond(json.dumps(res).encode())

    sub = await state.nc.subscribe("inventory.lock", cb=handle_inventory_lock)

    yield

    await sub.unsubscribe()
    await state.nc.close()
    await state.db_pool.close()

app = FastAPI(title="Inventory & AI RPC Service", lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "inventory_rpc", "runtime": "python@3.12-granian"}
```

---

## 5. Frappe Cloud / ERPNext REST Client ($0 SaaS Cost)

```typescript
// src/lib/erpnext-client.ts
export interface ERPNextInvoicePayload {
  customer: string;
  items: Array<{
    item_code: string;
    qty: number;
    rate: number;
  }>;
  taxes_and_charges?: string;
  posting_date?: string;
}

export class ERPNextClient {
  private baseUrl: string;
  private apiKey: string;
  private apiSecret: string;

  constructor() {
    this.baseUrl = process.env.FRAPPE_CLOUD_URL || 'https://your-company.frappe.cloud';
    this.apiKey = process.env.FRAPPE_API_KEY || '';
    this.apiSecret = process.env.FRAPPE_API_SECRET || '';
  }

  private getHeaders() {
    return {
      'Authorization': `token ${this.apiKey}:${this.apiSecret}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
  }

  async createSalesInvoice(payload: ERPNextInvoicePayload) {
    const res = await fetch(`${this.baseUrl}/api/resource/Sales Invoice`, {
      method: 'POST',
      headers: this.getHeaders(),
      body: JSON.stringify({
        docstatus: 1, // 1 = Submitted
        customer: payload.customer,
        posting_date: payload.posting_date || new Date().toISOString().split('T')[0],
        items: payload.items.map(it => ({
          item_code: it.item_code,
          qty: it.qty,
          rate: it.rate,
        })),
      }),
    });

    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`Error in Frappe Cloud ERPNext (${res.status}): ${errorText}`);
    }

    const data = await res.json();
    return data.data;
  }
}
```

---

## 6. Automated `pg_dump` Backups to Shared Storage

```bash
#!/bin/bash
# /var/www/scripts/backup-postgres.sh
set -euo pipefail

BACKUP_DIR="/mnt/localstorage/backups/postgresql"
TIMESTAMP=$(date +'%Y%m%d_%H%M%S')
TARGET_FILE="${BACKUP_DIR}/backup_${TIMESTAMP}.sql.gz"
RETENTION_DAYS=7

mkdir -p "${BACKUP_DIR}"

echo "Starting PostgreSQL 18 backup to ${TARGET_FILE}..."
timeout 120s pg_dump "${DATABASE_URL}" | gzip -9 > "${TARGET_FILE}"

echo "Backup completed successfully ($(du -h "${TARGET_FILE}" | cut -f1))."

# Purge backups older than 7 days
find "${BACKUP_DIR}" -type f -name "backup_*.sql.gz" -mtime +${RETENTION_DAYS} -delete
echo "Retention policy applied (${RETENTION_DAYS} days)."
```

---

## 7. Verification Commands & Health Attestation

```bash
# 1. Check NATS Server 2.12 health
curl -s http://nats:8222/varz | grep "version"

# 2. Check Valkey 7.2 memory and latency
valkey-cli -u "$VALKEY_URL" ping
valkey-cli -u "$VALKEY_URL" info memory | grep "used_memory_human"

# 3. Check PostgreSQL 18 connection
psql "$DATABASE_URL" -c "SELECT version(), current_setting('server_version');"
```

---

## 8. 5 Production Patterns in Backend Architecture

### Pattern 1: Atomic Mutations with Astro Actions & NATS RPC
Coordinates inventory reservation and database persistence across independent microservices via NATS `<0.3ms P99` RPC.

### Pattern 2: High-Speed Python Microservices with Granian & pgvector
Executes semantic vector searches against 1536-dimensional embeddings with HNSW indexing in sub-millisecond latencies.

### Pattern 3: Asynchronous Directus ➔ ERPNext Sync with BullMQ
Dispatches completed sales orders from Directus to Frappe Cloud ERPNext asynchronously via BullMQ on Valkey.

### Pattern 4: Sliding-Window Rate Limiting with Valkey
Protects public APIs against brute-force attacks using atomic Valkey Redis pipelining.

### Pattern 5: Deterministic pg_dump Backup Execution
Runs scheduled database backups to POSIX shared storage (`/mnt/localstorage/backups/`) with automated 7-day retention pruning.

### Pattern 6: Resilient PostgreSQL Upsert & Phone Variant Normalization
Prevents raw PostgreSQL unique constraint violations (`leads_email_key` / `leads_whatsapp_key`) during user checkout or registration. Generates phone variants (+57, 57, 10-digit), performs multi-variant queries, updates existing records without colliding on unique keys, and guarantees zero HTTP 500 errors in digital payment flows.

### Pattern 7: Intelligent Multi-Channel Lead Deduplication & Cross-Conflict Protection (409)
Tracks `registered_channels` inside PostgreSQL metadata JSONB (`jsonb_set` / array append). When a contact re-submits a form for a channel they are already part of, the API idempotently acknowledges the submission (`already_registered: true`) while suppressing duplicate email and WhatsApp dispatches. If a contact joins a new channel, the channel is appended and only the specific welcome flow fires. If an input email belongs to user A and the phone belongs to user B, the system halts with HTTP 409 Conflict, rejecting silent identity corruption.

---

## 9. Anti-Patterns & Common Gotchas

1. **Hardcoding Plaintext Credentials**: Never commit database passwords or tokens into git repositories; always reference `$db_connectionString` and `$cache_connectionString`.
2. **Blocking the Event Loop in Python**: Heavy CPU-bound AI inferences MUST execute inside `await asyncio.to_thread()`.
3. **Missing POSIX FUSE Permissions**: Always apply `chmod -R 777 /mnt/<storage>/<service>/` to avoid permission errors across container boundaries.
4. **Silent Identity Overwriting on Cross-Conflict**: Updating database records by matching either email OR phone without verifying mutual ownership allows accidental record corruption or hijacking. Always verify that email and phone belong to the same entity, returning HTTP 409 Conflict if they point to different existing contacts.

