---
name: brand-play
description: "Trigger: brand-play, transmutar playbook, hidratar slots, playbook tym, playbook universal, convertir playbook, brand playbook, tym downstream. Sovereign Downstream Playbook Transmutation & Slot Hydration Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# `brand-play` — Sovereign Downstream Playbook Transmutator (v2.1)

## Activation Contract
Activate when ingesting all 18 universal playbooks (`00..17`) and `INDEX.json` task routes from `/mnt/localstorage/knowledge_hub/02_PLAYBOOKS_MAESTROS/`, resolving semantic slots from workspace `brandbook.json` + `dev/verticals/<vertical>.json`, and synthesizing client-ready copy, WhatsApp/Email lifecycle sequences, ads specs, and Astro 5 tokens.

## Hard Rules & Positive Guidance
- **Dual-Upstream 18-Playbook Coverage (`00..17` via `INDEX.json`)**:
  - Anchor thesis in Crown Playbooks `00_category_of_one.md` and `01_sales_and_conversion_doctrine.md`, and distill full multi-touch tactical depth from `02..17` (Copy, Offers, Funnels/VSL, CRO, SEO/AEO/GEO, Telemetry, Instagram, WhatsApp, TikTok, LinkedIn, Email, Meta Ads, Google Ads, Consultative Closing, Personal Branding, Applied AI). Never reduce multi-touch sequences to generic 1-email stubs.
- **Two-Layer Workspace & Vertical Resolution**: Discover `<ROOT>/<PROJECT>/dev/workspaces/<vertical>/[brand, strategy, copy, web]` and `dev/verticals/<vertical>.json` case-insensitively before fallback paths.
- **Client-Facing Zero-Jargon & Spanish Orthography Gate**: All customer-facing copy, UI, emails, and WhatsApp flows MUST use natural local Spanish (`tú` for Colombia/LatAm unless brand specifies otherwise), complete accents (`á, é, í, ó, ú, ñ, ¿, ¡`), ZERO internal acronyms (`OPB`, `CO1`, `BANT`, `AEO`, `GEO`, `PWYW`, `Order Bump`, `Context Vault`, `Break-Even CPA`), ZERO `UPPER_SNAKE_CASE` enums, and ZERO regional voseo leakage. Validate every file with `anti-slop-linter --brand <brand>`.
- **Bifrost Gateway Routing**: Route synthesis via `http://bifrost:8080/v1/chat/completions` (`model: "auto"` first, deterministic non-voseo/non-hardcoded-price fallback offline).
- **Target Invariants**: Enforce Astro 5 `@theme` tokens, Schema.org JSON-LD, `llms.txt`, `ad-telemetry`, HTML `< 85 KB`, RFC 8058 One-Click headers, and transactional `isTransactional: true` T+0 WhatsApp/Email delivery.
- **Physical Certification**: Verify via `brand-play test`, `anti-slop-linter --test`, `skills-suite-validate`, and `ssot-parity-check`.

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Complete Usage Guide | Slot hydration algorithm, CLI commands & recipes | [`references/usage.md`](file:///var/www/zerops-astro-skills/brand-play/references/usage.md) |
| Zerops & SSoT Topology | Local Storage, Drive paths & Valkey cache | [`references/infra.md`](file:///var/www/zerops-astro-skills/brand-play/references/infra.md) |
| TYM Static Contracts | Formal Zod schemas & interfaces | [`assets/playbook_tym_contracts.ts`](file:///var/www/zerops-astro-skills/brand-play/assets/playbook_tym_contracts.ts) |
| Deterministic Hydrator | AST slot replacement engine | [`assets/slot_hydrator.ts`](file:///var/www/zerops-astro-skills/brand-play/assets/slot_hydrator.ts) |

## Commands
```bash
brand-play transmute --playbook 03_irresistible_offers_and_pricing --brand "<vertical>" --target all
anti-slop-linter --brand "<BRAND>" --file <copy_file>
```
