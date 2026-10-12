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
- **2. Interoperabilidad W3C DTCG (`brandbook_superfull_[MARCA].json`):**
  - Todo token incluye `$type` (`color`, `fontFamily`, `duration`, `cubicBezier`, `dimension`), `$value` y `$description`.
  - Ramas limpias: `brand_architecture`, `ethical_pillars_and_anti_bias`, `design_system`, `voice_tone_and_messaging`, `target_audience`, `llm_system_prompt_engine`.
  - Extensiones `$extensions.tailwind_v4` y `$extensions.css_variables` para generación frontend downstream.
- **3. Ejecutor Autónomo Dual-Track (`brandbook_pipeline_runner.py`):**
  - Ingesta shards Silver (~22 KB) y feeds Gold sin recorrer caché cruda (budget < 8k tokens).
  - Invoca Bifrost Gateway (`http://bifrost:8080/v1/chat/completions`) con `x-tier: production`, `temperature: 0.2` y `json_object`.
  - Deriva en paralelo `brandbook-theme.css` (`@theme` block para Tailwind CSS v4) y `system_prompt.md`.
- **4. Salida Determinista SSoT & Espejo Runtime Local Storage:** Escribir y sincronizar en:
  - **Runtime Zerops (Local Storage):** `/var/www/localstorage/[MARCA]/dev/` (`brandbook_superfull_[MARCA].json`, `brandbook-theme.css`, `system_prompt.md`).
  - **Drive SSoT:** `/var/www/baiosfera/PROYECTOS/[MARCA]/dev/` y `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/`.

## Output Contract
- `/var/www/localstorage/[MARCA]/dev/brandbook_superfull_[MARCA].json` (W3C DTCG 2025.10)
- `/var/www/localstorage/[MARCA]/dev/brandbook-theme.css` (Tailwind CSS v4 `@theme`)
- `/var/www/localstorage/[MARCA]/dev/system_prompt.md` (Conversational projection)
- `/var/www/baiosfera/PROYECTOS/[MARCA]/dev/brandbook_superfull_[MARCA].json` (Drive SSoT mirror)
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/brandbook.json` (Paridad retrocompatible)

## References
- `references/usage.md` — Especificación W3C DTCG, desacople SSoT, consumo downstream y pipeline de exportación gráfica.
- `scripts/brandbook_pipeline_runner.py` — Ejecutor Fast-Track CLI con Bifrost Gateway.
