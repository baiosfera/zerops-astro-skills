# Sales Enablement: Topology & Zerops Infrastructure (v2.0)

> **SSoT Reference Document:** `.agents/skills/sales-enablement/references/infra.md`  
> **Scope:** High-concurrency sales mesh architecture, PostgreSQL 18 pgvector HNSW indexing, Bifrost AI Gateway routing, and NATS JetStream handover topics.

---

## 1. Network Topology & Service Mesh

The sales enablement engine runs within the Zerops Incus private network, communicating over dedicated private DNS endpoints:

```mermaid
graph TD
    subgraph Zerops_Incus_Network["Zerops Private Network"]
        SalesEngine["Sales Engine Service<br/>• BANT / CHAMP / MEDDPICC<br/>• Hybrid Scoring & Battlecards<br/>• Runtime: Bun 1.3+ / Node 24"]
        
        Bifrost["Bifrost AI Gateway<br/>• Port: 8080<br/>• Semantic Cache & Multi-Provider"]
        
        NATS["NATS 2.12 JetStream<br/>• Port: 4222<br/>• Stream: sales.handover.*"]
        
        Postgres["PostgreSQL 18 + pgvector<br/>• Port: 5432<br/>• HNSW Vector Search"]
        
        CRM["CRM Target (Pluggable SPI)<br/>• Directus / HubSpot / Webhook"]
    end

    SalesEngine -->|Objection & Prompt Synthesis| Bifrost
    SalesEngine -->|Vector Cosine Search & ACID State| Postgres
    SalesEngine -->|Async Handover Events| NATS
    SalesEngine -->|Deal Creation & Sync| CRM
```

---

## 2. PostgreSQL 18 Schema & HNSW Vector Index

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS leads_embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL UNIQUE,
  contact_name TEXT NOT NULL,
  company_name TEXT,
  industry TEXT,
  tsv TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', coalesce(contact_name, '') || ' ' || coalesce(company_name, '') || ' ' || coalesce(industry, ''))) STORED,
  embedding vector(1536) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Fast HNSW cosine index for sub-2ms nearest-neighbor retrieval
CREATE INDEX IF NOT EXISTS idx_leads_embeddings_hnsw 
ON leads_embeddings 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 24, ef_construction = 100);

-- GIN index for full-text search sparse ranking
CREATE INDEX IF NOT EXISTS idx_leads_embeddings_tsv
ON leads_embeddings
USING gin (tsv);
```

---

## 3. Required Environment Variables

```ini
# ============================================================================
# BIFROST AI GATEWAY (PORT 8080)
# ============================================================================
BIFROST_URL="http://bifrost:8080/v1"
BIFROST_API_KEY="bf-service-token-internal"

# ============================================================================
# POSTGRESQL 18 & PGVECTOR
# ============================================================================
DATABASE_URL="postgres://zerops:password@database:5432/app_db"

# ============================================================================
# NATS JETSTREAM HANDOVER
# ============================================================================
NATS_URL="nats://nats:4222"
NATS_HANDOVER_STREAM="SALES_EVENTS"

# ============================================================================
# CRM ADAPTER CONFIGURATION (PLUGGABLE SPI)
# ============================================================================
CRM_PROVIDER="directus" # directus | postgres | webhook
DIRECTUS_URL="http://directus:8055"
DIRECTUS_SERVER_TOKEN="directus_admin_or_service_token"
CRM_WEBHOOK_URL="http://sales-agent:3000/api/crm/webhook"
```
