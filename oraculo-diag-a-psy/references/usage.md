# Manual de Uso: Oráculo Diag-A-Psy (Psicología Profunda) 🧠
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-a-psy` se especializa en psicología arquetípica profunda. Consume la *Data Lake* generada por las API (Fase 0) y ejecuta un escrutinio enfocado en la estructura de la personalidad, traumas kármicos y dinámica de poder.

## 2. Ingestión de Datos (Dual Ingestion - Opción B)
Esta skill **nunca** hace llamadas REST al exterior. Opera bajo arquitectura de **Ingestión Dual**:

- **Vía Primaria (Zero I/O waste / granular):** Ingestión granular de Shards específicos vía VirtualDataLake (punteros RFC 6901 en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/shards/`). Minimiza consumo de memoria y maximiza la velocidad de carga al resolver únicamente los fragmentos requeridos:
  - `shard_01_western_natal.json`: Tropical Placidus, escuelas Greene/Arroyo.
  - `shard_02_psychological.json`: Fagan-Campanus, Aldebaran 15 Tau Vehlow y arquetipos sombra.
- **Vía Fallback (Retrocompatibilidad total):** Ingestión del volcado monolítico tradicional en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/raw/omni_dump_mega.json` si los shards individuales no están disponibles.

### Vectores Aislados Obligatorios:
1. **Tropical + Equal Asc (Vector Consciente):** Extraído de `shard_01_western_natal.json` (o nodo `.fa_tropical_calculate` en fallback). Define la narrativa psicológica lineal.
2. **Sideral Fagan-Bradley + Campanus (Vector Inconsciente):** Extraído de `shard_02_psychological.json` (o `.fa_sidereal_fagan_campanus` / `.fa_sidereal_calculate` en fallback). Mapea impulsos sombríos.
3. **Sideral Aldebaran + Vehlow (Puntos Ciegos):** Usado para detectar intercepciones puras de la psique.

## 3. Protocolo de Ejecución LLM (U-Shape)
- **Atestación:** Validar que los campos `Ascendant`, `Sun`, `Moon` existan en el JSON de entrada.
- **Inferencia (Prompt Engineering):** Construir un bloque de texto que combine:
  `[REGLAS_STELLAR_MATRIX] + [DATOS_EXTRAIDOS] + [PLANTILLA_FORMATS]`
- **Generación:** El LLM redacta el diagnóstico bajo el formato estricto de `formats.md`.

## 4. Prohibiciones
- **PROHIBICIÓN ESPACIAL EXTREMA:** Para clientes con Hora Cero (sin hora confirmada), se ignora Vehlow y Campanus; el sistema **debe** caer en `Whole Sign` (Casas Iguales por Signo Completo) inyectando el Ascendente en el signo del Sol.

## 5. Workflow de Coach Astrológico
- **Ejecución Asíncrona:** Las skills `oraculo-diag-*` se ejecutan **exclusivamente de manera manual e independiente** por el coach astrológico *solo después* de que el Oráculo principal ha finalizado de generar las Fases 1 a 11 en `/DIAG/<ID>/`.
- **Independencia Transversal:** No hay orden secuencial entre las skills `diag-*`. Todas operan como satélites de lectura profunda de la data ya solidificada.
