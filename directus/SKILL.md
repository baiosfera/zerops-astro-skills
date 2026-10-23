---
name: directus
description: "Trigger: directus, directus 11, directus 12, directus bootstrap, directus flows, directus extensions, directus hooks, directus rag, directus auth. Enterprise Directus Headless CMS, BaaS & Data Engine with RAG, Flows, and Astro in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# Directus — Headless CMS, Unified BaaS & Data Engine (v2.1)

## Activation Contract
Activate whenever designing, bootstrapping, extending, or integrating Directus 11/12+ as a headless CMS, relational BaaS, dynamic data engine, content repository, or authentication provider on Zerops.

## Hard Rules & Positive Guidance
- **Database Backend**: Always wire Directus to managed PostgreSQL 18 (`${db_connectionString}`) using internal private network routing on port `5432`.
- **Cache & Webhook Layer**: Connect Valkey 7.2 (`${cache_connectionString}`) for high-speed metadata caching, rate-limiting, and session storage.
- **Media Asset Storage**: Store uploaded files in persistent volumes (`local-storage`) or S3 Object Storage (`storage`). Never store binary uploads in the application container filesystem.
- **Declarative Schema Sync**: Manage collections and permissions declaratively via Directus Schema snapshots (`directus-cli schema snapshot` / `apply`). Zero unversioned manual schema mutations.
- **Flows & Automation**: Implement asynchronous triggers via Directus Flows or route critical domain events to NATS (`events.directus.*`) for decoupled processing.
- **Security & RBAC**: Enforce Public role lockdown: all write and sensitive read endpoints require authenticated tokens or App API keys with minimal required scopes.

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Schema Design & PIM | Declarative relational collections & relations | [`references/usage.md#schema-design`](file:///var/www/.agents/skills/directus/references/usage.md) |
| Directus SDK & Astro | Typed SDK integration with Astro SSR actions | [`references/usage.md#sdk-integration`](file:///var/www/.agents/skills/directus/references/usage.md) |
| Container Topology | Directus runtime setup on Ubuntu/Node.js | [`references/infra.md#runtime-setup`](file:///var/www/.agents/skills/directus/references/infra.md) |
| Storage & Cache Wiring | PostgreSQL + Valkey + S3 configuration | [`references/infra.md#storage-cache`](file:///var/www/.agents/skills/directus/references/infra.md) |

## Critical Workflows
1. Provision Directus service paired with PostgreSQL 18 and Valkey 7.2 in `import.yaml`.
2. Configure environment variables in `zerops_env` (`KEY`, `SECRET`, `DB_CLIENT: pg`, `$db_connectionString`).
3. Apply initial schema snapshot and seed admin credentials securely.
4. Verify Directus health via physical sensor (`curl -s http://directus:8055/server/ping`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/directus/references/usage.md) — Directus TypeScript SDK, relational modeling, Flows, custom extensions, and auth patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/directus/references/infra.md) — Service deployment on Zerops, PostgreSQL/Valkey integration, environment variables, and scaling.
