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
Activar cuando se requiera ejecutar el pipeline completo de branding o coordinar la generación en cascada de sus 5 fases especializadas ($F1 \rightarrow F5$), garantizando la transferencia de selecciones definitivas entre etapas, validación de schemas y sincronización en tiempo real con `brandview`.

## Hard Rules (Directivas Obligatorias)
- **1. Handoff Hermético (SSoT Indivisible):** Consume herméticamente `astrobranding_[MARCA].md` (compilado por Oráculo en Fase 0 a partir de los 12 Shards) como SSoT sin tocar JSONs crudos ni esperar la ejecución de sub-diagnósticos. La suite de diseño opera 100% desacoplada de la data astronómica cruda.
- **2. Secuencia en Cascada Determinista:**
  $$\text{astrobranding} \xrightarrow{} \text{fontgen (F1)} \xrightarrow{\text{Fuentes Definitivas}} \text{symbol (F2 B/N)} \xrightarrow{\text{Vector Definitivo}} \text{chroma (F3 3-Eco)} \xrightarrow{\text{Colores Definitivos}} \text{kinetic (F4 3-Anim)} \xrightarrow{\text{Motion Definitivo}} \text{brandbook (F5 DTCG)}$$
- **3. Puntos de Control y Circuit Breakers:** Antes de desbloquear la fase $N+1$, verificar:
  - Existencia del archivo JSON en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/`.
  - Conformidad estricta con el JSON Schema correspondiente en `assets/schemas/`.
  - En caso de error de validación, reintentar con diagnóstico específico (máximo 2 intentos).
- **4. Respeto al Contrato Monocromático de Fase 2:** Asegurar que `symbol` no incruste colores antes de `chroma`.
- **5. Respeto al Contrato de 3 Ecosistemas en Fase 3:** Asegurar que `chroma` emita 3 propuestas completas en OKLCH con validación WCAG/APCA.
- **6. Respeto al Contrato de 3 Opciones de Animación en Fase 4:** Asegurar que `kinetic` emita 3 opciones de animación sobre el SVG definitivo.
- **7. Sincronización SSoT Bidireccional:** Todo artefacto debe sincronizarse entre `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/` y `/mnt/baiostorage/DIAG/[MARCA]/`.

## References
- `references/pipeline.md` — Topología del pipeline, dependencias y sincronización RFC 6902.
- `assets/schemas/pipeline_state.schema.json` — Esquema del estado de orquestación.
