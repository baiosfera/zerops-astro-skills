---
name: business-insights
description: "Trigger: business-insights, sales metrics, erpnext finances, directus analytics, commercial kpis, gmv analytics, aov metrics, checkout funnels, frappe sync. Master Business & Financial Insights Orchestrator with Directus Insights, ERPNext P&L sync & PostgreSQL in Zerops."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `business-insights` — Commercial & Financial Intelligence Orchestrator (v2.0)

## Activation Contract
Activate when orchestrating executive sales performance, GMV, Average Order Value (AOV), checkout conversion rate, WhatsApp cart recovery, or syncing financial P&L and valued stock from Frappe Cloud ERPNext into native **Directus 11+ Insights** dashboards on Zerops.

## Hard Rules
- **Zero Memory Bloat**: Never deploy heavy standalone BI containers (Metabase, Superset). All commercial and financial dashboards MUST run through native Directus Insights panels (~0 MB extra RAM).
- **Read-Only ERP Sync**: KPI sync workers polling Frappe Cloud MUST operate strictly in read-only mode, persisting snapshots into `business_kpis_snapshot` without mutating production accounting ledgers.
- **Analytical Indexing**: Ensure composite B-Tree indexes exist on `orders(status, created_at, total_amount)` in PostgreSQL 18.
- **Fractal CoHaLo**: Enforce strict hygiene (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans (`manage_task action="kill"`), sensor (Directus dashboard check).
- **Zero Deletion**: Consult [`references/usage.md`](file:///var/www/.agents/skills/business-insights/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/business-insights/references/infra.md) for full lossless APIs.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 4D Matrix & Comparison | Directus Insights vs Metabase, Superset, Looker | [`references/usage.md#1-4d-comparative-architectural-matrix`](file:///var/www/.agents/skills/business-insights/references/usage.md) |
| Dashboard Seeder Script | Provision GMV, AOV & Cart Recovery panels in Directus | [`references/usage.md#3-declarative-directus-insights-dashboard-seeder-typescript`](file:///var/www/.agents/skills/business-insights/references/usage.md) |
| Frappe Cloud P&L Sync | Scheduled worker extracting P&L and gross margins | [`references/usage.md#4-financial-kpi-synchronization-worker-from-frappe-cloud-0-saas`](file:///var/www/.agents/skills/business-insights/references/usage.md) |
| SQL Analytical Queries | Sub-millisecond PostgreSQL 18 sales aggregations | [`references/usage.md#5-optimized-sql-queries-for-real-time-aggregations-postgresql-18`](file:///var/www/.agents/skills/business-insights/references/usage.md) |
| Multi-Service Topology | Connect Directus, Astro, NATS, ERPNext & PostgreSQL | [`references/infra.md#1-multi-service-analytics-topology-in-zerops`](file:///var/www/.agents/skills/business-insights/references/infra.md) |
| Database Index Optimization | Composite B-Tree indexes on orders & funnel events | [`references/infra.md#2-postgresql-18-analytical-index-optimization`](file:///var/www/.agents/skills/business-insights/references/infra.md) |
| Production Recipes JSON | Seeder code and SQL index definitions | [`assets/business_insights_production_recipes.json`](file:///var/www/.agents/skills/business-insights/assets/business_insights_production_recipes.json) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/business-insights-validate.sh`](file:///var/www/.agents/skills/business-insights/scripts/business-insights-validate.sh) |

## Execution Steps
1. Verify `DIRECTUS_URL` and `FRAPPE_CLOUD_URL` in Zerops environment variables.
2. Apply analytical indexes on PostgreSQL 18 (`CREATE INDEX idx_orders_analytics_gmv...`).
3. Execute `seedBusinessDashboard()` to provision executive Directus Insights panels.
4. Schedule the 6-hour financial sync worker for Frappe Cloud P&L snapshots.
5. Verify dashboard presence via physical sensor check.

## Output Contract
- Zero-bloat executive control panel running inside Directus 11+ Insights on Zerops.
- Automated 6-hour P&L synchronization from Frappe Cloud and passing physical validation sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/business-insights/references/usage.md) — 4D matrix, dashboard seeders, Frappe Cloud sync workers, SQL queries, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/business-insights/references/infra.md) — Multi-service topology, PostgreSQL analytical indexing, and CoHaLo harness.
- [`assets/business_insights_production_recipes.json`](file:///var/www/.agents/skills/business-insights/assets/business_insights_production_recipes.json) — Production seeder code and SQL indexing recipes.
- [`scripts/business-insights-validate.sh`](file:///var/www/.agents/skills/business-insights/scripts/business-insights-validate.sh) — Deterministic quality & token validation sensor.
