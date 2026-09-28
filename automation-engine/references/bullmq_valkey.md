# Canonical BullMQ on Valkey 7.2 Configuration (v2.0)

## 1. Architectural Motivation
HTTP requests from payment webhooks and checkout endpoints must never block on heavy downstream operations (ERPNext Sales Invoice posting, PDF generation, email/WhatsApp dispatch). BullMQ provides persistent, Redis-compatible job queuing over Valkey with retry backoff and dead-letter queues.

---

## 2. Worker Implementation Pattern (TypeScript / Node.js or Bun)
```typescript
import { Queue, Worker, Job } from "bullmq";
import IORedis from "ioredis";

// Valkey connection parsed from Zerops environment
const connection = new IORedis(process.env.cache_connectionString || "redis://valkey:6379", {
  maxRetriesPerRequest: null,
  enableReadyCheck: false,
});

export const orderQueue = new Queue("orders:post-settlement", { connection });

export const orderWorker = new Worker(
  "orders:post-settlement",
  async (job: Job) => {
    const { orderId, transactionId } = job.data;

    // 1. Post to ERPNext (Frappe Cloud)
    await postSalesInvoiceToERPNext(orderId);

    // 2. Dispatch Confirmation Email via Listmonk
    await dispatchReceiptEmail(orderId);

    // 3. Dispatch WhatsApp via Evolution Go
    await dispatchWhatsAppConfirmation(orderId);
  },
  {
    connection,
    concurrency: 5,
    limiter: { max: 20, duration: 1000 },
  }
);

orderWorker.on("failed", (job, err) => {
  console.error(`Job ${job?.id} failed with error:`, err.message);
});
```

---

## 3. Exponential Retry Backoff & Dead Letter Queue (DLQ)
```typescript
await orderQueue.add(
  "process-order",
  { orderId: "ORDER-9912", transactionId: "tx_123" },
  {
    attempts: 3,
    backoff: {
      type: "exponential",
      delay: 2000, // 2s, 4s, 8s
    },
    removeOnComplete: 1000,
    removeOnFail: false, // Preserved for audit inspection
  }
);
```
