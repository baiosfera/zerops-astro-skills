# Manual de Uso: Oráculo Diag-E-Geo (Astrocartografía y Relocación) 🌍
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-e-geo` mapea el impacto geográfico del potencial de un cliente. Analiza las líneas planetarias proyectadas sobre los 4 ángulos cardinales (Ascendente, Descendente, Medio Cielo y Fondo del Cielo) para determinar los mejores mercados físicos para expansión comercial, retiros espirituales o relocación.

## 2. Ingestión de Datos (Canon 12-15-9 SSoT)
Esta skill **nunca** hace llamadas REST. Lee los datos geográficos bajo arquitectura de **Ingestión Granular**:

- **Vía Primaria (Zero I/O waste / granular):** Ingestión granular de Shards específicos vía VirtualDataLake (punteros RFC 6901 en `/var/www/baiosfera/ASTROLOGÍA/DIAG/<CLIENTE_ID>/raw/json/dumps/`):
  - `shard_08.json` (`shard_08_astrocartography.json`): GeoJSON ACG con coordenadas mundiales, cálculo de Espacio Local (Azimuth y elevación), y cruces planetarios angulares en los cuatro ejes cardinales (ASC, DSC, MC, IC).
- **Vía Fallback (Retrocompatibilidad total):** Ingestión del volcado maestro en `/var/www/baiosfera/ASTROLOGÍA/DIAG/<CLIENTE_ID>/raw/json/dumps/client_dumps_15_shards.json` o `omni_dump_mega.json`.

### Vectores Aislados Obligatorios:
1. **Líneas Angulares (ACG):** Extraído de `shard_08.json`. Contiene coordenadas lat/lon de intersección planetaria.
   - **Líneas ASC:** (Personalidad, inicios, magnetismo físico).
   - **Líneas DSC:** (Sociedades, matrimonios, atracción de clientes).
   - **Líneas MC:** (Carrera, fama, éxito público corporativo).
   - **Líneas IC:** (Hogar, raíces, fundaciones inmobiliarias).
2. **Espacio Local (Azimuth):** Direcciones cardinales desde la ciudad natal para micro-relocación y proyección geográfica.

## 3. Protocolo de Ejecución LLM (U-Shape)
- **Atestación:** Verificar en el JSON la existencia del array de ACG (líneas de Sol, Júpiter, Venus, etc.).
- **Inferencia:**
  `[REGLAS_ASTRO_GEO_MAPPING] + [COORDENADAS_EXTRAIDAS] + [PLANTILLA_FORMATS]`
- **Generación:** El LLM identifica países/ciudades clave donde caen las líneas de expansión (Júpiter MC, Sol ASC, Venus DSC) siguiendo `formats.md`.

## 4. Workflow Transversal y Dependencias
- **Ejecución Asíncrona:** Invocado exclusivamente de forma desacoplada consumiendo el Lakehouse compilado.
- **Independencia de Archivo:** Se graba atómicamente en `diag_e_geo_report.md` (o `diagnostico_e_geo.md` según el pipeline). No altera la Fase 11 ni ninguna otra.
