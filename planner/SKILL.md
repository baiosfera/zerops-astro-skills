---
name: planner
description: "Trigger: planner, plan, master-plan, planificar, crear plan, diseña un plan, /plan, change proposal, version plan, roadmap. Universal Master Planning & SSoT Governance Orchestrator under CoHaLo v7.0 and Supreme Directive v7.8."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.0"
---

# Planner — Universal Master Planning & SSoT Governance Orchestrator (v4.0)

## Activation Contract
Activate for architecture designs, multi-step roadmaps, Dual-Track evaluations, and structured governance workflows under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Unrelated single-action tasks execute inline without full planning ceremonies.

## Hard Rules (Positive Guidance)
- **Rule 1 (CoHaLo Positive Guidance & Continuous Present Inflow)**: Anchors decisions to runtime state (`date -u`). Grounding follows [`research`](file:///var/www/.agents/skills/research/SKILL.md) (Modality A inline or Modality B subagent contract with `<epistemic_attestation>`). Details in [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md).
- **Rule 2 (Dual-Track SSoT Governance & Lifecycle Bifurcation)**: Operates strictly under Track A (Skill Governance & SSoT — fully delegated to [`docu`](file:///var/www/.agents/skills/docu/SKILL.md) which executes the 8-node anti-amnesia physical harness without ceremonial paperwork) or Track B (Zerops Workloads — governing monorepo architecture, Hono/Astro APIs, BullMQ workers, PostgreSQL 18, Valkey 7.2, NATS JetStream, GitOps, and Incus LXC infrastructure). Flat individual uncompressed snapshots at `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/bak/skills/<skill_name>_v<current_version>.bak/`, SemVer bumps, Drive mirror, and Registry sensor are strictly enforced.
- **Rule 3 (Immutable Plan Versions, Anti-Amnesia Consolidation & Token Economy)**: Master plans reside at `/var/www/artifacts/<plan_name>_vN.md`. Iterations increment version numbers (`_v1.md` $\to$ `_v2.md`), strictly preserving prior versions until verified. Auto-Purge strictly targets target plan versions (`rm -f /var/www/artifacts/<plan_name>*.md`), strictly preserving inviolable inter-session handover artifacts (`*_handover*.md`, `*_blueprint*.md`, `*_dossier*.md`). Upon physical sensor attestation (exit code 0) and Engram commit (`mem_save`), temporary plans are purged.
- **Rule 4 (SSoT Indivisibility & Universal Clean-Room Virgin ZCP Law)**: Tooling assets reside in `0zcp-123/scripts/` and provision via `unisetup.sh`. Clean-room virgin ZCP benchmark requires 0 bytes of drift (`ssot-parity-check` exit 0). Mutating generator-backed files requires atomic updates to `setup-*.sh` / `unisetup.sh` and Drive mirror.
- **Rule 5 (Closed Lifecycle Topology & Zero-Omission Checklist Gate)**: Track A plans instantiate the closed 8-node canonical sequence in Section 4 and Section 5: $N_1$ Backup $\to$ $N_2$ `unisetup.sh` SSoT $\to$ $N_3$ SemVer $\to$ $N_4$ Zero Deletion / CoHaLo $\to$ $N_5$ Drive Mirror $\to$ $N_6$ Physical Sensors $\to$ $N_7$ Skill Registry $\to$ $N_8$ Auto-Purge & LTM.

## Decision Gates

| Use Case / Scenario | Action / Pattern | Reference |
|---|---|---|
| Inflow Grounding (F0) | 12-engine cascade via subagent contract | [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) · [`research`](file:///var/www/.agents/skills/research/SKILL.md) |
| Skill Audit / Certification (F2) | Dual-RAG audit & 5 Criteria (C1–C5) | [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) · [`docu`](file:///var/www/.agents/skills/docu/SKILL.md) |
| Skill Refactor / Zero Deletion | Lossless offload to `references/` | [`references/governance_contracts.md`](file:///var/www/.agents/skills/planner/references/governance_contracts.md) · [`skill-improver`](file:///var/www/.agents/skills/skill-improver/SKILL.md) |
| Skill Creation | Canonical anatomy & 4 archetypes | [`references/governance_contracts.md`](file:///var/www/.agents/skills/planner/references/governance_contracts.md) · [`skill-creator`](file:///var/www/.agents/skills/skill-creator/SKILL.md) |
| Workload Deploy (Track B) | Topology validation (`zcp-validate`) & GitOps | [`references/governance_contracts.md`](file:///var/www/.agents/skills/planner/references/governance_contracts.md) · [`bknd`](file:///var/www/.agents/skills/bknd/SKILL.md) · [`frnt`](file:///var/www/.agents/skills/frnt/SKILL.md) |
| Plan Integrity Lint (F4) | Run `plan-validate` (<100ms) before Halt | [`scripts/plan-validate.sh`](file:///var/www/.agents/skills/planner/scripts/plan-validate.sh) |
| Physical Attestation (F5) | Verify exit code 0 across deliverables | [`references/control_matrix_standard.md`](file:///var/www/.agents/skills/planner/references/control_matrix_standard.md) |
| Suite Verification (F5) | Run `skills-suite-validate` CLI before close | [`references/control_matrix_standard.md`](file:///var/www/.agents/skills/planner/references/control_matrix_standard.md) |

## Critical Workflows / Execution Steps
1. **F0 (Inflow)**: Recall local LTM (`mem_search`); execute Fast Grounding inline or deep research via [`research`](file:///var/www/.agents/skills/research/SKILL.md).
2. **F1 (Clarification Gate)**: Detect ambiguities; ask 1 single concise question, stopping immediately.
3. **F2 (Dual-RAG Pre-Plan)**: Verify `references/usage.md`, classify track, enforce positive guidance, map closed 8-node sequence.
4. **F3 (Validation Feedforward)**: Validate topology with deterministic static linters (`zcp-validate`).
5. **F4 (Plan Offload & Halt)**: Write plan in Spanish to `/var/www/artifacts/<plan_name>_v1.md` (`RequestFeedback: false`), validate with `plan-validate` (exit 0), and HALT for human 'go' in `USER_INPUT`.
6. **F5 (Execution & Purge)**: On human 'go', execute 8 nodes in sequence ($N_1$ to $N_8$). Bounded execution (`timeout 10s`). Purge plan post-attestation and commit to Engram (`mem_save`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) — Operational usage manual, 5-skill execution suite, and Dual-Track contracts.
- [`references/planning_heuristics.md`](file:///var/www/.agents/skills/planner/references/planning_heuristics.md) — Planning heuristics and iterative evolution rules.
- [`references/governance_contracts.md`](file:///var/www/.agents/skills/planner/references/governance_contracts.md) — SSoT governance, unisetup.sh-first, and clean-room contracts.
- [`references/control_matrix_standard.md`](file:///var/www/.agents/skills/planner/references/control_matrix_standard.md) — Acceptance criteria and physical sensor matrix.
- [`assets/plan_template.md`](file:///var/www/.agents/skills/planner/assets/plan_template.md) — Canonical plan template.
- [`scripts/planner-validate.sh`](file:///var/www/.agents/skills/planner/scripts/planner-validate.sh) — Deterministic physical validation sensor.
- [`scripts/plan-validate.sh`](file:///var/www/.agents/skills/planner/scripts/plan-validate.sh) — Deterministic plan linter sensor.
