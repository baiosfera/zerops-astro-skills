# `business-insights` Infrastructure, Analytics Indexing & Zerops Manual (v2.0)

This manual provides production-grade infrastructure blueprints, PostgreSQL 18 analytical index optimization, scheduled cron workers, environment variable management, and the Fractal CoHaLo operational harness for `business-insights`.

---

## 1. Multi-Service Analytics Topology in Zerops

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Enterprise Project Topology                                                                     │
│                                                                                                        │
│   ┌──────────────────────────────┐              ┌──────────────────────────────────────────────────┐   │
│   │ Astro Frontend UI (astro)    │              │ Directus 11+ Unified BaaS (directus)             │   │
│   │ (Checkout & User Funnels)    │─────────────▶│ (nodejs@24 / os: ubuntu)                         │   │
│   └──────────────┬───────────────┘              │ - Native Directus Insights Dashboards            │   │
│                  │                              │ - Collections: orders, funnel_events, snapshots  │   │
│                  │ Emite evento checkout        └────────────────────────┬─────────────────────────┘   │
│                  ▼                                                       ▲                             │
│   ┌──────────────────────────────┐                                       │ Updates KPIs snapshot       │
│   │ NATS JetStream (nats)        │                                       │                             │
│   │ - `events.orders.completed`  │              ┌────────────────────────┴─────────────────────────┐   │
│   └──────────────┬───────────────┘              │ Financial Sync Worker (aiworker / directus)      │   │
│                  │                              │ (bun@1.3 / nodejs@24)                            │   │
│                  │ Analytics Log Stream         │ - Scheduled Cron every 6 hours                   │   │
│                  ▼                              │ - Read-Only sync with Frappe Cloud ERPNext       │   │
│   ┌──────────────────────────────┐              └────────────────────────┬─────────────────────────┘   │
│   │ Managed PostgreSQL 18 (db)   │                                       │                             │
│   │ - Analytical Indexing B-Tree │                                       ▼                             │
│   │ - SSoT Orders & Funnel Data  │              ┌──────────────────────────────────────────────────┐   │
│   └──────────────────────────────┘              │ Frappe Cloud ERPNext REST API ($0 SaaS)          │   │
│                                                 │ - P&L Statement, Gross Margin, Valued Inventory  │   │
│                                                 └──────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. PostgreSQL 18 Analytical Index Optimization

To maintain sub-millisecond query latency on executive dashboard panels as order volume grows:

```sql
-- 1. Composite Index for 30-Day GMV and Order Status Aggregation
CREATE INDEX IF NOT EXISTS idx_orders_analytics_gmv 
ON orders (status, created_at DESC, total_amount);

-- 2. Index for Funnel Event Conversion Tracking
CREATE INDEX IF NOT EXISTS idx_funnel_events_conversion 
ON funnel_events (event_type, created_at DESC);

-- 3. Index for WhatsApp Cart Recovery
CREATE INDEX IF NOT EXISTS idx_orders_cart_recovery 
ON orders (recovered_from_whatsapp, created_at DESC) 
WHERE recovered_from_whatsapp = true;
```

---

## 3. Environment Variables Reference Dictionary

| Variable | Scope | Description |
|---|---|---|
| `DIRECTUS_URL` | Directus | Directus internal DNS endpoint (`http://directus:8055`) |
| `DIRECTUS_STATIC_TOKEN` | Directus | Admin API token for seeder and sync scripts |
| `FRAPPE_CLOUD_URL` | ERPNext | Frappe Cloud canonical URL (`https://your-company.frappe.cloud`) |
| `FRAPPE_API_KEY` | ERPNext | Frappe REST API key |
| `FRAPPE_API_SECRET` | ERPNext | Frappe REST API secret |
| `NATS_URL` | NATS | NATS internal connection string (`nats://nats:4222`) |

---

## 4. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with `business-insights` must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All sync scripts and API requests must use explicit timeouts (`timeout 10s curl -f ...`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all background monitoring scripts using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Directus Dashboards check: `curl -s http://directus:8055/dashboards | grep -q "Executive Commercial"` $\implies$ Exit 0.
  * ERPNext Health check: `curl -s -o /dev/null -w "%{http_code}" https://your-company.frappe.cloud/api/method/ping` $\implies$ Expected: `200`.
* **Circuit Breaker Policy**: If Frappe Cloud returns 401/403 or times out during scheduled sync, skip the snapshot and retry on the next 6-hour interval without crashing the main service.
