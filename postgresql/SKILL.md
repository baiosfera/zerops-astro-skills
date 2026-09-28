---
name: postgresql
description: "Trigger: postgresql, postgres, postgresql@18, pgvector, hnsw, ivfflat, json_table, uuidv7, bun.sql, drizzle-orm pg, prisma pg, postgresql:single, postgresql:ha. Architect, optimize, connect, and manage PostgreSQL 18 databases on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# PostgreSQL — Zerops Managed Relational & Vector Database Engine (v2.0)

## Activation Contract
Activate whenever architecting, querying, provisioning, tuning, or connecting to PostgreSQL 18, `pgvector` v0.8+ (HNSW/IVFFlat), SQL/JSON `JSON_TABLE`, `uuidv7()`, or managing Zerops semi-managed databases (`type: postgresql:single@18` or `type: postgresql:ha@18`).

## Hard Rules
- **Rule 1 (Immutable Variant Gate)**: Explicitly choose between `postgresql:single@18` (dev/staging/lean) and `postgresql:ha@18` (3-node HA cluster with automatic failover) before provisioning. Variants are immutable after creation.
- **Rule 2 (Scaling Profile Invariant)**: Always assign an explicit `profile:` (`oltp-hobby` for dev :single, `oltp-staging` for production lean, `oltp-production` for dedicated mission-critical). Do NOT author manual `verticalAutoscaling` min/max blocks.
- **Rule 3 (Port Routing Architecture)**:
  - Port `5432`: Primary Read/Write transactional connection.
  - Port `5433`: Balanced Read Replicas (available exclusively in `:ha`).
  - Port `6432`: External secure access via pgBouncer with TLS (`${db_portTls}`).
- **Rule 4 (Superuser Extension Flow)**: Install extensions (`vector`, `pg_stat_statements`, `pg_trgm`, `postgis`) using `${db_superUser}` (`postgres`) on `${db_dbName}` and MUST restart the service via `zerops_manage action="restart" serviceHostname="db"` to activate `shared_preload_libraries`.
- **Rule 5 (Disk Growth Law)**: Allocated NVMe storage expands dynamically and **never shrinks**.
- **Rule 6 (Fractal CoHaLo Bounded Execution)**: All synchronous commands MUST enforce timeouts (`timeout 10s`), synchronous wait (`WaitMsBeforeAsync: 10000`), and terminate orphan background processes with `manage_task action="kill"`.

## Decision Gates

| Task / Scenario | Recommended Strategy | Reference / Asset |
|---|---|---|
| PostgreSQL 18 SQL/JSON & `uuidv7()` | `JSON_TABLE`, `uuidv7()`, Virtual Columns | [`references/usage.md`](file:///var/www/.agents/skills/postgresql/references/usage.md) |
| Vector Search with `pgvector` v0.8+ | HNSW, IVFFlat, `halfvec`, `bit` quantized | [`references/usage.md`](file:///var/www/.agents/skills/postgresql/references/usage.md) |
| Zerops Topology & Profiles (:single vs :ha) | `oltp-hobby` vs `oltp-staging` vs `oltp-production` | [`references/infra.md`](file:///var/www/.agents/skills/postgresql/references/infra.md) |
| Four-Way Architecture Comparison | Managed Single vs HA vs Generic LXC vs Clients | [`references/infra.md`](file:///var/www/.agents/skills/postgresql/references/infra.md) |
| Verified SQL & Extension Recipes | Production HNSW indexes, JSON_TABLE, and setups | [`assets/postgresql_production_recipes.json`](file:///var/www/.agents/skills/postgresql/assets/postgresql_production_recipes.json) |

## Critical Workflows / Execution Steps
1. Define database topology in `import.yaml` using `type: postgresql:single@18` or `postgresql:ha@18` with explicit `profile:`.
2. Connect from application runtimes using `${db_hostname}` on port `5432` or `5433` (read replicas).
3. If installing extensions, run `CREATE EXTENSION` with superuser and trigger `zerops_manage action="restart"`.
4. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
5. **Circuit Breaker (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500 / timeout) before escalating.
6. **Sensor Attestation**: Verify physical sensor check (exit code 0 / DB query probe `SELECT 1`).

## Output Contract
- Validated `import.yaml` and `zerops.yaml` manifests targeting PostgreSQL on Zerops.
- Verified database connectivity with zero orphaned tasks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/postgresql/references/usage.md) — Developer manual, PostgreSQL 18 features, SQL/JSON `JSON_TABLE`, `uuidv7()`, `pgvector` HNSW/halfvec/bit, and ORM patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/postgresql/references/infra.md) — Infrastructure manual, :single vs :ha, profiles, ports, extension provisioning flow, Four-Way comparison, and CoHaLo process hygiene.
- [`assets/postgresql_production_recipes.json`](file:///var/www/.agents/skills/postgresql/assets/postgresql_production_recipes.json) — SQL recipes, vector index calibration, and extension setup.
- [`assets/import_template.yaml`](file:///var/www/.agents/skills/postgresql/assets/import_template.yaml) — Clean `import.yaml` template with native elastic autoscaling.
- [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/postgresql/assets/zerops_template.yaml) — Application lifecycle `zerops.yaml` template with database wiring.
- [`scripts/postgresql-validate.sh`](file:///var/www/.agents/skills/postgresql/scripts/postgresql-validate.sh) — Physical integrity validator for the postgresql skill suite.
