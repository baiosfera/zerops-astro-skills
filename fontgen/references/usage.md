# Fontgen: Art-Direction-First Spec, Modos CLI y Envato Filtering (v7.0)

Este manual detalla el flujo en dos etapas de `fontgen_engine.py v7.0` y `envato_font_preview.py v5.1` para generar tipografía distintiva en proyectos aislados o multimarca.

---

## 1. Stage 1 — `font_spec.json` a Medida del Posicionamiento

El agente director de arte redacta 3 ecosistemas tipográficos verdaderamente contrastantes (ej. Editorial Serif + Humanista, Grotesca Expresiva, Didone de Autoridad) dentro de `<ws>/brand/font_spec.json`:

```json
{
  "ecosystems": [
    {
      "id": "eco-1",
      "name": "Editorial Serif + Humanista",
      "rationale": "Autoridad intelectual con lectura cálida y alta densidad conceptual.",
      "display_web": "Source Serif 4",
      "body_web": "Hanken Grotesk",
      "italic_web": "Source Serif 4",
      "scale_ratio": 1.333,
      "tracking_em": -0.020,
      "display_weight": 700,
      "envato_display_query": "editorial serif",
      "envato_accent_query": "grotesk sans"
    }
  ]
}
```

---

## 2. Stage 2 — Compilación, Cero Fugas de Oráculo y Filtro de Calidad

- **Cero Rastreo Silencioso en Disco:** `fontgen_engine.py v7.0` eliminó cualquier búsqueda implícita sobre carpetas externas de Oráculo. Sin `--shards` ni `--brief` explícitos, `has_oraculo` es estrictamente `false`.
- **Filtro Anti-Slop Web (`GOOGLE_FONTS_CATALOG`):** 26 familias variables reales (`Source Serif 4`, `Literata`, `EB Garamond`, `Bodoni Moda`, `Bricolage Grotesque`, `Schibsted Grotesk`, `Hanken Grotesk`, `Albert Sans`, `Familjen Grotesk`, `Onest`, `Work Sans`, `Host Grotesk`, etc.) con bloqueo activo sobre fuentes quemadas por IA.
- **Scoring Profesional Envato (`_is_noisy_title` & `_score_candidate`):** Bloquea ruido amateur/temático (`futuristic`, `cyber`, `techno`, `wedding`, `calligraphy`, `"for elegant"`, `"for branding"`), penaliza títulos SEO con más de 3 palabras y prioriza `popular` + SVG verificado.
- **Disyunción entre Hermanos y Proyectos Aislados:** `--sibling-workspaces-dir` y `--exclude-fonts` garantizan cero superposición entre verticales; en contenedores ZCP aislados, `font_spec.json` + rotación por semilla producen selecciones únicas sin conocer proyectos vecinos.

---

## 3. Verificación Real & Captura Visual

```bash
fontgen-engine --brand <BRAND> --spec <ws>/brand/font_spec.json --brand-brief <vertical.json> --output-dir <ws>/brand
envato-font-preview --from-manifest <ws>/brand/font_manifest.json --chroma <ws>/brand/chroma_manifest.json \
  --texts "MARCA,SUBTITULO" --include-shortlist --out <ws>/brand/previews
fontgen-engine --test && envato-font-preview --test
google-chrome --headless --no-sandbox --disable-gpu --window-size=1440,1200 \
  --virtual-time-budget=3000 --screenshot=/tmp/font_gallery.png \
  "file://<ws>/brand/previews/preview_gallery.html"
```
