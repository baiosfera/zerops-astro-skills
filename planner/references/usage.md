# Planner Reference Manual: Operational Usage & Dual-RAG Architecture (v9.1)

> **SSoT Reference Document:** `/var/www/.agents/skills/planner/references/usage.md`  
> **Meta-Skill:** [`planner`](file:///var/www/.agents/skills/planner/SKILL.md)  
> **Archetype:** Cognitive, Planning & Governance Methodology  
> **Standard:** Dual-RAG Pattern (Docu v8.2), Fractal CoHaLo v8.4 & Supreme Directive v8.3.

---

## 1. Misión, Dúo Inseparable & Especialización JIT

La meta-skill `planner` no es un documento estático ni un receptor pasivo de texto; es el **orquestador central de gobernanza y planificación** estructurado sobre una arquitectura simétrica:

1. **El Dúo Inseparable de Planner (Rigor Simétrico de Entrada y Salida):**
   - **Entrada Blindada:** [`research`](file:///var/www/.agents/skills/research/SKILL.md) garantiza Inflow Epistémico sin asunciones estáticas (Anti-AMN).
   - **Salida Blindada:** [`skill-improver`](file:///var/www/.agents/skills/skill-improver/SKILL.md) garantiza Cero Eliminación y No-Mutilación de directivas previas en Track A.
2. **Skills Especializadas JIT (Bajo Demanda Real & Sensor Físico):**
   - [`cohalo`](file:///var/www/.agents/skills/cohalo/SKILL.md), [`docu`](file:///var/www/.agents/skills/docu/SKILL.md) y [`skill-creator`](file:///var/www/.agents/skills/skill-creator/SKILL.md) se activan únicamente cuando la tarea ejecuta su arnés físico y corre un sensor determinista en la Matriz de Control (Sección 5). Se vetan usos como membrete cosmético ("compliance theater"); cada skill invocada atestigua una aserción física real.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PLANNER ORCHESTRATOR                              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                   ┌───────────────────┴───────────────────┐
                   ▼                                       ▼
        ┌─────────────────────┐                 ┌─────────────────────┐
        │   research (F0)     │                 │ skill-improver (F5) │
        │  ENTRADA: Anti-AMN  │                 │ SALIDA: Zero-Loss   │
        └─────────────────────┘                 └─────────────────────┘
                   │                                       │
        ───────────┴───────────────────────────────────────┴───────────
                           Skills Especializadas JIT
               ┌───────────────────────┼───────────────────────┐
               ▼                       ▼                       ▼
        ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
        │   cohalo    │         │    docu     │         │skill-creator│
        │ Arneses     │         │ Dual-RAG    │         │ Scaffolding │
        │ Bounded 10s │         │ C1–C5 Arch  │         │ 4 Archetypes│
        └─────────────┘         └─────────────┘         └─────────────┘
```

### 1.1 `research` — Epistemic Grounding & Verbatim Extraction (Fase F0)
- **Activación:** Previo a cualquier diseño o afirmación técnica en arquitectura.
- **Modalidades de Ejecución:**
  - **Modality A (JIT Inline):** 1 hecho atómico o versión. Cascada rápida: `mem_search` $\to$ Exa / Tavily / DDG $\to$ Jina Reader (`r.jina.ai/<url>`).
  - **Modality B (Subagente Obligatorio):** Análisis multifuente, bugs complejos o cambios de arquitectura. Inyecta [`subagent_prompt_contract.md`](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md), escribe reporte exhaustivo en `/var/www/artifacts/<target>_research_report.md` (>10KB) y emite recibo `<epistemic_attestation>`.
- **Invariante:** Prohibido emitir texto o diseñar planes sin haber ejecutado las herramientas de grounding.

### 1.2 `cohalo` — Context, Harness & Loop Architecture
- **Context (Co):** KV-cache stability mediante Positive Guidance. Router ejecutivo acotado ($\le 450$ palabras para skills regulares, $\le 2500$ tokens para orquestadores de dominio). Desacoplamiento modular en `references/`.
- **Harness (Ha):** Ejecución acotada (`timeout 10s`), espera asíncrona segura (`WaitMsBeforeAsync: 10000`), limpieza proactiva de tareas huérfanas (`manage_task action="kill"`), atestación física determinista (`exit code 0` o `HTTP 200`), y cero residuos de compilación (cero `__pycache__` vía AST en memoria).
- **Loop (Lo):** Máquina de estados finita F0–F5 regida por [`00-SUPREME-DIRECTIVE.md`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md). Transición a F5 bloqueada hasta recibir el `"go"` explícito del usuario humano en `USER_INPUT`.

### 1.3 `docu` — Dual-RAG Architecture & Certification Gate (Fase F2)
- **Estructuración Dual-RAG:** Toda habilidad se desacopla en tres niveles:
  1. *Nivel 1 (Discovery):* Metadatos YAML en frontmatter (`name`, `description` con triggers exhaustivos).
  2. *Nivel 2 (Activation Router):* `SKILL.md` ejecutivo ($\le 450$ palabras) con reglas duras y compuertas de decisión.
  3. *Nivel 3 (Deep Knowledge):* `references/usage.md` (manual integral) y `references/infra.md` (para servicios de plataforma).
- **Compuerta de Certificación (C1 a C5):** Auditoría estricta contra los 5 criterios de [`docu/references/certification.md`](file:///var/www/.agents/skills/docu/references/certification.md). Si se cumplen, se emite el dictamen de invariancia (Zero Gratuitous Churn) preservando 0 bytes de modificación en disco.

### 1.4 `skill-improver` — Universal Zero Deletion Invariant (Fase F5 - $N_4$)
- **Activación:** Refactorización, saneamiento y optimización de skills existentes.
- **Invariante C3 (Zero Deletion):** Preserva el 100% de reglas, métodos, directivas, compuertas de decisión y contratos de error. Está terminantemente prohibido amputar o resumir conocimientos; la reducción del router se logra modularizando hacia `references/usage.md`.

### 1.5 `skill-creator` — Canonical Skill Scaffolding (Fase F5)
- **Activación:** Creación de nuevas habilidades sin precedentes.
- **Clasificación en 4 Arquetipos:** Framework, Infra, Domain o Cognitive. Despliega la plantilla canónica con arnés de validación determinista en `scripts/<target>-validate.sh`.

---

## 2. Gobernanza Tri-Track SSoT & Máquina de Estados F0–F5

Todo plan generado bajo `planner` se bifurca formalmente en una de tres pistas operativas:

### 2.1 Track A: Skill Governance & SSoT Tooling
Aplica a cambios en el ecosistema de habilidades (`.agents/skills/`), scripts Python de plataforma, scripts aprovisionadores (`setup-*.sh`, `unisetup.sh`, `iniciar.sh`) y directivas de gobernanza maestras.
Ejecuta de forma rigurosa la **Topología Cerrada de 8 Nodos**:
1. **$N_1$ (Backup Pre-Mutación):** Snapshot plano $O(1)$ en `0zcp-123/bak/skills/<name>_v<ver>_<date>.bak/` o `0zcp-123/bak/scripts/<name>_<date>.bak`.
2. **$N_2$ (Mapeo SSoT unisetup.sh):** Registro del activo en `unisetup.sh` y scripts provisionadores correspondientes.
3. **$N_3$ (SemVer Invariant):** Incremento semántico en YAML frontmatter y cabeceras de script.
4. **$N_4$ (Zero Deletion & CoHaLo):** Verificación física de preservación total de directivas vía `skill-improver` / `docu` C3.
5. **$N_5$ (Espejo Google Drive):** Sincronización atómica bidireccional hacia `0zcp-123/`.
6. **$N_6$ (Sensores Físicos):** Ejecución de `<skill>-validate.sh` y `skills-suite-validate.sh` retornando `exit code 0`.
7. **$N_7$ (Skill Registry):** Refresco y validación independiente vía `gentle-ai skill-registry refresh --force`.
8. **$N_8$ (Auto-Purge & LTM):** Purga de planes temporales en `/var/www/artifacts/` y persistencia en Engram mediante `mem_save`.

### 2.2 Track B: Zerops Workload Deployment
Aplica a código de aplicaciones, microservicios, bases de datos y pipelines de CI/CD en Zerops (`/var/www/{service}/`).
- Consume [`bknd`](file:///var/www/.agents/skills/bknd/SKILL.md) y [`frnt`](file:///var/www/.agents/skills/frnt/SKILL.md) como tablas de enrutamiento.
- **Rollback y versionado NATIVO en Git/GitHub:** El control de versiones y rollback de código se delega soberanamente a Git/GitHub (ramas, tags y commits), eliminando respaldos monolíticos de repositorios hacia carpetas `.bak`.
- **Exención de 8 Nodos y Backups Redundantes:** Despliegues greenfield (servicios nuevos) o cambios en repositorios prescinden de respaldo pre-mutación en `bak/` y pasos de `unisetup.sh`.
- Validación pre-vuelo estricta con `zcp-validate yaml <import.yaml>`.
- Despliegue GitOps y verificación en vivo vía subdominio Zerops (`HTTP 200 OK`).

### 2.3 Track C: Direct SSoT Data, Content & Business Assets
Aplica a modificaciones directas de documentos Markdown, brandbooks, JSONs de configuración de negocio, plantillas de correo y assets en Google Drive (`/var/www/baiosfera/...`).
- **Cero ceremonias de plataforma:** Prescinde de respaldos en `bak/` (Google Drive provee historial nativo de versiones y papelera), `unisetup.sh`, SemVer en frontmatter y refresco de `skill-registry`.
- **Ciclo ágil:** Paso 1 (Grounding e Inspección), Paso 2 (Mutación Quirúrgica / Transformación), Paso 3 (Validación de Integridad de Esquemas / Links) y Paso 4 (Persistencia en Engram LTM vía `mem_save`).

---

## 3. Matriz de Decisiones & Casos de Uso

| Caso de Uso / Necesidad | Skill Responsable | Protocolo / Acción | Referencia Canónica |
|---|---|---|---|
| Inflow Epistémico / Grounding | `research` | Recibo formal `<epistemic_attestation>` | [`research/SKILL.md`](file:///var/www/.agents/skills/research/SKILL.md) |
| Auditoría de Skills / Invarianza | `docu` | Verificación de 5 criterios C1–C5 | [`docu/references/certification.md`](file:///var/www/.agents/skills/docu/references/certification.md) |
| Refactorización sin Pérdida | `skill-improver` | Modularización a `references/usage.md` | [`skill-improver/SKILL.md`](file:///var/www/.agents/skills/skill-improver/SKILL.md) |
| Nueva Habilidad | `skill-creator` | Scaffolding canónico de 3 niveles | [`skill-creator/SKILL.md`](file:///var/www/.agents/skills/skill-creator/SKILL.md) |
| Arneses & Presupuesto Tokens | `cohalo` | Bounded execution (`timeout 10s`) | [`cohalo/SKILL.md`](file:///var/www/.agents/skills/cohalo/SKILL.md) |
| Despliegue de Workload Zerops | `bknd` / `frnt` | Validación `zcp-validate` y CI/CD | [`bknd/SKILL.md`](file:///var/www/.agents/skills/bknd/SKILL.md) · [`frnt/SKILL.md`](file:///var/www/.agents/skills/frnt/SKILL.md) |
| Validación de Plan en Disco | `planner` | `plan-validate <plan.md>` (<100ms) | [`scripts/plan-validate.sh`](file:///var/www/.agents/skills/planner/scripts/plan-validate.sh) |
| Linear Roadmap Sync (Epics) | `linear` | Sincronización de Epics/Roadmap | [`mcp/linear/`](file:///var/www/baiosfera/0ZEROPS-AGY/0zcp-123/mcp/schemas/linear/) |
| Sensor Físico de la Skill | `planner` | `bash scripts/planner-validate.sh` | [`scripts/planner-validate.sh`](file:///var/www/.agents/skills/planner/scripts/planner-validate.sh) |

---

## 4. Estándar de Planes en Disco, Halt Gate & Ciclo de Auto-Purga

1. **Ruta Transitoria:** Todo plan se redacta en español en `/var/www/artifacts/<plan_name>_vN.md` con `RequestFeedback: false`, en formato condensado de alta densidad.
2. **Invariante de Versionamiento Evolutivo Acumulativo (Anti-Amnesia):** Toda nueva versión `_v(N+1).md` es obligatoriamente un superset estricto de `_vN.md`. Preserva el 100% de requerimientos funcionales, tareas, rutas y descubrimientos previos, depurando exclusivamente lo erróneo y sumando el nuevo alcance sin pérdida de contexto.
3. **Mandato Anti-Desbocado & F4 Halt Gate:** La ejecución de código de aplicación requiere autorización explícita previa ('Go' del usuario). Todo plan debe ser validado físicamente con `plan-validate <ruta>` arrojando `exit code 0` y el agente debe detenerse a esperar el `"go"` humano.
4. **Política Cuantitativa de Linear:** Linear es obligatorio para macro-tareas (>10k tokens, multi-archivo, multi-sesión) asegurando persistencia de estado inter-sesión sin saturar la ventana de contexto. Las micro-tareas (fixes puntuales o modificaciones de un solo archivo) ejecutan directamente sin emisión de tickets en Linear para economía de tokens.
5. **Archival & Purga Post-Atestación:** Una vez completada la Fase F5 y confirmada por sensores físicos, el plan se archiva mediante `plan-archive <plan> --executed`, purga automáticamente borradores superseded obsoletos en `artifacts/archive/` y se almacena el resumen final en Engram (`mem_save`), garantizando cero acumulación de deuda técnica.
