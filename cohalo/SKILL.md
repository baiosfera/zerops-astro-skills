---
name: cohalo
description: "Trigger: cohalo, context engineering, prompt engineering, harness engineering, loop engineering, agent architecture, state machine, fractal cohalo, positive guidance, kv cache. SOTA Context, Harness & Loop architecture under Supreme Directive v7.6."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "7.0"
---

# `cohalo` — COntext, HArness & LOop Sovereign Architecture (v7.0)

## Activation Contract
Activate when architecting, authoring, auditing, or executing agent workflows, prompt/context caching, token optimization, deterministic execution harnesses, skill refactors, or the 6-phase gated state machine under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md).

## Hard Rules (Positive Guidance & Closed Domains)
- **Rule 1 (Context & Progressive Disclosure)**: Epistemic Inflow acquires facts via `date -u`, LTM recall ([`mem_search`](file:///var/www/.agents/skills/cohalo/references/context.md)), and verbatim extraction. Enforces 100% KV cache hits via the 4-tier immutable prefix (Tools $\to$ System SSoT $\to$ LTM JIT $\to$ User). Employs Progressive Disclosure, offloading roadmaps to `/var/www/artifacts/` and auto-purging plans (`rm -f`).
- **Rule 2 (Positive Guidance & Structured Output)**: Prompts use XML delimiters (`<instructions>`, `<rules>`, `<context>`, `<output_format>`). Specifies affirmative closed domains ("Instead, Do X"). Enforces Structured Outputs (JSON Schema / Pydantic / Zod) with constrained decoding and calibrated reasoning budgets.
- **Rule 3 (Harness & Deterministic Sensors)**: Encapsulates execution within feedforward guides (`zcp-validate`, linters) and feedback sensors (`exit code 0`, HTTP 200, unit tests). Enforces bounded limits (`timeout 10s`, `WaitMsBeforeAsync: 10000`, process cleanup via `manage_task action="kill"`), and filesystem shielding.
- **Rule 4 (Loops & 6-Phase State Machine)**: Mandates sequential progression: F0 (Inflow) $\to$ F1 (Clarification Gate) $\to$ F2 (Dual-RAG Pre-Plan) $\to$ F3 (Validation Feedforward) $\to$ F4 (Plan Offload & Halt) $\to$ F5 (Execution, Attestation & Auto-Purge). Circuit breakers enforce a 2-attempt limit. Phase F4 requires sovereign human authorization in `USER_INPUT`.
- **Rule 5 (Runtime-Agnostic Portability)**: Operates with vendor neutrality via POSIX shell standards, relative paths, semantic Markdown, and open specifications.

## Decision Gates

| Layer | Responsibilities & Techniques | Reference |
|---|---|---|
| **COntext** | Inflow, 4Rs, 4-tier KV prefix, Progressive Disclosure | [`references/context.md`](file:///var/www/.agents/skills/cohalo/references/context.md) · [`references/context_engineering_caching.md`](file:///var/www/.agents/skills/cohalo/references/context_engineering_caching.md) |
| **Prompt** | Positive Guidance, XML delimiters, reasoning models | [`references/prompt_engineering_foundations.md`](file:///var/www/.agents/skills/cohalo/references/prompt_engineering_foundations.md) · [`references/sota_reasoning_prompting.md`](file:///var/www/.agents/skills/cohalo/references/sota_reasoning_prompting.md) |
| **Purge** | Antipatterns removal, Pink Elephant elimination | [`references/antipatterns_deprecations.md`](file:///var/www/.agents/skills/cohalo/references/antipatterns_deprecations.md) |
| **HArness** | Guides, sensors (`exit code 0`), process hygiene | [`references/harness.md`](file:///var/www/.agents/skills/cohalo/references/harness.md) |
| **LOops** | 6-phase FSM (F0-F5), circuit breaker (2 retries), HITL | [`references/loops.md`](file:///var/www/.agents/skills/cohalo/references/loops.md) |
| **Sensor** | Deterministic validator checking v7.0 & Positive Guidance | [`scripts/cohalo-validate.sh`](file:///var/www/.agents/skills/cohalo/scripts/cohalo-validate.sh) |

## Commands
```bash
# Execute deterministic physical validation sensor
bash /var/www/.agents/skills/cohalo/scripts/cohalo-validate.sh
```

## Resources
- [`references/context.md`](file:///var/www/.agents/skills/cohalo/references/context.md) · [`references/context_engineering_caching.md`](file:///var/www/.agents/skills/cohalo/references/context_engineering_caching.md)
- [`references/prompt_engineering_foundations.md`](file:///var/www/.agents/skills/cohalo/references/prompt_engineering_foundations.md) · [`references/sota_reasoning_prompting.md`](file:///var/www/.agents/skills/cohalo/references/sota_reasoning_prompting.md)
- [`references/antipatterns_deprecations.md`](file:///var/www/.agents/skills/cohalo/references/antipatterns_deprecations.md) · [`references/harness.md`](file:///var/www/.agents/skills/cohalo/references/harness.md) · [`references/loops.md`](file:///var/www/.agents/skills/cohalo/references/loops.md)
- [`scripts/cohalo-validate.sh`](file:///var/www/.agents/skills/cohalo/scripts/cohalo-validate.sh)
