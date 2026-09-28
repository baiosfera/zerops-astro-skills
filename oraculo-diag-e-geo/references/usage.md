# Manual de Uso: Oráculo Diag-E-Geo (Astrocartografía y Relocación) 🌍
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-e-geo` mapea el impacto geográfico del potencial de un cliente. Analiza las líneas planetarias proyectadas sobre los 4 ángulos cardinales (Ascendente, Descendente, Medio Cielo y Fondo del Cielo) para determinar los mejores mercados físicos para expansión comercial, retiros espirituales o relocación.

## 2. Ingestión de Datos (Dual Ingestion - Opción B)
Esta skill **nunca** hace llamadas REST. Lee los datos geográficos bajo arquitectura de **Ingestión Dual**:

- **Vía Primaria (Zero I/O waste / granular):** Ingestión granular de Shards específicos vía VirtualDataLake (punteros RFC 6901 en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/shards/`). Carga espacial de alta densidad sin latencia I/O:
  - `shard_09_astrocartography.json`: GeoJSON ACG con 34k ciudades mundiales, cálculo de Espacio Local (Azimuth y elevación), y cruces planetarios angulares en los cuatro ejes cardinales (ASC, DSC, MC, IC).
- **Vía Fallback (Retrocompatibilidad total):** Ingestión del volcado monolítico tradicional en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/raw/omni_dump_mega.json` si el shard individual no está presente.

### Vectores Aislados Obligatorios:
1. **Líneas Angulares (ACG):** Extraído de `shard_09_astrocartography.json` (o nodo `.aw_astrocartography` en fallback). Contiene coordenadas lat/lon de intersección planetaria.
   - **Líneas ASC:** (Personalidad, inicios, magnetismo físico).
   - **Líneas DSC:** (Sociedades, matrimonios, atracción de clientes).
   - **Líneas MC:** (Carrera, fama, éxito público corporativo).
   - **Líneas IC:** (Hogar, raíces, fundaciones inmobiliarias).
2. **Espacio Local (Azimuth):** Direcciones cardinales desde la ciudad natal para micro-relocación (Feng Shui Astrológico).

## 3. Protocolo de Ejecución LLM (U-Shape)
- **Atestación:** Verificar en el JSON la existencia del array de ACG (líneas de Sol, Júpiter, Venus, etc.).
- **Inferencia:**
  `[REGLAS_ASTRO_GEO_MAPPING] + [COORDENADAS_EXTRAIDAS] + [PLANTILLA_FORMATS]`
- **Generación:** El LLM identifica países/ciudades clave donde caen las líneas de expansión (Júpiter MC, Sol ASC, Venus DSC) siguiendo `formats.md`.

## 4. Workflow Transversal y Dependencias
- **Ejecución Asíncrona:** Invocado por el coach humano exclusivamente **después** del Oráculo base (Fases 1-11).
- **Independencia de Archivo:** Se graba atómicamente en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/diag_e_geo_report.md` (mismo nivel que `coach_report/`). No altera la Fase 11 ni ninguna otra.
