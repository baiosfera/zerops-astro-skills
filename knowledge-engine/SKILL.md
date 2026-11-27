---
name: knowledge-engine
description: "Trigger: knowledge-engine, upstream knowledge, notebooklm, nlm, knowledge-hub, playbooks, bancos tacticos, destilar playbooks, compendios, nlm-tutor. Master Upstream Knowledge Engine & Drive-First Playbook Compiler in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "4.1"
---

# Master Upstream Knowledge Engine & Drive-First Playbooks (v4.1)

High-density upstream knowledge compiler transforming clean educational transcripts in `/mnt/localstorage/knowledge_hub/01_TRANSCRIPCIONES_LIMPIAS/` and `/var/www/baiosfera/PLATZI/12 DEV WEB/` (curated from `/CURSOS`, `/DIGITALMARKETER`, and `/PLATZI` minus `Z_NON-MKTNG`) into granular, `Zerops-First`, Apotelos-aligned Master Playbooks (`00..19` + `INDEX.json`) in `02_PLAYBOOKS_MAESTROS/` (aliased at `/mnt/localstorage/playbooks/`), consumable across any Zerops project via `iniciar.sh` and `zcp-sync`.

## Operational Contracts (Positive Guidance)

1. **Drive-First Sequential SSoT (`01 -> 02`)**: Compile and mirror all Master Playbooks (`00..19` + `INDEX.json`) in `/var/www/baiosfera/KNOWLEDGE_HUB/02_PLAYBOOKS_MAESTROS/` and `/mnt/localstorage/knowledge_hub/02_PLAYBOOKS_MAESTROS/` (aliased at `/mnt/localstorage/playbooks/`).
2. **Clean Markdown Distillation (`$0`)**: Distill verified course transcripts (`<= 4,500` tokens/call, bilingual `EN -> ES` neutral Spanish) into dense section-delimited (`## `) Markdown playbooks with zero invented boilerplate.
3. **Full Conversion & Web Craft Scope (`Zerops-First`)**: Cover positioning (`00`), sales/copy/funnels/CRO (`01..05`), SEO/AEO/GEO (`06`), telemetry (`07`), acquisition channels (`08..15`), branding/AI/affiliates (`16..18`), and Web Design Systems, Vibecoding Craft, Typography, Composition, Performance & Motion (`19`) grounded in Astro 5 SSR + Bun, Tailwind v4, `@fontsource-variable/*`, `impeccable`, GSAP/Lenis, PostgreSQL 18, Valkey 7.2, and NATS.
4. **Audio-First `$0` Transcription**: Convert incoming media to `24k` mono `.m4a` on NVMe prior to NotebookLM extraction (`nlm source content --json`), clearing buffer sources immediately after saving clean `.md`.
5. **Decoupled Downstream Handoff**: Delegate brand token hydration, Apotelos Blackboard alignment, and multi-surface transmutation to [`brand-play`](file:///var/www/zerops-astro-skills/brand-play/SKILL.md) and [`apotelos`](file:///var/www/zerops-astro-skills/apotelos/SKILL.md).
6. **Physical AST Certification**: Validate skills and parity via `skills-suite-validate` and `ssot-parity-check`.

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Knowledge Catalog & Routes | Emergent Playbooks (`00..19`) + `INDEX.json` | [`references/catalog.md`](file:///var/www/zerops-astro-skills/knowledge-engine/references/catalog.md) |
| Systemic Prompts | Extraction & Map-Reduce blueprints | [`references/system_prompts.md`](file:///var/www/zerops-astro-skills/knowledge-engine/references/system_prompts.md) |
| Anti-Slop Fusion | Separating skeletons from `brandbook.json` | [`references/anti_slop_fusion.md`](file:///var/www/zerops-astro-skills/knowledge-engine/references/anti_slop_fusion.md) |
| Brand Transmutation | Downstream slot hydration & CrewAI routing | [`brand-play`](file:///var/www/zerops-astro-skills/brand-play/SKILL.md) |
| Physical Certification | Suite validation & SSoT parity gate | `skills-suite-validate` · `ssot-parity-check` |
