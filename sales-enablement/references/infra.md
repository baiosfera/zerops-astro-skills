# Sales Enablement: Topología & Infraestructura Zerops (v1.0)

> **SSoT Reference Document:** `.agents/skills/sales-enablement/references/infra.md`  
> **Ámbito:** Directus 11+ CRM, colecciones de prospección, PostgreSQL 18 con `pgvector` HNSW y variables de entorno.

---

## 1. Topología del Motor de Sales Enablement en Zerops

El motor de ventas se integra con Directus 11+ (Headless CRM) y PostgreSQL 18 con extensión `pgvector` para el scoring semántico en tiempo real:

```mermaid
graph TD
    subgraph Zerops_Incus_Network["Red Privada del Proyecto Zerops"]
        SalesEngine["Servicio Sales Enablement (Node 24)<br/>• Motor BANT/CHAMP & Lead Scoring<br/>• Selector de Battlecards Dinámicas<br/>• Puerto: 3005"]
        
        Directus["Servicio Directus 11+ (Headless CRM)<br/>• Colecciones: leads, crm_deals, battlecards<br/>• Puerto: 8055"]
        
        Postgres["Servicio PostgreSQL 18<br/>• Tabla: leads_embeddings (pgvector HNSW)<br/>• Puerto: 5432"]
    end

    SalesEngine -->|Cálculo Similitud Coseno (<=>)| Postgres
    SalesEngine -->|Creación de Deal & Handover| Directus
```

---

## 2. DDL para Lead Scoring Vectorial en PostgreSQL 18

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS leads_embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL UNIQUE,
  contact_name TEXT NOT NULL,
  company_name TEXT,
  industry TEXT,
  embedding vector(1536) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índice HNSW con métrica coseno para scoring semántico (<1ms)
CREATE INDEX IF NOT EXISTS idx_leads_embeddings_hnsw 
ON leads_embeddings 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 24, ef_construction = 100);
```

---

## 3. Required Environment Variables

```ini
# ============================================================================
# DIRECTUS 11+ CRM
# ============================================================================
DIRECTUS_URL="http://directus:8055"
DIRECTUS_SERVER_TOKEN="directus_admin_or_service_token_2026"

# ============================================================================
# POSTGRESQL 18 & PGVECTOR
# ============================================================================
DATABASE_URL="postgres://zerops:password@postgres:5432/crm_db"

# ============================================================================
# AI & EMBEDDINGS
# ============================================================================
OPENAI_API_KEY="sk-proj-..."
ICP_TARGET_EMBEDDING="[-0.012, 0.045, ...]" # Embedding serializado del Perfil Ideal
```
