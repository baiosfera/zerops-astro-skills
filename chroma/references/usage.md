# Chroma: Art-Direction-First Spec, Modos CLI y Auditoría (v8.0)

Este manual documenta el flujo en dos etapas de `chroma_engine.py v8.0` bajo Playbook 19 (`v2.0.0`) y Radix Colors Step-9 para `orchesbrand v4.5`, `brandfont` y `astro-web`.

---

## 1. Arquitectura en Dos Etapas (Dirección de Arte -> Compilador OKLCH)

El motor **no inventa "arquetipos enlatados"** para imponer paletas idénticas entre marcas. En cada proyecto —incluso en contenedores ZCP aislados sin acceso a otros clientes— se diseña un `chroma_spec.json` a medida y luego se compila matemáticamente:

```json
{
  "selected_ecosystem_id": "eco_1_oxblood_alabaster",
  "vertical_archetype": "editorial_brand",
  "surface_geometry": { "radius_card": "8px", "radius_control": "4px", "elevation_style": "border_1px" },
  "ecosystems": [
    {
      "id": "eco_1_oxblood_alabaster",
      "name": "Alabastro & Carmesí Sangre de Buey",
      "recommended_mode": "light",
      "color_strategy": "Committed",
      "concept": "Autoridad editorial sin cian genérico ni pasteles apagados.",
      "light": {
        "background": "#f8f6f2", "surface": "#efece6", "primary": "#8c151c",
        "accent": "#1e293b", "secondary": "#554f49", "text_primary": "#141312", "text_muted": "#56514b"
      },
      "dark": {
        "background": "#111216", "surface": "#181a20", "primary": "#c92a34",
        "accent": "#d9b99b", "secondary": "#8c8982", "text_primary": "#edeae4", "text_muted": "#a7a49d"
      }
    }
  ]
}
```

Si solo se define `"light"` o solo `"dark"`, `_synthesize_opposite_mode` deriva el modo complementario preservando pigmentos **Step-9** en botones oscuros (texto `#fafaf9` nítido) o modo monocromo platino.

---

## 2. Prioridad de Entradas y Opt-In Estricto de Oráculo

1. **`--spec chroma_spec.json`** (o `chroma_spec.json` detectado en `--output-dir` en `--mode auto`): **ruta primaria**.
2. **`--palette-json <palettes.json>`**: lista de paletas curadas.
3. **`--seed-hex "#HEX"`** (opcional `--bg-hex`, `--accent-hex`): expansión matemática anclada en marca.
4. **`--mode brief --brief <astrobranding_*.md>`**: **opt-in explícito** de tabla §3 de Oráculo (requiere pasar `--brief` / `--shards` explícitamente; nunca rastrea `DIAG/` en silencio).
5. **Fallback limpio PB19:** síntesis editorial sin pasteles ni cianes plantilla.

---

## 3. Reglas Duras de Contraste, Gamut y Anti-Slop

- **Gamut Mapping CSS Color 4 (`gamut_map_oklch`):** Búsqueda binaria sobre croma `C` preservando Luminancia (`L`) y Tono (`H`) antes de cuantizar sRGB e inyectar `color(display-p3 ...)`.
- **Stepping Oscuro Step-9 + Zero Washout:** `_harden_mode_tokens` mantiene los colores ricos (`WCAG >= 3.0:1` contra fondo oscuro, `on_primary >= 4.5:1`) sin lavarlos a pastel `L=0.76`.
- **Auditoría Dual + Acromática (`C = 0`):** Cuerpo `>= 7.0:1` (`|Lc| >= 75`), UI/Controles `>= 4.5:1`, delta luminancia acromático `>= 0.55` y monotonicidad `Z0 < Z1 <= Z2 <= Z3`.

---

## 4. Verificación Real & Captura Headless

```bash
chroma-engine --brand <BRAND> --spec <ws>/brand/chroma_spec.json --output-dir <ws>/brand
chroma-engine --test
google-chrome --headless --no-sandbox --disable-gpu --window-size=1440,1200 \
  --virtual-time-budget=2500 --screenshot=/tmp/chroma_check.png \
  "file://<ws>/brand/chroma_preview.html"
```
