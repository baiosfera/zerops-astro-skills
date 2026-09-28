# Frappe CRM — Infrastructure & Operational Engineering Reference (v1.0)

> **Governance Framework:** Supreme Directive v6.8 · Docu v5.5 · Fractal CoHaLo v6.0 · Continuous Present 2026 · SSoT Indivisible

---

## 1. Multi-Service Integration Topology

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            Astro Frontend Service                           │
│  - Hostname: frnt                                                           │
│  - Runtime: Node.js 22 LTS / Bun                                            │
│  - Role: High-performance SSR, Lead Capture forms, Client Portal           │
│  - Handoff: POST to /api/resource/CRM Lead or BullMQ async push             │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Valkey In-Memory Data Store                         │
│  - Hostname: valkey                                                         │
│  - Role: Fast session caching, BullMQ queues ('crm-lead-queue')             │
│  - Isolation: Protects Frappe Cloud from ingestion spikes                   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                 Frappe Cloud Bench Site (multi-tenant)                      │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      Shared MariaDB Database                        │   │
│   │  - Single database instance ($0 extra cost on shared site)          │   │
│   │  - Zero data duplication between CRM entities and ERP balances      │   │
│   └──────────────────┬───────────────────────────────┬──────────────────┘   │
│                      │                               │                      │
│                      ▼                               ▼                      │
│   ┌─────────────────────────────────────┐  ┌────────────────────────────┐   │
│   │       Frappe CRM (FCRM App)         │  │    ERPNext (Fiscal SoR)    │   │
│   │  - CRM Lead / Deal Pipeline         │  │  - Master Items & Warehouses│  │
│   │  - VoIP Twilio WebRTC Softphone     │─▶│  - Customer Master Auto-gen│   │
│   │  - WhatsApp Omnichannel Chat        │  │  - Quotation Prefill RPC   │   │
│   │  - Deals SLA & Escalation Worker    │  │  - Electronic Invoice DIAN │   │
│   └─────────────────────────────────────┘  └────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Environment Variables Dictionary

| Variable Name | Required | Default | Sensitivity | Description |
|---|---|---|---|---|
| `FRAPPE_URL` | Yes | `https://{{FRAPPE_SITE_NAME}}` | Public | Base URL of the Frappe Bench instance hosting ERPNext and CRM. |
| `FRAPPE_API_KEY` | Yes | N/A | High | API Key generated for administrative or service user in Frappe. |
| `FRAPPE_API_SECRET` | Yes | N/A | Critical | API Secret paired with `FRAPPE_API_KEY` for Token auth. |
| `FRAPPE_SITE_NAME` | Yes | `{{FRAPPE_SITE_NAME}}` | Public | Bench site identifier sent in multi-tenant HTTP headers. |
| `FRAPPE_COMPANY` | Yes | `{{COMPANY_LEGAL_NAME}}` | Public | Default fiscal Company owning converted deals and invoices. |
| `FRAPPE_WEBHOOK_SECRET`| No | N/A | Critical | HMAC-SHA256 secret for validating outbound Frappe webhooks. |
| `TWILIO_ACCOUNT_SID` | Optional | N/A | High | Twilio master Account SID for programmable voice. |
| `TWILIO_AUTH_TOKEN` | Optional | N/A | Critical | Twilio Auth Token for REST API and webhook signature checks. |
| `TWILIO_API_KEY` | Optional | N/A | High | Twilio API Key for generating in-browser WebRTC voice JWTs. |
| `TWILIO_API_SECRET` | Optional | N/A | Critical | Twilio API Secret for signing Voice Client JWT tokens. |
| `TWILIO_TWIML_APP_SID` | Optional | N/A | High | TwiML Application SID routing incoming/outgoing browser calls.|
| `TWILIO_CALLER_ID` | Optional | N/A | Public | Verified phone number shown as Caller ID on outbound calls. |
| `META_WA_PHONE_NUMBER_ID`| Optional| N/A | High | WhatsApp Business Account phone number ID from Meta Developers.|
| `META_WA_ACCESS_TOKEN` | Optional | N/A | Critical | Permanent System User Token for WhatsApp Cloud API. |
| `META_WEBHOOK_VERIFY_TOKEN`| Optional| N/A | High | Verification token configured in Meta App Webhook settings. |
| `VALKEY_URL` | Yes | `redis://valkey:6379` | Medium | Redis/Valkey connection string for BullMQ queue operations. |

---

## 3. Configuration & Deployment Runbooks

### Runbook 1: Twilio In-Browser Softphone Setup
1. In Twilio Console:
   - Create an API Key & Secret (`SK...`).
   - Create a TwiML App pointing Voice Request URL to:
     `https://<frappe-url>/api/method/crm.integrations.twilio.api.voice`
2. In Frappe Desk (`CRM Twilio Settings`):
   - Set `enabled = 1`.
   - Enter `account_sid`, `auth_token`, `api_key`, `api_secret`, `twiml_sid`.
   - Enable `record_calls = 1`.
3. In `CRM Telephony Agent`:
   - Assign user: `admin@{{COMPANY_DOMAIN}}`.
   - Set `call_receiving_device = "Computer"` (browser softphone).
   - Set `twilio_number` to verified business line.

### Runbook 2: WhatsApp Cloud API Integration
1. In Meta Developer Dashboard:
   - Configure Webhook Callback URL:
     `https://<frappe-url>/api/method/frappe_whatsapp.utils.webhook.webhook`
   - Set Verify Token matching `META_WEBHOOK_VERIFY_TOKEN`.
   - Subscribe to `messages` field.
2. In Frappe Desk:
   - Open `WhatsApp Settings` and enter `Phone Number ID` and `Access Token`.
   - Inbound messages automatically resolve to matching `Contact`, `CRM Lead` or `CRM Deal` by sender phone number.

### Runbook 3: Deal Won to ERPNext Customer Auto-Provisioning
1. In Frappe Desk, navigate to `ERPNext CRM Settings`:
   - Check `Enabled`.
   - Set `ERPNext Company` to `{{COMPANY_LEGAL_NAME}}`.
   - Set `Is ERPNext in Different Site` to `0` (shared bench mode).
   - Check `Sync Products` to link `CRM Product` with `Item`.
   - Check `Create Customer on Status Change`.
   - Set `Deal Status` to `Won`.
2. Operational Verification:
   - Upon moving any `CRM Deal` to `Won`, the system triggers `create_customer_in_erpnext()`, updates `deal.erpnext_customer`, and makes `prefill_quotation_items` available.

### Runbook 4: Headless Onboarding & Zero-Banner Setup (v1.1)
1. Context & Objective:
   - Suppress the 9-step Frappe CRM onboarding checklist across all existing and future users in clean-room ZCP deployments.
2. Execution via CLI Automation:
   ```bash
   # Dry-run inspection
   python3 scripts/crmfrappe-onboard.py --dry-run

   # Live execution (Level 1 + Level 2)
   python3 scripts/crmfrappe-onboard.py
   ```
3. Verification:
   - Level 1: Verify `User.onboarding_status` contains 9 completed steps for each `System User`.
   - Level 2: Verify `DocType/Server Script/User Auto Complete Onboarding` is active (`disabled: 0`).

---

## 4. Compiled Fractal CoHaLo Execution Harness

Every agent invoking or modifying `crmfrappe` MUST operate under these compiled bounds:

```yaml
fractal_harness:
  version: "6.0"
  process_hygiene:
    local_timeout: "10s"
    network_timeout: "15s"
    wait_ms_before_async: 10000
    orphan_task_termination: "manage_task action='kill'"
  circuit_breakers:
    max_consecutive_retries: 2
    escalate_on: "HTTP 401 Unauthorized, HTTP 403 Forbidden, Connection Timeout"
  sensors:
    http_probe:
      url: "${FRAPPE_URL}/api/method/frappe.auth.get_logged_user"
      expected_status: 200
      expected_header: "content-type: application/json"
    crm_module_probe:
      url: "${FRAPPE_URL}/api/resource/CRM%20Lead?limit_page_length=1"
      expected_status: 200
    file_system_probe:
      script: "bash scripts/crmfrappe-validate.sh"
      expected_exit_code: 0
```

---

## 5. Error Catalog & Remediation Matrix

| Error Code / Symptom | Root Cause | Remediation Protocol |
|---|---|---|
| `401 Invalid credentials` | Malformed or expired `FRAPPE_API_KEY` / `FRAPPE_API_SECRET`. | Re-generate API keys in Frappe Desk under User record -> API Access. Ensure header format is `Authorization: token <key>:<secret>`. |
| `403 Not Permitted` | User role lacks `read`/`write` permission on DocType `CRM Lead` or `CRM Deal`. | Assign `CRM User` or `CRM Manager` role to the API user in Frappe Desk. |
| `MandatoryError: lost_reason` | Transitioning `CRM Deal` to `Lost` without specifying `lost_reason`. | Supply a valid `CRM Lost Reason` in payload. If `Other`, also supply non-empty `lost_notes`. |
| `ItemNotFoundError: ERPNext Customer` | `ERPNext CRM Settings` enabled but company or customer group missing. | Ensure Company `{{COMPANY_LEGAL_NAME}}` exists and Customer Group `All Customer Groups` is present. |
| `Twilio WebRTC 31208` | Browser client token expired or invalid identity string. | Re-fetch access token via `/api/method/crm.integrations.twilio.api.generate_access_token`. Check agent email formatting. |
| `BullMQ ETIMEDOUT` | Valkey container unavailable or network partition. | Verify Valkey service state via `zerops_verify` or reconnect socket. |
