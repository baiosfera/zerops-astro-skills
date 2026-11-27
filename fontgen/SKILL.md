---
name: fontgen
description: "Trigger: fontgen, tipografia, fuentes, matriz tipografica, design tokens de fuentes, emparejamiento tipografico, 3 ecosistemas. Genera la direccion de arte y 3 ecosistemas tipograficos hibridos (Envato + Google Fonts) con 6 capas funcionales."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "7.0"
---

# `fontgen` — Art-Direction-First Variable WOFF2, Astro Fonts API & CLS=0 Engine (v7.0)

## Activation Contract
Activate when conceiving, compiling, or auditing typographic systems with `fontgen-engine` (`v7.0`) aligned to Playbook 19 (`v2.0.0`) and Astro 2026 Native Fonts API (`fontProviders.fontsource()` + `fontProviders.local()`). Separates **Creative Art Direction** (`font_spec.json`, authored fresh per project from domain tone — zero hidden Oráculo crawl) from **Deterministic Compilation** (26 curated Fontsource variable families, Envato quality filtering, dual `CLS = 0` metric overrides, and SVG specimens in `envato-font-preview v5.1`).

## Two-Stage Workflow & Zero Silent Oráculo Leak
1. **Stage 1 — Bespoke Art Direction (`font_spec.json`):** Author 3 genuinely distinct typographic directions in `<ws>/brand/font_spec.json` (Display Web, Body Web, scale ratio, tracking, and targeted Envato display/accent queries) tailored to the brand's positioning — never generic tech/startup clichés.
2. **Stage 2 — Compile & Render Specimens:**
   - **Art-Direction Spec (Default):** `fontgen-engine --brand <BRAND> --spec <ws>/brand/font_spec.json --brand-brief <vertical.json> --output-dir <ws>/brand`
   - **Oráculo Opt-In Only:** Add `--shards <15_shards.json> --brief <astrobranding_*.md>` explicitly when astrological chart axes are intentionally part of the design brief. Without `--shards`/`--brief`, `has_oraculo` stays strictly `false`.
   - **Web + SVG Gallery:** `envato-font-preview --from-manifest <ws>/brand/font_manifest.json --chroma <ws>/brand/chroma_manifest.json --texts "MARCA,SUBTITULO" [--include-shortlist] --out <ws>/brand/previews`
3. **Strict Isolation:** Writes exclusively inside `--output-dir` (`font_manifest.json`, `fontgen_<vertical>.md`) and supports `--sibling-workspaces-dir` / `--exclude-fonts` for cross-vertical distinctness.

## Hard Rules (Positive Guidance)
1. **Anti-Slop Typographic Floor & <=2 Core Families:** Blocks AI clichés (`Inter`, `Fraunces`, `Instrument Serif`, `Plus Jakarta Sans`, `Space Grotesk`, `DM Sans`, `Instrument Sans`, `Outfit`, `Syne`, `Playfair Display`, `Newsreader`, `IBM Plex`, `Lora`, `Cormorant`, `Crimson`, `Space Mono`). Restricts active families to `display` + `body` (+ conditional `mono`).
2. **Quality-Gated Envato Discovery:** Blocks sci-fi/amateur noise (`futuristic`, `cyber`, `techno`, `scifi`, `wedding`, `calligraphy`, `"for elegant"`, `"for branding"`), penalizes keyword-stuffed titles, and weights `popular` craft above unvetted `latest`.
3. **Verified Astro 2026 Native Fonts Config:** Generates Context7-compliant `astro.config.mjs` entries (`fontProviders.fontsource()` and `fontProviders.local({ options: { variants: [...] } })`) with zero runtime third-party font CDNs.
4. **Dual `CLS = 0` & Readable Visual Specimens:** Emits `@font-face` metric overrides for Display and Body, `font-size-adjust: from-font`, `60ch–72ch` prose measure, and crisp `width`/`height`/`viewBox` SVG fallbacks inside `preview_gallery.html`.
5. **Byte-Parity & Verification:** Keep `scripts/fontgen_engine.py` byte-identical between `zerops-astrobranding/scripts/` and `zerops-astro-skills/fontgen/scripts/`, pass `fontgen-engine --test` + `envato-font-preview --test`, and inspect `preview_gallery.html` in headless Chrome.

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/fontgen/references/usage.md) · [`references/infra.md`](file:///var/www/zerops-astro-skills/fontgen/references/infra.md)
- [`assets/schemas/font_manifest.schema.json`](file:///var/www/zerops-astro-skills/fontgen/assets/schemas/font_manifest.schema.json)
