---
name: brand-play
description: "Trigger: brand-play, transmutar playbook, hidratar slots, playbook tym, playbook universal, convertir playbook, brand playbook, tym downstream. Sovereign Human-SSoT Copy & Campaign Sync + Linter Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.4"
---

# `brand-play` — Copy & Campaign SSoT Sync Engine (v3.4)

> **División exacta de roles (`brand-studio` vs. `brand-play`):** `brand-studio` (y `ad-campaign-factory` vía `run_workflow`) **crean** posicionamiento, ángulos, copy estratégico y campañas leyendo los 18 Playbooks íntegros (reemplazando al viejo `brand-play transmute`). **`brand-play` (`sync-copy`)** protege y reconcilia tus ediciones manuales en `copy/*.md` y `campaigns/*.json` antes de cada build.

## Activation Contract
Activar al verificar o reconciliar ediciones manuales del usuario en `workspaces/<vertical>/copy/*.md` y `workspaces/<vertical>/campaigns/*.json` contra `web/copy_strings.es.json`, y para auditar invariantes mecánicos deterministas con `anti-slop-linter v2.4`.

## Hard Rules & Positive Guidance
- **Prioridad Absoluta Human SSoT (`copy/*.md` + `campaigns/*.json` > `web/copy_strings.es.json`):** Ejecutar `brand-play sync-copy --workspace <ws_dir> [--check]` antes de compilar `astro-web`. Detecta cambios manuales vía checksum SHA-256 (`NEEDS_RECONCILIATION`) y actualiza `_ssot_policy.source_checksums` + `_ssot_policy.campaign_checksums`.
- **Guardia Mecánica vs. Criterio Editorial (`anti-slop-linter v2.4`):** Audita prosa Markdown y valores públicos en `campaigns/*.json` enfocándose exclusivamente en invariantes deterministas: clichés AI universales, tildes/`ñ`, tabúes dinámicos del brandbook/vertical, tarifas privadas y jerga interna (`BANT`, `PWYW`, `Order Bump`, `DIY/DWY/DFY`, `Rotación Barista`, `Ads-First`, `Comprador Ideal`, `UPPER_SNAKE_CASE`). El criterio editorial y anclaje semántico viven en `brand-studio` y el Crítico Ciego.
- **Compatibilidad Legacy (`transmute`):** Utiliza `brand-studio` o `ad-campaign-factory` para redactar copy nuevo; `transmute` permanece únicamente por compatibilidad histórica.
- **Certificación Física:** `brand-play test` · `anti-slop-linter --test` · `skills-suite-validate`.

## Commands
```bash
brand-play sync-copy --workspace /mnt/localstorage/<Project>/dev/workspaces/<vertical> --check
anti-slop-linter --brand "<BRAND>" --vertical "<vertical>" --file <copy_file>
```
