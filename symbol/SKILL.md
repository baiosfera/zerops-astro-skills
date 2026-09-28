---
name: symbol
description: "Trigger: symbol, isologo, monograma, logo vectorial, geometria sagrada, svg, icono de marca, vectores b/n. Disena y cura isologos, monogramas y vectores SVG puros y monocromaticos."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.2"
---

# Symbol — Motor Vectorial, Sacred Geometry & Monocromía Dual-RAG

## Activation Contract
Activar para diseñar, vectorizar y validar el sistema de Isologos, Monogramas y Favicons SVG de una marca derivándolos del arquetipo rector, la proporción áurea ($\Phi = 1.618$) y la geometría sagrada. Opera desacoplado con ingestión directa desde `astrobranding_[MARCA].md` o en modo interactivo.

## Input Rule (Desacople SSoT)
- **Ingestión Directa Primaria:** Ingiere directamente desde `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/astrobranding_[MARCA].md` (compilado por Oráculo en Fase 0) sin requerir que fases previas se hayan ejecutado o bloqueen el pipeline. Si `font_manifest.json` existe, hereda sus tipografías; de lo contrario toma las directrices del SSoT.
- **Modo Standalone / Manual:** Acepta requerimientos directos del usuario o `brand_input.json`.

## Hard Rules (Directivas Obligatorias)
- **1. Monocromía Estricta (Regla B/N):** Vectores en **estricto blanco y negro puro**. Prohibido incrustar colores (ni verdes, dorados ni hex fijos). Emplear exclusivamente `currentColor`, `var(--vector-stroke, #ffffff)` y `var(--vector-fill, none)` o fondos neutros. El teñido corresponde a `chroma`.
- **2. Generación Triple por Categoría (3 Opciones):**
  - **3 Isologos:** Isologo A (Geometría Áurea / Elipses), Isologo B (Monograma Esculpido), Isologo C (Geometría Simétrica / Octagrama / Flor de la Vida).
  - **3 Monogramas:** Iniciales de marca estilizadas (Entrelazado, Minimalista, Geométrico).
  - **3 Favicons:** Glifos compactos de alta legibilidad a 16px/32px/64px.
- **3. Semántica de IDs para Animación Downstream:** Estructurar nodos `<g>`, `<circle>`, `<ellipse>`, `<path>`, `<polygon>` con IDs semánticos:
  - `#symbol-core`: Núcleo central del símbolo.
  - `#symbol-orbit-1` & `#symbol-orbit-2`: Elementos orbitales / elipses cinéticas.
  - `#symbol-geometry-star`: Polígonos de geometría sagrada / estrellas / sellos.
  - `#symbol-monogram`: Nodos vectoriales de iniciales.
- **4. Pureza Vectorial & Escalabilidad:** SVGs 100% vectoriales, `viewBox` explícito (`512x512` o `256x256`), `vector-effect="non-scaling-stroke"`, sin `<image>` ni scripts. Emite código dev SVG puro.
- **5. Contrato de Selección:** Incluir `selected_vector_id` (ej: `"isologo_a"`).
- **6. Salida Determinista SSoT:** Escribir en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/symbol_manifest.json` validado contra `symbol_manifest.schema.json`.

## Output Contract
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/symbol_manifest.json`

## References
- `references/usage.md` — Guía de geometría sagrada, monocromía estricta, desacople SSoT y exportación.
- `assets/schemas/symbol_manifest.schema.json` — Esquema JSON Draft 2020-12.
- `assets/templates/symbol_manifest_template.json` — Plantilla del manifiesto vectorial monocromático.
