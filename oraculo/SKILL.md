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
Activar ante solicitudes de diagnóstico astrológico, numerológico, vocacional y puente semiótico a `orchesbrand` / `brand-studio`.

### Fast-Path Fase 0
Ante "fase 0", "fase0" o "carta natal" (la ausencia de `raw/` es normal), ejecutar de inmediato:
`python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py <ruta>` o `bash /var/www/.agents/skills/oraculo/scripts/fase0.sh <ruta>`.
Compila atómicamente Fase 0 (12 shards físicos, 15 shards PostgreSQL, 9 feeds Gold y 4 artefactos Platino en `raw/llm/`).

## Hard Rules (CoHaLo Positive Guidance)
- **Regla 1 (Arquitectura Federada):** Cada sub-skill astrológica mantiene su extractor; Oráculo actúa como conductor asíncrono y sintetizador.
- **Regla 2 (Motor Matemático):** Python extrae cómputos exactos y literatura clásica verbatim sin textos inventados.
- **Regla 3 (Data Lakehouse 12-15-9-4):**
  - **Bronze / Silver:** 12 shards en `raw/json/dumps/` + 15 shards en `client_dumps_15_shards.json` y `manifest.json` (RFC 6901).
  - **Gold (`-c`):** Reconcilia Tropical Placidus/Campanus, Sideral Fagan-Bradley, Védico Lahiri D1-D60 y BaZi True Solar Time en 9 feeds verbatim.
  - **Runner (`brandbook_pipeline_runner.py`):** Sintetiza en `/var/www/baiosfera/PROYECTOS/[MARCA]/dev/` (`coach_technical_sheet.md`, `fase0_author_psychology.md`, `astrobranding_[marca].md`, `brandbook_[marca].json`).
  - **Audit:** Micro-audits en `raw/json/audit/` (`X-Credits-Remaining`).
- **Regla 4 (Domificaciones & SSoT):** Mapeo en [`references/domifications_matrix.md`](file:///var/www/.agents/skills/oraculo/references/domifications_matrix.md); SSoT en `/var/www/zerops-astro-skills/oraculo/`.
- **Regla 5 (Puente al Copy & Avatar `Casa 7 Descendente`):** Cuando Oráculo esté activo, `brand-studio` y `ad-campaign-factory` consumen la **Tríada del Avatar (`Casa 7 Descendente`, `Casa 8`, `Casa 11`) + `Venus`** desde `astrobranding_*.md` para moldear la psicología y voz del comprador.

## Decision Gates

| Requerimiento | Acción Determinista | Referencia |
|---|---|---|
| **Fase 0 (Data Lake)** | `omni_engine.py --file <ruta>` | [`references/omni_engine.md`](file:///var/www/.agents/skills/oraculo/references/omni_engine.md) |
| **F1 (Tropical)** | Placidus / Whole Sign (Shard 01) | [`references/phases.md`](file:///var/www/.agents/skills/oraculo/references/phases.md) |
| **F2 (Sideral)** | Fagan-Campanus (Shard 02) | [`references/domifications_matrix.md`](file:///var/www/.agents/skills/oraculo/references/domifications_matrix.md) |
| **F3 (Jyotish)** | Lahiri Whole Sign, D10 & Shadbala (Shard 03) | [`references/phases.md`](file:///var/www/.agents/skills/oraculo/references/phases.md) |
| **F4–F6 (Ontología)** | BaZi, Human Design y Tikkun (Shards 04–06) | [`references/phases.md`](file:///var/www/.agents/skills/oraculo/references/phases.md) |
| **F7–F9 (Estrategia)** | Vocación, Timing y Mentoría (Shards 07–10) | [`references/phases.md`](file:///var/www/.agents/skills/oraculo/references/phases.md) |
| **Sub-Oráculos (`diag-*`)** | Consumen `manifest.json` | [`references/domifications_matrix.md`](file:///var/www/.agents/skills/oraculo/references/domifications_matrix.md) |
| **Validación** | `skills-suite-validate` (`exit 0`) | [`references/usage.md`](file:///var/www/.agents/skills/oraculo/references/usage.md) |

## Resources
- [`references/domifications_matrix.md`](file:///var/www/.agents/skills/oraculo/references/domifications_matrix.md) · [`references/omni_engine.md`](file:///var/www/.agents/skills/oraculo/references/omni_engine.md) · [`references/tikkun_berg_taxonomy.md`](file:///var/www/.agents/skills/oraculo/references/tikkun_berg_taxonomy.md) · [`references/phases.md`](file:///var/www/.agents/skills/oraculo/references/phases.md) · [`references/infra.md`](file:///var/www/.agents/skills/oraculo/references/infra.md) · [`references/usage.md`](file:///var/www/.agents/skills/oraculo/references/usage.md)
