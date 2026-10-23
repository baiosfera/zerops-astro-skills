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
1. **Facts-First Grounding & Anti-Grilling**: Iniciar siempre con inspección en disco o subagente `research` para verificar hechos de entorno o web antes de planificar. Cero preguntas si la evidencia existe en código o docs. Reservar preguntas exclusivamente para bifurcaciones arquitectónicas reales (máx 1 pregunta atómica a la vez).
2. **Linear Invariable Grouping & Explicit Criteria**: Todo issue `BAI-*` nace estrictamente dentro de un Proyecto padre (`linear-cli create ... --project <ID>`) con criterios de aceptación verificables y alcance explícito. Hallazgos y decisiones se registran como comentario del issue (`linear-cli comment <ID> "..."`) antes de responder al usuario.
3. **Thin Orchestrator & Bounded Delegation**: Mantener contexto ligero delegando tareas multi-archivo ($\ge 2$ archivos) a subagentes temporales (`invoke_subagent`). El orquestador sintetiza únicamente el resultado verificado.
4. **Behavioral Physical Attestation (Zero-Slop Done)**: Prohibido marcar `Done` sin evidencia física de comportamiento que ejercite el cambio (`bun test`, `pytest`, o sensor específico del contrato modificado, no meros validadores genéricos).
5. **Arquitectura Lego Desacoplada (Plantilla v4 & Zerops)**: Chasis inmutable en `/var/www/zerops-astrobranding`. Servicios interconectados vía DNS privado (`http://<servicio>:<puerto>`), con staging efímero.

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
