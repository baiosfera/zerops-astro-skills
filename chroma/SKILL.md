---
name: chroma
description: "Trigger: chroma, paleta de color, oklch, wcag aaa, apca, psicologia del color, tokens de color, contraste de marca, 3 ecosistemas. Disena y valida 3 ecosistemas de color en OKLCH y ratios WCAG AAA/APCA."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.1"
---

# Chroma — Motor OKLCH Multi-Eje Oráculo + 5 Arquetipos Verticales (v4.1)

## Activation Contract
Activar para diseñar o regenerar la arquitectura cromática mediante `chroma-engine` (`v4.1`), generando **3 Mundos Cromáticos Diferenciados** (Dark & Light compuestos intencionalmente) a partir de los 15 shards crudos de Oráculo (`client_dumps_15_shards.json`), `verticals/<v>.json` (bajo un único cliente/holding sombrilla) y reglas anti-slop de `design-taste-frontend` + `impeccable`.

## Input Rule (Multi-Vertical SSoT & Aislamiento)
- **CLI Canónico:** `chroma-engine --brand <BRAND> --vertical <slug> --shards <client_dumps_15_shards.json> --vertical-json <vertical.json> --brief <astrobranding_<brand>.md> --output-dir <workspace>/brand`.
- **Diferenciación por Arquetipo Vertical (`vertical_archetype`):** Un mismo cliente (`shards`) genera mundos cromáticos propios según la vertical: `architectural_b2b` (Porcelana/Cobalto Light-First), `cosmic_archetypal` (Observatorio Índigo Nocturno Dark-First / Efemérides), `design_system_atelier`, `editorial_manifesto` o `editorial_brand`.
- **Invariante `yong_shen`:** Los 15 shards prevalecen sobre el texto narrativo del brief al resolver elementos (`Water`, `Wood`, `Fire`, `Earth`, `Metal`).
- **Aislamiento Estricto:** Escribe exclusivamente en `--output-dir`. Nunca crea directorios fantasmas globales.

## Hard Rules (Directivas Obligatorias)
1. **Reglas Anti-Slop (`taste-skill` §4.2 + `impeccable`):** Prohibido el cliché AI azul neón (`#38b6ff`/`#080c14`), púrpuras neón (`#9333ea`) y beige cálido + latón (`#f5f1ea`/`#b08947`); croma acotado (`< 0.17`), 1 único acento consistente y composición separada Light/Dark.
2. **Tokens W3C DTCG 2025.10 + Tailwind v4:** Emite `$value` (`oklch`), `components`, `hex`, `p3`, `derivation_parameters` y `:root` alineado a `recommended_mode`.
3. **Auditoría Física Real:** Garantiza WCAG 2.2 AAA $\ge 7.0:1$ en texto, $\ge 4.5:1$ en botones sobre su fondo y APCA $|L_c| \ge 75.0$ en ambos modos.
4. **Previsualización & Self-Test:** Emite `chroma_preview.html` y se valida con `chroma-engine --test`.

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/chroma/references/usage.md) — Manual OKLCH, WCAG/APCA y `chroma-engine`.
- [`references/infra.md`](file:///var/www/zerops-astro-skills/chroma/references/infra.md) — Conversión P3/sRGB e inyección Tailwind CSS v4.
- [`assets/schemas/chroma_manifest.schema.json`](file:///var/www/zerops-astro-skills/chroma/assets/schemas/chroma_manifest.schema.json) — Esquema JSON.
- [`assets/templates/chroma_manifest_template.json`](file:///var/www/zerops-astro-skills/chroma/assets/templates/chroma_manifest_template.json) — Plantilla.
