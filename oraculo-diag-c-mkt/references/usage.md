# Manual de Uso: Oráculo Diag-C-Mkt (Market Timing & KP Eleccional) 📈
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-c-mkt` es un especialista en *Timing* de Mercado y Astrología Eleccional. Utiliza los micro-tiempos de la Astrología KP (Krishnamurti Paddhati) y Dashas Vimshottari en 5 niveles para encontrar ventanas temporales precisas para lanzamientos, firma de contratos y campañas comerciales.

## 2. Ingestión de Datos (Canon 12-15-9 SSoT)
Esta skill **nunca** hace llamadas REST al exterior. Ingiere herméticamente los datos compilados por Oráculo:

- **Vía Primaria (Zero I/O waste / granular):** Ingestión granular de Shards específicos vía VirtualDataLake (punteros RFC 6901 en `/var/www/baiosfera/ASTROLOGÍA/DIAG/<CLIENTE_ID>/raw/json/dumps/`):
  - `shard_03.json` (`shard_03_vedic_jyotish.json`): KP Krishnamurti Paddhati Star Lord / Sub Lord / Sub Sub Lord en cúspides de casas 2, 6, 10 y 11.
  - `shard_10.json` (`shard_10_predictive_timing.json`): Timeline dinámica, tránsitos planetarios, línea de tiempo helenística y Dashas Vimshottari en 5 niveles.
  - `shard_14.json` (`shard_14_cross_bridges.json` / `raw/json/cache/`): Asteroides comerciales, estrellas fijas y tránsitos conectadas a éxito y visibilidad.
- **Vía Fallback (Retrocompatibilidad total):** Ingestión del volcado maestro en `/var/www/baiosfera/ASTROLOGÍA/DIAG/<CLIENTE_ID>/raw/json/dumps/client_dumps_15_shards.json` o `omni_dump_mega.json`.

### Vectores Aislados Obligatorios:
1. **Krishnamurti Paddhati (KP) Puntos:** Extraído de `shard_03.json`.
   - El sistema divide cada Nakshatra (13°20') en 9 porciones desiguales (proporción Vimshottari). El regente de la porción es el **Sub Lord**.
   - **Regla KP:** El planeta es la *fuente* del evento, el Star Lord indica la *naturaleza* del evento, y el Sub Lord decide si el evento es *favorable o no*.
2. **Ciclos de Proyección y Dashas (5 niveles):** Ciclos lunares, eclipses, Mahadasha, Antardasha y Pratyantardasha extraídos de `shard_10.json`.
3. **Puntos de Impacto Comercial:** Activaciones por estrellas fijas y asteroides clave extraídos de `shard_14.json` y del Lakehouse natal.

## 3. Protocolo de Ejecución LLM (U-Shape)
- **Atestación:** Verificar en el JSON la presencia de `KP_Sub_Lord` y `KP_Star_Lord` de la Casa 2, 6, 10 y 11 (Finanzas y Ganancias).
- **Inferencia:**
  `[REGLAS_KP_MARKET_TIMING] + [DATOS_EXTRAIDOS] + [PLANTILLA_FORMATS]`
- **Generación:** El LLM diagnostica los gatillos comerciales usando la plantilla `formats.md`.

## 4. Workflow Transversal y Dependencias
- **Ejecución Asíncrona:** Invocado exclusivamente de forma desacoplada consumiendo el Lakehouse compilado.
- **Independencia de Archivo:** Se graba de forma aislada en `diag_c_mkt_report.md` (o `diagnostico_c_mkt.md` según el pipeline), preservando intactos los reportes canónicos.
