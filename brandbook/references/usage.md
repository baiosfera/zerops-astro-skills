# Brandbook: Manual de Compilación W3C DTCG 2025.10 y Fusión No Destructiva (`v2.0`)

Este documento especifica cómo se consolidan los manifiestos de `chroma v6.0`, `fontgen v5.0`, `symbol v2.0` y `kinetic v2.0` dentro de `brandbook.json` y `brandbook-theme.css` para su consumo directo en `astro-web`, `brand-studio`, `brand-play` y `brandfont`.

---

## 1. Separación entre Estrategia Humana y Tokens Visuales

Para evitar que una regeneración de colores o fuentes borre el posicionamiento comercial de la marca:
- **Ramas preservadas:** `metadata`, `brand_architecture`, `voice_tone_and_messaging`, `lexicon`, `target_audience`, `vertical_context`.
- **Rama actualizada:** `design_system` (`colors`, `typography`, `dtcg_tokens`), heredando `surface_geometry`, `web_ready_bridge` y `astro_web_ready`.

---

## 2. CSS de Producción Sin Fuentes Fantasma (`brandbook-theme.css`)

`brandbook-theme.css` se compila listo para importarse en `astro-web` (`@import "tailwindcss"; @theme inline { ... }`):
- **Colores:** `[data-brand]` + `[data-theme="light"|"dark"]`, `color-scheme: light dark`, `oklch(from var(--brand-primary) ...)` y superficies nativas (`::selection`, `caret-color`, `scrollbar-color`, `:focus-visible`).
- **Tipografía:** `astro_web_ready.css_typography_system` con familias auto-hospedadas verificadas, `@font-face` duales `CLS = 0`, `clamp()`, `60ch–72ch`, `text-wrap: balance`, `font-optical-sizing: auto` y `tabular-nums`.

---

## 3. Integración Vectorial y Cinética

- **Vectores (`symbol v2.0`):** `symbol/BrandMark.astro` y `symbol/favicon.svg` consumen directamente `--brand-primary` del tema activo.
- **Movimiento (`kinetic v2.0`):** `kinetic/kinetic_motion.css` anima únicamente las partes reales del SVG con `transform`, `opacity` y `clip-path`.
