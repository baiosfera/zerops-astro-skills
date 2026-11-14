---
name: oraculo
description: "Trigger: oraculo, fase 0, fase0, carta natal, astrologia. Ejecuta omni_engine.py para compilar el Data Lakehouse y Fase 0. Arquitecto de diagnóstico astrológico multidimensional SOTA con arquitectura federada."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "7.2" # pipeline engine version: "7.2"
---

# `oraculo` — Oráculo Maestro & Diagnóstico Multidimensional (v7.2)

## Activation Contract
Activar ante solicitudes de diagnóstico astrológico, numerológico, vocacional y puente semiótico a `orchesbrand`.

### Fast-Path Inmediato para Fase 0:
Ante cualquier solicitud de "fase 0", "fase0", "carta natal": la ausencia de `raw/` es normal. Ejecutar de inmediato:
`python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py <ruta>`
o mediante el wrapper directo:
`bash /var/www/.agents/skills/oraculo/scripts/fase0.sh <ruta>`
Compila atómicamente la totalidad de Fase 0 (12 shards físicos, 15 shards PostgreSQL, 9 feeds enciclopédicos Gold, y en Capa Platino los 4 artefactos en `raw/llm/`).

## Hard Rules (CoHaLo Positive Guidance)
- **Regla 1 (Arquitectura Federada):** Cada sub-skill astrológica mantiene su extractor canónico; Oráculo actúa como conductor asíncrono y sintetizador.
- **Regla 2 (Motor Matemático):** Python extrae cómputos exactos y literatura clásica verbatim sin textos inventados.
- **Regla 3 (Virtual Data Lakehouse Canon 12-15-9-4):**
  - **Bronze / Silver**: 12 shards JSON en `raw/json/dumps/` + 15 shards relacionales en `client_dumps_15_shards.json` y `manifest.json` (RFC 6901).
  - **Gold (`-c`)**: Ingesta dinámica de `raw/json/cache/` reconciliando Tropical Placidus/Campanus, Sideral Fagan-Bradley, Védico Lahiri D1-D60 y BaZi True Solar Time en 9 feeds verbatim.
  - **Runner (`brandbook_pipeline_runner.py`)**: Sintetiza en `/var/www/baiosfera/PROYECTOS/[MARCA]/dev/` (`coach_technical_sheet.md`, `fase0_author_psychology.md`, `astrobranding_[marca].md`, `brandbook_[marca].json`).
  - **Audit**: Micro-audits en `raw/json/audit/` y `extraction_health_audit.md` con estado HTTP y `X-Credits-Remaining`.
- **Regla 4 (Domificaciones & SSoT):** Mapeo en [`references/domifications_matrix.md`](file:///var/www/.agents/skills/oraculo/references/domifications_matrix.md); mantenimiento en `/var/www/zerops-astro-skills/oraculo/`.

## Decision Gates

| Requerimiento | Acción Determinista | Referencia |
|---|---|---|
| **Fase 0 (Data Lake & Dossier)** | Ejecutar `omni_engine.py --file <ruta>` | [`references/omni_engine.md`](file:///var/www/.agents/skills/oraculo/references/omni_engine.md) |
| **F1 (Occidental Tropical)** | Placidus / Whole Sign desde Shard 01 | [`references/phases.md`](file:///var/www/.agents/skills/oraculo/references/phases.md) |
| **F2 (Occidental Sideral)** | Fagan-Campanus desde Shard 02 (Mundoscopio & Cruz de Malta) | [`references/domifications_matrix.md`](file:///var/www/.agents/skills/oraculo/references/domifications_matrix.md) |
| **F3 (Védica Jyotish)** | Lahiri Whole Sign, D10 & Shadbala desde Shard 03 | [`references/phases.md`](file:///var/www/.agents/skills/oraculo/references/phases.md) |
| **F4 a F6 (Ontología)** | BaZi, Human Design y Tikkun desde Shards 04, 05 y 06 | [`references/phases.md`](file:///var/www/.agents/skills/oraculo/references/phases.md) |
| **F7 a F9 (Estrategia)** | Vocación, Timing y Mentoría desde Shards 07 a 10 | [`references/phases.md`](file:///var/www/.agents/skills/oraculo/references/phases.md) |
| **Sub-Oráculos (`diag-*`)** | Consumir variantes de `VirtualDataLake` o `manifest.json` | [`references/domifications_matrix.md`](file:///var/www/.agents/skills/oraculo/references/domifications_matrix.md) |
| **Validación Física** | Ejecutar validador físico (`exit code 0`) | `skills-suite-validate` |

## Commands

```bash
# Extracción federada y generación de Fase 0 y Data Lake (Fast-Path)
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py --file /ruta/a/consultante.txt

# Wrapper directo en un solo paso
bash /var/www/.agents/skills/oraculo/scripts/fase0.sh /ruta/a/consultante.txt

# Validación física de integridad
skills-suite-validate
```

## Resources
- **Matriz de Domificaciones & Ayanamsas**: [`references/domifications_matrix.md`](file:///var/www/.agents/skills/oraculo/references/domifications_matrix.md)
- **Motor Omni Engine & Data Lake**: [`references/omni_engine.md`](file:///var/www/.agents/skills/oraculo/references/omni_engine.md)
- **Taxonomía Tikkun**: [`references/tikkun_berg_taxonomy.md`](file:///var/www/.agents/skills/oraculo/references/tikkun_berg_taxonomy.md)
- **Especificación de Fases**: [`references/phases.md`](file:///var/www/.agents/skills/oraculo/references/phases.md)
- **Infraestructura & Sharding**: [`references/infra.md`](file:///var/www/.agents/skills/oraculo/references/infra.md)
- **Guía de APIs & MCPs**: [`references/usage.md`](file:///var/www/.agents/skills/oraculo/references/usage.md)
- **Validador Físico**: `skills-suite-validate`
