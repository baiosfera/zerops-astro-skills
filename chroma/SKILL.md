---
name: chroma
description: "Trigger: chroma, paleta de color, oklch, wcag aaa, apca, psicologia del color, tokens de color, contraste de marca, 3 ecosistemas. Disena y valida 3 ecosistemas de color en OKLCH y ratios WCAG AAA/APCA."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.0"
---

# Chroma — Motor OKLCH, 3 Ecosistemas Dark/Light & Auditoría WCAG/APCA (v3.0)

## Activation Contract
Activar para diseñar o regenerar la arquitectura cromática de una marca o vertical mediante `chroma-engine`, produciendo **3 Ecosistemas Cromáticos Completos** (modos **Dark** y **Light** en cada uno) con matemática física OKLCH $\to$ Display P3 / sRGB y validación real WCAG 2.2 AAA + APCA.

## Input Rule (Desacople SSoT & Aislamiento)
- **CLI Canónico:** `chroma-engine --brand <BRAND> --brief <astrobranding_<brand>.md> --output-dir <workspace>/brand`.
- **Ingestión Directa SSoT:** Extrae paletas `§3` directamente desde `astrobranding_<brand>.md` (y sintetiza automáticamente el modo Light complementario WCAG AAA para ecosistemas que solo traigan Dark Mode) o calcula la rueda polar solar de 360° cuando no hay tabla explícita.
- **Aislamiento de Carpetas:** Escribe exclusivamente en `--output-dir`. Nunca crea directorios globales fantasmas en `/mnt/localstorage/` ni en Drive.

## Hard Rules (Directivas Obligatorias)
1. **3 Ecosistemas Cromáticos Contextuales Completos:** Cada propuesta deriva de la semiótica y brief real de la marca (prohibido hardcodear nombres o hexes fijos de otra marca).
2. **Dark & Light Mode en los 3 Ecosistemas:** Cada ecosistema define 7 tokens semánticos (`primary`, `secondary`, `accent`, `background`, `surface`, `text_primary`, `text_muted`) tanto en `dark` como en `light`.
3. **Tokens W3C DTCG 2025.10 + Tailwind v4:** Emite `$value` (`oklch(L C H)`), `$type: "color"`, `components`, `hex`, `p3`, bloque `@theme` y variables `:root` / `[data-theme="light"]`.
4. **Auditoría Física Real (Sin Valores Hardcodeados):** Calcula luminancia relativa y APCA $L_c$ reales garantizando WCAG 2.2 AAA $\ge 7.0:1$ y APCA $|L_c| \ge 75.0$ en texto sobre fondo en Dark y Light Mode.
5. **Previsualización Visual & Self-Test:** Emite `chroma_preview.html` junto a `chroma_manifest.json` y se valida con `chroma-engine --test`.

## Output Contract
- `<output_dir>/chroma_manifest.json`
- `<output_dir>/chroma_preview.html`

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/chroma/references/usage.md) — Manual OKLCH, WCAG/APCA y `chroma-engine`.
- [`references/infra.md`](file:///var/www/zerops-astro-skills/chroma/references/infra.md) — Conversión P3/sRGB e inyección Tailwind CSS v4.
- [`assets/schemas/chroma_manifest.schema.json`](file:///var/www/zerops-astro-skills/chroma/assets/schemas/chroma_manifest.schema.json) — Esquema JSON Draft 2020-12.
- [`assets/templates/chroma_manifest_template.json`](file:///var/www/zerops-astro-skills/chroma/assets/templates/chroma_manifest_template.json) — Plantilla con 3 ecosistemas cromáticos.
