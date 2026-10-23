# Docu — Certification, SSoT Harness & Physical Validation Specification (v2.0)

Este documento define los criterios normativos de certificación, el arnés físico de validación y la infraestructura de sincronización SSoT para skills.

---

## 1. Criterios Normativos de Certificación (5 Compuertas)

Toda skill producida o refactorizada por `docu` o `meta-skill` debe superar 5 compuertas físicas:

1. **Frontmatter Canónico**: `name`, `description` con triggers ortogonales sin colisiones, `license`, y `metadata.author`.
2. **Presupuesto de Router**: Conteo estricto $\le 480$ palabras en `SKILL.md` (verificado con `wc -w`).
3. **Completitud Dual-RAG**: Existencia verificada de `references/usage.md` e `references/infra.md`.
4. **Integridad de Enlaces**: Cero enlaces rotos; rutas canónicas absolutas con esquema `file:///var/www/...`.
5. **Cero Mutilación de Código**: Preservación invariable de AST y scripts auxiliares.

---

## 2. Topología de Persistencia y SSoT Indivisible

- **Workspace de Desarrollo:** `/var/www/zerops-astro-skills/<skill>/`
- **Google Drive SSoT:** `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/.agents/skills/<skill>/`
- **Control de Snapshots Preventivos:** `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/bak/skills/`
- **Índice Global:** `/var/www/.atl/skill-registry.md`

---

## 3. Sensores Físicos de Calidad

- **Sensor Universal de Capacidades:** `skills-suite-validate` (127+ skills evaluadas en runtime).
- **Sensor de Paridad Anti-Drift:** `ssot-parity-check` (verificación SHA256 y Git status en Zerops y Drive).
- **Prohibición de Checklist Theater:** Quedan prohibidos scripts cosméticos basados en `grep` o `[ -f ]` superficiales sin verificación de AST o compilación real.
