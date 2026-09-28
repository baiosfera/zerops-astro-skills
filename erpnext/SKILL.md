---
name: erpnext
description: "Trigger: erpnext, frappe, frappe rest api, erpnext webhooks, frappe cloud, directus erpnext sync, doctype api, valkey bullmq sync, dian invoicing, sales order erpnext, ciiu resolver. Enterprise agnostic ERPNext integration with Frappe Cloud, DIAN Colombia e-invoicing, Directus 11+ & BullMQ in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.5"
---

# `erpnext` — Universal Enterprise ERP, DIAN Invoicing & Advanced REST/RPC Suite (v2.5)

## Activation Contract
Activate when orchestrating integrations between ERPNext / Frappe Cloud, Colombian DIAN compliance (CIIU Rev. 4 A.C.), Directus 11+, and accounting agents across 8 business archetypes.

## Hard Rules
- **Rule 1 (SoR Authority & Zero Brand Coupling)**: ERPNext acts as System of Record for accounting, DIAN, and stock (`tabBin`), while Directus acts as SoR for PIM and clients. Resolves company defaults, warehouses, and tax rules dynamically at runtime with tenant-agnostic execution.
- **Rule 2 (Dynamic CIIU-to-PUC & DIAN Invoicing)**: Resolves economic activities to PUC ledgers via [`scripts/erpnext-ciiu-resolver.py`](file:///var/www/.agents/skills/erpnext/scripts/erpnext-ciiu-resolver.py). Binds strictly to Amazon SES v2 (`$AWS_*`) and configures `System Settings.enable_onboarding = 0` for headless desk operation.
- **Rule 3 (Fractal CoHaLo Bounded Execution)**: Enforces `timeout 10s`, `WaitMsBeforeAsync: 10000`, standard token authorization (`Authorization: token <api_key>:<api_secret>`), and physical sensor validation with exit code 0.

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| **Batch RPC & Child Tables** | `insert_many`, `bulk_update`, atomic `set_value`, lifecycle | [`references/usage.md`](file:///var/www/.agents/skills/erpnext/references/usage.md) |
| **Files, Jinja & SES Outbound** | Uploads, DIAN PDFs & Amazon SES outbound configuration | [`references/usage.md`](file:///var/www/.agents/skills/erpnext/references/usage.md) |
| **Canonical REST & Invoicing** | CRUD, filters, projections, CUFE & QR code generation | [`references/usage.md`](file:///var/www/.agents/skills/erpnext/references/usage.md) |
| **Multi-Service Architecture** | Directus 11+, Valkey BullMQ, Frappe CRM & ERPNext mesh | [`references/infra.md`](file:///var/www/.agents/skills/erpnext/references/infra.md) |
| **Autonomous Accounting** | UVT monitoring ($52.374 COP for 2026) & gateway fees | [`references/agent_accounting.md`](file:///var/www/.agents/skills/erpnext/references/agent_accounting.md) |
| **Declarative Profile & Recipes** | Agnostic client profile & production JSON recipes | [`assets/onboarding_profile.json`](file:///var/www/.agents/skills/erpnext/assets/onboarding_profile.json) · [`assets/erpnext_production_recipes.json`](file:///var/www/.agents/skills/erpnext/assets/erpnext_production_recipes.json) |
| **Lifecycle Hooks & Webhooks** | BullMQ order queue hook & HMAC-SHA256 verification | [`assets/directus_frappe_hook.ts`](file:///var/www/.agents/skills/erpnext/assets/directus_frappe_hook.ts) · [`assets/frappe_webhook_endpoint.ts`](file:///var/www/.agents/skills/erpnext/assets/frappe_webhook_endpoint.ts) |
| **Setup Engine & Parsers** | Dynamic onboarding, RUT PDF parser & CIIU resolver | [`scripts/erpnext-onboard.py`](file:///var/www/.agents/skills/erpnext/scripts/erpnext-onboard.py) · [`scripts/erpnext-rut-parser.py`](file:///var/www/.agents/skills/erpnext/scripts/erpnext-rut-parser.py) · [`scripts/erpnext-ciiu-resolver.py`](file:///var/www/.agents/skills/erpnext/scripts/erpnext-ciiu-resolver.py) |
| **REST & RPC Client Engine** | Python client with token auth, batching, files & tests | [`scripts/erpnext-client.py`](file:///var/www/.agents/skills/erpnext/scripts/erpnext-client.py) |
| **Physical Validation Sensor** | Deterministic validator checking v2.5, links & tests | [`scripts/erpnext-validate.sh`](file:///var/www/.agents/skills/erpnext/scripts/erpnext-validate.sh) |

## Commands

```bash
# Run universal physical validation sensor
bash /var/www/.agents/skills/erpnext/scripts/erpnext-validate.sh

# Run internal unit tests of Frappe REST & RPC client
python3 /var/www/.agents/skills/erpnext/scripts/erpnext-client.py --test

# Resolve business archetype and accounts from any CIIU code
python3 /var/www/.agents/skills/erpnext/scripts/erpnext-ciiu-resolver.py --ciiu 4791
```

## Resources
- **Usage Reference**: [`references/usage.md`](file:///var/www/.agents/skills/erpnext/references/usage.md)
- **Infrastructure Guide**: [`references/infra.md`](file:///var/www/.agents/skills/erpnext/references/infra.md)
- **Accounting Protocol**: [`references/agent_accounting.md`](file:///var/www/.agents/skills/erpnext/references/agent_accounting.md)
- **Agnostic Profile**: [`assets/onboarding_profile.json`](file:///var/www/.agents/skills/erpnext/assets/onboarding_profile.json)
- **Production Recipes**: [`assets/erpnext_production_recipes.json`](file:///var/www/.agents/skills/erpnext/assets/erpnext_production_recipes.json)
- **Directus Hook**: [`assets/directus_frappe_hook.ts`](file:///var/www/.agents/skills/erpnext/assets/directus_frappe_hook.ts)
- **Webhook Endpoint**: [`assets/frappe_webhook_endpoint.ts`](file:///var/www/.agents/skills/erpnext/assets/frappe_webhook_endpoint.ts)
- **CIIU Resolver**: [`scripts/erpnext-ciiu-resolver.py`](file:///var/www/.agents/skills/erpnext/scripts/erpnext-ciiu-resolver.py)
- **Onboarding Engine**: [`scripts/erpnext-onboard.py`](file:///var/www/.agents/skills/erpnext/scripts/erpnext-onboard.py)
- **RUT Parser**: [`scripts/erpnext-rut-parser.py`](file:///var/www/.agents/skills/erpnext/scripts/erpnext-rut-parser.py)
- **REST & RPC Client**: [`scripts/erpnext-client.py`](file:///var/www/.agents/skills/erpnext/scripts/erpnext-client.py)
- **Validation Sensor**: [`scripts/erpnext-validate.sh`](file:///var/www/.agents/skills/erpnext/scripts/erpnext-validate.sh)
