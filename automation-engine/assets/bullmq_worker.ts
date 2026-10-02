import { Queue, Worker, Job, type WorkerOptions } from "bullmq";
import Redis from "ioredis";
import crypto from "node:crypto";

export interface WorkerConfig {
  queueName: string;
  connectionString?: string;
  concurrency?: number;
  dlqQueueName?: string;
}

export function createAutomationWorker<TData = unknown, TResult = unknown>(
  config: WorkerConfig,
  processor: (job: Job<TData, TResult>) => Promise<TResult>,
  options?: Partial<WorkerOptions>
) {
  const connection = new Redis(config.connectionString || process.env.VALKEY_CONNECTION_STRING || "redis://valkey:6379", {
    maxRetriesPerRequest: null,
    enableAutoPipelining: true
  });

  const dlqQueue = new Queue(config.dlqQueueName || `${config.queueName}-dlq`, { connection });

  const worker = new Worker<TData, TResult>(
    config.queueName,
    async (job: Job<TData, TResult>) => {
      return await processor(job);
    },
    {
      connection,
      concurrency: config.concurrency || 10,
      ...options
    }
  );

  worker.on("failed", async (job, error) => {
    if (!job) return;
    const maxAttempts = job.opts.attempts || 1;
    if (job.attemptsMade >= maxAttempts) {
      console.error(`[DLQ Routing] Job ${job.id} on queue ${config.queueName} exhausted ${job.attemptsMade} attempts. Routing to DLQ.`);
      await dlqQueue.add("dead-letter-job", {
        deadLetterId: crypto.randomUUID(),
        queueName: config.queueName,
        jobId: job.id,
        jobName: job.name,
        attemptsMade: job.attemptsMade,
        error: error.message,
        failedAt: new Date().toISOString(),
        payload: job.data
      });
    }
  });

  return { worker, dlqQueue, connection };
}
