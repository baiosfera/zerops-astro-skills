# Planner Reference Manual: Operational Usage & Sovereign Governance Architecture (v10.0)

> **SSoT Reference Document:** `/var/www/.agents/skills/planner/references/usage.md`  
> **Meta-Skill:** [`planner`](file:///var/www/.agents/skills/planner/SKILL.md)  
> **Archetype:** Cognitive, Planning & Governance Orchestrator  
> **Standard:** CoHaLo Positivo v8.4, Skill-Improver & Supreme Directive v8.4.

---

## 1. Misión: El Supremo Gobernador de Orquestación

`planner` es la **habilidad gobernadora soberana** de todo el ecosistema en Zerops. No es un receptor pasivo ni un formato burocrático; es la autoridad directiva que subordina a todas las demás herramientas y skills:

1. **Subordinación Estricta de `grilling` & Mandato de Espera Epistémica F0:**
   - El grilling ceremonial indiscriminado desgasta al usuario y quema tokens innecesarios intentando averiguar lo que ya está en el código o en los documentos.
   - **Protocolo Facts-First:** Toda sesión arranca inspeccionando hechos en disco (`view_file`, `run_command`, `grep`) o delegando a subagentes exploradores `research`.
   - **Mandato de Espera Epistémica:** Al despachar subagentes de `research` (o tareas de investigación asíncronas), el agente debe aguardar la recepción e ingestión de los reportes de los subagentes antes de redactar conclusiones, formular planes o hacer preguntas de grilling. Informá brevemente que la investigación está en vuelo y aguardá su retorno en silencio.
   - Si la respuesta existe en el repositorio, la especificación o el historial, cero preguntas. Procedé directamente con la propuesta sustentada en hechos.
   - Si existe una bifurcación arquitectónica genuina con tradeoffs irreversibles (ej. elegir entre dos proveedores o modelos incompatibles), se formula **máximo 1 sola pregunta atómica a la vez** con opciones concretas y bien explicadas. Al preguntar, se detiene la ejecución inmediatamente y se espera respuesta.

2. **Invariante de Agrupación en Linear, Aislamiento de Borradores & Anti-Monolítico:**
   - **Aislamiento de Borradores en F0–F3:** Durante las fases de investigación, clarificación y alineación (F0 a F3), los planes preliminares residen estrictamente como borradores (`draft_<slug>.md`) en `/var/www/artifacts/plans/` o en memoria Engram (`mem_save`).
   - **Reserva de Ticketaje en F4:** La creación de proyectos o tareas `BAI-*` en Linear se reserva exclusivamente para F4 (Plan & Approval Gate), una vez que el Plan Maestro ha sido completado y el usuario ha otorgado un 'Go' explícito. Durante F0–F3, los descubrimientos se registran en Engram (`mem_save`).
   - **Desglose Modular Anti-Monolítico:** Descomponer stacks heterogéneos e iniciativas multi-servicio en issues `BAI-*` atómicos y comprobables por cada subsistema, framework o frontera de runtime (ej. Bifrost Gateway, pool FreeLLMAPI, NATS JetStream, Python Worker), evitando tickets gigantes indivisibles.
   - **Regla Inquebrantable:** Ningún issue `BAI-*` puede existir suelto o huérfano. Todo ticket de Linear debe pertenecer a un Plan / Proyecto padre.
   - **Contrato de Creación de Issues:** Cada issue nace obligatoriamente con:
     1. **Alcance explícito:** qué archivos y componentes se modifican, y qué queda expresamente fuera de alcance.
     2. **Criterios de aceptación verificables:** lista numerada de condiciones comprobables con comandos y resultados esperados.
     3. **Grounding verificado:** afirmaciones sobre el entorno o APIs web deben verificarse primero con `research` antes de ingresar al plan.
   - **Protocolo de Comentarios en Linear (Anti-Chat Amnesia):** En F4–F5, todo hallazgo técnico, tradeoff o decisión de arquitectura se registra inmediatamente como comentario en el issue (`linear-cli comment <ID> "..."`) antes de redactar la respuesta al usuario en chat. Esto garantiza la persistencia SSoT incluso tras compactions o muertes de sesión.
   - **Flujo de Proyecto:**
     ```bash
     # 1. Fijar o crear el Proyecto / Plan maestro
     linear-cli set-project "<Nombre o UUID del Proyecto>"
     # O crear un proyecto nuevo para una iniciativa mayor:
     linear-cli create-project "Nombre del Plan" "Descripción y objetivos"

     # 2. Crear las tareas agrupadas automáticamente bajo ese proyecto
     linear-cli create "Título de la Tarea" "Descripción, criterios de aceptación y contexto"
     ```
   - **Auto-Grouping & Bloqueo Físico:** `linear-cli` persiste el proyecto activo en `/var/www/artifacts/linear_active_project.json` y auto-resuelve el proyecto para toda nueva tarea. Si un agente intenta crear una tarea sin proyecto y no hay proyecto activo resoluble, `linear-cli` rechaza la creación físicamente con error.
   - **Economía de Tokens Inter-Sesión:** Toda la bitácora acumulada, decisiones y criterios de aceptación residen en el cuerpo del Issue en Linear. Esto permite que el chat se mantenga ultraliviano sin tener que reinyectar miles de tokens de contexto en cada turno.

3. **Thin Orchestrator & Bounded Delegation (Patrón Gentle-AI):**
   - El orquestador principal (AGY) mantiene un hilo de contexto delgado (Thin Orchestrator): **no carga archivos masivos (ej. 2.000 líneas) en su ventana principal si va a realizar múltiples modificaciones**.
   - **Regla de Delegación Bounded:** Si una tarea requiere editar >= 2 archivos no triviales, compilar suites completas o explorar directorios extensos, el orquestador define e invoca un subagente worker temporal (`invoke_subagent`).
   - El worker recibe el alcance específico, realiza las modificaciones, corre las comprobaciones locales y devuelve únicamente un reporte sintético con el diff y el resultado exit code 0.
   - El orquestador recibe el recibo, realiza la comprobación final de alto nivel y continúa, ahorrando decenas de miles de tokens de la ventana de contexto.

4. **Compuerta de Sensores Físicos & Pruebas de Comportamiento (Anti-Checklist Theater):**
   - Quedan erradicados los scripts sintéticos y validadores ceremoniales artificiales que bloquean o fallan con falsos positivos.
   - **Requisito de Comportamiento en Done:** Prohibido marcar `Done` basándose únicamente en validadores genéricos o meros lintings. El arnés requiere evidencia física de pruebas que ejerciten el comportamiento del cambio (`bun test`, `pytest`, o sensor que verifique el contrato modificado exit code 0).
   - La verdad reside en tres sensores físicos rápidos, baratos y deterministas:
     1. **Sensor de Sintaxis / Compilación:** `bun run build`, `python3 -m py_compile`, `node --check` o `bash -n` (exit code 0).
     2. **Sensor de Comportamiento:** `bun test`, `pytest` o tests unitarios dedicados del arnés (`tool-guard.py --test`) (exit code 0).
     3. **Sensor Funcional / Grep de Dominio:** comprobación viva mediante curl (`HTTP 200 OK`) o escaneo grep para verificar que no existan regresiones.
   - Solo cuando los sensores devuelven exit code 0, se procede a marcar la tarea como resuelta en Linear:
     ```bash
     linear-cli update-status <ID> "Done" --evidence "45 tests unitarios pasan exit code 0 (tool-guard.py --test) y py_compile exit 0"
     ```

5. **Arquitectura Lego Desacoplada & Upstream Inmutable:**
   - **Chasis Upstream:** `/var/www/zerops-astrobranding` es el plano maestro y esqueleto de Zerops. Permanece inmutable y desacoplado de la lógica de clientes.
   - **Plantilla Constructora:** `/var/www/artifacts/templates/plantilla-universal-web-zerops-v4.md` define el modelo arquitectónico para cualquier marca o proyecto.
   - **Workloads Derivadas:** Cada marca o aplicación tiene su propio repositorio de cliente (`<app>-prod` en `main`, `<app>-stage` en `stage`). El entorno de `stage` es efímero y se utiliza para verificar cambios a costo cero.
   - **Interconexión Dinámica:** Cero acoplamiento hardcodeado. Los servicios se conectan vía DNS interno privado de Zerops (`http://bifrost:8080`, `http://evolution:8085`, `http://listmonk:9000`).

---

## 2. Gobernanza Quad-Track SSoT & Máquina de Estados F0–F5

Todo plan generado bajo `planner` se bifurca formalmente en una de cuatro pistas operativas:

### 2.1 Track A: Skill Governance & SSoT Tooling
Aplica a cambios en el ecosistema de habilidades (`.agents/skills/`), scripts Python de plataforma, scripts aprovisionadores (`setup-*.sh`, `unisetup.sh`, `iniciar.sh`) y directivas de gobernanza maestras.
- Snapshot plano en `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/bak/skills/<name>_v<ver>_<date>.bak/`.
- Verificación de no-mutilación mediante `skill-improver`.
- Reflejo indivisible hacia Google Drive SSoT (`/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/`) y `git push origin main` a `zerops-astro-skills`.
- Sensor físico universal: `skills-suite-validate` retornando exit code 0.

### 2.2 Track B: Chasis Central Zerops Astrobranding
Aplica al chasis central `/var/www/zerops-astrobranding` (plantilla Astro 5 SSR compartida, tokens base y herramientas).
- Versionado y rollback nativo en Git/GitHub (ramas, tags y commits).
- Cierre con commit convencional y `git push origin main` al repositorio de `zerops-astrobranding`.

### 2.3 Track C: Workloads & Apps Derivadas (Plantilla Universal v4)
Aplica a aplicaciones de clientes y microservicios desplegados en Zerops (`webdev`, tiendas, APIs) derivados de la Plantilla Universal v4.
- Modelo GitOps Multi-Servicio (`<app>-prod` en `main`, `<app>-stage` en `stage`).
- Repositorio de cliente propio con remoto `origin` en GitHub. El chasis actúa estrictamente como `upstream` para recibir mejoras sin empujar código del cliente hacia él.
- Verificación física en vivo vía subdominio Zerops (`HTTP 200 OK`).

### 2.4 Track D: Direct SSoT Data, Content & Business Assets
Aplica a modificaciones directas de documentos Markdown, brandbooks, JSONs de configuración de negocio, plantillas de correo y assets en Google Drive (`/var/www/baiosfera/...`).
- Cero ceremonias de plataforma: Prescinde de respaldos en `bak/` (Google Drive provee historial nativo de versiones).
- Ciclo ágil: Inspección -> Mutación -> Validación de enlaces -> Persistencia en Engram LTM vía `mem_save`.

---

## 3. Matriz de Decisiones & Casos de Uso

| Caso de Uso / Necesidad | Skill Responsable | Protocolo / Acción | Referencia Canónica |
|---|---|---|---|
| Inflow Epistémico / Grounding | `research` | Inspección silenciosa previa; cero asunciones | [`research/SKILL.md`](file:///var/www/.agents/skills/research/SKILL.md) |
| Aclaración de Requisitos | `planner` | Facts-first; máx 1 pregunta atómica a la vez | [`SKILL.md`](file:///var/www/.agents/skills/planner/SKILL.md) |
| Linear Project Grouping | `linear-cli` | `linear-cli set-project` -> `create --project` | [`linear-cli`](file:///var/www/.bin/linear-cli) |
| Refactorización sin Pérdida | `skill-improver` | Modularización a `references/usage.md` | [`skill-improver/SKILL.md`](file:///var/www/.agents/skills/skill-improver/SKILL.md) |
| Nueva Habilidad | `skill-creator` | Scaffolding canónico de 3 niveles | [`skill-creator/SKILL.md`](file:///var/www/.agents/skills/skill-creator/SKILL.md) |
| Arneses & Presupuesto Tokens | `cohalo` | Bounded execution (`timeout 10s`, thin context) | [`cohalo/SKILL.md`](file:///var/www/.agents/skills/cohalo/SKILL.md) |
| Despliegue de Workload Zerops | `bknd` / `frnt` | Validación `zcp-validate` y CI/CD GitOps | [`bknd/SKILL.md`](file:///var/www/.agents/skills/bknd/SKILL.md) · [`frnt/SKILL.md`](file:///var/www/.agents/skills/frnt/SKILL.md) |
| Sensor Físico Universal | `skills-suite-validate` | `skills-suite-validate` exit code 0 | [`/usr/local/bin/skills-suite-validate`](file:///usr/local/bin/skills-suite-validate) |
| Sensor de Aplicación | `bun test` / `pytest` | Suite física de pruebas exit code 0 | `ssh <svc> "cd /var/www && npm test"` |

---

## 4. Política de Linear & Cierre en Memoria

1. **Política de Linear:** Linear es obligatorio para iniciativas de proyecto, tareas de múltiples archivos o trabajos entre sesiones, asegurando persistencia de estado sin saturar la ventana de contexto. Toda tarea `BAI-*` debe ser hija de un Proyecto en Linear (`linear-cli set-project`).
2. **Cierre de Memoria LTM:** Todo plan completado concluye registrando la bitácora arquitectónica ejecutando `mem_session_summary` en Engram, preservando los descubrimientos y archivos relevantes para la próxima sesión.
