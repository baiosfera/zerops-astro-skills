---
name: crewai-engine
description: "Trigger: crewai-engine, crewai, swarm compiler, dynamic crews, polymorphic agents, knowledge source rag, bifrost llm proxy, crewai zero cost, crewai multiagent mesh. High-Performance Polymorphic Dynamic Swarm Compiler & Skill-Tool Bridge for CrewAI 1.15.30+ on Zerops."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# CrewAI Engine: Sovereign Polymorphic Swarm Compiler (v1.1)

Compiles dynamic, zero-cost AI swarms from declarative specs, hydrating agents with Dual-RAG skills, CrewAI Knowledge sources (`ONNX` local `$0` embedder), and in-memory Pydantic v2 validation.

## Sovereign Invariants

1. **Pure Programmatic Swarm Compilation**: Instantiate agents, tasks, and crews strictly from Pydantic v2 models (`DynamicSwarmSpec`) or YAML specs. Abolish static `@CrewBase` classes and hardcoded squads.
2. **Zero-Cost Local Knowledge & Path Invariant**: Ingest playbooks and brand dossiers via `TextFileKnowledgeSource` (`chunk_size=2000`, `chunk_overlap=200`) with explicit `pathlib.Path` objects (bypassing the `knowledge/` prefix bug) and CrewAI's built-in `{"provider": "onnx"}` embedder persisted under `CREWAI_STORAGE_DIR` (never hit non-existent OpenAI embedding models on Bifrost).
3. **In-Memory Pydantic v2 Validation**: Enforce schema constraints via prompt-injected JSON schema (`InMemoryPydanticParser`) and validate outputs in memory. Avoid `output_pydantic` with `InternalInstructor` on free tiers to eliminate 2x HTTP call overhead.
4. **Strict `$0` Inference via Bifrost Gateway**: Route agent reasoning through Bifrost (`http://bifrost:8080/v1`) using env-backed `BIFROST_MASTER_VK` (`openai/auto` with `x-routing-tier: free`), never hardcoded `vk-crewai` and never auto-draining paid Pro tiers without explicit opt-in (`x-force-deepseek: true`).
5. **Polymorphic Skill-Tool Bridge**: Expose scripts and Dual-RAG references (`references/usage.md`, `references/infra.md`) from installed skills via `SkillToolBridge` using progressive disclosure (`SKILL.md <= 480` words).

## Activation Contract

1. Load `DynamicSwarmSpec` defining mission goal, agents, tasks, required skills, and `Path` playbooks.
2. Resolve required skills via `SkillToolBridge` and `references/`.
3. Configure `crewai.LLM` with Bifrost endpoint, `BIFROST_MASTER_VK`, and explicit routing tier (`free` or `pro`).
4. Assemble sequential or hierarchical `Crew` with ONNX-embedded knowledge sources.
5. Execute `crew.kickoff()` and validate structured deliverables via `InMemoryPydanticParser`.

## Output Contract

- Validated structured deliverable conforming to the mission's Pydantic v2 schema.
- Zero automatic escalation to paid commercial models on free-tier `429`/timeout.

## Dual-RAG Progressive Disclosure

- Spec & Assembly API: [references/usage.md](file:///var/www/zerops-astro-skills/crewai-engine/references/usage.md)
- Runtime Infra & Bifrost Mesh: [references/infra.md](file:///var/www/zerops-astro-skills/crewai-engine/references/infra.md)
- Domain Schemas & Contracts: [references/contracts.md](file:///var/www/zerops-astro-skills/crewai-engine/references/contracts.md)
