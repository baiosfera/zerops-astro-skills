# Manual de Uso: Oráculo Diag-B-Voc (Carrera, Riqueza & Dasamsa) 💼
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-b-voc` se especializa en vocación, talento monetizable y proyección pública. Interpreta las configuraciones profesionales usando herramientas profundas como la carta armónica Dasamsa (D-10) y las casas artha.

## 2. Ingestión de Datos (Dual Ingestion - Canon 12-15-9 SSoT)
Esta skill **nunca** hace llamadas REST al exterior. Ingiere herméticamente los datos compilados por Oráculo:

- **Vía Primaria (Zero I/O waste / granular):** Ingestión granular de Shards específicos vía VirtualDataLake (punteros RFC 6901 en `/var/www/baiosfera/ASTROLOGÍA/DIAG/<CLIENTE_ID>/raw/json/dumps/`):
  - `shard_07.json` (`shard_07_vocational_wealth.json`): Vargas D-10 Dasamsa (vocación y estatus profesional), D-9 Navamsa y D-60 Shashtiamsa.
  - `shard_03.json` (`shard_03_vedic_jyotish.json`): Shadbala, Nakshatras y casas artha (2 finanzas, 6 servicio, 10 autoridad pública).
  - `shard_04.json` (`shard_04_chinese_bazi.json`): BaZi Day Master (Tiempo Solar Verdadero), estructura de los Diez Dioses (Shi Shen) y balance elemental.
  - `shard_12.json` (`shard_12_tcm_constitution.json`): Salud MTC (Medicina Tradicional China) y curva de vitalidad Neijing aplicada al rendimiento profesional.
- **Vía Fallback (Retrocompatibilidad total):** Ingestión del volcado maestro en `/var/www/baiosfera/ASTROLOGÍA/DIAG/<CLIENTE_ID>/raw/json/dumps/client_dumps_15_shards.json` o `omni_dump_mega.json`.

### Vectores Aislados Obligatorios:
1. **Dasamsa (D-10) Védico:** Extraído de `shard_07.json`. El D-10 es la clave canónica del Jyotish para "Actions in Society, Profession".
2. **Day Master (BaZi):** Extraído de `shard_04.json` (calculado en Tiempo Solar Verdadero + JieQi). Mapea la estructura elemental de la riqueza y el talento innato.
3. **Casas Terrenales y Artha (2, 6, 10):** Extraídas de `shard_01.json` (Tropical) y `shard_03.json` (Védico). Determinan el flujo de capital, rutinas y clímax de autoridad pública.
4. **Vitalidad & Biotipo (MTC):** Extraído de `shard_12.json` para alinear ritmos de productividad con el meridiano dominante y la curva Neijing.

## 3. Protocolo de Ejecución LLM (U-Shape)
- **Atestación:** Validar que los campos del Medio Cielo (MC), regente de casa 10 y el Day Master de BaZi estén presentes en el JSON.
- **Inferencia:** El prompt orquestador debe fusionar:
  `[REGLAS_STELLAR_MATRIX_VOCACIONAL] + [DATOS_EXTRAIDOS] + [PLANTILLA_FORMATS]`
- **Generación:** El LLM redacta el diagnóstico bajo el formato estricto de `formats.md`.

## 4. Workflow Transversal y Dependencias
- **Ejecución Asíncrona:** Se ejecuta de forma desacoplada consumiendo el Lakehouse compilado de Fase 0.
- **Independencia de Archivo:** El resultado se persiste en `diag_b_voc_report.md` (o `diagnostico_b_voc.md` según el pipeline de destino).
