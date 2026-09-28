---
name: sales-enablement
description: "Trigger: sales-enablement, ai sdr, ai closer, bant qualification, champ framework, lead scoring pgvector, sales battlecards, crm handover directus, sales objections latam. Architect, deploy, and operate autonomous AI SDRs, AI Closers, BANT/CHAMP qualification engines, pgvector HNSW hybrid lead scoring (0-100), real-time LatAm battlecards, and seamless human handover protocols on Directus 11+ and PostgreSQL 18."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# Sales Enablement — AI SDR, Closer & Lead Scoring Engine (v1.1.0)

## Activation Contract
Activate whenever designing, implementing, or optimizing automated sales qualification pipelines, AI SDR / AI Closer conversational agents, **BANT** (Budget, Authority, Need, Timing) and **CHAMP** frameworks, hybrid lead scoring (0-100) with pgvector, real-time objection battlecards, or human agent CRM handover protocols on Directus 11+.

---

## Hard Rules & Technical Invariants

1. **Deterministic BANT/CHAMP Scoring (0-100):**
   - Lead qualification scores MUST be computed deterministically combining explicit criteria (Budget: 30pts, Authority: 25pts, Need: 25pts, Timing: 20pts) with semantic similarity vector search.
2. **Seamless Human Agent Handover Invariant:**
   - Whenever an AI agent detects complex negotiation, customer frustration, or a high-ticket score (>80), it MUST lock the conversational state in Directus and dispatch an alert to human closers without dropping context.
3. **Objection Battlecard Grounding:**
   - AI Closers MUST ground responses strictly in validated objection battlecards stored in PostgreSQL/pgvector to avoid hallucinated pricing or unapproved discounts.

---

## References & SSoT Documents

- [`references/usage.md`](file:///var/www/.agents/skills/sales-enablement/references/usage.md) — Lead scoring algorithm, BANT prompts, objection handling logic, and Directus CRM triggers.
- [`references/infra.md`](file:///var/www/.agents/skills/sales-enablement/references/infra.md) — Database schema (`leads`, `lead_events`, `battlecards`), pgvector indexes, and webhook flow setup.
- [`assets/lead_scoring_engine.ts`](file:///var/www/.agents/skills/sales-enablement/assets/lead_scoring_engine.ts) — TypeScript calculation engine for BANT lead scoring.
- [`assets/battlecards_latam.json`](file:///var/www/.agents/skills/sales-enablement/assets/battlecards_latam.json) — Structured objection-handling dataset for Colombia and Latin America.
