# Infraestructura y CoHaLo: Oráculo Diag-E-Geo ⚙️
*Dual-RAG SSoT*

## 1. Dependencias y Runtimes
- **Parser de Datos:** `jq` (obligatorio para filtrado de coordenadas GPS y arrays de líneas).
- **Procesamiento LLM:** `gemini-pro` o análogo (32K+).
- **Ruta de Salida:** Escribe obligatoriamente en `DIAG/<CLIENTE_ID>/diag_e_geo_report.md` (mismo nivel que `coach_report/`). 

## 2. Higiene de Procesos (Fractal CoHaLo)
- **Timeouts:** 
  - Consultas de parseo geoespacial con `jq`: `timeout 5s`.
  - Consultas sincrónicas al LLM: `WaitMsBeforeAsync: 10000`.
- **Circuit Breaker Espacial:** Si el módulo de Astroway no arrojó coordenadas de Astrocartografía en el JSON (ej. `aw_astrocartography` es nulo), abortar inmediatamente. No se puede calcular ACG sin el volcado de vectores planetarios geolocalizados (Permitido: 1 reintento lógico para parseo).
- **Limpieza (Zero Orphaned Tasks):** Todo sub-shell usado para parseo lat/lon debe morir explícitamente (`manage_task kill`).
