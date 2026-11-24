---
name: cohalo
description: "Trigger: cohalo, context engineering, prompt engineering, harness engineering, loop engineering, agent architecture, positive guidance. Context, Harness & Loop architecture under Supreme Directive v10.0."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "10.0"
---

# `cohalo` — COntext, HArness & LOop Architecture (v10.0)

## Activation Contract
Activate when architecting, authoring, or auditing agent workflows, affirmative prompting (Positive Guidance), deterministic harnesses, or context-budget optimization under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Token optimization and Dual-RAG refactoring reside in [`skill-improver`](file:///var/www/.agents/skills/skill-improver/SKILL.md).

## Sovereign Invariants (Positive Guidance)
- **Rule 1 (Dual-Domain Invariant)**: Scripts/code obey CoHaLo Engineering (`py_compile`/`bash -n`, real tests `exit 0`, zero artificial token caps). Prompts/skills obey CoHaLo Prompting (affirmative closed-domain bounds, Dual-RAG, `SKILL.md <= 480` words).
- **Rule 2 (Scoped Reality Over Checklist Theater)**: Verify the exact modified scope with executable assertions (`bun test`, `pytest`, `py_compile`, `bash -n`, HTTP probes).
- **Rule 3 (Proportional Native Orchestration)**: Track multi-step work natively via `update_steps`. Reserve `/var/www/artifacts/plans/` + explicit `Go` for multi-service or high-risk changes; keep `linear-cli` strictly optional.
- **Rule 4 (KV-Cache Stability & Zero Hook Bloat)**: Keep system prompts and rules lean and immutable during turns; never inject repetitive `PreInvocation` messages into conversation history.
- **Rule 5 (Harness & Process Safety)**: `tool-guard.py` enforces PreToolUse physical safety (<15ms); bound commands (`timeout 10s`) and clean background tasks via `manage_task`.
- **Rule 6 (Epistemic Honesty & Anti-AMN)**: Ground claims in live primary sources via [`mem_search`](file:///var/www/.agents/skills/cohalo/references/context.md), `context7`, `exa`/`tavily`, and `jina:read_url` (`date -u`). Use `Model: "flash"` when delegating broad local read-only audits.
- **Rule 7 (Runtime Hygiene)**: Keep `sys.dont_write_bytecode=True` in platform Python scripts.
- **Rule 8 (Pure Positive Guidance)**: Write deterministic affirmative bounds aligned with [`writing-skills`](file:///var/www/.agents/skills/writing-skills/SKILL.md) and [`writing-for-agents`](file:///var/www/.agents/skills/writing-for-agents/SKILL.md).

## Decision Gates

| Layer | Responsibilities & Techniques | Reference |
|---|---|---|
| **COntext** | Inflow, 4Rs, 4-tier KV prefix, Progressive Disclosure | [`references/context.md`](file:///var/www/.agents/skills/cohalo/references/context.md) · [`references/context_engineering_caching.md`](file:///var/www/.agents/skills/cohalo/references/context_engineering_caching.md) |
| **Prompt** | Positive Guidance, XML delimiters, reasoning models | [`references/prompt_engineering_foundations.md`](file:///var/www/.agents/skills/cohalo/references/prompt_engineering_foundations.md) · [`references/sota_reasoning_prompting.md`](file:///var/www/.agents/skills/cohalo/references/sota_reasoning_prompting.md) |
| **Purge** | Antipatterns removal, Pink Elephant elimination | [`references/antipatterns_deprecations.md`](file:///var/www/.agents/skills/cohalo/references/antipatterns_deprecations.md) |
| **HArness** | Reality sensors (`exit code 0`), AST, process hygiene | [`references/harness.md`](file:///var/www/.agents/skills/cohalo/references/harness.md) |
| **LOops** | Native `agy` Orchestrator, circuit breaker (2 retries), HITL | [`references/loops.md`](file:///var/www/.agents/skills/cohalo/references/loops.md) |
| **Sensor** | Structural & behavioral skill validator | `skills-suite-validate` |

## Resources
- [`references/context.md`](file:///var/www/.agents/skills/cohalo/references/context.md) · [`references/context_engineering_caching.md`](file:///var/www/.agents/skills/cohalo/references/context_engineering_caching.md)
- [`references/prompt_engineering_foundations.md`](file:///var/www/.agents/skills/cohalo/references/prompt_engineering_foundations.md) · [`references/sota_reasoning_prompting.md`](file:///var/www/.agents/skills/cohalo/references/sota_reasoning_prompting.md)
- [`references/antipatterns_deprecations.md`](file:///var/www/.agents/skills/cohalo/references/antipatterns_deprecations.md) · [`references/harness.md`](file:///var/www/.agents/skills/cohalo/references/harness.md) · [`references/loops.md`](file:///var/www/.agents/skills/cohalo/references/loops.md)
