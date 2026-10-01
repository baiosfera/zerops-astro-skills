---
name: listmonk
description: "Trigger: listmonk, newsletter, mailing list, transactional email, campaigns, email templates, bounce webhooks, listmonk api, listmonk zerops. High-performance open-source newsletter, subscriber manager & transactional email engine for Zerops."
license: AGPL-3.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# Listmonk — Sovereign Email Marketing & Transactional Engine (v1.0)

## Activation Contract
Activate whenever deploying, configuring, integrating, or managing Listmonk newsletter campaigns, mailing lists, transactional emails (`/api/tx`), Go template engines, subscriber APIs, or bounce webhooks inside Zerops services.

## Hard Rules
- **Zerops Native Architecture**: Deploy Listmonk as a native Go service (`type: go@1.22` or binary on `os: alpine`) connected to managed PostgreSQL (`type: postgresql@16:single` or `:ha`).
- **Atomic Migrations (`zsc execOnce`)**: Always execute `./listmonk --install --idempotent --yes --config=""` and `./listmonk --upgrade --yes --config=""` wrapped inside `zsc execOnce ${appVersionId}` to prevent concurrent migration race conditions.
- **PostgreSQL 18 Schema Pre-Creation**: When configuring `LISTMONK_db__params: "search_path=listmonk"`, execute `CREATE SCHEMA IF NOT EXISTS listmonk;` before `./listmonk --install` to prevent schema selection failures.
- **Double Underscore Env Mapping & API Auth**: Pass configuration dynamically via Zerops environment variables using double underscores (`LISTMONK_admin__username: "admin"`). In Listmonk v5, REST API endpoints require a dedicated bot account with `type = 'api'` and `user_role_id = 1` in `listmonk.users`.
- **Fractal CoHaLo Execution**: Enforce strict process hygiene (`timeout 10s`), synchronous wait (`WaitMsBeforeAsync: 10000`), zero orphaned tasks (`manage_task action="kill"`), and sensor verification (HTTP `200` on `/admin`).
- **Zero Deletion Invariant**: Consult [`references/usage.md`](file:///var/www/.agents/skills/listmonk/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/listmonk/references/infra.md) for complete lossless APIs, schemas, and recipes.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 4D Matrix & Benchmarks | Contrast Listmonk vs Ghost, Mailcoach, Sendy, Resend | [`references/usage.md#1-4d-comparative-architectural-matrix`](file:///var/www/.agents/skills/listmonk/references/usage.md) |
| Subscriber REST APIs | Query with SQL expressions, create, update, blocklist | [`references/usage.md#3-subscribers-management-api`](file:///var/www/.agents/skills/listmonk/references/usage.md) |
| High-Throughput `/api/tx` | Dispatch transactional emails with dynamic JSON data | [`references/usage.md#4-high-performance-transactional-engine-post-apitx`](file:///var/www/.agents/skills/listmonk/references/usage.md) |
| Go Template & Sprig Engine | Render `{{ UnsubscribeURL }}`, `{{ TrackView }}`, `{{ .Tx.Data.* }}` | [`references/usage.md#5-templating-engine-syntax--sprig-functions`](file:///var/www/.agents/skills/listmonk/references/usage.md) |
| Zerops `import.yaml` & `zerops.yaml` | Production deployment lifecycle, LXC Alpine, FUSE storage | [`references/infra.md#2-provisioning-blueprint-importyaml`](file:///var/www/.agents/skills/listmonk/references/infra.md) |
| JSON Production Recipes | Pre-built `zerops.yaml` blueprints & API payloads | [`assets/listmonk_production_recipes.json`](file:///var/www/.agents/skills/listmonk/assets/listmonk_production_recipes.json) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/listmonk-validate.sh`](file:///var/www/.agents/skills/listmonk/scripts/listmonk-validate.sh) |

## Execution Steps
1. Provision PostgreSQL database and Listmonk service via Zerops `import.yaml`.
2. Configure `zerops.yaml` with pre-compiled static binary on `os: alpine` and `zsc execOnce` migrations.
3. Inject dynamic database connection environment variables (`LISTMONK_db__host: ${db_hostname}`).
4. Mount persistent upload storage to `/mnt/baiostorage/listmonk/uploads` with `chmod -R 777`.
5. Integrate application code with Listmonk REST API (`/api/subscribers` and `/api/tx`) over internal Zerops DNS.
6. Verify deployment health via physical sensor check (`curl -f http://listmonk:9000/admin`).

## Output Contract
- Operational Listmonk service running on Zerops Incus LXC with sub-second cold boot and ~20 MB RAM footprint.
- Validated REST API integration with passing physical sensor checks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/listmonk/references/usage.md) — Complete REST API guide, transactional dispatch, Sprig templates, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/listmonk/references/infra.md) — Zerops topology, `import.yaml`, `zerops.yaml` lifecycle, environment dictionary, and CoHaLo harness.
- [`assets/listmonk_production_recipes.json`](file:///var/www/.agents/skills/listmonk/assets/listmonk_production_recipes.json) — Production deployment recipes and JSON payloads.
- [`scripts/listmonk-validate.sh`](file:///var/www/.agents/skills/listmonk/scripts/listmonk-validate.sh) — Deterministic quality & token validation sensor.
