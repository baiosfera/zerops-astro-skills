---
name: chroma
description: "Trigger: chroma, paleta de color, oklch, wcag aaa, apca, psicologia del color, tokens de color, contraste de marca, 3 ecosistemas. Disena y valida 3 ecosistemas de color en OKLCH y ratios WCAG AAA/APCA."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.0"
---

# Chroma — Motor OKLCH Multi-Eje Oráculo + Vertical & Anti-Slop Editorial (v4.0)

## Activation Contract
Activar para diseñar o regenerar la arquitectura cromática mediante `chroma-engine` (`v4.0`), produciendo **3 Ecosistemas Cromáticos Radicados en Mundos Visuales Distintos** (modos **Dark** y **Light** compuestos intencionalmente en cada uno) desde los 15 shards crudos de Oráculo (`client_dumps_15_shards.json`), contexto de vertical (`verticals/<v>.json`) y reglas anti-slop de `design-taste-frontend` + `impeccable`.

## Input Rule (Multi-Eje Real & Aislamiento)
- **CLI Canónico:** `chroma-engine --brand <BRAND> --shards <client_dumps_15_shards.json> --vertical-json <vertical.json> --brief <astrobranding_<brand>.md> --output-dir <workspace>/brand`.
- **Síntesis Multi-Eje vs. Brief Estático:** Por defecto (`--mode auto`), cuando existen `--shards` o `--vertical-json` sintetiza 3 ecosistemas verdaderamente diferenciados (Claro Editorial, Carbón Arquitectónico y Basalto Mineral), reservando `--mode brief` para copiar tablas `§3` estáticas únicamente cuando se solicite literalidad.
- **Aislamiento de Carpetas:** Escribe exclusivamente en `--output-dir`. Nunca crea directorios fantasmas globales.

## Hard Rules (Directivas Obligatorias)
1. **Reglas Anti-Slop (`taste-skill` §4.2 + `impeccable`):** Prohibido el cliché AI azul neón sobre azul oscuro (`#38b6ff` sobre `#080c14`), prohibido beige cálido + latón (`#f5f1ea` / `#b08947`), croma acotado (`< 0.17`), máximo 1 acento interactivo consistente por página y composición separada para Light y Dark.
2. **3 Mundos Visuales Distintos:** Separación cromática real ($\ge 35^\circ$ entre propuestas cromáticas) combinando eje Tropical/Yong Shen (Eco 1 `recommended_mode: light`), Shadbala/Nakshatra Lord/BaZi Mes (Eco 2 `recommended_mode: dark`) y BaZi Day Master/Venus Sideral (Eco 3 dual).
3. **Tokens W3C DTCG 2025.10 + Tailwind v4:** Emite `$value` (`oklch(L C H)`), `$type: "color"`, `components`, `hex`, `p3`, `derivation_parameters`, `:root` ajustado al `recommended_mode` y `[data-theme="..."]`.
4. **Auditoría Física Real:** Garantiza WCAG 2.2 AAA $\ge 7.0:1$ en texto, $\ge 4.5:1$ en botones primarios sobre su fondo y APCA $|L_c| \ge 75.0$ en ambos modos.
5. **Previsualización Visual & Self-Test:** Emite `chroma_preview.html` con tarjetas comparativas y se valida con `chroma-engine --test`.

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/chroma/references/usage.md) — Manual OKLCH, WCAG/APCA y `chroma-engine`.
- [`references/infra.md`](file:///var/www/zerops-astro-skills/chroma/references/infra.md) — Conversión P3/sRGB e inyección Tailwind CSS v4.
- [`assets/schemas/chroma_manifest.schema.json`](file:///var/www/zerops-astro-skills/chroma/assets/schemas/chroma_manifest.schema.json) — Esquema JSON.
- [`assets/templates/chroma_manifest_template.json`](file:///var/www/zerops-astro-skills/chroma/assets/templates/chroma_manifest_template.json) — Plantilla.
