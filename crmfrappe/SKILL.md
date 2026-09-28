---
name: crmfrappe
description: "Trigger: crmfrappe, frappe crm, fcrm, crm lead, crm deal, deal won, lead qualification, twilio webrtc, frappe whatsapp, erpnext crm handoff, crm onboarding. Manages Frappe CRM v1.83+ and ERPNext sales pipelines."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.2"
---

# Frappe CRM — High-Velocity Sales & Omnichannel Engine (v1.2)

## Activation Contract
Activate when orchestrating sales pipelines, ingesting web leads, managing deals, configuring Twilio WebRTC softphones, processing WhatsApp conversations, suppressing onboarding banners, or executing Deal-to-ERPNext `Quotation` handoffs under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md).

## Hard Rules
- **Rule 1 (Zero Database Duplication & SSoT Invariant)**: Frappe CRM resides on the same MariaDB bench instance as ERPNext ($0 extra on Frappe Cloud). Store and access CRM data exclusively within this shared database, maintaining relational integrity without external data replication.
- **Rule 2 (Autonomous Sales Handoff & Governance)**: Transitioning `CRM Deal` to `Won` triggers `create_customer_in_erpnext()`, links `erpnext_customer`, and exposes `prefill_quotation_items`. Setting `CRM Deal` to `Lost` requires a valid `lost_reason` (and `lost_notes` when `"Other"`).
- **Rule 3 (Fractal CoHaLo Bounded Execution)**: Enforce `timeout 10s`, `WaitMsBeforeAsync: 10000`, circuit breakers, and standard token authorization (`Authorization: token <api_key>:<api_secret>`). Detailed 38-DocType schemas and BullMQ worker templates reside in [`references/`](file:///var/www/.agents/skills/crmfrappe/references/).

## Decision Gates

| Operational Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| **Batch Lead Ingestion** | Ingest up to 200 leads per call via `frappe.client.insert_many` | [`references/usage.md`](file:///var/www/.agents/skills/crmfrappe/references/usage.md) |
| **Multimedia & Analytics** | File uploads, timespan filters & HMAC-SHA256 webhooks | [`references/usage.md`](file:///var/www/.agents/skills/crmfrappe/references/usage.md) |
| **Headless Onboarding Engine** | Two-level zero-banner suppression for existing and future users | [`scripts/crmfrappe-onboard.py`](file:///var/www/.agents/skills/crmfrappe/scripts/crmfrappe-onboard.py) |
| **API Reference & 4D Comparison** | Full DocType schemas, RPC endpoints, and 5 production patterns | [`references/usage.md`](file:///var/www/.agents/skills/crmfrappe/references/usage.md) |
| **Topology & Environment Config** | Zero-latency bench topology, env dictionary, and CoHaLo harness | [`references/infra.md`](file:///var/www/.agents/skills/crmfrappe/references/infra.md) |
| **Ready-to-Use Payloads** | Standard JSON recipes for Leads, Deals, and Quotations | [`assets/crmfrappe_production_recipes.json`](file:///var/www/.agents/skills/crmfrappe/assets/crmfrappe_production_recipes.json) |
| **Live API Health Check** | CLI sensor testing Frappe Cloud connectivity and CRM DocTypes | [`scripts/crmfrappe-client.py`](file:///var/www/.agents/skills/crmfrappe/scripts/crmfrappe-client.py) |
| **Physical Skill Attestation** | Deterministic validator verifying tokens (<700), links, and schemas | [`scripts/crmfrappe-validate.sh`](file:///var/www/.agents/skills/crmfrappe/scripts/crmfrappe-validate.sh) |

## Commands

```bash
# Execute two-level headless onboarding automation
python3 /var/www/.agents/skills/crmfrappe/scripts/crmfrappe-onboard.py

# Execute physical validation sensor
bash /var/www/.agents/skills/crmfrappe/scripts/crmfrappe-validate.sh

# Run live Frappe Cloud API health check
python3 /var/www/.agents/skills/crmfrappe/scripts/crmfrappe-client.py

# Ingest new lead directly via cURL
curl -s -X POST "${FRAPPE_URL}/api/resource/CRM%20Lead" \
  -H "Authorization: token ${FRAPPE_API_KEY}:${FRAPPE_API_SECRET}" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jane", "email": "lead@example.com", "status": "New"}'
```

## Resources
- **Usage Guide**: [`references/usage.md`](file:///var/www/.agents/skills/crmfrappe/references/usage.md)
- **Infrastructure Guide**: [`references/infra.md`](file:///var/www/.agents/skills/crmfrappe/references/infra.md)
- **Production Recipes**: [`assets/crmfrappe_production_recipes.json`](file:///var/www/.agents/skills/crmfrappe/assets/crmfrappe_production_recipes.json)
