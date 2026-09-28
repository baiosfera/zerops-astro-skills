# `business-insights`: Developer Manual, Contracts & Implementation Recipes (v2.0)

`business-insights` is the master business, commercial, and financial intelligence orchestrator for the Zerops sovereign stack. Under the strict **$0 SaaS licensing and ~0 MB extra RAM overhead** governance model, it consolidates commercial analytics, sales performance, cash flow, and financial health into native **Directus 11+ Insights** panels (`directus_dashboards`, `directus_panels`) and integrates with **Frappe Cloud ERPNext REST API**, eliminating the need for standalone, memory-heavy BI tools (like Metabase, Grafana, or Superset).

---

## 1. 4D Comparative Architectural Matrix

| Dimension | Directus 11+ Insights (Target) | Metabase (Self-Hosted) | Apache Superset | Looker Studio / PowerBI |
|---|---|---|---|---|
| **Server RAM Footprint** | **0 MB Extra** (Natively inside Directus/Postgres) | ~800 MB–1.5 GB RAM (Java JVM) | ~1 GB–2 GB RAM (Python/Celery) | 0 MB (Remote SaaS) |
| **SaaS Licensing Cost** | **$0 SaaS** (Open-source data engine) | $0 Open Source / Enterprise | $0 Open Source | Per user / connector billing |
| **Query Latency** | **Sub-millisecond** (Direct SQL in PostgreSQL) | Dependent on JDBC pool | Dependent on Celery workers | 1–5 seconds (External network) |
| **ERPNext Sync Method** | **Lightweight async worker in Bun/Node** | Complex ETL / Dbt | Complex SQL pipelines | Paid third-party connectors |
| **Zerops Execution** | **100% Native on existing container mesh** | Requires dedicated heavy LXC | Requires multi-service cluster | Exposes data to public cloud |

---

## 2. Sub-Skills Inventory & Direct File Pointers

* **Financial Metrics & P&L:** [`erpnext`](file:///var/www/.agents/skills/erpnext/SKILL.md) ([usage](file:///var/www/.agents/skills/erpnext/references/usage.md), [infra](file:///var/www/.agents/skills/erpnext/references/infra.md)).
* **Visual Dashboards in Directus Insights:** [`directus`](file:///var/www/.agents/skills/directus/SKILL.md) ([usage](file:///var/www/.agents/skills/directus/references/usage.md), [infra](file:///var/www/.agents/skills/directus/references/infra.md)).

---

## 3. Declarative Directus Insights Dashboard Seeder (TypeScript)

Automated provisioning script that builds the executive commercial dashboard inside Directus 11+:

```typescript
// scripts/seed-business-dashboard.ts
import { createDirectus, rest, staticToken, createItem } from '@directus/sdk';

const directus = createDirectus(process.env.DIRECTUS_URL || 'http://directus:8055')
  .with(staticToken(process.env.DIRECTUS_STATIC_TOKEN || ''))
  .with(rest());

export async function seedBusinessDashboard() {
  // 1. Create main executive dashboard
  const dashboard = await directus.request(
    createItem('directus_dashboards', {
      name: 'Executive Commercial & Financial Dashboard',
      icon: 'insights',
      note: 'Real-time GMV, conversion, recovered carts, and Frappe Cloud P&L',
    })
  );

  const dashboardId = dashboard.id;

  // 2. Panel 1: Monthly GMV Metric
  await directus.request(
    createItem('directus_panels', {
      dashboard: dashboardId,
      name: 'Current Month GMV (COP)',
      icon: 'payments',
      type: 'metric',
      position_x: 1,
      position_y: 1,
      width: 6,
      height: 6,
      options: {
        collection: 'orders',
        aggregate: { function: 'sum', field: 'total_amount' },
        filter: { status: { _eq: 'completed' } },
        prefix: '$ ',
        format: true,
      },
    })
  );

  // 3. Panel 2: Average Order Value (AOV)
  await directus.request(
    createItem('directus_panels', {
      dashboard: dashboardId,
      name: 'Average Order Value (AOV)',
      icon: 'receipt_long',
      type: 'metric',
      position_x: 7,
      position_y: 1,
      width: 6,
      height: 6,
      options: {
        collection: 'orders',
        aggregate: { function: 'avg', field: 'total_amount' },
        filter: { status: { _eq: 'completed' } },
        prefix: '$ ',
        format: true,
      },
    })
  );

  // 4. Panel 3: Recovered Carts Metric
  await directus.request(
    createItem('directus_panels', {
      dashboard: dashboardId,
      name: 'Recovered Carts Count',
      icon: 'shopping_cart_checkout',
      type: 'metric',
      position_x: 13,
      position_y: 1,
      width: 6,
      height: 6,
      options: {
        collection: 'orders',
        aggregate: { function: 'count', field: 'id' },
        filter: { recovered_from_whatsapp: { _eq: true } },
        suffix: ' recovered',
      },
    })
  );

  console.log(`Business Insights dashboard configured with ID: ${dashboardId}`);
}
```

---

## 4. Financial KPI Synchronization Worker from Frappe Cloud ($0 SaaS)

Periodic worker that queries P&L and gross margin statements from Frappe Cloud and persists snapshots into Directus:

```typescript
// workers/sync-financial-kpis.ts
import { createDirectus, rest, staticToken, createItem } from '@directus/sdk';

const directus = createDirectus(process.env.DIRECTUS_URL || 'http://directus:8055')
  .with(staticToken(process.env.DIRECTUS_STATIC_TOKEN || ''))
  .with(rest());

export async function syncFinancialKPIs() {
  const baseUrl = process.env.FRAPPE_CLOUD_URL || 'https://your-company.frappe.cloud';

  // Fetch cumulative monthly Profit & Loss statement
  const res = await fetch(`${baseUrl}/api/method/erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement.execute`, {
    headers: {
      'Authorization': `token ${process.env.FRAPPE_API_KEY}:${process.env.FRAPPE_API_SECRET}`,
      'Accept': 'application/json',
    },
  });

  if (res.ok) {
    const reportData = await res.json();
    const message = reportData.message || {};
    const totalIncome = message.total_income || 0;
    const totalExpense = message.total_expense || 0;
    const netProfit = totalIncome - totalExpense;
    const grossMarginPct = totalIncome > 0 ? ((totalIncome - totalExpense) / totalIncome) * 100 : 0;

    // Persist snapshot to Directus collection
    await directus.request(
      createItem('business_kpis_snapshot', {
        date: new Date().toISOString().split('T')[0],
        total_income_cop: totalIncome,
        total_expense_cop: totalExpense,
        net_profit_cop: netProfit,
        gross_margin_percentage: grossMarginPct,
        synced_at: new Date().toISOString(),
      })
    );
    console.log(`[ERPNext Sync] Financial snapshot saved: Net Profit = COP ${netProfit}`);
  }
}
```

---

## 5. Optimized SQL Queries for Real-Time Aggregations (PostgreSQL 18)

```sql
-- 1. 30-Day Sales Performance by Payment Gateway
SELECT 
    payment_gateway,
    COUNT(id) AS total_orders,
    SUM(total_amount) AS gmv_cop,
    AVG(total_amount) AS aov_cop,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) AS successful_orders
FROM orders
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY payment_gateway
ORDER BY gmv_cop DESC;

-- 2. Checkout Funnel Conversion Rate (30 Days)
SELECT 
    COUNT(CASE WHEN event_type = 'checkout_initiated' THEN 1 END) AS initiated,
    COUNT(CASE WHEN event_type = 'payment_submitted' THEN 1 END) AS submitted,
    COUNT(CASE WHEN event_type = 'checkout_completed' THEN 1 END) AS completed,
    (COUNT(CASE WHEN event_type = 'checkout_completed' THEN 1 END)::float / 
     NULLIF(COUNT(CASE WHEN event_type = 'checkout_initiated' THEN 1 END), 0) * 100) AS conversion_rate_pct
FROM funnel_events
WHERE created_at >= NOW() - INTERVAL '30 days';
```

---

## 6. 5 Production Patterns in Zerops

### Pattern 1: Automated Directus Insights Provisioning on Bootstrap
Execute `seedBusinessDashboard()` during `run.initCommands` to ensure executive panels exist automatically upon deploy.

### Pattern 2: Asynchronous Financial Sync Worker with Frappe Cloud
Scheduled task executing every 6 hours to fetch cumulative P&L and gross margin without locking operational tables.

### Pattern 3: High-Performance Funnel Aggregations with PostgreSQL Indexes
PostgreSQL composite indexes on `orders(created_at, status, total_amount)` provide sub-millisecond aggregations for 100k+ records.

### Pattern 4: WhatsApp Cart Recovery Tracking ([`evolutiongo`](file:///var/www/.agents/skills/evolutiongo/SKILL.md))
Directus collection flag `recovered_from_whatsapp = true` enables tracking revenue saved via automated WhatsApp sequences.

### Pattern 5: Low-Margin & High-AR Alerts via NATS JetStream
Background worker analyzes P&L and outstanding accounts receivable, emitting alert messages to NATS when margins drop below threshold.

---

## 7. Anti-Patterns & Common Gotchas

1. **Deploying Heavy BI Stacks on Small VPS**: Running Metabase or Superset adds 1–2 GB RAM overhead. Use Directus Insights for $0 and 0 MB extra RAM.
2. **Mutating ERPNext Records during Analytics Sync**: Sync workers must operate strictly in read-only mode to prevent polluting accounting books.
3. **Unindexed Aggregations on Large Tables**: Running `SUM()` or `AVG()` on unindexed `created_at` fields slows down dashboard rendering. Always add composite B-Tree indexes.
