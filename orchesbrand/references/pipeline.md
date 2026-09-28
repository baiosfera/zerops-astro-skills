# Orchesbrand: Especificación del Pipeline de Identidad Visual & Live-Sync (SOTA 2026)

Este documento formaliza el flujo secuencial determinista, las dependencias de datos entre fases, los puntos de control (checkpoints) y la arquitectura de sincronización en tiempo real con la WebApp `brandgeneration` (Bun/Node.js).

---

## 1. Topología del Pipeline Lineal & Modo Dual

### Modo A: Ingestión Hermética desde Oráculo (Fase 0 SSoT Desacoplada)
Fase 0 de Oráculo compila herméticamente el artefacto ultra-denso `astrobranding_[MARCA].md` sintetizando los 12 Shards astronómicos del VirtualDataLake (incluyendo salud MTC y curva Neijing, especificaciones de microinteracciones a 60fps para kinetic, tokens W3C DTCG para chroma/brandbook, y ciudades de poder ACG para anclaje de marca). Este artefacto actúa como SSoT canónico único: **la fuente primaria de verdad es `astrobranding_[MARCA].md`; la cascada entre fases es opcional y no bloqueante**. La suite de diseño especializada (`fontgen`, `symbol`, `chroma`, `kinetic`, `brandbook`) trabaja 100% desacoplada de los JSONs astronómicos crudos y sin requerir la ejecución previa secuencial de las otras fases:

$$\text{Oráculo (F0 SSoT)} \xrightarrow{\text{astrobranding\_[MARCA].md}} \begin{cases} \text{fontgen (F1: 3 Ecosistemas Tipográficos & 6 Capas)} \\ \text{symbol (F2: 3 Isologos, 3 Monogramas, 3 Favicons B/N)} \\ \text{chroma (F3: 3 Ecosistemas OKLCH & WCAG AAA/APCA)} \\ \text{kinetic (F4: 3 Presets 60fps & Web Audio ADSR)} \\ \text{brandbook (F5: Compilador DTCG & Manual)} \end{cases}$$

### Modo B: Ingestión Standalone / Interactiva (Brandview)
$$\text{brand\_input.json / SSoT} \xrightarrow{} \text{Fase Seleccionada a Demanda} \xrightarrow{} \text{Manifiesto Específico Actualizado}$$

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ORCHESBRAND FLEXIBLE DISPATCHER                       │
│                     SSoT: astrobranding_[MARCA].md                          │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
  [Fase 1: FONTGEN]             [Fase 2: SYMBOL]              [Fase 3: CHROMA]
  3 Ecosistemas Tipográficos    Isologos & Favicons SVG B/N   OKLCH, P3, APCA
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

### 1.1 Especificación del Modo Desacoplado Hermético (Oráculo F0 -> Suite de Diseño)
- **Compilación en Fase 0:** Oráculo procesa los 12 Shards del VirtualDataLake (`shard_01` a `shard_12`) y genera `astrobranding_[MARCA].md` conteniendo:
  - **MTC & Ritmos Biológicos (Shard 11):** Integración de biotipos, meridianos horarios y curva Neijing para tono, pausas cognitivas y tiempos de interacción.
  - **Dinámica Cinética & Audio (Shard 08 + Shard 10):** Especificaciones de aceleración física a 60fps (GSAP) y envolventes ADSR (Web Audio API) para microinteracciones de marca.
  - **Tokens de Color W3C DTCG (Shard 01 + Shard 02):** Valores OKLCH, ratios APCA / WCAG 2.2 AAA y paletas tri-ecosistémicas.
  - **Ciudades de Poder ACG (Shard 09):** Coordenadas geográficas angulares de máxima influencia para activación y eventos de marca.
- **Desacoplamiento Estricto:** La suite de diseño NUNCA analiza JSONs crudos (`omni_dump_mega.json`), no realiza consultas REST astronómicas ni espera la ejecución de los sub-diagnósticos (`diag-a-psy`, `diag-b-voc`, `diag-c-mkt`, `diag-d-leg`, `diag-e-geo`).
- **Cascada Opcional y No Bloqueante:** Cada skill puede ejecutarse de forma aislada consumiendo directamente `astrobranding_[MARCA].md`. Si existen manifiestos previos en disco, se integran armónicamente; de lo contrario, la skill genera su artefacto autónomamente.
- **Máxima Densidad Informativa:** Todos los insumos visuales, tipográficos, simbólicos, cinéticos y arquitectónicos requeridos por F1–F5 están pre-digeridos en `astrobranding_[MARCA].md`.

---

## 2. Matriz de Contratos de Entrada y Salida por Fase

| Fase | Skill | Contrato de Entrada Requerido | Contrato de Salida Emitido | Ubicación SSoT |
|---|---|---|---|---|
| **0** | **Pre-Flight (Oráculo F0)** | 12 Shards astronómicos compilados en `astrobranding_[MARCA].md` | Directorio inicializado y SSoT hermético | `.../DIAG/[MARCA]/` |
| **1** | `fontgen` | Directrices desde `astrobranding_[MARCA].md` | `fontgen_[MARCA].md` + `font_manifest.json` | `.../DIAG/[MARCA]/` |
| **2** | `symbol` | `astrobranding_[MARCA].md` (opcional: `font_manifest.json`) | `symbol_manifest.json` (B/N puro) | `.../DIAG/[MARCA]/` |
| **3** | `chroma` | `astrobranding_[MARCA].md` (opcional: `symbol_manifest.json`) | `chroma_manifest.json` (3 ecosistemas) | `.../DIAG/[MARCA]/` |
| **4** | `kinetic` | `astrobranding_[MARCA].md` (opcional: manifiestos F2/F3) | `kinetic_manifest.json` (3 presets 60fps) | `.../DIAG/[MARCA]/` |
| **5** | `brandbook` | `astrobranding_[MARCA].md` o consolidación de manifiestos disponibles | `brandbook_manifest.md` + `brandbook.json` + `index.html` | `.../DIAG/[MARCA]/` |


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
