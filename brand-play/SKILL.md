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
Activate when ingesting universal TYM (Type-YAML-Markdown) playbooks from `/var/www/baiosfera/PLAYBOOKS/`, resolving algebraic semantic slots (`{{SLOT}}`) using W3C DTCG tokens from `/var/www/localstorage/${PROJECT_NAME}/dev/brandbook.json`, transmuting structural playbooks into high-converting copy (`growth-engine`), Astro 5 SSR components (`astro-web`), conversational WhatsApp qualification flows (`whatsapp-engine`), or deliverability-certified transactional emails (`email-marketing`).

## Hard Rules & Positive Guidance
- **Decoupled Downstream Boundary**: Consume solely universal, zero-slop TYM playbooks from `/var/www/baiosfera/PLAYBOOKS/`. Never embed author names, commercial academies, or static vendor identities into output artifacts.
- **Deterministic Token Ingestion**: Read W3C DTCG tokens strictly from active local storage (`/var/www/localstorage/${PROJECT_NAME}/dev/brandbook.json`). Map DTCG nodes (`$value`, `$type`) to algebraic slots via compile-time validated RFC 6901 JSON pointers.
- **Atomic Slot Hydration**: Execute AST-first replacement of all declared `{{SLOT}}` tags. Apply strict coalescing fallbacks for undefined non-required slots. Trigger validation halt when required slots fail resolution.
- **Bifrost Production Gateway**: Route all downstream AI synthesis through `http://bifrost:8080/v1/chat/completions` sending `x-tier: production` and structured JSON/TYM schemas to prevent 429 timeouts and model degradation.
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
brand-play transmute --playbook offers_pricing --brand elplacerdc --target all
skills-suite-validate && ssot-parity-check
```
