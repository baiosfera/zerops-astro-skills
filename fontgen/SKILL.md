---
name: fontgen
description: "Trigger: fontgen, tipografia, fuentes, matriz tipografica, design tokens de fuentes, emparejamiento tipografico, 3 ecosistemas. Genera la direccion de arte y 3 ecosistemas tipograficos hibridos (Envato + Google Fonts) con 6 capas funcionales."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.3"
---

# Fontgen — Verified @fontsource-variable, Dual-Sort Envato & Anti-Slop Engine (v4.3)

## Activation Contract
Activar para diseñar la matriz tipográfica con `fontgen-engine` (`v4.3`) combinando Oráculo 15-shards, `verticals/<v>.json`, exclusión automática de fuentes hermanas (`--sibling-workspaces-dir`), catálogo Google Fonts variable verificado alineado con `impeccable-engine` (`web_ready_bridge.fontsource_packages`), búsqueda dual-sort en Envato Elements y galería SVG (`envato-font-preview v4.1`).

## Input & Output Isolation
- **CLI Canónico:** `fontgen-engine --brand <BRAND> --shards <shards.json> --vertical-json <vertical.json> --brief <astrobranding_<brand>.md> --sibling-workspaces-dir <dev>/workspaces --output-dir <ws>/brand --sort hybrid [--seed N]`.
- **Galería SVG:** `envato-font-preview --from-manifest <ws>/brand/font_manifest.json --chroma <ws>/brand/chroma_manifest.json --texts "MARCA,SUBTITULO" [--include-shortlist] --out <ws>/brand/previews`.
- **Aislamiento Estricto:** Con `--output-dir`, escribe únicamente ahí (`font_manifest.json`, `fontgen_<vertical>.md`). Nunca crea carpetas fantasmas.

## Hard Rules (Directivas Obligatorias)
1. **Alineación `impeccable` y Cero Fuentes Sobreusadas:** Prohíbe seleccionar defaults de plantilla AI (`Inter`, `Fraunces`, `Instrument Serif`, `Plus Jakarta Sans`, `Space Grotesk`, `DM Sans`, `Instrument Sans`, `Outfit`, `Syne`, `Playfair Display`, `Newsreader`, `IBM Plex`). Selecciona display, cuerpo y acento itálico editorial desde familias `@fontsource-variable/*` verificadas y exclusivas entre ramas hermanas.
2. **Inexistencia de Fuentes Fantasma (`optional_upgrade_only_when_woff2_present`):** Las tipografías de Envato se registran como mejora opcional (`envato_upgrade_targets`) y únicamente se declaran en CSS web cuando existan sus archivos `.woff2` locales en `public/fonts/`. El puente web compila directamente desde `web_ready_bridge.fontsource_packages`.
3. **Búsqueda Vanguardista Real (`sort-by-latest` + `sort-by-popular`):** Puntúa novedad y oficio (`inktrap`, `grotesk`, `neo`, `variable`, `mono`, `editorial`), filtra kitsch, verifica `<svg` vivo y emite `shortlist_candidates`.
4. **Galería Interactiva & Paridad:** `envato-font-preview v4.1` deduplica por UUID, aísla IDs SVG y valida cambio de vistas + tildes ES; `scripts/fontgen_engine.py` debe mantenerse byte-idéntico al repo de skills y pasar `fontgen-engine --test`.

## References
- `references/usage.md` — Manual Gestalt, Dual-Sort Envato y `envato-font-preview`.
- `assets/schemas/font_manifest.schema.json` — Esquema JSON Draft 2020-12.
