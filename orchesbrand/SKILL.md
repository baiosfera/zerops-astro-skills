---
name: orchesbrand
description: "Trigger: orchesbrand, orquestar branding, pipeline de marca, identidad visual, suite de branding, live sync. Orquesta el pipeline integral de marca desde Oraculo/Diagnostico hasta el Brandbook."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.2"
---

# Orchesbrand — Orquestador Visual Multimarca & Visual World (v4.2)

## Activation Contract
Activar para orquestar `chroma`, `fontgen` (`v4.3`), `previews` Full-Color (`envato-font-preview v4.1`), `DESIGN.md` y `brandbook` tanto para clientes con Oráculo (`brand_slug` en `ecosystem.json` → `client_dumps_15_shards.json`) como sin carta natal (`--brand-brief` + `--palette-json` / `--seed-hex` + `--envato-urls`).

## Input Rule (Dual Intake & Multimarca Disjunto)
- **Con Oráculo:** `orchesbrand --brand <Project> --vertical <slug> --project-dir /mnt/localstorage/<Project>/dev [--palette-json <palettes.json>] --preview-texts "<MARCA>,<MÉTODO>" --audit`. Resuelve `brand_slug` desde `ecosystem.json`, excluye fuentes hermanas vía `--sibling-workspaces-dir` y aísla en `workspaces/<vertical>/brand/`.
- **Sin Oráculo (Art Direction First):** `orchesbrand --brand <BRAND> --vertical <slug> --brand-brief <brand_brief.json> --palette-json <palettes.json> --envato-urls "<url1>,<url2>" --output-dir <ws>/brand --audit`.

## Hard Rules (Directivas Obligatorias)
1. **Visual World antes de Tokens (`PB19`):** Exigir `PRODUCT.md` + `impeccable concept-seed` + `DESIGN.md` para asegurar mundos visuales propios entre verticales sin clonar referencias ni caer en plantillas uniformes.
2. **Tipografía Real Sin Fantasmas (`fontgen v4.3`):** Garantizar que `font_manifest.json -> web_ready_bridge.fontsource_packages` resuelva exclusivamente `@fontsource-variable/*` verificadas (cero `Plus Jakarta Sans`, `Space Grotesk`, `Inter`, `Fraunces`, `Instrument Serif`, `DM Sans`, `Outfit`, `Syne`) y marque fuentes Envato como mejora opcional solo si hay `.woff2` locales.
3. **Motor Cromático (`chroma-engine v5.1`) & Geometría Deliberada:** Rotar matices entre ramas hermanas, auditar WCAG AAA ($\ge 7:1$ texto, $\ge 4.5:1$ botón) y declarar radios/elevación coherentes (`12–16px` por defecto; `0px` únicamente cuando el mundo visual lo exija).
4. **Galería Full-Color & Merge SSoT (`--audit`):** `envato-font-preview v4.1` deduplica por UUID y ofrece alternancia de paletas/tildes ES; fusiona `design_system` en `brandbook.json` + `brandbook-theme.css` y pasa `orchesbrand --test`.

## References
- [`references/pipeline.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/pipeline.md) · [`references/usage.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/usage.md) · [`references/infra.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/infra.md)
- [`assets/schemas/pipeline_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/pipeline_state.schema.json) · [`assets/schemas/brandview_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/brandview_state.schema.json)
