---
name: knowledge-engine
description: "Trigger: knowledge-engine, upstream knowledge, notebooklm, nlm, knowledge-hub, qdrant, playbooks, bancos tacticos, destilar playbooks, compendios, nlm-tutor. Master Upstream Knowledge Engine & Baiosfera Knowledge Hub Orchestrator in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.0"
---

# Master Upstream Knowledge Engine & Knowledge Hub (v3.0)

High-density upstream knowledge orchestrator connecting raw educational repositories in Google Drive (`baiosfera:CURSOS`, `PLATZI`, `DIGITALMARKETER`), `$0` audio transcription (`mega-downloader` -> Speech `.m4a` -> NotebookLM `nlm source content`), `$0` FreeLLMAPI distillation, and the live **Baiosfera Knowledge Hub** (`http://knowledge:8000`, MCP `/mcp`, Qdrant `baiosfera_knowledge`). Guarantees zero generic marketing slop by enforcing mathematical, systemic extraction into canonical TYM playbooks (`03_PLAYBOOKS_MAESTROS/`) and tactical banks (`04_BANCOS_TACTICOS/`).

## Operational Contracts (Positive Guidance)

1. **Pure Upstream Grounding**: Compile distilled universal playbooks into `/var/www/localstorage/knowledge_hub/03_PLAYBOOKS_MAESTROS/` (`00`..`19`) and tactical banks into `04_BANCOS_TACTICOS/` without embedding client brands, commercial academies, or static author identities.
2. **$0 Quota-Safe Transcription**: Convert non-`.m4a` media to lightweight `24k` mono `.m4a` Speech on NVMe with `mega-downloader` / `ffmpeg` BEFORE uploading to NotebookLM buffer notebooks; extract transcriptions strictly with `nlm source content --json` (`0%` chat quota) and delete buffer sources immediately.
3. **Resumable Zero-Downtime Indexing**: Re-index `/var/www/localstorage/knowledge_hub` into Qdrant (`baiosfera_knowledge`) via `scripts/index_drive.py` with checkpointed staging (`POST /v1/stage` -> `/v1/index/documents` -> `/v1/alias/swap`) and export portable `.snapshot` files via `scripts/export_snapshot.py`.
4. **Decoupled Downstream Handoff**: Delegate all brand token hydration, copy transmutations, and UI component generation to [`brand-play`](file:///var/www/zerops-astro-skills/brand-play/SKILL.md).
5. **Physical AST Validation**: Certify skills and parity via `skills-suite-validate` and `ssot-parity-check`.

## Deep Reference Architecture (Dual-RAG)

- **Thematic Catalog & Cluster Mapping**: Consult [`catalog.md`](file:///var/www/zerops-astro-skills/knowledge-engine/references/catalog.md) for the 20 Master Playbooks, 3 Tactical Banks, Crown clusters, and Knowledge Hub paths.
- **System Prompts & Extraction Blueprints**: Consult [`system_prompts.md`](file:///var/www/zerops-astro-skills/knowledge-engine/references/system_prompts.md) for specialized 10,000-character extraction blueprints.
- **Decoupled Anti-Slop Fusion Protocol**: Consult [`anti_slop_fusion.md`](file:///var/www/zerops-astro-skills/knowledge-engine/references/anti_slop_fusion.md) for separating upstream skeletons from downstream `brandbook.json` tokens.

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Knowledge Catalog | 20 Playbooks + 3 Banks + Qdrant endpoints | [`references/catalog.md`](file:///var/www/zerops-astro-skills/knowledge-engine/references/catalog.md) |
| Systemic Prompts | 18 system prompts (10k chars) | [`references/system_prompts.md`](file:///var/www/zerops-astro-skills/knowledge-engine/references/system_prompts.md) |
| Brand Transmutation | Downstream token hydration & conversion | [`brand-play`](file:///var/www/zerops-astro-skills/brand-play/SKILL.md) |
| Physical Certification | Suite validation & SSoT parity gate | `skills-suite-validate` · `ssot-parity-check` |
