---
name: growth-engine
description: "Trigger: growth-engine, copywriting-vanguard, neurocopywriting, abandoned cart recovery, hormozi offer, storybrand, bifrost llm copy, anti spam email, brandbook voice. Sovereign E-Commerce Growth, Neurocopywriting & Abandoned Cart Recovery Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `growth-engine` — Sovereign Growth, Neurocopywriting & Cart Recovery (v2.0)

## Activation Contract
Activate when designing conversion funnels, generating high-converting sales copy (**Hormozi $100M Offers**, **StoryBrand 2.0**, **P.A.S.T.O.R.**), executing behavioral abandoned cart recovery with self-discarding fencing tokens in Valkey and BullMQ, enforcing the **2026 Anti-SPAM Deliverability Linter**, or routing structured LLM synthesis through the **Bifrost AI Gateway** (`bifrost:8080`) in Zerops.

## Hard Rules & Positive Guidance
- **Decoupled Brand SSoT Ingestion**: Ingest voice parameters dynamically from `$BRAND_SSOT_PATH`, `src/config/brand.json`, or direct runtime arguments. Extract archetypes, tone constraints, and forbidden jargon.
- **Bifrost AI Gateway Single Front Door**: Route all copy generation and recovery messages through `http://bifrost:8080/v1/chat/completions` using structured JSON output schemas.
- **Cart Fencing & Monotonic Versioning**: Capture leads on input blur via Astro Actions, staging records in Valkey (`cart:abandoned:${id}`) with 24h TTL. Schedule BullMQ delayed jobs containing `{ cartId, version }`. Workers self-discard when `job.version !== current.version` or when status is `CONVERTED`.
- **Dynamic Capped Discounting**: Enforce mathematical margin protection across all recovery offers:
  $$\text{Discount Ceil} = \min(\text{Product Margin} - 0.05, \, \text{LTV Tier Cap}, \, \text{Attempt Ceiling})$$
  Attempt 1 (15-30m): 0% discount. Attempt 2 (2-4h): 5-10% capped. Attempt 3 (24h): single-use bounded offer.
- **2026 Anti-SPAM & Deliverability Compliance**: Enforce RFC 8058 One-Click List-Unsubscribe headers, DMARC/DKIM/SPF alignment, 30-50 character subject lines (4-7 words), zero all-caps, zero multiple exclamation points, and max 1 emoji. Maintain spam complaint rate under 0.1%.
- **Agnostic Multi-Touch Attribution**: Decouple attribution models (First-Touch, Last-Touch, Linear, Time-Decay, U-Shaped) via server-side session tracking and NATS JetStream event dispatch.

## Decision Gates

| Objective | Action | Reference / Asset |
|---|---|---|
| Complete Usage Guide | Cart fencing, copy formulas & linter | [`references/usage.md`](file:///var/www/.agents/skills/growth-engine/references/usage.md) |
| Copywriting Formulas | Neurocopywriting, Hormozi offer & StoryBrand | [`references/copywriting_usage.md`](file:///var/www/.agents/skills/growth-engine/references/copywriting_usage.md) |
| Zerops & Bun Infra | Private DNS, ports & deployment | [`references/infra.md`](file:///var/www/.agents/skills/growth-engine/references/infra.md) |
| Zod Schemas | Multi-locale, typed copy contracts | [`assets/copywriting_zod_schemas.ts`](file:///var/www/.agents/skills/growth-engine/assets/copywriting_zod_schemas.ts) |
| AI Atomizer Engine | Structured inference via Bifrost | [`assets/copy_atomizer_engine.ts`](file:///var/www/.agents/skills/growth-engine/assets/copy_atomizer_engine.ts) |
| Omnichannel Templates | Universal Hook-Story-Offer & SB7 | [`assets/omnichannel_copy_templates.md`](file:///var/www/.agents/skills/growth-engine/assets/omnichannel_copy_templates.md) |
| Production Recipes | Gateway, staging & linter configuration | [`assets/growth_engine_recipes.json`](file:///var/www/.agents/skills/growth-engine/assets/growth_engine_recipes.json) |
| Physical Sensor | Attest integrity, AST & algorithms | [`scripts/growth-engine-validate.sh`](file:///var/www/.agents/skills/growth-engine/scripts/growth-engine-validate.sh) |

## Output Contract
- High-converting, brand-aligned omnichannel copy and mathematically bounded cart recovery.
- Full 2026 Anti-SPAM deliverability compliance and passing physical validation tests (Exit 0).
