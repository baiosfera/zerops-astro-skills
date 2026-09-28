# Infraestructura y CoHaLo: Oráculo Diag-A-Psy ⚙️
*Dual-RAG SSoT*

## 1. Dependencias y Runtimes
- **Herramientas de Parsing:** `jq` (obligatorio para filtrado JSON en shell).
- **Procesamiento de Lenguaje (LLM):** `gemini-pro` o `notebooklm_rag`. Las evaluaciones psicológicas de alta densidad requieren un motor con ventana de contexto de al menos 32K.
- **Rutas de Guardado:** El resultado debe escribirse atómicamente en un archivo aislado `diag_a_psy_report.md` (ej: DIAG/<CLIENTE_ID>/diag_a_psy_report.md, al mismo nivel que coach_report/). PROHIBICIÓN ESTRICTA: Jamás debe sobreescribir los archivos de las Fases 1 a 11 generados por el Oráculo Principal.

## 2. Higiene de Procesos (Fractal CoHaLo)
- **Extracción de JSON Segura:** Los comandos `jq` deben contar con timeout de procesamiento si el JSON pesa más de 5MB (`timeout 5s jq ...`).
- **Llamadas al Agente LLM:** 
  - `WaitMsBeforeAsync: 10000` si se dispara un subagente orquestador.
  - El límite de reintentos por alucinación (si el LLM omite secciones del formato de `formats.md`) es de **2 rondas máximas de corrección**. Si a la tercera falla, se detiene y reporta al usuario.
- **Zero Orphaned Tasks:** Cualquier script bash secundario usado para pre-parsear los JSON debe limpiarse del sistema antes de finalizar.
