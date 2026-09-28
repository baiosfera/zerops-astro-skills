# Autonomous Accounting Agents: Integration Architecture & Protocols (v2.1)

This reference documents the formal contracts and protocols for integrating autonomous accounting agents (**Paperclip.ing**, **CrewAI**, and **Hermes-Agent**) with ERPNext (Frappe Cloud) in the Zerops sovereign architecture.

---

## 1. Architectural Topology & Control Plane

```
+-------------------------------------------------------------+
|               Paperclip.ing (Control Plane)                 |
|  - Agent Org Chart (CEO, Auditor, Accountant, Operations)   |
|  - Strict Budget Caps & Spend Guardrails                    |
|  - Immutable Audit Log & Heartbeat Monitor                  |
+------------------------------+------------------------------+
                               |
            +------------------+------------------+
            |                                     |
            v                                     v
+-----------------------+             +-----------------------+
|  CrewAI Accountant    |             | Hermes-Agent Co-Pilot |
|  - Automated P&L      |             | - Telegram Alerting   |
|  - UVT Threshold Check|             | - On-Demand Inquiries |
|  - Wompi Reconciliation             | - Executive Reports   |
+-----------+-----------+             +-----------+-----------+
            |                                     |
            +------------------+------------------+
                               |
                               | (HTTPS REST API / Bearer Token)
                               v
+-------------------------------------------------------------+
|              ERPNext v15/v16 (Frappe Cloud)                 |
|              System of Record (SoR) Fiscal                  |
|  - General Ledger (`GL Entry`)                              |
|  - Sales Invoices (`Sales Invoice`) & Taxes                 |
|  - Payment Reconciliation (`Payment Entry`)                 |
|  - Official Stock Balances (`tabBin`, `Stock Ledger Entry`) |
+-------------------------------------------------------------+
```

---

## 2. Mandatory Security & Access Boundaries

1. **Dedicated Service User**: Autonomous agents MUST NOT authenticate using the root `Administrator` account. They must use a dedicated API role:
   - User: `agent-accountant@{{COMPANY_DOMAIN}}`
   - Roles: `Accounts User`, `Auditor` (strictly Read-Only on posted transactions; Draft creation only for reconciliations).
2. **Audit Trail Invariant**: Every document created or queried by an agent must carry the metadata tag `_agent_source: "paperclip"` or `_agent_source: "hermes"`.
3. **No Direct Mutation of Submitted Ledgers**: Posted GL Entries and Stock Ledger Entries are completely immutable. Adjustments require generating formal `Journal Entry` or `Credit Note` in Draft mode (`docstatus: 0`) for human review.

---

## 3. Core Autonomous Capabilities & Canonical Endpoints

### A. Annual 3,500 UVT Threshold Monitor
Colombian tax law (Art. 437 E.T.) requires non-VAT responsible entities (Code 49) to transition to the general regime if gross taxable revenue exceeds 3,500 UVT in a calendar year:
- **2025 Threshold**: COP 174,296,500 (~COP 14,520,000/month).
- **2026 Threshold**: COP 183,309,000 (~COP 15,275,000/month).

**Agent Monitoring Query**:
```http
GET /api/resource/Sales%20Invoice?fields=["grand_total","posting_date"]&filters=[["docstatus","=",1],["posting_date",">=","2026-01-01"],["company","=","{{COMPANY_NAME}}"]]&limit_page_length=1000
Authorization: token {api_key}:{api_secret}
```
*The agent computes the running sum of `grand_total` and alerts at 75%, 90%, and 95% of the threshold via Hermes-Agent / Telegram.*

### B. VAT Compliance Auditor (Code 49 Guardrail)
If the RUT specifies Responsibility `49`, no sales invoice should have `total_taxes_and_charges > 0`.

**Agent Verification Query**:
```http
GET /api/resource/Sales%20Invoice?fields=["name","total_taxes_and_charges","grand_total"]&filters=[["docstatus","=",1],["total_taxes_and_charges",">",0]]
Authorization: token {api_key}:{api_secret}
```
*If records return, the agent triggers an immediate high-priority audit incident.*

### C. Wompi Payment Reconciliation
Cross-checks gross settlements from Wompi webhook events against `Payment Entry` and `Sales Invoice` records to identify unpaid balances or gateway discrepancies.

**Agent Query**:
```http
GET /api/resource/Payment%20Entry?fields=["name","paid_amount","reference_no","status"]&filters=[["docstatus","=",1],["posting_date",">=","2026-01-01"]]
Authorization: token {api_key}:{api_secret}
```

---

## 4. Paperclip.ing Agent Manifest Template

To register the accountant agent inside a Paperclip cluster:

```json
{
  "name": "colombian-fiscal-auditor",
  "role": "Accountant & Tax Compliance Specialist",
  "goal": "Monitor ERPNext General Ledger, audit VAT compliance, and track UVT thresholds",
  "budget_monthly_usd": 15.00,
  "runtime": "hermes-agent",
  "tools": [
    "erpnext_get_general_ledger",
    "erpnext_audit_vat_invoices",
    "erpnext_calculate_uvt_headroom"
  ],
  "environment": {
    "FRAPPE_URL": "https://{{SITE_SUBDOMAIN}}.v.frappe.cloud",
    "COMPANY_NAME": "{{COMPANY_NAME}}",
    "TAX_REGIME": "NO_RESPONSABLE_IVA_49",
    "UVT_YEAR": 2026,
    "UVT_VALUE_COP": 52374
  }
}
```
