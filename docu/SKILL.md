---
name: docu
description: "Builds, evolves, certifies, and holistically audits deep Dual-RAG skills across 4 functional archetypes with Fractal CoHaLo. Trigger: docu, build skill, create skill, document tool, generate usage.md, generate infra.md, dual-rag, package skill, scaffold skill, reference builder, audit skill."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "7.2"
---

# `docu` — Autonomous Dual-RAG Skill & Reference Architect (v7.2)

## Activation Contract
Activate when authoring, updating, certifying, or auditing Dual-RAG skills across 4 functional archetypes (Framework, Infra, Domain, Cognitive), generating reference manuals (`references/usage.md` and `references/infra.md`), or executing Phase F2 under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Operates in: **Scaffold Mode** (via `skill-creator`), **Patch / Refactor Mode** (via `skill-improver` + Zero Deletion + CoHaLo), and **Certification & Invariance Mode**.

## Hard Rules (Positive Guidance & Closed Domains)
- **Rule 1 (Epistemic Inflow & Archetype Mapping)**: Ingests research dossiers and maps tools to 1 of 4 archetypes (Framework, Infra, Domain, Cognitive) per [`assets/research_ingestion_protocol.md`](file:///var/www/.agents/skills/docu/assets/research_ingestion_protocol.md). Unbundles 100% of discoveries into target references. Zero permanent links to temporary `/var/www/artifacts/`.
- **Rule 2 (Normative Layout & Progressive Disclosure)**: Enforces 3 levels: Discovery (`name` + `description` with triggers), Activation (`SKILL.md` router <= 550 tokens), and Execution JIT (`references/`, `assets/`, `scripts/`).
- **Rule 3 (Lossless Invariant, Zero Deletion & skill-improver)**: Preserves 100% of technical signals (endpoints, types, recipes, error codes) via spatial offloading to `references/` without truncation, applying `skill-improver` audit standards (converting prose into decision matrices, enforcing style guide).
- **Rule 4 (Fractal CoHaLo Isomorphism & Deep Hygiene)**: Compiled skills require executable harnesses (`timeout 10s`, `WaitMsBeforeAsync: 10000`, process cleanup), sensor attestation (`exit code 0`), circuit breakers (2-attempt limit), and zero bytecode residue (zero `__pycache__`).
- **Rule 5 (Scaffolding & skill-creator Standard)**: Scaffolds new skills strictly adhering to `skill-creator` standards (compact router, progressive disclosure, assets/references layout) via [`assets/skill_scaffold.py`](file:///var/www/.agents/skills/docu/assets/skill_scaffold.py).
- **Rule 6 (8-Node Anti-Amnesia Physical Harness & SSoT Parity)**: Executes skill mutations strictly through 8 sequential checkpoints: (1) Backup in `0zcp-123/bak/skills/` (enforced by `tool-guard.py`), (2) `skill-improver` lossless unbundling, (3) SemVer bump, (4) CoHaLo positive guidance, (5) Drive SSoT mirror, (6) Generator sync in `unisetup.sh` / `setup-drive.sh`, (7) Deterministic sensor attestation (`exit code 0`), and (8) Registry refresh (`gentle-ai skill-registry refresh --force`) + Engram commit (`mem_save`). Bypassing any checkpoint is strictly prohibited.

## Decision Gates

| Task / Need | Action / Protocol | Reference |
|---|---|---|
| **Skill Certification & Invariance** | Audit existing skills against 5 normative criteria; zero mutations | [`references/certification.md`](file:///var/www/.agents/skills/docu/references/certification.md) |
| **Construction & Audit Lifecycle** | 8-step lifecycle across 4 functional archetypes | [`references/workflow.md`](file:///var/www/.agents/skills/docu/references/workflow.md) |
| **Dual-RAG Skeletons & Harness** | Canonical `SKILL.md`, `usage.md`, `infra.md` templates | [`references/templates.md`](file:///var/www/.agents/skills/docu/references/templates.md) |
| **Research Ingestion Protocol** | Decoupled archetype mapping without rigid pass counts | [`assets/research_ingestion_protocol.md`](file:///var/www/.agents/skills/docu/assets/research_ingestion_protocol.md) |
| **Research Subagent Delegation** | Canonical research contract (12 engines) | [`assets/subagent_meta_prompt_template.md`](file:///var/www/.agents/skills/docu/assets/subagent_meta_prompt_template.md) |
| **Automated Scaffolding** | Python generator with 4 archetypes and AST verification | [`assets/skill_scaffold.py`](file:///var/www/.agents/skills/docu/assets/skill_scaffold.py) |
| **Physical Sensor** | Deterministic validator with live round-trip scaffolding test | [`scripts/docu-validate.sh`](file:///var/www/.agents/skills/docu/scripts/docu-validate.sh) |

## Commands
```bash
# Execute deterministic physical validation sensor
bash /var/www/.agents/skills/docu/scripts/docu-validate.sh
```

## Resources
- [`references/certification.md`](file:///var/www/.agents/skills/docu/references/certification.md) · [`references/workflow.md`](file:///var/www/.agents/skills/docu/references/workflow.md) · [`references/templates.md`](file:///var/www/.agents/skills/docu/references/templates.md)
- [`assets/research_ingestion_protocol.md`](file:///var/www/.agents/skills/docu/assets/research_ingestion_protocol.md) · [`assets/subagent_meta_prompt_template.md`](file:///var/www/.agents/skills/docu/assets/subagent_meta_prompt_template.md) · [`assets/skill_scaffold.py`](file:///var/www/.agents/skills/docu/assets/skill_scaffold.py)
- [`scripts/docu-validate.sh`](file:///var/www/.agents/skills/docu/scripts/docu-validate.sh)
