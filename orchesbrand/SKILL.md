---
name: orchesbrand
description: "Trigger: orchesbrand, orquestar branding, pipeline de marca, identidad visual, suite de branding, live sync. Orquesta el pipeline integral de marca desde Oraculo/Diagnostico hasta el Brandbook."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.1"
---

# Orchesbrand — Orquestador Visual Multimarca (v4.1)

## Activation Contract
Activar para orquestar `chroma`, `fontgen`, `previews` Full-Color (`envato-font-preview v4.1`) y `brandbook` tanto para clientes con Oráculo (`brand_slug` en `ecosystem.json` $\to$ `client_dumps_15_shards.json`) como sin carta natal (`--brand-brief` + `--palette-json` / `--seed-hex` + `--envato-urls`).

## Input Rule (Dual Intake & Multimarca Disjunto)
- **Con Oráculo:** `orchesbrand --brand <Project> --vertical <slug> --project-dir /mnt/localstorage/<Project>/dev [--palette-json <palettes.json>] --preview-texts "<MARCA>,<MÉTODO>" --audit`. Resuelve automáticamente `brand_slug` desde `ecosystem.json`, excluye fuentes hermanas vía `--sibling-workspaces-dir` y aísla en `workspaces/<vertical>/brand/`.
- **Sin Oráculo (Art Direction First):** `orchesbrand --brand <BRAND> --vertical <slug> --brand-brief <brand_brief.json> --palette-json <palettes.json> --envato-urls "<url1>,<url2>" --output-dir <ws>/brand --audit`.

## Hard Rules (Directivas Obligatorias)
1. **Cero Perfiles Hardcodeados y Cero Carpetas Fantasmas:** Escribe únicamente en `--output-dir` o `workspaces/<vertical>/brand/`.
2. **Exclusión Multimarca Real:** Nunca duplica fuentes Envato/Google ni expone nombres internos de proyecto en `--preview-texts` de una rama.
3. **Motor Cromático (`chroma-engine v5.1`):** Preserva hexes vibrantes curados, calcula `on_primary` / `on_accent` ($\ge 4.5:1$), rota matices entre ramas hermanas y audita WCAG AAA ($\ge 7:1$ texto).
4. **Galería Full-Color (`envato-font-preview v4.1`):** Deduplica por UUID canónico, aísla IDs SVG y ofrece pestañas + selector de paleta + fallback estático probado en Chrome headless.
5. **Merge No Destructivo & Auditoría Física (`--audit`):** Fusiona `design_system` en `brandbook.json` + `brandbook-theme.css` y valida JSON/contraste antes de Exit 0.

## References
- [`references/pipeline.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/pipeline.md) — Topología del pipeline.
- [`references/usage.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/usage.md) — Manual CLI.
- [`references/infra.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/infra.md) — Persistencia SSoT y Brandview.
- [`assets/schemas/pipeline_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/pipeline_state.schema.json) — Estado.
- [`assets/schemas/brandview_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/brandview_state.schema.json) — Brandview.
