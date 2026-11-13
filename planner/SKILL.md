---
name: planner
description: "Trigger: planner, plan, master-plan, planificar, crear plan, diseña un plan, /plan, change proposal, version plan, roadmap. Linear Planning & SSoT Execution Router subordinate to meta-plan and Supreme Directive v9.1."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "11.0"
---

# Planner — Orquestador de Planes, Linear & Cierre Real (v11.0)

## Activation Contract
Subordinado directo de [`meta-plan`](file:///var/www/.agents/skills/meta-plan/SKILL.md) y [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Tasks atómicas ejecutan inline sin ceremonias. Iniciativas multi-servicio ($\ge 2$ runtimes o $\ge 3$ pasos) usan F0–F5 con `/var/www/artifacts/plans/` y Linear.

## Invariantes Soberanos (Positive Guidance)
1. **Facts-First & Anti-Grilling**: Inspeccionar disco vivo y fuentes primarias (`research`) antes de preguntar. Reservar F1 para 1 bifurcación real con tradeoffs a la vez.
2. **F4 Audit & Go Gate (Zero Premature Execution)**: En F4 publicar el plan en `/var/www/artifacts/plans/<slug>.md` con criterios ejecutables de cierre y esperar `Go` explícito antes de ejecutar código o crear/cerrar épicas `BAI-*` en Linear.
3. **Linear Scoping & Auto-Archive**: Agrupar cada `BAI-*` bajo su proyecto (`linear-cli create ... --project <ID|name>`). Al completar F5 con evidencia real, mover el plan a `artifacts/plans/archive/<slug>.executed.md` y guardar síntesis en `mem_save`.
4. **Honest Reality Proof (Zero Checklist-Theater)**: Validar el alcance exacto modificado con comandos ejecutables (`bun test`, `pytest`, `go build`, `zcli`/Zerops smoke). Reportar por separado `BEHAVIORALLY_VERIFIED`, `SYNTAX_ONLY` y `UNVERIFIED` antes de marcar `Done`.
5. **Catálogo Modular & Repos Plantilla `baiosfera/*`**: [`zerops-astrobranding`](file:///var/www/zerops-astrobranding/iniciar.sh) gobierna recetas, blueprints, templates y scripts compartidos; el código fuente de cada runtime vive en su repo plantilla `baiosfera/runtime-*` + `template-astro-web`, interconectados vía DNS interno (`zerops_discover`).

## Decision Gates

| Capa | Protocolo / Acción | Referencia |
|---|---|---|
| Orquestador Padre | Umbral proporcional y tabla meta-suites | [`meta-plan`](file:///var/www/.agents/skills/meta-plan/SKILL.md) |
| Epistémico F0 | Inspección viva + subagente `research` | [`research`](file:///var/www/.agents/skills/research/SKILL.md) |
| Linear CLI | `create-project`, `create --project`, `comment`, `update-status` | [`linear-cli`](file:///var/www/.bin/linear-cli) |
| Sensores Reales | Tests reales + `skills-suite-validate` + `ssot-parity-check` | [`skills-suite-validate`](file:///var/www/.bin/skills-suite-validate) |
| Detalles Operativos | Heurísticas y contratos SSoT Git-first | [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) |
