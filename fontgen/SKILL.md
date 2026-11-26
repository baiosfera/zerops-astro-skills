---
name: fontgen
description: "Trigger: fontgen, tipografia, fuentes, matriz tipografica, design tokens de fuentes, emparejamiento tipografico, 3 ecosistemas. Genera la direccion de arte y 3 ecosistemas tipograficos hibridos (Envato + Google Fonts) con 6 capas funcionales."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.2"
---

# Fontgen — Vanguard Dual-Sort Envato, Sibling-Disjoint & Live Previews (v4.2)

## Activation Contract
Activar para diseñar la matriz tipográfica con `fontgen-engine` (`v4.2`) combinando Oráculo 15-shards, `verticals/<v>.json`, exclusión automática de fuentes hermanas (`--sibling-workspaces-dir`), catálogo anti-slop de **20 fuentes Google Fonts variables**, búsqueda **dual-sort** en `elements.envato.com` (`sort-by-latest` + `sort-by-popular`) y galería SVG deduplicada (`envato-font-preview v4.1`).

## Input & Output Isolation
- **CLI Canónico:** `fontgen-engine --brand <BRAND> --shards <shards.json> --vertical-json <vertical.json> --brief <astrobranding_<brand>.md> --sibling-workspaces-dir <dev>/workspaces --output-dir <ws>/brand --sort hybrid [--seed N]`.
- **Galería SVG:** `envato-font-preview --from-manifest <ws>/brand/font_manifest.json --chroma <ws>/brand/chroma_manifest.json --texts "MARCA,SUBTITULO" [--include-shortlist] --out <ws>/brand/previews`.
- **Aislamiento Estricto:** Con `--output-dir`, escribe únicamente ahí (`font_manifest.json`, `fontgen_<vertical>.md`). Nunca crea carpetas fantasmas.

## Hard Rules (Directivas Obligatorias)
1. **Disciplina Tipográfica y Cero Duplicados Hermanos:** Prohibido usar `Fraunces`, `Instrument Serif` o `Inter`. Rota consultas Envato y pool de 20 Google Fonts por `vertical_slug` y excluye automáticamente Envato + Google Fonts usadas en ramas hermanas.
2. **Búsqueda Vanguardista Real (`sort-by-latest` + `sort-by-popular`):** Puntúa novedad (`isNew`) y oficio (`inktrap`, `grotesk`, `neo`, `variable`, `mono`, `editorial`), filtra clichés, verifica `<svg` vivo y emite `shortlist_candidates`.
3. **Galería Interactiva (`envato-font-preview v4.1`):** Deduplica por UUID, aísla IDs SVG, valida cambios de vista en Chrome headless e incluye botón `"Probar Tildes ES"`.
4. **Puente Astro 5 & Paridad:** Emite `web_ready_bridge` libre de `Fraunces`; `scripts/fontgen_engine.py` debe mantenerse byte-idéntico al repo catálogo y pasar `fontgen-engine --test`.

## References
- `references/usage.md` — Manual Gestalt, Dual-Sort Envato y `envato-font-preview`.
- `assets/schemas/font_manifest.schema.json` — Esquema JSON Draft 2020-12.
