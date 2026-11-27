# Symbol: Normalización SVG Real, Partes Semánticas y `<BrandMark.astro />` (`v2.0`)

Este manual define la ingeniería vectorial real de `symbol_engine.py v2.0` alineada a `PB19 v2.0.0` para transformar logotipos o monogramas `.svg` crudos (con transformaciones anidadas, fondos rígidos o colores hardcodeados) en activos listos para `astro-web` y `kinetic`.

---

## 1. Flujo de Normalización Vectorial

1. **Aplanado de Matrices Afines:** Convierte `translate()`, `scale()`, `rotate()` y `matrix()` anidados en coordenadas absolutas sobre cada `<path>`.
2. **Limpieza de Fondo y Colores:** Detecta rectángulos de fondo sólido (`<rect fill="...">`), registra el color original en `normalization.background_stripped` y lo elimina del master vectorial.
3. **Subpaths Inteligentes (`#symbol-part-1..N`):** Separa trazos independientes en nodos `<path id="symbol-part-k" />` dentro de `<g id="symbol-mark">` para que `kinetic` pueda coreografiarlos, conservando unidos los huecos internos (*counters* de letras como `O`, `A`, `D`) mediante análisis de caja envolvente.
4. **Normalización Óptica (`0 0 100 100`):** Evalúa puntos de control Bézier (`Q`/`C`) para calcular la caja real y centra proporcionalmente el símbolo dentro de `viewBox="0 0 100 100"` con margen de seguridad (`12%`).

---

## 2. Artefactos Emitidos (`--output-dir`)

- `symbol_mono.svg`: maestro monocromo puro (`fill="currentColor"`).
- `symbol_brand.svg`: maestro reactivo a tokens (`fill="var(--brand-primary, currentColor)"`).
- `favicon.svg`: icono adaptativo 2026 con `@media (prefers-color-scheme: light)` alimentado por `chroma_manifest.json`.
- `BrandMark.astro`: componente Astro SSR de `0 KB` JS con props `size`, `variant="mono"|"brand"` y accesibilidad automática (`aria-hidden` vs `role="img"` + `aria-label`).
- `symbol_manifest.json`: metadatos, partes semánticas, `lockup_ratios` y SVG embebidos.
- `symbol_preview.html`: inspector interactivo comparando SVG original vs. normalizado, B/N, teñido `chroma`, legibilidad de favicon (`16–64px`) y lockup horizontal en cabecera.
