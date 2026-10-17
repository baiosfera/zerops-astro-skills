# Manual de Uso: Oráculo Diag-D-Leg (Blindaje Legal & Sociedades) ⚖️
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-d-leg` se encarga de analizar los flujos de riesgo corporativo. Ejecuta un mapeo astrológico centrado en la protección patrimonial, auditoría de socios comerciales y prevención de litigios o conflictos fiscales.

## 2. Ingestión de Datos (Canon 12-15-9 SSoT)
Consume de manera exclusiva y *offline* los datos estructurados bajo arquitectura de **Ingestión Granular**:

- **Vía Primaria (Zero I/O waste / granular):** Ingestión granular de Shards específicos vía VirtualDataLake (punteros RFC 6901 en `/var/www/baiosfera/ASTROLOGÍA/DIAG/<CLIENTE_ID>/raw/json/dumps/`):
  - `shard_03.json` (`shard_03_vedic_jyotish.json`): Bhava Bala, Casas 6 (litigios y disputas laborales), 7 (sociedades y contratos), 8 (patrimonio, impuestos y pasivos contingentes), y evaluación de aflicciones duras de Saturno y Marte.
  - `shard_10.json` (`shard_10_predictive_timing.json`): Tránsitos críticos, aspectos tensos y eclipses que activan los ejes de las casas 6, 7 y 8.
- **Vía Fallback (Retrocompatibilidad total):** Ingestión del volcado maestro en `/var/www/baiosfera/ASTROLOGÍA/DIAG/<CLIENTE_ID>/raw/json/dumps/client_dumps_15_shards.json` o `omni_dump_mega.json`.

### Vectores Aislados Obligatorios:
1. **Triada de Riesgo y Sociedades (Casas 6, 7, 8):** Extraído de `shard_01.json` y `shard_03.json`.
   - **Casa 6:** Litigios, deudas, conflictos laborales y enemigos abiertos.
   - **Casa 7:** Sociedades, contratos comerciales, fusiones y adquisiciones.
   - **Casa 8:** Patrimonio conjunto, impuestos (taxes), recursos de terceros y riesgos ocultos.
2. **Aflicciones de Saturno y Marte:** Identificación de aspectos duros (cuadraturas, oposiciones) hacia los regentes de las casas 6, 7 y 8.
3. **Ventanas Temporales Críticas:** Activación por tránsitos severos o eclipses en casas 6/7/8 provenientes de `shard_10.json`.

## 3. Protocolo de Ejecución LLM (U-Shape)
- **Atestación:** Validar en el JSON la posición y regencia de las Casas 6, 7 y 8.
- **Inferencia:**
  `[REGLAS_LEGAL_ASTRO_MATRIX] + [DATOS_EXTRAIDOS_C6_C7_C8] + [PLANTILLA_FORMATS]`
- **Generación:** El LLM redacta el dictamen de blindaje basándose en `formats.md`.

## 4. Workflow Transversal y Dependencias
- **Ejecución Asíncrona:** Invocado exclusivamente de forma desacoplada consumiendo el Lakehouse compilado.
- **Independencia de Archivo:** Se graba atómicamente en `diag_d_leg_report.md` (o `diagnostico_d_leg.md` según el pipeline). **PROHIBICIÓN ESTRICTA**: Jamás sobreescribe los análisis previos.
