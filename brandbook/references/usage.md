# Brandbook: Manual de Compilación W3C DTCG, Consumo por Agentes LLM & Exportación Gráfica SOTA

Este documento establece la metodología para compilar el `brandbook.json` bajo el estándar formal **W3C Design Tokens Community Group (DTCG)**, facilitando su consumo automatizado por otros agentes de IA, y especificando los pipelines de exportación visual fidedigna.

---

## 1. Por qué `brandbook.json` debe ser 100% W3C DTCG para Agentes Downstream

Cuando otro agente de IA (como `sdd-apply`, un scaffold de Astro, Next.js o PayloadCMS) necesita implementar la interfaz de usuario:
1. **Tipado Estricto de Tokens:** Cada nodo contiene `$type` (`color`, `fontFamily`, `duration`, `cubicBezier`, `dimension`), evitando que el LLM confunda un string de color con una clase CSS.
2. **Jerarquía Unívoca:** El árbol se divide en `brand`, `typography`, `color`, `motion`, `sound`, `vectors`, `accessibility`.
3. **Extensiones Listas para Usar (`$extensions`):**
   - `$extensions.tailwind_v4`: Bloque `@theme` completo para copiar directamente en `global.css`.
   - `$extensions.css_variables`: Declaraciones `:root` para componentes Web Components o CSS puro.
   - `$extensions.zerops`: Variables de entorno de diseño.

```json
{
  "$schema": "https://www.designtokens.org/TR/2025.10/format/",
  "name": "NombreDeMarca",
  "version": "1.0.0",
  "brand": {
    "name": { "$value": "CATALINA GLAMUR", "$type": "string" },
    "slogan": { "$value": "Quiet Luxury Athleisure", "$type": "string" }
  },
  "color": {
    "brand": {
      "primary": {
        "$value": "oklch(0.85 0.12 85)",
        "$type": "color",
        "$description": "Oro Champagne satinado para autoridad y monograma",
        "hex": "#E2C974"
      }
    }
  },
  "typography": {
    "display": {
      "$value": "Rising",
      "$type": "fontFamily",
      "$description": "Modern Luxury Serif para titulares H1"
    }
  }
}
```

---

## 2. Pipeline de Exportación Gráfica Fidedigna (SVG, PNG, JPG, PDF)

La exportación en `brandview` debe renderizar **el Isologotipo exactamente como fue evolucionado**:
- **SVG:** Vectorial puro limpio sin tags innecesarios, con los textos tipográficos convertidos o referenciados a las fuentes definitivas y colores inyectados.
- **PNG Retina ($2\times/3\times$):** Renderizado en backend mediante `@resvg/resvg-js` + `sharp` o en frontend vía Canvas HTML5 escalado con `window.devicePixelRatio`.
- **JPG High-Res:** Fondo sólido según el tema seleccionado (`#0f172a` o `#ffffff`).
- **PDF Vectorial:** Maquetado con `jsPDF` + `svg2pdf.js` incluyendo la ficha técnica, valores OKLCH/HEX, muestras tipográficas y el isologotipo principal.

---

## 3. Arquitectura Desacoplada & Ingestión Directa SSoT

La fuente primaria y canónica de verdad es `astrobranding_[MARCA].md` compilado por Oráculo en Fase 0 a partir de los shards del VirtualDataLake.
- **Desacople Total de Cascada:** `brandbook` puede compilar el `brandbook.json` DTCG y el manual ejecutivo directamente desde el SSoT sin requerir que los 4 manifiestos previos (`font_manifest.json`, `symbol_manifest.json`, `chroma_manifest.json`, `kinetic_manifest.json`) existan completos en disco.
- **Cascada No Bloqueante & Consolidación Flexible:** Si uno o más manifiestos existen en disco, consolida sus selecciones definitivas; cualquier token faltante se deriva armoniosamente desde el SSoT sin detener la compilación.
- **Contratos de Salida Garantizados:** Emite `brandbook.json` (W3C DTCG completo con extensiones Tailwind v4 y CSS variables), `brandbook_manifest.md` e `index.html` interactivo descargable consumibles por `brandview` o herramientas downstream.

