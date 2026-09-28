import { Queue, Worker, Job } from "bullmq";
import Redis from "ioredis";
import crypto from "node:crypto";

const connection = new Redis(process.env.VALKEY_CONNECTION_STRING || "redis://valkey:6379", {
  maxRetriesPerRequest: null,
  enableAutoPipelining: true
});

export const mainQueue = new Queue("main-events-queue", {
  connection,
  defaultJobOptions: {
    attempts: 5,
    backoff: { type: "exponential", delay: 1000 },
    removeOnComplete: { count: 1000 }
  }
});

export const deadLetterQueue = new Queue("dead-letter-queue", { connection });

export const eventWorker = new Worker(
  "main-events-queue",
  async (job: Job) => {
    console.log(`[Event Worker] Procesando trabajo ${job.name} (ID: ${job.id})`);
    return { success: true };
  },
  { connection, concurrency: 10 }
);

eventWorker.on("failed", async (job, error) => {
  if (!job) return;
  if (job.attemptsMade >= (job.opts.attempts || 1)) {
    console.error(`[DLQ ALERT] Trabajo ${job.id} falló definitivamente tras ${job.attemptsMade} intentos. Transfiriendo a DLQ.`);
    await deadLetterQueue.add("dlq-event", {
      deadLetterId: crypto.randomUUID(),
      queueName: job.queueName,
      jobId: job.id,
      jobName: job.name,
      attemptsMade: job.attemptsMade,
      error: error.message,
      failedAt: new Date().toISOString(),
      payload: job.data
    });
  }
});
