---
name: erpnext
description: "Trigger: erpnext, frappe, frappe rest api, erpnext webhooks, frappe cloud, directus erpnext sync, doctype api, valkey bullmq sync, dian invoicing, sales order erpnext, ciiu resolver. Enterprise agnostic ERPNext integration with Frappe Cloud, DIAN Colombia e-invoicing, Directus 11+ & BullMQ in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.6"
---

# `erpnext` — Universal Enterprise ERP, DIAN Invoicing & Advanced REST/RPC Suite (v2.6)

## Activation Contract
Orchestrating integrations between ERPNext / Frappe Cloud, Colombian DIAN compliance (CIIU Rev. 4 A.C.), Directus 11+, and accounting agents across business archetypes.

## Core Directives & Invariants
- **SoR Authority & Decoupling**: ERPNext acts as System of Record for accounting, DIAN, and stock (`tabBin`), while Directus acts as SoR for PIM and clients. Resolves company defaults, warehouses, and tax rules dynamically at runtime.
- **Dynamic CIIU-to-PUC & DIAN Invoicing**: Resolves economic activities to PUC ledgers via [`scripts/erpnext-ciiu-resolver.py`](file:///var/www/zerops-astro-skills/erpnext/scripts/erpnext-ciiu-resolver.py). Binds to Amazon SES v2 (`$AWS_*`) and configures `System Settings.enable_onboarding = 0` for headless desk operation.
- **Process Hygiene & Security**: Enforces `timeout 10s`, `WaitMsBeforeAsync: 10000`, standard token authorization (`Authorization: token <api_key>:<api_secret>`), and physical sensor validation with exit code 0.

## Decision Gates & References
- **REST & Batch RPC API**: [`usage.md`](file:///var/www/zerops-astro-skills/erpnext/references/usage.md) — CRUD operations, filters, projections, and batch RPC methods.
- **Multi-Service Architecture**: [`infra.md`](file:///var/www/zerops-astro-skills/erpnext/references/infra.md) — Directus 11+, Valkey BullMQ, and Frappe CRM mesh.
- **Autonomous Accounting**: [`agent_accounting.md`](file:///var/www/zerops-astro-skills/erpnext/references/agent_accounting.md) — UVT monitoring and gateway fee reconciliations.
- **Declarative Profile & Recipes**: [`onboarding_profile.json`](file:///var/www/zerops-astro-skills/erpnext/assets/onboarding_profile.json) · [`erpnext_production_recipes.json`](file:///var/www/zerops-astro-skills/erpnext/assets/erpnext_production_recipes.json) — Agnostic templates and JSON recipes.
- **Lifecycle Hooks**: [`directus_frappe_hook.ts`](file:///var/www/zerops-astro-skills/erpnext/assets/directus_frappe_hook.ts) · [`frappe_webhook_endpoint.ts`](file:///var/www/zerops-astro-skills/erpnext/assets/frappe_webhook_endpoint.ts) — BullMQ order queue and webhook verification.
- **Tooling & Validation**: [`erpnext-onboard.py`](file:///var/www/zerops-astro-skills/erpnext/scripts/erpnext-onboard.py) · [`erpnext-rut-parser.py`](file:///var/www/zerops-astro-skills/erpnext/scripts/erpnext-rut-parser.py) · [`erpnext-client.py`](file:///var/www/zerops-astro-skills/erpnext/scripts/erpnext-client.py) · [`erpnext-validate.sh`](file:///var/www/zerops-astro-skills/erpnext/scripts/erpnext-validate.sh) — Client engine and deterministic validator.

## Commands
```bash
# Run universal physical validation sensor
bash /var/www/zerops-astro-skills/erpnext/scripts/erpnext-validate.sh

# Run internal unit tests of Frappe REST & RPC client
python3 /var/www/zerops-astro-skills/erpnext/scripts/erpnext-client.py --test

# Resolve business archetype and accounts from any CIIU code
python3 /var/www/zerops-astro-skills/erpnext/scripts/erpnext-ciiu-resolver.py --ciiu 4791
```
