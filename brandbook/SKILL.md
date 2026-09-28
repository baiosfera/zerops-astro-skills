---
name: brandbook
description: "Trigger: brandbook, manual de marca, guia de estilos, brand guidelines, showcase de marca, consolidacion de branding, exportacion pdf png svg, dtcg tokens. Compila el Identity Manual Corporativa, tokens W3C DTCG y Showcase interactivo."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# Brandbook — Compilador Maestro W3C DTCG & Motor de Exportación Fidedigno Dual-RAG

## Activation Contract
Activar cuando se requiera compilar la identidad visual consolidada, generando el manifiesto interoperable **`brandbook.json`** bajo el estándar **W3C Design Tokens Community Group (DTCG)**, el manual ejecutivo en Markdown (`brandbook_manifest.md`), el showcase interactivo (`index.html`) y los paquetes de exportación multi-formato (SVG, PNG Retina 2x/3x, JPG, PDF).

## Hard Rules (Directivas Obligatorias)
- **1. Consolidación de Selecciones Definitivas ($F1 \rightarrow F4$):** El compilador debe leer y ensamblar exclusivamente las selecciones definitivas del usuario:
  - *Fase 1:* Fuentes definitivas de Display, UI, Slogan y Acento (`definitiveDisplayFont`, `definitiveUiFont`, etc.).
  - *Fase 2:* Vector definitivo (Isologo, Monograma o Favicon en SVG puro seleccionado).
  - *Fase 3:* Ecosistema cromático definitivo seleccionado (Dark & Light Mode en OKLCH).
  - *Fase 4:* Preset de animación y micro-audio seleccionado.
- **2. Interoperabilidad W3C DTCG (`brandbook.json`):**
  - Todo token debe incluir `$type` (`color`, `fontFamily`, `duration`, `cubicBezier`, `string`), `$value` y `$description`.
  - Debe estructurarse sin ambigüedades en ramas limpias: `brand`, `typography`, `color`, `motion`, `sound`, `vectors`, `accessibility`, `extensions`.
  - Debe contener la extensión `$extensions.tailwind_v4` y `$extensions.css_variables` para que cualquier agente downstream (Astro, Next.js, SolidJS) genere el frontend sin alucinaciones.
- **3. Motor de Exportación Fidedigno:**
  - Los archivos generados (SVG, PNG Retina, JPG, PDF) deben renderizar **el Isologotipo exactamente como fue evolucionado** (vector de F2 teñido con colores de F3 y lockup con fuentes de F1).
  - Prohibido generar exports con placeholders, textos por defecto o colores desalineados.
- **4. Salida Determinista SSoT:** Escribir en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/`:
  - `brandbook.json`
  - `brandbook_manifest.md`
  - `index.html`

## Execution Steps
1. Leer los 4 manifiestos previos (`font_manifest.json`, `symbol_manifest.json`, `chroma_manifest.json`, `kinetic_manifest.json`) y extraer las selecciones definitivas.
2. Compilar el árbol W3C DTCG en `brandbook.json`.
3. Redactar el manual corporativo en `brandbook_manifest.md`.
4. Ensamblar el showcase web interactivo `index.html`.
5. Ejecutar la exportación gráfica multi-formato.

## Output Contract
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/brandbook.json`
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/brandbook_manifest.md`
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/index.html`

## References
- `references/usage.md` — Especificación W3C DTCG, consumo downstream por LLMs y pipeline de exportación gráfica.
