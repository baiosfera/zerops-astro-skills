# Planning Heuristics & F4 Approval Gate (v12.0)

> **Standard:** Supreme Directive v10.0 · Proportional Activation · Optional Linear

---

## 1. When to Activate `meta-plan` / `planner`
- **Inline Direct (`update_steps`, zero plan file, zero Linear)**: Bounded changes in a single runtime, script, or doc.
- **Full Plan + `Go` Gate (Linear still optional)**: Multi-service initiatives ($\ge 2$ runtimes), constitutional/governance changes, or high-risk migrations.

## 2. F4 Approval Gate (`Audit & Go`)
1. During exploration, keep drafts in `/var/www/artifacts/plans/draft_<slug>.md` or `mem_save`.
2. Present the plan with exact files, risks, and executable checks, then wait for explicit `Go`.
3. After `Go`, execute step-by-step, verify the modified scope, archive the plan to `/var/www/artifacts/plans/archive/<slug>.executed.md`, and run `mem_save`. Only touch Linear if the user requested it.
