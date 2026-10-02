---
name: sales-enablement
description: "Trigger: sales-enablement, ai sdr, ai closer, bant qualification, champ framework, meddpicc, lead scoring pgvector, sales battlecards, crm handover, bifrost sales gateway. Architect, deploy, and operate autonomous AI SDRs, AI Closers, BANT/CHAMP/MEDDPICC qualification state machines, pgvector HNSW hybrid lead scoring (0-100), real-time battlecards via Bifrost Gateway, and pluggable CRM handover SPI in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `sales-enablement` — AI SDR, Closer & Commercial Mesh (v2.0)

## Activation Contract
Activate when designing, implementing, or operating automated sales pipelines, AI SDR or AI Closer conversational workflows, qualification engines (**BANT**, **CHAMP**, **MEDDPICC**), hybrid lead scoring with `pgvector` HNSW on PostgreSQL 18, dynamic battlecards via **Bifrost AI Gateway** (`http://bifrost:8080/v1`), or pluggable CRM handover integrations.

## Hard Rules & Technical Invariants
- **Deterministic Qualification State Machines**: Conversational qualification MUST NOT rely on unstructured prose. Every stage (BANT, CHAMP, MEDDPICC) MUST map to closed Zod schemas executed via tool calls.
- **Sub-1.5s Battlecard Synthesis**: Real-time objection handling prompts MUST route through the local Bifrost AI Gateway (`http://bifrost:8080/v1`) to leverage semantic caching (<15ms repeat hits) and automatic multi-provider fallback.
- **Hybrid Semantic Lead Scoring (0–100)**: Calculate lead grade combining explicit attributes (35%), implicit behavior (25%), and normalized semantic cosine similarity (40%) using Reciprocal Rank Fusion ($k=60$) on PostgreSQL 18 `pgvector`.
- **Agnostic CRM Decoupling**: NEVER tightly couple sales logic to a single proprietary CRM. Handover and deal synchronization MUST use the pluggable `ICrmAdapter` interface supporting Directus, PostgreSQL, or Webhooks.
- **Seamless Human Handover**: When a prospect reaches grade `A_HOT` ($\ge 75$) or signals complex enterprise requirements, serialize context via `HandoverBriefingSchema` and emit an event to NATS JetStream or CRM webhook without dropping state.

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Qualification Schemas | BANT, CHAMP, MEDDPICC Zod contracts | [`assets/sales_zod_schemas.ts`](file:///var/www/.agents/skills/sales-enablement/assets/sales_zod_schemas.ts) |
| Hybrid Lead Scoring | Cosine distance + RRF ranking engine | [`assets/lead_scoring_engine.ts`](file:///var/www/.agents/skills/sales-enablement/assets/lead_scoring_engine.ts) |
| Pluggable CRM SPI | Directus, Postgres & Webhook adapters | [`assets/crm_adapter.ts`](file:///var/www/.agents/skills/sales-enablement/assets/crm_adapter.ts) |
| Human Agent Handover | Context briefing & event dispatch | [`assets/handover_pack.ts`](file:///var/www/.agents/skills/sales-enablement/assets/handover_pack.ts) |
| Dynamic Battlecards | Universal objection dataset & scripts | [`assets/battlecards_dataset.json`](file:///var/www/.agents/skills/sales-enablement/assets/battlecards_dataset.json) |
| Implementation Guide | SOTA qualification & RRF query recipes | [`references/usage.md`](file:///var/www/.agents/skills/sales-enablement/references/usage.md) |
| Topology & Infra | PostgreSQL pgvector DDL & Bifrost ports | [`references/infra.md`](file:///var/www/.agents/skills/sales-enablement/references/infra.md) |
| Physical Validation | Deterministic integrity sensor | [`scripts/sales-enablement-validate.sh`](file:///var/www/.agents/skills/sales-enablement/scripts/sales-enablement-validate.sh) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/sales-enablement/references/usage.md) — Qualification state machines, hybrid scoring math, and battlecard synthesis.
- [`references/infra.md`](file:///var/www/.agents/skills/sales-enablement/references/infra.md) — PostgreSQL 18 pgvector HNSW DDL, Bifrost gateway setup, and NATS topics.
- [`assets/sales_zod_schemas.ts`](file:///var/www/.agents/skills/sales-enablement/assets/sales_zod_schemas.ts) — Universal Zod qualification and deal contracts.
- [`assets/lead_scoring_engine.ts`](file:///var/www/.agents/skills/sales-enablement/assets/lead_scoring_engine.ts) — Deterministic scoring and RRF fusion calculator.
- [`assets/crm_adapter.ts`](file:///var/www/.agents/skills/sales-enablement/assets/crm_adapter.ts) — Decoupled CRM adapter implementation.
- [`assets/handover_pack.ts`](file:///var/www/.agents/skills/sales-enablement/assets/handover_pack.ts) — Contextual human agent handover pack.
- [`assets/battlecards_dataset.json`](file:///var/www/.agents/skills/sales-enablement/assets/battlecards_dataset.json) — Universal objection dataset.
- [`scripts/sales-enablement-validate.sh`](file:///var/www/.agents/skills/sales-enablement/scripts/sales-enablement-validate.sh) — Deterministic physical validator.
