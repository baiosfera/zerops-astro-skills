# Fontgen: Infraestructura Astro 2026 Fonts API, WOFF2 Local y `CLS = 0` (`v7.0`)

Este documento define el suministro tipográfico en producción para `astro-web` (cero peticiones runtime a CDNs externos), la sintaxis verificada de Astro 2026 y las métricas duales `CLS = 0` de `fontgen_engine.py v7.0`.

---

## 1. Astro 2026 Native Fonts API (`astro.config.mjs`)

En `astro-web`, las fuentes se descargan y empaquetan en **tiempo de build** como `WOFF2` locales con *fallbacks* métricos automáticos (`optimizedFallbacks: true`) y sintaxis verificada en Context7 (`/websites/astro_build_en`):

```js
// astro.config.mjs — generado en font_manifest.json -> astro_web_ready.astro_fonts_config
import { defineConfig, fontProviders } from "astro/config";

export default defineConfig({
  fonts: [
    {
      provider: fontProviders.fontsource(),
      name: "Source Serif 4",
      cssVariable: "--font-display",
      weights: ["300 800"],
      styles: ["normal", "italic"],
      optimizedFallbacks: true,
    },
    {
      provider: fontProviders.fontsource(),
      name: "Hanken Grotesk",
      cssVariable: "--font-body",
      weights: ["300 800"],
      styles: ["normal", "italic"],
      optimizedFallbacks: true,
    },
    // Opcional cuando existan archivos .woff2 licenciados en src/assets/fonts/:
    // { provider: fontProviders.local(), name: "CustomDisplay", cssVariable: "--font-display", options: { variants: [{ weight: "400 800", style: "normal", src: ["./src/assets/fonts/display.woff2"] }] } }
  ],
});
```

---

## 2. Prevención Dual de Layout Shift (`CLS = 0.00`)

`fontgen_engine.py v7.0` emite `@font-face` de respaldo calibrados tanto para **Display** como para **Body** (`size-adjust`, `ascent-override`, `descent-override`, `line-gap-override`), junto con `font-optical-sizing: auto` y `font-size-adjust: from-font` (respaldado por `@supports not (font-size-adjust: from-font)`).

---

## 3. Contratos de Persistencia y Paridad SSoT

- **Salida Aislada (`--output-dir`):** `font_manifest.json` y `fontgen_<vertical>.md`.
- **Paridad Obligatoria:** `/var/www/zerops-astrobranding/scripts/fontgen_engine.py` debe mantenerse byte-idéntico a `/var/www/zerops-astro-skills/fontgen/scripts/fontgen_engine.py` (sin residuos `__pycache__`).
- **Validación:** `python3 -B -m py_compile` + `fontgen-engine --test` + esquema `assets/schemas/font_manifest.schema.json`.
