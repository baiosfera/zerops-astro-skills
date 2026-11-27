# Orchesbrand: Manual de Invocación Art-Direction-First & Control de Estado (v4.5)

Este documento describe la operativa técnica de `orchesbrand v4.5` sobre proyectos independientes (`ZCP` aislados o multimarca), integrando `chroma v8.0`, `fontgen v7.0`, `envato-font-preview v5.1`, `symbol v2.0` y `kinetic v2.1`.

---

## 1. Flujo en Dos Etapas (Dirección de Arte -> Compiladores)

1. **Dirección de Arte (`chroma_spec.json` + `font_spec.json`):** El agente concibe 3 ecosistemas cromáticos y 3 ecosistemas tipográficos originales a partir de la categoría, audiencia y posicionamiento real de la marca.
2. **Compilación Determinística:**
```bash
orchesbrand --brand <BRAND> --vertical <slug> --brand-brief <brand_brief.json> \
  --chroma-spec <ws>/brand/chroma_spec.json --font-spec <ws>/brand/font_spec.json \
  --preview-texts "<MARCA>,<SUBTITULO>" --output-dir <ws>/brand --audit
```
3. **Opt-In de Oráculo (Solo si se solicita explícitamente):** Pasar `--brief <astrobranding_*.md>` y `--shards <15_shards.json>` (+ `--chroma-mode brief` si se desea extraer tablas §3). Sin esos flags explícitos, no se contamina la marca con archivos externos en disco.

---

## 2. Manejo de Errores, Inspección Visual y Diagnóstico Forense

- **Auditoría Estructural (`--audit`):** Valida `>= 3` ecosistemas en `chroma_manifest.json` y `font_manifest.json`, cumplimiento `status_aaa`, y presencia de `brandbook.json` + `brandbook-theme.css`.
- **Inspección Visual Obligatoria:** Capturar y revisar con herramienta visual `chroma_preview.html` y `previews/preview_gallery.html` en Chrome headless (`1440x1200`) antes de dar por cerrada una identidad.

---

## 3. Merge No Destructivo y Sincronía SSoT

- Preserva `brand_architecture`, `voice_tone_and_messaging`, `lexicon` y `target_audience` dentro de `brandbook.json`.
- Actualiza únicamente `design_system` (`colors`, `typography`, `dtcg_tokens`, `astro_web_ready`) y `brand_colors`, generando `brandbook-theme.css` con `OKLCH` + `CLS = 0`.
