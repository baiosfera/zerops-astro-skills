# CoHaLo Reference Manual: Context Engineering, KV Cache & Progressive Disclosure (v7.0)

## 1. Concepto Fundamental
La capa de **Context Engineering** gobierna la memoria de trabajo y la superficie de atención del modelo de lenguaje durante la inferencia. En la arquitectura CoHaLo, los pesos pre-entrenados operan estrictamente como un **motor semántico de razonamiento en tiempo real**, jamás como una base de datos estática.

> **Principio de Preservación Invariante (Lossless Token Economy):**
> La economía de tokens en CoHaLo se logra mediante **Progressive Disclosure** (carga por niveles) y **Estabilidad de Prefijo KV Cache**, NUNCA mediante la mutilación, el resumen ciego o la pérdida de conocimiento técnico. Todo algoritmo, tipo de dato, parámetro de configuración y código de error se preserva íntegramente.

---

## 2. Jerarquía Cuadridimensional de Prefijo KV Cache (100% Cache Hits)
En motores de inferencia de alto rendimiento (vLLM PagedAttention, SGLang RadixAttention, y APIs con Prompt Caching), la caché KV se evalúa secuencialmente desde el token 0. Cualquier mutación en el prefijo inicial invalida el 100% de la caché subsiguiente.

Para alcanzar una tasa de acierto de caché de hasta el 100% (reducción del 90% en costos y latencia sub-segundo), CoHaLo impone la siguiente estructura jerárquica estricta:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ NIVEL 1 — INMUTABLE (Token 0): Definiciones de herramientas y esquemas │
│             Serializados en orden alfabético estricto determinista.    │
├────────────────────────────────────────────────────────────────────────┤
│ NIVEL 2 — ESTÁTICO: Directivas centrales del sistema (SSoT)            │
│             Reglas de gobernanza inmutables y catálogo de skills.      │
├────────────────────────────────────────────────────────────────────────┤
│ NIVEL 3 — SEMI-ESTÁTICO: Documentación de referencia JIT y memoria LTM │
│             Memoria de largo plazo (Engram) y módulos cargados.        │
├────────────────────────────────────────────────────────────────────────┤
│ NIVEL 4 — DINÁMICO (Punta del Contexto): Mensaje del turno del usuario │
│             Inputs del turno actual y resultados efímeros de comandos. │
└────────────────────────────────────────────────────────────────────────┘
```

### Reglas de Caché KV:
1. **Inmutabilidad del Token 0:** Cero marcas de tiempo dinámicas (`Current time: ...`) al inicio del system prompt. Las marcas temporales se evalúan bajo demanda o se colocan en el estrato dinámico (Nivel 4).
2. **Serialización Determinista:** Todas las herramientas y módulos deben serializarse siempre en el mismo orden canónico para evitar invalidación accidental de tensores KV.

---

## 3. El Patrón de Progressive Disclosure (Divulgación Progresiva en 3 Niveles)
Para evitar el colapso de contexto (*context bloat*) y la degradación de atención (*Lost in the Middle*), la información se segmenta en tres niveles de granularidad:

- **Nivel 1 (Discovery):** Metadatos de catálogo (`name` + `description` con triggers explícitos). Consume ~50 a 100 tokens por skill en el System Prompt.
- **Nivel 2 (Activation):** Enrutador ejecutivo (`SKILL.md`). Se carga únicamente al activarse el trigger. Contenido ultra-denso de 180 a 450 tokens con directivas duras y compuertas de decisión.
- **Nivel 3 (Execution JIT):** Recursos especializados cargados bajo demanda Just-in-Time (`references/usage.md`, `references/infra.md`, esquemas en `assets/`, scripts en `scripts/`).

---

## 4. Auditoría de Contexto bajo el Marco de las 4Rs

1. **Relevance (Relevancia):** Mantener el mínimo conjunto de tokens de máxima señal. El exceso de herramientas degrada la precisión de selección (de 41% de error con 46 tools a 6% de error con 19 tools contextuales).
2. **Recency (Recencia):** El estado presente anula supuestos obsoletos. Arrastrar errores en turnos conversacionales degrada el rendimiento de la tarea en un 39% (*Context Poisoning*). Ante envenenamiento, se reinicia a una sesión limpia (*Concat-and-Retry*).
3. **Retrieval (Recuperación JIT):** Mantener punteros livianos (rutas relativas, IDs de memoria) en el prompt activo, cargando payloads completos únicamente cuando sea requerido.
4. **Ranking (Posicionamiento Espacial & Regla "Query at the End"):** La atención decae en el centro de la ventana (15-20 puntos porcentuales menos de recuerdo). Colocar las instrucciones específicas y la consulta concreta al final de la ventana incrementa hasta un 30% la precisión de respuesta.

---

## 5. Pipeline de Epistemic Inflow (Adquisición Epistémica Continua)
Toda aserción técnica sobre bibliotecas, arquitecturas, comandos o sintaxis debe fundamentarse en adquisición en vivo:

```text
[1. Fecha de Sistema]       ➔ date -u (Anclaje al Presente Continuo dinámico)
         ↓
[2. Memoria LTM]             ➔ engram (mem_search) para hitos previos
         ↓
[3. Triangulación Neural]    ➔ exa + tavily + brave + duckduckgo
         ↓
[4. Extracción Oficial]      ➔ context7 (docs de paquetes y tipos)
         ↓
[5. Extracción Verbatim]     ➔ Jina Reader (r.jina.ai/<url>) o scrapers locales
```

### Principio "Snippet is Not Evidence":
Los fragmentos de motores de búsqueda son meros índices de descubrimiento. La evidencia técnica vinculante requiere la lectura verbatim de la fuente canónica.

---

## 6. Mitigación de Context Rot & Higiene de Disco
- **Poda de Volcados Crudos (Raw Output Pruning):** Sintetizar la conclusión operativa tras invocar herramientas masivas y purgar el payload crudo del historial.
- **Offloading a Disco:** Escribir diagnósticos y planes en `/var/www/artifacts/` para mantener el chat minimalista.
- **Invariante de Auto-Purge:** Eliminar físicamente los planes temporales de `/var/www/artifacts/` inmediatamente después de la atestación por sensores físicos (`exit code 0`).
- **Subagentes Efímeros:** Delegar investigaciones profundas a subagentes con ventana de contexto limpia de 0 tokens.
