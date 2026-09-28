# CoHaLo Reference Manual: Context Engineering, 4Rs, Caching & Anti-Rot

## 1. Definición Formal de Context Engineering
> **Context Engineering** es la disciplina de **curar y optimizar el conjunto de tokens durante la inferencia**. Resuelve qué información ingresa a la memoria de trabajo del modelo, de dónde proviene y qué se desecha cuando ya no cabe.
> 
> *El verbo principal no es escribir; es **decidir**. Y decidir incluye **quitar**.*

---

## 2. Los 4 Principios Fundamentales de Auditoría (Las 4Rs)

### 1. Relevance (Relevancia) — *Principio Raíz*
- **Regla:** Encontrar el conjunto más pequeño posible de tokens de alta señal que maximice la probabilidad del resultado deseado.
- **Evidencia Dura:** Modelos con catálogos inflados (46 tools) fallan por indecisión; al podar a 19 tools esenciales, el éxito sube drásticamente.
- **Pregunta de Auditoría:** *"Si elimino esta línea o herramienta, ¿cambia la respuesta? Si no cambia, sobra."*

### 2. Recency (Recencia) — *Lo Nuevo vence a lo Viejo*
- **Regla:** Las correcciones y el estado presente deben sobreescribir las asunciones tempranas.
- **Evidencia Dura:** Investigaciones de Microsoft & Salesforce en 200k+ conversaciones demuestran una caída del **39% en rendimiento** en multi-turno cuando se arrastran errores tempranos.
- **Pregunta de Auditoría:** *"¿La información obsoleta se puede morir o solo se acumula en el historial?"*

### 3. Retrieval (Búsqueda / Just-in-Time) — *Buscar en vez de Cargar*
- **Regla:** En lugar de precargar todo en el prompt, mantener referencias ligeras (rutas de archivo, links, IDs) y cargar datos bajo demanda usando herramientas.
- **Trade-off:** La búsqueda añade latencia; la arquitectura óptima es híbrida (cargar directivas críticas arriba y buscar detalles JIT).
- **Pregunta de Auditoría:** *"¿Esto tiene que estar aquí siempre o solo cuando se solicite?"*

### 4. Ranking (Posicionamiento Espacial) — *El Dónde pesa tanto como el Qué*
- **Regla:** La atención de los transformers decae en el centro de la ventana (*Lost in the Middle*).
- **Evidencia Dura:** Un dato al inicio o final tiene 70-75% de exactitud; al medio cae a 55-60% (15-20 puntos de degradación por posición).
- **Regla Query at the End:** Colocar datos masivos arriba y la query/instrucciones específicas al final para ganar hasta un 30% en precisión.
- **Pregunta de Auditoría:** *"¿Lo más crítico está donde más se ve (al inicio o al final)?"*

---

## 3. Diagnóstico de Fallas por Contexto Contaminado

| Tipo de Falla | Síntoma Observable | Acción Correctiva Determinista |
|---|---|---|
| **Envenenamiento (Poisoning)** | La IA insiste con firmeza en un dato falso o alucinado y lo repite. | **Abrir sesión nueva limpia** (corregir en el chat solo agrega ruido). |
| **Distracción (Distraction)** | Entra en loops, repite lo que ya fracasó o da la misma idea con otras palabras. | **Compactar contexto y reiniciar.** |
| **Confusión (Confusion)** | Elige la herramienta equivocada o rehúsa usarla cuando debería. | **Podar catálogo de herramientas.** |
| **Choque (Clash)** | Respuestas contradictorias o inconsistentes entre turnos. | **Eliminar duplicaciones y conflictos en instrucciones.** |
| **Degradación Normal** | Olvida datos o directivas del principio de la sesión. | **Mover a Memoria Persistente (LTM) o System Prompt.** |

---

## 4. Mitigación de Context Rot en Horizontes Largos
El **Context Rot** es la erosión progresiva de coherencia a medida que la ventana se llena. Se combate con 4 técnicas:
1. **Compactación:** Resumir el estado actual, registrar los invariantes y arrancar una ventana limpia.
2. **Poda de Outputs (Pruning):** Eliminar volcados crudos de herramientas pasadas (la conclusión se conserva, el volcado crudo se va).
3. **Notas Estructuradas (Offloading):** Escribir planes, reportes y estado intermedio en disco (`/var/www/artifacts/`) y re-leer bajo demanda.
4. **Subagentes:** Delegar tareas a workers efímeros que nacen y mueren con una ventana de contexto 100% limpia.

---

## 5. Asignación Espacial de Información (Los 5 Contenedores)
1. **System Prompt:** Identidad, restricciones duras, formato invariable. (Aplica siempre).
2. **User Prompt:** Tarea del turno actual. (Cambia cada turno).
3. **Memoria (LTM):** Preferencias, estado del proyecto, decisiones históricas. (Persiste entre sesiones).
4. **Herramientas (JIT):** Datos dinámicos o masivos que cambian o no caben en el prompt.
5. **Artefactos (Disco):** Entregables extensos, código fuente y planes de ejecución.

---

## 6. Jerarquía de Prefijos & Optimización de Caché KV
Para garantizar 100% de cache hits:
- **Nivel 1 (Inmutable):** Definiciones de Herramientas (Tools).
- **Nivel 2 (Estático):** System Prompt y Manuales SSoT.
- **Nivel 3 (Dinámico):** Mensajes de conversación e inputs de turno.
*Cualquier mutación en un nivel superior invalida ese nivel y todos los subsiguientes en la caché KV.*

---

## 7. Protocolo Anti-Psicofancia (Anti-Sycophancy)
1. No inducir conclusiones en la pregunta (Preguntar *"¿Qué observas en este código?"* en vez de *"Creo que esto está mal, ¿verdad?"*).
2. Solicitar activamente el contra-argumento (*"Presenta el mejor argumento técnico en contra"*).
3. Inyectar directivas de contradicción constructiva en el **System Prompt**, nunca en el chat efímero.
4. Evaluar contra rúbricas objetivas y sensores deterministas.
