# Orchesbrand: Especificación del Pipeline de Identidad Visual & Live-Sync (SOTA 2026)

Este documento formaliza el flujo secuencial determinista, las dependencias de datos entre fases, los puntos de control (checkpoints) y la arquitectura de sincronización en tiempo real con la WebApp `brandgeneration` (Bun/Node.js).

---

## 1. Topología del Pipeline Lineal & Modo Dual

### Modo A: Ingestión desde Oráculo (Fase 10)
$$\text{Oráculo} \xrightarrow{\text{astrobranding}} \text{fontgen} \xrightarrow{\text{font\\_manifest}} \text{symbol} \xrightarrow{\text{symbol\\_manifest}} \text{chroma} \xrightarrow{\text{chroma\\_manifest}} \text{kinetic} \xrightarrow{\text{kinetic\\_manifest}} \text{brandbook}$$

### Modo B: Ingestión Standalone (WebApp / Directo)
$$\text{brand\\_input.json} \xrightarrow{} \text{fontgen} \xrightarrow{} \text{symbol} \xrightarrow{} \text{chroma} \xrightarrow{} \text{kinetic} \xrightarrow{} \text{brandbook}$$

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

---

## 2. Matriz de Contratos de Entrada y Salida por Fase

| Fase | Skill | Contrato de Entrada Requerido | Contrato de Salida Emitido | Ubicación SSoT |
|---|---|---|---|---|
| **0** | **Pre-Flight** | `astrobranding_[MARCA].md` o `brand_input.json` | Directorio inicializado | `.../DIAG/[MARCA]/` |
| **1** | `fontgen` | Directrices de marca | `fontgen_[MARCA].md` + `font_manifest.json` | `.../DIAG/[MARCA]/` |
| **2** | `symbol` | `font_manifest.json` + Arquetipo | `symbol_manifest.json` | `.../DIAG/[MARCA]/` |
| **3** | `chroma` | `symbol_manifest.json` + Arquetipo | `chroma_manifest.json` | `.../DIAG/[MARCA]/` |
| **4** | `kinetic` | `font_manifest` + `symbol_manifest` + `chroma_manifest` | `kinetic_manifest.json` | `.../DIAG/[MARCA]/` |
| **5** | `brandbook` | Manifiestos completos de Fases 1 a 4 | `brandbook_manifest.md` + `brandbook.json` + `index.html` | `.../DIAG/[MARCA]/` |

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
