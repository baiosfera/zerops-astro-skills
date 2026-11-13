# Planning Heuristics & F4 Approval Gate (v11.0)

> **Standard:** Supreme Directive v9.1 · Proportional Activation · Zero Premature Execution

---

## 1. Cuándo Activar `meta-plan` / `planner`
- **Inline Directo (sin Linear)**: Cambios acotados en un único servicio, script o doc ($\le 2$ pasos reversibles).
- **F0–F5 Completo (`meta-plan` + Linear)**: Iniciativas multi-servicio, cambios constitucionales o migraciones estructurales ($\ge 3$ pasos).

## 2. Compuerta F4 (`Audit & Go`)
1. Durante **F0–F3**, toda investigación y borrador viven en `/var/www/artifacts/plans/draft_<slug>.md` y `mem_save`.
2. En **F4**, presentar el plan al usuario con archivos exactos, riesgos y criterios de verificación real, y **detenerse hasta recibir `Go` explícito**.
3. Recién después del `Go`: promover el plan (`Status: Approved`), crear/actualizar tickets `BAI-*` bajo su proyecto en Linear, ejecutar secuencialmente, verificar en vivo y archivar el plan cerrado en `/var/www/artifacts/plans/archive/<slug>.executed.md`.

## 3. Higiene Post-Ejecución
- Nunca marcar `Done` si faltan builds/tests reales del alcance modificado.
- Actualizar Engram con decisiones duraderas y causas raíz (`mem_save` / `mem_session_summary`).
