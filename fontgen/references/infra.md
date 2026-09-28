# Fontgen: Infraestructura, APIs y Suministro Tipográfico SOTA (2026)

Este documento define la infraestructura de conectividad, APIs de catálogo, CDNs y provisión tipográfica de alta fidelidad.

---

## 1. APIs de Búsqueda y Validación en Vivo (Tier 1)

- **Exa Search Engine (`web_search_exa`):**
  - Rastreo en tiempo real de fuentes en `site:elements.envato.com` y `site:fonts.google.com`.
  - Verificación de enlaces canónicos reales con ID alfanumérico para evitar alucinaciones.

- **Google Fonts API v2 (Multi-Eje Variable):**
  - **Estructura de URL SOTA:**
    Los ejes de variación deben ordenarse alfabéticamente (`ital`, `opsz`, `slnt`, `wdth`, `wght`) y especificar tuplas ordenadas:
    ```html
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Flex:ital,opsz,wght@0,8..144,100..900;1,8..144,100..900&family=Space+Grotesk:wght@300..700&display=swap" rel="stylesheet">
    ```

---

## 2. Prevención de Cumulative Layout Shift (CLS = 0.00)

Para anular el salto de maquetación cuando la fuente web carga sobre la fuente del sistema (`font-display: swap`), se calculan e inyectan los descriptores métricos en el `@font-face` local:

```css
@font-face {
  font-family: 'Space Grotesk Fallback';
  src: local('Arial');
  size-adjust: 102.5%;
  ascent-override: 95%;
  descent-override: 22%;
  line-gap-override: 0%;
}
```

---

## 3. Contratos de Persistencia SSoT

Toda ejecución de `fontgen` escribe exclusivamente en:
- **Reporte Markdown:** `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/fontgen_[MARCA].md`
- **Manifiesto JSON W3C DTCG:** `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/font_manifest.json`
