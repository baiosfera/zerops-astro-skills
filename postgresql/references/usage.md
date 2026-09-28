# PostgreSQL 18 — Developer & Architecture Usage Manual on Zerops

This manual provides production-tested specifications, PostgreSQL 18 LTS features (Async Direct I/O, SQL/JSON `JSON_TABLE`, `uuidv7()`), `pgvector` v0.8+ vector search calibration, and canonical ORM connection patterns on Zerops.

---

## 1. PostgreSQL 18 LTS Engine Features

### A. SQL/JSON Standard `JSON_TABLE`
Transforms nested hierarchical JSON documents directly into relational tabular rows without intermediate plpgsql functions:

```sql
SELECT jt.id, jt.username, jt.role, jt.created_at
FROM raw_events,
JSON_TABLE(
  event_data, '$.users[*]'
  COLUMNS (
    id INT PATH '$.id',
    username TEXT PATH '$.username',
    role TEXT PATH '$.role' DEFAULT 'member' ON EMPTY,
    created_at TIMESTAMP PATH '$.created_at'
  )
) AS jt;
```

### B. Native `uuidv7()` & Virtual Generated Columns
`uuidv7()` generates time-ordered UUIDs that prevent B-Tree index fragmentation under high-concurrency inserts. Virtual generated columns compute values on read with zero disk footprint:

```sql
CREATE TABLE orders (
  id UUID PRIMARY KEY DEFAULT uuidv7(),
  subtotal NUMERIC(12, 2) NOT NULL,
  tax_rate NUMERIC(4, 2) NOT NULL,
  total NUMERIC(12, 2) GENERATED ALWAYS AS (subtotal * (1 + tax_rate)) VIRTUAL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### C. Enhanced RETURNING with OLD and NEW References
```sql
UPDATE users
SET email = 'newemail@example.com'
WHERE id = '018f4a12-7000-7c2a-9e1b-252f5b61a34d'
RETURNING OLD.email AS previous_email, NEW.email AS updated_email;
```

---

## 2. High-Performance Vector Search with `pgvector` (v0.8+)

### A. Supported Vector Column Types
* `vector(1536)`: Standard 32-bit floating point embeddings (~6 KB per 1536-dim vector).
* `halfvec(1536)`: 16-bit floating point embeddings (cuts RAM and disk usage by 50% with negligible loss in accuracy).
* `bit(1024)`: 1 bit per dimension for binary quantized embeddings with Hamming distance `<~>` (up to 30x storage reduction).
* `sparsevec(10000)`: Sparse vector representations for BM25/hybrid search.

### B. Index Calibration (HNSW vs IVFFlat)
```sql
-- HNSW (Multi-layer graph for low-latency RAG retrieval)
CREATE INDEX idx_documents_embedding_hnsw ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 128);

-- IVFFlat (Inverted file clustering for massive datasets)
CREATE INDEX idx_documents_embedding_ivf ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### C. Query-Time Tuning
```sql
-- Calibrate recall vs latency dynamically per transaction
SET LOCAL hnsw.ef_search = 100;

SELECT id, title, content, embedding <=> $1::vector AS distance
FROM documents
ORDER BY distance ASC
LIMIT 5;
```

---

## 3. Production Patterns & Verified Code Recipes

### Pattern 1: High-Speed Bun.SQL Client
```typescript
import { SQL } from "bun";

export const db = new SQL({
  url: process.env.DATABASE_URL!,
  max: 20,
  idleTimeout: 30,
  maxLifetime: 3600,
  tls: false // Internal VXLAN encrypted private network
});

export async function searchSimilar(vector: number[]) {
  return await db`
    SELECT id, title, embedding <=> ${JSON.stringify(vector)}::vector AS distance
    FROM documents
    ORDER BY distance ASC
    LIMIT 5;
  `;
}
```

### Pattern 2: Node.js `pg` Connection Pool
```typescript
import { Pool } from 'pg';

export const pool = new Pool({
  host: process.env.DB_HOST || 'db',
  port: parseInt(process.env.DB_PORT || '5432', 10),
  user: process.env.DB_USER,
  password: process.env.DB_PASS,
  database: process.env.DB_NAME || 'db',
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
  ssl: false
});
```

### Pattern 3: Python `asyncpg` High-Performance Pool
```python
import asyncpg
import os

async def create_db_pool():
    return await asyncpg.create_pool(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME", "db"),
        min_size=5,
        max_size=20,
        command_timeout=10.0
    )
```

### Pattern 4: Go `pgx/v5` Binary Connection Pool
```go
package db

import (
	"context"
	"os"
	"github.com/jackc/pgx/v5/pgxpool"
)

func NewPool(ctx context.Context) (*pgxpool.Pool, error) {
	connString := os.Getenv("DATABASE_URL")
	config, err := pgxpool.ParseConfig(connString)
	if err != nil {
		return nil, err
	}
	config.MaxConns = 25
	config.MinConns = 5
	return pgxpool.NewWithConfig(ctx, config)
}
```

### Pattern 5: Rust `sqlx` Async Pool
```rust
use sqlx::postgres::{PgPool, PgPoolOptions};
use std::env;

pub async fn establish_connection() -> Result<PgPool, sqlx::Error> {
    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    PgPoolOptions::new()
        .max_connections(20)
        .connect(&database_url)
        .await
}
```

---

## 4. Anti-Patterns & Gotchas in Zerops

| Anti-Pattern | Why it Fails | Correct Solution |
|---|---|---|
| Installing extensions without service restart | Extension shared libraries remain uninitialized | Run `CREATE EXTENSION` with superuser and execute `zerops_manage action="restart"`. |
| Modifying the internal `zps` user | Breaks Zerops platform healthchecks and telemetry | Never modify, alter, or drop the `zps` user. |
| Hardcoding `verticalAutoscaling` | Overrides native dynamic autoscaling tier defined by `profile:` | Use `profile:` (`oltp-hobby`, `oltp-staging`, `oltp-production`) and let Zerops auto-scale. |
| Using internal SSL for port 5432 | Port 5432 is internal plaintext over VXLAN; SSL handshake fails | Set `ssl: false` on internal connections; use port 6432 (`${db_portTls}`) for external TLS. |
| Expecting immediate sync on port 5433 | Read replicas replicate asynchronously with minimal lag | Route writes strictly to 5432; use 5433 only for read-tolerant queries. |
