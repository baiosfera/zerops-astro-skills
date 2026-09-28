# Orchesbrand: Especificación del Pipeline de Identidad Visual & Live-Sync (SOTA 2026)

Este documento formaliza el flujo secuencial determinista, las dependencias de datos entre fases, los puntos de control (checkpoints) y la arquitectura de sincronización en tiempo real con la WebApp `brandgeneration` (Bun/Node.js).

---

## 1. Topología del Pipeline Lineal & Modo Dual

### Modo A: Ingestión Hermética desde Oráculo (Fase 0 SSoT)
Fase 0 de Oráculo compila herméticamente el artefacto ultra-denso `astrobranding_[MARCA].md` sintetizando los 12 Shards astronómicos del VirtualDataLake (incluyendo salud MTC y curva Neijing, especificaciones de microinteracciones a 60fps para kinetic, tokens W3C DTCG para chroma/brandbook, y ciudades de poder ACG para anclaje de marca). Este artefacto actúa como SSoT canónico único: la suite de diseño especializada (`fontgen`, `symbol`, `chroma`, `kinetic`, `brandbook`) trabaja 100% desacoplada de los JSONs astronómicos crudos y sin requerir la ejecución previa ni asíncrona de los sub-diagnósticos satélite.

$$\text{Oráculo (F0: 12 Shards)} \xrightarrow{\text{astrobranding\_[MARCA].md (Hermético)}} \text{fontgen (F1)} \xrightarrow{\text{font\_manifest}} \text{symbol (F2)} \xrightarrow{\text{symbol\_manifest}} \text{chroma (F3)} \xrightarrow{\text{chroma\_manifest}} \text{kinetic (F4)} \xrightarrow{\text{kinetic\_manifest}} \text{brandbook (F5)}$$

### Modo B: Ingestión Standalone (WebApp / Directo)
$$\text{brand\_input.json} \xrightarrow{} \text{fontgen} \xrightarrow{} \text{symbol} \xrightarrow{} \text{chroma} \xrightarrow{} \text{kinetic} \xrightarrow{} \text{brandbook}$$

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            ORCHESBRAND DISPATCHER                           │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
  [Fase 1: FONTGEN]             [Fase 2: SYMBOL]              [Fase 3: CHROMA]
  3 Ecosistemas Tipográficos    Isologos & Favicons SVG       OKLCH, P3, APCA
  Google Fonts v2 Multi-Eje     vector-effect non-scaling     & WCAG 2.2 AAA
        │                              │                              │
        └──────────────────────────────┼──────────────────────────────┘
                                       │
        ┌──────────────────────────────┴──────────────────────────────┐
        ▼                                                             ▼
  [Fase 4: KINETIC]                                             [Fase 5: BRANDBOOK]
  GSAP 60fps & Web Audio ADSR                                   Compilador DTCG brandbook.json,
  Hydration Lock & View Transitions                             Manual .md & Showcase index.html
```

### 1.1 Especificación del Modo A Hermético (Oráculo F0 -> Suite de Diseño)
- **Compilación en Fase 0:** Oráculo procesa los 12 Shards del VirtualDataLake (`shard_01` a `shard_12`) y genera `astrobranding_[MARCA].md` conteniendo:
  - **MTC & Ritmos Biológicos (Shard 11):** Integración de biotipos, meridianos horarios y curva Neijing para tono, pausas cognitivas y tiempos de interacción.
  - **Dinámica Cinética & Audio (Shard 08 + Shard 10):** Especificaciones de aceleración física a 60fps (GSAP) y envolventes ADSR (Web Audio API) para microinteracciones de marca.
  - **Tokens de Color W3C DTCG (Shard 01 + Shard 02):** Valores OKLCH, ratios APCA / WCAG 2.2 AAA y paletas tri-ecosistémicas.
  - **Ciudades de Poder ACG (Shard 09):** Coordenadas geográficas angulares de máxima influencia para activación y eventos de marca.
- **Desacoplamiento Estricto:** La suite de diseño NUNCA analiza JSONs crudos (`omni_dump_mega.json`), no realiza consultas REST astronómicas ni espera la ejecución de los sub-diagnósticos (`diag-a-psy`, `diag-b-voc`, `diag-c-mkt`, `diag-d-leg`, `diag-e-geo`).
- **Máxima Densidad Informativa:** Todos los insumos visuales, tipográficos, simbólicos, cinéticos y arquitectónicos requeridos por F1–F5 están pre-digeridos en `astrobranding_[MARCA].md`.

---

## 2. Matriz de Contratos de Entrada y Salida por Fase

| Fase | Skill | Contrato de Entrada Requerido | Contrato de Salida Emitido | Ubicación SSoT |
|---|---|---|---|---|
| **0** | **Pre-Flight (Oráculo F0)** | 12 Shards astronómicos compilados en `astrobranding_[MARCA].md` (o `brand_input.json` en Modo B) | Directorio inicializado y SSoT hermético | `.../DIAG/[MARCA]/` |
| **1** | `fontgen` | Directrices de marca desde `astrobranding_[MARCA].md` | `fontgen_[MARCA].md` + `font_manifest.json` | `.../DIAG/[MARCA]/` |
| **2** | `symbol` | `font_manifest.json` + Arquetipo / Simbología sagrada | `symbol_manifest.json` | `.../DIAG/[MARCA]/` |
| **3** | `chroma` | `symbol_manifest.json` + Arquetipo / 3 Ecosistemas | `chroma_manifest.json` | `.../DIAG/[MARCA]/` |
| **4** | `kinetic` | `font_manifest` + `symbol_manifest` + `chroma_manifest` + Spec 60fps | `kinetic_manifest.json` | `.../DIAG/[MARCA]/` |
| **5** | `brandbook` | Manifiestos completos de Fases 1 a 4 + Tokens W3C DTCG | `brandbook_manifest.md` + `brandbook.json` + `index.html` | `.../DIAG/[MARCA]/` |

---

## 3. Protocolo de Sensor Validation & Circuit Breaker

Antes de desbloquear la Fase $N+1$, el orquestador valida:
1. **Existencia en Disco:** El archivo JSON generado existe en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/`.
2. **Conformidad con JSON Schema:** El archivo cumple estrictamente su schema Draft 2020-12 en `assets/schemas/`.
3. **Circuit Breaker:** Si la validación falla, se re-invoca al subagente indicando el campo defectuoso (máximo 2 reintentos). Al segundo fallo persistente, se detiene el pipeline emitiendo un reporte forense.

---

## 4. Arquitectura de Sincronización WebApp (Bun/Node.js + RFC 6902)

Para la WebApp `brandgeneration`:
- **Live-Sync:** Servidor Bun observando `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/*.json`.
- **Deltas JSON Patch (RFC 6902):** Emisión de parches atómicos por WebSockets al mover sliders en la UI.
- **Escrituras Atómicas sin Corrupción:** `Temp File (.tmp) -> fsync -> Atomic Rename` para garantizar integridad SSoT.
