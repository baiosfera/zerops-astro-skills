---
name: kinetic
description: "Trigger: kinetic, animacion gsap, microinteracciones, motion design, 60fps, 3 opciones animacion, view transitions. Genera 3 presets de motion 60fps GPU-only vinculados a partes reales SVG y transiciones Astro."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# `kinetic` — 60fps GPU-Only Motion, Deliberate Cadence & Subtle Living Loop (v2.1)

## Activation Contract
Activate when authoring, testing, or auditing brand motion systems (`60fps`) on `astro-web` via `kinetic-engine` (`v2.1`). Binds directly to real normalized SVG parts (`#symbol-part-1..N` from `symbol_manifest.json`), reads Oráculo §5 cadence (`--brief astrobranding_*.md`) when present, and pairs **human-readable entrances** (`1150ms–1618ms`) with a **subtle continuous living loop** (`6.8s–8.0s infinite`) that keeps the mark alive without distorting geometry.

## Canonical CLI & Isolation
```bash
kinetic-engine --symbol <ws>/brand/symbol/symbol_manifest.json [--chroma <ws>/brand/chroma_manifest.json] [--brief <astrobranding_*.md>] --brand "<BRAND>" --output-dir <ws>/brand/kinetic
```
- **Self-Test:** `kinetic-engine --test`
- **Strict Isolation:** Emits solely inside `--output-dir` (`kinetic_manifest.json`, `kinetic_motion.css`, `kinetic_preview.html`).

## Hard Rules (Positive Guidance)
1. **Bind Only to Real SVG Selectors (`symbol_manifest.json`):** Target `#symbol-mark` and the actual `#symbol-part-1..N` IDs emitted by `symbol-engine` — never invent phantom orbital IDs.
2. **GPU-Composited Properties Only (`RAIL < 16ms`, `0` Bounce):** Animate strictly `transform`, `opacity`, and `clip-path` using deliberate editorial easing (`cubic-bezier(0.22, 1, 0.36, 1)`). Zero layout thrashing (`width`/`height`/`top`/`left`), zero `transition: all`, and zero unsolicited audio autoplay.
3. **3 Authored Presets (`0 KB` CSS Core + Living Loop):**
   - `editorial_reveal`: `1618ms` calm `clip-path` + `translateY(14px)` reveal chained to `7.2s` gentle `scale(1 -> 1.018)` breathing loop.
   - `staggered_precision`: staggered entrance across real `#symbol-part-1..N` strokes (`1150ms` + `320ms` stagger) chained to subtle phase-offset living float (`6.8s`, `-1.8px`).
   - `ambient_signature`: `1380ms` radial emergence chained to continuous calm solar float (`8.0s`, `-2.2px` / `scale 1.022`) + hover lift.
4. **Astro View Transitions & `prefers-reduced-motion`:** Use lazy `requestIdleCallback` `IntersectionObserver` wiring with `astro:before-swap` teardown and `astro:page-load` re-init, plus strict `@media (prefers-reduced-motion: reduce)` stop for both entrance and infinite loop.
5. **Interactive Visual Verification:** Inspect `kinetic_preview.html` (Replay All/Each, `Loop continuo: ON/OFF`, Light/Dark chroma toggle, and Reduced-Motion simulation) and pass `kinetic-engine --test`.

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/kinetic/references/usage.md) · [`references/infra.md`](file:///var/www/zerops-astro-skills/kinetic/references/infra.md)
- [`assets/schemas/kinetic_manifest.schema.json`](file:///var/www/zerops-astro-skills/kinetic/assets/schemas/kinetic_manifest.schema.json)
