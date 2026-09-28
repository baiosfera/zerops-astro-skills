---
name: cohalo
description: "Trigger: cohalo, context engineering, prompt engineering, harness engineering, loop engineering, agent architecture, state machine, fractal cohalo, positive guidance, kv cache. SOTA Context, Harness & Loop architecture under Supreme Directive v8.2."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "8.2"
---

# `cohalo` — COntext, HArness & LOop Sovereign Architecture (v8.2)

## Activation Contract
Activate when architecting, authoring, auditing, or executing agent workflows, prompt/context caching, token optimization, deterministic execution harnesses, skill refactors, or the 6-phase gated state machine under [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md).

## Sovereign Invariants & Hard Rules (Positive Guidance)
- **Rule 1 (Reality Over Checklist Theater)**: All verification relies on physical software assertions (`bun test`, `tsc`, `bash -n`, AST, exit code 0). Replaces checklist theater with deterministic execution sensors.
- **Rule 2 (Autonomous Remediation & Execution Closure)**: Mandatory execution closure within the same turn. F0 activation reads physical `SKILL.md`, executes compilers and tests, reflects to SSoT, and pushes to git (`git push`).
- **Rule 3 (ZCP-First & Indivisible SSoT)**: Active development resides in ZCP (`/var/www`). Tested changes reflect indivisibly to Google Drive SSoT (`0zcp-123/`). Offloads roadmaps to `/var/www/artifacts/`.
- **Rule 4 (Process-Level Safety & Token Hygiene)**: Process safety and deduplication are enforced by `tool-guard.py` at PreToolUse/PreInvocation. Harnesses enforce bounded limits (`timeout 10s`, `WaitMsBeforeAsync: 10000`) and process cleanup via `manage_task`.
- **Rule 5 (Epistemic Honesty & Absolute Anti-AMN Mandate)**: Eliminates pretrained memory assumptions (AMN). Code and claims anchor in live primary sources via [`mem_search`](file:///var/www/.agents/skills/cohalo/references/context.md), Context7, and verbatim official documentation.
- **Rule 6 (Continuous Present & Token Economy)**: Anchors to live runtime state (`date -u`). Ensures 100% KV cache hits via the immutable 4-tier prefix (Tools $\to$ System SSoT $\to$ LTM JIT $\to$ User). Maintains router budgets <= 480 words and zero bytecode residue (`__pycache__`).

## Decision Gates

| Layer | Responsibilities & Techniques | Reference |
|---|---|---|
| **COntext** | Inflow, 4Rs, 4-tier KV prefix, Progressive Disclosure | [`references/context.md`](file:///var/www/.agents/skills/cohalo/references/context.md) · [`references/context_engineering_caching.md`](file:///var/www/.agents/skills/cohalo/references/context_engineering_caching.md) |
| **Prompt** | Positive Guidance, XML delimiters, reasoning models | [`references/prompt_engineering_foundations.md`](file:///var/www/.agents/skills/cohalo/references/prompt_engineering_foundations.md) · [`references/sota_reasoning_prompting.md`](file:///var/www/.agents/skills/cohalo/references/sota_reasoning_prompting.md) |
| **Purge** | Antipatterns removal, Pink Elephant elimination | [`references/antipatterns_deprecations.md`](file:///var/www/.agents/skills/cohalo/references/antipatterns_deprecations.md) |
| **HArness** | Reality sensors (`exit code 0`), AST, process hygiene | [`references/harness.md`](file:///var/www/.agents/skills/cohalo/references/harness.md) |
| **LOops** | 6-phase FSM (F0-F5), circuit breaker (2 retries), HITL | [`references/loops.md`](file:///var/www/.agents/skills/cohalo/references/loops.md) |
| **Sensor** | Deterministic validator checking v8.2 & Positive Guidance | [`scripts/cohalo-validate.sh`](file:///var/www/.agents/skills/cohalo/scripts/cohalo-validate.sh) |

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
