---
name: chroma
description: "Trigger: chroma, paleta de color, oklch, wcag aaa, apca, psicologia del color, tokens de color, contraste de marca, 3 ecosistemas. Disena y valida 3 ecosistemas de color en OKLCH y ratios WCAG AAA/APCA."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "5.2"
---

# Chroma — Art-Direction OKLCH, Surface Geometry & Sibling-Aware Engine (v5.2)

## Activation Contract
Activar al diseñar o validar ecosistemas cromáticos mediante `chroma-engine` (`v5.1`) + contrato de superficie (`PB19`), generando **3 Mundos Cromáticos Diferenciados** (Dark & Light) desde Dirección de Arte (`--palette-json` / `--seed-hex` / `--brand-brief`) o desde 15 shards + `verticals/<v>.json` con rotación por rama hermana (`--sibling-workspaces-dir`).

## Input Rule (Con o Sin Oráculo & Fidelidad Cromática)
- **CLI Sin Oráculo (Art Direction First):** `chroma-engine --brand <BRAND> --brand-brief <brand_brief.json> --palette-json <art_direction_palettes.json> [--seed-hex "#HEX"] --output-dir <ws>/brand`. Preserva hexes vibrantes curados y calcula `on_primary` / `on_accent` ($\ge 4.5:1$).
- **CLI Con Oráculo:** `chroma-engine --brand <BRAND> --vertical <slug> --shards <client_dumps_15_shards.json> --vertical-json <vertical.json> --sibling-workspaces-dir <dev>/workspaces --output-dir <ws>/brand`.
- **Aislamiento Estricto:** Escribe exclusivamente en `--output-dir` (cero carpetas fantasma).

## Hard Rules (Directivas Obligatorias)
1. **Estrategia Cromática Deliberada & Neutros Tintados:** Declarar estrategia (`Restrained`, `Committed`, `Full Palette` o `Drenched`) coherente con el mundo visual de `DESIGN.md`. Todo negro/neutro lleva matiz OKLCH de marca (`chroma 0.008–0.018`), evitando `#000000` puro, azul neón AI (`#38b6ff`/`#080c14`), púrpuras neón sin intención o beige + latón genérico.
2. **Geometría y Elevación No Dogmática (`PB19`):** Usar radios `12–16px` en tarjetas y `8–12px` / `999px` en controles por defecto; restringir `0px` estrictamente a mundos brutalistas/editoriales con justificación explícita. Declarar elevación una sola vez (borde sutil `1px` O sombra direccional suave, nunca ambos).
3. **Tokens W3C DTCG 2025.10 + Tailwind v4:** Emitir `$value` (`oklch`), `on_primary`, `on_accent`, `hex`, `p3`, `--brand-on-primary`, `--brand-on-accent` y `:root` alineado a `recommended_mode`.
4. **Auditoría Física Real:** Garantizar WCAG 2.2 AAA $\ge 7.0:1$ en texto, $\ge 4.5:1$ en `on_primary` sobre `primary` y APCA $|L_c| \ge 75.0$ en ambos modos; validar con `chroma-engine --test` y `chroma_preview.html`.

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/chroma/references/usage.md) · [`references/infra.md`](file:///var/www/zerops-astro-skills/chroma/references/infra.md)
- [`assets/schemas/chroma_manifest.schema.json`](file:///var/www/zerops-astro-skills/chroma/assets/schemas/chroma_manifest.schema.json) · [`assets/templates/chroma_manifest_template.json`](file:///var/www/zerops-astro-skills/chroma/assets/templates/chroma_manifest_template.json)
