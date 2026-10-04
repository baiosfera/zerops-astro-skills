# Frappe CRM — Operational Reference Manual (v1.1)

> **Governance Framework:** Supreme Directive v6.8 · Docu v5.5 · Zero Deletion Invariant · Frappe CRM v1.83+ (Continuous Present 2026) · SSoT Indivisible

---

## 1. 4D Architectural Comparison Matrix

| Architectural Dimension | Frappe CRM (v1.83+ / FCRM) | HubSpot CRM | Salesforce Sales Cloud | Zoho CRM |
|---|---|---|---|---|
| **Underlying Architecture** | Frappe Framework (Python/MariaDB) + Vue 3 SPA | Proprietary Multi-tenant Cloud | Force.com Multi-tenant Cloud | Proprietary SaaS Stack |
| **Hosting & Data Sovereignty** | 100% Self-hostable / Frappe Cloud Shared Bench | Closed SaaS (US/EU Data Centers) | Closed SaaS (Global Hyperscalers) | Closed SaaS (Proprietary DC) |
| **ERP Co-location** | Zero-latency shared MariaDB with ERPNext | REST API / Third-party sync (HubSpot-to-ERP) | Mulesoft / Integration Middleware | Zoho One / REST Connectors |
| **Cost at Scale (100 Users)** | $5–$25/mo (Server/Bench cost only) | $5,000–$12,000/mo (Seat tiers) | $15,000–$30,000/mo (Enterprise) | $2,000–$4,500/mo (Enterprise) |
| **Omnichannel VoIP** | Native WebRTC softphone via Twilio/Exotel | Native VoIP / Twilio Bridge | CTI / OpenCTI integrations | Native Zoho PhoneBridge |
| **WhatsApp Integration** | Native bidirectional via `frappe_whatsapp` | Meta integration add-on | Digital Engagement add-on | Native WhatsApp Business |
| **Customizability** | Custom DocTypes, Client Scripts, Jinja, Hooks | Custom Objects (Enterprise only) | Apex, Visualforce, LWC | Deluge Scripts, Custom Modules |

---

## 2. DocType Schemas & Field Catalog

### 2.1 `CRM Lead` (DocType: `CRM Lead`, Module: `FCRM`)
* **Naming Series:** `CRM-LEAD-.YYYY.-`
* **Mandatory Core Fields:**
  * `first_name` (`Data`): Lead contact first name.
  * `status` (`Link` -> `CRM Lead Status`): Qualification stage (defaults to `New`).
* **Identity & Demographics:**
  * `salutation` (`Link` -> `Salutation`), `middle_name`, `last_name`
  * `lead_name` (`Data`): Evaluated full name.
  * `email` (`Data`), `mobile_no` (`Data` / Phone), `phone` (`Data` / Phone)
  * `gender` (`Link` -> `Gender`), `job_title` (`Data`)
  * `organization` (`Data` in Lead, auto-converted to `CRM Organization` upon conversion)
  * `website` (`Data`), `industry` (`Link` -> `CRM Industry`), `territory` (`Link` -> `CRM Territory`)
  * `no_of_employees` (`Select`: `1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `1000+`)
  * `annual_revenue` (`Currency`), `company_description` (`Text`), `organization_logo` (`Attach Image`)
* **Pipeline & SLA Metadata:**
  * `source` (`Link` -> `CRM Lead Source`, e.g., `Web Form`, `Meta Lead Ads`, `Directus`, `Inbound WhatsApp`)
  * `lead_owner` (`Link` -> `User`): Automatic docshare permission granted on assignment.
  * `converted` (`Check`): Set to `1` when converted to deal.
  * `sla` (`Link` -> `CRM Service Level Agreement`), `sla_creation`, `sla_status` (`First Response Due`, `Rolling Response Due`, `Failed`, `Fulfilled`)
  * `first_response_time`, `first_responded_on`, `last_response_time`, `last_responded_on`, `response_by`
  * `lost_reason` (`Link` -> `CRM Lost Reason`), `lost_notes` (`Text`, mandatory when `lost_reason == "Other"`)
* **Child Tables:**
  * `products` (`Table` -> `CRM Products`): Proposed line items before deal inception.
  * `rolling_responses` (`Table` -> `CRM Rolling Response Time`)
  * `status_change_log` (`Table` -> `CRM Status Change Log`)
  * `total` (`Currency`), `net_total` (`Currency`)
* **Ad Attribution:** `facebook_lead_id` (`Data`), `facebook_form_id` (`Data`)

### 2.2 `CRM Deal` (DocType: `CRM Deal`, Module: `FCRM`)
* **Naming Series:** `CRM-DEAL-.YYYY.-`
* **Mandatory Core Fields:**
  * `status` (`Link` -> `CRM Deal Status`): e.g., `Qualification`, `Proposal`, `Negotiation`, `Won`, `Lost`.
* **Financial & Forecasting Fields:**
  * `probability` (`Percent`): Auto-populated from `CRM Deal Status.probability` upon status transition.
  * `deal_value` (`Currency`): Actual contracted or estimated value.
  * `expected_deal_value` (`Currency`): Computed from `total` or status probability formula.
  * `expected_closure_date` (`Date`): Target milestone date.
  * `closed_date` (`Date`): Auto-stamped with `nowdate()` when status type reaches `Won`.
  * `next_step` (`Data`): Tactical operational follow-up.
  * `deal_owner` (`Link` -> `User`).
* **Entity Associations:**
  * `organization` (`Link` -> `CRM Organization`), `organization_name` (`Data`)
  * `lead` (`Link` -> `CRM Lead`), `lead_name` (`Data`)
  * `erpnext_customer` (`Data`): Direct reference to ERPNext `Customer` record.
  * `source` (`Link` -> `CRM Lead Source`), `currency` (`Link` -> `Currency`), `exchange_rate` (`Float`)
* **Primary Contact Aggregates:**
  * `contact` (`Link` -> `Contact`), `first_name`, `last_name`, `email`, `mobile_no`, `phone`
* **Child Tables:**
  * `contacts` (`Table` -> `CRM Contacts`): Multi-stakeholder deal engagement matrix.
  * `products` (`Table` -> `CRM Products`): Itemized line items under negotiation.
  * `rolling_responses` (`Table` -> `CRM Rolling Response Time`)
  * `status_change_log` (`Table` -> `CRM Status Change Log`)
* **Lost Reason Governance:**
  * `lost_reason` (`Link` -> `CRM Lost Reason`): Mandatory when status is categorized as `Lost`.
  * `lost_notes` (`Text`): Mandatory when `lost_reason` is `"Other"`.

### 2.3 `CRM Product` & Child Table `CRM Products`
* **Catalog Entity (`CRM Product`):**
  * `product_code` (`Data`, unique identifier, autoname `field:product_code`)
  * `product_name` (`Data`), `standard_rate` (`Currency`), `disabled` (`Check`)
  * `description` (`Text Editor`), `image` (`Attach Image`)
  * `erpnext_item_code` (`Data`, read-only link to ERPNext `Item.item_code`)
* **Negotiation Line Item (`CRM Products` Child Table):**
  * `product_code` (`Link` -> `CRM Product`, required)
  * `product_name` (`Data`), `qty` (`Float`, default `1.0`), `rate` (`Currency`)
  * `discount_percentage` (`Percent`), `discount_amount` (`Currency`)
  * `amount` (`Currency` = `qty * rate`), `net_amount` (`Currency` = `amount - discount_amount`)

### 2.4 `CRM Call Log` & VoIP Entities
* **Call Telemetry (`CRM Call Log`):**
  * `id` (`Data`, Twilio `CallSid` or UUID)
  * `caller` (`Link` -> `User`), `receiver` (`Link` -> `User`)
  * `type` (`Select`: `Incoming`, `Outgoing`)
  * `status` (`Select`: `Initiated`, `Ringing`, `In Progress`, `Completed`, `Failed`, `Busy`, `No Answer`, `Queued`, `Canceled`)
  * `duration` (`Duration`, seconds)
  * `from` (`Data`), `to` (`Data`)
  * `telephony_medium` (`Select`: `Manual`, `Twilio`, `Exotel`)
  * `recording_url` (`SmallText`), `recording_url_path` (`SmallText`, SSRF-proxied stream endpoint)
  * `reference_doctype` (`Link` -> `DocType`), `reference_docname` (`Dynamic Link`)
  * `start_time` (`Datetime`), `end_time` (`Datetime`)
* **Twilio Configuration (`CRM Twilio Settings` Single DocType):**
  * `enabled` (`Check`), `account_sid` (`Data`), `auth_token` (`Password`), `api_key` (`Data`), `api_secret` (`Password`), `twiml_sid` (`Data`), `record_calls` (`Check`).

---

## 3. Whitelisted RPC API Methods

Authentication for all endpoints requires:
`Authorization: token <api_key>:<api_secret>`

### 3.1 Lead to Deal Conversion
* **RPC Endpoint:** `POST /api/method/crm.fcrm.doctype.crm_lead.crm_lead.convert_to_deal`
* **Payload:**
```json
{
  "lead": "CRM-LEAD-2026-00042",
  "deal": {
    "status": "Qualification",
    "expected_deal_value": 45000000.0,
    "expected_closure_date": "2026-10-31"
  },
  "existing_contact": null,
  "existing_organization": null
}
```
* **Response:** `{"message": "CRM-DEAL-2026-00018"}`

### 3.2 Programmatic Deal Inception
* **RPC Endpoint:** `POST /api/method/crm.fcrm.doctype.crm_deal.crm_deal.create_deal`
* **Payload:**
```json
{
  "doc": {
    "organization_name": "Empresa Ejemplo S.A.S.",
    "first_name": "Carlos",
    "last_name": "Gómez",
    "email": "carlos.gomez@ejemplo.co",
    "mobile_no": "+573001234567",
    "currency": "COP",
    "deal_value": 85000000.0,
    "status": "Qualification"
  }
}
```
* **Response:** `{"message": "CRM-DEAL-2026-00019"}`

### 3.3 Prefill ERPNext Quotation Items from Deal
* **RPC Endpoint:** `POST /api/method/crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings.prefill_quotation_items`
* **Payload:** `{"crm_deal": "CRM-DEAL-2026-00018"}`
* **Response:**
```json
{
  "message": [
    {
      "item_code": "PROD-SPA-001",
      "qty": 5.0,
      "price_list_rate": 1200000.0,
      "discount_percentage": 5.0
    }
  ]
}
```

### 3.4 Prefilled Quotation URL Generator for ERPNext Desk
* **RPC Endpoint:** `POST /api/method/crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings.get_quotation_url`
* **Payload:** `{"crm_deal": "CRM-DEAL-2026-00018", "organization": "Inversiones San Jerónimo S.A.S."}`
* **Response:**
```json
{
  "message": "/app/quotation/new?quotation_to=Customer&crm_deal=CRM-DEAL-2026-00018&party_name=Inversiones+Ejemplo+S.A.S.&company={{COMPANY_LEGAL_NAME}}"
}
```

---

## 4. Production Code Patterns

### Pattern 1: Inbound Web Lead Capture (Astro Server Action / TypeScript)
```typescript
import { defineAction, z } from 'astro:actions';

export const server = {
  submitLead: defineAction({
    accept: 'form',
    input: z.object({
      firstName: z.string().min(2),
      lastName: z.string().optional(),
      email: z.string().email(),
      phone: z.string().regex(/^\+?[1-9]\d{7,14}$/),
      company: z.string().optional(),
      notes: z.string().optional(),
    }),
    handler: async (input) => {
      const frappeUrl = process.env.FRAPPE_URL?.replace(/\/$/, '');
      const apiKey = process.env.FRAPPE_API_KEY;
      const apiSecret = process.env.FRAPPE_API_SECRET;

      if (!frappeUrl || !apiKey || !apiSecret) {
        throw new Error('Frappe credentials missing from environment');
      }

      const payload = {
        first_name: input.firstName,
        last_name: input.lastName || '',
        email: input.email,
        mobile_no: input.phone,
        organization: input.company || '',
        source: 'Web Form',
        status: 'New',
        details: input.notes || '',
      };

      const res = await fetch(`${frappeUrl}/api/resource/CRM Lead`, {
        method: 'POST',
        headers: {
          'Authorization': `token ${apiKey}:${apiSecret}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorDetails = await res.text();
        throw new Error(`Frappe Lead Ingest Failed (${res.status}): ${errorDetails}`);
      }

      const { data } = await res.json();
      return { success: true, leadId: data.name };
    },
  }),
};
```

### Pattern 2: Deal Pipeline Lifecycle & Won/Lost Automation (Python)
```python
#!/usr/bin/env python3
import requests

class FrappeCRMManager:
    def __init__(self, base_url: str, api_key: str, api_secret: str):
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"token {api_key}:{api_secret}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def set_deal_stage(self, deal_name: str, status: str, lost_reason: str = None, lost_notes: str = None):
        url = f"{self.base_url}/api/resource/CRM Deal/{deal_name}"
        payload = {"status": status}

        if status == "Lost":
            if not lost_reason:
                raise ValueError("lost_reason is mandatory when setting Deal to Lost")
            payload["lost_reason"] = lost_reason
            if lost_reason == "Other":
                if not lost_notes:
                    raise ValueError("lost_notes is mandatory when lost_reason is Other")
                payload["lost_notes"] = lost_notes

        res = requests.put(url, headers=self.headers, json=payload, timeout=10)
        res.raise_for_status()
        deal = res.json().get("data", {})

        if status == "Won":
            print(f"[+] Deal {deal_name} won! Linked Customer: {deal.get('erpnext_customer')}")
        return deal
```

### Pattern 3: Twilio Voice Inbound TwiML Server (Node.js / Express)
```typescript
import express from 'express';
import twilio from 'twilio';

const app = express();
app.use(express.urlencoded({ extended: true }));

app.post('/api/twilio/voice', (req, res) => {
  const { From, CallSid } = req.body;
  const voice = new twilio.twiml.VoiceResponse();
  const frappeUrl = process.env.FRAPPE_URL;

  const dial = voice.dial({
    callerId: From,
    record: 'record-from-answer',
    recordingStatusCallback: `${frappeUrl}/api/method/crm.integrations.twilio.api.update_recording_info`,
    recordingStatusCallbackEvent: ['completed'],
  });

  const agentIdentity = (process.env.DEFAULT_AGENT_EMAIL || 'admin@{{COMPANY_DOMAIN}}').replace('@', '(at)');

  dial.client({
    statusCallback: `${frappeUrl}/api/method/crm.integrations.twilio.api.update_call_status_info`,
    statusCallbackEvent: ['initiated', 'ringing', 'answered', 'completed'],
    statusCallbackMethod: 'POST',
  }, agentIdentity);

  res.type('text/xml');
  res.send(voice.toString());
});
```

### Pattern 4: Asynchronous Lead Ingestion Worker (Valkey / BullMQ)
```typescript
import { Worker, Job } from 'bullmq';
import Redis from 'ioredis';

const connection = new Redis(process.env.VALKEY_URL || 'redis://valkey:6379');

export const crmWorker = new Worker(
  'crm-lead-queue',
  async (job: Job) => {
    const { contact, source } = job.data;
    const frappeUrl = process.env.FRAPPE_URL?.replace(/\/$/, '');
    const apiKey = process.env.FRAPPE_API_KEY;
    const apiSecret = process.env.FRAPPE_API_SECRET;

    const res = await fetch(`${frappeUrl}/api/resource/CRM Lead`, {
      method: 'POST',
      headers: {
        'Authorization': `token ${apiKey}:${apiSecret}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        first_name: contact.firstName,
        last_name: contact.lastName || '',
        email: contact.email,
        mobile_no: contact.phone,
        organization: contact.company || '',
        source: source || 'BullMQ Sync',
        status: 'New',
      }),
    });

    if (!res.ok) {
      throw new Error(`Failed to ingest lead: ${await res.text()}`);
    }

    const payload = await res.json();
    return { leadName: payload.data.name };
  },
  { connection, concurrency: 5 }
);
```

### Pattern 5: Deal Won to ERPNext Quotation Handoff (Python)
```python
#!/usr/bin/env python3
import requests

def convert_deal_to_erpnext_quotation(base_url: str, api_key: str, api_secret: str, lead_id: str):
    headers = {
        "Authorization": f"token {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }

    # Step 1: Convert Lead to Deal
    c_res = requests.post(
        f"{base_url}/api/method/crm.fcrm.doctype.crm_lead.crm_lead.convert_to_deal",
        headers=headers,
        json={"lead": lead_id},
        timeout=10
    )
    c_res.raise_for_status()
    deal_name = c_res.json()["message"]

    # Step 2: Transition Deal to Won (triggers ERPNext Customer creation)
    d_res = requests.put(
        f"{base_url}/api/resource/CRM Deal/{deal_name}",
        headers=headers,
        json={"status": "Won"},
        timeout=10
    )
    d_res.raise_for_status()
    customer_id = d_res.json()["data"].get("erpnext_customer")

    # Step 3: Fetch prefilled items
    p_res = requests.post(
        f"{base_url}/api/method/crm.fcrm.doctype.erpnext_crm_settings.erpnext_crm_settings.prefill_quotation_items",
        headers=headers,
        json={"crm_deal": deal_name},
        timeout=10
    )
    p_res.raise_for_status()
    items = p_res.json().get("message", [])

    # Step 4: Instantiate Quotation
    quotation_doc = {
        "doctype": "Quotation",
        "quotation_to": "Customer" if customer_id else "CRM Deal",
        "party_name": customer_id or deal_name,
        "crm_deal": deal_name,
        "company": "{{COMPANY_LEGAL_NAME}}",
        "order_type": "Sales",
        "items": items
    }
    q_res = requests.post(f"{base_url}/api/resource/Quotation", headers=headers, json=quotation_doc, timeout=10)
    q_res.raise_for_status()
    return q_res.json()["data"]["name"]
```

---

## 6. Two-Level Headless Onboarding & Zero-Banner Architecture (v1.1)

### 6.1 Architectural Mechanism
Frappe CRM tracks onboarding state per user inside the `User` DocType under field `onboarding_status`:
```json
{
  "frappecrm_onboarding_status": [
    {"name": "setup_your_password", "completed": true},
    {"name": "create_first_lead", "completed": true},
    {"name": "invite_your_team", "completed": true},
    {"name": "convert_lead_to_deal", "completed": true},
    {"name": "create_first_task", "completed": true},
    {"name": "create_first_note", "completed": true},
    {"name": "add_first_comment", "completed": true},
    {"name": "send_first_email", "completed": true},
    {"name": "change_deal_status", "completed": true}
  ]
}
```
When all 9 steps evaluate to `completed: true`, `useOnboarding('frappecrm')` in `AppSidebar.vue` sets `isOnboardingStepsCompleted.value = true`, completely suppressing the `<GettingStartedBanner />` widget and rendering the clean `<HelpModal />` action instead.

### 6.2 Level 1: CLI Batch Synchronization (`scripts/crmfrappe-onboard.py`)
Queries all `System User` records and patches their `onboarding_status` via REST API.

### 6.3 Level 2: Backend Server Script Hook (`User Auto Complete Onboarding`)
Registered as a `DocType Event` on `User` `Before Insert`:
```python
import json

steps = [
    {"name": "setup_your_password", "completed": True},
    {"name": "create_first_lead", "completed": True},
    {"name": "invite_your_team", "completed": True},
    {"name": "convert_lead_to_deal", "completed": True},
    {"name": "create_first_task", "completed": True},
    {"name": "create_first_note", "completed": True},
    {"name": "add_first_comment", "completed": True},
    {"name": "send_first_email", "completed": True},
    {"name": "change_deal_status", "completed": True}
]

status = {}
if doc.onboarding_status:
    try:
        status = json.loads(doc.onboarding_status) if isinstance(doc.onboarding_status, str) else doc.onboarding_status
    except Exception:
        status = {}

if not status.get("frappecrm_onboarding_status"):
    status["frappecrm_onboarding_status"] = steps
    doc.onboarding_status = json.dumps(status)
```

---

## 7. High-Throughput Batch Lead Ingestion (`frappe.client.insert_many`)

Ingesting marketing leads from advertising platforms (Meta Lead Ads, TikTok, Google Ads) or high-volume cold outreach campaigns individually creates substantial HTTP latency and thread contention on Frappe Cloud. Frappe CRM supports batch ingestion of up to 200 `CRM Lead` documents in a single atomic transaction.

### A. Batch Creation Endpoint
- **Endpoint:** `POST /api/method/frappe.client.insert_many`
- **Headers:** `Authorization: token API_KEY:API_SECRET`, `Content-Type: application/json`

### B. Payload Structure
```json
{
  "docs": [
    {
      "doctype": "CRM Lead",
      "first_name": "Mateo",
      "last_name": "Gómez",
      "email": "mateo.gomez@example.com",
      "mobile_no": "+573001234567",
      "organization": "Andes Tech SAS",
      "status": "New",
      "source": "Meta Lead Ads"
    },
    {
      "doctype": "CRM Lead",
      "first_name": "Camila",
      "last_name": "Restrepo",
      "email": "camila.restrepo@example.com",
      "mobile_no": "+573109876543",
      "organization": "Boutique Café",
      "status": "New",
      "source": "Web Form"
    }
  ]
}
```

### C. Python Ingestion Engine
```python
import os
import requests

def ingest_leads_batch(leads_data: list) -> list:
    url = f"{os.getenv('FRAPPE_URL').rstrip('/')}/api/method/frappe.client.insert_many"
    headers = {
        "Authorization": f"token {os.getenv('FRAPPE_API_KEY')}:{os.getenv('FRAPPE_API_SECRET')}",
        "Content-Type": "application/json"
    }
    payload = {
        "docs": [{"doctype": "CRM Lead", **lead} for lead in leads_data]
    }
    res = requests.post(url, headers=headers, json=payload, timeout=10)
    res.raise_for_status()
    return res.json().get("message", [])
```

---

## 8. Multimedia, Telemetry & File Attachments in Frappe CRM

Frappe CRM enables linking multimedia assets (company logos, customer identification, and Twilio/Exotel VoIP call recordings) directly to CRM DocTypes using `/api/method/upload_file`.

### A. Uploading Organization Logo
```bash
curl -X POST "${FRAPPE_URL}/api/method/upload_file" \
  -H "Authorization: token ${FRAPPE_API_KEY}:${FRAPPE_API_SECRET}" \
  -F "file=@/path/to/logo.png" \
  -F "filename=andes_tech_logo.png" \
  -F "is_private=0" \
  -F "doctype=CRM Organization" \
  -F "docname=Andes Tech SAS" \
  -F "fieldname=organization_logo"
```
*Note: Setting `is_private=0` allows Desk and client portals to render the company logo publicly.*

### B. Uploading VoIP Call Recording (`CRM Call Log`)
For compliance and telemetry storage, recorded softphone calls are saved to protected private storage:
```bash
curl -X POST "${FRAPPE_URL}/api/method/upload_file" \
  -H "Authorization: token ${FRAPPE_API_KEY}:${FRAPPE_API_SECRET}" \
  -F "file=@/tmp/call_recording_sid123.mp3" \
  -F "filename=call_20260907_sid123.mp3" \
  -F "is_private=1" \
  -F "doctype=CRM Call Log" \
  -F "docname=CL-2026-00892" \
  -F "fieldname=recording_url"
```

---

## 9. Pipeline Analytics & High-Precision Timespan Filtering

Frappe REST API includes dynamic time-range operators (`timespan`) and compound filters, allowing instant generation of sales pipeline dashboards without server-side custom scripts.

### A. Query Deals Won During the Current Month
```typescript
const params = new URLSearchParams({
  fields: JSON.stringify(['name', 'organization', 'deal_value', 'currency', 'closed_date', 'deal_owner']),
  filters: JSON.stringify([
    ['CRM Deal', 'status', '=', 'Won'],
    ['CRM Deal', 'closed_date', 'timespan', 'this month']
  ]),
  order_by: 'deal_value desc'
});

const response = await fetch(`${FRAPPE_URL}/api/resource/CRM%20Deal?${params.toString()}`, {
  headers: {
    'Authorization': `token ${API_KEY}:${API_SECRET}`,
    'Accept': 'application/json'
  }
});
```

### B. Supported `timespan` Operator Literals
- `today`, `yesterday`, `this week`, `last week`
- `this month`, `last month`, `this quarter`, `last quarter`
- `this year`, `last year`, `last 7 days`, `last 30 days`

### C. Identifying Stagnant Deals (High Value & Approaching Close Date)
```json
[
  ["CRM Deal", "status", "not in", ["Won", "Lost"]],
  ["CRM Deal", "deal_value", ">=", 10000000],
  ["CRM Deal", "expected_closure_date", "<=", "2026-09-30"],
  ["CRM Deal", "probability", ">=", 60]
]
```

---

## 10. Declarative Webhook Dispatch & Cryptographic HMAC-SHA256 Verification

Frappe Framework provides native event dispatching through the `Webhook` DocType. When a `CRM Deal` transitions to `Won`, Frappe immediately fires an HTTP POST payload to the configured consumer endpoint (e.g. `bknd`/Directus or BullMQ worker).

### A. Declarative Webhook Configuration (`DocType: Webhook`)
- **Webhook Name:** `FCRM Deal Won Notification`
- **Webhook DocType:** `CRM Deal`
- **Webhook Event:** `on_update`
- **Condition:** `doc.status == "Won" and doc.has_value_changed("status")`
- **Request URL:** `https://api.domain.com/webhooks/crm/deal-won`
- **Webhook Secret:** Configured in Frappe Webhook to compute HMAC-SHA256.

### B. Constant-Time HMAC-SHA256 Signature Verification (Node.js / Express)
Frappe delivers the signature in the `X-Frappe-Webhook-Signature` request header. Consumers MUST verify authenticity using constant-time comparison to prevent timing attacks:

```typescript
import crypto from 'crypto';
import { Request, Response } from 'express';

export function verifyFrappeWebhook(req: Request, secret: string): boolean {
  const signature = req.headers['x-frappe-webhook-signature'] as string;
  if (!signature) return false;

  // Compute expected HMAC-SHA256 using the raw request body
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(req.rawBody); // Ensure body-parser exposes rawBuffer
  const expectedSignature = hmac.digest('hex');

  const sigBuffer = Buffer.from(signature, 'hex');
  const expectedBuffer = Buffer.from(expectedSignature, 'hex');

  if (sigBuffer.length !== expectedBuffer.length) {
    return false;
  }

  return crypto.timingSafeEqual(sigBuffer, expectedBuffer);
}
```

