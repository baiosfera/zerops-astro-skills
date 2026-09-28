# ERPNext & Frappe Cloud REST API Developer Reference Manual (v2.4)

`erpnext` is the master enterprise ERP and Colombian DIAN electronic invoicing integration suite for the Zerops sovereign stack. Under the strict **$0 SaaS licensing and strict Authority Separation (SSoT)** governance model, it integrates **Frappe Cloud / ERPNext v15-v16** with Directus 11+ using token-authenticated REST operations, BullMQ queues on Valkey 7.2, HMAC-SHA256 verified webhooks, and formal Colombian DIAN e-invoicing pipelines (UBL 2.1).

---

## 1. 4D Comparative Architectural Matrix

| Enterprise Dimension | Frappe Cloud ERPNext (Target) | SAP Business One | Oracle NetSuite | Odoo Community/Enterprise |
|---|---|---|---|---|
| **SaaS Licensing Cost** | **$0 SaaS** (Open Source / Frappe Cloud) | $3,000–$5,000 / user / year | $10,000+ / year base | Free / $25 / user / month |
| **REST API & Extensibility** | **Native in Python/DocTypes (v15/v16)** | Service Layer SOAP/REST | Proprietary SuiteScript | XML-RPC / JSON-RPC |
| **Colombian DIAN Invoicing** | **Native UBL 2.1 (CUFE & QR)** | Expensive 3rd-party add-on | Expensive 3rd-party add-on | Paid community module |
| **Directus/Node Integration** | **HTTP Token Auth + BullMQ (<1ms lock)** | Heavy enterprise middleware | Complex integration engine | Slow XML-RPC wrappers |
| **Zerops Execution** | **100% Native on async worker mesh** | Requires dedicated heavy VM | Closed multi-tenant cloud | Requires dedicated Postgres |

---

## 2. Canonical REST Endpoints & DocType Resources

### A. Standard CRUD Operations
- **List Resources:** `GET /api/resource/:doctype`
- **Create Resource:** `POST /api/resource/:doctype`
- **Read Single Document:** `GET /api/resource/:doctype/:name`
- **Update Document:** `PUT /api/resource/:doctype/:name`
- **Delete Document:** `DELETE /api/resource/:doctype/:name`

### B. Python RPC Method Calls
- `GET /api/method/:dotted.path.to.method`
- `POST /api/method/:dotted.path.to.method` (Requires `@frappe.whitelist()` decorator)

---

## 3. Authentication & Request Headers

All Frappe REST API requests require:

```http
Authorization: token API_KEY:API_SECRET
Content-Type: application/json
Accept: application/json
```

> **Invariant:** Always concatenate `API_KEY` and `API_SECRET` separated by a single colon (`:`) and prefixed with the literal word `token`.

---

## 4. Filters, Projections & Pagination (TypeScript)

```typescript
export async function getStockItems(frappeUrl: string, apiKey: string, apiSecret: string) {
  const params = new URLSearchParams({
    fields: JSON.stringify(['name', 'item_name', 'item_group', 'standard_rate', 'valuation_rate']),
    filters: JSON.stringify([
      ['Item', 'is_stock_item', '=', 1],
      ['Item', 'disabled', '=', 0]
    ]),
    order_by: 'item_name asc',
    limit_start: '0',
    limit_page_length: '50'
  });

  const response = await fetch(`${frappeUrl}/api/resource/Item?${params.toString()}`, {
    method: 'GET',
    headers: {
      'Authorization': `token ${apiKey}:${apiSecret}`,
      'Accept': 'application/json'
    }
  });

  if (!response.ok) {
    throw new Error(`Frappe API Error: ${response.status} ${response.statusText}`);
  }

  const result = await response.json();
  return result.data;
}
```

---

## 5. Sales Order & Sales Invoice Creation with Child Tables

### Document Status Lifecycle (`docstatus`)
* `docstatus: 0` $\implies$ **Draft** (Editable, no accounting/stock impact).
* `docstatus: 1` $\implies$ **Submitted** (Formalized, ledger & inventory booked).
* `docstatus: 2` $\implies$ **Cancelled** (Voided ledger transaction).

```typescript
export async function createSalesOrder(
  frappeUrl: string,
  apiKey: string,
  apiSecret: string,
  orderData: {
    customer: string;
    delivery_date: string;
    items: Array<{ item_code: string; qty: number; rate: number; warehouse?: string }>;
    directus_order_id: string;
  }
) {
  const payload = {
    customer: orderData.customer,
    delivery_date: orderData.delivery_date,
    po_no: orderData.directus_order_id,
    items: orderData.items.map(item => ({
      item_code: item.item_code,
      qty: item.qty,
      rate: item.rate,
      warehouse: item.warehouse || 'Stores - E'
    })),
    docstatus: 1 // Automatically submit/formalize
  };

  const response = await fetch(`${frappeUrl}/api/resource/Sales Order`, {
    method: 'POST',
    headers: {
      'Authorization': `token ${apiKey}:${apiSecret}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Sales Order Error: ${response.statusText}`);
  }

  const result = await response.json();
  return result.data;
}
```

---

## 6. Colombian DIAN Electronic Invoicing (UBL 2.1)

To emit a legally compliant electronic invoice in Colombia:

```typescript
export async function createDianSalesInvoice(
  frappeUrl: string,
  apiKey: string,
  apiSecret: string,
  invoiceData: {
    customer: string;
    customer_tax_id: string; // NIT or National ID
    customer_tax_dv?: string; // Verification digit
    items: Array<{ item_code: string; qty: number; rate: number; tax_code?: string }>;
    payment_method: string; // e.g. 'Wompi', 'PSE', 'Credit Card'
  }
) {
  const payload = {
    customer: invoiceData.customer,
    posting_date: new Date().toISOString().split('T')[0],
    is_electronic_invoice: 1,
    tax_id: invoiceData.customer_tax_id,
    tax_dv: invoiceData.customer_tax_dv || '',
    items: invoiceData.items.map(item => ({
      item_code: item.item_code,
      qty: item.qty,
      rate: item.rate
    })),
    docstatus: 1 // Submit to trigger DIAN XML generation and CUFE signing
  };

  const response = await fetch(`${frappeUrl}/api/resource/Sales Invoice`, {
    method: 'POST',
    headers: {
      'Authorization': `token ${apiKey}:${apiSecret}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  const result = await response.json();
  return result.data; // Contains cufe, qr_code, and electronic_invoice_status
}
```

---

## 7. Frappe Cloud Outgoing Webhook Configuration

1. **DocType:** `Stock Ledger Entry` or `Sales Invoice`.
2. **Doc Event:** `on_submit`.
3. **Request URL:** `https://cms.yourdomain.com/frappe/webhook`.
4. **Enable Security:** Enabled (Set secure 32+ char secret).
5. **JSON Template:**
```json
{
  "event": "stock_update",
  "item_code": "{{ doc.item_code }}",
  "actual_qty": {{ doc.actual_qty }},
  "qty_after_transaction": {{ doc.qty_after_transaction }},
  "warehouse": "{{ doc.warehouse }}",
  "voucher_no": "{{ doc.voucher_no }}"
}
```

---

## 8. 5 Production Patterns in Zerops

### Pattern 1: Asynchronous Sales Order Sync via Directus Hook & BullMQ
Directus lifecycle hook pushes order payloads to `sync-to-frappe` queue in Valkey, ensuring checkout response time remains under 200ms.

### Pattern 2: HMAC-SHA256 Verified Stock Update Webhook in Directus
Custom Directus endpoint `/frappe/webhook` verifies cryptographic signatures using `crypto.timingSafeEqual`, updating product stock quantities safely.

### Pattern 3: Automated DIAN Electronic Invoicing Workflow on Order Payment
Upon payment webhook confirmation from Wompi/Stripe, worker submits a `Sales Invoice` with `docstatus: 1`, receiving the CUFE code and invoice PDF.

### Pattern 4: Financial Profit & Loss Statement RPC Query for Business Insights
Scheduled task queries ERPNext P&L method (`erpnext.accounts.report.profit_and_loss_statement`), populating `business_kpis_snapshot` in Directus.

### Pattern 5: Multi-Payment Reconciliation (`Payment Entry`)
Matches incoming payment gateway transaction IDs with outstanding `Sales Invoice` records, marking invoices as `Paid` in ERPNext accounting ledgers.

---

## 9. Anti-Patterns & Common Gotchas

1. **Synchronous REST Calls in Directus Hooks**: Never call Frappe Cloud synchronously within Directus hooks; slow network responses will hang Directus transactions. Always push to BullMQ.
2. **Updating Submitted Documents (`docstatus: 1`)**: ERPNext prevents mutating formalized accounting records. To adjust a submitted invoice, you must cancel (`docstatus: 2`) and re-issue an amended document.
3. **Infinite Loop Echoes**: Always include `_sync_source: 'frappe'` and verify Valkey locks before persisting synced records in Directus.

---

## 10. System of Record (SoR) Authority Matrix

| Entity Domain | System of Record (SoR) | Primary Storage | Sync Mechanism | Consumer Runtimes |
|---|---|---|---|---|
| **Accounting & General Ledger** | **ERPNext (Frappe Cloud)** | MariaDB / Ledger | BullMQ Async | `directus`, `business-insights`, `hermes-agent` |
| **Legal Stock & Kardex** | **ERPNext (Frappe Cloud)** | `tabBin`, `tabStock Ledger Entry` | Outgoing Webhooks | `directus`, `orders-fulfillment` |
| **Catalog Metadata (PIM)** | **Directus 12** | PostgreSQL 18 + S3 MinIO | Read-Only REST | `astro` (Frontend) |
| **Web Customer Sessions** | **Directus 12** | PostgreSQL 18 (Cookies) | Directus SDK | `astro` (Middleware SSR) |
| **Atomic Inventory Lock (<0.3ms)** | **NATS Broker** | Memory Cache / JetStream | Request-Reply RPC | `astro` (Checkout Action) |

---

## 11. Universal RUT-First Onboarding Protocol

1. **Extract Metadata from DIAN RUT**:
   ```bash
   python3 scripts/erpnext-rut-parser.py /path/to/rut.pdf --out assets/extracted_rut.json
   ```
2. **Execute Idempotent Setup**:
   ```bash
   python3 scripts/erpnext-onboard.py --rut /path/to/rut.pdf
   ```
3. **Audit Results**:
   - Company `tax_id` set to official NIT with DV.
   - Company address registered in official municipality.
   - Sales tax template set to 0% if Code 49 (Non-VAT responsible).
   - Compliance notice emitted if business activity requires adding CIIU `4791`.

---

## 12. Headless Desk Mode & Onboarding Suppression Architecture

Frappe Framework ships with 9 interactive module onboarding tours (`Organization`, `Selling`, `Buying`, `Stock`, `Accounts`, `Manufacturing`, `Projects`, `Assets`, `Subcontracting`). When `enable_onboarding` is set to `1` in `System Settings`, Desk mounts the Vue component `UserOnboarding` (`user_onboarding.bundle.js`), prompting users to manually create dummy entities.

### A. Global Headless Suppression Invariant
In production headless commerce architectures, ERPNext operates purely as the fiscal System of Record. Interactive walkthroughs must be globally deactivated to prevent UI friction and database contamination with dummy orders:

```python
# Programmatic Headless Activation (via REST API)
client.update_doc("System Settings", "System Settings", {"enable_onboarding": 0})
```

### B. Programmatic Step Completion (CVE-Patched Protocol)
Due to security patch CVE-2026-44976, direct `PUT` modifications to `Onboarding Step` DocTypes are restricted (`403 Forbidden`). When individual onboarding checklist steps must be marked complete programmatically, invoke the whitelisted Frappe desktop RPC endpoint:

```http
POST /api/method/frappe.desk.desktop.update_onboarding_step
Content-Type: application/json
Authorization: token API_KEY:API_SECRET

{
  "name": "Step Name",
  "field": "is_complete",
  "value": 1
}
```

---

## 13. Agnostic Amazon SES v2 Outbound Dispatch & Disjoint Namespaces

To maintain strict architectural separation of concerns (SoR), transactional email dispatch is partitioned into disjoint namespaces:

- **Customer / Marketing Namespace (`bknd` & Directus)**: Utilizes ZeptoMail, Brevo, or Resend via `$SMTP_HOST`, `$SMTP_USER`, `$SMTP_PASSWORD` for customer notifications, receipts, and marketing.
- **Enterprise / Fiscal Namespace (`erpnext`)**: Exclusively binds to **Amazon SES v2** (`$AWS_ACCESS_KEY_ID`, `$AWS_SECRET_ACCESS_KEY`, `$AWS_REGION`, `$AWS_SES_DEFAULT_FROM`) for administrative alerts, password resets, and official DIAN tax invoice PDF transmissions.

### A. Pre-Calculated vs Algorithmic SES SMTP Credentials
Amazon SES SMTP uses the IAM Access Key ID as the SMTP Username. The SMTP Password is an HMAC-SHA256 signature calculated over the string `SendRawEmail` with version byte `0x04`:
1. **Pre-Calculated Console Credential**: When created via the AWS SES Console ("Create SMTP Credentials"), the password already starts with the prefix `B...` (base64-encoded SigV4 signature). It MUST be used directly without re-hashing.
2. **Algorithmic Derivation**: If only a raw IAM Secret Access Key is provided, the SMTP password must be derived using SigV4 HMAC-SHA256.

### B. Canonical Frappe `Email Account` Configuration (Amazon SES)
```json
{
  "email_id": "{{DEFAULT_FROM_EMAIL}}",
  "email_account_name": "Amazon SES Outbound",
  "enable_incoming": 0,
  "enable_outgoing": 1,
  "default_outgoing": 1,
  "smtp_server": "email-smtp.{{AWS_REGION}}.amazonaws.com",
  "smtp_port": "587",
  "use_tls": 1,
  "use_ssl_for_outgoing": 0,
  "login_id_is_different": 1,
  "login_id": "{{AWS_ACCESS_KEY_ID}}",
  "password": "{{AWS_SECRET_ACCESS_KEY}}"
}
```

---

## 14. Batch Ingestion & High-Velocity Mutations (`insert_many` & `bulk_update`)

Ingesting hundreds of catalog items, inventory adjustments, or imported order records via sequential `POST /api/resource/:doctype` introduces substantial HTTP latency and network overhead (N+1 anti-pattern). Frappe Framework provides high-performance RPC methods in `frappe.client` to execute batch operations in single atomic HTTP requests.

### A. Batch Creation (`frappe.client.insert_many`)
Creates up to 200 documents in a single HTTP request within an atomic database transaction.

- **Endpoint:** `POST /api/method/frappe.client.insert_many`
- **Headers:** `Authorization: token API_KEY:API_SECRET`, `Content-Type: application/json`
- **Payload Schema:**
  ```json
  {
    "docs": [
      {
        "doctype": "Item",
        "item_code": "PROD-A01",
        "item_name": "Solar Inverter 5kW",
        "item_group": "Products",
        "stock_uom": "Nos",
        "is_stock_item": 1,
        "standard_rate": 1250.00
      },
      {
        "doctype": "Item",
        "item_code": "PROD-A02",
        "item_name": "Lithium Battery 48V",
        "item_group": "Products",
        "stock_uom": "Nos",
        "is_stock_item": 1,
        "standard_rate": 2100.00
      }
    ]
  }
  ```
- **Response:** Array containing the names/IDs of the inserted documents:
  ```json
  {
    "message": ["PROD-A01", "PROD-A02"]
  }
  ```

### B. Bulk Updates (`frappe.client.bulk_update`)
Updates multiple documents across various DocTypes in one call:
```json
{
  "docs": [
    {"doctype": "Sales Order", "name": "SO-2026-00101", "status": "Completed"},
    {"doctype": "Sales Order", "name": "SO-2026-00102", "status": "Cancelled"}
  ]
}
```

---

## 15. Child Table Synchronization & Atomic Row Surgery

Child tables in Frappe (e.g., `items` in `Sales Order`, `taxes` in `Sales Invoice`) are stored as separate database tables linked by `parent`, `parenttype`, and `parentfield`. Handling child tables over REST requires strict adherence to Frappe's synchronization mechanics.

### A. Destructive Child Table Invariant in Standard `PUT`
When updating a parent document via `PUT /api/resource/:doctype/:name`:
- **Destructive Purge Behavior:** The array passed in the child table property is treated as the **complete desired state**. Any existing child row whose `name` is omitted from the array will be **permanently deleted**.
- **In-Place Modification:** To modify an existing row, provide its existing child `name` identifier:
  ```json
  {
    "items": [
      {
        "name": "d2a4b8e1f0",
        "item_code": "PROD-001",
        "qty": 5,
        "rate": 150000
      },
      {
        "item_code": "PROD-002",
        "qty": 1,
        "rate": 80000
      }
    ]
  }
  ```
  *(Row `d2a4b8e1f0` is updated in-place; the second entry without `name` is inserted as a new row; any other existing rows are purged).*

### B. Atomic Row Surgery (`frappe.client.set_value`)
When you need to update a single cell in a child table (e.g., updating a serial number or line discount) without sending the full document payload and risking race conditions:

```http
POST /api/method/frappe.client.set_value
Authorization: token API_KEY:API_SECRET
Content-Type: application/json

{
  "doctype": "Sales Order Item",
  "name": "d2a4b8e1f0",
  "fieldname": "discount_percentage",
  "value": 10.0
}
```

### C. Direct Child Row Insertion
You can directly insert rows into child tables via the Resource API. Frappe automatically detects the `parent` relationship, saves the child, and re-triggers total recalculation on the parent document:

```http
POST /api/resource/Sales%20Order%20Item
Authorization: token API_KEY:API_SECRET
Content-Type: application/json

{
  "parent": "SO-2026-00042",
  "parenttype": "Sales Order",
  "parentfield": "items",
  "item_code": "CONS-001",
  "qty": 2,
  "rate": 350000
}
```

---

## 16. Document Lifecycle, Submissions & Amendment Protocol

In ERPNext, fiscal documents (`Sales Invoice`, `Purchase Invoice`, `Payment Entry`, `Journal Entry`, `Stock Entry`) are governed by formal document statuses (`docstatus`):
- `0`: **Draft** (Editable, no accounting impact).
- `1`: **Submitted** (Locked, generates General Ledger entries and Stock Ledger entries).
- `2`: **Cancelled** (Voided, creates reverse GL entries where applicable).

### A. Submitting Documents (`frappe.client.submit`)
Directly updating `docstatus: 1` via `PUT /api/resource/...` is blocked by Frappe's security validators. Submissions must invoke the official RPC method:

```http
POST /api/method/frappe.client.submit
Authorization: token API_KEY:API_SECRET
Content-Type: application/json

{
  "doc": {
    "doctype": "Sales Invoice",
    "name": "ACC-SINV-2026-00012"
  }
}
```

### B. Cancelling Documents (`frappe.client.cancel`)
To cancel a submitted document and reverse financial movements:

```http
POST /api/method/frappe.client.cancel
Authorization: token API_KEY:API_SECRET
Content-Type: application/json

{
  "doctype": "Sales Invoice",
  "name": "ACC-SINV-2026-00012"
}
```

### C. Amendment Pattern (`amended_from`)
Cancelled documents cannot be un-cancelled or directly edited. To rectify a cancelled invoice or order:
1. Fetch the cancelled document: `GET /api/resource/Sales Invoice/ACC-SINV-2026-00012`
2. Remove immutable fields (`name`, `creation`, `modified`, `modified_by`, `owner`, `docstatus`).
3. Set `"amended_from": "ACC-SINV-2026-00012"`.
4. Apply corrections and insert as new document: `POST /api/resource/Sales Invoice`.
5. Frappe names the new record `ACC-SINV-2026-00012-1` and links the audit trail.

---

## 17. Private File Uploads & Chunked Attachments

Attaching tax certificates (RUT PDF), fiscal electronic invoices (DIAN XML), and customer proof of payments requires secure file handling.

### A. Multipart Upload (`/api/method/upload_file`)
- **Endpoint:** `POST /api/method/upload_file`
- **Encoding:** `multipart/form-data`
- **Fields:**
  - `file`: The binary file content.
  - `filename`: Target filename (e.g., `RUT_900123456_2026.pdf`).
  - `is_private`: `1` (stores in `/private/files/`, requires authentication) or `0` (public `/files/`).
  - `doctype`: (Optional) Parent DocType to attach to (e.g., `Customer`, `Sales Invoice`).
  - `docname`: (Optional) Target document ID (e.g., `CUST-2026-001`).
  - `fieldname`: (Optional) Document field to automatically receive the uploaded file URL (e.g., `tax_id_attachment`).
  - `folder`: Destination folder inside File Manager (defaults to `Home`).

### B. Example cURL Upload with DocType Field Binding
```bash
curl -X POST "https://${FRAPPE_URL}/api/method/upload_file" \
  -H "Authorization: token ${FRAPPE_API_KEY}:${FRAPPE_API_SECRET}" \
  -F "file=@/local/path/to/invoice_cufe.xml" \
  -F "filename=DIAN_UBL21_INV1001.xml" \
  -F "is_private=1" \
  -F "doctype=Sales Invoice" \
  -F "docname=ACC-SINV-2026-00015" \
  -F "fieldname=custom_dian_xml"
```

### C. Protected File Download
Files marked `is_private=1` cannot be accessed via direct static URLs without credentials. They must be requested with authentication:
```http
GET /api/method/frappe.utils.file_manager.download_file?file_url=/private/files/DIAN_UBL21_INV1001.xml
Authorization: token API_KEY:API_SECRET
```

---

## 18. Jinja Template Engine for Fiscal Print Formats (DIAN Colombia)

Frappe executes Jinja inside a secure server-side sandbox for **Print Formats** (rendered to PDF via `wkhtmltopdf`), automated transactional emails, and dynamic webhook payloads.

### A. Available Methods in Jinja Sandbox
The following primitives are whitelisted inside Frappe Jinja templates:
- `frappe.format_value(value, df)`: Formats numeric, currency, or date values according to DocField configuration and system locale.
- `frappe.format_date(date, "dd/MM/yyyy")`: Standard date formatter.
- `frappe.db.get_value(doctype, name, fieldname)`: Fetches single attributes from related tables without building heavy SQL queries.
- `frappe.get_url()`: Resolves base URL for asset and image embedding.
- `_("Translate String")`: Multilingual translation helper.

### B. Standard Colombian DIAN Fiscal Print Format Snippet
```jinja
<div class="dian-invoice-container">
  <div class="header">
    <h2>{{ doc.company }}</h2>
    <p>NIT: {{ frappe.db.get_value("Company", doc.company, "tax_id") }}</p>
    <p>Resolución DIAN No. {{ doc.custom_dian_resolution }} del {{ frappe.format_date(doc.custom_dian_res_date, "dd/MM/yyyy") }}</p>
    <p>Rango autorizado: {{ doc.custom_dian_prefix }} {{ doc.custom_dian_from }} a {{ doc.custom_dian_to }}</p>
  </div>

  <div class="cufe-box">
    <strong>CUFE:</strong>
    <p class="cufe-string" style="word-break: break-all; font-family: monospace; font-size: 8pt;">
      {{ doc.custom_cufe or "DOCUMENTO EN TRÁMITE DIAN" }}
    </p>
  </div>

  <table class="table table-bordered items-table">
    <thead>
      <tr>
        <th>Ítem</th>
        <th>Descripción</th>
        <th class="text-right">Cant.</th>
        <th class="text-right">Precio Unit.</th>
        <th class="text-right">Total</th>
      </tr>
    </thead>
    <tbody>
      {% for item in doc.items %}
      <tr>
        <td>{{ item.item_code }}</td>
        <td>{{ item.item_name }}</td>
        <td class="text-right">{{ item.qty }}</td>
        <td class="text-right">{{ frappe.format_value(item.rate, {"fieldtype": "Currency", "currency": doc.currency}) }}</td>
        <td class="text-right">{{ frappe.format_value(item.amount, {"fieldtype": "Currency", "currency": doc.currency}) }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>

  {% if doc.custom_dian_qr %}
  <div class="qr-code-section text-center">
    <img src="{{ doc.custom_dian_qr }}" alt="Código QR DIAN" style="width: 120px; height: 120px;" />
  </div>
  {% endif %}
</div>
```



