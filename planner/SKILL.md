---
name: planner
description: "Trigger: planner, plan, master-plan, planificar, crear plan, diseña un plan, /plan, change proposal, version plan, roadmap. Universal Master Planning & SSoT Governance Orchestrator under CoHaLo v8.4 and Supreme Directive v8.3."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "10.0"
---

# Planner — Supremo Gobernador de Orquestación & SSoT (v10.0)

## Activation Contract
Gobernador supremo de orquestación y arquitectura Zerops-First. Subordina `grilling`, comanda subagentes delegados y garantiza el arnés físico determinista bajo [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Tareas atómicas de un solo archivo ejecutan inline sin planes ceremoniales.

## 5 Invariantes Soberanos (Positive Guidance)
1. **Facts-First Grounding & Anti-Grilling**: Iniciar siempre con inspección en disco o subagente `research`. Si los datos existen en el repo o la documentación, ejecutar sin preguntas. Reservar preguntas exclusivamente para bifurcaciones arquitectónicas reales con tradeoffs (máximo 1 pregunta atómica a la vez).
2. **Linear Invariable Grouping (Zero-Orphan BAI)**: Todo issue `BAI-*` se crea estrictamente dentro de un Plan/Proyecto padre (`linear-cli create ... --project <ID|name>`). Prohibido generar issues huérfanos. Consolidar estado, decisiones y criterios en la descripción del Issue para economizar tokens en chat.
3. **Thin Orchestrator & Bounded Delegation**: Mantener contexto ligero delegando ediciones multi-archivo ($\ge 2$ archivos) o builds a subagentes temporales acotados (`invoke_subagent`). El orquestador sintetiza únicamente el resultado verificado.
4. **Fast & Cheap Physical Attestation**: Toda tarea se valida con sensores deterministas de bajo costo antes de reportar completitud o marcar Done:
   - Chequeo estático / sintaxis: `bun run build` o `node --check` (exit 0).
   - Tests de comportamiento: `bun test` o `pytest` (exit 0).
   - Sensor funcional / grep: rutas correctas y cero regresiones.
5. **Arquitectura Lego Desacoplada (Plantilla v4 & Zerops)**: Chasis inmutable en `/var/www/zerops-astrobranding`. Construcción según `plantilla-universal-web-zerops-v4.md`. Servicios interconectados vía DNS privado (`http://<servicio>:<puerto>`), con staging efímero.

## Decision Gates

| Capa | Protocolo / Acción | Referencia |
|---|---|---|
| Inflow Epistémico | Inspección en disco $\to$ `research` 360 | [`research`](file:///var/www/.agents/skills/research/SKILL.md) |
| Aclaración Restringida | Facts-first; máx 1 pregunta con opciones | [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) |
| Plan & Agrupación | `linear-cli create-project` / `create --project` | [`linear-cli`](file:///var/www/.bin/linear-cli) |
| Ejecución Delegada | Subagente worker acotado para $\ge 2$ archivos | [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) |
| Sensores Físicos | Tests exit code 0 $\to$ `linear-cli update-status` | [`skills-suite-validate`](file:///usr/local/bin/skills-suite-validate) |
| Cierre SSoT | `mem_save` / `mem_session_summary` | [`engram`](file:///var/www/.agents/skills/planner/references/usage.md) |

## Workflows Ejecutivos (F0–F5)
1. **F0 (Inflow)**: Inspección silenciosa de hechos con subagente `research` o disco local.
2. **F1 (Clarification Gate)**: Preguntar solo si no existe evidencia física en disco.
3. **F2 (Dual-RAG Alignment)**: Consultar especificaciones en `references/usage.md`.
4. **F3 (Validation Feedforward)**: Chequeo de sintaxis física.
5. **F4 (Plan & Approval)**: Enlazar a Proyecto en Linear con criterios verificables.
6. **F5 (Execution & Fast Attestation)**: Delegación a subagente, tests físicos (`bun test` exit 0), actualización a Done y persistencia en Engram.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/planner/references/usage.md) · [`references/planning_heuristics.md`](file:///var/www/.agents/skills/planner/references/planning_heuristics.md)
