---
name: meta-plan
description: "Trigger: meta-plan, planner, plan, master-plan, planificar, crear plan, /plan, epic breakdown, linear-cli, systemic-issue-triage, proportional activation, epistemic tracking. Master Strategic Planning, Proportional Activation & Epistemic Tracking Orchestrator."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `meta-plan` — Master Strategic Planning & Epistemic Tracking Orchestrator (v1.0)

## Activation Contract
Activate when structuring multi-step initiatives, architectural refactors, multi-service features, or triaging systemic defects across the Zerops ecosystem. Governs EPICS, TASK DECOMPOSITION, LINEAR SYNCHRONIZATION, AND EPISTEMIC RECALL.

## Hard Rules & Positive Guidance
- **Proportional Activation Threshold**: Apply the strict dual-gate rule:
  1. *Direct Domain Execution (Zero-Friction)*: Single-runtime tasks or standalone CLI tools (`.bin`) bypass `meta-plan` and execute directly with domain skills (`astro-web`, `postgresql`, `bun`, `codecraft`).
  2. *Meta-Plan Activation (Mandatory)*: Multi-service initiatives ($\ge 2$ runtimes), foundational architectural changes, or complex tasks of $\ge 3$ steps require `meta-plan` and Linear issue tracking.
- **Epistemic Persistence Before Delivery**: Persist technical discoveries and decisions in Linear (`linear-cli comment`) and Engram (`mem_save`) before formulating chat replies. Never lose architecture findings in chat context.
- **Physical Attestation on Transition**: Update Linear issue status with verified exit-0 physical evidence (`linear-cli update-status <id> Done --evidence "<proof>"`).
- **Subordinate Execution Without Drifts**: Execute plans sequentially through `writing-plans` and `executing-plans`. Validate each step with physical tests before proceeding.

## Active Sub-Skills Dispatch Table

| Focus | Sub-Skill | Canonical SSoT Pointer | Responsibility |
|---|---|---|---|
| **State Machine** | `cohalo` | [`cohalo`](file:///var/www/.agents/skills/cohalo/SKILL.md) | Fractal CoHaLo execution flow (F0 to F5) |
| **Linear Engine** | `planner` | [`planner`](file:///var/www/.agents/skills/planner/SKILL.md) | Linear issue management, acceptance criteria, scope control |
| **Plan Design** | `writing-plans` | [`writing-plans`](file:///var/www/.agents/skills/writing-plans/SKILL.md) | Granular step-by-step task breakdown |
| **Implementation** | `executing-plans` | [`executing-plans`](file:///var/www/.agents/skills/executing-plans/SKILL.md) | Subordinate step execution without scope creep |
| **Root Resolution** | `systemic-issue-triage` | [`systemic-issue-triage`](file:///var/www/.agents/skills/systemic-issue-triage/SKILL.md) | Audit systemic clusters and resolve at the root |

## Meta-Suites Dispatch Routing

| Scope | Dispatched Meta-Suite | Target Boundary |
|---|---|---|
| Constitutional Rules & System Directives | `meta-system` | `.agents/rules/`, `AGENTS.md`, system prompts |
| LLM Skills & Dual-RAG Architecture | `meta-skill` | `zerops-astro-skills/`, routers $\le$ 480 words |
| Platform Scripts, Hooks & Python/Bash | `meta-script` | `scripts/`, `tool-guard.py`, automation hooks |
| GitOps, Versioning & Deployment Pipelines | `meta-gitops` | CI/CD workflows, zerops.yaml, releases |
| Multi-Tier Epistemic Research & Benchmarks | `meta-research` | Compound research pipeline (Exa, Context7, Jina) |
| Dedicated Application Software | Domain Skills | `astro-web`, `postgresql`, `bun`, `codecraft` |

## Commands
```bash
# View active issue details
LINEAR_SERVICE="zerops-astro-skills" linear-cli issue <ID>

# Add progress comment or architectural decision
LINEAR_SERVICE="zerops-astro-skills" linear-cli comment <ID> "<note>"

# Close issue with mandatory physical evidence
LINEAR_SERVICE="zerops-astro-skills" linear-cli update-status <ID> Done --evidence "<proof>"
```

## References
- [`references/usage.md`](file:///var/www/.agents/skills/meta-plan/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/meta-plan/references/infra.md)
