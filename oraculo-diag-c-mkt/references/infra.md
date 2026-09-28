# Infraestructura y CoHaLo: Oráculo Diag-C-Mkt ⚙️
*Dual-RAG SSoT*

## 1. Dependencias y Runtimes
- **Parser de Datos:** `jq` (obligatorio para filtrar la estructura KP profunda).
- **Procesamiento LLM:** `gemini-pro` o análogo con ventana de contexto extendida.
- **Ruta de Salida:** Escribe obligatoriamente en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/diag_c_mkt_report.md`. **PROHIBICIÓN ESTRICTA:** No tocar los archivos de las Fases 1 a 11.

## 2. Higiene de Procesos (Fractal CoHaLo)
- **Timeouts:** 
  - Consultas sobre grandes arrays KP con `jq`: `timeout 5s`.
  - Consultas sincrónicas al LLM: `WaitMsBeforeAsync: 10000`.
- **Circuit Breaker Matemático:** El algoritmo KP es híper sensible al tiempo de nacimiento. Si el JSON no tiene el nivel `Sub_Lord`, abortar con un error explícito (1 reintento permitido si fue un fallo de parsing). No alucinar un Sub Lord.
- **Limpieza (Zero Orphaned Tasks):** Usar `manage_task kill` en scripts Bash que hayan quedado rezagados filtrando tránsitos planetarios.
