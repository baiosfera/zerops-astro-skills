# Brandbook: Infraestructura, Persistencia SSoT y Pipeline de Exportación (v2.0)

Este documento define la infraestructura de persistencia, integración con gateways de IA y exportación multi-formato para el compilador de identidad corporativa en Zerops.

---

## 1. Topología de Persistencia y Espejo SSoT

Toda ejecución de `brandbook` opera bajo el principio de indivisibilidad entre el volumen persistente de Zerops y Google Drive:

- **Runtime Activo (Zerops Local Storage):**
  `/var/www/localstorage/${PROJECT_NAME}/dev/`
  - `brandbook_superfull_${PROJECT_NAME}.json`: Manifiesto W3C DTCG maestro.
  - `brandbook-theme.css`: Bloque `@theme` para Tailwind CSS v4.
  - `system_prompt.md`: Proyección de personalidad para agentes conversacionales.

- **Almacenamiento SSoT Indivisible (Google Drive):**
  - `/var/www/baiosfera/PROYECTOS/${PROJECT_NAME}/dev/`
  - `/var/www/baiosfera/ASTROLOGÍA/DIAG/${PROJECT_NAME}/brandbook.json` (retrocompatibilidad)

---

## 2. Inferencia y Conectividad con Bifrost AI Gateway

La generación semántica de tokens y proyecciones de voz se procesa a través de la red privada interna de Zerops:

- **Endpoint:** `http://bifrost:8080/v1/chat/completions`
- **Headers Requeridos:**
  - `Content-Type: application/json`
  - `Authorization: Bearer ${BIFROST_VIRTUAL_KEY}`
  - `x-tier: production` (enrutamiento directo a modelos de alta fidelidad como DeepSeek V3/V4)
- **Parámetros de Ejecución:** `temperature: 0.2`, `response_format: { type: "json_object" }`, `timeout: 60s`.

---

## 3. Motor Headless de Renderizado y Exportación Gráfica

Para la exportación desasistida de manuales en PDF y assets rasterizados de alta densidad:

- **Motor:** Chromium headless ejecutado mediante Playwright o Puppeteer en Incus LXC.
- **Perfiles de Exportación:**
  - **PDF de Marca:** Generación a 300 DPI con sangrado de 3mm (`printBackground: true`, `format: "A4"`).
  - **PNG Retina:** Captura a doble y triple densidad de píxeles (`deviceScaleFactor: 2` y `3`).
  - **SVG Vectorial:** Optimización mediante `svgo` con eliminación de metadatos de edición e inyección de viewBox canónico.

---

## 4. Validación de Esquema W3C DTCG

El manifiesto generado se valida contra el esquema de Design Tokens Community Group:

```bash
bun test --filter brandbook-schema
```
