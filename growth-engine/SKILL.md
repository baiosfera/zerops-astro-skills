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
Activate when drafting or optimizing commercial copy, crafting high-converting offers (**Hormozi $100M Offers**), narrative positioning (**StoryBrand 2.0**, **PASTOR**), orchestrating cart recovery pipelines in Valkey, enforcing the **2026 Anti-SPAM Linter**, or injecting **Brand SSoT** identity via the **Bifrost LLM Gateway** in Zerops.

## Hard Rules & Positive Guidance
- **Brand SSoT Ingestion**: Ingest directly from `astrobranding_[MARCA].md` (compiled by Oráculo in Fase 0) to extract:
  - Archetypal psychology for neurocopywriting tone calibration (Greene, Arroyo, Fagan).
  - Wealth houses (2, 6, 10) & Shadbala for Hormozi Value Equation framing ($100M Offers).
  - ACG lines & power cities for Meta CAPI geographic segmentation.
  - Fallback to `brandbook.json` if present.
- **Bifrost LLM Gateway**: Sales copy and recovery route through `http://bifrost:8000/v1/chat/completions`.
- **Valkey Staging & Recovery**: Capture contact on input blur, store in Valkey (`cart:abandoned:${id}`, 24h TTL), schedule 15-minute BullMQ recovery worker.
- **2026 Anti-SPAM Invariant**: Subject lines 30-50 characters (4-7 words), zero all-caps, zero multiple exclamation points, max 1 emoji.
- **Fractal CoHaLo**: Strict timeouts (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphan tasks, sensor checks.

## Decision Gates

| Objective | Action | Reference / Asset |
|---|---|---|
| Brand Ingestion & Voice | SSoT extraction from astrobranding | [`references/usage.md`](file:///var/www/.agents/skills/growth-engine/references/usage.md) |
| Bifrost Copy Pipeline | Universal OpenAI gateway prompts | [`references/usage.md`](file:///var/www/.agents/skills/growth-engine/references/usage.md) |
| Cart Recovery Sequence | Blur capture, Valkey staging & BullMQ | [`references/usage.md`](file:///var/www/.agents/skills/growth-engine/references/usage.md) |
| Anti-SPAM Standards | Email deliverability & character limits | [`references/usage.md`](file:///var/www/.agents/skills/growth-engine/references/usage.md) |
| Environment & Paths | Gateway URLs, Valkey strings & mounts | [`references/infra.md`](file:///var/www/.agents/skills/growth-engine/references/infra.md) |
| Copywriting Deep Guide | Neurocopywriting & Hormozi formulas | [`references/copywriting_usage.md`](file:///var/www/.agents/skills/growth-engine/references/copywriting_usage.md) |
| Production Recipes JSON | Prompts, blur capture & linter recipes | [`assets/growth_engine_recipes.json`](file:///var/www/.agents/skills/growth-engine/assets/growth_engine_recipes.json) |
| Validation Sensor | Attest skill integrity & token budget | [`scripts/growth-engine-validate.sh`](file:///var/www/.agents/skills/growth-engine/scripts/growth-engine-validate.sh) |

## Execution Steps
1. Ingest brand voice and archetype from `astrobranding_[MARCA].md`.
2. Configure Astro Action beacon for blurred checkout input capture.
3. Schedule delayed BullMQ worker checking payment settlement in Valkey.
4. Synthesize recovery message via Bifrost and publish to NATS.
5. Run physical sensor check (`scripts/growth-engine-validate.sh`).

## Output Contract
- High-converting, brand-authentic copy and automated abandoned cart recovery.
- Zero-SPAM email deliverability and passing physical sensor checks.
