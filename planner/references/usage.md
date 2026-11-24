# Planner Reference Manual: Proportional Planning & Git-First Governance (v12.0)

> **Parent Meta-Skill:** [`meta-plan`](file:///var/www/.agents/skills/meta-plan/SKILL.md)  
> **Standard:** Supreme Directive v10.0 & Zero Checklist-Theater

---

## 1. Mission: Proportional Planning & Honest Closure

`planner` structures multi-service ($\ge 2$ runtimes) or high-risk architectural changes under [`meta-plan`](file:///var/www/.agents/skills/meta-plan/SKILL.md) while keeping bounded tasks friction-free via `update_steps`.

1. **Facts-First & Anti-Grilling**: Inspect disk and live primary sources before asking. Ask at most 1 focused question with trade-offs when a real product fork exists.
2. **Plan & Go Gate**: Keep F0–F3 drafts in `/var/www/artifacts/plans/${PROJECT_NAME}/draft_<slug>.md`. Publish the F4 plan in `/var/www/artifacts/plans/${PROJECT_NAME}/<slug>.md` (`project: ${PROJECT_NAME}`) with executable checks and wait for explicit `Go`.
3. **Optional Linear (`BAI-*`)**: Interactive `agy 1.5.16` sessions use `update_steps` + `Engram` by default. Invoke `linear-cli` (`set-project`, `create`, `update-status --evidence`) **only** when the user explicitly asks for Linear or in unattended `hermes`/`paperclip` runs.
4. **Scoped Reality Proof**:
   - Report `BEHAVIORALLY_VERIFIED`, `SYNTAX_ONLY`, and `UNVERIFIED` separately.
   - Archive executed plans to `/var/www/artifacts/plans/archive/<slug>.executed.md` and persist learnings in `mem_save`.
5. **Modular `baiosfera/*` Topology**:
   - `/var/www/zerops-astrobranding`: Catalog & Registry (`recipes/`, `blueprints/`, `templates/`, `scripts/`, `iniciar.sh`).
   - `/var/www/zerops-astro-skills`: Sovereign Skills Suite (`baiosfera/zerops-astro-skills`).
   - `baiosfera/runtime-*` + `template-astro-web`: Deployable runtime template repos discovered via `zerops_discover`.

---

## 2. Git-First Operational Tracks

- **Track A (Skills, Scripts & Governance)**: Changes in `zerops-astro-skills/`, `zerops-astrobranding/scripts/`, `.agents/rules/`, `AGENTS.md`. Verify with scoped checks (`tool-guard.py --test`, `skills-suite-validate`, `ssot-parity-check`) and `git push origin main`.
- **Track B (Runtimes & `baiosfera/*` Templates)**: Changes in `runtime-*` / `template-astro-web` / client apps. Verify inside container via `zcp run {hostname} <test>`, `zerops_deploy`, and HTTP probes.
- **Track C (Content / Business Drive)**: Docs in `/var/www/baiosfera/PROYECTOS/<Brand>/`. Verify links, schemas, and `mem_save`.
