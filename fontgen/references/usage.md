# Fontgen: Manual de Sourcing Híbrido, Art Direction y Workbench Tipográfico

Este documento especifica la metodología de emparejamiento tipográfico, leyes de Gestalt, el protocolo de búsqueda con verificación de enlaces reales y la integración con el Workbench interactivo (`webapp.html`).

---

## 1. Arquitectura de los 3 Design Tokens (W3C DTCG)

El sistema tipográfico se organiza estrictamente en 3 capas de diseño complementarias:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       MATRIZ DE 3 DESIGN TOKENS                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. TOKEN PRIMARIO (Display & Autoridad)                                      │
│    - Fuente: Exclusiva de Envato Elements / Local Upload.                    │
│    - Uso: Encabezados H1, H2, Slogan / Tagline, Títulos Hero.               │
│    - Razón: Otorga exclusividad, diferenciación y alta gama estética.       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2. TOKEN SECUNDARIO (Workhorse & Lectura de Fricción Cero)                   │
│    - Fuente: Exclusiva de Google Fonts Variable por CDN.                     │
│    - Uso: Cuerpo de texto, párrafos, tablas, labels y componentes UI.       │
│    - Razón: Legibilidad extrema en pantallas pequeñas, carga optimizada.     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 3. TOKEN DE ACENTO (Brand Voice & Personalidad Gráfica)                      │
│    - Fuente: Exclusiva de Envato Elements / Script / Monograma.              │
│    - Uso: Isologos, citas destacadas, iniciales y monogramas de marca.       │
│    - Razón: Impacto visual y pregnancia nemotécnica.                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Protocolo de Búsqueda Vanguardia Dual-Sort en Envato & Previsualización SVG (`envato-font-preview`)

Para garantizar fuentes actualizadas, vanguardistas y previsualizables antes de descargar archivos `.woff2`:
- **Sourcing Dual-Sort (`fontgen-engine` v4.1):** Consulta **`elements.envato.com/fonts/<término>/<categoría>/sort-by-latest`** y **`sort-by-popular`** (`window.INITIAL_HYDRATION_DATA`) más fallback a `app.envato.com/search`. Puntúa novedad (`isNew`) y oficios de fundición (`inktrap`, `grotesk`, `neo`, `variable`, `mono`, `editorial`), filtra novedades kitsch (`retro`, `90s`, `western`, `pixel`, `horror`, `wedding`, `calligraphy`), diferencia el perfil por vertical (`architectural_b2b`, `cosmic_archetypal`, `design_system_atelier`, `editorial_manifesto`), emite 3 `shortlist_candidates` alternativos y genera `web_ready_bridge` para Astro 5 (sin `Fraunces` ni `Inter`).
- **Previsualización SVG Multipaleta (`envato-font-preview` v3.2):**
  ```bash
  envato-font-preview --from-manifest <ws>/brand/font_manifest.json --chroma <ws>/brand/chroma_manifest.json --texts "MARCA,SUBTITULO" --include-shortlist --out <ws>/brand/previews
  ```
  Incluye reintentos automáticos ante `502`/`503`/`429`, botón rápido `"Probar Tildes ES"` y renderizado opcional de alternativas de `shortlist_candidates`.
- **Catálogo Curado Offline:** Si no hay red (`--no-live`), recurre a `ENVATO_VERIFIED_CATALOG` con UUIDs verificados en `app.envato.com/fonts/{uuid}`.

### Reglas de Validación de Enlaces:
- **Envato Elements:** Formato canónico `https://elements.envato.com/[slug]-[ALFANUMERICO-7]` (HTTP 200 OK obligatorio)
- **Google Fonts:** Formato canónico `https://fonts.google.com/specimen/[Nombre+De+Fuente]` (API v2 Variable)

---

## 3. Matriz de Herencia Funcional de 6 Capas (Leyes de Gestalt)

Cada ecosistema debe definir explícitamente cómo heredan las 6 capas funcionales:

1. **Logo / Marca:** Instancia `Token de Acento` (peso Black o Display 900).
2. **Slogan / Tagline:** Instancia `Token Primario`. *Regla:* Si el logo es muy decorativo, el slogan DEBE usar el token primario para generar contraste armónico.
3. **H1 / Títulos Hero:** Instancia `Token Primario` (Peso 400-600 máx).
4. **H2 / Subtítulos:** Instancia `Token Primario` (Aplica regla de "The Jump": tamaño 3x menor que H1).
5. **Cuerpo / Párrafos:** Instancia `Token Secundario` (Peso Regular 400, line-height 1.5 a 1.6).
6. **UI / Botones (Labels):** Instancia `Token Secundario` (Inversión de peso: Medium 600 o Bold 700).

---

## 4. Integración Bidireccional con el Workbench (`webapp.html`)

El manifiesto JSON (`font_manifest.json`) exporta e importa los presets de los controles interactivos:
- `letter_spacing_em`: Rango `-0.2` a `1.0` em.
- `line_height`: Rango `0.5` a `3.0`.
- `text_transform`: `uppercase`, `lowercase`, `capitalize`, `none`.
- `ligatures_enabled`: Activa `font-feature-settings: "liga" 1, "dlig" 1`.
- `transform_x` / `transform_y` / `rotation_deg` / `mirror_enabled`: Coordenadas de transformación visual en lienzo.

---

## 5. Arquitectura Desacoplada & Ingestión Directa SSoT

La fuente primaria y canónica de verdad es `astrobranding_[MARCA].md` compilado por Oráculo en Fase 0 a partir de los shards del VirtualDataLake.
- **Desacople Total de Cascada:** `fontgen` no requiere que ninguna otra fase del pipeline se haya ejecutado previamente. Puede invocarse de manera autónoma o interactiva desde `brandview`.
- **Cascada No Bloqueante:** La cascada entre fases es opcional y no bloqueante.
- **Contratos de Salida Garantizados:** Emite `font_manifest.json` (3 ecosistemas, 6 capas funcionales y `selected_ecosystem_id`), `fontgen_[MARCA].md` y código dev (`@font-face` y Google Fonts v2) para `brandview`.

