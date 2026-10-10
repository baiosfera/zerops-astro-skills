---
name: skill-improver
description: "Trigger: improve skills, audit skills, refactor skills, skill quality. Audit and upgrade existing LLM-first skills."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.2"
---

## Activation Contract

Use this skill when asked to audit, refactor, normalize, or improve existing `SKILL.md` files. Use `skill-creator` instead when creating a brand-new skill from a reusable pattern.

## Hard Rules

- Treat `docs/skill-style-guide.md` as the normative style contract when it exists.
- For installed global skills, use `references/skill-style-guide.md` as the bundled local copy when `docs/skill-style-guide.md` is unavailable.
- Treat `SKILL.md` as the source of truth; preserve author intent, critical rules, activation semantics, and output requirements.
- Use `.atl/skill-registry.md` as an index of skill names, triggers, scopes, and exact paths.
- Default to audit-only. Modify files exclusively upon explicit user request.
- Preserve all meaningful content unconditionally; relocate extensive explanations, schemas, and templates into local `references/` or `assets/` to enable Dual-RAG progressive disclosure.
- Derive triggers, policies, and domain rules strictly from validated codebase evidence, flagging ambiguous cases for human review.
- Enforce Pure Positive Guidance: formulate directives as affirmative closed-domain instructions, eliminating negative shouting and pink elephants.
- Enforce Dual-RAG Token Optimization without Mutilation: keep router bodies lean (180–450 tokens) while preserving 100% of technical contracts in modular references.

## Decision Gates

| Situation | Action |
| --- | --- |
| Missing or invalid frontmatter | Standardize `name`, quoted one-line `description`, `license`, and `metadata` |
| Negative prohibitions or shouting | Transmute into affirmative closed-domain bounds per `references/cohalo_guidelines.md` |
| Tutorial prose or extensive schemas | Relocate to `references/` preserving complete technical contracts (Dual-RAG) |
| Body exceeds budget | Retain rules in router; move examples and background to supporting references |
| Branching logic hidden in prose | Convert to a compact decision table |
| Conflicting rules or unclear intent | Escalate for human review, keeping the existing rule unchanged |

## Execution Steps

1. Read `docs/skill-style-guide.md`; if unavailable, read `references/skill-style-guide.md`; if neither exists, enforce the core LLM-first structure: frontmatter, Activation Contract, Hard Rules, Decision Gates, Execution Steps, Output Contract, References.
2. Read `.atl/skill-registry.md`; use listed paths to select skills. If missing, scan known skill directories for `*/SKILL.md`.
3. For each selected skill, audit metadata, trigger clarity, section order, body budget, actionability, decision gates, output contract, and local references.
4. Return an audit report grouped by skill with severity and exact proposed changes.
5. In apply mode, edit only safe issues, preserve content, create supporting files when needed, then rerun or request `gentle-ai skill-registry refresh`.

## Output Contract

Return:
- Skills audited and paths used.
- Issues found, grouped by severity.
- Files changed, if apply mode was requested.
- Registry refresh recommendation when skill metadata or paths changed.
- Ambiguities that need human review.

## References

- `docs/skill-style-guide.md` — normative LLM-first skill style guide for this repo.
- `references/skill-style-guide.md` — bundled local copy for installed global skills when the repo doc is unavailable.
- `references/cohalo_guidelines.md` — CoHaLo pure positive guidance and Dual-RAG token optimization specifications.
