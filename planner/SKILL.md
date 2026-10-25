---
name: planner
description: "Trigger: planner, plan, master-plan, planificar, crear plan, diseña un plan, /plan, change proposal, version plan, roadmap. Universal Master Planning & SSoT Governance Orchestrator under CoHaLo v8.4 and Supreme Directive v8.5."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "10.1"
---

# Planner — Supremo Gobernador de Orquestación & SSoT (v10.1)

## Activation Contract
Gobernador supremo de arquitectura Zerops-First. Subordina grilling, comanda subagentes delegados y garantiza el arnés determinista bajo [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Tareas atómicas de un solo archivo ejecutan inline sin planes ceremoniales.

## 5 Invariantes Soberanos (Positive Guidance)
1. **Facts-First Grounding & Espera Epistémica F0**: Iniciar con inspección en disco o subagente `research`. Si se lanzan subagentes, aguardar sus reportes antes de concluir, redactar planes o grilling. Cero preguntas si la evidencia existe en código o docs (máx 1 pregunta en bifurcaciones reales).
2. **Borradores Aislados & Linear Gate en F4**: En F0–F3 los borradores residen en `draft_<slug>.md` y descubrimientos en Engram (`mem_save`). Prohibido crear proyectos o BAIs en Linear antes de F4. La sincronización Linear se activa únicamente en F4 tras 'Go' explícito al Plan Maestro en `/var/www/artifacts/plans/<slug>_v1.md`.
3. **Desglose Modular Anti-Monolítico**: Dividir epics en BAIs atómicos por subsistema o runtime. Prohibido condensar stacks heterogéneos en un único ticket monolítico.
4. **Thin Orchestrator & Bounded Delegation**: Mantener contexto ligero delegando tareas multi-archivo a subagentes (`invoke_subagent`). El orquestador sintetiza únicamente el resultado verificado.
5. **Behavioral Physical Attestation (Zero-Slop Done)**: Prohibido marcar `Done` sin evidencia física (`bun test`, `pytest`, `skills-suite-validate`). Al cerrar épica, archivar a `archive/<slug>.executed.md` y purgar `.json` residuales.

## Decision Gates

| Capa | Protocolo / Acción | Referencia |
|---|---|---|
| Inflow Epistémico | Inspección en disco $\to$ `research` 360 | [`research`](file:///var/www/zerops-astro-skills/research/SKILL.md) |
| Aclaración Restringida | Facts-first; máx 1 pregunta con opciones | [`references/usage.md`](file:///var/www/zerops-astro-skills/planner/references/usage.md) |
| Plan & Agrupación | Delegar a `meta-plan` o `linear-cli` | [`meta-plan`](file:///var/www/.agents/skills/meta-plan/SKILL.md) |
| Infraestructura & SSoT | Ciclo de vida `/artifacts/plans/`, cerrojos Linear | [`references/infra.md`](file:///var/www/zerops-astro-skills/planner/references/infra.md) |
| Sensores Físicos | Tests exit code 0 $\to$ `linear-cli update-status` | [`skills-suite-validate`](file:///usr/local/bin/skills-suite-validate) |
| Cierre SSoT | `mem_save` / `mem_session_summary` | [`engram`](file:///var/www/zerops-astro-skills/planner/references/usage.md) |

## Workflows Ejecutivos (F0–F5)
1. **F0 (Inflow)**: Inspección silenciosa con subagente `research` o disco. Aguardar reportes antes de avanzar.
2. **F1 (Clarification Gate)**: Grilling con `draft_<slug>.md` solo si falta evidencia física.
3. **F2 (Dual-RAG Alignment)**: Consultar especificaciones en `references/usage.md`.
4. **F3 (Validation Feedforward)**: Chequeo de sintaxis física (`bash -n`, `py_compile`).
5. **F4 (Plan & Approval)**: Plan maestro en `/artifacts/plans/`, alta de proyecto/BAIs en Linear y solicitud de Go.
6. **F5 (Execution & Fast Attestation)**: Delegación, tests físicos, update-status Done y persistencia Engram.

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/planner/references/usage.md) · [`references/infra.md`](file:///var/www/zerops-astro-skills/planner/references/infra.md) · [`references/planning_heuristics.md`](file:///var/www/zerops-astro-skills/planner/references/planning_heuristics.md)
