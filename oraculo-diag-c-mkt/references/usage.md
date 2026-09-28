# Manual de Uso: Oráculo Diag-C-Mkt (Market Timing & KP Eleccional) 📈
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-c-mkt` es un especialista en *Timing* de Mercado y Astrología Eleccional. Utiliza los micro-tiempos de la Astrología KP (Krishnamurti Paddhati) para encontrar ventanas temporales precisas para lanzamientos, firma de contratos y campañas comerciales.

## 2. Ingestión de Datos (Inputs)
Esta skill **nunca** hace llamadas REST al exterior. Lee los datos ya generados en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/raw/omni_dump_mega.json`.

### Vectores Aislados Obligatorios:
1. **Krishnamurti Paddhati (KP) Puntos:** Extraído del nodo `.fa_sidereal_krishnamurti` o la API de Astroway KP. 
   - El sistema divide cada Nakshatra (13°20') en 9 porciones desiguales (proporción Vimshottari). El regente de la porción es el **Sub Lord**.
   - **Regla KP:** El planeta es la *fuente* del evento, el Star Lord indica la *naturaleza* del evento, y el Sub Lord decide si el evento es *favorable o no*.
2. **Ciclos de Proyección:** Ciclos lunares, eclipses y planetas lentos (Júpiter/Saturno/Nodos) extraídos de las efemérides en tránsito.

## 3. Protocolo de Ejecución LLM (U-Shape)
- **Atestación:** Verificar en el JSON la presencia de `KP_Sub_Lord` y `KP_Star_Lord` de la Casa 2, 6, 10 y 11 (Finanzas y Ganancias).
- **Inferencia:** 
  `[REGLAS_KP_MARKET_TIMING] + [DATOS_EXTRAIDOS] + [PLANTILLA_FORMATS]`
- **Generación:** El LLM diagnostica los gatillos comerciales usando la plantilla `formats.md`.

## 4. Workflow Transversal y Dependencias
- **Ejecución Asíncrona:** Invocado por el coach humano exclusivamente **después** del Oráculo base (Fases 1-11).
- **Independencia de Archivo:** Se graba en su propio archivo aislado `diag_c_mkt_report.md` en el root del cliente (`DIAG/<CLIENTE_ID>/`). JAMÁS sobreescribe los reportes canónicos.
