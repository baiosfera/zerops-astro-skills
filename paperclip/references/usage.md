# Paperclip Autonomous Agent Operating System — Usage & Orchestration Manual

This manual provides the comprehensive architectural and operational specification for operating Paperclip (`paperclip.ing` / `@paperclipai`) as an autonomous enterprise control plane on Zerops.

---

## 1. The Tri-Pillar Paradigm: Control Plane vs. Execution Plane

Paperclip operates strictly as the **Control Plane / Operating System** of the AI workforce:
- **Control Plane (Paperclip)**: Decides *what* work needs to be done, *who* is assigned, *how much budget* is authorized, *what tools* require human sign-off, and *what status* a task occupies in the corporate hierarchy.
- **Execution Plane (Hermes / CrewAI / Pi / Goose / Aider)**: Decides *how* reasoning, code generation, tool calls, and LLM inference loops are executed.

```
┌─────────────────────────────────────────────────────────────────┐
│                    HUMAN BOARD OF DIRECTORS                     │
│                (Invites, Approvals, Spend Caps)                 │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                 PAPERCLIP AGENT OPERATING SYSTEM                │
│   • Goal Tree (Initiative ➔ Project ➔ Milestone ➔ Issue)        │
│   • Org Chart (CEO ➔ Leads ➔ Workers) via `reports_to`          │
│   • Single-Assignee Kanban Board with Atomic Checkout Locks     │
│   • Governed MCP Gateway & Tool Policies (Allow/Deny/HITL)      │
│   • Monthly Budget Policies ($ Cents) & Reservation Circuit Breaker │
└───────────────┬─────────────────┬──────────────────┬────────────┘
                │                 │                  │
                ▼                 ▼                  ▼
┌───────────────────────┐ ┌───────────────┐ ┌─────────────────────┐
│  HERMES CHIEF OF STAFF│ │ PI BUILDER    │ │ CREWAI SWARM RUNNER │
│  (hermes_gateway v1)  │ │ (pi_local)    │ │ (hermes_gateway/SSE)│
└───────────────────────┘ └───────────────┘ └─────────────────────┘
```

---

## 2. Org Chart Architecture & Agent Hierarchy

The corporate structure in Paperclip is maintained in the `agents` table via a recursive foreign key `reports_to`:

### Role Hierarchy
1. **CEO / Chief of Staff (`role: 'ceo'`)**:
   - Holds structural authority over the company.
   - Assigned the highest spend cap (e.g., $1,000 / month = `100000` cents).
   - In Zerops, **Hermes** occupies this position, communicating over `hermes_gateway`.
2. **Technical Leads & Architects (`role: 'lead'`)**:
   - Report directly to the CEO (`reports_to: <ceo_id>`).
   - Own technical domains and projects.
   - Example: **Pi Code Builder** (`pi_local`), specialized in Astro 5 SSR and rapid code mutations.
3. **Worker Specialists & Swarms (`role: 'worker'`)**:
   - Report to Leads or the CEO.
   - Execute tactical units of work.
   - Example: **CrewAI Swarms** (`hermes_gateway` with `X-Crew-Name: <swarm>`), running research swarms at $0 token cost over Bifrost Gateway.

### Agent Permissions Schema
Stored in `agents.permissions` JSONB:
```json
{
  "canCreateAgents": true,
  "canCreateSkills": true,
  "canHire": true
}
```

---

## 3. Goal Tree to Kanban Workflow

Paperclip enforces an uncompromised structural hierarchy for work decomposition:

### The Hierarchy
1. **Initiatives / Company Goals (`goals`)**: High-level strategic targets set by the board (e.g., "Deploy Autonomous Agent Mesh v1").
2. **Projects (`projects`)**: Concrete delivery vehicles with assigned lead agents (e.g., "Plataforma Baiosfera").
3. **Issues / Tasks (`issues`)**: Atomic units of work with exact acceptance criteria, single assignee (`assignee_agent_id`), and Kanban lifecycle states:
   - `backlog`: Defined but uncommitted.
   - `todo`: Actionable, ready for agent checkout.
   - `in_progress`: Actively checked out with an atomic execution lock (`checkout_run_id`).
   - `in_review`: Completed by agent, awaiting human approval or verification.
   - `done`: Verified and accepted.
   - `cancelled`: Deprecated or superseded.

### The Single Assignee & Atomic Checkout Invariant
To prevent racing conditions, an issue can only have **one** assignee at any moment. When an agent picks up an issue:
1. Paperclip issues an atomic checkout lock (`issues.checkout_run_id`).
2. Concurrent checkout attempts by other agents are rejected with HTTP 409 Conflict.
3. Upon completion, the agent submits a completion receipt, releasing the checkout lock.

---

## 4. Governance, Spend Caps & Human In The Loop (HITL)

### Spend Caps & Budget Policies
Budgets are tracked in integer cents (`budget_monthly_cents`).
- **Concurrent Reservations (`reservation_cents`)**: When a run starts, Paperclip reserves a budget slice.
- **Hard Stop Circuit Breaker**: If `spent_monthly_cents + reservation_cents >= budget_monthly_cents`, Paperclip pauses agent heartbeats immediately.
- **Reset Cycles**: Budgets evaluate over `spend_month_utc` (YYYY-MM) and automatically refresh on the 1st of each calendar month.

### Human In The Loop (HITL) Approvals
Stored in `approvals` and `tool_action_requests`:
- Sensitive operations (e.g., invoking production deployment, high-spend inference, remote git mutations) require explicit human sign-off.
- The agent transitions the task to blocked/pending-approval and emits an approval card to the dashboard (and optionally external channels like Telegram or Slack).
- Execution resumes only after a human clicks "Approve" in the Paperclip UI or sends the authorized callback.

---

## 5. Dual MCP Plane Architecture

Paperclip provides a bidirectional Model Context Protocol (MCP) interface:

### 1. Paperclip as MCP Server (`@paperclipai/mcp-server`)
Enables external agents (Goose, Aider, OpenCode, Pi) to interact with Paperclip via standard MCP tools:
- `paperclipCheckoutIssue({ issueId })`: Locks and assigns an issue to the calling agent.
- `paperclipAddComment({ issueId, body })`: Posts a progress update or telemetry.
- `paperclipCompleteTask({ issueId, summary, artifacts })`: Submits completion proof and moves issue to review.
- `paperclipListIssues({ projectId, status })`: Discovers available work units.

### 2. Paperclip as Governed MCP Gateway (`tool_mcp_gateways`)
Proxies external MCP servers (GitHub, PostgreSQL, Linear, Directus) to protect the infrastructure:
- **Allow Policy**: Safe read-only operations pass transparently.
- **Require Approval Policy**: Mutating or destructive operations trigger an HITL approval request.
- **Deny Policy**: Unauthorized tools are blocked at the proxy boundary.

---

## 6. CLI Reference & Operational Commands

Paperclip provides an authenticated wrapper at `/usr/local/bin/paperclipai` (and `/var/www/.bin/paperclipai`):

```bash
# Print a one-time bootstrap invite URL for the first CEO admin
paperclipai auth bootstrap-ceo

# Run database migrations manually
paperclipai db migrate

# Inspect instance configuration
cat /mnt/localstorage/paperclip/instances/default/config.json

# Check server health and database status
curl -s http://paperclip:3100/api/health
```
