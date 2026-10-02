# Sales Enablement & AI SDR / Closer: Usage & Development Guide (v2.0)

> **SSoT Reference Document:** `.agents/skills/sales-enablement/references/usage.md`  
> **Scope:** Agnostic commercial qualification (BANT, CHAMP, MEDDPICC), hybrid lead scoring with `pgvector` HNSW and RRF ($k=60$), dynamic battlecard synthesis via Bifrost AI Gateway (`http://bifrost:8080/v1`), and decoupled CRM handover SPI.

---

## 1. Commercial Qualification State Machines

SOTA AI SDRs avoid conversational monologues and ungrounded prose. Qualification state transitions are driven by deterministic tool calls validating against strict Zod schemas.

### A. BANT Qualification (High-Velocity / Inbound)
1. **Budget:** Quantified or elastic status. Currency stored as standard 3-letter ISO code (`USD`, `EUR`, etc.).
2. **Authority:** Role identification (`sole_decision_maker`, `economic_buyer`, `influencer`, `champion`, `gatekeeper`).
3. **Need:** Business urgency and quantified pain points (`critical_urgency`, `moderate`, `low_nice_to_have`).
4. **Timing:** Implementation horizon (`immediate`, `short_term`, `medium_term`, `long_term`).

### B. CHAMP Qualification (Mid-Market Consultative)
1. **Challenges:** Core operational bottlenecks and root pain points before discussing commercials.
2. **Authority:** Decision-making unit (DMU) and organizational buy-in process.
3. **Money:** Investment viability, anticipated ROI vs. Cost of Inaction (COI).
4. **Prioritization:** Ranking of this initiative against company top strategic priorities (`top_1`, `top_3`, `backlog`).

### C. MEDDPICC Qualification (Enterprise B2B Pipelines)
1. **Metrics:** Quantifiable economic returns required for business case approval.
2. **Economic Buyer:** Person with final discretionary budget sign-off.
3. **Decision Criteria:** Technical, operational, and commercial vendor benchmarks.
4. **Decision Process:** Formal stages from validation to procurement contract execution.
5. **Paper Process:** Legal, info-sec, and compliance review timeline.
6. **Identify Pain:** Root business consequences of status quo.
7. **Champion:** Internal stakeholder actively advocating for selection.
8. **Competition:** Incumbent or alternative vendor evaluation.

---

## 2. Hybrid Lead Scoring Engine (0–100) & RRF

Lead scoring combines explicit criteria (firmographics, role, budget), implicit signals (conversational velocity, high-intent queries), and semantic cosine similarity from embeddings:

$$\text{LeadScore} = (\text{Score}_{\text{explicit}} \times 0.35) + (\text{Score}_{\text{implicit}} \times 0.25) + (\text{Similarity}_{\text{semantic}} \times 0.40)$$

Where grades are partitioned:
- **A_HOT** ($\ge 75$): Instant human closer routing or high-priority booking link.
- **B_WARM** ($50–74$): Consultative nurture sequence or automated pilot proposal.
- **C_NURTURE** ($30–49$): Asynchronous email drip with educational case studies.
- **D_COLD** ($< 30$): Automated archive or low-frequency newsletter subscription.

### Reciprocal Rank Fusion (RRF) SQL Query
When combining PostgreSQL full-text search (`tsvector`) with semantic dense vectors (`vector(1536)`):

```sql
WITH semantic_search AS (
  SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> $1) AS rank_dense
  FROM leads_catalog
  LIMIT 50
),
text_search AS (
  SELECT id, ROW_NUMBER() OVER (ORDER BY ts_rank(tsv, plainto_tsquery($2)) DESC) AS rank_sparse
  FROM leads_catalog
  WHERE tsv @@ plainto_tsquery($2)
  LIMIT 50
)
SELECT 
  COALESCE(s.id, t.id) AS lead_id,
  (COALESCE(1.0 / (60 + s.rank_dense), 0.0) + COALESCE(1.0 / (60 + t.rank_sparse), 0.0)) AS rrf_score
FROM semantic_search s
FULL OUTER JOIN text_search t ON s.id = t.id
ORDER BY rrf_score DESC
LIMIT 10;
```

---

## 3. Real-Time Battlecards via Bifrost AI Gateway

To guarantee sub-1.5s latency during live interactions, objection handling queries are routed through the local Bifrost AI Gateway at `http://bifrost:8080/v1`:
- **Semantic Caching:** Common objections (price, timing, competitor comparisons) are cached with cosine similarity thresholding (0.82), dropping response latency to <15ms.
- **Provider Cascade:** Automatically falls back between available LLM providers (e.g. Cerebras, Groq, Anthropic, OpenAI) with zero application code modification.

---

## 4. Contextual Human Handover Protocol

When a lead achieves grade `A_HOT`, triggers an explicit human request, or surfaces complex legal/procurement questions:
1. The AI engine serializes conversation history and qualification state via `HandoverBriefingSchema`.
2. Emits an event `sales.handover.requested` to NATS JetStream or triggers `ICrmAdapter.createDeal()`.
3. Sets conversational state to paused for AI, notifying human sales reps with full contextual briefing.
