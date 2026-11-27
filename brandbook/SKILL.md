---
name: brandbook
description: "Trigger: brandbook, manual de marca, guia de estilos, brand guidelines, consolidacion de branding, dtcg tokens. Compila y sincroniza brandbook.json W3C DTCG 2025.10 y brandbook-theme.css sin destruir estrategia ni lexico."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `brandbook` — Non-Destructive W3C DTCG 2025.10 & Theme Compiler (v2.0)

## Activation Contract
Activate when consolidating brand strategy (`brand_architecture`, `voice_tone_and_messaging`, `lexicon`) with verified visual outputs from `chroma` (`v6.0`), `fontgen` (`v5.0`), `symbol` (`v2.0`), and `kinetic` (`v2.0`) into `brandbook.json` and `brandbook-theme.css` for `brand-studio`, `brand-play`, `brandfont`, and `astro-web`.

## Canonical Execution Paths
- **Non-Destructive Merge (Recommended via `orchesbrand`):**
  ```bash
  orchesbrand --brand <BRAND> --vertical <slug> --project-dir /mnt/localstorage/<Project>/dev --phases chroma,fontgen,previews,brandbook --audit
  ```
- **Direct Fast-Track Superfull Compiler (Oráculo Shards -> Full JSON):**
  `scripts/brandbook_pipeline_runner.py` when bootstrapping initial brand strategy from scratch.

## Hard Rules (Positive Guidance)
1. **Non-Destructive Merge Invariant:** Never overwrite `brand_architecture`, `voice_tone_and_messaging`, `lexicon`, or `target_audience` when updating `design_system` (`colors`, `typography`, `dtcg_tokens`, `astro_web_ready`) in workspace `brandbook.json`.
2. **W3C DTCG 2025.10 Three-Layer Contract:** Store primitive `OKLCH` values, semantic aliases, and component geometry (`radius_card`, `radius_control`, `elevation_style`, `color_strategy`) plus `typography` composite tokens (`scale_ratio`, `h1`, `body`, conditional `mono`).
3. **Zero Phantom Fonts in `brandbook-theme.css`:** Emit `@theme inline`, `[data-brand]` / `[data-theme]` variables, `oklch(from ...)` hover tokens, `color-mix(in oklch, ...)` borders, and dual Display + Body `CLS = 0` `@font-face` fallbacks wired strictly to verified self-hosted families (`web_ready_bridge` / Astro 2026 Fonts API).
4. **Decoupled Vector & Motion Composition:** Integrate `symbol/symbol_manifest.json` (`BrandMark.astro`, adaptive `favicon.svg`) and `kinetic/kinetic_manifest.json` (`kinetic_motion.css`) without requiring them as blocking preconditions.
5. **Physical Verification:** Pass `orchesbrand --test` and verify `brandbook.json` + `brandbook-theme.css` contain zero banned AI fonts or `#000000`.

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/brandbook/references/usage.md) · [`references/infra.md`](file:///var/www/zerops-astro-skills/brandbook/references/infra.md)
- [`scripts/brandbook_pipeline_runner.py`](file:///var/www/zerops-astro-skills/brandbook/scripts/brandbook_pipeline_runner.py)
