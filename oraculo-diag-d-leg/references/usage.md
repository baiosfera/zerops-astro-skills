# Manual de Uso: Oráculo Diag-D-Leg (Blindaje Legal & Sociedades) ⚖️
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-d-leg` se encarga de analizar los flujos de riesgo corporativo. Ejecuta un mapeo astrológico centrado en la protección patrimonial, auditoría de socios comerciales y prevención de litigios o conflictos fiscales.

## 2. Ingestión de Datos (Dual Ingestion - Opción B)
Consume de manera exclusiva y *offline* los datos estructurados bajo arquitectura de **Ingestión Dual**:

- **Vía Primaria (Zero I/O waste / granular):** Ingestión granular de Shards específicos vía VirtualDataLake (punteros RFC 6901 en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/shards/`). Aislamiento de vectores de riesgo sin transferir datos superfluos:
  - `shard_03_vedic_sidereal.json`: Bhava Bala, Casas 6 (litigios y disputas laborales), 7 (sociedades y contratos), 8 (patrimonio, impuestos y pasivos contingentes), y evaluación de aflicciones duras de Saturno y Marte.
  - `shard_08_timing_transits.json`: Tránsitos críticos, aspectos tensos y eclipses que activan los ejes de las casas 6, 7 y 8.
- **Vía Fallback (Retrocompatibilidad total):** Ingestión del volcado monolítico tradicional en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/raw/omni_dump_mega.json` si los shards individuales no están disponibles.

### Vectores Aislados Obligatorios:
1. **Triada de Riesgo y Sociedades (Casas 6, 7, 8):** Extraído de `shard_03_vedic_sidereal.json` (o `.fa_tropical_calculate` y `.va_all_planet_data` en fallback).
   - **Casa 6:** Litigios, deudas, conflictos laborales y enemigos abiertos.
   - **Casa 7:** Sociedades, contratos comerciales, fusiones y adquisiciones.
   - **Casa 8:** Patrimonio conjunto, impuestos (taxes), recursos de terceros y riesgos ocultos.
2. **Aflicciones de Saturno y Marte:** Identificación de aspectos duros (cuadraturas, oposiciones) hacia los regentes de las casas 6, 7 y 8.
3. **Ventanas Temporales Críticas:** Activación por tránsitos severos o eclipses en casas 6/7/8 provenientes de `shard_08_timing_transits.json`.

## 3. Protocolo de Ejecución LLM (U-Shape)
- **Atestación:** Validar en el JSON la posición y regencia de las Casas 6, 7 y 8.
- **Inferencia:**
  `[REGLAS_LEGAL_ASTRO_MATRIX] + [DATOS_EXTRAIDOS_C6_C7_C8] + [PLANTILLA_FORMATS]`
- **Generación:** El LLM redacta el dictamen de blindaje basándose en `formats.md`.

## 4. Workflow Transversal y Dependencias
- **Ejecución Asíncrona:** Invocado por el coach humano exclusivamente **después** del Oráculo base (Fases 1-11).
- **Independencia de Archivo:** Se graba atómicamente en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/diag_d_leg_report.md`. **PROHIBICIÓN ESTRICTA**: Jamás sobreescribe los análisis previos.
