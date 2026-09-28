# Automation Engine: Usage & Development Guide (v1.0)

> **SSoT Reference Document:** `.agents/skills/automation-engine/references/usage.md`  
> **Ámbito:** Broker de eventos NATS JetStream 2.12, Directus Flows 11+, CloudEvents 1.0 y BullMQ sobre Valkey 7.2 con Dead Letter Queue (DLQ).

---

## 1. NATS JetStream 2.12: Configuración de Streams & Consumo Pull

```typescript
import { connect, JetStreamClient, JetStreamManager, headers, StorageType, RetentionPolicy, AckPolicy } from "nats";

export class NatsEngine {
  private js!: JetStreamClient;
  private jsm!: JetStreamManager;

  async init(serverUrl = process.env.NATS_URL || "nats://127.0.0.1:4222") {
    const nc = await connect({ servers: serverUrl, name: "automation-engine" });
    this.js = nc.jetstream();
    this.jsm = await nc.jetstreamManager();
  }

  async setupCommerceStream() {
    await this.jsm.streams.add({
      name: "COMMERCE",
      subjects: ["orders.*", "payments.*", "fulfillment.*"],
      storage: StorageType.File,
      retention: RetentionPolicy.Limits,
      max_bytes: 1024 * 1024 * 1024, // 1GB
      duplicate_window: 120 * 1_000_000_000 // 2 min
    });
  }

  async publishCloudEvent(subject: string, event: { id: string; type: string; data: Record<string, unknown> }) {
    const h = headers();
    // Invariante: Deduplicación atómica en NATS con Nats-Msg-Id
    h.set("Nats-Msg-Id", event.id);

    const payload = {
      specversion: "1.0",
      id: event.id,
      type: event.type,
      source: "gentle.automation.engine",
      time: new Date().toISOString(),
      datacontenttype: "application/json",
      data: event.data
    };

    return await this.js.publish(subject, Buffer.from(JSON.stringify(payload)), { headers: h });
  }

  async startOrderConsumer(handler: (event: any) => Promise<void>) {
    const consumer = await this.js.consumers.get("COMMERCE", "order-processor").catch(async () => {
      return await this.jsm.consumers.add("COMMERCE", {
        durable_name: "order-processor",
        filter_subject: "orders.*",
        ack_policy: AckPolicy.Explicit,
        max_deliver: 5
      }).then(() => this.js.consumers.get("COMMERCE", "order-processor"));
    });

    return await consumer.consume({
      callback: async (msg) => {
        try {
          const event = JSON.parse(msg.data.toString());
          await handler(event);
          msg.ack();
        } catch (err) {
          msg.nak();
        }
      }
    });
  }
}
```

---

## 2. Directus Flows 11+: Transformación in-process a CloudEvents

```javascript
// Directus Flow: Operation "Run Script" (Sandbox JS)
module.exports = function (data) {
  const trigger = data.$trigger;
  const payload = trigger.payload;

  if (!payload.total_cop || payload.total_cop <= 0) {
    throw new Error("Transacción inválida: total_cop debe ser mayor a 0");
  }

  return {
    id: crypto.randomUUID(),
    specversion: "1.0",
    type: "commerce.order.created",
    source: "directus.flows.orders",
    subject: `orders.${trigger.keys?.[0] || 'new'}`,
    time: new Date().toISOString(),
    datacontenttype: "application/json",
    data: {
      orderId: trigger.keys?.[0],
      customerEmail: payload.customer_email,
      totalCop: payload.total_cop,
      paymentMethod: payload.payment_method || "WOMPI_PSE"
    }
  };
};
```

---

## 3. BullMQ Bridge con Valkey 7.2 & Dead Letter Queue (DLQ)

```typescript
import { Queue, Worker, Job } from "bullmq";
import Redis from "ioredis";

const connection = new Redis(process.env.VALKEY_CONNECTION_STRING || "redis://valkey:6379", {
  maxRetriesPerRequest: null,
  enableAutoPipelining: true
});

export const commerceQueue = new Queue("commerce-jobs", {
  connection,
  defaultJobOptions: {
    attempts: 5,
    backoff: { type: "exponential", delay: 1000 },
    removeOnComplete: { count: 1000 }
  }
});

export const commerceDlq = new Queue("commerce-dlq", { connection });

export const commerceWorker = new Worker(
  "commerce-jobs",
  async (job: Job) => {
    // Procesamiento de tarea pesada
    return { success: true };
  },
  { connection, concurrency: 10 }
);

commerceWorker.on("failed", async (job, error) => {
  if (!job) return;
  if (job.attemptsMade >= (job.opts.attempts || 1)) {
    console.error(`[DLQ ALERT] Trabajo ${job.id} agotó intentos. Moviendo a DLQ.`);
    await commerceDlq.add("dead-letter-item", {
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
