# ERPNext & Frappe Cloud: Infrastructure, Queue Workers & Console Runbook (v2.3)

This manual provides production-grade infrastructure blueprints, environment variable specifications for Frappe Cloud / ERPNext integration, BullMQ worker configuration on Valkey 7.2, and the Fractal CoHaLo operational harness for `erpnext` running in Zerops.

---

## 1. Multi-Service Integration Topology in Zerops


```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Internal High-Speed Network                                                                     │
│                                                                                                        │
│   ┌──────────────────────────────────────────────────┐                                                 │
│   │ Directus 11+ Headless CMS (directus)             │                                                 │
│   │ (nodejs@24 / os: ubuntu)                         │                                                 │
│   │ ├─ Hook: `orders.items.create` (defineHook)      │                                                 │
│   │ └─ Endpoint: `/frappe/webhook` (HMAC-SHA256)     │                                                 │
│   └───────────────┬──────────────────────────▲───────┘                                                 │
│                   │ Enqueues order sync      │ Updates stock_quantity                                  │
│                   ▼                          │ (with `_sync_source: frappe`)                           │
│   ┌──────────────────────────────────────────┴───────┐                                                 │
│   │ Valkey 7.2 In-Memory (cache:6379)                │                                                 │
│   │ ├─ Queue: `sync-to-frappe` (BullMQ)              │                                                 │
│   │ └─ Distributed Locks: `lock:sync:order:<id>`     │                                                 │
│   └───────────────┬──────────────────────────────────┘                                                 │
│                   │ Dispatches job                                                                     │
│                   ▼                                                                                    │
│   ┌──────────────────────────────────────────────────┐                                                 │
│   │ ERPNext Sync Worker (aiworker / directus)        │                                                 │
│   │ (bun@1.3 / nodejs@24)                            │                                                 │
│   │ ├─ 1. Authenticates: `Authorization: token ...`  │                                                 │
│   │ ├─ 2. POST /api/resource/Sales Order             │                                                 │
│   │ └─ 3. Emits NATS event `events.erp.synced`       │                                                 │
│   └───────────────┬──────────────────────────────────┘                                                 │
│                   │ HTTPS REST API                                                                     │
│                   ▼                                                                                    │
│   ┌──────────────────────────────────────────────────┐                                                 │
│   │ External Frappe Cloud / ERPNext v15-v16 ($0 SaaS)│                                                 │
│   │ ├─ DocTypes: Customer, Item, Sales Order         │                                                 │
│   │ ├─ DIAN Electronic Invoicing (CUFE / QR)         │                                                 │
│   │ └─ Outgoing HMAC Webhooks (X-Frappe-Webhook-Sig) │                                                 │
│   └──────────────────────────────────────────────────┘                                                 │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Environment Variables Reference Dictionary

```ini
# ============================================================================
# FRAPPE CLOUD / ERPNEXT CREDENTIALS & HEADLESS SETTINGS
# ============================================================================
FRAPPE_URL="https://your-company.frappe.cloud"
FRAPPE_API_KEY="9a8b7c6d5e4f3a2b"
FRAPPE_API_SECRET="1a2b3c4d5e6f7a8b"
FRAPPE_WEBHOOK_SECRET="super_secret_hmac_key_32_chars_long"
FRAPPE_SITE_NAME="frontend"
ERPNEXT_HEADLESS_ONBOARDING="0"  # Injected into System Settings.enable_onboarding

# ============================================================================
# AMAZON SES v2 OUTBOUND SMTP (ERP & FISCAL NAMESPACE EXCLUSIVE)
# ============================================================================
# Injected via unisetup.sh / setup-keys.sh from client *-keys.md
AWS_ACCESS_KEY_ID="AKIA..."
AWS_SECRET_ACCESS_KEY="B..."     # Pre-calculated SES SMTP password (prefix B...)
AWS_REGION="us-east-1"
AWS_SES_CONFIGURATION_SET="deliverability-set"
AWS_SES_DEFAULT_FROM="notifications@{{COMPANY_DOMAIN}}"

# NOTE (Disjoint Namespace Invariant):
# Generic SMTP_* and ZEPTOMAIL_* variables are reserved strictly for Directus /
# bknd customer marketing dispatch and are completely ignored by ERPNext.

# ============================================================================
# ZEROPS INFRASTRUCTURE
# ============================================================================
VALKEY_CONNECTION_STRING="redis://cache:6379"
DIRECTUS_URL="http://directus:8055"
```

---

## 3. Third-Party Console Setup Runbook: Frappe Cloud

1. Log in to your ERPNext / Frappe Cloud instance as an **Administrator**.
2. In the global search bar, type **User List** and select the designated integration user.
3. Scroll down to the **API Access** section and click **Generate Keys**.
4. Copy the **API Key** and **API Secret** immediately (*the Secret is only displayed once*).
5. In the global search bar, type **Webhook** $\to$ Click **Add Webhook**:
   - **DocType:** `Sales Invoice` (or `Item`, `Stock Ledger Entry`).
   - **Webhook Doctype Event:** `after_insert` / `on_submit` / `on_update`.
   - **Request URL:** `https://cms.yourdomain.com/frappe/webhook`.
   - **Webhook Secret:** Set a secure random string and configure it as `FRAPPE_WEBHOOK_SECRET` in Zerops.
6. Test webhook delivery using Frappe's native preview tool.

---

## 4. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with `erpnext` must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All Frappe REST API calls and webhooks must use explicit timeouts (`timeout 10s curl -f ...`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all background sync workers using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Frappe Cloud Ping check: `curl -s -o /dev/null -w "%{http_code}" https://your-company.frappe.cloud/api/method/ping` $\implies$ Expected: `200`.
* **Circuit Breaker Policy**: If Frappe Cloud returns 429 Too Many Requests or 502/503 errors, BullMQ worker retries with exponential backoff (delay: 2000ms, max 5 attempts) without dropping messages.
