---
name: brand-play
description: "Trigger: brand-play, transmutar playbook, hidratar slots, playbook tym, playbook universal, convertir playbook, brand playbook, tym downstream. Sovereign Downstream Playbook Transmutation & Slot Hydration Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# `brand-play` — Copy SSoT Sync & Linter Engine (v3.0)

> **Importante:** Para redactar copy estratégico desde cero leyendo tus 18 Playbooks íntegros sin truncar a 4.000 chars ni usar plantillas `{{SLOT}}`, usa el workflow [`brand-studio`](file:///var/www/zerops-astro-skills/brand-studio/SKILL.md) (`run_workflow`). `brand-play` queda enfocado en **sincronización Human-SSoT (`copy/*.md -> web/copy_strings.es.json`)** y validación `anti-slop-linter`.

## Activation Contract
Activar al verificar o reconciliar ediciones manuales del usuario en `workspaces/<vertical>/copy/*.md` contra `web/copy_strings.es.json`, y para auditar ortografía, clichés AI y fugas de jerga interna con `anti-slop-linter v2.1`.

## Hard Rules & Positive Guidance
- **Prioridad Absoluta Human SSoT (`copy/*.md > JSON`):** Ejecutar `brand-play sync-copy --workspace <ws_dir> [--check]` antes de compilar `astro-web`. Detecta cambios manuales vía checksum SHA-256 (`NEEDS_RECONCILIATION`) y actualiza `_ssot_policy.source_checksums`.
- **Conceptos Estratégicos Públicos vs. Jerga Backend (`anti-slop-linter v2.1`):** Permite términos de categoría declarados públicos en `public_brand_concepts` (ej. `OPB`, `CO1` cuando el brief los educa), mientras prohíbe jerga interna técnica (`BANT`, `PWYW`, `Order Bump`, `Context Vault`, `Break-Even CPA`, `server-side`, `UPPER_SNAKE_CASE`) y omisiones de tildes/`ñ`.
- **Transmutador `transmute` Deprecado:** Reservado únicamente por compatibilidad legacy; prohibido usarlo como sustituto de la Fase 4 de `brand-studio`.
- **Certificación Física:** `brand-play test` · `anti-slop-linter --test` · `skills-suite-validate`.

## Commands
```bash
brand-play sync-copy --workspace /mnt/localstorage/<Project>/dev/workspaces/<vertical> --check
anti-slop-linter --brand "<BRAND>" --vertical "<vertical>" --file <copy_file>
```
