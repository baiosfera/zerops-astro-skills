---
name: planner
description: "Trigger: planner, plan, master-plan, planificar, crear plan, diseña un plan, /plan, change proposal, version plan, roadmap. Universal Master Planning & SSoT Governance Orchestrator under CoHaLo v8.4 and Supreme Directive v8.3."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "9.4"
---

# Planner — Universal Master Planning & SSoT Governance Orchestrator (v9.4)

## Activation Contract
Activate for multi-step refactors and governance under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Bounded tasks execute inline without ceremonial plans. Eradicates checklist theater.

## Hard Rules (Positive Guidance)
- **Rule 1 (CoHaLo Positive Guidance & Continuous Present Inflow)**: Anchors decisions to live runtime state (`date -u`). Grounding follows [`research`](file:///var/www/.agents/skills/research/SKILL.md) inline or via subagent. Details in [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md).
- **Rule 2 (Dual-Track SSoT Governance & Lifecycle Bifurcation)**: Quad-Track lifecycle: Track A (Skills, Python platform scripts, setup-*) executes via [`docu`](file:///var/www/.agents/skills/docu/SKILL.md) through the 8-node harness with atomic snapshots in `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/bak/skills/<skill_name>_v<current_version>.bak/` and `git push origin main` to `zerops-astro-skills`. Track B governs core chassis `zerops-astrobranding` with native Git rollback and push to its own repo. Track C governs derived workloads and apps under Plantilla Universal v4 with client repositories and GitOps pipelines. Track D governs direct SSoT data and content ops in Google Drive.
- **Rule 3 (Linear State Machine, Anti-Amnesia Consolidation & Token Economy)**: El planner erradica el bloat de tokens migrando 100% la burocracia de planes al sistema de tickets Linear. Todo plan, paso a paso, descubrimiento o ajuste de feedback se consolida de forma acumulativa en la descripción de los Issues y Sub-issues en Linear (vía `linear-cli issue create` y `linear-cli issue update`). Se vincula el Issue ID raíz en `/var/www/artifacts/linear_active.json` para destrabar los arneses de mutación. F4 Feedback Loop Mandate: Todo ajuste de diseño o feedback exige registrar y consolidar las adiciones o sustracciones en el Issue/Sub-issue correspondiente antes de pedir Go. F5 Parity: Linear opera mediante `/usr/local/bin/linear-cli` conectando a `https://api.linear.app/graphql`, indexando cada nodo a un ID (`BAI-*`). Tras la atestación de compiladores/tests, se avanza el estado del Issue a "Done" (`linear-cli update-status "Done"`).
- **Rule 4 (SSoT Indivisibility & Universal Clean-Room Virgin ZCP Law)**: Tooling assets reside in `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/scripts/` and provision via `unisetup.sh`. Clean-room benchmark requires 0 drift (`ssot-parity-check` exit 0). Blindaje Anti-Freeze FUSE: Prohibido ejecutar comandos recursivos ciegos (`find`, `grep -r`) sobre montajes remotos de Google Drive sin podar (`-prune`); los sensores y herramientas residen fijos en `/usr/local/bin/`.
- **Rule 5 (Closed Lifecycle Topology & Zero-Omission Checklist Gate)**: Executes the closed 8-node sequence ($N_1$ Backup $\to$ $N_2$ `unisetup.sh` SSoT $\to$ $N_3$ SemVer $\to$ $N_4$ Zero Deletion / CoHaLo $\to$ $N_5$ Drive Mirror & Sovereign Repo Sync (`zerops-astro-skills` git push) $\to$ $N_6$ Physical Sensors $\to$ $N_7$ Skill Registry $\to$ $N_8$ Auto-Purge, Git Parity & LTM) strictly on Track A. Tracks B, C and D execute domain-native agile steps.

## Decision Gates

| Use Case | Action / Protocol | Reference |
|---|---|---|
| Inflow Grounding (F0) | 12-engine cascade | [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) · [`research`](file:///var/www/.agents/skills/research/SKILL.md) · [`cohalo`](file:///var/www/.agents/skills/cohalo/SKILL.md) |
| Skill Governance (Track A) | Physical 8-node harness | [`docu`](file:///var/www/.agents/skills/docu/SKILL.md) · [`skill-improver`](file:///var/www/.agents/skills/skill-improver/SKILL.md) · [`skill-creator`](file:///var/www/.agents/skills/skill-creator/SKILL.md) |
| Governance Contracts | SSoT indivisibility | [`references/governance_contracts.md`](file:///var/www/.agents/skills/planner/references/governance_contracts.md) |
| Plan Integrity (F4) | Sincronizar y Crear Issue | `linear-cli issue create` |
| Plan Archival & Hygiene | Cerrar Issue | `linear-cli update-status "Done"` |
| Linear Roadmap Sync | Sincronizar epics | [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) |
| Physical Attestation (F5) | Verify exit code 0 | [`references/control_matrix_standard.md`](file:///var/www/.agents/skills/planner/references/control_matrix_standard.md) |

## Critical Workflows / Execution Steps
1. **F0 (Inflow)**: Recall local LTM (`mem_search`); execute grounding via [`research`](file:///var/www/.agents/skills/research/SKILL.md).
2. **F1 (Clarification Gate)**: Ask 1 concise question for ambiguities, stopping immediately.
3. **F2 (Dual-RAG Pre-Plan)**: Verify [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) and map closed 8-node sequence.
4. **F3 (Validation Feedforward)**: Validate topology with static linters (`zcp-validate`).
5. **F4 (Plan Offload & Halt)**: **Organización Linear**: Enforce the creation of a NEW Linear Project for EVERY plan, without exception. Strictly isolate each domain in a separate BAI Issue. Create the Project and Issues via Linear CLI detailing the requirements, reference the active Issue ID in `/var/www/artifacts/linear_active.json`, and HALT (freno de mano) en chat solicitando exclusivamente el Go del usuario.
6. **F5 (Execution & Parity)**: Execute Track steps (8 nodes $N_1$ to $N_8$ for Track A; agile deployment/verification milestones for Track B/C). Bounded execution (`timeout 10s`). Al completar cada sub-tarea y validar con tests, actualizar el estado en Linear a "Done", y realizar `ssot-parity-check` y `git push` respectivos.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) · [`references/planning_heuristics.md`](file:///var/www/.agents/skills/planner/references/planning_heuristics.md)
- [`references/governance_contracts.md`](file:///var/www/.agents/skills/planner/references/governance_contracts.md) · [`references/control_matrix_standard.md`](file:///var/www/.agents/skills/planner/references/control_matrix_standard.md)
