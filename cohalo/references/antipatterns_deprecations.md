# CoHaLo Reference Manual: Deprecations & Antipatterns (Legacy Prompting Purge)

## 1. Concepto Fundamental
En la evolución de la IA hacia arquitecturas agénticas y modelos de razonamiento en el Presente Dinámico, múltiples prácticas tempranas de *prompting amateur* han quedado formalmente **deprecadas**. Mantenerlas introduce ruido en la atención, invalida cachés y degrada el rendimiento.

---

## 2. Catálogo de Antipatrones y Prácticas Deprecadas

### 1. Manipulación Emocional y "Hacks" Psicológicos ❌
- **Antipatrón:** *"Te daré 500 dólares de propina si lo haces bien"*, *"Mi carrera/vida depende de esta respuesta"*, *"Respira hondo y relájate antes de responder"*.
- **Razón Técnica:** Los modelos frontera están alineados con RLHF riguroso y optimizados para atención semántica pura. Estos tokens consumen presupuesto de atención, ensucian la caché KV y no aportan ninguna mejora en benchmarks objetivos.
- **Sustituto SOTA:** Instrucciones claras, criterios deterministas de aceptación y esquemas tipados.

### 2. Forzado de Pseudo-CoT en Modelos de Razonamiento ❌
- **Antipatrón:** Añadir *"Piensa paso a paso"* o *"Let us think step by step"* a prompts dirigidos a OpenAI o1/o3/o4-mini, Claude 3.7 Thinking o Gemini 3 Thinking.
- **Razón Técnica:** Los modelos de razonamiento ya ejecutan cadenas de inferencia deliberativa nativas. Inyectar CoT manual en texto visible genera interferencia entre el razonamiento interno del modelo y el texto generado, inflando tokens innecesariamente.
- **Sustituto SOTA:** Calibrar `reasoning_effort` o `thinking_budget` y proveer invariantes duros.

### 3. Parsing Frágil por Expresiones Regulares en Texto Libre ❌
- **Antipatrón:** Pedirle al modelo que responda en texto libre con un formato semi-estructurado y luego intentar extraer campos mediante regex en el código cliente.
- **Razón Técnica:** Altamente vulnerable a variaciones sintácticas, cambios de formato o alucinaciones leves en la puntuación.
- **Sustituto SOTA:** **Structured Outputs** nativo con esquemas Pydantic / Zod / JSON Schema y validadores deterministas (`zcp-validate`).

### 4. Prefills Forzados del Turno del Asistente ❌
- **Antipatrón:** Prefillar el inicio del mensaje del asistente con `{
  "data":` o ````json` para forzar la salida.
- **Razón Técnica:** Deprecado oficialmente en APIs modernas (e.g. Claude 4.6+ y Mythos devuelven error HTTP 400).
- **Sustituto SOTA:** Structured Outputs y Function Calling nativo.

### 5. Corregir Envenenamiento en el Mismo Chat ❌
- **Antipatrón:** Cuando el modelo comete un error grave o alucina, responderle en el chat *"No, eso está mal, corrígelo con X"*.
- **Razón Técnica:** No borra el error; agrega el dato falso, la corrección y la discusión al historial, provocando una degradación de rendimiento del 39% por arrastre de supuestos erróneos.
- **Sustituto SOTA:** Reiniciar inmediatamente a una **sesión limpia** con el dato corregido en el System Prompt o contexto inicial (*Concat-and-retry*).

### 6. Acrónimos Forzados como "Hechizos Mágicos" ❌
- **Antipatrón:** Imponer plantillas rígidas (PREP, STAR, CREATE, etc.) como fórmulas mágicas de éxito.
- **Razón Técnica:** Añaden verbosidad innecesaria. Lo que importa es la separación semántica clara (Rol, Instrucciones, Reglas, Contexto, Formato) delimitada con etiquetas XML.
- **Sustituto SOTA:** Delimitadores semánticos universales XML.
