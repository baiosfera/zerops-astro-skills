---
name: meta-skill
description: "Trigger: meta-skill, author skill, create skill, audit skill, refactor skill, optimize skill, certificar skill, dual-rag skill, skill governance. Master Skill Authoring, Auditing & Dual-RAG Orchestrator."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `meta-skill` — Master Skill Authoring & Governance Orchestrator (v1.0)

## Activation Contract
Activate when creating new skills, auditing existing skills, optimizing triggers, unbundling oversized routers into Dual-RAG `references/`, or certifying skill quality. Exclusively governs SKILLS (never application software, scripts, or system rules).

## Hard Rules & Positive Guidance
- **Domain Boundary (Skills-Only)**: Operate strictly on `SKILL.md`, `references/`, `assets/`, and skill metadata. Direct application software changes to `codecraft` and system rules to `meta-system`.
- **Dual-RAG Progressive Disclosure**: Routers (`SKILL.md`) strictly <= 480 words / ~550 tokens. Spatial offloading of deep specifications to `references/usage.md` and `references/infra.md`.
- **Lossless AST & Zero Mutilation**: Enforce `skill-improver` standards. Preserve 100% of functional classes, methods, and error-handling code during unbundling.
- **Pure Positive Guidance**: Formulate all instructions as deterministic, affirmative, and closed-domain contracts ("Emit strictly", "Execute via").
- **Physical Attestation Before Assertion**: Claim task completion strictly after `skills-suite-validate` passes with exit code 0.

## Active Sub-Skills Dispatch Table

| Focus | Sub-Skill | Canonical SSoT Pointer | Responsibility |
|---|---|---|---|
| **Dual-RAG Architecture** | `docu` | [`docu`](file:///var/www/.agents/skills/docu/SKILL.md) | Dual-RAG structure, references decoupling |
| **Constitutional CoHaLo** | `cohalo` | [`cohalo`](file:///var/www/.agents/skills/cohalo/SKILL.md) | Positive guidance, closed domains, router budget |
| **New Skill Scaffold** | `skill-creator` | [`skill-creator`](file:///var/www/.agents/skills/skill-creator/SKILL.md) | Clean-room scaffolding, YAML frontmatter |
| **Lossless Refactor** | `skill-improver` | [`skill-improver`](file:///var/www/.agents/skills/skill-improver/SKILL.md) | AST preservation, unbundling without deletion |
| **Anthropic Evaluation** | `writing-skills` | [`writing-skills`](file:///var/www/.agents/skills/writing-skills/SKILL.md) | Benchmark, evaluation & evaluation harness |
| **Cognitive Clarity** | `writing-for-agents` | [`writing-for-agents`](file:///var/www/.agents/skills/writing-for-agents/SKILL.md) | Interface seams, agent cognitive load |
| **Antigravity CLI** | `agy-customizations` | [`agy-customizations`](file:///home/zerops/.gemini/antigravity-cli/builtin/skills/agy-customizations/SKILL.md) | Loading priority, hooks, MCP and CLI rules |

## Decision Gates

| Challenge | Action / Protocol | Reference |
|---|---|---|
| New Skill Scaffolding | Scaffold via `skill-creator` + `docu` | [`references/usage.md#1-scaffolding-protocol`](file:///var/www/.agents/skills/meta-skill/references/usage.md) |
| Skill Audit & Triggers | Audit frontmatter triggers, unbundle deep text | [`references/usage.md#2-audit-protocol`](file:///var/www/.agents/skills/meta-skill/references/usage.md) |
| AST & Symbol Preservation | Zero deletion, verify AST | [`references/infra.md#1-ast-preservation`](file:///var/www/.agents/skills/meta-skill/references/infra.md) |
| Physical Certification | Execute universal validation sensor | `skills-suite-validate` |

## Commands
```bash
# Execute universal physical validation sensor
skills-suite-validate
```

## Resources
- [`references/usage.md`](file:///var/www/.agents/skills/meta-skill/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/meta-skill/references/infra.md)
