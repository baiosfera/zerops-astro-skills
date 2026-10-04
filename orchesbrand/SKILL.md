---
name: orchesbrand
description: "Trigger: orchesbrand, orquestar branding, pipeline de marca, identidad visual, suite de branding, live sync. Orquesta el pipeline integral de marca desde Oraculo/Diagnostico hasta el Brandbook."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.2"
---

# Orchesbrand — Orquestador de Pipeline de Identidad Visual Dual-RAG

## Activation Contract
Activar para ejecutar el pipeline completo de branding o coordinar la generación de sus 5 fases especializadas ($F1 \rightarrow F5$), garantizando la transferencia de selecciones definitivas entre etapas, validación de schemas y sincronización en tiempo real con `brandview`. Opera en modo desacoplado directo o interactivo paso a paso.

## Input Rule (Desacople SSoT & Modos de Ejecución)
- **Fuente Primaria Indivisible:** Consume herméticamente `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/astrobranding_[MARCA].md` (compilado por Oráculo en Fase 0).
- **Modo Desacoplado Directo:** Cada fase especializada (`fontgen`, `symbol`, `chroma`, `kinetic`, `brandbook`) puede ejecutarse de forma autónoma e ingerir directamente desde el SSoT sin bloqueos en cascada.
- **Modo Interactivo Paso a Paso (Brandview):** Permite disparar fases individuales a demanda desde la UI web, permitiendo al usuario seleccionar variantes y mutar manifiestos interactivamente.

## Hard Rules (Directivas Obligatorias)
- **1. Handoff Hermético (SSoT Indivisible):** Ingiere `astrobranding_[MARCA].md` sin tocar JSONs crudos ni esperar sub-diagnósticos. La suite de diseño opera 100% desacoplada de la data astronómica cruda.
- **2. Cascada Flexible & No Bloqueante:**
  $$\text{astrobranding} \xrightarrow{} \text{fontgen (F1)} \rightleftarrows \text{symbol (F2 B/N)} \rightleftarrows \text{chroma (F3 3-Eco)} \rightleftarrows \text{kinetic (F4 3-Anim)} \rightleftarrows \text{brandbook (F5 DTCG)}$$
  La secuencia secuencial es opcional y no bloqueante; cada skill puede consumir directamente el SSoT y enriquecer los manifiestos existentes.
- **3. Puntos de Control y Circuit Breakers:** Al ejecutar fases supervisadas:
  - Verificar existencia del artefacto en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/`.
  - Conformidad estricta con el JSON Schema correspondiente en `assets/schemas/`.
  - En caso de error de validación, reintentar con diagnóstico específico (máximo 2 intentos).
- **4. Respeto a Contratos de Fase:** Asegurar monocromía estricta en `symbol` (F2), 3 ecosistemas OKLCH en `chroma` (F3), 3 presets 60fps en `kinetic` (F4) y tokens W3C DTCG en `brandbook` (F5).
- **5. Sincronización SSoT Bidireccional:** Todo artefacto debe sincronizarse entre `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/` y `/mnt/localstorage/DIAG/[MARCA]/`.

## References
- `references/pipeline.md` — Topología del pipeline desacoplado, dependencias y sincronización RFC 6902.
- `references/usage.md` — Manual de invocación Antigravity, modo interactivo y control de estado.
- `assets/schemas/pipeline_state.schema.json` — Esquema del estado de orquestación.
