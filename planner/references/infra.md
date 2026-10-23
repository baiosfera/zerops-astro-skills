# Planner: Infraestructura de Planificación, SSoT y Ciclo de Vida de Artefactos (v2.0)

Este documento define la infraestructura de persistencia, integración con Linear y ciclo de vida de los planes maestros bajo Fractal CoHaLo v8.4.

---

## 1. Topología de Directorios y Persistencia Indivisible

Los artefactos de planificación residen en una jerarquía física con enlace directo a Google Drive:

- **Planes Activos (SSoT en disco):**
  `/var/www/artifacts/plans/<slug>_v1.md`
  - Solo debe albergar el plan activo en ejecución actual.
  - Se vincula directamente al proyecto o épica en Linear.

- **Historial de Planes Ejecutados (Archivo Histórico):**
  `/var/www/artifacts/archive/<slug>.executed.md`
  - Al completar la fase de ejecución (F5) y marcar la épica como `Done` en Linear, el plan se mueve a este directorio para evitar contaminación de contexto.

- **Espejo SSoT Indivisible:**
  `/var/www/baiosfera/PROYECTOS/${PROJECT_NAME}/plans/`

---

## 2. Integración con Linear CLI y Cerrojo Físico

El arnés de procesos (`tool-guard.py`) supervisa la interacción con Linear:

- **Registro de Actividad:**
  Cada mutación de estado o comentario ejecutado mediante `linear-cli` actualiza atómicamente `/tmp/.linear_activity_state.json` y `/var/www/artifacts/.linear_activity_state.json`.
- **Pre-Tool Lock:**
  Si existe un plan activo en `/var/www/artifacts/plans/`, las mutaciones sobre código o skills requieren haber registrado actividad reciente en Linear (< 2h).
- **Stop Hook:**
  El agente no puede cerrar su turno en chat habiendo realizado inspecciones o descubrimientos sin antes persistirlos en Linear vía `linear-cli comment <ID>`.

---

## 3. Integración con Meta-Plan

Para planificación estratégica de alta fidelidad, desglose de épicas complejas ($\ge 3$ pasos o multi-servicio) y gobernanza de issues, Planner delega directamente a [`meta-plan`](file:///var/www/.agents/skills/meta-plan/SKILL.md).
