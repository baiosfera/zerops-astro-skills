---
name: planner
description: "Trigger: planner, plan, master-plan, planificar, crear plan, diseña un plan, /plan, change proposal, version plan, roadmap. Universal Master Planning & SSoT Governance Orchestrator under CoHaLo v8.4 and Supreme Directive v8.3."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "9.3"
---

# Planner — Universal Master Planning & SSoT Governance Orchestrator (v9.3)

## Activation Contract
Activate for multi-step refactors and governance under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Bounded tasks execute inline without ceremonial plans. Eradicates checklist theater.

## Hard Rules (Positive Guidance)
- **Rule 1 (CoHaLo Positive Guidance & Continuous Present Inflow)**: Anchors decisions to live runtime state (`date -u`). Grounding follows [`research`](file:///var/www/.agents/skills/research/SKILL.md) inline or via subagent. Details in [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md).
- **Rule 2 (Dual-Track SSoT Governance & Lifecycle Bifurcation)**: Quad-Track lifecycle: Track A (Skills, Python platform scripts, setup-*) executes via [`docu`](file:///var/www/.agents/skills/docu/SKILL.md) through the 8-node harness with atomic snapshots in `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/bak/skills/<skill_name>_v<current_version>.bak/` and `git push origin main` to `zerops-astro-skills`. Track B governs core chassis `zerops-astrobranding` with native Git rollback and push to its own repo. Track C governs derived workloads and apps under Plantilla Universal v4 with client repositories and GitOps pipelines. Track D governs direct SSoT data and content ops in Google Drive.
- **Rule 3 (Immutable Plan Versions, Anti-Amnesia Consolidation & Token Economy)**: In `/var/www/artifacts/` there is strictly EXACTLY ONE active plan per workflow (`<name>_vN.md`, 50–80 lines). Invariante Anti-Inflación & Token Economy: Planes son contratos ejecutables ultra-densos (50-80 líneas); prohibido reescribir diagnósticos enciclopédicos completos o narrativa redundante entre versiones. Invariante de Versionamiento Evolutivo Acumulativo (Anti-Amnesia): Toda versión subsiguiente `_v(N+1).md` es obligatoriamente un superset estricto de `_vN.md`, preservando el 100% de requerimientos funcionales, tareas, rutas y descubrimientos previos mediante deltas concisos. F4 Feedback Loop Mandate & Invariante Anti-Cháchara: Todo ajuste de diseño, consulta o feedback recibido tras F4 invalida la versión actual y exige bump inmediato a `_v(N+1).md` en disco en el mismo turno antes de responder en chat, archivo atómico de la versión previa vía `plan-archive`, y validación con `plan-validate` (exit 0) antes de solicitar Go. Resumption requires explicit user Go (`Go`, `si`). On execution completion in F5, `plan-archive <plan> --executed` archiva la versión final ejecutada y purga borradores superseded obsoletos en `artifacts/archive/`. Linear Direct API: Linear opera 100% mediante `/var/www/.bin/linear-cli` consumiendo directamente `https://api.linear.app/graphql` (<300ms), indexando cada nodo a un ID de Linear (`BAI-*`) y actualizando estados (In Progress -> exit 0 -> Done) para erradicar falsos OK.
- **Rule 4 (SSoT Indivisibility & Universal Clean-Room Virgin ZCP Law)**: Tooling assets reside in `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/scripts/` and provision via `unisetup.sh`. Clean-room benchmark requires 0 drift (`ssot-parity-check` exit 0). Blindaje Anti-Freeze FUSE: Prohibido ejecutar comandos recursivos ciegos (`find`, `grep -r`) sobre montajes remotos de Google Drive sin podar (`-prune`); los sensores y herramientas residen fijos en `/usr/local/bin/`.
- **Rule 5 (Closed Lifecycle Topology & Zero-Omission Checklist Gate)**: Executes the closed 8-node sequence ($N_1$ Backup $\to$ $N_2$ `unisetup.sh` SSoT $\to$ $N_3$ SemVer $\to$ $N_4$ Zero Deletion / CoHaLo $\to$ $N_5$ Drive Mirror & Sovereign Repo Sync (`zerops-astro-skills` git push) $\to$ $N_6$ Physical Sensors $\to$ $N_7$ Skill Registry $\to$ $N_8$ Auto-Purge, Git Parity & LTM) strictly on Track A. Tracks B, C and D execute domain-native agile steps.

## Decision Gates

| Use Case | Action / Protocol | Reference |
|---|---|---|
| Inflow Grounding (F0) | 12-engine cascade | [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) · [`research`](file:///var/www/.agents/skills/research/SKILL.md) |
| Skill Governance (Track A) | Physical 8-node harness | [`docu`](file:///var/www/.agents/skills/docu/SKILL.md) · [`skill-improver`](file:///var/www/.agents/skills/skill-improver/SKILL.md) · [`skill-creator`](file:///var/www/.agents/skills/skill-creator/SKILL.md) |
| Governance Contracts | SSoT indivisibility | [`references/governance_contracts.md`](file:///var/www/.agents/skills/planner/references/governance_contracts.md) |
| Plan Integrity (F4) | Run `plan-validate` | [`scripts/plan-validate.sh`](file:///var/www/.agents/skills/planner/scripts/plan-validate.sh) |
| Plan Archival & Hygiene | Run `plan-archive` | [`scripts/plan-archive.sh`](file:///var/www/.agents/skills/planner/scripts/plan-archive.sh) |
| Linear Roadmap Sync | Sincronizar epics | [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) |
| Physical Attestation (F5) | Verify exit code 0 | [`references/control_matrix_standard.md`](file:///var/www/.agents/skills/planner/references/control_matrix_standard.md) |

## Critical Workflows / Execution Steps
1. **F0 (Inflow)**: Recall local LTM (`mem_search`); execute grounding via [`research`](file:///var/www/.agents/skills/research/SKILL.md).
2. **F1 (Clarification Gate)**: Ask 1 concise question for ambiguities, stopping immediately.
3. **F2 (Dual-RAG Pre-Plan)**: Verify [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) and map closed 8-node sequence.
4. **F3 (Validation Feedforward)**: Validate topology with static linters (`zcp-validate`).
5. **F4 (Plan Offload & Halt)**: Write condensed plan to `/var/www/artifacts/<plan_name>_v1.md`, archive prior versions via `plan-archive`, validate with `plan-validate` (exit 0), and HALT for user Go.
6. **F5 (Execution & Purge)**: Execute Track steps (8 nodes $N_1$ to $N_8$ for Track A; agile deployment/verification milestones for Track B/C). Bounded execution (`timeout 10s`). Archive plan via `plan-archive <plan> --executed`, verify root artifacts cleanliness, and commit (`mem_save`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) · [`references/planning_heuristics.md`](file:///var/www/.agents/skills/planner/references/planning_heuristics.md)
- [`references/governance_contracts.md`](file:///var/www/.agents/skills/planner/references/governance_contracts.md) · [`references/control_matrix_standard.md`](file:///var/www/.agents/skills/planner/references/control_matrix_standard.md)
- [`assets/plan_template.md`](file:///var/www/.agents/skills/planner/assets/plan_template.md) · [`scripts/planner-validate.sh`](file:///var/www/.agents/skills/planner/scripts/planner-validate.sh) · [`scripts/plan-validate.sh`](file:///var/www/.agents/skills/planner/scripts/plan-validate.sh) · [`scripts/plan-archive.sh`](file:///var/www/.agents/skills/planner/scripts/plan-archive.sh)
