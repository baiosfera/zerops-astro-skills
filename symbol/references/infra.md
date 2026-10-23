# Symbol: Infraestructura, Optimización Vectorial y Pipeline de Favicons (v2.0)

Este documento define la infraestructura de optimización SVG, sanitización estricta de seguridad y pipeline de generación de favicons multiplataforma.

---

## 1. Motor de Optimización SVG (`svgo` v3+)

Symbol utiliza `svgo` con una configuración que preserva la semántica de IDs para downstream animation (`kinetic`):

```javascript
import { optimize } from 'svgo';

export function optimizeBrandSvg(svgContent) {
  return optimize(svgContent, {
    multipass: true,
    plugins: [
      'removeDoctype',
      'removeXMLProcInst',
      'removeComments',
      'removeMetadata',
      'removeEditorsNSData',
      'cleanupAttrs',
      'mergeStyles',
      'inlineStyles',
      'minifyStyles',
      {
        name: 'cleanupIds',
        params: {
          preserve: ['symbol-core', 'symbol-orbit-1', 'symbol-orbit-2', 'symbol-geometry-star', 'symbol-monogram']
        }
      },
      'removeUselessDefs',
      'cleanupNumericValues',
      'convertColors',
      'removeUnknownsAndDefaults',
      'removeNonInheritableGroupAttrs',
      'removeUselessStrokeAndFill',
      'removeEmptyContainers',
      'cleanupEnableBackground'
    ]
  }).data;
}
```

---

## 2. Sanitización y Seguridad Vectorial

Para prevenir vulnerabilidades XSS o inyección de código:
- **Cero Elementos Ejecutables:** Se purgan automáticamente `<script>`, `<foreignObject>`, `<animate>`, `onload`, `onclick` o cualquier manejador de eventos inline.
- **Cero Enlaces Externos:** Prohibido el uso de `<image xlink:href="...">` o referencias a CDNs externos. Todo glifo debe estar completamente trazado en paths vectoriales.
- **Escalabilidad Vectorial:** Inyección de `vector-effect="non-scaling-stroke"` en trazos para mantener grosor constante al reescalar.

---

## 3. Pipeline Multi-Superficie de Favicons (PNG, ICO, SVG)

Generación automatizada de la suite completa de iconos mediante `sharp` / `resvg`:
- `favicon.svg`: Icono vectorial dinámico para navegadores modernos con soporte Dark/Light mode (`prefers-color-scheme`).
- `favicon-32x32.png` & `favicon-16x16.png`: Rasterizados nítidos para pestañas y barras de marcadores.
- `apple-touch-icon.png`: 180x180 píxeles con padding de seguridad para iOS.
- `favicon.ico`: Contenedor multi-resolución de legado (16, 32, 48px).

---

## 4. Contratos de Persistencia SSoT

- **Manifiesto Vectorial SSoT:** `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/symbol_manifest.json`
- **Espejo en Runtime Zerops:** `/var/www/localstorage/[MARCA]/dev/symbol_manifest.json`
- **Validación de Integridad:** Validado contra `assets/schemas/symbol_manifest.schema.json`.
