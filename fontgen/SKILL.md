---
name: fontgen
description: "Trigger: fontgen, tipografia, fuentes, matriz tipografica, design tokens de fuentes, emparejamiento tipografico, 3 ecosistemas. Genera la direccion de arte y 3 ecosistemas tipograficos hibridos (Envato + Google Fonts) con 6 capas funcionales."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.1"
---

# Fontgen — Art Direction Tipográfica, Live Envato Previews & 6 Capas Gestalt (v3.1)

## Activation Contract
Activar para diseñar la matriz tipográfica mediante `fontgen-engine` (`3` ecosistemas híbridos Envato Elements + Google Fonts Variable v2 en `6` capas funcionales + `web_ready_bridge` para Astro 5 `experimental.fonts`) y previsualizar las fuentes Envato como SVGs reales con `envato-font-preview` mientras el usuario decide cuáles descargar en `.woff2`.

## Input & Output Isolation
- **CLI Canónico:** `fontgen-engine --brand <BRAND> --brief <astrobranding_<brand>.md> --output-dir <workspace>/brand`.
- **Galería SVG Previa a `.woff2`:** `envato-font-preview --from-manifest <workspace>/brand/font_manifest.json --chroma <workspace>/brand/chroma_manifest.json --texts "MARCA,SUBTITULO" --out <workspace>/brand/previews`.
- **Aislamiento Estricto:** Con `--output-dir`, escribe únicamente en ese directorio. Nunca crea carpetas globales fantasmas.

## Hard Rules (Directivas Obligatorias)
1. **3 Ecosistemas Diferenciados sin Repetición:** Display y Acento desde Envato (`https://app.envato.com/fonts/{uuid}` con `item_uuid` verificado como previsualizable en SVG) + Body/UI en Google Fonts v2 Variable con calibración anti-CLS (`size-adjust`, `ascent-override`, `descent-override`).
2. **Parsing Bilingüe Real (ES/EN):** Lee signos zodiacales, Medio Cielo, Day Master y Nakshatra en español o inglés directamente desde `astrobranding_<brand>.md` o los 15 shards; nunca usa valores estáticos falsos.
3. **Herencia de 6 Capas & Puente Web Astro 5:** Define `logo`, `slogan`, `h1`, `h2`, `body`, `ui` más `web_ready_bridge` (`fontProviders.google()` inmediato + `envato_upgrade_targets` para `fontProviders.local()` al subir `.woff2`).
4. **Previsualización Instantánea SVG:** Todo token Envato emitido incluye `item_uuid` y `url`, permitiendo generar `<svg>` reales y `preview_gallery.html` interactivo sin login ni descarga previa.
5. **Paridad & Auto-Test:** `scripts/fontgen_engine.py` debe mantenerse 100% idéntico al SSoT del catálogo y pasar `fontgen-engine --test`.

## References
- `references/usage.md` — Manual Gestalt, Envato live sourcing, `envato-font-preview` y anti-CLS.
- `assets/schemas/font_manifest.schema.json` — Esquema JSON Draft 2020-12.
