---
name: orchesbrand
description: "Trigger: orchesbrand, orquestar branding, pipeline de marca, identidad visual, suite de branding, live sync. Orquesta el pipeline integral de marca desde Oraculo/Diagnostico hasta el Brandbook."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.0"
---

# Orchesbrand — Orquestador Agnóstico de Identidad Visual (v3.0)

## Activation Contract
Activar para orquestar el pipeline de branding (`chroma`, `fontgen`, `previews`, `brandbook`) sobre la SSoT `astrobranding_<brand>.md` y `dev/verticals/<vertical>.json`, escribiendo de forma aislada en `dev/workspaces/<vertical>/brand/` sin sobrescribir arquitectura de marca ni crear carpetas globales fantasmas.

## Input Rule (Desacople SSoT & Aislamiento de Workspace)
- **Fuente Primaria Indivisible:** Ingiere `astrobranding_<brand>.md` (y opcionalmente `dev/verticals/<vertical>.json`) sin tocar JSONs astronómicos crudos.
- **Marcas Sombrilla & Verticales:** Para cualquier `<vertical>` bajo un proyecto sombrilla, `<project_dir>/astrobranding_<brand>.md` rige la identidad junto con `dev/verticals/<vertical>.json`.
- **CLI Canónico (v3.0):** `orchesbrand --brand <BRAND> --vertical <slug> --project-dir /var/www/localstorage/<Project>/dev --phases chroma,fontgen,previews,brandbook --audit`.

## Hard Rules (Directivas Obligatorias)
1. **Cero Perfiles Hardcodeados y Cero Carpetas Fantasmas:** Prohibido inventar cartas natales, colores o fuentes fijas por vertical. Toda salida va estrictamente a `--output-dir` o `workspaces/<vertical>/brand/`.
2. **Motor Cromático Real (`chroma-engine`):** Deriva 3 ecosistemas completos OKLCH (Dark & Light Mode) desde `astrobranding_<brand>.md §3` (o derivación polar matemática), verificando contraste físico WCAG 2.2 AAA ($\ge 7:1$) y APCA ($L_c \ge 75$), más `chroma_preview.html`.
3. **Motor Tipográfico Vivo (`fontgen-engine` + `envato-font-preview`):** Sourcing en vivo desde Envato Elements (`app.envato.com/fonts/{uuid}`) + Google Fonts Variable v2 + puente `web_ready_bridge` (Astro 5 `experimental.fonts`), acompañado de galería SVG interactiva `previews/preview_gallery.html` sin requerir login ni descarga `.woff2` previa.
4. **Merge No Destructivo de `brandbook.json`:** Actualiza únicamente `design_system.colors`, `design_system.typography` y `brandbook-theme.css`, preservando intactas `brand_architecture`, `voice_tone_and_messaging`, `lexicon` y `target_audience`.
5. **Auditoría Física Obligatoria (`--audit`):** Valida JSON Schema, WCAG AAA / APCA real y presencia de los 3 ecosistemas antes de emitir Exit 0.

## References
- [`references/pipeline.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/pipeline.md) — Topología del pipeline desacoplado, dependencias y sincronización.
- [`references/usage.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/usage.md) — Manual CLI y control de estado.
- [`references/infra.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/infra.md) — Infraestructura de persistencia SSoT y conectividad Brandview.
- [`assets/schemas/pipeline_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/pipeline_state.schema.json) — Esquema del estado de orquestación.
- [`assets/schemas/brandview_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/brandview_state.schema.json) — Esquema unificado de Brandview.
