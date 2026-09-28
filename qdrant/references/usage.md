# Qdrant 1.12 — Developer & Architecture Usage Manual on Zerops

This manual provides production-tested specifications, collection provisioning patterns, multi-vector setups (Dense + Sparse), Hybrid Search with Reciprocal Rank Fusion (RRF), payload pre-filtering, and polyglot client recipes for **Qdrant 1.12** on Zerops.

---

## 1. Core Qdrant Concepts & Client Initialization

### A. Client Initialization in TypeScript (`@qdrant/js-client-rest`)
```typescript
import { QdrantClient } from '@qdrant/js-client-rest';

export const qdrant = new QdrantClient({
  url: `http://${process.env.QDRANT_HOST || 'qdrant'}:${process.env.QDRANT_PORT || '6333'}`,
  apiKey: process.env.QDRANT_API_KEY,
  checkCompatibility: true
});
```

### B. Multi-Vector Collection Setup (Named Dense + Sparse)
```typescript
await qdrant.createCollection('knowledge_base', {
  vectors: {
    'dense-text': {
      size: 1536, // e.g. text-embedding-3-small
      distance: 'Cosine'
    }
  },
  sparse_vectors: {
    'sparse-text': {
      index: {
        on_disk: false // Keep sparse index in memory for fast retrieval
      }
    }
  },
  quantization_config: {
    scalar: {
      type: 'int8',
      quantile: 0.99,
      always_ram: true
    }
  }
});

// Index payload field for sub-millisecond pre-filtering
await qdrant.createPayloadIndex('knowledge_base', {
  field_name: 'tenant_id',
  field_schema: 'keyword'
});
```

---

## 2. Ingestion & Fast Point Upsert

```typescript
await qdrant.upsert('knowledge_base', {
  wait: true,
  points: [
    {
      id: 'doc_98124',
      vector: {
        'dense-text': [0.012, -0.045, 0.089, /* ... 1536 dims */],
        'sparse-text': {
          indices: [142, 891, 10294],
          values: [0.85, 0.42, 0.99]
        }
      },
      payload: {
        tenant_id: 'org_acme_corp',
        document_type: 'contract',
        created_at: 1719500000,
        content: 'Master services agreement clause 4...'
      }
    }
  ]
});
```

---

## 3. Hybrid Search with Reciprocal Rank Fusion (RRF)

Using the Query API with `prefetch` sub-requests and server-side RRF scoring:

```typescript
const hybridResults = await qdrant.query('knowledge_base', {
  prefetch: [
    {
      query: {
        indices: [142, 10294],
        values: [0.75, 0.91]
      },
      using: 'sparse-text',
      limit: 25,
      filter: {
        must: [{ key: 'tenant_id', match: { value: 'org_acme_corp' } }]
      }
    },
    {
      query: [0.012, -0.042, 0.091, /* ... query dense vector */],
      using: 'dense-text',
      limit: 25,
      filter: {
        must: [{ key: 'tenant_id', match: { value: 'org_acme_corp' } }]
      }
    }
  ],
  query: {
    rrf: { k: 60 } // Server-side Reciprocal Rank Fusion
  },
  limit: 10,
  with_payload: true
});

console.log('Hybrid Search Results:', hybridResults.points);
```

---

## 4. Production Patterns & Verified Polyglot Recipes

### Pattern 1: Python `qdrant-client` Async FastEmbed Integration
```python
import os
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = AsyncQdrantClient(
    host=os.getenv("QDRANT_HOST", "qdrant"),
    port=int(os.getenv("QDRANT_GRPC", "6334")),
    api_key=os.getenv("QDRANT_API_KEY"),
    prefer_grpc=True
)

async def search_documents(query_dense: list[float], tenant_id: str, limit: int = 10):
    response = await client.query_points(
        collection_name="knowledge_base",
        query=query_dense,
        using="dense-text",
        query_filter={
            "must": [{"key": "tenant_id", "match": {"value": tenant_id}}]
        },
        limit=limit
    )
    return response.points
```

### Pattern 2: Go `qdrant/go-client` High-Throughput Ingestion
```go
package main

import (
	"context"
	"log"
	"os"
	"github.com/qdrant/go-client/qdrant"
)

func main() {
	client, err := qdrant.NewClient(&qdrant.Config{
		Host:   os.Getenv("QDRANT_HOST"),
		Port:   6334,
		APIKey: os.Getenv("QDRANT_API_KEY"),
		UseTLS: false,
	})
	if err != nil {
		log.Fatalf("Failed to connect: %v", err)
	}
	defer client.Close()

	health, err := client.HealthCheck(context.Background())
	if err != nil {
		log.Fatalf("Health check failed: %v", err)
	}
	log.Printf("Qdrant Version: %s", health.GetVersion())
}
```

---

## 5. Anti-Patterns & Gotchas in Zerops

| Anti-Pattern | Why it Fails | Correct Solution |
|---|---|---|
| Connecting without `api-key` header | Qdrant in Zerops enforces API key authentication $\to$ 401 Unauthorized | Always supply `${qdrant_apiKey}` or `${qdrant_readOnlyApiKey}`. |
| Client-side manual rank fusion | Transmits huge intermediate vector payloads over the network | Use server-side Query API with `prefetch` and `query: { rrf: { k: 60 } }`. |
| Missing payload keyword indexes | Full-table scans on unindexed payload attributes during pre-filtering | Create payload index with `createPayloadIndex(field, 'keyword')`. |
| Hardcoding `verticalAutoscaling` | Overrides native dynamic autoscaling on Incus LXC | Omit `verticalAutoscaling` and allow Zerops to auto-scale. |
| Using internal TLS on port 6333/6334 | Internal communication is plaintext over encrypted VXLAN | Connect via plaintext internal ports; TLS is only used on external ingress. |
