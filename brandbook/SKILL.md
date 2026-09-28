---
name: brandbook
description: "Trigger: brandbook, manual de marca, guia de estilos, brand guidelines, showcase de marca, consolidacion de branding, exportacion pdf png svg, dtcg tokens. Compila el Identity Manual Corporativa, tokens W3C DTCG y Showcase interactivo."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.2"
---

# Brandbook — Compilador Maestro W3C DTCG & Motor de Exportación Fidedigno Dual-RAG

## Activation Contract
Activar para compilar la identidad visual consolidada, generando el manifiesto **`brandbook.json`** bajo el estándar **W3C Design Tokens Community Group (DTCG)**, el manual ejecutivo en Markdown (`brandbook_manifest.md`), el showcase interactivo (`index.html`) y los paquetes de exportación multi-formato (SVG, PNG Retina 2x/3x, JPG, PDF). Opera desacoplado con ingestión directa o consolidando manifiestos.

## Input Rule (Desacople SSoT)
- **Ingestión Directa Primaria:** Puede compilar directamente desde `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/astrobranding_[MARCA].md` (compilado por Oráculo en Fase 0) o consolidar los manifiestos disponibles en disco (`font_manifest.json`, `symbol_manifest.json`, `chroma_manifest.json`, `kinetic_manifest.json`). Ninguna fase previa bloquea la compilación; cualquier token o parámetro no definido en manifiestos se extrae directamente del SSoT.
- **Modo Standalone / Manual:** Acepta datos directos del usuario o `brand_input.json`.

## Hard Rules (Directivas Obligatorias)
- **1. Consolidación de Selecciones Definitivas:** Ensamblar las selecciones de marca definitivas:
  - *Tipografía:* Fuentes definitivas de Display, UI, Slogan y Body (`font_manifest.json` o SSoT).
  - *Vectores:* Isologo, Monograma o Favicon en SVG puro (`symbol_manifest.json` o SSoT).
  - *Color:* Ecosistema cromático Dark & Light en OKLCH (`chroma_manifest.json` o SSoT).
  - *Motion & Audio:* Preset de animación 60fps y micro-audio ADSR (`kinetic_manifest.json` o SSoT).
- **2. Interoperabilidad W3C DTCG (`brandbook.json`):**
  - Todo token incluye `$type` (`color`, `fontFamily`, `duration`, `cubicBezier`, `string`), `$value` y `$description`.
  - Ramas limpias: `brand`, `typography`, `color`, `motion`, `sound`, `vectors`, `accessibility`, `extensions`.
  - Extensiones `$extensions.tailwind_v4` y `$extensions.css_variables` para generación frontend downstream.
- **3. Motor de Exportación Fidedigno & Showcase:** Generar `index.html` interactivo descargable y paquetes de exportación (SVG, PNG Retina, JPG, PDF) con renderizado exacto del Isologotipo y paletas reales sin placeholders.
- **4. Salida Determinista SSoT:** Escribir en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/`:
  - `brandbook.json`
  - `brandbook_manifest.md`
  - `index.html`

## Output Contract
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/brandbook.json`
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/brandbook_manifest.md`
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/index.html`

## References
- `references/usage.md` — Especificación W3C DTCG, desacople SSoT, consumo downstream y pipeline de exportación gráfica.
