# Symbol: Manual de Diseño Vectorial, Sacred Geometry & Monocromía SOTA

Este documento formaliza las directrices matemáticas, reglas de pureza vectorial monocromática y especificaciones de exportación client-side para el sistema de Isologos, Monogramas y Favicons.

---

## 1. Principios de Sacred Geometry y Proporción Áurea ($\Phi = 1.618$)

Los símbolos de marca deben construirse sobre retículas matemáticas rigurosas:
- **La Flor de la Vida & Octagrama Sagrado:** Para arquetipos de Gobernanza, Autoridad y Trascendencia (ángulos de 45° y proporciones pitagóricas).
- **La Espiral Áurea & Elipses Cinéticas:** Para arquetipos de Alto Rendimiento, Dinamismo, Creador y Movimiento Anatómico.
- **Monogramas Esculpidos:** Iniciales de marca estilizadas con curvas de Bézier cúbicas fluidas.

---

## 2. Regla de Monocromía Estricta en Fase 2 (Black & White Puro)

Para evaluar la fuerza del diseño, pregnancia y balance espacial sin el sesgo cromático:
1. **Cero Colores Prematuros:** Queda estrictamente prohibido incrustar tonos verdes, dorados, azules o degradados de color en los trazos de Fase 2.
2. **Uso de Variables Neutras:**
   ```xml
   <svg viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" fill="none">
     <g id="symbol-core">
       <circle id="symbol-orbit-outer" cx="256" cy="256" r="230" stroke="currentColor" stroke-width="6" vector-effect="non-scaling-stroke" />
       <ellipse id="symbol-orbit-1" cx="256" cy="256" rx="210" ry="110" stroke="currentColor" stroke-width="4" transform="rotate(-30 256 256)" vector-effect="non-scaling-stroke" />
       <ellipse id="symbol-orbit-2" cx="256" cy="256" rx="210" ry="110" stroke="currentColor" stroke-width="4" transform="rotate(30 256 256)" vector-effect="non-scaling-stroke" />
     </g>
     <g id="symbol-monogram">
       <!-- Trazos esculpidos monocromáticos -->
     </g>
   </svg>
   ```
3. **Soporte Dark Mode / Light Mode:**
   - **Dark Mode:** Trazos blancos (`#ffffff` o `currentColor`) sobre fondo negro/grafito (`#000000` / `#0f172a`).
   - **Light Mode:** Trazos negros (`#000000` o `currentColor`) sobre fondo blanco/marfil (`#ffffff` / `#f8fafc`).

---

## 3. Estructura de 3 Opciones por Categoría en `symbol_manifest.json`

El archivo `symbol_manifest.json` debe contener:
- **`isologos`:** Array de 3 propuestas completas con nombre, descripción geométrica y código `svg_raw`.
- **`monograms`:** Array de 3 propuestas de iniciales (`svg_raw`).
- **`favicons`:** Array de 3 glifos micro-optimizados (64x64).
- **`selected_vector_id`:** ID del vector elegido por defecto o seleccionado por el usuario (ej: `"isologo-1"`).
- **`lockup`:** Coordenadas espaciales para el ensamblado con la tipografía de Fase 1.

---

## 4. Pipeline de Exportación Client-Side (Canvas Retina + PDF Vectorial)

La WebApp `brandview` consume `symbol_manifest.json` y permite exportar mediante:
1. **Canvas Retina ($2\times/3\times$):** Renderizado escalado por `window.devicePixelRatio` para PNG nítido.
2. **PDF Vectorial:** Incrustación directa de comandos vectoriales a 300 DPI mediante `jsPDF` + `svg2pdf.js`.

---

## 5. Arquitectura Desacoplada & Ingestión Directa SSoT

La fuente primaria y canónica de verdad es `astrobranding_[MARCA].md` compilado por Oráculo en Fase 0 a partir de los shards astronómicos y arquetípicos.
- **Desacople de Cascada:** `symbol` puede ejecutarse directamente sin requerir que `fontgen` haya concluido. Si `font_manifest.json` existe en disco, hereda las fuentes y proporciones de lockup; de lo contrario toma las directrices del SSoT o valores por defecto armónicos ($\Phi = 1.618$).
- **Cascada No Bloqueante:** La cascada entre fases es opcional y no bloqueante.
- **Contratos de Salida Garantizados:** Emite `symbol_manifest.json` (3 isologos, 3 monogramas, 3 favicons en estricto B/N con IDs semánticos `#symbol-core`, `#symbol-orbit-1`, `#symbol-orbit-2`, `#symbol-geometry-star`, `#symbol-monogram`) y código dev SVG puro para `brandview`.

