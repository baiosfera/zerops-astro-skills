---
name: oraculo
description: "Trigger: oraculo, fase 0, fase0, carta natal, astrologia. Ejecuta omni_engine.py para compilar el Data Lakehouse y Fase 0. Arquitecto de diagnóstico astrológico multidimensional SOTA con arquitectura federada."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "7.3"
---

# `oraculo` — Oráculo Maestro & Diagnóstico Multidimensional (v7.3)

## Activation Contract
Activar ante solicitudes de diagnóstico astrológico, numerológico, vocacional y compilación de Fase 0 (Data Lakehouse).

### Fast-Path Inmediato para Fase 0
Ante solicitudes de "fase 0", "fase0" o "carta natal": la ausencia de `raw/` es normal. Ejecutar de inmediato:
```bash
python3 /var/www/zerops-astro-skills/oraculo/scripts/omni_engine.py <ruta_consultante>
# o mediante el wrapper directo:
bash /var/www/zerops-astro-skills/oraculo/scripts/fase0.sh <ruta_consultante>
```
Compila atómicamente la totalidad de Fase 0 bajo el Canon 12-15-9-4 (12 shards Bronze, 15 relacionales Silver, 9 feeds Gold y 4 artefactos Platinum).

## Core Directives & Canon 12-15-9-4
- **Arquitectura Federada**: Cada sub-skill astrológica mantiene su extractor y referencias oficiales; Oráculo actúa como conductor asíncrono y sintetizador.
- **Motor Matemático Invariable**: Extracción de cómputos exactos y literatura clásica verbatim. Cero textos inventados en el motor.
- **Canon Virtual Data Lakehouse**:
  - *Bronze*: 12 Shards Físicos JSON en `raw/json/dumps/` (`shard_01` a `shard_12`).
  - *Silver*: 15 Shards Relacionales en `client_dumps_15_shards.json` para PostgreSQL y `manifest.json`.
  - *Gold*: Universal dynamic cache crawler ingesta `raw/json/cache/`, reconcilia Tropical Placidus, Tropical Campanus, Sideral Fagan-Bradley, Védico Lahiri D1-D60 y BaZi True Solar Time.
  - *Platinum*: Síntesis de artefactos en `/var/www/baiosfera/PROYECTOS/[MARCA]/dev/` (`coach_technical_sheet.md`, `fase0_author_psychology.md`, `astrobranding_[marca].md`, `brandbook_[marca].json`).
- **Zero-Waste Single-Pass**: Fase 0 extrae el 100% en un único pase concurrente. Prohibido re-consumir APIs externas de pago post-Fase 0; las fases posteriores leen exclusivamente de disco.

## Decision Gates & References
- **Fase 0 & Data Lake**: [`omni_engine.md`](file:///var/www/zerops-astro-skills/oraculo/references/omni_engine.md) — Extracción federada, crawler de caché y síntesis.
- **Domificaciones & Ayanamsas**: [`domifications_matrix.md`](file:///var/www/zerops-astro-skills/oraculo/references/domifications_matrix.md) — Placidus, Campanus, Whole Sign y Fagan-Bradley.
- **Especificación de Fases (F1 a F11)**: [`phases.md`](file:///var/www/zerops-astro-skills/oraculo/references/phases.md) — Tropical, Sideral, Védica, BaZi, Human Design y Tikkun.
- **APIs & MCPs Usage**: [`usage.md`](file:///var/www/zerops-astro-skills/oraculo/references/usage.md) — Endpoints REST, rate limits y token-buckets.
- **Infraestructura & Sharding**: [`infra.md`](file:///var/www/zerops-astro-skills/oraculo/references/infra.md) — Variables de entorno, storage topology y CoHaLo harness.
- **Validación Física**: [`oraculo-validate.sh``skills-suite-validate` — Verificador físico de integridad de shards (exit code 0).

## Output Contract
Data Lakehouse estructurado en `raw/`, 4 artefactos Platinum en `raw/llm/` y sincronización con SSoT.
