---
name: brand-play
description: "Trigger: brand-play, transmutar playbook, hidratar slots, playbook tym, playbook universal, convertir playbook, brand playbook, tym downstream. Sovereign Downstream Playbook Transmutation & Slot Hydration Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `brand-play` — Sovereign Downstream Playbook Transmutator (v1.0)

## Activation Contract
Activate when ingesting universal TYM playbooks and Tactical Banks from **Baiosfera Knowledge Hub** (`/var/www/localstorage/knowledge_hub/03_PLAYBOOKS_MAESTROS/` and `04_BANCOS_TACTICOS/`, or `/mnt/localstorage/knowledge_hub/`), resolving algebraic semantic slots (`{{SLOT_*}}`) using W3C DTCG tokens from brand workspaces and `brandbook.json`, and transmuting structural playbooks into high-converting copy (`growth-engine`), Astro 5 SSR components (`astro-web`), conversational WhatsApp qualification flows (`whatsapp-engine`), or deliverability-certified transactional emails (`email-marketing`).

## Hard Rules & Positive Guidance
- **Dual-Upstream Doctrine Hierarchy (Layer 1 Invariant)**:
  - *Layer 1A (Authority & Category)*: Consume Crown Playbook `00_category_of_one.md` + `00_category_of_one_swipes_y_guiones.md` for ontological positioning, personal monopoly, and value pricing.
  - *Layer 1B (Conversion & Sales)*: Consume Crown Playbook `01_velocity_sales_doctrine.md` + Specialty Playbooks (`02_avatar_research.md`..`19_product_startup.md`) + Tactical Banks (`01_biblioteca_210_prompts_maestros.md`, `02_swipes_copy_email_y_paid_ads.md`) for consultative sales scripts, direct-response copy, paid ads, and CRO funnels. Neither layer may be bypassed or subordinated.
- **Decoupled Downstream Boundary**: Consume solely universal, zero-slop TYM playbooks from `/var/www/localstorage/knowledge_hub/` (or Qdrant `baiosfera_knowledge` via `http://knowledge:8000/mcp`). Never embed author names, commercial academies, or static vendor identities into output artifacts.
- **Deterministic Token Ingestion**: Read W3C DTCG tokens from the active client workspace (`/var/www/localstorage/workspaces/${PROJECT_NAME}/`, `/var/www/localstorage/${PROJECT_NAME}/`, or `/var/www/baiosfera/PROYECTOS/${PROJECT_NAME}/dev/brandbook.json`). Map DTCG nodes (`$value`, `$type`) to algebraic slots via RFC 6901 JSON pointers.
- **Atomic Slot Hydration**: Execute AST-first replacement of all declared `{{SLOT_*}}` tags with coalescing fallbacks for optional slots and validation gates on required slots.
- **Bifrost Production Gateway**: Route downstream AI synthesis through `http://bifrost:8080/v1/chat/completions` (`x-tier: production`) with structured JSON/TYM schemas.
- **Target Invariant Compliance**:
  - *Growth Engine*: Enforce 2026 Anti-SPAM constraints (30-50 char subject lines, spam rate <0.10%).
  - *Astro Web*: Transpile tokens to Tailwind CSS v4 `@theme` blocks; calibrate Variance, Motion, and Density dials.
  - *WhatsApp*: Ground conversational flows in real-time present (`date >= NOW()`) and operator takeover monotonicity.
  - *Email Marketing*: Enforce compiled HTML footprint strictly under 85 KB and RFC 8058 One-Click headers.
- **Physical Certification**: Attest integrity through the Universal Sensor `skills-suite-validate` and `ssot-parity-check` (Exit code 0).

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Complete Usage Guide | Slot hydration algorithm, CLI commands & recipes | [`references/usage.md`](file:///var/www/zerops-astro-skills/brand-play/references/usage.md) |
| Zerops & SSoT Topology | Local Storage, Google Drive paths & Valkey cache | [`references/infra.md`](file:///var/www/zerops-astro-skills/brand-play/references/infra.md) |
| TYM Static Contracts | Formal Zod schemas & interfaces for Playbooks | [`assets/playbook_tym_contracts.ts`](file:///var/www/zerops-astro-skills/brand-play/assets/playbook_tym_contracts.ts) |
| Deterministic Hydrator | AST slot replacement engine with fallbacks | [`assets/slot_hydrator.ts`](file:///var/www/zerops-astro-skills/brand-play/assets/slot_hydrator.ts) |
| Physical Certification | Universal suite validation and SSoT parity gate | `skills-suite-validate` · `ssot-parity-check` |

## Commands
```bash
brand-play transmute --playbook offers_pricing --brand "${PROJECT_NAME}" --target all
skills-suite-validate && ssot-parity-check
```
