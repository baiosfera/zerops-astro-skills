---
name: meta-plan
description: "Trigger: meta-plan, planner, plan, master-plan, planificar, crear plan, /plan, epic breakdown, linear-cli, systemic-issue-triage, proportional activation, epistemic tracking. Master Strategic Planning, Proportional Activation & Epistemic Tracking Orchestrator."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# `meta-plan` — Master Strategic Planning & Epistemic Tracking Orchestrator (v1.1)

## Activation Contract
Activate when structuring multi-step initiatives, architectural refactors, multi-service features, or triaging systemic defects across Zerops. Governs EPICS, MODULAR TASK DECOMPOSITION, LINEAR SYNCHRONIZATION, AND EPISTEMIC RECALL.

## Hard Rules & Positive Guidance
- **Epistemic Subagent Wait (F0 Mandate)**: Await all research subagent reports before jumping to conclusions, drafting master plans, or conducting grilling.
- **Proportional Activation Threshold**: Single-runtime tasks bypass meta-plan and execute directly with domain skills (`astro-web`, `postgresql`, `bun`, `codecraft`). Multi-service initiatives ($\ge 2$ runtimes), architectural changes, or complex tasks of $\ge 3$ steps activate `meta-plan`.
- **Draft Isolation & F4 Linear Gate**: During F0–F3, work resides in `draft_<slug>.md` and Engram (`mem_save`). Creating Linear projects or BAIs is strictly prohibited in F0–F3; Linear sync activates strictly in F4 upon explicit 'Go' to the Master Plan in `/var/www/artifacts/plans/<slug>_v1.md`.
- **Anti-Monolithic BAI Invariant**: Decompose architectures into granular BAI issues per runtime and boundary. Prohibited to collapse heterogeneous stacks into a single monolithic ticket.
- **Epistemic Persistence & Clean Lifecycle**: Persist discoveries in Engram (F0–F5) and Linear comments (F4–F5). On completion, attest with physical evidence (exit 0), archive to `archive/<slug>.executed.md`, and purge operational `.json` states leaving `/artifacts/` clean.

## Active Sub-Skills Dispatch Table

| Focus | Sub-Skill | Canonical SSoT Pointer | Responsibility |
|---|---|---|---|
| **State Machine** | `cohalo` | [`cohalo`](file:///var/www/.agents/skills/cohalo/SKILL.md) | Fractal CoHaLo execution flow (F0 to F5) |
| **Linear Engine** | `planner` | [`planner`](file:///var/www/.agents/skills/planner/SKILL.md) | Linear issue management, acceptance criteria, scope control |
| **Plan Design** | `writing-plans` | [`writing-plans`](file:///var/www/.agents/skills/writing-plans/SKILL.md) | Granular step-by-step task breakdown |
| **Execution** | `executing-plans` | [`executing-plans`](file:///var/www/.agents/skills/executing-plans/SKILL.md) | Subordinate step execution without scope creep |
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

## References
- [`references/usage.md`](file:///var/www/.agents/skills/meta-plan/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/meta-plan/references/infra.md)
