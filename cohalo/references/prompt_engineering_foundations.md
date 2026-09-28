# CoHaLo Reference Manual: Prompt Engineering Foundations & Positive Guidance (v7.0)

## 1. Concepto Fundamental
El **Prompt Engineering** en la arquitectura CoHaLo es la disciplina de formular contratos de interfaz semántica no ambiguos, estructurados y matemáticamente orientados para motores de inferencia. Trata al modelo fundacional exclusivamente como un **procesador semántico probabilístico**, eliminando suposiciones de memoria estática y garantizando reproducibilidad.

---

## 2. Delimitación Semántica Universal (Jerarquía XML)
Para aislar datos pasivos de directivas ejecutables y blindar al modelo contra *Indirect Prompt Injection* y confusión de roles, toda especificación de prompt compleja emplea delimitación semántica estricta mediante etiquetas XML:

```xml
<system_role>
Definición formal de identidad, nivel de seniority, dominio cerrado de autoridad y tono.
</system_role>

<instructions>
Directivas afirmativas secuenciales paso a paso en orden lógico de ejecución.
</instructions>

<rules>
Invariantes duros, restricciones de dominio cerrado y condiciones de parada deterministas.
</rules>

<context>
<!-- Ingested documents, API outputs, and external payloads reside here as PASSIVE data -->
<payload id="sample-1">
  {"key": "value"}
</payload>
</context>

<output_format>
Especificación determinista de estructura requerida (Structured Outputs / JSON Schema / Markdown formal).
</output_format>
```

### Reglas de Uso de Delimitadores:
1. **Inviolabilidad de Datos:** Los datos inyectados por usuarios o herramientas externas residen exclusivamente dentro de `<context>`. Las directivas establecen que cualquier instrucción contenida dentro de `<context>` debe tratarse como texto inerte, jamás como comando de ejecución.
2. **Anidamiento Semántico:** Al inyectar múltiples fuentes, anidar formalmente: `<documents><document id="1"><content>...</content></document></documents>`.

---

## 3. Definición Quirúrgica de Roles (System Prompts)
Un rol efectivo no es una descripción novelesca ni un adorno retórico. Establece el **marco ontológico, los límites de autoridad y las condiciones de frontera** del agente:

- **Enfoque Directo:** Declaración concisa del dominio de especialidad técnica y años de experiencia contextual.
- **Límites de Dominio:** Especificación afirmativa del conjunto cerrado de herramientas, archivos y operaciones sobre las que el rol ejerce autoridad.
- **Tono y Voz:** Directo, técnico, conciso y fundamentado en evidencia comprobable.

---

## 4. Principio SOTA de Guía Positiva (Positive Guidance Engine)

### 4.1 La Falla Cognitiva de las Directivas Negativas (El Efecto Elefante Rosa)
En modelos basados en la arquitectura Transformer, el mecanismo de auto-atención calcula la correlación cruzada entre todos los tokens:
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

Cuando una directiva se formula negativamente (*"No uses Markdown"*, *"Prohibido alucinar"*, *"No hagas explicaciones largas"*):
1. **Activación Semántica Forzada:** La auto-atención activa con máxima prioridad los embeddings de los términos prohibidos (*"Markdown"*, *"alucinar"*, *"explicaciones"*).
2. **Fallo de Cabezas Inhibitorias:** Aunque existan mecanismos de alineación (RLHF), las cabezas de atención inhibitoria fallan en contextos extensos o bajo alta carga de razonamiento.
3. **Espacio de Búsqueda Infinito:** La prohibición describe lo que *no* se debe hacer, dejando un espacio de estados residual infinito sin un vector de gradiente claro.

### 4.2 Especificación Afirmativa de Dominios Cerrados ("Instead, Do X")
La **Guía Positiva** define con precisión milimétrica la única rama válida que el modelo debe transitar, sustituyendo restricciones difusas por condiciones ejecutables.

### 4.3 Matriz de Conversión: De Negativismo Novato a Positive Guidance SOTA

| Intención / Objetivo | Directiva Negativa Novata (Legacy) ❌ | Especificación Positiva SOTA (CoHaLo v7.0) ✅ | Justificación Técnica |
|---|---|---|---|
| **Formato de Salida** | *"No uses markdown, no agregues saludos, no pongas texto, solo dame el json."* | `Emit strictly a valid JSON object matching <schema>, starting with '{' and ending with '}'.` | Guía la decodificación directamente hacia los delimitadores JSON sin activar tokens de texto. |
| **Límites de Longitud** | *"Prohibido escribir respuestas largas o aburridas. No te extiendas."* | `Constrain the response to a concise summary of 3 to 5 bullet points, each under 20 words.` | Reemplaza adjetivos subjetivos por cotas numéricas medibles en la ventana de contexto. |
| **Manejo de Incertidumbre** | *"No inventes cosas que no sepas, no alucines jamás."* | `If the requested parameter is not present in <context>, emit strictly 'DATA_UNAVAILABLE'.` | Provee una rama de retorno determinista (*fallback branch*) en lugar de un mandato negativo ambiguo. |
| **Estilo y Redacción** | *"No uses lenguaje coloquial, no uses muletillas, no uses adjetivos vacíos."* | `Compose the response using formal technical prose with precise domain terminology.` | Establece el espacio léxico afirmativo deseado. |
| **Súplicas Emocionales** | *"Te daré 200$ de propina, mi empleo depende de esto, por favor hazlo bien."* | `Verify all outputs against the deterministic criteria defined in <acceptance_criteria>.` | Elimina ruido que contamina el KV cache; sustituye súplicas por criterios de aceptación formales. |

---

## 5. Modelos de Razonamiento Nativos (o1, o3, Claude 3.7 Thinking, Gemini 3)

1. **Extirpación de Pseudo-CoT en Texto Visible:**
   - *Práctica Deprecada:* Instrucciones como *"Piensa paso a paso"* o *"Razona antes de contestar"*.
   - *Causa de Degradación:* Provocan colisión y redundancia con los tokens de razonamiento interno deliberativo nativo del modelo.
   - *Práctica SOTA:* Calibrar el presupuesto de inferencia en la API (`reasoning_effort` o `thinking_budget`) y mantener el system prompt puramente declarativo.
2. **Declaración de Invariantes y Condiciones de Frontera:**
   - Suministrar al modelo de razonamiento: (1) Estado inicial, (2) Invariantes que deben conservarse en toda transición, y (3) Condiciones deterministas de parada.
3. **Structured Outputs Nativo (Constrained Decoding):**
   - Validación mediante esquemas JSON Schema / Pydantic acoplados a gramáticas libres de contexto (CFG) durante la generación de tokens, garantizando 100% de cumplimiento sintáctico.

---

## 6. Estrategia Few-Shot de Alta Densidad
- **Zero-Shot First:** En modelos frontera y de razonamiento, validar primero en Zero-Shot con especificaciones claras.
- **Cuándo aplicar Few-Shot:** Únicamente para formatos de salida complejos o calibración de casos límite (*edge cases*).
- **Diversidad Controlada:** Proveer entre **3 y 5 ejemplos diversos** que cubran discrepancias y bordes del dominio, evitando listas homogéneas que inflan el contexto.

---

## 7. Calibración de Hiperparámetros de Inferencia
| Tipo de Tarea | Temperatura | Top-P | Justificación |
|---|---|---|---|
| **Arquitectura, Código, Manifiestos, Schemas** | `0.0` a `0.1` | `0.05` a `0.1` | Máxima reproducibilidad, consistencia determinista y minimización de varianza. |
| **Análisis Comparativo, Heurísticas** | `0.2` a `0.3` | `0.2` | Mantiene rigor lógico permitiendo flexibilidad en estructuración de explicaciones. |
| **Diseño Creativo, Naming, Copywriting** | `0.7` a `0.9` | `0.9` | Amplitud léxica controlada dentro de los límites del esquema. |
