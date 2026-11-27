# Chroma: Infraestructura OKLCH, W3C DTCG 2025.10 y CSS Color Level 5 (v8.0)

Este documento especifica el motor matemático `OKLCH`, las primitivas CSS Color Level 5 y los contratos SSoT de `chroma_engine.py v8.0`.

---

## 1. Motor Matemático `OKLCH`, CSS Color 4 Gamut Mapping y Auditoría Dual

- **Conversión Exacta + Gamut Mapping:** `sRGB Hex <-> Linear sRGB <-> OKLab <-> OKLCH` con reducción binaria de croma `gamut_map_oklch` y proyección `Display P3` (`color(display-p3 r g b)`).
- **Auditoría Dual + Acromática:**
  - **WCAG 2.2:** `>= 7.0:1` cuerpo, `>= 4.5:1` `on_primary`/`on_accent`/muted, `>= 3.0:1` gráfico UI (`primary` vs `background`).
  - **APCA (`0.0.98G-4g`):** `|Lc| >= 75` cuerpo, `>= 60` titulares, `>= 45` UI.
  - **Acromático (`C = 0`):** Delta de luminancia `>= 0.55` y monotonicidad Z en modo oscuro (`bg < surface <= surface_elevated <= border_subtle`).

---

## 2. Salida CSS Color Level 5 para `astro-web`

```css
:root,
[data-brand="marca"] {
  --brand-radius-card: 8px;
  --brand-radius-control: 4px;
  --elevation-card: none;
  --card-border: 1px solid color-mix(in oklch, var(--brand-muted) 20%, transparent);
  color-scheme: light;
  --brand-primary: oklch(0.4175 0.1573 25.1);
  --brand-primary-hover: oklch(from var(--brand-primary) calc(l + -0.06) c h);
  --brand-on-primary: oklch(0.982 0.006 25.1);
  --brand-bg: oklch(0.972 0.007 84.6);
  --brand-surface: oklch(0.941 0.011 84.6);
  --brand-surface-elevated: oklch(0.980 0.006 84.6);
  --brand-border: oklch(0.842 0.006 84.6);
  --brand-text: oklch(0.184 0.003 84.6);
  --brand-muted: oklch(0.436 0.011 84.6);
}
```

---

## 3. Contratos de Persistencia y Validación SSoT

- **Salida Aislada (`--output-dir`):** `chroma_manifest.json` (incluyendo `dtcg_tokens`, `brandfont_export` y `css_integration`) y `chroma_preview.html`.
- **Integración Downstream:** Ingerido por `orchesbrand v4.5` (`brandbook.json` + `brandbook-theme.css`), `brand-studio` (`DESIGN.md`), `brandfont` (`brandfont_export`) y `astro-web`.
- **Validación:** `python3 -B -m py_compile /var/www/zerops-astrobranding/scripts/chroma_engine.py && chroma-engine --test`.
