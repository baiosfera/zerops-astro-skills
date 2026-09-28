# 🏛️ Manual de Identidad Corporativa: [MARCA]
> **Versión Ejecutiva SOTA 2026** | Sistema de Diseño, Design Tokens W3C DTCG & Guía de Implementación

---

## 1. Fundamentos & Arquetipo de Marca
- **Nombre de Marca:** [MARCA]
- **Arquetipo Principal:** [ARQUETIPO_1]
- **Arquetipo Secundario:** [ARQUETIPO_2]
- **Propósito & UVP:** [RESUMEN_UVP]
- **Tono de Comunicación:** [TONO_DE_VOZ]

---

## 2. Identidad Vectorial (Isologo, Monograma & Favicon)

### Isologo Principal (Vectorial Puro)
```xml
[SVG_ISOLOGO_PRINCIPAL]
```

### Monograma Responsive
```xml
[SVG_MONOGRAMA]
```

### Favicon de Navegador (64x64 / 32x32)
```xml
[SVG_FAVICON]
```

*Directiva de Exportación:* Todos los SVGs incorporan `vector-effect="non-scaling-stroke"` y admiten rasterizado Retina HiDPI ($2\times/3\times$) o exportación vectorial a PDF mediante `svg2pdf.js`.

---

## 3. Sistema Tipográfico & Calibración Anti-CLS

| Capa Funcional | Token W3C DTCG | Familia Tipográfica | Peso / Ejes | Sourcing |
|---|---|---|---|---|
| **Logo / Monograma** | `typography.accent` | [FUENTE_ACENTO] | Black / 900 | Envato Elements / Local |
| **Slogan / Tagline** | `typography.display` | [FUENTE_PRIMARIA] | Regular / 500 | Envato Elements / Local |
| **H1 / Hero Títulos** | `typography.display` | [FUENTE_PRIMARIA] | 400 - 600 | Envato Elements / Local |
| **H2 / Subtítulos** | `typography.display` | [FUENTE_PRIMARIA] | The Jump (3x menor) | Envato Elements / Local |
| **Cuerpo / Párrafos** | `typography.body` | [FUENTE_SECUNDARIA] | Variable 400 | Google Fonts API v2 |
| **UI / Botones** | `typography.body` | [FUENTE_SECUNDARIA] | Medium 600 / Bold | Google Fonts API v2 |

### Fallback Métrico Anti-CLS (CLS = 0.00)
```css
@font-face {
  font-family: '[FUENTE_SECUNDARIA] Fallback';
  src: local('Arial');
  size-adjust: [SIZE_ADJUST]%;
  ascent-override: [ASCENT]%;
  descent-override: [DESCENT]%;
  line-gap-override: 0%;
}
```

---

## 4. Paleta Cromática OKLCH, Gamut P3 & Accesibilidad Dual

```css
@import "tailwindcss";

@theme {
  --color-brand-primary: [OKLCH_PRIMARY];
  --color-brand-secondary: [OKLCH_SECONDARY];
  --color-brand-accent: [OKLCH_ACCENT];
  --color-brand-bg: [OKLCH_BG];
  --color-brand-surface: [OKLCH_SURFACE];
  --color-brand-text: [OKLCH_TEXT];
  --color-brand-muted: [OKLCH_MUTED];
}
```

### Tabla de Auditoría de Contraste
- **WCAG 2.2 AAA (Piso Legal):** Texto Principal / Fondo = **[RATIO_TEXTO]:1** | Botón Primario / Fondo = **[RATIO_BOTON]:1** (PASS AAA).
- **APCA $L_c$ (Perceptual WCAG 3.0):** Cuerpo de Texto = **$L_c$ [LC_BODY]** ($\ge 75$ PASS) | Títulos Display = **$L_c$ [LC_HEADINGS]** ($\ge 60$ PASS).
- **Interpolación de Gradientes:** `linear-gradient(in oklch to right, var(--color-brand-primary), var(--color-brand-accent))`.

---

## 5. Motion Design & Micro-Audio Procedural (Zero MP3s)
- **FPS Target:** 60fps con Hydration Lock (`document.fonts.ready`) y `gsap.context()`.
- **Curva de Animación Hero:** `duration: 1.2s`, `ease: "power3.out"`.
- **Sintetizador Procedural ADSR:** Hover (Sine @ 520Hz, Attack 15ms), Click (Triangle @ 740Hz), Confirm (Triangle @ 880Hz).

---

## 6. Design Tokens SSoT (W3C DTCG `brandbook.json`)
El archivo `brandbook.json` en este directorio contiene la exportación formal en formato neutral W3C DTCG lista para ser consumida por Astro, Directus, PayloadCMS, Tailwind v4 y agentes de IA.
