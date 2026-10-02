# Automation Engine: Usage & Architecture Guide (v2.0)

> **SSoT Reference Document:** `.agents/skills/automation-engine/references/usage.md`  
> **Scope:** NATS JetStream 2.12 Message Broker, Core NATS Request-Reply (<0.3ms P99), CNCF CloudEvents v1.0, BullMQ 6.x on Valkey 7.2 with Dead Letter Queue (DLQ), and Tri-State Circuit Breakers.

---

## 1. NATS JetStream 2.12: Stream Configuration, Pull Consumer Pools & Core RPC {#1-nats}

NATS Server 2.12 enforces the Strict JetStream API, preventing extraneous schema fields and providing durable pull consumers with queue groups for horizontally scalable worker pools:

```typescript
import { connect, JetStreamClient, JetStreamManager, headers, StorageType, RetentionPolicy, AckPolicy } from "nats";

export class NatsEventMesh {
  private js!: JetStreamClient;
  private jsm!: JetStreamManager;

  async init(serverUrl = process.env.NATS_URL || "nats://127.0.0.1:4222") {
    const nc = await connect({ servers: serverUrl, name: "automation-engine" });
    this.js = nc.jetstream();
    this.jsm = await nc.jetstreamManager();
    return nc;
  }

  async declareStream(streamName: string, subjects: string[]) {
    await this.jsm.streams.add({
      name: streamName,
      subjects: subjects,
      storage: StorageType.File,
      retention: RetentionPolicy.Limits,
      max_bytes: 1024 * 1024 * 1024, // 1GB
      duplicate_window: 120 * 1_000_000_000 // 2 minutes deduplication window
    });
  }

  async publishCloudEvent(subject: string, event: {
    id: string;
    type: string;
    source: string;
    data: Record<string, unknown>;
    traceparent?: string;
  }) {
    const h = headers();
    // Atomic deduplication via Nats-Msg-Id header
    h.set("Nats-Msg-Id", event.id);
    if (event.traceparent) {
      h.set("traceparent", event.traceparent);
    }

    const payload = {
      specversion: "1.0",
      id: event.id,
      type: event.type,
      source: event.source,
      time: new Date().toISOString(),
      datacontenttype: "application/json",
      data: event.data
    };

    return await this.js.publish(subject, Buffer.from(JSON.stringify(payload)), { headers: h });
  }

  async startDurablePullConsumer(stream: string, consumerName: string, filterSubject: string, handler: (event: any) => Promise<void>) {
    const consumer = await this.js.consumers.get(stream, consumerName).catch(async () => {
      return await this.jsm.consumers.add(stream, {
        durable_name: consumerName,
        filter_subject: filterSubject,
        ack_policy: AckPolicy.Explicit,
        max_deliver: 5
      }).then(() => this.js.consumers.get(stream, consumerName));
    });

    return await consumer.consume({
      callback: async (msg) => {
        try {
          const event = JSON.parse(msg.data.toString());
          await handler(event);
          msg.ack();
        } catch (err) {
          // If max deliveries reached, terminate poison pill to route to advisory stream
          if (msg.info.deliveryCount >= 5) {
            msg.term();
          } else {
            msg.nak();
          }
        }
      }
    });
  }
}
```

---

## 2. BullMQ on Valkey 7.2: Deduplication, Debouncing & Dead Letter Queue (DLQ) {#2-bullmq}

BullMQ 6.x running on Valkey 7.2 provides high-throughput background processing with exponential backoff and DLQ routing:

```typescript
import { Queue, Worker, Job } from "bullmq";
import Redis from "ioredis";

const connection = new Redis(process.env.VALKEY_URL || "redis://valkey:6379", {
  maxRetriesPerRequest: null,
  enableAutoPipelining: true
});

export const taskQueue = new Queue("background-tasks", {
  connection,
  defaultJobOptions: {
    attempts: 5,
    backoff: { type: "exponential", delay: 1000 },
    removeOnComplete: { count: 1000 }
  }
});

export const deadLetterQueue = new Queue("tasks-dlq", { connection });

export const taskWorker = new Worker(
  "background-tasks",
  async (job: Job) => {
    // Process heavy asynchronous workload
    return { success: true, processedAt: new Date().toISOString() };
  },
  { connection, concurrency: 10 }
);

taskWorker.on("failed", async (job, error) => {
  if (!job) return;
  if (job.attemptsMade >= (job.opts.attempts || 1)) {
    console.error(`[DLQ EXHAUSTION] Job ${job.id} failed after ${job.attemptsMade} attempts. Routing to DLQ.`);
    await deadLetterQueue.add("dead-letter-task", {
      jobId: job.id,
      jobName: job.name,
      attemptsMade: job.attemptsMade,
      error: error.message,
      payload: job.data,
      failedAt: new Date().toISOString()
    });
  }
});
```

---

## 3. CNCF CloudEvents v1.0 Transformation Pipeline

Agnostic transformation pipeline converting any incoming trigger or mutation payload into a strictly compliant CloudEvents v1.0 structure:

```typescript
export function toCloudEvent<T extends Record<string, unknown>>(
  eventType: string,
  source: string,
  data: T,
  subject?: string
) {
  return {
    specversion: "1.0" as const,
    id: crypto.randomUUID(),
    type: eventType,
    source: source,
    subject: subject || undefined,
    time: new Date().toISOString(),
    datacontenttype: "application/json",
    data: data
  };
}
```

---

## 4. Standalone Tri-State Circuit Breaker Integration

To prevent cascade failures across downstreams:

```typescript
import { CircuitBreaker } from "../assets/circuit_breaker";

const externalApiBreaker = new CircuitBreaker({
  failureThreshold: 5,
  cooldownPeriodMs: 30000,
  halfOpenMaxSuccesses: 2
});

export async function resilientDispatch(fn: () => Promise<any>) {
  return await externalApiBreaker.execute(fn);
}
```
