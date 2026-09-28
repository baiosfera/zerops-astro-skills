# CoHaLo Reference Manual: SOTA Reasoning & Agentic Prompting (Continuous Present)

## 1. Concepto Fundamental
En el Presente Continuo Dinámico, los modelos frontera se dividen en dos categorías complementarias:
1. **Modelos de Razonamiento Nativo ("The Planners"):** (OpenAI o1/o3/o4-mini, Claude 3.7 Extended Thinking, Gemini 3 Thinking). Cuentan con bucles internos de pensamiento oculto/visible y tokens dedicados a la deliberación formal.
2. **Modelos de Ejecución Rápida ("The Workhorses"):** (GPT-4o, Claude Sonnet 4.6/5, Gemini 2.5 Flash). Optimizados para baja latencia, llamadas a herramientas en bucle y transformaciones directas.

---

## 2. Prompting para Modelos de Razonamiento Nativos
Los modelos de razonamiento aprovechan su propio motor interno de deliberación estructurada.

### Reglas de Oro para Modelos de Razonamiento:
1. **Autonomía del Razonamiento Nativo:**
   - Calibrar el presupuesto de pensamiento mediante parámetros de API (`reasoning_effort: "low"|"medium"|"high"` o `budget_tokens: 4096`) y permitir la deliberación nativa del modelo, estructurando el prompt con invariantes duros, condiciones de frontera y criterios deterministas.
2. **Especificación Exhaustiva del Problema & Invariantes:**
   - Proporcionar objetivos nítidos, condiciones de frontera, casos límite y criterios de parada inequívocos.
3. **Cero-Shot First:**
   - Evaluar siempre el comportamiento en Zero-Shot antes de agregar ejemplos Few-Shot que puedan sesgar el camino de deducción del modelo.

---

## 3. Protocolo de Planificación Explícita (`<planning_process>`) & Auto-Crítica
Para tareas complejas de arquitectura o refactorización:

```xml
<planning_process>
1. Análisis de Metas: Descomponer el objetivo en sub-tareas atómicas e independientes.
2. Chequeo de Completitud: Evaluar si los datos provistos en <context> son suficientes. Si faltan datos críticos, detenerse y solicitar clarificación.
3. Selección de Estrategia: Identificar la ruta óptima de ejecución antes de mutar el estado.
4. Auto-Crítica Pre-Emisión: Revisar la solución contra los invariantes del usuario antes de retornar la respuesta final.
</planning_process>
```

---

## 4. Arneses para Tool Calling Agéntico

### A. Directiva de Persistencia Agéntica (Persistence Directive)
Los agentes autónomos deben operar de manera proactiva hasta la resolución total del problema:
- Trabajar de forma continua y autónoma hasta que la meta esté completamente verificada.
- Si una herramienta o comando falla, analizar la causa raíz del error y probar una ruta alternativa sin ceder control prematuramente al usuario.
- Ceder el control únicamente tras haber atestado el resultado final mediante sensores deterministas.

### B. Pre-Computación Reflexiva (Tool Reflection)
Antes de invocar cualquier herramienta de inspección o mutación, el agente debe declarar internamente o en su arnés:
1. **Motivo:** Por qué se invoca la herramienta.
2. **Expectativa:** Qué datos o estado específico se espera obtener.
3. **Aporte:** Cómo esa información contribuye a la resolución del objetivo.

### C. Optimización de Tool Calls Paralelos vs Secuenciales
- **Llamadas Independientes en Paralelo:** Si se requiere leer 3 archivos o ejecutar 3 búsquedas sin dependencias mutuas, ejecutarlas en un único lote paralelo para maximizar velocidad y reducir turnos.
- **Llamadas Dependientes en Secuencia:** Si una llamada depende de los parámetros de salida de la anterior, ejecutarlas estrictamente en secuencia sin inventar parámetros preliminares.

---

## 5. Ejecución de Código & Manejo de Datos Extensos
Al interactuar con bases de datos o entornos bash:
- Usar comandos selectivos (`head`, `tail`, `grep`, `jq`, `LIMIT`) para inspeccionar datos masivos.
- **Procesamiento Selectivo:** Inspeccionar esquemas, métricas agregadas o subsets representativos, manteniendo datasets voluminosos procesados fuera de la ventana de contexto.
