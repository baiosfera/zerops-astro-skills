# Planner Reference Manual: Operational Usage & Git-First Governance (v11.0)

> **SSoT Reference Document:** `/var/www/.agents/skills/planner/references/usage.md`  
> **Parent Meta-Skill:** [`meta-plan`](file:///var/www/.agents/skills/meta-plan/SKILL.md)  
> **Standard:** Supreme Directive v9.1 & Zero Checklist-Theater

---

## 1. Misión: Planeación Real & Cierre Honesto

`planner` estructura iniciativas multi-servicio ($\ge 2$ runtimes o $\ge 3$ pasos) bajo [`meta-plan`](file:///var/www/.agents/skills/meta-plan/SKILL.md) sin burocracia innecesaria para tareas simples.

1. **Facts-First & Anti-Grilling**: Inspeccionar disco vivo y fuentes primarias (`research`) antes de preguntar. Si hace falta decisión humana con tradeoffs reales, formular **máximo 1 pregunta atómica a la vez** y esperar respuesta.
2. **F4 Audit & Go Gate**: Mantener borradores F0–F3 en `/var/www/artifacts/plans/draft_<slug>.md`. Publicar el plan maestro en `/var/www/artifacts/plans/<slug>.md` con criterios ejecutables y esperar `Go` explícito antes de ejecutar código o crear/cerrar épicas `BAI-*`.
3. **Agrupación en Linear (`BAI-*`)**: Toda issue creada tras F4 `Go` pertenece a un Proyecto en Linear (`linear-cli set-project "<ID|name>"` / `create-project`).
4. **Honest Reality Proof (Zero Checklist-Theater)**:
   - Distinguir explícitamente `BEHAVIORALLY_VERIFIED` (tests/builds/sondas reales ejecutados en el alcance exacto) de `SYNTAX_ONLY` o `UNVERIFIED`.
   - Marcar Linear `Done` exige `--evidence` con comandos reales ejecutados tras el último cambio y `exit 0`.
5. **Topología Modular (`baiosfera/*` + Catálogo)**:
   - `/var/www/zerops-astrobranding`: **Catálogo & Registry** (`recipes/`, `blueprints/`, `templates/`, `scripts/`, `iniciar.sh`).
   - `/var/www/zerops-astro-skills`: **Suite de Skills** (`baiosfera/zerops-astro-skills`).
   - `baiosfera/runtime-*` + `template-astro-web`: repositorios plantilla por runtime desplegables e interconectados por DNS interno (`zerops_discover`).

---

## 2. Pistas Operativas (Git-First)

- **Track A (Skills, Scripts & Gobernanza)**: Cambios en `zerops-astro-skills/`, `zerops-astrobranding/scripts/`, `.agents/rules/`, `AGENTS.md`. Validación con `tool-guard.py --test`, `skills-suite-validate`, `ssot-parity-check` y `git push origin main`.
- **Track B (Runtimes & Plantillas `baiosfera/*`)**: Cambios en `runtime-*` / `template-astro-web` / apps de cliente. Validación con tests nativos (`bun test`, `pytest`, `go test`), `zerops_deploy` y sondas HTTP reales.
- **Track C (Contenido / Documentación / Drive de Negocio)**: Docs de proyecto en `/var/www/baiosfera/PROYECTOS/<Marca>/`. Verificación de enlaces, esquema JSON y `mem_save`.
