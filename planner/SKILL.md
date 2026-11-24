---
name: planner
description: "Trigger: planner, plan, master-plan, planificar, crear plan, /plan, change proposal, roadmap, optional linear. Proportional planning router subordinate to meta-plan and Supreme Directive v10.0."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "12.0"
---

# Planner — Proportional Planning & Honest Closure (v12.0)

## Activation Contract
Subordinate to [`meta-plan`](file:///var/www/.agents/skills/meta-plan/SKILL.md) and [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Bounded tasks run inline with `update_steps`. Multi-service ($\ge 2$ runtimes) or high-risk architectural changes use `/var/www/artifacts/plans/` and require explicit `Go`. Linear (`linear-cli`) is **optional** (only when explicitly requested by the user or run autonomously by `hermes`/`paperclip`).

## Sovereign Invariants
1. **Facts-First & Anti-Grilling**: Inspect local files and live primary sources before asking. Limit clarifications to 1 concrete decision with trade-offs.
2. **Proportional Plan & Go Gate**: Publish multi-service/high-risk plans in `/var/www/artifacts/plans/<PROJECT_NAME>/<slug>.md` (YAML `project: <PROJECT_NAME>`) with executable verification criteria and wait for explicit `Go`.
3. **Optional Linear Scoping**: When Linear is requested, group `BAI-*` issues under a project (`linear-cli create ... --project <ID|name>`) and close with `--evidence`. Do not create Linear tickets unasked in interactive `agy` sessions.
4. **Scoped Reality Proof**: Verify the exact modified scope (`zcp run {hostname} ...`, `py_compile`, `bash -n`, HTTP probe; `skills-suite-validate` / `ssot-parity-check` only when skills/governance changed). Report `BEHAVIORALLY_VERIFIED`, `SYNTAX_ONLY`, and `UNVERIFIED` separately, archive executed plans to `archive/<slug>.executed.md`, and save durable decisions via `mem_save`.
5. **Modular `baiosfera/*` Topology**: [`zerops-astrobranding`](file:///var/www/zerops-astrobranding/iniciar.sh) owns recipes, blueprints, templates, and shared scripts; runtime code lives in `baiosfera/runtime-*` + `template-astro-web`.

## Decision Gates

| Layer | Protocol / Action | Reference |
|---|---|---|
| Parent Orchestrator | Proportional threshold & meta-suite routing | [`meta-plan`](file:///var/www/.agents/skills/meta-plan/SKILL.md) |
| External Grounding | Inline MCP (`context7`, `exa`, `tavily`, `jina`); `flash` subagent for broad local scans | [`research`](file:///var/www/.agents/skills/research/SKILL.md) |
| Optional Linear CLI | `create-project`, `create`, `comment`, `update-status` (on request only) | [`linear-cli`](file:///var/www/.bin/linear-cli) |
| Operational Details | Git-first tracks and scoped verification | [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) |
