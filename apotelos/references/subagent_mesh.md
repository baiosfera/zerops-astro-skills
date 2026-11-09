# Multi-Agent Mesh & Blackboard Pattern (Hermes, CrewAI & Zerops)

Authoritative guide for executing Apotelos swarms without memory leaks, context bloat, or redundant token burn.

---

## 1. The Blackboard Pattern vs Chaining Naive

In standard CrewAI, `Task(context=[...])` flattens all preceding outputs into a raw string `"\n".join([task.output.raw])`. For a 5-step reverse causality pipeline, this generates:
1. Quadratic token growth.
2. Loss of validated Pydantic types.
3. Confusion in LLMs from reading historical execution noise.

**The Apotelos Blackboard Solution**:
- Every step emits a structured schema written atomically to:
  `/.apotelos/manifests/{brand}_{vertical}.json` (or `$LOCAL_STORAGE_PATH/manifests/...`).
- Subsequent tasks receive **ONLY** the specific slice of state needed.
- Hermes acts as the supervisor, validating the intermediate state before the next crew starts.

---

## 2. Eliminating Redundant LLM Calls (`InternalInstructor`)

CrewAI's `output_pydantic` triggers an internal synchronous call via `converter.py:InternalInstructor` to parse raw text into Pydantic models using LiteLLM.

**Engineering Standard**:
1. In `universal_harness.py`, instruct the LLM directly via prompt engineering and JSON Mode (`response_format={"type": "json_object"}`).
2. Parse the output deterministically using Pydantic v2's native `model_validate_json(raw_text)` in Python memory.
3. Completely bypass `InternalInstructor` to save 50% token cost and eliminate rate-limit drops on free inference layers.

---

## 3. Physical Zerops Container Boundaries & Symmetric CLI Parity

- **Symmetric Native CLI Architecture (`/usr/local/bin/apotelos`)**:
  The `apotelos` executable is installed identically at `/usr/local/bin/apotelos` across both `zcp` (control plane) and `hermes` (agent execution runtime), sharing `/mnt/localstorage/MentorIA/dev/verticals/` and `/mnt/localstorage/playbooks/` with zero environment drift.
- **`zcp` Container (Control Plane)**:
  Runs `/usr/local/bin/apotelos` for discovery, static contract auditing, behavioral testing, and Linear coordination.
- **`hermes` Container (Ubuntu Python 3.12 Runtime)**:
  Runs `/usr/local/bin/apotelos` natively via shell (`run_command`) or python imports.
  Hosts `crewai==1.15.30`, `pydantic==2.12.5`, and `pydantic-ai-slim`.
  Exposes `POST /v1/runs` and streams execution deltas.
- **`bifrost` Container (Alpine Go 1.22 AI Gateway)**:
  Exposes OpenAI drop-in proxy on port 8080.
  Routes `vk-crewai` directly to FreeLLMAPI ($0 tier) with automatic failover to DeepSeek Pro tier.

---

## 4. Self-Healing Lifecycle via `zerops_manage`

If `hermes` or `bifrost` are stopped during kickoff:
```bash
# Auto-healed autonomously by ZCP without human manual intervention
zerops_manage action="start" serviceHostname="bifrost"
zerops_manage action="start" serviceHostname="hermes"
```
The CLI waits for HTTP 200 on `/healthz` before dispatching tasks.

---

## 5. PydanticAI como Schema Governor para Linear GraphQL y CrewAI

En el runtime Python (`hermes`), PydanticAI no compite con CrewAI; actúa como su **gobernador determinista de contratos**:
1. **Linear GraphQL Typed Tooling**: `pydantic-ai` modela `LinearIssueInput` y `LinearPlanSpec`. Toda descomposición de issues cumple estrictamente los invariantes anti-monolíticos (5 BAIs atómicos por vertical).
2. **Reintentos Estrictos (`ModelRetry`)**: Si el modelo propone un ticket sin criterios de aceptación o sin dependencias DAG, PydanticAI intercepta la validación y fuerza reintento local sin contaminar Linear.
3. **Pidev Equivalence**: `pidev` (Node/Bun) consume los esquemas compilados utilizando **Zod**, manteniendo paridad tipada 1:1 entre el backend Python y el frontend Astro.

---

## 6. Ruteo Asimétrico de Modelos (Razonamiento F1–F4 vs Ejecución F5)

Para optimizar costos (hasta 15x-20x) y velocidad sin perder rigor arquitectónico:
- **F1–F4 (Razonamiento, Arquitectura, Planificación y Grilling)**: Modelos Frontier Reasoning (**Claude 3.7 Sonnet / Opus 4.8**, **Argon Thinking**).
- **F5 (Scaffolding, Tool Calling, Tests, I/O)**: Modelos rápidos de alto rendimiento (**Gemini Flash 3.8 / 3.5**, Claude Haiku 4.5).
- **Bifrost CEL Gateway**: Gobierna el ruteo mediante Virtual Keys (`vk-planner` -> Reasoning tier; `vk-crewai-exec` -> FreeLLMAPI / Flash tier).

---

## 7. Dossier Markdown SSoT y Aislamiento de Memoria

Para evitar que Hermes, CrewAI o Pidev consuman tokens analizando documentos DOCX/PDF o redescubriendo verticales:
- Apotelos compila `/.apotelos/dossiers/{brand}_approved_dossier.md` y lo replica al volumen NVMe `/var/www/localstorage/dossiers/`.
- Todos los agentes leen este documento y los manifiestos JSON directamente como la Verdad Aprobada.

---

## 8. Arquitectura de Dos Capas y Workspaces Verticales Bounded Contexts

Para evitar que los agentes constructores (Hermes, CrewAI, PiDev) saturen el contexto escaneando docenas de archivos en la raíz de `dev/` o contaminen los tokens de diseño entre marcas:
1. **Capa 0 (Raíz `dev/`)**: Ingestión maestra del diagnóstico global (`brandbook.json`, `chroma_manifest.json`, `font_manifest.json`, `astrobranding_*.md`, `system_prompt.md`). Sincronizada bidireccionalmente con Google Drive SSoT vía `zcp-sync`. **Nunca se borra de la raíz.**
2. **Capa 1 (`dev/workspaces/{vertical_slug}/`)**: Espacios de trabajo aislados por vertical con 4 subcapas funcionales:
   - `brand/`: Tokens especializados asignados (`brandbook.json`, `chroma_manifest.json`, `theme.css`).
   - `strategy/`: Dossier consolidado, estrategia SEO/AEO (`seo.md`), psicología arquetípica.
   - `copy/`: Landings, ofertas, copys y secuencias de conversión.
   - `web/`: Especificaciones y contratos de componentes para PiDev / Astro 5 SSR.
3. **Resolución en Cascada para Herramientas**:
   - `get_brandbook_tokens(slug)`: Lee prioritariamente de `dev/workspaces/{slug}/brand/brandbook.json`; si no fue bifurcado, realiza fallback transparente al maestro `dev/brandbook.json`.
4. **Invariante Headless CrewAI**:
   - `CREWAI_TELEMETRY_OPT_OUT="true"` y `OTEL_SDK_DISABLED="true"` para eliminar el prompt interactivo de 20s en runtimes desatendidos.
