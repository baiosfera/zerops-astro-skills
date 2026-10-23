# Orchesbrand: Infraestructura, Sincronización SSoT y Conectividad Brandview (v2.0)

Este documento define la infraestructura de coordinación, persistencia bidireccional y comunicación en caliente para el pipeline de branding.

---

## 1. Topología del Pipeline y Aislamiento de Procesos

Orchesbrand coordina la ejecución secuencial o paralela de las 5 micro-habilidades especializadas:

```
                  ┌─────────────────────────────────────────┐
                  │ SSoT Primario: astrobranding_[MARCA].md │
                  └────────────────────┬────────────────────┘
                                       │
        ┌──────────────┬───────────────┼───────────────┬──────────────┐
        ▼              ▼               ▼               ▼              ▼
  [F1 fontgen]   [F2 symbol]     [F3 chroma]     [F4 kinetic]   [F5 brandbook]
        │              │               │               │              │
        └──────────────┴───────────────┼───────────────┴──────────────┘
                                       │
                                       ▼
                  ┌─────────────────────────────────────────┐
                  │ Manifiesto Unificado: brandbook.json    │
                  │ (W3C Design Tokens Community Group)     │
                  └────────────────────┬────────────────────┘
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
        [Zerops Local Storage]                   [Google Drive SSoT]
     /var/www/localstorage/[MARCA]/dev/       /var/www/baiosfera/PROYECTOS/[MARCA]/
```

---

## 2. Sincronización SSoT Bidireccional y Zero-Lock

- **Directorio de Trabajo Local:** `/var/www/localstorage/[MARCA]/dev/`
- **Repositorio Global Indestructible:** `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/` y `/var/www/baiosfera/PROYECTOS/[MARCA]/dev/`
- **Herramienta de Sincronización:** `zcp-sync [MARCA]`
  Permite propagar los artefactos generados en local hacia Drive de forma no bloqueante ("Zero-Lock").

---

## 3. Conectividad en Tiempo Real con Brandview Studio

- **Transporte:** WebSockets / SSE sobre red privada interna de Zerops.
- **Formato de Mensajes:** Parches RFC 6902 (JSON Patch) para mutaciones parciales de variantes seleccionadas sin invalidar el manifiesto completo.
- **Validación de Esquema:** Todo parche se valida contra `assets/schemas/pipeline_state.schema.json` y `assets/schemas/brandview_state.schema.json`.
