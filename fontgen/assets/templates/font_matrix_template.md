# ♟️ Dirección de Arte Tipográfica SOTA: [MARCA]
> **Resumen de Arquitectura:** [Resumen analítico de 3-4 líneas cruzando la psicología arquetípica de Oráculo y las leyes de Gestalt para la arquitectura visual].

---

### Ecosistema 1: [Nombre Conceptual del Ecosistema]
- **Arquetipo Rector:** [Arquetipo / Personalidad de Marca]
- **Justificación Gestalt:** [Explicación de armonía, peso visual y contraste entre las 3 familias].

#### Matriz de 3 Design Tokens (W3C DTCG)
1. **Token Primario (Autoridad / Display):** `[Familia 1]` — *Fuente:* [Envato Elements con ID real / Local] — *Uso:* H1, H2, Hero, Slogan.
2. **Token Secundario (UI & Lectura Continua):** `[Familia 2]` — *Fuente:* [Google Fonts Variable] — *Uso:* Párrafos, UI, Botones, Tablas.
3. **Token de Acento (Brand Voice / Logo):** `[Familia 3]` — *Fuente:* [Envato Elements con ID real / Local] — *Uso:* Isologo, Monograma, Citas destacadas.

#### Herencia Funcional de 6 Capas
- **1. Logo / Monograma:** Instancia `Token de Acento` *(Peso: Black / Display 900)*.
- **2. Slogan / Tagline:** Instancia `Token Primario` *(Contraste armónico frente al logo decorativo)*.
- **3. H1 / Títulos Hero:** Instancia `Token Primario` *(Peso: 400-600)*.
- **4. H2 / Subtítulos:** Instancia `Token Primario` *(Regla "The Jump": tamaño 3x menor que H1)*.
- **5. Cuerpo / Párrafos:** Instancia `Token Secundario` *(Peso: Regular 400, Line-height: 1.5 - 1.6)*.
- **6. UI / Botones (Labels):** Instancia `Token Secundario` *(Inversión de peso: Medium 600 o Bold 700)*.

#### Implementación Web & Calibración Anti-CLS (CLS = 0.00)
```html
<!-- CDN Google Fonts API v2 Multi-Eje -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=[FAMILIA_2]:[EJES_VARIABLES]&display=swap" rel="stylesheet">
```

```css
/* Fallback Métrico para evitar saltos de maquetación */
@font-face {
  font-family: '[FAMILIA_2] Fallback';
  src: local('Arial');
  size-adjust: [SIZE_ADJUST]%;
  ascent-override: [ASCENT]%;
  descent-override: [DESCENT]%;
  line-gap-override: 0%;
}

:root {
  --font-display: '[FAMILIA_1]', serif;
  --font-body: '[FAMILIA_2]', '[FAMILIA_2] Fallback', system-ui, sans-serif;
  --font-accent: '[FAMILIA_3]', cursive;
}
```

#### Presets Sugeridos para Workbench (webapp.html)
- **Tamaño Display:** `[PX]` | **Letter Spacing:** `[EM]` | **Line Height:** `[LH]`
- **Ligaduras OpenType:** [Activadas / Desactivadas] | **Transformación:** [Uppercase / None]

---

### Ecosistema 2: [Nombre Conceptual 2]
[Misma estructura detallada que Ecosistema 1]

---

### Ecosistema 3: [Nombre Conceptual 3]
[Misma estructura detallada que Ecosistema 1]
