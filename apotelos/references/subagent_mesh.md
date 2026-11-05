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

## 3. Physical Zerops Container Boundaries

- **`zcp` Container (Control Plane)**:
  Runs `/usr/local/bin/apotelos` for discovery, static validation, and Linear coordination. Does not host heavy CrewAI swarms.
- **`hermes` Container (Ubuntu Python 3.12 Runtime)**:
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
