---
name: chroma
description: "Trigger: chroma, paleta de color, oklch, wcag aaa, apca, psicologia del color, tokens de color, contraste de marca, 3 ecosistemas. Disena y valida 3 ecosistemas de color en OKLCH y ratios WCAG AAA/APCA."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# Chroma — Motor de Color SOTA, 3 Ecosistemas OKLCH & Auditoría Dual Dual-RAG

## Activation Contract
Activar cuando se requiera diseñar la arquitectura cromática de una marca, formulando **3 Ecosistemas Cromáticos Completos**, auditados bajo WCAG 2.2 AAA y APCA en espacio perceptual OKLCH, e inyectándolos sobre el SVG monocromático de Fase 2.

## Hard Rules (Directivas Obligatorias)
- **1. Formulación de 3 Ecosistemas Cromáticos Completos:** Generar obligatoriamente 3 propuestas cromáticas completas y conceptualmente diferenciadas (ej: *Quiet Luxury*, *High Performance*, *Bio-Sensual Sacred Glamour*).
- **2. Arquitectura Bipolar (Dark Mode & Light Mode por Ecosistema):** Cada uno de los 3 ecosistemas debe contener su paleta Dark Mode y Light Mode completas con 7 tokens semánticos:
  - `primary`: Color dominante de marca y monograma.
  - `secondary`: Color de apoyo y elipses secundarias.
  - `accent`: Color de alto impacto para micro-interacciones.
  - `background`: Lienzo base de la interfaz.
  - `surface`: Superficie elevada de tarjetas y módulos.
  - `text_primary`: Texto principal de máximo contraste.
  - `text_muted`: Texto secundario y metadatos.
- **3. Espacio Perceptual OKLCH & Tokens W3C DTCG:** Cada token debe definir `$value`, `$type: "color"`, componentes `{ lightness, chroma, hue }`, código `hex` y `p3`.
- **4. Auditoría Dual Estricta (WCAG 2.2 AAA + APCA):**
  - WCAG 2.2 AAA: Ratio $\ge 7.0:1$ para texto regular sobre background.
  - APCA: $L_c \ge 75.0$ para texto Body y $\ge 60.0$ para display.
- **5. Inyección Directa sobre el Vector de Fase 2:** Mapear las variables `--brand-primary`, `--brand-secondary`, `--brand-accent` para teñir los nodos semánticos del SVG monocromático de la Fase 2 (`#symbol-core`, `#symbol-orbit-1`, `#symbol-monogram`).
- **6. Contrato de Selección:** Incluir `selected_ecosystem_id` (ej: `"eco-dark-obsidian"`) para transferir la elección del usuario a Fase 4 y 5.
- **7. Salida Determinista SSoT:** Escribir en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/chroma_manifest.json` y validar contra `chroma_manifest.schema.json`.

## Decision Gates

| Condición | Acción |
|---|---|
| Contraste WCAG AAA < 7.0:1 | Ajustar la componente `lightness` en OKLCH hasta alcanzar $\ge 7.0:1$ sin alterar el `hue` |
| APCA Body $L_c < 75.0$ | Aumentar la polaridad luminosa entre `text_primary` y `background` |
| Pantallas Retina / P3 | Emitir valores `color(display-p3 r g b)` para gamas amplias |

## Execution Steps
1. Leer el arquetipo rector y el `symbol_manifest.json` generado en Fase 2.
2. Formular los 3 Ecosistemas Cromáticos Completos en OKLCH con justificación psicológica.
3. Auditar cada ecosistema con algoritmos de luminosidad relativa WCAG 2.2 y contraste perceptual APCA.
4. Generar el bloque CSS `@theme` para Tailwind CSS v4 e inyección `:root`.
5. Emitir `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/chroma_manifest.json` validado con `chroma_manifest.schema.json`.

## Output Contract
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/chroma_manifest.json`

## References
- `references/usage.md` — Manual de 3 ecosistemas OKLCH, psicología del color y validación dual WCAG/APCA.
- `assets/schemas/chroma_manifest.schema.json` — Esquema JSON Draft 2020-12.
- `assets/templates/chroma_manifest_template.json` — Plantilla con 3 ecosistemas cromáticos.
