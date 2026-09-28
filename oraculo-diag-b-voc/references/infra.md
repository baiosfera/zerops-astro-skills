# Infraestructura y CoHaLo: Oráculo Diag-B-Voc ⚙️
*Dual-RAG SSoT*

## 1. Dependencias y Runtimes
- **Parser de Datos:** `jq` (obligatorio).
- **Procesamiento LLM:** `gemini-pro` o análogo con ventana de 32K+.
- **Rutas de Salida:** Se guardará en `/var/www/data/astrologia/DIAG/<CLIENTE_ID>/diag_b_voc_report.md` (o directorio equivalente). **PROHIBICIÓN ESTRICTA:** No sobreescribir `fase7_voc.md`.

## 2. Higiene de Procesos (Fractal CoHaLo)
- **Timeouts:** 
  - Extracción `jq`: `timeout 5s`.
  - Invocación de orquestador LLM: `WaitMsBeforeAsync: 10000`.
- **Circuit Breaker Lógico:** Si el Dasamsa (D-10) no puede aislarse de la metadata védica, el script de inferencia debe escalar (2 reintentos de extracción) antes de abortar el diagnóstico vocacional.
- **Limpieza (Zero Orphaned Tasks):** Todo proceso de background o script subshell abierto para analizar el Day Master de BaZi debe ser purgado usando `manage_task kill`.
