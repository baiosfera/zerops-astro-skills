# Directus 11+ Developer Manual: SDK, Flows, RAG, Telemetry & Full-Stack Zerops Engine (v2.0)

Directus 11+ (`directus`) is an enterprise-grade Headless CMS, Backend-as-a-Service (BaaS), and relational data engine built on Node.js/TypeScript. It introspects PostgreSQL 18 databases directly without imposing proprietary ORM layers, providing instant REST and GraphQL APIs, real-time WebSockets, automated Flows, extension hooks, and zero-bloat Insights dashboards.

In Zerops, Directus serves as the **Single Source of Truth (SSoT)** and unified backend engine for **`bknd`**, **`devllm-telemetry`**, **`business-insights`**, **Astro** frontends, **RAG semantic search (`pgvector`)**, and **WhatsApp engines** ([`whatsapp-engine`](file:///var/www/.agents/skills/whatsapp-engine/SKILL.md)).

---

## 1. 4D Comparative Architectural Matrix

| Dimension | Directus 11+ (Target) | Strapi v5 | Supabase (Self-hosted) | Payload CMS v3 |
|---|---|---|---|---|
| **Database Architecture** | **Direct SQL Introspection** (Zero ORM overhead) | Schema-driven with internal ORM | Pure PostgreSQL with PostgREST | Next.js / Node.js with Drizzle/Mongoose |
| **Supported Databases** | **PostgreSQL 18, MySQL, SQLite, Oracle, MSSQL** | PostgreSQL, MySQL, SQLite | PostgreSQL only | PostgreSQL, MongoDB |
| **Admin Panel (Studio)** | **Vue 3 UI, drag & drop, no-code Dashboards** | React Admin UI | React Dashboard Studio | React / Next.js integrated UI |
| **Automation Engine** | **Directus Flows nativo** (Visual, Cron, Webhooks, Script) | Cron & Lifecycle Hooks manuales | Database Webhooks & pg_cron | Next.js Server Actions & Hooks |
| **Multi-Node Sync & Caching**| **Valkey/Redis native** (`SYNCHRONIZATION_STORE`) | Redis manual | Redis / Realtime Go server | Redis / Memory cache |
| **AI, Embeddings & RAG** | **Native MCP Server + `pgvector` HNSW indexing** | External plugins | `pgvector` via SQL functions | Manual implementation in code |
| **Telemetry & BI Dashboards**| **Native Directus Insights (~0 MB extra RAM)** | Heavy plugins / Grafana | Supabase Logs / Grafana | Custom dashboard pages |
| **Zerops Execution Profile** | **100% Native on Incus LXC (`nodejs@24` Ubuntu)** | Node.js Runtime in Zerops | Multi-container Docker VM | Node.js Runtime in Zerops |

### Zerops Runtime Profile: `os: ubuntu` vs `os: alpine`

| Operating Characteristic | Directus 11+ on `os: ubuntu` (Recommended SSoT) | Directus 11+ on `os: alpine` |
|---|---|---|
| **Image Processing (`sharp`)**| **100% Stable & Compatible** (Native Debian glibc) | Requires musl pre-compilation & libvips patches |
| **Database Drivers (`pg`)** | **Optimized for glibc 2.39** | musl libc (can show thread pool latency) |
| **Bootstrap Cold Boot** | **Fast (< 3 seconds)** | ~5–8 seconds |
| **System Utilities** | `apt-get install -y ffmpeg curl ca-certificates` | `apk add --no-cache ffmpeg curl` |
| **Zerops Suitability** | **Standard SSoT for Directus in Zerops** | Not recommended for production Sharp builds |

---

## 2. Data Engine & Schema Management on PostgreSQL 18

Directus connects directly to PostgreSQL 18 without code generation or abstract schema layers:
* **System Collections (`directus_*`)**: Manage RBAC roles, permissions, audit logs, file metadata, and dashboards.
* **Declarative CLI Schema Management**:
  ```bash
  # Snapshot current data model
  npx directus schema snapshot ./schema.yaml

  # Diff changes against production database
  npx directus schema diff ./schema.yaml

  # Apply atomic schema migrations
  npx directus schema apply ./schema.yaml
  ```

---

## 3. Composable `@directus/sdk` Client (TypeScript)

```typescript
import {
  createDirectus,
  rest,
  graphql,
  authentication,
  realtime,
  readItems,
  createItem,
  updateItem,
  staticToken
} from '@directus/sdk';

export interface AppSchema {
  articles: {
    id: number;
    title: string;
    slug: string;
    content: string;
    status: 'draft' | 'published';
    published_at: string | null;
  }[];
  orders: {
    id: string;
    customer_email: string;
    customer_name: string;
    total_amount: number;
    status: 'pending' | 'completed' | 'cancelled';
  }[];
  llm_telemetry_logs: {
    id: string;
    model_name: string;
    prompt_tokens: number;
    completion_tokens: number;
    total_cost_usd: number;
    latency_ms: number;
    caller_service: string;
    timestamp: string;
  }[];
}

// Initializing typed client with Cookie Auth, REST, GraphQL and WebSockets
export const directus = createDirectus<AppSchema>('http://directus:8055')
  .with(staticToken(process.env.DIRECTUS_STATIC_TOKEN || ''))
  .with(rest())
  .with(graphql())
  .with(realtime());

// Type-Safe Relational Queries with Sorting and Filtering
export async function getPublishedArticles() {
  return await directus.request(
    readItems('articles', {
      filter: { status: { _eq: 'published' } },
      sort: ['-published_at'],
      limit: 10,
      fields: ['id', 'title', 'slug', 'published_at']
    })
  );
}

// Real-Time Live WebSocket Subscriptions
export function subscribeToOrders(onNewOrder: (order: any) => void) {
  const { subscribe } = directus.with(realtime());
  return subscribe('orders', {
    event: 'create',
    query: { fields: ['id', 'customer_name', 'total_amount', 'status'] }
  }, (message) => {
    if (message.type === 'subscription' && message.event === 'create') {
      onNewOrder(message.data[0]);
    }
  });
}
```

---

## 4. Backend Engine for `devllm-telemetry` (Zero-RAM LLMOps Observability)

Directus stores all AI token usage and infrastructure health logs natively in PostgreSQL 18, rendering real-time dashboards via Directus Insights without spinning up Prometheus or Grafana:

### Collection Schemas

| Collection Name | Key Attributes | Ingestion Mechanism |
|---|---|---|
| **`llm_telemetry_logs`** | `model_name`, `prompt_tokens`, `completion_tokens`, `total_cost_usd`, `latency_ms`, `caller_service`, `status` | Async fire-and-forget API / NATS event |
| **`system_health_logs`** | `nats_connections`, `nats_in_msgs`, `valkey_used_memory_mb`, `bullmq_dlq_count`, `last_backup_status` | 60s background poller script |

### Non-Blocking Telemetry Ingestion (Node.js / Bun)

```typescript
export async function recordLLMUsage(data: {
  model: string;
  promptTokens: number;
  completionTokens: number;
  costUsd: number;
  latencyMs: number;
  service: string;
}) {
  // Fire-and-forget: does not block the caller
  directus.request(
    createItem('llm_telemetry_logs', {
      model_name: data.model,
      prompt_tokens: data.promptTokens,
      completion_tokens: data.completionTokens,
      total_cost_usd: data.costUsd,
      latency_ms: data.latencyMs,
      caller_service: data.service,
      timestamp: new Date().toISOString()
    })
  ).catch(err => console.error('[Telemetry] Logging error:', err.message));
}
```

---

## 5. Backend Engine for `business-insights` (Commercial & Financial Analytics)

Directus Insights aggregates commercial metrics directly from relational tables, syncing P&L data with Frappe Cloud ERPNext:

### Core Metric Aggregation Queries

```sql
-- 1. Real-Time Gross Merchandise Value (GMV - Last 30 Days)
SELECT SUM(total_amount) AS gmv_30d
FROM orders
WHERE status = 'completed' AND created_at >= NOW() - INTERVAL '30 days';

-- 2. Average Order Value (AOV / Average Ticket)
SELECT AVG(total_amount) AS aov
FROM orders
WHERE status = 'completed';

-- 3. Checkout Funnel Conversion Rate
SELECT 
  (COUNT(CASE WHEN event_type = 'checkout_completed' THEN 1 END)::float / 
   NULLIF(COUNT(CASE WHEN event_type = 'checkout_initiated' THEN 1 END), 0) * 100) AS conversion_rate
FROM funnel_events
WHERE created_at >= NOW() - INTERVAL '30 days';
```

---

## 6. Backend Engine for `bknd` (Astro Actions + NATS RPC Triad)

```typescript
// src/actions/checkout.ts
import { defineAction, ActionError } from 'astro:actions';
import { z } from 'astro:schema';
import { connect, JSONCodec } from 'nats';
import { createDirectus, rest, createItem, staticToken } from '@directus/sdk';

const jc = JSONCodec();
const directus = createDirectus(process.env.DIRECTUS_URL || 'http://directus:8055')
  .with(staticToken(process.env.DIRECTUS_STATIC_TOKEN || ''))
  .with(rest());

export const server = {
  processOrder: defineAction({
    accept: 'json',
    input: z.object({
      customerEmail: z.string().email(),
      customerName: z.string().min(2),
      customerPhone: z.string().min(10),
      items: z.array(z.object({ productId: z.string(), quantity: z.number() })),
      totalAmount: z.number().positive(),
    }),
    handler: async (input) => {
      const nc = await connect({ servers: process.env.NATS_URL || 'nats://nats:4222' });
      
      // 1. Atomic NATS RPC Inventory Lock (<0.3ms P99)
      const rpcRes = await nc.request('inventory.lock', jc.encode({ items: input.items }), { timeout: 2000 });
      const lockData = jc.decode(rpcRes.data) as { success: boolean; lockId?: string };

      if (!lockData.success) {
        throw new ActionError({ code: 'PRECONDITION_FAILED', message: 'Inventory unavailable.' });
      }

      // 2. Persist in Directus 11+
      const order = await directus.request(
        createItem('orders', {
          customer_email: input.customerEmail,
          customer_name: input.customerName,
          customer_phone: input.customerPhone,
          total_amount: input.totalAmount,
          status: 'pending_payment',
          inventory_lock_id: lockData.lockId,
        })
      );

      return { success: true, orderId: order.id };
    }
  })
};
```

---

## 7. Directus Flows & Automation Engine

Directus Flows provides visual event-driven automation:

* **Triggers**:
  - `Event Hook`: Listen to collection lifecycle events (`items.create`, `items.update`, `items.delete`).
  - `Webhook`: External HTTP trigger receiving incoming requests.
  - `Schedule (Cron)`: Periodic tasks (e.g. `0 9 * * 1-5` for morning CRM summary).
  - `Manual`: Button triggered by staff in Directus Studio.
* **Operations**:
  - `Run Script`: Sandboxed JavaScript execution with custom payload transformations.
  - `Request URL`: Webhook dispatcher sending events to NATS or Evolution Go WhatsApp gateway.
  - `Read / Create / Update Data`: Direct database mutations without API latency.

---

## 8. RAG & Semantic Vector Search with PostgreSQL `pgvector`

### Automatic Embedding Generation Hook (`defineHook`)

```typescript
import { defineHook } from '@directus/extensions-sdk';
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default defineHook(({ action }) => {
  // Vectorize document upon creation
  action('knowledge_base.items.create', async (meta, { database }) => {
    try {
      const item = await database('knowledge_base').where('id', meta.key).first();
      if (!item || !item.content) return;

      const embeddingRes = await openai.embeddings.create({
        model: 'text-embedding-3-small',
        input: `${item.title}\n\n${item.content}`,
      });

      const vector = embeddingRes.data[0].embedding;

      // Update vector column in PostgreSQL directly
      await database('knowledge_base')
        .where('id', meta.key)
        .update({ embedding: JSON.stringify(vector) });

      console.log(`[RAG] Document ${meta.key} vectorized successfully.`);
    } catch (err: any) {
      console.error('[RAG] Vectorization failed:', err.message);
    }
  });
});
```

### Semantic Cosine Search Endpoint (`defineEndpoint`)

```typescript
import { defineEndpoint } from '@directus/extensions-sdk';
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default defineEndpoint((router, { database }) => {
  router.post('/semantic-search', async (req, res) => {
    try {
      const { query, limit = 5 } = req.body;
      if (!query) return res.status(400).json({ error: 'Query required' });

      const embeddingRes = await openai.embeddings.create({
        model: 'text-embedding-3-small',
        input: query,
      });

      const vector = JSON.stringify(embeddingRes.data[0].embedding);

      // Execute cosine distance search (<=>) on PostgreSQL pgvector
      const results = await database.raw(`
        SELECT id, title, content, 1 - (embedding <=> ?::vector) AS similarity
        FROM knowledge_base
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> ?::vector
        LIMIT ?
      `, [vector, vector, limit]);

      res.json({ results: results.rows });
    } catch (err: any) {
      res.status(500).json({ error: err.message });
    }
  });
});
```

---

## 9. 5 Production Patterns in Zerops

### Pattern 1: Unified BaaS for LLMOps Telemetry and Business Insights
Directus acts as the unified data store for AI token usage and commercial sales KPIs, rendering real-time dashboards with zero extra container overhead.

### Pattern 2: Omnichannel CRM with Directus + NATS + Evolution Go (WhatsApp)
Directus Flows emit mutation events to NATS (`events.directus.orders`), triggering automated WhatsApp order confirmations via Evolution Go without blocking database operations.

### Pattern 3: Automated RAG Document Vectorization in Directus Lifecycle Hooks
Content editors author articles in Directus Studio; background hooks automatically vectorize text with OpenAI and persist vectors in PostgreSQL for AI agents.

### Pattern 4: Astro SSR Portal with Google OAuth 2.0 & Directus SDK
Astro SSR frontend handles Google OAuth 2.0 callbacks and issues HTTP-only session cookies connected to Directus user profiles.

### Pattern 5: Multi-Node Schema Synchronization with Valkey Cache Auto-Purge
Enabling `SYNCHRONIZATION_STORE=redis` and `CACHE_AUTO_PURGE=true` ensures horizontally scaled Directus containers in Zerops stay synchronized with zero stale cache reads.

---

## 10. Anti-Patterns & Common Gotchas

1. **Omitting `zsc execOnce` on Bootstrap**: Running `npx directus bootstrap` without `zsc execOnce` on multi-container deployments causes concurrent database table creation race conditions.
2. **Deploying on Alpine for Sharp Image Processing**: Running Directus on Alpine can trigger `sharp` / `libvips` compilation failures and memory crashes. Always use `os: ubuntu`.
3. **Synchronous Telemetry Logging**: Blocking client requests to write telemetry records synchronously adds latency. Always use non-blocking fire-and-forget or NATS streams.
4. **Hardcoding OAuth Credentials**: Never hardcode Google Client ID or Secret in code. Use Zerops runtime variables (`AUTH_GOOGLE_CLIENT_ID`).
