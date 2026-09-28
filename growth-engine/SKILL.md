---
name: growth-engine
description: "Trigger: growth-engine, copywriting-vanguard, neurocopywriting, abandoned cart recovery, hormozi offer, storybrand, bifrost llm copy, anti spam email, brandbook voice. Sovereign E-Commerce Growth, Neurocopywriting & Abandoned Cart Recovery Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `growth-engine` — Sovereign Growth, Neurocopywriting & Cart Recovery (v1.0)

## Activation Contract
Activate when structuring, drafting, or optimizing commercial copy, crafting high-converting offers (**Hormozi $100M Offers**), narrative positioning (**StoryBrand 2.0**, **PASTOR**), orchestrating abandoned cart recovery pipelines in Valkey, inverting SPAM risks with the **2026 Anti-SPAM Linter**, or injecting **Brand SSoT** identity from `/brand/` via the **Bifrost LLM Gateway** in Zerops.

## Hard Rules & Positive Guidance
- **Brand SSoT Ingestion**: All commercial copy, PDP descriptions, and recovery messages MUST ingest voice, tone, and archetype directly from the local single-tenant path `/brand/fase0_system_prompt.md` and `/brand/brandbook.json`.
- **Bifrost LLM Gateway Integration**: Outbound sales copy and recovery variations MUST route through the local gateway `http://bifrost:8000/v1/chat/completions`.
- **Valkey Abandoned Cart Staging**: Capture pre-checkout contact info on input blur, store in Valkey (`cart:abandoned:${id}`) with 24-hour TTL, and schedule a 15-minute delayed recovery sequence via BullMQ.
- **2026 Anti-SPAM Linter Invariant**:
  - Subject lines strictly between **30 and 50 characters** (4 to 7 words).
  - ZERO all-caps words (`COMPRA YA`), zero exclamation clusters (`!!!`).
  - Maximum **1 contextual emoji** per subject line.
- **Hormozi Value Equation**: Maximize Dream Outcome and Perceived Likelihood of Achievement while minimizing Time Delay and Effort/Sacrifice.
- **Fractal CoHaLo Execution**: Enforce strict hygiene (`timeout 10s`), wait limits (`WaitMsBeforeAsync: 10000`), zero orphan tasks, and sensor verification.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Brand Ingestion & Voice | Local `/brand/` system prompt extraction and archetype matching | [`references/usage.md#1-brand-ssot-ingestion--voice-calibration`](file:///var/www/.agents/skills/growth-engine/references/usage.md) |
| Bifrost Copy Pipeline | Universal OpenAI-compatible gateway prompt formatting | [`references/usage.md#2-bifrost-llm-gateway-pipeline`](file:///var/www/.agents/skills/growth-engine/references/usage.md) |
| Cart Recovery Sequence | Astro blur capture, Valkey staging, and 15-min delayed worker | [`references/usage.md#3-abandoned-cart-recovery-pipeline`](file:///var/www/.agents/skills/growth-engine/references/usage.md) |
| Anti-SPAM Linter Standards | Email deliverability rules, subject character limits, and emojis | [`references/usage.md#4-2026-anti-spam-email-standards`](file:///var/www/.agents/skills/growth-engine/references/usage.md) |
| Environment & Paths | Gateway URLs, Valkey connection strings, and local brand mounts | [`references/infra.md`](file:///var/www/.agents/skills/growth-engine/references/infra.md) |
| Copywriting Deep References | Lossless comprehensive neurocopywriting and StoryBrand guide | [`references/copywriting_usage.md`](file:///var/www/.agents/skills/growth-engine/references/copywriting_usage.md) |
| Production Recipes JSON | Prompt injection recipes, blur capture, and SPAM linter rules | [`assets/growth_engine_recipes.json`](file:///var/www/.agents/skills/growth-engine/assets/growth_engine_recipes.json) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/growth-engine-validate.sh`](file:///var/www/.agents/skills/growth-engine/scripts/growth-engine-validate.sh) |

## Execution Steps
1. Ingest brand voice and archetype from `/brand/fase0_system_prompt.md`.
2. Configure Astro Action beacon for blurred checkout input capture.
3. Schedule delayed BullMQ worker checking payment settlement in Valkey.
4. Synthesize recovery message via Bifrost and publish to NATS.
5. Run physical sensor check (`scripts/growth-engine-validate.sh`).

## Output Contract
- High-converting, brand-authentic copy and automated abandoned cart recovery.
- Zero-SPAM email deliverability and passing physical sensor checks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/growth-engine/references/usage.md) — Brand voice calibration, Bifrost pipelines, and cart recovery workflows.
- [`references/infra.md`](file:///var/www/.agents/skills/growth-engine/references/infra.md) — Environment variables, Valkey staging, and local brand mounts.
- [`references/copywriting_usage.md`](file:///var/www/.agents/skills/growth-engine/references/copywriting_usage.md) — Comprehensive neurocopywriting templates and Hormozi frameworks.
- [`assets/growth_engine_recipes.json`](file:///var/www/.agents/skills/growth-engine/assets/growth_engine_recipes.json) — Production prompt templates and linter definitions.
- [`scripts/growth-engine-validate.sh`](file:///var/www/.agents/skills/growth-engine/scripts/growth-engine-validate.sh) — Deterministic quality & token validation sensor.
