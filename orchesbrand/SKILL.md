---
name: orchesbrand
description: "Trigger: orchesbrand, orquestar branding, pipeline de marca, identidad visual, suite de branding, live sync. Orquesta el pipeline integral de marca desde Oraculo/Diagnostico hasta el Brandbook."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.1"
---

# Orchesbrand — Orquestador Agnóstico de Identidad Visual (v3.1)

## Activation Contract
Activar para orquestar el pipeline completo (`chroma`, `fontgen`, `previews`, `brandbook`) ingiriendo conjuntamente `client_dumps_15_shards.json`, `astrobranding_<brand>.md` y `dev/verticals/<vertical>.json`, aplicando reglas anti-slop de `impeccable` y `design-taste-frontend` y aislando toda salida en `dev/workspaces/<vertical>/brand/`.

## Input Rule (Ingesta Multi-Fuente & Aislamiento)
- **Autodescubrimiento SSoT:** Detecta `ASTROLOGÍA/DIAG/<BRAND>/raw/json/dumps/client_dumps_15_shards.json`, `astrobranding_<brand>.md` y `<project_dir>/verticals/<vertical>.json`.
- **CLI Canónico (v3.1):** `orchesbrand --brand <BRAND> --vertical <slug> --project-dir /var/www/localstorage/<Project>/dev --shards <shards.json> --vertical-json <vertical.json> --phases chroma,fontgen,previews,brandbook --audit [--seed N]`.

## Hard Rules (Directivas Obligatorias)
1. **Cero Perfiles Fijos y Cero Carpetas Fantasmas:** Prohibido hardcodear cartas natales, paletas cliché o nombres estáticos. Toda salida va a `--output-dir` o `workspaces/<vertical>/brand/`.
2. **Motor Cromático Multi-Eje (`chroma-engine v4.0`):** Genera 3 mundos cromáticos diferenciados (Porcelana/Cobalto Light-First, Carbón/Señal Dark-First, Basalto/Viridiano Dual), verificando WCAG 2.2 AAA ($\ge 7:1$ texto, $\ge 4.5:1$ botón) y APCA ($L_c \ge 75$), con `chroma_preview.html`.
3. **Motor Tipográfico (`fontgen-engine v4.0` + `envato-font-preview v3.1`):** Sourcing Envato filtrado anti-ruido según perfil vertical (`architectural_b2b` sin `Fraunces` ni scripts nupciales) + galería SVG interactiva conectada a los 3 ecosistemas cromáticos en `previews/preview_gallery.html`.
4. **Merge No Destructivo de `brandbook.json`:** Preserva `brand_architecture`, `voice_tone_and_messaging`, `lexicon` y `target_audience`; actualiza `design_system` y `brandbook-theme.css`.
5. **Auditoría Obligatoria (`--audit`):** Valida JSON Schema, contraste real y 3 ecosistemas antes de Exit 0.

## References
- [`references/pipeline.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/pipeline.md) — Topología del pipeline desacoplado.
- [`references/usage.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/usage.md) — Manual CLI.
- [`references/infra.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/infra.md) — Persistencia SSoT y Brandview.
- [`assets/schemas/pipeline_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/pipeline_state.schema.json) — Estado.
- [`assets/schemas/brandview_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/brandview_state.schema.json) — Brandview.
