---
name: meta-plan
description: "Trigger: meta-plan, planner, plan, master-plan, planificar, crear plan, /plan, systemic-issue-triage, proportional activation, optional linear-cli. Strategic planning, proportional activation, and epistemic tracking orchestrator."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `meta-plan` — Strategic Planning & Proportional Activation (v2.0)

## Activation Contract
Activate when structuring multi-service initiatives ($\ge 2$ runtimes), high-risk architectural refactors, or systemic defect triage across Zerops. Bounded single-service tasks execute inline with `update_steps` and domain skills (`astro-web`, `postgresql`, `bun`, `codecraft`).

## Hard Rules & Positive Guidance
- **Proportional Activation**: Use native `update_steps` for multi-step execution tracking. Reserve `/var/www/artifacts/plans/<PROJECT_NAME>/<slug>.md` + explicit `Go` strictly for multi-service or high-risk architectural changes whose trade-offs require approval.
- **Optional Linear (`linear-cli`)**: Linear tracking is strictly **optional** in interactive `agy 1.5.16` sessions—activate it only when the user explicitly requests Linear or during unattended `hermes`/`paperclip` background runs.
- **Token-Frugal Grounding**: Verify live topology (`zerops_discover`) and primary docs before drafting plans; pass `Model: "flash"` when delegating broad local read-only exploration to `research` subagents.
- **Scoped Real Proof**: Separate `BEHAVIORALLY_VERIFIED` (tests/builds/probes exit 0) from `SYNTAX_ONLY` and `UNVERIFIED` on the exact modified scope. Run `skills-suite-validate` / `ssot-parity-check` only when skills, catalog, or governance files change. Archive executed plans to `archive/<slug>.executed.md` and persist learnings via `mem_save`.

## Active Sub-Skills Dispatch Table

| Focus | Sub-Skill | Canonical SSoT Pointer | Responsibility |
|---|---|---|---|
| **State Machine** | `cohalo` | [`cohalo`](file:///var/www/.agents/skills/cohalo/SKILL.md) | Context, Harness & Loops discipline |
| **Plan & Optional Linear** | `planner` | [`planner`](file:///var/www/.agents/skills/planner/SKILL.md) | Proportional planning, F4 Go gate, optional Linear |
| **Root Resolution** | `systemic-issue-triage` | [`systemic-issue-triage`](file:///var/www/.agents/skills/systemic-issue-triage/SKILL.md) | Audit systemic clusters and resolve at the root |

## Meta-Suites Dispatch Routing

| Scope | Dispatched Meta-Suite | Target Boundary |
|---|---|---|
| Constitutional Rules & System Directives | `meta-system` | `.agents/rules/`, `AGENTS.md`, system prompts |
| LLM Skills & Dual-RAG Architecture | `meta-skill` | `zerops-astro-skills/`, routers $\le$ 480 words |
| Platform Scripts, Hooks & Python/Bash | `meta-script` | `scripts/`, `tool-guard.py`, automation hooks |
| GitOps, Versioning & Deployment Pipelines | `meta-gitops` | CI/CD workflows, zerops.yaml, releases |
| Multi-Tier Epistemic Research & Benchmarks | `meta-research` | Compound research pipeline (Context7, Exa, Tavily, Jina) |
| Dedicated Application Software | Domain Skills | `astro-web`, `postgresql`, `bun`, `codecraft` |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/meta-plan/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/meta-plan/references/infra.md)
