# Chroma: Infraestructura, Espacio OKLCH y Pipeline de Contraste (v2.0)

Este documento define la infraestructura matemática, conversión a espacios de color P3/sRGB, generación de temas para Tailwind CSS v4 y contratos de persistencia para el motor cromático.

---

## 1. Motor Matemático OKLCH & Auditoría de Contraste

Chroma opera en el espacio perceptual uniforme OKLCH para garantizar transiciones de luminosidad uniformes y predecibles:

- **Espacio Canónico:** `oklch(L C H)`
  - $L$ (Luminosidad): $0.0$ a $1.0$ (o $0\%$ a $100\%$)
  - $C$ (Croma): $0.0$ a $0.4$
  - $H$ (Matiz / Hue): $0^\circ$ a $360^\circ$

- **Métricas de Conformidad Dual:**
  - **WCAG 2.2 AAA:** Ratio matemático $\ge 7:1$ para texto regular (`text_primary` sobre `background` y `surface`).
  - **APCA (Advanced Perceptual Contrast Algorithm):** $L_c \ge 75$ para texto continuo y $L_c \ge 60$ para títulos y displays.

---

## 2. Inyección Downstream en Tailwind CSS v4 & CSS Variables

El manifiesto cromático exporta bloques nativos para Tailwind CSS v4 mediante directivas `@theme`:

```css
@theme {
  --color-brand-primary: var(--brand-primary);
  --color-brand-secondary: var(--brand-secondary);
  --color-brand-accent: var(--brand-accent);
  --color-brand-bg: var(--brand-bg);
  --color-brand-surface: var(--brand-surface);
  --color-brand-text: var(--brand-text);
  --color-brand-muted: var(--brand-muted);
}

:root {
  --brand-primary: oklch(0.55 0.18 280);
  --brand-secondary: oklch(0.70 0.12 250);
  --brand-accent: oklch(0.65 0.22 340);
  --brand-bg: oklch(0.98 0.01 280);
  --brand-surface: oklch(0.95 0.02 280);
  --brand-text: oklch(0.15 0.03 280);
  --brand-muted: oklch(0.45 0.04 280);
}

[data-theme="dark"] {
  --brand-bg: oklch(0.12 0.02 280);
  --brand-surface: oklch(0.18 0.03 280);
  --brand-text: oklch(0.95 0.01 280);
  --brand-muted: oklch(0.65 0.03 280);
}
```

---

## 3. Contratos de Persistencia SSoT

- **Manifiesto Cromático SSoT:** `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/chroma_manifest.json`
- **Espejo en Runtime Zerops:** `/var/www/localstorage/[MARCA]/dev/chroma_manifest.json`
- **Validación de Integridad:** Validado contra `assets/schemas/chroma_manifest.schema.json`.
