---
name: knowledge-engine
description: "Trigger: knowledge-engine, marketing upstream, copywritting, copywriting, landings, funnels, ofertas, brandbook fusion, playbooks, cursos baiosfera, notebooklm sync. Master Upstream Knowledge Engine & Strategic Synthesizer linking Google NotebookLM course clusters with local brandbook tokens in Zerops."
---

# Master Upstream Knowledge Engine & Strategic Synthesizer

High-density knowledge bridge connecting Google NotebookLM course clusters with local project execution in Zerops. Guarantees zero generic marketing slop by enforcing strict 2-step decoupled synthesis: extraction of universal frameworks from course intelligence followed by lexical and aesthetic transmutation into the active brand's identity tokens.

## Operational Contracts (Positive Guidance)

1. **Upstream Grounding Over Hallucination**: Query thematic NotebookLM clusters via `nlm chat` or read distilled SSoT playbooks in `/var/www/baiosfera/PLAYBOOKS/` before writing copy, sales architectures, or funnel logic.
2. **2-Step Decoupled Transmutation**:
   - **Step 1 (Framework Extraction)**: Extract pure structural mechanics (heuristics, value equations, psychological triggers, conversion steps) without final vocabulary.
   - **Step 2 (Local Infusion)**: Map framework variables strictly into active brand tokens (`brandbook.json`, tone, prohibited words, OKLCH palette, audience pains).
3. **Living Catalog Ingestion**: Scan, deduplicate, and sync new courses incrementally using `knowledge-sync push --target-cluster <name>`.
4. **Physical Anti-Slop Gate**: Validate all generated copy and landing structures against `anti-slop-linter --brand <name>`. Reject any output containing blacklisted clichés or off-brand vocabulary.

## Deep Reference Architecture (Dual-RAG)

- **Thematic Catalog & Cluster Mapping**: Consult [`catalog.md`](file:///var/www/zerops-astro-skills/knowledge-engine/references/catalog.md) for notebook IDs, source clusters, course roots, and playbook destinations.
- **System Prompts & Extraction Blueprints**: Consult [`system_prompts.md`](file:///var/www/zerops-astro-skills/knowledge-engine/references/system_prompts.md) for specialized 10,000-character prompts tailored for NotebookLM synthesis.
- **Decoupled Anti-Slop Fusion Protocol**: Consult [`anti_slop_fusion.md`](file:///var/www/zerops-astro-skills/knowledge-engine/references/anti_slop_fusion.md) for concrete workflows combining high-density course intelligence with local brand systems.

## Workflow

1. Identify task domain (Copywriting, Offers, Funnels, WhatsApp, Email, Ads, Branding).
2. Load relevant playbook from `/var/www/baiosfera/PLAYBOOKS/<topic>_playbook.md` or execute cross-query in NotebookLM.
3. Ingest active brand tokens from `/var/www/localstorage/${PROJECT_NAME}/dev/brandbook.json` (or Google Drive SSoT).
4. Synthesize copy or architecture through the 2-step decoupled pipeline.
5. Execute `anti-slop-linter` to verify physical compliance.
