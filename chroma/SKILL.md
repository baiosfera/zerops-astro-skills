---
name: chroma
description: "Trigger: chroma, paleta de color, oklch, wcag aaa, apca, psicologia del color, tokens de color, contraste de marca, 3 ecosistemas. Disena y valida 3 ecosistemas de color en OKLCH y ratios WCAG AAA/APCA."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.2"
---

# Chroma — Motor de Color SOTA, 3 Ecosistemas OKLCH & Auditoría Dual Dual-RAG

## Activation Contract
Activar para diseñar la arquitectura cromática de una marca, formulando **3 Ecosistemas Cromáticos Completos**, auditados bajo WCAG 2.2 AAA y APCA en espacio perceptual OKLCH, con exportación Tailwind CSS v4 `@theme` y variables CSS. Opera desacoplado con ingestión directa desde `astrobranding_[MARCA].md` o en modo interactivo.

## Input Rule (Desacople SSoT)
- **Ingestión Directa Primaria:** Ingiere directamente desde `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/astrobranding_[MARCA].md` (compilado por Oráculo en Fase 0) sin requerir que fases previas se hayan ejecutado o bloqueen el pipeline. Si `symbol_manifest.json` existe, mapea sobre sus vectores; de lo contrario formula la paleta sobre los IDs semánticos estándar.
- **Modo Standalone / Manual:** Acepta especificaciones directas del usuario o `brand_input.json`.

## Hard Rules (Directivas Obligatorias)
- **1. Formulación de 3 Ecosistemas Cromáticos Completos:** Generar 3 propuestas conceptualmente diferenciadas (ej: *Quiet Luxury*, *High Performance*, *Bio-Sensual*).
- **2. Arquitectura Bipolar (Dark & Light Mode por Ecosistema):** Cada ecosistema define Dark y Light Mode con 7 tokens semánticos:
  - `primary`: Dominante de marca y monograma.
  - `secondary`: Apoyo y elipses secundarias.
  - `accent`: Alto impacto para micro-interacciones.
  - `background`: Lienzo base de la interfaz.
  - `surface`: Superficie elevada de tarjetas y módulos.
  - `text_primary`: Texto principal de máximo contraste.
  - `text_muted`: Texto secundario y metadatos.
- **3. Espacio OKLCH & Tokens W3C DTCG:** Cada token define `$value`, `$type: "color"`, `{ lightness, chroma, hue }`, `hex` y `p3`. Emite código dev Tailwind v4 `@theme` y variables CSS `:root`.
- **4. Auditoría Dual Estricta (WCAG 2.2 AAA + APCA):**
  - WCAG 2.2 AAA: Ratio $\ge 7.0:1$ para texto regular sobre background.
  - APCA: $L_c \ge 75.0$ para texto Body y $\ge 60.0$ para display.
- **5. Mapeo a IDs Semánticos:** Mapear `--brand-primary`, `--brand-secondary`, `--brand-accent` hacia `#symbol-core`, `#symbol-orbit-1`, `#symbol-monogram`.
- **6. Contrato de Selección:** Incluir `selected_ecosystem_id` (ej: `"eco-dark-obsidian"`).
- **7. Salida Determinista SSoT:** Escribir en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/chroma_manifest.json` validado contra `chroma_manifest.schema.json`.

## Output Contract
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/chroma_manifest.json`

## References
- `references/usage.md` — Manual de 3 ecosistemas OKLCH, psicología del color, desacople SSoT y validación WCAG/APCA.
- `assets/schemas/chroma_manifest.schema.json` — Esquema JSON Draft 2020-12.
- `assets/templates/chroma_manifest_template.json` — Plantilla con 3 ecosistemas cromáticos.
