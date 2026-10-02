---
name: listmonk
description: "Trigger: listmonk, newsletter, mailing list, transactional email, campaigns, email templates, bounce webhooks, listmonk api, listmonk zerops. High-performance open-source newsletter, subscriber manager & transactional email engine for Zerops."
license: AGPL-3.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `listmonk` — Sovereign Email Marketing & Transactional Engine (v2.0)

## Activation Contract
Activate when provisioning, deploying, or orchestrating Listmonk (v6.2.0+) within Zerops Incus LXC containers, executing transactional email dispatch (`POST /api/tx`), managing subscribers and lists via the REST API v6, rendering Go/Sprig templates with RFC 8058 One-Click Unsubscribe headers, or architecting multi-container horizontal scaling with PostgreSQL 18 and S3 Object Storage.

## Hard Rules & Positive Guidance
- **Native Go Architecture & Upstream v6.2.0**: Deploy official static binary (`v6.2.0_linux_amd64`) on `os: alpine` connecting to managed PostgreSQL 18 (`postgresql:single@18` or `postgresql:ha@18`).
- **PostgreSQL 18 Schema & Search Path Invariant**: Always execute `CREATE SCHEMA IF NOT EXISTS listmonk;` and set `LISTMONK_db__params: "search_path=listmonk,public"` to guarantee extension and `pgcrypto` resolution.
- **Atomic Migrations via `zsc execOnce`**: Wrap `./listmonk --install --idempotent --yes --config=""` and `./listmonk --upgrade --yes --config=""` inside `zsc execOnce ${appVersionId}` to prevent concurrent migration collisions.
- **Split-Brain Prevention in Horizontal Scaling (`--passive`)**: When running 2+ containers for high availability, start the primary container with `./listmonk --config=""` and auxiliary HTTP replicas with `./listmonk --config="" --passive` to prevent duplicate campaign job execution.
- **Decoupled S3 Media Storage**: Use Zerops Object Storage (`upload.provider: "s3"`) with Listmonk native reverse proxying, eliminating single-tenant local disk paths.
- **REST API Bot Token Authentication**: Authenticate service-to-service calls using dedicated API service accounts (`type = 'api'`) via header `Authorization: token <api_token>` against internal DNS `http://listmonk:9000`.

## Decision Gates

| Objective | Action | Reference / Asset |
|---|---|---|
| Complete API & Templates | REST API v6 endpoints, `/api/tx`, Sprig & RFC 8058 | [`references/usage.md`](file:///var/www/.agents/skills/listmonk/references/usage.md) |
| Zerops Topology & Infra | `import.yaml`, `zerops.yaml`, PG18 & `--passive` scaling | [`references/infra.md`](file:///var/www/.agents/skills/listmonk/references/infra.md) |
| Typed TypeScript Client | Polymorphic API client with bot token authentication | [`assets/listmonk_client.ts`](file:///var/www/.agents/skills/listmonk/assets/listmonk_client.ts) |
| Production Recipes | Zerops YAML blueprints and JSON transactional payloads | [`assets/listmonk_production_recipes.json`](file:///var/www/.agents/skills/listmonk/assets/listmonk_production_recipes.json) |
| Physical Validation Sensor | Attest skill integrity, schema validation & algorithms | [`scripts/listmonk-validate.sh`](file:///var/www/.agents/skills/listmonk/scripts/listmonk-validate.sh) |

## Execution Steps
1. Provision PostgreSQL 18 database and Listmonk service container via Zerops `import.yaml`.
2. Configure `zerops.yaml` with pre-compiled static binary on `os: alpine` and `zsc execOnce` migrations.
3. Wire dynamic database environment variables and set `search_path=listmonk,public`.
4. Configure S3 Object Storage provider credentials for campaign media uploads.
5. Integrate Astro 5 SSR actions using typed `listmonk_client.ts` over internal Zerops DNS.
6. Verify deployment health via physical sensor check (`curl -f http://listmonk:9000/admin`).

## Output Contract
- Sovereign, sub-second Listmonk v6.2.0 service running on Zerops with ~20 MB RAM footprint.
- Robust transactional email and campaign pipelines passing all physical validation sensors (Exit 0).
