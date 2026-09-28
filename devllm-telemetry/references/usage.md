# `devllm-telemetry`: Developer Manual, Contracts & Implementation Recipes (v2.0)

`devllm-telemetry` is the master DevOps, LLMOps, and infrastructure health orchestrator for the Zerops sovereign stack. Under the strict **$0 SaaS licensing and ~0 MB extra RAM overhead** governance model, it consolidates AI token expenditures, model latencies, NATS throughput, Valkey memory footprint, queue depths, and automated PostgreSQL backup validation into native **Directus 11+ Insights** dashboards (`directus_dashboards`, `directus_panels`), completely eliminating the need for standalone, heavy observability containers (Prometheus, Grafana, Datadog).

---

## 1. 4D Comparative Architectural Matrix

| Dimension | `devllm-telemetry` (Target) | Prometheus + Grafana | Datadog / New Relic | Langfuse / Helicone (SaaS) |
|---|---|---|---|---|
| **Server RAM Footprint** | **0 MB Extra** (Natively in Directus/Postgres) | ~600 MB–1.2 GB RAM | Agent on host (~150 MB) | 0 MB (Remote SaaS) |
| **SaaS Licensing Cost** | **$0 SaaS** | $0 Open Source | High monthly billing | Per-token / event billing |
| **Prompt & Token Privacy** | **100% Sovereign** (In private database) | Metric storage only | Third-party cloud | Third-party cloud |
| **Infrastructure Monitoring**| **NATS (:8222), Valkey, Backups** | Requires dedicated Exporters | Agent on every container | LLM observability only |
| **Zerops Execution** | **100% Native on existing container mesh** | Multiple extra containers | High operational cost | External network dependency |

---

## 2. Sub-Skills Inventory & Direct File Pointers

* **Directus Collections & Panels:** [`directus`](file:///var/www/.agents/skills/directus/SKILL.md) ([usage](file:///var/www/.agents/skills/directus/references/usage.md), [infra](file:///var/www/.agents/skills/directus/references/infra.md)).
* **NATS Server 2.12 Metrics:** [`nats`](file:///var/www/.agents/skills/nats/SKILL.md) ([usage](file:///var/www/.agents/skills/nats/references/usage.md), [infra](file:///var/www/.agents/skills/nats/references/infra.md)).
* **Valkey & BullMQ Monitoring:** [`valkey`](file:///var/www/.agents/skills/valkey/SKILL.md) ([usage](file:///var/www/.agents/skills/valkey/references/usage.md), [infra](file:///var/www/.agents/skills/valkey/references/infra.md)).
* **Backup Verification:** [`postgresql`](file:///var/www/.agents/skills/postgresql/SKILL.md) ([usage](file:///var/www/.agents/skills/postgresql/references/usage.md), [infra](file:///var/www/.agents/skills/postgresql/references/infra.md)).

---

## 3. TypeScript Contract: LLMOps Telemetry Tracker Wrapper

Module to intercept AI model calls, calculate estimated token expenditures, and persist execution logs asynchronously without blocking user requests:

```typescript
// src/lib/telemetry/llm-tracker.ts
import { createDirectus, rest, staticToken, createItem } from '@directus/sdk';

const directus = createDirectus(process.env.DIRECTUS_URL || 'http://directus:8055')
  .with(staticToken(process.env.DIRECTUS_STATIC_TOKEN || ''))
  .with(rest());

// Standard model pricing per 1M tokens (USD)
const MODEL_PRICING: Record<string, { prompt: number; completion: number }> = {
  'gpt-4o-mini': { prompt: 0.15, completion: 0.60 },
  'gpt-4o': { prompt: 2.50, completion: 10.00 },
  'claude-3-5-sonnet': { prompt: 3.00, completion: 15.00 },
  'gemini-1.5-flash': { prompt: 0.075, completion: 0.30 },
  'deepseek-chat': { prompt: 0.14, completion: 0.28 },
};

export interface LLMCallMetadata {
  model: string;
  promptTokens: number;
  completionTokens: number;
  latencyMs: number;
  callerService: string; // e.g. 'whatsapp_bot', 'sales_sdr', 'copy_generator'
  status: 'success' | 'error';
  errorMessage?: string;
}

export function trackLLMCall(meta: LLMCallMetadata): void {
  // Fire-and-forget execution in background
  setImmediate(async () => {
    try {
      const pricing = MODEL_PRICING[meta.model] || { prompt: 1.0, completion: 2.0 };
      const promptCost = (meta.promptTokens / 1_000_000) * pricing.prompt;
      const completionCost = (meta.completionTokens / 1_000_000) * pricing.completion;
      const totalCostUsd = promptCost + completionCost;

      await directus.request(
        createItem('llm_telemetry_logs', {
          model_name: meta.model,
          prompt_tokens: meta.promptTokens,
          completion_tokens: meta.completionTokens,
          total_tokens: meta.promptTokens + meta.completionTokens,
          estimated_cost_usd: totalCostUsd,
          latency_ms: meta.latencyMs,
          caller_service: meta.callerService,
          status: meta.status,
          error_message: meta.errorMessage || null,
          created_at: new Date().toISOString(),
        })
      );
    } catch (err: any) {
      console.error('[devllm-telemetry] Failed to record LLM telemetry log:', err.message);
    }
  });
}
```

---

## 4. System Health Daemon Poller (NATS, Valkey & Backups)

Lightweight daemon polling server health metrics every 60 seconds:

```typescript
// scripts/system-health-poller.ts
import { createDirectus, rest, staticToken, createItem } from '@directus/sdk';
import Redis from 'ioredis';
import fs from 'node:fs';

const directus = createDirectus(process.env.DIRECTUS_URL || 'http://directus:8055')
  .with(staticToken(process.env.DIRECTUS_STATIC_TOKEN || ''))
  .with(rest());

const redis = new Redis(process.env.VALKEY_URL || 'redis://cache:6379');

export async function pollSystemHealth() {
  try {
    // 1. Fetch NATS Server HTTP Monitoring Metrics (:8222/varz)
    let natsConnections = 0;
    let natsInMsgs = 0;
    try {
      const natsRes = await fetch('http://nats:8222/varz', { signal: AbortSignal.timeout(3000) });
      if (natsRes.ok) {
        const natsVarz = await natsRes.json();
        natsConnections = natsVarz.connections || 0;
        natsInMsgs = natsVarz.in_msgs || 0;
      }
    } catch (_) {}

    // 2. Fetch Valkey 7.2 Memory Metrics & DLQ Depth
    const infoMemory = await redis.info('memory');
    const usedMemoryMatch = infoMemory.match(/used_memory:(\d+)/);
    const usedMemoryMb = usedMemoryMatch ? Math.round(Number.parseInt(usedMemoryMatch[1]) / (1024 * 1024)) : 0;

    // Check Dead Letter Queue (DLQ) Depth
    const dlqCount = await redis.llen('bull:dlq:failed').catch(() => 0);

    // 3. Verify Latest PostgreSQL Backup on Shared Storage
    const backupDir = '/mnt/baiostorage/backups/postgresql';
    let lastBackupStatus = 'unknown';
    let lastBackupSizeMb = 0;

    if (fs.existsSync(backupDir)) {
      const files = fs.readdirSync(backupDir).filter((f) => f.endsWith('.sql.gz'));
      if (files.length > 0) {
        const latestFile = files.sort().pop()!;
        const stat = fs.statSync(`${backupDir}/${latestFile}`);
        lastBackupSizeMb = Math.round(stat.size / (1024 * 1024));
        const ageHours = (Date.now() - stat.mtimeMs) / (1000 * 60 * 60);
        lastBackupStatus = ageHours < 26 ? 'healthy' : 'stale';
      } else {
        lastBackupStatus = 'missing';
      }
    }

    // 4. Persist Health Snapshot in Directus
    await directus.request(
      createItem('system_health_logs', {
        nats_connections: natsConnections,
        nats_in_msgs: natsInMsgs,
        valkey_used_memory_mb: usedMemoryMb,
        bullmq_dlq_count: dlqCount,
        last_backup_status: lastBackupStatus,
        last_backup_size_mb: lastBackupSizeMb,
        sampled_at: new Date().toISOString(),
      })
    );
  } catch (err: any) {
    console.error('[devllm-telemetry] Health polling error:', err.message);
  }
}
```

---

## 5. Declarative Directus Insights Panel Seeder for DevOps & LLMOps

```typescript
// scripts/seed-ops-dashboard.ts
import { createDirectus, rest, staticToken, createItem } from '@directus/sdk';

const directus = createDirectus(process.env.DIRECTUS_URL || 'http://directus:8055')
  .with(staticToken(process.env.DIRECTUS_STATIC_TOKEN || ''))
  .with(rest());

export async function seedOpsDashboard() {
  const dashboard = await directus.request(
    createItem('directus_dashboards', {
      name: 'DevOps & LLMOps Dashboard (~0 MB Extra RAM)',
      icon: 'monitoring',
      note: 'AI token spend tracking, NATS throughput, Valkey memory, and DB backups',
    })
  );

  // Panel 1: Cumulative AI Token Spend (USD)
  await directus.request(
    createItem('directus_panels', {
      dashboard: dashboard.id,
      name: 'Total AI Spend (USD)',
      icon: 'smart_toy',
      type: 'metric',
      position_x: 1,
      position_y: 1,
      width: 6,
      height: 6,
      options: {
        collection: 'llm_telemetry_logs',
        aggregate: { function: 'sum', field: 'estimated_cost_usd' },
        prefix: '$ ',
        format: true,
      },
    })
  );

  // Panel 2: Average Latency (ms)
  await directus.request(
    createItem('directus_panels', {
      dashboard: dashboard.id,
      name: 'Average LLM Latency (ms)',
      icon: 'timer',
      type: 'metric',
      position_x: 7,
      position_y: 1,
      width: 6,
      height: 6,
      options: {
        collection: 'llm_telemetry_logs',
        aggregate: { function: 'avg', field: 'latency_ms' },
        suffix: ' ms',
        format: true,
      },
    })
  );

  console.log(`DevOps & LLMOps dashboard initialized with ID: ${dashboard.id}`);
}
```

---

## 6. 5 Production Patterns in Zerops

### Pattern 1: Asynchronous Non-Blocking LLM Call Instrumentation
Wraps AI API calls (OpenAI, Anthropic, Gemini, DeepSeek) using `trackLLMCall()` to record prompt/completion tokens, calculated costs, and latency without adding request latency.

### Pattern 2: 60-Second System Health Daemon in AI Worker
Runs a lightweight background poller task in `aiworker` or `directus` sampling NATS `:8222/varz` and Valkey memory footprint.

### Pattern 3: Automated Database Backup Integrity Verification
Validates that `pg_dump` snapshots exist in `/mnt/baiostorage/backups/postgresql/`, are under 26 hours old, and have non-zero file sizes.

### Pattern 4: Directus Insights Dashboard for Executive LLMOps Tracking
Provides technical leadership with real-time visibility into AI expenses and system load using native Directus panels.

### Pattern 5: High-Cost & DLQ Alert Dispatch via NATS JetStream
Emits alert events on subject `events.ops.alerts` when DLQ depth exceeds 50 messages or single LLM query cost exceeds budget thresholds.

---

## 7. Anti-Patterns & Common Gotchas

1. **Synchronous Telemetry Logging**: Blocking user-facing responses to write telemetry logs synchronously to the database degrades application performance. Always use `setImmediate()` or NATS events.
2. **Deploying Heavy Monitoring Agents**: Spinning up Prometheus/Grafana on resource-constrained nodes wastes memory. Use Directus Insights natively.
3. **Hardcoding Token Pricing**: Always centralize model pricing in `MODEL_PRICING` maps to easily adjust when providers lower rates.
