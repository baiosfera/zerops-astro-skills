# Chroma: Manual de Color SOTA, 3 Ecosistemas OKLCH y Validación Dual WCAG 2.2 / APCA

Este documento formaliza la metodología para la generación de **3 Ecosistemas Cromáticos Completos**, la teoría psicológica del color arquetípico y la auditoría de accesibilidad legal y perceptual.

---

## 1. Por qué 3 Ecosistemas Cromáticos Completos

Una marca de alto nivel requiere explorar 3 direcciones cromáticas autónomas para definir su personalidad rectora:
1. **Ecosistema 1 (Quiet Luxury / Autoridad Sobria):** Tonos grafito, obsidiana y oro champagne o platino.
2. **Ecosistema 2 (High-Performance / Energía Cinética):** Negros de carbón mineral con acentos esmeralda, cian o cobalto de alto impacto.
3. **Ecosistema 3 (Bio-Sensual / Calidez Orgánica):** Marfiles cálidos, terracotas aterciopeladas y acentos cobre.

Cada ecosistema debe formularse con sus modos **Dark** y **Light** completos (7 tokens semánticos cada uno).

---

## 2. Espacio Perceptual OKLCH y Gamut Display P3

El espacio **OKLCH** ($L$ = Lightness, $C$ = Chroma, $H$ = Hue) asegura que las gradaciones lumínicas no distorsionen la tonalidad percibida por el ojo humano:
- **Consistencia Perceptual:** $L=0.85$ produce idéntico nivel de brillo en cualquier ángulo de tono $H$.
- **Display P3:** Representación fidedigna en pantallas modernas de alta gama.
- **Interpolación `in oklch`:** Erradica zonas muertas grisáceas en transiciones de color.

---

## 3. Matriz de Auditoría Dual: WCAG 2.2 AAA vs APCA

Cada ecosistema debe ser auditado formalmente:
- **WCAG 2.2 AAA (Luminancia Relativa):**
  - Texto Normal vs Fondo: Ratio $\ge 7.0:1$.
  - Botones y Controles: Ratio $\ge 3.0:1$.
- **APCA (Accessible Perceptual Contrast Algorithm / WCAG 3.0):**
  - Texto Body: $L_c \ge 75.0$.
  - Titulares Display: $L_c \ge 60.0$.
  - Componentes UI: $L_c \ge 45.0$.

---

## 4. Teñido Reactivo del Isologo de Fase 2

Los tokens de color se conectan directamente a los IDs semánticos del SVG monocromático de la Fase 2:
- `--brand-primary` $\rightarrow$ tiñe `#symbol-core` y `#symbol-monogram`.
- `--brand-secondary` $\rightarrow$ tiñe `#symbol-orbit-1` y `#symbol-orbit-2`.
- `--brand-accent` $\rightarrow$ tiñe `#symbol-geometry-star` y estados `:hover`.

---

## 5. Arquitectura Desacoplada & Ingestión Directa SSoT

La fuente primaria y canónica de verdad es `astrobranding_[MARCA].md` compilado por Oráculo en Fase 0 a partir de los shards del VirtualDataLake.
- **Desacople de Cascada:** `chroma` formula los 3 ecosistemas cromáticos completos, la auditoría dual WCAG 2.2 AAA / APCA y los tokens DTCG directamente a partir de las directrices de color y psicología del SSoT, sin requerir que `fontgen` o `symbol` se hayan ejecutado.
- **Cascada No Bloqueante:** La cascada entre fases es opcional y no bloqueante. Si `symbol_manifest.json` existe, mapea sobre sus trazos; de lo contrario mapea sobre los IDs semánticos estándar.
- **Contratos de Salida Garantizados:** Emite `chroma_manifest.json` (3 ecosistemas OKLCH, Dark/Light Mode, WCAG AAA / APCA y `selected_ecosystem_id`), el bloque `@theme` para Tailwind CSS v4 y variables CSS `:root` consumibles por `brandview`.

