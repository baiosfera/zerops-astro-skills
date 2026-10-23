---
name: postgresql
description: "Trigger: postgresql, postgres, postgresql@18, pgvector, hnsw, ivfflat, json_table, uuidv7, bun.sql, drizzle-orm pg, prisma pg, postgresql:single, postgresql:ha. Architect, optimize, connect, and manage PostgreSQL 18 databases on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# PostgreSQL — Zerops Managed Relational & Vector Database Engine (v2.1)

## Activation Contract
Activate whenever architecting, querying, provisioning, tuning, or connecting to PostgreSQL 18, `pgvector` v0.8+ (HNSW/IVFFlat), SQL/JSON `JSON_TABLE`, `uuidv7()`, or managing Zerops databases (`type: postgresql:single@18` or `type: postgresql:ha@18`).

## Hard Rules & Positive Guidance
- **Immutable Variant Gate**: Choose between `postgresql:single@18` (lean dev/stage) and `postgresql:ha@18` (3-node HA with automatic failover) before provisioning. Variants are immutable after creation.
- **Scaling Profiles**: Assign an explicit `profile:` (`oltp-hobby` for dev, `oltp-staging` for production lean, `oltp-production` for dedicated high-throughput). Rely on Zerops platform scaling over manual autoscaling blocks.
- **Port Routing Architecture**:
  - Port `5432`: Primary Read/Write transactional connection (Internal mesh, direct, no SSL required).
  - Port `5433`: Balanced Read Replicas (available exclusively in `:ha`).
  - Port `6432`: External secure access via pgBouncer with TLS (`${db_portTls}`). Node/Bun clients connecting to 6432 must supply TLS configuration.
- **Superuser Extensions Flow**: Install extensions (`vector`, `pg_stat_statements`, `pg_trgm`, `postgis`) using `${db_superUser}` (`postgres`) and restart via `zerops_manage action="restart"` to activate `shared_preload_libraries`.
- **Dynamic NVMe Storage**: Storage expands automatically as data grows; size allocations never shrink.
- **Connection Isolation & Quota**:
  - Set limits: `ALTER DATABASE <db> WITH CONNECTION LIMIT 60;` on primary application DB and `WITH CONNECTION LIMIT 15;` on satellite DBs.
  - Terminate idle sessions: Set `idle_session_timeout = '2min'` and `idle_in_transaction_session_timeout = '30s'`.
  - Use stateless `pool.query()` over dedicated persistent checkouts in web endpoints.

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| PostgreSQL 18 SQL/JSON & uuidv7 | JSON_TABLE, uuidv7, virtual columns | [`references/usage.md#postgresql-18-features`](file:///var/www/.agents/skills/postgresql/references/usage.md) |
| Vector Search with pgvector | HNSW, IVFFlat, halfvec, bit quantized | [`references/usage.md#pgvector-search`](file:///var/www/.agents/skills/postgresql/references/usage.md) |
| Zerops Topology & Profiles | oltp-hobby vs oltp-staging vs oltp-production | [`references/infra.md#managed-profiles`](file:///var/www/.agents/skills/postgresql/references/infra.md) |
| Architecture Comparison | Managed Single vs HA vs Generic LXC | [`references/infra.md#four-way-comparison`](file:///var/www/.agents/skills/postgresql/references/infra.md) |

## Critical Workflows
1. Define database topology in `import.yaml` using `type: postgresql:single@18` or `postgresql:ha@18` with explicit `profile:`.
2. Connect from application runtimes using `${db_hostname}` on port `5432` or `5433` (read replicas).
3. Install extensions with superuser and trigger restart via `zerops_manage action="restart"`.
4. Validate connectivity with physical database sensor (`SELECT 1;`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/postgresql/references/usage.md) — Developer manual, PostgreSQL 18 features, SQL/JSON, `uuidv7()`, `pgvector` HNSW, and ORM patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/postgresql/references/infra.md) — Infrastructure manual, :single vs :ha profiles, ports, extension provisioning, and connection quotas.
