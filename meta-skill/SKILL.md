---
name: meta-skill
description: "Trigger: meta-skill, author skill, create skill, audit skill, refactor skill, optimize skill, certificar skill, dual-rag skill. Master Skill Authoring, Epistemic Grounding & Governance Orchestrator."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `meta-skill` — Master Skill Authoring & Epistemic Governance Orchestrator (v2.0)

## Activation Contract
Activate when authoring new skills, auditing existing skills, upgrading triggers, unbundling into Dual-RAG `references/`, or certifying skill quality. Enforces the sovereign epistemic pipeline: `research` $\to$ `docu` $\to$ `cohalo` $\to$ `skill-improver` $\to$ `writing-*` $\to$ `meta-skill`.

## Hard Rules & Positive Guidance
- **Epistemic Supremacy (`research`-First)**: Triangulate live sources via `research` using subagents (`invoke_subagent` typeName: `research`) and 12 live engines (Context7, Exa, Tavily, Brave, Jina, Firecrawl) before authoring or modifying skills.
- **Absolute Role Demarcation**:
  * `research`: Queen engine. Gathers live ground truth outside the black box.
  * `docu`: Documentalist of truth. Synthesizes research dossiers into canonical specs.
  * `cohalo`: Positive Guidance, affirmative contracts, closed domains.
  * `skill-improver`: Lossless Dual-RAG unbundling (`SKILL.md` $\le 480$ words).
  * `writing-for-agents` & `writing-skills`: Agent ergonomics and benchmarks.
  * `skill-creator`: Clean-room scaffolding.
- **Word Budget & Progressive Disclosure**: Routers (`SKILL.md`) strictly $\le 480$ words. Spatial offload to `references/`.
- **Lossless AST**: Preserve 100% of methods, classes, and error handling during unbundling.
- **Physical Attestation**: Claim completion strictly after `skills-suite-validate` and `ssot-parity-check` pass exit code 0.

## Active Sub-Skills Dispatch Table

| Focus | Sub-Skill | Canonical SSoT Pointer | Responsibility |
|---|---|---|---|
| **Epistemic Inflow** | `research` | [`research`](file:///var/www/.agents/skills/research/SKILL.md) | Queen engine, subagents, 12 engines, live ground truth |
| **Truth Documentation** | `docu` | [`docu`](file:///var/www/.agents/skills/docu/SKILL.md) | Canonical documentation, API specs, reality verification |
| **CoHaLo Prompting** | `cohalo` | [`cohalo`](file:///var/www/.agents/skills/cohalo/SKILL.md) | Positive guidance, affirmative instructions |
| **Lossless Dual-RAG** | `skill-improver` | [`skill-improver`](file:///var/www/.agents/skills/skill-improver/SKILL.md) | Dual-RAG unbundling ($\le 480$ words), AST preservation |
| **New Skill Scaffold** | `skill-creator` | [`skill-creator`](file:///var/www/.agents/skills/skill-creator/SKILL.md) | Clean-room scaffolding, YAML frontmatter |
| **Cognitive Seams** | `writing-for-agents` | [`writing-for-agents`](file:///var/www/.agents/skills/writing-for-agents/SKILL.md) | Seams, agent cognitive load reduction |
| **Anthropic Evaluation** | `writing-skills` | [`writing-skills`](file:///var/www/.agents/skills/writing-skills/SKILL.md) | Benchmark, test scenarios, evaluation harness |

## Decision Gates

| Challenge / Phase | Action / Protocol | Reference |
|---|---|---|
| F0 Epistemic Grounding | Delegate deep research via subagent + 12 engines | [`references/usage.md#1`](file:///var/www/.agents/skills/meta-skill/references/usage.md) |
| Canonical Documentation | Ingest research dossiers into exact specs via `docu` | [`references/usage.md#2`](file:///var/www/.agents/skills/meta-skill/references/usage.md) |
| Prompt Formulation | Apply affirmative Positive Guidance via `cohalo` | [`references/usage.md#3`](file:///var/www/.agents/skills/meta-skill/references/usage.md) |
| Dual-RAG Unbundling | Unbundle into Dual-RAG ($\le 480$ words) via `skill-improver` | [`references/usage.md#4`](file:///var/www/.agents/skills/meta-skill/references/usage.md) |
| Cognitive Optimization | Refine agent readability via `writing-for-agents` | [`references/usage.md#5`](file:///var/www/.agents/skills/meta-skill/references/usage.md) |
| Physical Certification | Execute universal physical sensors (exit 0) | `skills-suite-validate` · `ssot-parity-check` |

## Commands
```bash
skills-suite-validate && ssot-parity-check
```

## Resources
- [`references/usage.md`](file:///var/www/.agents/skills/meta-skill/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/meta-skill/references/infra.md)
