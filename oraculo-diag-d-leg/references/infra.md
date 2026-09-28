# Infraestructura y CoHaLo: Oráculo Diag-D-Leg ⚙️
*Dual-RAG SSoT*

## 1. Dependencias y Runtimes
- **Parser de Datos:** `jq` (obligatorio para filtrado de casas y dignidades).
- **Procesamiento LLM:** `gemini-pro` o análogo con ventana de contexto extendida (32K+).
- **Ruta de Salida:** Escribe obligatoriamente en `DIAG/<CLIENTE_ID>/diag_d_leg_report.md` (mismo nivel que `coach_report/`). No altera la Fase 11 ni ninguna otra.

## 2. Higiene de Procesos (Fractal CoHaLo)
- **Timeouts:** 
  - Consultas sobre nodos de regencias de casas con `jq`: `timeout 5s`.
  - Consultas sincrónicas al LLM: `WaitMsBeforeAsync: 10000`.
- **Circuit Breaker Lógico:** Si el JSON extraído carece de información detallada sobre las Casas 6, 7 y 8 (por ejemplo, si el sistema falló al generar las cúspides Placidus o Whole Sign), abortar el proceso inmediatamente (Límite: 2 reintentos lógicos). No se puede diagnosticar riesgo corporativo sin la triada 6-7-8.
- **Limpieza (Zero Orphaned Tasks):** Procesos background de `jq` o requests a Python deben limpiarse con `manage_task kill`.
