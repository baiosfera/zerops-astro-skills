---
name: fontgen
description: "Trigger: fontgen, tipografia, fuentes, matriz tipografica, design tokens de fuentes, emparejamiento tipografico, 3 ecosistemas. Genera la direccion de arte y 3 ecosistemas tipograficos hibridos (Envato + Google Fonts) con 6 capas funcionales."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.0"
---

# Fontgen — Art Direction Tipográfica Anti-Slop, Oráculo 15-Shards & Live Envato Previews (v4.0)

## Activation Contract
Activar para diseñar la matriz tipográfica mediante `fontgen-engine` (`v4.0`) integrando los 15 shards de Oráculo (`client_dumps_15_shards.json`), el brief semiótico, `verticals/<v>.json` y la disciplina tipográfica de `design-taste-frontend` + `impeccable`, junto con previsualización SVG interactiva en vivo con `envato-font-preview`.

## Input & Output Isolation
- **CLI Canónico:** `fontgen-engine --brand <BRAND> --shards <client_dumps_15_shards.json> --vertical-json <vertical.json> --brief <astrobranding_<brand>.md> --output-dir <workspace>/brand [--seed N]`.
- **Galería SVG Interactiva Multipaleta:** `envato-font-preview --from-manifest <ws>/brand/font_manifest.json --chroma <ws>/brand/chroma_manifest.json --texts "MARCA,NOMBRE,ESLOGAN" --out <ws>/brand/previews`.
- **Aislamiento Estricto:** Con `--output-dir`, escribe únicamente en ese directorio. Nunca crea carpetas fantasmas.

## Hard Rules (Directivas Obligatorias)
1. **Disciplina Tipográfica (`taste-skill` §4.1 + `impeccable`):** Prohibido usar `Fraunces`, `Instrument Serif` o `Inter` por defecto. En verticales B2B/consultoría/sistemas/IA (`architectural_b2b`), Eco 1 y Eco 2 priorizan displays **Sans arquitectónicos / neo-grotescos** limpios y Eco 3 ofrece como máximo 1 alternativa serif editorial cortante—**jamás scripts caligráficos nupciales ni fuentes de terror/grafiti**.
2. **Búsqueda Viva Filtrada + `--seed`:** `app.envato.com/search?itemType=fonts` deduplica UUIDs, filtra ruido (`wedding`, `horror`, `calligraphy`, `script`, `lavish`), verifica `<svg` en `elements.envato.com/font-preview.svg` y permite rotar candidatos con `--seed`.
3. **Ingesta Conjunta:** Combina simultáneamente `shard_01..04` (Sol/MC tropical, Fagan-Bradley sideral, Shadbala/Nakshatra védico, Day Master/Mes BaZi) + `astrobranding_<brand>.md` + `verticals/<v>.json`.
4. **Puente Astro 5 Seguro:** `web_ready_bridge` usa familias Google limpias (`Space Grotesk`, `Bricolage Grotesque`, `Plus Jakarta Sans`, `DM Sans`, `Instrument Sans`, `JetBrains Mono`) con `envato_upgrade_targets` para `.woff2` vía `fontProviders.local()`.
5. **Paridad & Auto-Test:** `scripts/fontgen_engine.py` debe mantenerse 100% idéntico al SSoT del catálogo y pasar `fontgen-engine --test`.

## References
- `references/usage.md` — Manual Gestalt, filtrado Envato en vivo y `envato-font-preview`.
- `assets/schemas/font_manifest.schema.json` — Esquema JSON Draft 2020-12.
