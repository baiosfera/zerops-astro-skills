---
name: symbol
description: "Trigger: symbol, isologo, monograma, logo vectorial, svg, icono de marca, favicon adaptativo, brandmark. Normaliza, limpia y compila iconos y monogramas SVG en monocromo, tokens CSS reactivos y componentes astro-web."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `symbol` — SVG Normalizer, Subpath Splitter & Astro BrandMark Engine (v2.0)

## Activation Contract
Activate when normalizing a raw brand mark / monogram `.svg` (or designing clean SVG brand marks) for `astro-web` and `orchesbrand` via `symbol-engine` (`v2.0`). Replaces fake sacred-geometry boilerplate with real affine transform flattening, optical `viewBox` normalization, semantic subpath splitting (`#symbol-part-1..N`) for `kinetic`, adaptive `favicon.svg`, and zero-JS `<BrandMark.astro />`.

## Canonical CLI & Isolation
```bash
symbol-engine --input <raw_icon.svg> --brand "<BRAND>" [--chroma <ws>/brand/chroma_manifest.json] --output-dir <ws>/brand/symbol
```
- **Self-Test:** `symbol-engine --test`
- **Strict Isolation:** Emits solely inside `--output-dir` (`symbol_mono.svg`, `symbol_brand.svg`, `favicon.svg`, `BrandMark.astro`, `symbol_manifest.json`, `symbol_preview.html`).

## Hard Rules (Positive Guidance)
1. **Flatten Nested Transforms & Strip Raw Canvas:** Flatten all chained `<g transform="...">` matrices directly onto absolute coordinates, strip solid background `<rect>` layers, compute exact curve extrema (`Q`/`C`), and normalize uniformly into `viewBox="0 0 100 100"` with `12%` optical safe padding.
2. **Semantic Subpath Splitting (`#symbol-part-1..N`):** Split independent strokes/glyphs into `<path id="symbol-part-1" ... />`, `<path id="symbol-part-2" ... />` inside `<g id="symbol-mark">` while keeping interior counter holes merged with their outer contour so fills remain intact.
3. **Zero Hardcoded Colors in Masters:** `symbol_mono.svg` uses `fill="currentColor"` with transparent background; `symbol_brand.svg` binds to `fill="var(--brand-primary, currentColor)"` for automatic `[data-brand]` / `[data-theme]` switching.
4. **Adaptive Dark/Light `favicon.svg` & `<BrandMark.astro />`:** Generate a single modern `favicon.svg` with embedded `@media (prefers-color-scheme: light|dark)` wired to `chroma_manifest.json`, plus a zero-JS accessible `<BrandMark.astro />` (`aria-hidden` when decorative, `role="img"` + `aria-label` when semantic).
5. **Visual & Optical Legibility Inspection:** Inspect `symbol_preview.html` across Dark/Light/B&W/Chroma and `16px–64px` favicon sizes before promoting.

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/symbol/references/usage.md) · [`references/infra.md`](file:///var/www/zerops-astro-skills/symbol/references/infra.md)
- [`assets/schemas/symbol_manifest.schema.json`](file:///var/www/zerops-astro-skills/symbol/assets/schemas/symbol_manifest.schema.json)
