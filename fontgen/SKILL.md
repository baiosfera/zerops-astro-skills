---
name: fontgen
description: "Trigger: fontgen, tipografia, fuentes, matriz tipografica, design tokens de fuentes, emparejamiento tipografico, 3 ecosistemas. Genera la direccion de arte y 3 ecosistemas tipograficos hibridos (Envato + Google Fonts) con 6 capas funcionales."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.2"
---

# Fontgen — Art Direction Tipográfica, 3 Ecosistemas & 6 Capas Gestalt Dual-RAG

## Activation Contract
Activar cuando se requiera diseñar la matriz tipográfica de una marca, generando **3 Ecosistemas Tipográficos Híbridos** (Envato Elements + Google Fonts v2 Variable) estructurados en **6 capas funcionales** con métricas anti-CLS. Opera desacoplado con ingestión directa desde `astrobranding_[MARCA].md` o en modo interactivo.

## Input Rule (Desacople SSoT)
- **Ingestión Directa Primaria:** Ingiere directamente desde `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/astrobranding_[MARCA].md` (compilado por Oráculo en Fase 0) sin dependencias ni bloqueos de fases previas.
- **Modo Standalone / Manual:** Acepta especificaciones directas del usuario o `brand_input.json`.

## Hard Rules (Directivas Obligatorias)
- **1. Generación de 3 Ecosistemas Tipográficos Diferenciados:**
  - Cada ecosistema responde a una interpretación arquetípica única de la marca.
  - Cada ecosistema define sus 6 capas funcionales:
    1. `logo`: Tipografía para monograma / isotipo.
    2. `slogan`: Tipografía con tracking expandido para tagline.
    3. `h1`: Titulares principales hero.
    4. `h2`: Subtítulos y cabeceras de sección.
    5. `body`: Texto de párrafo de ultra-legibilidad (Google Fonts Variable).
    6. `ui`: Botones, badges, controles interactivos y navegación.
- **2. Emparejamiento Gestalt & Jerarquía:**
  - Salto de escala armónica (1.25 mayor / 1.33 cuarta perfecta / 1.618 áurea).
  - Regla de contraste formal: Serif Display con Sans-Serif Body o Neo-Grotesque Display con Humanist Body.
- **3. Prevención Anti-CLS & Código Dev:** Declarar `ascent-override`, `descent-override` y `size-adjust` junto con el código dev `@font-face` y Google Fonts v2 listo para frontend.
- **4. Contrato de Selección:** Incluir `selected_ecosystem_id` (ej: `"eco-1"`).
- **5. Salida Determinista SSoT:** Escribir en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/`:
  - `font_manifest.json` (3 ecosistemas, 6 capas, tokens y selección)
  - `fontgen_[MARCA].md` (ficha técnica, muestras, justificación arquetípica)

## Output Contract
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/font_manifest.json`
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/fontgen_[MARCA].md`

## References
- `references/usage.md` — Manual de emparejamiento Gestalt, fuentes Envato/Google, desacople SSoT y optimización anti-CLS.
- `assets/schemas/font_manifest.schema.json` — Esquema JSON Draft 2020-12.
