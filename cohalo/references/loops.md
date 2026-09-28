# CoHaLo Reference Manual: Loop Engineering & State Machine Architecture

## 1. Arquitectura Tridimensional CoHaLo
CoHaLo desacopla la ejecución de agentes en tres capas concéntricas e interdependientes:

```
┌─────────────────────────────────────────────────────────────┐
│                       LOOP LAYER                            │
│  State Machine: Grounding → Gate → Docu → Validate → Verify │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  HARNESS LAYER                        │  │
│  │   Guides: Validators, Schemas, Process & FS Shield    │  │
│  │   Sensors: HTTP 200, Sensor Attestation, Linters      │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │               CONTEXT LAYER                     │  │  │
│  │  │  Epistemic Inflow, Token Budgets, Offloading,   │  │  │
│  │  │  Cumulative Evolution, Fractal Isomorphism      │  │  │
│  │  │  ┌───────────────────────────────────────────┐  │  │  │
│  │  │  │             FOUNDATION MODEL              │  │  │  │
│  │  │  │     (NLP Engine, NEVER a Knowledge Base)  │  │  │  │
│  │  │  └───────────────────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Máquina de Estados de 6 Fases (Gated State Machine)

Todo flujo de trabajo agéntico o implementación multi-paso debe atravesar secuencialmente las 6 fases:

| Fase | Nombre | Invariante de Transición Dura |
|---|---|---|
| **Fase 0** | **Epistemic Grounding** | Consulta obligatoria a memoria (`engram`) e investigación en vivo (`research` / `zerops_knowledge`) para obtener hechos técnicos atestados en tiempo real. |
| **Fase 1** | **Clarification Gate (HARD STOP)** | Si faltan hostnames, SO base (`ubuntu`/`alpine`) o variantes de BD (`:single`/`:ha`), formular preguntas concretas y **DETENERSE INMEDIATAMENTE**. |
| **Fase 2** | **Dual-RAG Documentation & Fractal Compilation** | Verificar la existencia de `.agents/skills/<target>/references/infra.md` y `usage.md` antes de planificar. Compilar en cada skill sus propios arneses de ejecución y circuit breakers (`docu`). |
| **Fase 3** | **Topological Validation** | Ejecutar validación de manifiestos con `zcp-validate yaml <import.yaml>` y verificar montaje de volúmenes persistentes. |
| **Fase 4** | **Plan Offloading** | Escribir plan exhaustivo en `/var/www/artifacts/<plan_name>.md`. En el chat emitir solo el enlace y esperar aprobación humana. |
| **Fase 5** | **Execution & Attestation** | Desplegar vía Git/GGA (Receipt-Driven Development), verificar con sensor (HTTP 200 / exit code 0), auto-purgar planes y guardar hito en `engram` (`mem_save`). |

---

## 3. Circuit Breakers y Bucles de Auto-Remediación

1. **Límite de Intentos de Auto-Corrección**:
   - Cuando un sensor de salida detecta un error de compilación o runtime, el arnés permite un máximo de **2 ciclos de corrección autónoma**.
2. **Escalación a Humano**:
   - Si tras 2 intentos el fallo persiste, el circuito se abre: el agente recopila la traza exacta del sensor, detiene la ejecución y solicita clarificación o intervención humana sin entrar en bucles infinitos.
3. **Receipt-Driven Development (RDD)**:
   - Toda mutación de código en producción se efectúa a través de commits convencionales auditables y pipelines de CI/CD.

---

## 4. Persistencia Agéntica & Subagentes con Ventana Limpia

1. **Bucle de Persistencia Autónoma:**
   - El agente no cede control prematuramente ante un error recuperable; inspecciona, ajusta su plan y continúa hasta completar el objetivo o alcanzar el límite del circuit breaker.
2. **Aislamiento por Subagentes (Clean Context Workers):**
   - Para tareas complejas de exploración o mutación profunda, delegar la ejecución a subagentes que inician con una ventana de contexto 100% limpia.
   - El subagente realiza el trabajo pesado y retorna únicamente una síntesis compacta de alta señal (1.000 a 2.000 tokens), previniendo la contaminación y el *Context Rot* del hilo principal.
