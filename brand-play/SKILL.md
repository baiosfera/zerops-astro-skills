---
name: brand-play
description: "Trigger: brand-play, transmutar playbook, hidratar slots, playbook tym, playbook universal, convertir playbook, brand playbook, tym downstream. Sovereign Human-SSoT Copy & Campaign Sync + Linter Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.3"
---

# `brand-play` — Copy & Campaign SSoT Sync Engine (v3.3)

> **División exacta de roles (`brand-studio` vs. `brand-play`):** `brand-studio` (y `ad-campaign-factory` vía `run_workflow`) **crean** posicionamiento, ángulos, copy estratégico y campañas leyendo los 18 Playbooks íntegros (reemplazando al viejo `brand-play transmute`). **`brand-play` (`sync-copy`)** protege y reconcilia tus ediciones manuales en `copy/*.md` y `campaigns/*.json` antes de cada build.

## Activation Contract
Activar al verificar o reconciliar ediciones manuales del usuario en `workspaces/<vertical>/copy/*.md` y `workspaces/<vertical>/campaigns/*.json` contra `web/copy_strings.es.json`, y para auditar ortografía, clichés AI, listas genéricas de audiencia, anclaje semántico y fugas de jerga interna con `anti-slop-linter v2.3`.

## Hard Rules & Positive Guidance
- **Prioridad Absoluta Human SSoT (`copy/*.md` + `campaigns/*.json` > `web/copy_strings.es.json`):** Ejecutar `brand-play sync-copy --workspace <ws_dir> [--check]` antes de compilar `astro-web`. Detecta cambios manuales vía checksum SHA-256 (`NEEDS_RECONCILIATION`) y actualiza `_ssot_policy.source_checksums` + `_ssot_policy.campaign_checksums`.
- **Conceptos Estratégicos Públicos vs. Jerga Backend (`anti-slop-linter v2.3`):** Audita prosa Markdown y valores públicos en `campaigns/*.json` (ignorando claves técnicas de esquema). Bloquea `audience_laundry_list` (5+ roles/áreas enumeradas en una frase), `unanchored_proprietary_term` (términos propios sin disciplina humana previa vía `proprietary_terms_anchors`), jerga interna (`BANT`, `PWYW`, `Order Bump`, `DIY/DWY/DFY`, `Rotación Barista`, `Ads-First`, `Comprador Ideal`, `UPPER_SNAKE_CASE`) y omisiones de tildes/`ñ`.
- **Transmutador `transmute` Deprecado:** Reservado únicamente por compatibilidad legacy; prohibido usarlo como sustituto de `brand-studio` o `ad-campaign-factory`.
- **Certificación Física:** `brand-play test` · `anti-slop-linter --test` · `skills-suite-validate`.

## Commands
```bash
brand-play sync-copy --workspace /mnt/localstorage/<Project>/dev/workspaces/<vertical> --check
anti-slop-linter --brand "<BRAND>" --vertical "<vertical>" --file <copy_file>
```
