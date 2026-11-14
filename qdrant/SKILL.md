---
name: qdrant
description: "Trigger: qdrant, vector db, qdrant@1.12, qdrant-client, @qdrant/js-client-rest, hybrid search, rrf, dense sparse, qdrant:single, qdrant:ha. Architect, optimize, connect, and operate Qdrant 1.12 vector search engine on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# Qdrant — Zerops Managed Vector Database & Hybrid Search Engine (v1.0)

## Activation Contract
Activate when architecting, querying, provisioning, or connecting to Qdrant 1.12, dense embeddings, sparse vectors (SPLADE), Hybrid Search with Reciprocal Rank Fusion (RRF), payload pre-filtering, or managing Zerops semi-managed services (`type: qdrant:single@1.12` or `type: qdrant:ha@1.12`).

## Hard Rules
- **Rule 1 (Version & Invariant)**: MUST use `qdrant:single@1.12` or `qdrant:ha@1.12`. Zero manual `verticalAutoscaling` min/max blocks (native LXC autoscaling).
- **Rule 2 (Mandatory Authentication)**: All client connections MUST authenticate via `api-key` header using `${qdrant_apiKey}` (read/write) or `${qdrant_readOnlyApiKey}` (public read-only).
- **Rule 3 (Port Routing Architecture)**:
  - Port `6333`: HTTP REST API and built-in Web UI (`/dashboard`).
  - Port `6334`: Binary gRPC protocol (3x lower latency, recommended for production).
- **Rule 4 (Hybrid Search with Server-Side RRF)**: Use Query API with `prefetch` and `query: { rrf: { k: 60 } }` to eliminate client-side fusion overhead.
- **Rule 5 (Payload Pre-Filtering)**: In multi-tenant systems, define keyword indexes on `tenant_id` and apply filter conditions before vector graph traversal.
- **Rule 6 (Fractal CoHaLo Bounded Execution)**: Enforce command timeouts (`timeout 10s`), wait limits (`WaitMsBeforeAsync: 10000`), and terminate orphan background tasks with `manage_task action="kill"`.

## Decision Gates

| Task / Scenario | Recommended Strategy | Reference / Asset |
|---|---|---|
| Vector DB Choice (Qdrant vs pgvector) | Qdrant for dedicated vector search (>500k, gRPC, RRF); pgvector for relational ACID | [`references/infra.md`](file:///var/www/.agents/skills/qdrant/references/infra.md) |
| Collection Setup (Dense + Sparse) | Named vectors (`dense-text`, `sparse-text`), Cosine distance | [`references/usage.md`](file:///var/www/.agents/skills/qdrant/references/usage.md) |
| Hybrid Search & RRF | Query API with `prefetch` and `query: { rrf: {} }` | [`references/usage.md`](file:///var/www/.agents/skills/qdrant/references/usage.md) |
| Multi-Tenancy Pre-Filtering | `createPayloadIndex('tenant_id', 'keyword')`, `must` filter | [`references/usage.md`](file:///var/www/.agents/skills/qdrant/references/usage.md) |
| Zerops Infrastructure (:single vs :ha) | Port 6333 / 6334, API keys, NVMe persistence, 4-Way Comparison | [`references/infra.md`](file:///var/www/.agents/skills/qdrant/references/infra.md) |
| Verified Client Recipes | TypeScript (`@qdrant/js-client-rest`), Python (`qdrant-client`), Go gRPC | [`assets/qdrant_production_recipes.json`](file:///var/www/.agents/skills/qdrant/assets/qdrant_production_recipes.json) |

## Critical Workflows / Execution Steps
1. Define `type: qdrant:single@1.12` or `type: qdrant:ha@1.12` in `import.yaml` and connect via `6333` (REST) or `6334` (gRPC) using `${qdrant_hostname}` and `${qdrant_apiKey}`.
2. Provision collections with named dense/sparse vectors and `tenant_id` keyword payload indexes.
3. Enforce CoHaLo bounds (`timeout 10s`, max 2 retries, `manage_task action="kill"`) and verify HTTP `200` on `:6333/healthz`.

## Output Contract
- Validated `import.yaml` and `zerops.yaml` manifests targeting Qdrant on Zerops.
- Verified collection creation, hybrid search, and payload filtering with zero orphaned tasks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/qdrant/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/qdrant/references/infra.md)
- [`assets/qdrant_production_recipes.json`](file:///var/www/.agents/skills/qdrant/assets/qdrant_production_recipes.json) · [`assets/import_template.yaml`](file:///var/www/.agents/skills/qdrant/assets/import_template.yaml) · [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/qdrant/assets/zerops_template.yaml)
- [`scripts/qdrant-validate.sh``skills-suite-validate`
