# Manual de Uso: Oráculo Diag-C-Mkt (Market Timing & KP Eleccional) 📈
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-c-mkt` es un especialista en *Timing* de Mercado y Astrología Eleccional. Utiliza los micro-tiempos de la Astrología KP (Krishnamurti Paddhati) para encontrar ventanas temporales precisas para lanzamientos, firma de contratos y campañas comerciales.

## 2. Ingestión de Datos (Dual Ingestion - Opción B)
Esta skill **nunca** hace llamadas REST al exterior. Opera bajo arquitectura de **Ingestión Dual**:

- **Vía Primaria (Zero I/O waste / granular):** Ingestión granular de Shards específicos vía VirtualDataLake (punteros RFC 6901 en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/shards/`). Carga de alta velocidad optimizada para micro-tiempos:
  - `shard_03_vedic_sidereal.json`: KP V2 Krishnamurti Paddhati Star Lord / Sub Lord / Sub Sub Lord en casas 2, 6, 10 y 11.
  - `shard_08_timing_transits.json`: Timeline dinámica, tránsitos planetarios y Dashas Vimshottari en 5 niveles.
  - `shard_10_asteroids_fixed_stars.json`: Asteroides comerciales y estrellas fijas conectadas a éxito y visibilidad.
- **Vía Fallback (Retrocompatibilidad total):** Ingestión del volcado monolítico tradicional en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/raw/omni_dump_mega.json` si los shards individuales no se encuentran presentes.

### Vectores Aislados Obligatorios:
1. **Krishnamurti Paddhati (KP) Puntos:** Extraído de `shard_03_vedic_sidereal.json` (o `.fa_sidereal_krishnamurti` / Astroway KP en fallback).
   - El sistema divide cada Nakshatra (13°20') en 9 porciones desiguales (proporción Vimshottari). El regente de la porción es el **Sub Lord**.
   - **Regla KP:** El planeta es la *fuente* del evento, el Star Lord indica la *naturaleza* del evento, y el Sub Lord decide si el evento es *favorable o no*.
2. **Ciclos de Proyección:** Ciclos lunares, eclipses y planetas lentos (Júpiter/Saturno/Nodos) extraídos de `shard_08_timing_transits.json` (o efemérides en tránsito en fallback).
3. **Puntos de Impacto Comercial:** Activaciones por estrellas fijas y asteroides clave extraídos de `shard_10_asteroids_fixed_stars.json`.

## 3. Protocolo de Ejecución LLM (U-Shape)
- **Atestación:** Verificar en el JSON la presencia de `KP_Sub_Lord` y `KP_Star_Lord` de la Casa 2, 6, 10 y 11 (Finanzas y Ganancias).
- **Inferencia:**
  `[REGLAS_KP_MARKET_TIMING] + [DATOS_EXTRAIDOS] + [PLANTILLA_FORMATS]`
- **Generación:** El LLM diagnostica los gatillos comerciales usando la plantilla `formats.md`.

## 4. Workflow Transversal y Dependencias
- **Ejecución Asíncrona:** Invocado por el coach humano exclusivamente **después** del Oráculo base (Fases 1-11).
- **Independencia de Archivo:** Se graba en su propio archivo aislado `diag_c_mkt_report.md` en el root del cliente (`DIAG/<CLIENTE_ID>/`). JAMÁS sobreescribe los reportes canónicos.
