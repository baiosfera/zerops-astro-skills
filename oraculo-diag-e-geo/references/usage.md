# Manual de Uso: Oráculo Diag-E-Geo (Astrocartografía y Relocación) 🌍
*Dual-RAG SSoT - Invariant 0 Validated*

## 1. Propósito y Dominio
El sub-agente `oraculo-diag-e-geo` mapea el impacto geográfico del potencial de un cliente. Analiza las líneas planetarias proyectadas sobre los 4 ángulos cardinales (Ascendente, Descendente, Medio Cielo y Fondo del Cielo) para determinar los mejores mercados físicos para expansión comercial, retiros espirituales o relocación.

## 2. Ingestión de Datos (Inputs)
Esta skill **nunca** hace llamadas REST. Lee los datos geográficos del JSON central en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/raw/omni_dump_mega.json`.

### Vectores Aislados Obligatorios:
1. **Líneas Angulares (ACG):** Extraído del nodo `.aw_astrocartography` (proveedor Astroway). Contiene coordenadas lat/lon de intersección planetaria.
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
