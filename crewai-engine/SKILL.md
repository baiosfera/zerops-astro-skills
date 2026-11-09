---
name: crewai-engine
description: "Trigger: crewai-engine, crewai, swarm compiler, dynamic crews, polymorphic agents, knowledge source rag, bifrost llm proxy, crewai zero cost, crewai multiagent mesh. High-Performance Polymorphic Dynamic Swarm Compiler & Skill-Tool Bridge for CrewAI 1.15.30+ on Zerops."
---

# CrewAI Engine: Sovereign Polymorphic Swarm Compiler (v1.0 SOTA)

Compiles dynamic, zero-cost AI swarms from declarative specs, hydrating agents with any of the 166 sovereign skills, RAG knowledge sources from playbooks, and in-memory Pydantic v2 validation.

## Sovereign Invariants

1. **Pure Programmatic Swarm Compilation**: Instantiate agents, tasks, and crews strictly from Pydantic v2 models (`DynamicSwarmSpec`) or YAML specs. Abolish static `@CrewBase` classes and hardcoded squads.
2. **Zero-Token-Waste Knowledge Ingestion**: Ingest playbooks and brand dossiers via `TextFileKnowledgeSource` (chunk 2000, overlap 200) with explicit `pathlib.Path` objects and Bifrost embedder. Never stuff raw 20k-token playbooks into agent backstories.
3. **In-Memory Pydantic v2 Validation**: Enforce schema constraints via prompt-injected JSON schema and validate outputs in memory using `model_validate_json()`. Never use `output_pydantic` with `InternalInstructor` (eliminates 2x HTTP call overhead and 429 rate limit triggers).
4. **$0 Inference via Bifrost Gateway**: Route all agent reasoning through Maxim AI Bifrost (`http://bifrost:8080/v1`) using Virtual Key `vk-crewai` (`openai/auto` with header `x-routing-tier: free`) to FreeLLMAPI pool with automatic failover.
5. **Polymorphic Skill-Tool Bridge**: Expose scripts (`.ts` via Bun, `.py` via Python, `.sh` via Bash) and Dual-RAG references (`usage.md`, `infra.md`) from any skill in `/mnt/localstorage/skills/` as typed `BaseTool` instances.

## Activation Contract

1. Load `DynamicSwarmSpec` defining mission goal, agents, tasks, required skills, and playbooks.
2. Resolve required skills from `/mnt/localstorage/skills/` via `SkillToolBridge`.
3. Configure `crewai.LLM` with Bifrost endpoint and routing headers (`free` or `pro`).
4. Assemble sequential or hierarchical `Crew` with chunked knowledge sources.
5. Execute `crew.kickoff()` and validate structured deliverables in memory against Pydantic schema.

## Output Contract

- Validated structured deliverable conforming to the mission's Pydantic schema.
- Zero markdown noise or preambles in automated downstream pipelines.
- Execution metrics logged to Linear and PostgreSQL audit trail.

## Dual-RAG Progressive Disclosure

- Spec & Assembly API: [references/usage.md](file:///var/www/zerops-astro-skills/crewai-engine/references/usage.md)
- Runtime Infra & Bifrost Mesh: [references/infra.md](file:///var/www/zerops-astro-skills/crewai-engine/references/infra.md)
- Domain Schemas & Contracts: [references/contracts.md](file:///var/www/zerops-astro-skills/crewai-engine/references/contracts.md)
