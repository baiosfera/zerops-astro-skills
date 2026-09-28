# Manual de Uso: Oráculo Diag-B-Voc (Carrera, Riqueza & Dasamsa) 💼
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-b-voc` se especializa en vocación, talento monetizable y proyección pública. Interpreta las configuraciones profesionales usando herramientas profundas como la carta armónica Dasamsa (D-10).

## 2. Ingestión de Datos (Dual Ingestion - Opción B)
Esta skill **nunca** hace llamadas REST al exterior. Opera bajo arquitectura de **Ingestión Dual**:

- **Vía Primaria (Zero I/O waste / granular):** Ingestión granular de Shards específicos vía VirtualDataLake (punteros RFC 6901 en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/shards/`). Carga quirúrgica sin latencia I/O:
  - `shard_12_harmonic_charts.json`: Vargas D-10 Dasamsa (vocación y estatus), D-9 Navamsa y D-60 Shashtiamsa.
  - `shard_03_vedic_sidereal.json`: Shadbala y casas artha (2 finanzas, 6 servicio, 10 autoridad profesional).
  - `shard_04_chinese_metaphysics.json`: BaZi Day Master, estructura de los Diez Dioses (Shi Shen) y balance elemental.
  - `shard_11_tcm_health.json`: Salud MTC (Medicina Tradicional China) y curva de vitalidad Neijing aplicada al rendimiento profesional.
- **Vía Fallback (Retrocompatibilidad total):** Ingestión del volcado monolítico tradicional en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/raw/omni_dump_mega.json` si los shards no están disponibles.

### Vectores Aislados Obligatorios:
1. **Dasamsa (D-10) Védico:** Extraído de `shard_12_harmonic_charts.json` (o nodo correspondiente en `.va_horoscope_predictions` / `va_all_planet_data` en fallback). El D-10 es la clave canónica del Jyotish para "Actions in Society, Profession".
2. **Day Master (BaZi):** Extraído de `shard_04_chinese_metaphysics.json` (o `.fa_chinese_bazi` en fallback). Mapea la estructura elemental de la riqueza y el talento de producción innato.
3. **Casas Terrenales (2, 6, 10 Tropical):** Extraído de `shard_03_vedic_sidereal.json` (o `.fa_tropical_calculate` en fallback). Determina el flujo de dinero, rutinas operativas y clímax de autoridad pública.
4. **Vitalidad & Biotipo (MTC):** Extraído de `shard_11_tcm_health.json` para alinear ritmos de productividad con el meridiano dominante y la curva Neijing.

## 3. Protocolo de Ejecución LLM (U-Shape)
- **Atestación:** Validar que los campos del Medio Cielo (MC), regente de casa 10 y el Day Master de BaZi estén presentes en el JSON.
- **Inferencia:** El prompt orquestador debe fusionar:
  `[REGLAS_STELLAR_MATRIX_VOCACIONAL] + [DATOS_EXTRAIDOS] + [PLANTILLA_FORMATS]`
- **Generación:** El LLM redacta el diagnóstico bajo el formato estricto de `formats.md`.

## 4. Workflow Transversal y Dependencias
- **Ejecución Asíncrona:** Se ejecuta manualmente por el consultor humano **solo después** de finalizadas las Fases 1 a 11.
- **Independencia de Archivo:** El resultado debe aislarse en `diag_b_voc_report.md` sin sobreescribir jamás la fase original `fase7_voc.md`.
