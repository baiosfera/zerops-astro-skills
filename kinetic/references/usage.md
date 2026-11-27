# Kinetic: Manual de Motion 60fps GPU-Only y Live Preview (`v2.0`)

Este manual formaliza cómo `kinetic_engine.py v2.0` traduce la doctrina de movimiento de `PB19 v2.0.0` (Módulo 6.3) a presets reutilizables de `0 KB` JS en CSS puro más un hook perezoso compatible con Astro View Transitions.

---

## 1. Por qué 3 Presets Sobrios (y Cero Ruido)

En `astro-web`, el movimiento no adorna tarjetas en bucle ni dispara audios sin permiso: dirige la atención en **un momento coreografiado por vista** respetando `LCP < 1.0s`, `CLS = 0` e `INP < 200ms`.

1. **`editorial_reveal` (`650ms`):** revelado por máscara `clip-path` + desplazamiento `translateY(10px -> 0)` en curva exponencial `cubic-bezier(0.16, 1, 0.3, 1)`. Ideal para portadas y encabezados de marca.
2. **`staggered_precision` (`520ms` + `120ms/trazo`):** entrada secuencial sobre cada trazo real del símbolo (`#symbol-part-1`, `#symbol-part-2`, ...) generado por `symbol-engine`, más micro-elevación `translateY(-2px)` en `:hover`.
3. **`ambient_signature` (`540ms` + hover `scale(1.035)`):** entrada limpia + respuesta arquitectónica al puntero para cabeceras y navegación.

---

## 2. Invariantes de Rendimiento y Accesibilidad

- **Solo propiedades compuestas GPU:** `opacity`, `transform`, `clip-path`. Queda excluida cualquier propiedad de *Layout* o *Paint* (`width`, `height`, `margin`, `top`, `left`, `transition: all`).
- **Degradación obligatoria:** todo CSS generado incluye `@media (prefers-reduced-motion: reduce)` anulando animaciones y dejando `opacity: 1` inmediato.
- **Ciclo de vida Astro:** `astro_lifecycle_ts` encapsula el `IntersectionObserver` dentro de `requestIdleCallback`, limpia en `astro:before-swap` y reinicia en `astro:page-load`.

---

## 3. Visor Interactivo `kinetic_preview.html`

Permite inspeccionar el símbolo real de `symbol_manifest.json` teñido con `chroma_manifest.json` en los 3 presets a la vez, con botones para repetir animaciones, alternar Dark/Light y simular `prefers-reduced-motion`.
