---
name: orchesbrand
description: "Trigger: orchesbrand, orquestar branding, pipeline de marca, identidad visual, suite de branding, live sync. Orquesta el pipeline integral de marca desde Oraculo/Diagnostico hasta el Brandbook."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.2"
---

# Orchesbrand — Orquestador Visual Flexible (Con o Sin Oráculo · v4.0)

## Activation Contract
Activar para orquestar `chroma`, `fontgen`, `previews` Full-Color (`envato-font-preview v4.0`) y `brandbook` tanto para clientes con Oráculo como para clientes sin carta natal (`--brand-brief` + `--palette-json` / `--seed-hex` + `--envato-urls`).

## Input Rule (Dual Intake & Multimarca)
- **Con Oráculo:** `orchesbrand --brand <BRAND> --vertical <slug> --project-dir /mnt/localstorage/<Project>/dev --phases chroma,fontgen,previews,brandbook --include-shortlist --audit`. Aísla cada vertical bajo `workspaces/<vertical>/brand/` sin tocar hermanas.
- **Sin Oráculo (Art Direction First):** `orchesbrand --brand <BRAND> --vertical <slug> --brand-brief <brand_brief.json> --palette-json <palettes.json> --envato-urls "<url1>,<url2>" --output-dir <ws>/brand --audit`.

## Hard Rules (Directivas Obligatorias)
1. **Cero Perfiles Hardcodeados y Cero Carpetas Fantasmas:** Escribe únicamente en `--output-dir` o `workspaces/<vertical>/brand/`.
2. **Motor Cromático (`chroma-engine v5.0`):** Preserva hexes vibrantes curados, calcula `on_primary` / `on_accent` ($\ge 4.5:1$) y audita WCAG AAA ($\ge 7:1$ texto).
3. **Galería Full-Color (`envato-font-preview v4.0`):** Renderiza 4 lockups reales de marca (`--primary`, `--accent`, tarjeta invertida y Mini Hero + CTA) y soporta `--envato-urls` directas del fundador.
4. **Merge No Destructivo de `brandbook.json`:** Hereda arquitectura padre, fusiona `design_system`, inyecta `--brand-on-primary` y `--brand-on-accent` en `brandbook-theme.css`.
5. **Auditoría Física Obligatoria (`--audit`):** Valida JSON Schema, contraste real y 3 ecosistemas antes de Exit 0.

## References
- [`references/pipeline.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/pipeline.md) — Topología del pipeline.
- [`references/usage.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/usage.md) — Manual CLI.
- [`references/infra.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/infra.md) — Persistencia SSoT y Brandview.
- [`assets/schemas/pipeline_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/pipeline_state.schema.json) — Estado.
- [`assets/schemas/brandview_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/brandview_state.schema.json) — Brandview.
