---
name: orchesbrand
description: "Trigger: orchesbrand, orquestar branding, pipeline de marca, identidad visual, suite de branding, live sync. Orquesta el pipeline integral de marca desde Oraculo/Diagnostico hasta el Brandbook."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.2"
---

# Orchesbrand — Orquestador Multimarca / Multi-Vertical Agnóstico (v3.2)

## Activation Contract
Activar para orquestar `chroma`, `fontgen`, `previews` y `brandbook` bajo un cliente sombrilla (`astrobranding_<brand>.md` + `client_dumps_15_shards.json` + `brandbook.json` madre) generando identidades diferenciadas y aisladas por vertical en `dev/workspaces/<vertical>/brand/`.

## Input Rule (Un Brandbook Madre → N Verticales Aisladas)
- **Autodescubrimiento SSoT:** Localiza `client_dumps_15_shards.json`, `astrobranding_<brand>.md` y `<project_dir>/verticals/<vertical>.json`.
- **Aislamiento de Verticales:** Nunca sobreescribe el `brandbook.json` madre ni mezcla archivos entre `workspaces/<a>/` y `workspaces/<b>/`. Cada vertical recibe su propio `vertical_context`, su `vertical_archetype` cromático y su `style_profile` tipográfico.
- **CLI Canónico (v3.2):** `orchesbrand --brand <BRAND> --vertical <slug> --project-dir /var/www/localstorage/<Project>/dev --phases chroma,fontgen,previews,brandbook --include-shortlist --audit [--sort hybrid] [--seed N]`.

## Hard Rules (Directivas Obligatorias)
1. **Cero Perfiles Hardcodeados y Cero Carpetas Fantasmas:** Todo artefacto va a `--output-dir` o `workspaces/<vertical>/brand/`.
2. **Motor Cromático (`chroma-engine v4.1`):** 3 mundos OKLCH diferenciados por `vertical_archetype`, WCAG AAA ($\ge 7:1$ texto, $\ge 4.5:1$ botón) y APCA ($L_c \ge 75$).
3. **Motor Tipográfico Vanguardia (`fontgen-engine v4.1` + `envato-font-preview v3.2`):** Dual-sort `elements.envato.com` (`sort-by-latest` + `sort-by-popular`), cero `Fraunces`/caligrafía nupcial en B2B, shortlist de alternativas y galería SVG multipaleta con reintentos ante 502.
4. **Merge No Destructivo de `brandbook.json`:** Hereda `brand_architecture` del sombrilla si falta en el workspace, actualiza `design_system`, inyecta `vertical_context` y corrige fallbacks CSS (`sans-serif`/`serif`) en `brandbook-theme.css`.
5. **Auditoría Física Obligatoria (`--audit`):** Valida JSON Schema, contraste y 3 ecosistemas antes de Exit 0.

## References
- [`references/pipeline.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/pipeline.md) — Topología del pipeline.
- [`references/usage.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/usage.md) — Manual CLI.
- [`references/infra.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/infra.md) — Persistencia SSoT y Brandview.
- [`assets/schemas/pipeline_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/pipeline_state.schema.json) — Estado.
- [`assets/schemas/brandview_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/brandview_state.schema.json) — Brandview.
