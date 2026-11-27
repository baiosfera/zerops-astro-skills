---
name: orchesbrand
description: "Trigger: orchesbrand, orquestar branding, pipeline de marca, identidad visual, suite de branding, live sync. Orquesta el pipeline integral de marca desde Oraculo/Diagnostico hasta el Brandbook."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.5"
---

# `orchesbrand` — Orquestador Visual Art-Direction-First & PB19 (v4.5)

## Activation Contract
Activar para orquestar `chroma` (`v8.0`), `fontgen` (`v7.0`), `previews` (`envato-font-preview v5.1`), `DESIGN.md` y `brandbook`, tanto para marcas **sin Oráculo** (ruta agnóstica por defecto mediante `--chroma-spec` / `--font-spec` / `--brand-brief`) como **con Oráculo** mediante opt-in explícito (`--brief <astrobranding_*.md> --shards <15_shards.json>`). Las fases vectoriales (`symbol v2.0`) y de movimiento (`kinetic v2.1`) operan desacopladas sobre los mismos tokens `OKLCH` y piezas SVG reales.

## Input Routes (Agnóstico por Defecto · Oráculo Opt-In)
- **Art Direction First (Por Defecto):** `orchesbrand --brand <BRAND> --vertical <slug> --brand-brief <brand_brief.json> [--chroma-spec <ws>/brand/chroma_spec.json] [--font-spec <ws>/brand/font_spec.json] --output-dir <ws>/brand --audit`
  *(Detecta automáticamente `chroma_spec.json` y `font_spec.json` dentro de `--output-dir` si existen).*
- **Con Oráculo Explícito:** `orchesbrand --brand <Project> --vertical <slug> --project-dir <dev> --brief <astrobranding_*.md> --shards <15_shards.json> --preview-texts "<MARCA>,<SUB>" --audit`

## Hard Rules (Directivas Obligatorias)
1. **Separación Dirección de Arte vs Compilación (`chroma v8.0`):** Diseña `chroma_spec.json` a medida por marca y compila con gamut mapping CSS Color 4, Step-9 oscuro saturado (`on_primary` legible sin lavado pastel), WCAG 2.2 AAA, APCA `0.0.98G-4g` y auditoría acromática `C=0`. Cero plantillas o arquetipos fijos.
2. **Tipografía Curada & Cero Fugas (`fontgen v7.0` + `envato-font-preview v5.1`):** Compila `font_spec.json` o ejes explícitos sin rastreo silencioso en disco (`has_oraculo=False` por defecto), filtra ruido amateur/sci-fi en Envato, emite `astro_web_ready` (sintaxis Context7 `options.variants` y `CLS=0`) y garantiza galería legible SVG+Web.
3. **Merge No Destructivo, Symbol & Kinetic (`v2.0`/`v2.1`):** Actualiza `design_system` (`colors`, `typography`, `dtcg_tokens`, `astro_web_ready`) y `brand_colors` en `brandbook.json` + `brandbook-theme.css` sin pisar `brand_architecture` ni léxico; valida `symbol-engine` (atributos `width`/`height` explícitos), `kinetic-engine` (`1150–1618ms` + loop vivo sutil) y pasa `orchesbrand --test`.

## References
- [`references/pipeline.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/pipeline.md) · [`references/usage.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/usage.md) · [`references/infra.md`](file:///var/www/zerops-astro-skills/orchesbrand/references/infra.md)
- [`assets/schemas/pipeline_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/pipeline_state.schema.json) · [`assets/schemas/brandview_state.schema.json`](file:///var/www/zerops-astro-skills/orchesbrand/assets/schemas/brandview_state.schema.json)
