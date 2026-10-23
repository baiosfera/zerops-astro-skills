---
name: meta-system
description: "Trigger: meta-system, supreme directive, 00-supreme, agents md, system prompt, governance rules, positive guidance, closed domain, cognitive doc design, domain modeling, system architecture. Master System Directives, Governance Rules & Context Architecture Orchestrator."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `meta-system` — Master System Directives & Context Architecture Orchestrator (v1.0)

## Activation Contract
Activate when creating, auditing, refactoring, or optimizing system directives, constitutional rules (`00-SUPREME-DIRECTIVE.md`), platform contracts (`AGENTS.md`), system prompts, or agent personas. Exclusively governs SYSTEM-LEVEL RULES, CONTEXT ARCHITECTURE, AND GOVERNANCE (never individual skills, application code, or platform scripts).

## Hard Rules & Positive Guidance
- **Domain Boundary (System Governance Only)**: Operate strictly on rules (`.agents/rules/`), instructions (`AGENTS.md`), agent personas, and system prompts. Direct skill changes to `meta-skill`, application software to `codecraft`, and shell/python scripts to `meta-script`.
- **Pure Positive Guidance**: Formulate all constitutional directives and rules as deterministic, affirmative, and closed-domain contracts ("Emit strictly", "Execute via", "Anchor in"). Eliminate open-ended negative prohibitions.
- **Cognitive Load Minimization**: Structure rules with `cognitive-doc-design`: lead with the decision, use progressive disclosure, chunk related invariants into high-contrast tables, and prioritize recognition over recall.
- **Checkable Completion Criteria**: Every system directive must specify its physical verification sensor or exit-0 proof command (`writing-for-agents`). Vague bounds ("maintain quality", "be careful") are strictly prohibited.
- **Physical Attestation Before Assertion**: Claim task completion strictly after `skills-suite-validate` and `ssot-parity-check` pass with exit code 0.

## Active Sub-Skills Dispatch Table

| Focus | Sub-Skill | Canonical SSoT Pointer | Responsibility |
|---|---|---|---|
| **Context & Harness** | `cohalo` | [`cohalo`](file:///var/www/.agents/skills/cohalo/SKILL.md) | CoHaLo Prompting, Positive Guidance, closed domains, state machines |
| **Agent Clarity** | `writing-for-agents` | [`writing-for-agents`](file:///var/www/.agents/skills/writing-for-agents/SKILL.md) | Context pointers, information hierarchy, checkable criteria |
| **Cognitive Design** | `cognitive-doc-design` | [`cognitive-doc-design`](file:///var/www/.agents/skills/cognitive-doc-design/SKILL.md) | Chunking, recognition over recall, visual tables, review empathy |
| **Canonical Terms** | `domain-modeling` | [`domain-modeling`](file:///var/www/.agents/skills/domain-modeling/SKILL.md) | Bounded context terminology, GLOSSARY.md, Architectural Decision Records (ADRs) |

## Decision Gates

| Challenge | Action / Protocol | Reference |
|---|---|---|
| Directive Authoring & Sizing | Formulate affirmative bounds under Cognitive Doc Design | [`references/usage.md#1-directive-authoring`](file:///var/www/.agents/skills/meta-system/references/usage.md) |
| Negative to Positive Refactor | Convert prohibitive clauses to closed-domain contracts | [`references/usage.md#2-positive-guidance-refactor`](file:///var/www/.agents/skills/meta-system/references/usage.md) |
| Architecture Decision Records | Document foundational decisions using ADR templates | [`references/usage.md#3-adr-governance`](file:///var/www/.agents/skills/meta-system/references/usage.md) |
| Rule Invariants & Thresholds | Verify rule size bounds and single-screen legibility | [`references/infra.md#1-rule-sizing-thresholds`](file:///var/www/.agents/skills/meta-system/references/infra.md) |
| Physical Certification | Execute universal validation and SSoT anti-drift sensors | `skills-suite-validate` · `ssot-parity-check` |

## Commands
```bash
# Execute universal physical validation sensor
skills-suite-validate

# Verify SSoT parity across Drive, Git, and active rules
ssot-parity-check
```

## References
- [`references/usage.md`](file:///var/www/.agents/skills/meta-system/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/meta-system/references/infra.md)
