---
name: paperclip
description: "Trigger: paperclip, paperclipai, paperclip.ing, agent os, control plane, hermes_gateway, chief of staff, hitl, budget_policies, spend caps, mcp-server. Autonomous Agent Operating System & Multi-Agent Control Plane for Zerops."
version: "1.0"
---

# Paperclip Autonomous Agent Operating System & Control Plane (v1.0)

Autonomous Agent Operating System and corporate control plane (`paperclip.ing` / `@paperclipai`) orchestrating multi-agent meshes across Zerops environments. Manages organizational hierarchy, recursive agent reporting (`reports_to`), goal trees (`goals` $\to$ `projects` $\to$ `issues`), single-assignee Kanban boards, human-in-the-loop approvals (HITL), spend caps with concurrent budget reservations, governed MCP gateways, and multi-agent runtime adapters.

## Core Capabilities & Reference Map

| Domain | Scope & Capabilities | Authoritative Guide |
|---|---|---|
| **Agent OS & Org Chart** | Recursive `reports_to` agent tree, role hierarchy (CEO / Lead / Worker), permissions, heartbeat loops | [`references/usage.md#1`](file:///var/www/.agents/skills/paperclip/references/usage.md) |
| **Multi-Agent Connectivity** | Native adapters for Hermes (`hermes_gateway`), Pi Coding Agent (`pi_local`), CrewAI swarms, Goose/Aider (`process` + `@paperclipai/mcp-server`) | [`references/multi_agent_mesh.md`](file:///var/www/.agents/skills/paperclip/references/multi_agent_mesh.md) |
| **Goal Tree & Kanban** | `goals` (Initiatives) $\to$ `projects` $\to$ `issues` hierarchy, atomic checkout locks, status cards, completion contracts | [`references/usage.md#2`](file:///var/www/.agents/skills/paperclip/references/usage.md) |
| **Governance & Spend Caps** | Monthly budget ceilings (`budget_monthly_cents`), `reservation_cents`, automated circuit breakers, HITL action approvals | [`references/usage.md#3`](file:///var/www/.agents/skills/paperclip/references/usage.md) |
| **Dual MCP Plane** | Paperclip as MCP Server for task management and Paperclip as Governed MCP Gateway with security policies | [`references/usage.md#4`](file:///var/www/.agents/skills/paperclip/references/usage.md) |
| **Zerops Infrastructure** | Node.js 26 LXC runtime, PostgreSQL 18 schema, LocalStorage NVMe persistence (`PAPERCLIP_HOME`), automated seeding | [`references/infra.md`](file:///var/www/.agents/skills/paperclip/references/infra.md) |

## Operational State Machine (CoHaLo Protocol)

```
[Inflow: Strategic Initiative / Linear Goal] ──> [Gate 0: Budget & Permission Check]
                                                        │
                                                        ▼
[Gate 1: Agent Assignment & Checkout Lock] ───> [Gate 2: Adapter Execution (Hermes / Pi / CrewAI)]
                                                        │
                                                        ▼
[Gate 3: HITL Approval / MCP Policy Audit] ───> [Outflow: Verified Kanban Delivery / Metrics SSoT]
```

## Quick Reference Commands

- **Generate First-Admin Bootstrap Invite**:
  ```bash
  paperclipai auth bootstrap-ceo
  ```
- **Inspect Service Health & DB Connectivity**:
  ```bash
  curl -s http://paperclip:3100/api/health
  ```
- **Query Active Agents & Org Chart**:
  ```bash
  PAPERCLIP_DB=$(jq -r '.database.connectionString' /mnt/localstorage/paperclip/instances/default/config.json 2>/dev/null || echo "$DATABASE_URL")
  psql "$PAPERCLIP_DB" -c "SELECT id, name, role, title, adapter_type, reports_to, status FROM agents;"
  ```
- **Validate Skill Suite & Governance**:
  ```bash
  skills-suite-validate
  ```

## Authoritative Documentation

- Comprehensive Usage Manual: [`references/usage.md`](file:///var/www/.agents/skills/paperclip/references/usage.md)
- Multi-Agent Integration Guide: [`references/multi_agent_mesh.md`](file:///var/www/.agents/skills/paperclip/references/multi_agent_mesh.md)
- Zerops Infrastructure & Schema: [`references/infra.md`](file:///var/www/.agents/skills/paperclip/references/infra.md)
