---
name: fontgen
description: "Trigger: fontgen, tipografia, fuentes, matriz tipografica, design tokens de fuentes, emparejamiento tipografico, 3 ecosistemas. Genera la direccion de arte y 3 ecosistemas tipograficos hibridos (Envato + Google Fonts) con 6 capas funcionales."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.1"
---

# Fontgen — Vanguard Dual-Sort Envato, Multi-Vertical & Live Previews (v4.1)

## Activation Contract
Activar para diseñar la matriz tipográfica con `fontgen-engine` (`v4.1`) combinando Oráculo 15-shards, `verticals/<v>.json`, reglas de `design-taste-frontend` + `impeccable` y búsqueda **vanguardista dual-sort** en `elements.envato.com` (`sort-by-latest` + `sort-by-popular` vía `INITIAL_HYDRATION_DATA`) + `app.envato.com`, junto con galería SVG multipaleta mediante `envato-font-preview`.

## Input & Output Isolation
- **CLI Canónico:** `fontgen-engine --brand <BRAND> --shards <shards.json> --vertical-json <vertical.json> --brief <astrobranding_<brand>.md> --output-dir <ws>/brand --sort hybrid [--seed N]`.
- **Galería SVG + Shortlist:** `envato-font-preview --from-manifest <ws>/brand/font_manifest.json --chroma <ws>/brand/chroma_manifest.json --texts "MARCA,SUBTITULO" --include-shortlist --out <ws>/brand/previews`.
- **Aislamiento Estricto:** Con `--output-dir`, escribe únicamente ahí (`font_manifest.json`, `fontgen_<vertical>.md`). Nunca crea carpetas fantasmas.

## Hard Rules (Directivas Obligatorias)
1. **Disciplina Tipográfica (`taste-skill` §4.1 + `impeccable`):** Prohibido usar `Fraunces`, `Instrument Serif` o `Inter` como defaults. Diferencia el perfil automáticamente por vertical: `architectural_b2b` (inktrap / neo-grotesk / mono), `cosmic_archetypal` (celestial/editorial moderno o geométrico experimental, nunca scripts de boda), `design_system_atelier` y `editorial_manifesto`.
2. **Búsqueda Vanguardista Real (`sort-by-latest` + `sort-by-popular`):** Extrae hasta 48 ítems por consulta desde `elements.envato.com/fonts/...`, puntúa novedad (`isNew`) y oficios de fundición (`inktrap`, `grotesk`, `neo`, `variable`, `mono`, `editorial`), filtra clichés/novedades (`retro`, `90s`, `western`, `pixel`, `horror`, `wedding`, `calligraphy`), verifica `<svg` vivo y emite 3 `shortlist_candidates` alternativos por rol.
3. **Resiliencia & Tildes ES:** `envato-font-preview` reintenta errores `502`/`503`/`429` (3 intentos) e incluye botón rápido `"Probar Tildes ES"` en `preview_gallery.html`.
4. **Puente Astro 5 & Paridad:** Emite `web_ready_bridge` libre de `Fraunces`; `scripts/fontgen_engine.py` debe mantenerse byte-idéntico al repo catálogo y pasar `fontgen-engine --test`.

## References
- `references/usage.md` — Manual Gestalt, Dual-Sort Envato y `envato-font-preview`.
- `assets/schemas/font_manifest.schema.json` — Esquema JSON Draft 2020-12.
