---
name: chroma
description: "Trigger: chroma, paleta de color, oklch, wcag aaa, apca, psicologia del color, tokens de color, contraste de marca, 3 ecosistemas. Disena y valida 3 ecosistemas de color en OKLCH y ratios WCAG AAA/APCA."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "5.1"
---

# Chroma — Art-Direction OKLCH & Sibling-Aware Engine (v5.1)

## Activation Contract
Activar al diseñar o validar ecosistemas cromáticos mediante `chroma-engine` (`v5.1`), generando **3 Mundos Cromáticos Diferenciados** (Dark & Light) desde Dirección de Arte (`--palette-json` / `--seed-hex` / `--brand-brief`) o desde 15 shards + `verticals/<v>.json` con rotación por rama hermana (`--sibling-workspaces-dir`).

## Input Rule (Con o Sin Oráculo & Fidelidad Cromática)
- **CLI Sin Oráculo (Art Direction First):** `chroma-engine --brand <BRAND> --brand-brief <brand_brief.json> --palette-json <art_direction_palettes.json> [--seed-hex "#HEX"] --output-dir <ws>/brand`. Preserva hexes vibrantes curados y calcula `on_primary` / `on_accent` ($\ge 4.5:1$).
- **CLI Con Oráculo:** `chroma-engine --brand <BRAND> --vertical <slug> --shards <client_dumps_15_shards.json> --vertical-json <vertical.json> --sibling-workspaces-dir <dev>/workspaces --output-dir <ws>/brand`. Prioriza shards sobre brief y extrae signo/MC/Nakshatra/Day Master desde brief si faltan shards.
- **Aislamiento Estricto:** Escribe exclusivamente en `--output-dir` (cero carpetas fantasma).

## Hard Rules (Directivas Obligatorias)
1. **Reglas Anti-Slop (`taste-skill` §4.2 + `impeccable`):** Prohibido el cliché AI azul neón (`#38b6ff`/`#080c14`), púrpuras neón sin intención (`#9333ea`) y beige cálido + latón (`#f5f1ea`/`#b08947`).
2. **Tokens W3C DTCG 2025.10 + Tailwind v4:** Emite `$value` (`oklch`), `on_primary`, `on_accent`, `hex`, `p3`, `--brand-on-primary`, `--brand-on-accent` y `:root` alineado a `recommended_mode`.
3. **Auditoría Física Real:** Garantiza WCAG 2.2 AAA $\ge 7.0:1$ en texto, $\ge 4.5:1$ en `on_primary` sobre botón `primary` y APCA $|L_c| \ge 75.0$ en ambos modos.
4. **Previsualización & Self-Test:** Emite `chroma_preview.html` y se valida con `chroma-engine --test`.

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/chroma/references/usage.md) — Manual OKLCH, WCAG/APCA y `chroma-engine`.
- [`references/infra.md`](file:///var/www/zerops-astro-skills/chroma/references/infra.md) — Conversión P3/sRGB e inyección Tailwind CSS v4.
- [`assets/schemas/chroma_manifest.schema.json`](file:///var/www/zerops-astro-skills/chroma/assets/schemas/chroma_manifest.schema.json) — Esquema JSON.
- [`assets/templates/chroma_manifest_template.json`](file:///var/www/zerops-astro-skills/chroma/assets/templates/chroma_manifest_template.json) — Plantilla.
