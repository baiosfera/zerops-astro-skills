---
name: oraculo
description: "Trigger: oraculo, fase 0, fase0, carta natal, astrologia. Ejecuta omni_engine.py para compilar el Data Lakehouse y Fase 0. Arquitecto de diagnóstico astrológico multidimensional SOTA con arquitectura federada."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.7"
---

# `oraculo` — Oráculo Maestro & Diagnóstico Multidimensional (v4.7)

## Activation Contract
Activar ante solicitudes de diagnóstico astrológico, numerológico, vocacional y puente semiótico a `orchesbrand`.

### Fast-Path Inmediato para Fase 0:
Ante cualquier solicitud de "fase 0", "fase0", "carta natal": la ausencia de `raw/` es normal. Ejecutar de inmediato:
`python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py --file <ruta>`
o mediante el wrapper directo:
`bash /var/www/.agents/skills/oraculo/scripts/fase0.sh <ruta>`
Compila atómicamente la totalidad de Fase 0 (10 shards, feeds XML, Ficha Técnica y `fase0_author_psychology.md`).

## Hard Rules (CoHaLo Positive Guidance)
- **Regla 1 (Arquitectura Federada):** Cada sub-skill astrológica mantiene su extractor canónico y referencias oficiales. Oráculo actúa como conductor asíncrono y sintetizador.
- **Regla 2 (Motor Matemático):** Python extrae cómputos exactos y literatura clásica verbatim. Cero textos inventados en el motor.
- **Regla 3 (Virtual Data Lakehouse):**
  - **Bronze**: 10 Shards JSON en `raw/json/dumps/` sin directorios residuales.
  - **Silver**: `manifest.json` con punteros RFC 6901 y `VirtualDataLake`.
  - **Gold**: Feeds en `raw/feeds/`, incluyendo `feed_fase0_author_dossier.md` (XML).
  - **LLM**: `fase0_author_psychology.md` (>8 KB) y `coach_technical_sheet.md` (12 secciones en español).
- **Regla 4 (Auditoría de Cuotas):** `extraction_health_audit.md` registra estados HTTP reales y créditos en vivo (`X-Credits-Remaining`).
- **Regla 5 (Matriz de Domificaciones):** Mapeo canónico en [`references/domifications_matrix.md`](file:///var/www/.agents/skills/oraculo/references/domifications_matrix.md).
- **Regla 6 (Indivisibilidad SSoT):** Replicación exacta en `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/.agents/skills/oraculo/`.

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
| **Validación Física** | Ejecutar validador físico (`exit code 0`) | [`scripts/oraculo-validate.sh`](file:///var/www/.agents/skills/oraculo/scripts/oraculo-validate.sh) |

## Commands

```bash
# Extracción federada y generación de Fase 0 y Data Lake (Fast-Path)
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py --file /ruta/a/consultante.txt

# Wrapper directo en un solo paso
bash /var/www/.agents/skills/oraculo/scripts/fase0.sh /ruta/a/consultante.txt

# Validación física de integridad
bash /var/www/.agents/skills/oraculo/scripts/oraculo-validate.sh
```

## Resources
- **Matriz de Domificaciones & Ayanamsas**: [`references/domifications_matrix.md`](file:///var/www/.agents/skills/oraculo/references/domifications_matrix.md)
- **Motor Omni Engine & Data Lake**: [`references/omni_engine.md`](file:///var/www/.agents/skills/oraculo/references/omni_engine.md)
- **Taxonomía Tikkun**: [`references/tikkun_berg_taxonomy.md`](file:///var/www/.agents/skills/oraculo/references/tikkun_berg_taxonomy.md)
- **Especificación de Fases**: [`references/phases.md`](file:///var/www/.agents/skills/oraculo/references/phases.md)
- **Infraestructura & Sharding**: [`references/infra.md`](file:///var/www/.agents/skills/oraculo/references/infra.md)
- **Guía de APIs & MCPs**: [`references/usage.md`](file:///var/www/.agents/skills/oraculo/references/usage.md)
- **Validador Físico**: [`scripts/oraculo-validate.sh`](file:///var/www/.agents/skills/oraculo/scripts/oraculo-validate.sh)
