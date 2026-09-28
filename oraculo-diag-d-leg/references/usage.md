# Manual de Uso: Oráculo Diag-D-Leg (Blindaje Legal & Sociedades) ⚖️
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-d-leg` se encarga de analizar los flujos de riesgo corporativo. Ejecuta un mapeo astrológico centrado en la protección patrimonial, auditoría de socios comerciales y prevención de litigios o conflictos fiscales.

## 2. Ingestión de Datos (Inputs)
Consume de manera exclusiva y *offline* el `omni_dump_mega.json` ubicado en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/raw/`.

### Vectores Aislados Obligatorios:
1. **Triada de Riesgo y Sociedades (Casas 6, 7, 8):** Extraído del nodo `.fa_tropical_calculate` y `.va_all_planet_data`.
   - **Casa 6:** Litigios, deudas, conflictos laborales y enemigos abiertos.
   - **Casa 7:** Sociedades, contratos comerciales, fusiones y adquisiciones.
   - **Casa 8:** Patrimonio conjunto, impuestos (taxes), recursos de terceros y riesgos ocultos.
2. **Aflicciones de Saturno y Marte:** Identificación de aspectos duros (cuadraturas, oposiciones) hacia los regentes de las casas 6, 7 y 8.

## 3. Protocolo de Ejecución LLM (U-Shape)
- **Atestación:** Validar en el JSON la posición y regencia de las Casas 6, 7 y 8.
- **Inferencia:** 
  `[REGLAS_LEGAL_ASTRO_MATRIX] + [DATOS_EXTRAIDOS_C6_C7_C8] + [PLANTILLA_FORMATS]`
- **Generación:** El LLM redacta el dictamen de blindaje basándose en `formats.md`.

## 4. Workflow Transversal y Dependencias
- **Ejecución Asíncrona:** Invocado por el coach humano exclusivamente **después** del Oráculo base (Fases 1-11).
- **Independencia de Archivo:** Se graba atómicamente en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/diag_d_leg_report.md`. **PROHIBICIÓN ESTRICTA**: Jamás sobreescribe los análisis previos.
