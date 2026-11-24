# `meta-plan` — Usage & Implementation Guide (v2.0)

Operational procedures for proportional planning, native `agy 1.5.16` step tracking, and optional Linear coordination under Supreme Directive v10.0.

---

## 1. Proportional Activation Threshold (Zero-Friction vs Structured)

| Scope Class | Execution Route | Justification |
|---|---|---|
| **Bounded Domain Task** (single runtime/script/doc) | Inline + `update_steps` + Domain Skill | Zero artifact or ticket overhead. |
| **Multi-Service or High-Risk Architecture** ($\ge 2$ runtimes, migrations, constitutional rules) | `meta-plan` + `/var/www/artifacts/plans/` + explicit `Go` | Aligns contracts and trade-offs before mutation. |
| **Explicit User Linear Request / Autonomous 24/7 (`hermes`/`paperclip`)** | Add optional `linear-cli` issues (`BAI-*`) | Persists asynchronous backlog state when requested. |

---

## 2. Tracking & Plan Lifecycle

1. **Primary Tracking**: Use `update_steps` for live checklist progress in `agy 1.5.16` and `engram:mem_save` for durable cross-session decisions.
2. **Draft & Master Plan**: Keep multi-service drafts in `/var/www/artifacts/plans/<PROJECT_NAME>/draft_<slug>.md` and present the approved F4 plan in `<slug>.md` (with `project: <PROJECT_NAME>` YAML frontmatter) with executable verification criteria before mutating.
3. **Optional Linear Discipline**: Only create/update `BAI-*` issues via `linear-cli` when explicitly requested by the user or driven by `hermes`/`paperclip`. When used, decompose per runtime boundary rather than monolithic tickets.
4. **Immediate SSoT Mutation**: When requirements change, update the active plan file and `mem_save` immediately without conversational filler.
5. **Clean Archive**: After scoped verification passes (`exit 0`), move executed plans to `/var/www/artifacts/plans/archive/<slug>.executed.md`.

---

## 3. Systemic Root Cause Triage (`systemic-issue-triage`)

1. **Map the Mechanism**: Trace recurring defects to their structural root rather than patching symptoms.
2. **Deletion-Driven Fixes**: Prefer removing dead code, redundant shims, or duplicate rules over adding defensive layers.
3. **Scoped Verification**: Run only the tests/validators matching the modified scope (`exit 0`).
