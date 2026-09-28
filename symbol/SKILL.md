---
name: symbol
description: "Trigger: symbol, isologo, monograma, logo vectorial, geometria sagrada, svg, icono de marca, vectores b/n. Disena y cura isologos, monogramas y vectores SVG puros y monocromaticos."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# Symbol — Motor Vectorial, Sacred Geometry & Monocromía Dual-RAG

## Activation Contract
Activar cuando se requiera diseñar, vectorizar y validar el sistema de Isologos, Monogramas y Favicons SVG de una marca derivándolos del arquetipo rector, la proporción áurea ($\Phi = 1.618$) y la geometría sagrada.

## Hard Rules (Directivas Obligatorias)
- **1. Monocromía Estricta en Fase 2 (Regla B/N):** En esta etapa los vectores son **estrictamente monocromáticos** (Blanco y Negro puro). Queda estrictamente prohibido incrustar colores (ni verdes, dorados ni hex fijos). Se debe emplear exclusivamente `currentColor`, `var(--vector-stroke, #ffffff)` y `var(--vector-fill, none)` o fondos neutros. El teñido y la paleta cromática corresponden exclusivamente a la Fase 3 (`chroma`).
- **2. Generación Triple por Categoría (3 Opciones):** Generar obligatoriamente 3 propuestas diferenciadas por cada categoría:
  - **3 Isologos:** Isologo A (Geometría Áurea / Elipses Cinéticas), Isologo B (Monograma Esculpido / Escudo), Isologo C (Geometría Simétrica / Octagrama o Flor de la Vida).
  - **3 Monogramas:** Iniciales de marca estilizadas (Entrelazado, Minimalista Lineal, Geométrico).
  - **3 Favicons / Micro-Badges:** Glifos compactos de alta legibilidad a 16px/32px/64px.
- **3. Semántica de IDs para Animación Downstream (Fase 4):** Todo SVG principal debe estructurar sus nodos `<g>`, `<circle>`, `<ellipse>`, `<path>`, `<polygon>` con IDs semánticos predecibles:
  - `#symbol-core`: Núcleo central del símbolo.
  - `#symbol-orbit-1` & `#symbol-orbit-2`: Elementos orbitales / elipses cinéticas.
  - `#symbol-geometry-star`: Polígonos de geometría sagrada / estrellas / sellos.
  - `#symbol-monogram`: Nodos vectoriales de las iniciales.
- **4. Pureza Vectorial & Escalabilidad:** SVGs 100% vectoriales, `viewBox` explícito (`0 0 512 512` o `0 0 256 256`), `vector-effect="non-scaling-stroke"`, sin bitmaps (`<image>`) ni scripts.
- **5. Contrato de Selección y Herencia:** El manifiesto debe incluir `selected_vector_id` (ej: `"isologo_a"`) para transferir la selección definitiva del usuario a las fases subsiguientes.
- **6. Salida Determinista SSoT:** Escribir en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/symbol_manifest.json` y validar contra `symbol_manifest.schema.json`.

## Decision Gates

| Condición | Acción |
|---|---|
| Arquetipo de Sabio / Gobernante | Generar geometría euclidiana simétrica (Círculos concéntricos, Octagrama, Flor de la Vida) |
| Arquetipo de Mago / Rebelde / Atleta | Incorporar elipses cinéticas dinámicas, espirales áureas o sellos abstractos angulares |
| SVG supera límite de peso | Optimizar trazados `<path>` reduciendo decimales superfluos |

## Execution Steps
1. Leer el arquetipo rector, nombre y slogan desde `font_manifest.json` o diagnóstico de entrada.
2. Modelar matemáticamente las 3 opciones de Isologos, 3 Monogramas y 3 Favicons en **estricto blanco y negro**.
3. Incorporar los IDs semánticos obligatorios en cada nodo vectorial para la posterior fase cinética.
4. Generar parámetros de lockup (`symbolScale`, `symbolX`, `symbolY`, `brandY`, `sloganY`).
5. Emitir `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/symbol_manifest.json` validado con `symbol_manifest.schema.json`.

## Output Contract
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/symbol_manifest.json`

## References
- `references/usage.md` — Guía de geometría sagrada, monocromía estricta y pipelines de exportación Canvas/PDF.
- `assets/schemas/symbol_manifest.schema.json` — Esquema JSON Draft 2020-12.
- `assets/templates/symbol_manifest_template.json` — Plantilla del manifiesto vectorial monocromático.
