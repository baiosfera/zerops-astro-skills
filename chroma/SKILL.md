---
name: chroma
description: "Trigger: chroma, paleta de color, oklch, wcag aaa, apca, psicologia del color, tokens de color, contraste de marca, 3 ecosistemas. Disena y valida 3 ecosistemas de color en OKLCH y ratios WCAG AAA/APCA."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "8.0"
---

# `chroma` — Art-Direction-First OKLCH, Step-9 & 3-Layer DTCG Engine (v8.0)

## Activation Contract
Activate when conceiving, compiling, or auditing brand color systems with `chroma-engine` (`v8.0`) aligned to Playbook 19 (`v2.0.0`), Radix Colors Step-9 saturation discipline, and CSS Color Level 5 (`OKLCH` / `Display P3`). Separates **Creative Art Direction** (`chroma_spec.json`, conceived fresh per project from positioning and visual world — never from canned archetypes) from **Deterministic Engineering Compilation** (CSS Color 4 gamut mapping, WCAG 2.2 AAA, APCA `0.0.98G-4g`, achromatic `C=0` Z-elevation monotonicity, and DTCG 2025.10 tokens).

## Two-Stage Workflow & Strict Opt-In Isolation
1. **Stage 1 — Bespoke Art Direction (`chroma_spec.json`):** Author 3 contrasting visual worlds in `<ws>/brand/chroma_spec.json` grounded strictly in the client brief, competitive field, and intended surface mood (zero copied palettes across projects, zero AI cyan/violet defaults, zero washed-out dark pastels).
   - Optionally anchor **Oráculo** ONLY when `--brief <astrobranding_*.md> --mode brief` or `--shards <15_shards.json>` are passed explicitly; never auto-crawl unrelated briefs on disk.
2. **Stage 2 — Compile & Harden:**
   `chroma-engine --brand <BRAND> --spec <ws>/brand/chroma_spec.json --output-dir <ws>/brand`
   - Fallback direct modes (when no `chroma_spec.json` exists): `--palette-json <palettes.json>`, `--seed-hex "#HEX"`, `--mode brief --brief <astrobranding_*.md>`, or brand-brief synthesis.
3. **Strict Isolation:** Writes solely inside `--output-dir` (`chroma_manifest.json`, `chroma_preview.html`). Works identically across isolated ZCP containers that have zero visibility into sibling projects.

## Hard Rules (Positive Guidance)
1. **Art-Direction-First, Zero Canned Pastels:** Preserves designer primary/accent pigments verbatim when accessible. In dark mode, prefers **Radix Step-9 solid saturated CTAs** (`L ~ 0.46–0.56` with crisp off-white `on_primary` ink `>= 4.5:1`) or pure monochrome bone (`#f2efe9`) rather than forcing vivid hues into muted `L=0.76` pastels.
2. **Deliberate Strategy & Tinted OKLCH Neutrals:** Declares `color_strategy` (`Restrained`, `Committed`, `Full Palette`, `Drenched`) and `60-30-10` proportion. Eliminates pure `#000000` and beige/muddy AI slop while keeping subtle tinted neutrals (`C ~ 0.005–0.014`) and single-elevation geometry (`border_1px` OR `soft_shadow`).
3. **CSS Color 4 Gamut Mapping & Display P3:** Clamps `sRGB` safely via binary search in `OKLCH` chroma (`gamut_map_oklch`) preserving perceptual Lightness and Hue while emitting `@supports (color: color(display-p3 ...))`.
4. **Dark-Mode Z-Elevation & Achromatic Audit (`C = 0`):** Enforces progressive dark elevation (`Z0 < Z1 <= Z2 <= Z3`), luminance delta `>= 0.55`, and complete semantic/component DTCG 2025.10 tokens (`primitive -> semantic -> component`).
5. **Physical & Visual Verification:** Guarantees WCAG 2.2 AAA (`>= 7.0:1` body), AA (`>= 4.5:1` buttons/muted), APCA (`|Lc| >= 75` body), passes `chroma-engine --test`, and verifies `chroma_preview.html` visually in headless Chrome.

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/chroma/references/usage.md) · [`references/infra.md`](file:///var/www/zerops-astro-skills/chroma/references/infra.md)
- [`assets/schemas/chroma_manifest.schema.json`](file:///var/www/zerops-astro-skills/chroma/assets/schemas/chroma_manifest.schema.json) · [`assets/templates/chroma_manifest_template.json`](file:///var/www/zerops-astro-skills/chroma/assets/templates/chroma_manifest_template.json)
