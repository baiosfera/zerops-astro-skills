import { Worker, Job } from "bullmq";
import Redis from "ioredis";
import { UnifiedEmailDispatcher, UnifiedEmailPayload } from "./email_dispatcher";

const connection = new Redis(process.env.VALKEY_CONNECTION_STRING || "redis://valkey:6379", {
  maxRetriesPerRequest: null,
  enableReadyCheck: false
});

const dispatcher = new UnifiedEmailDispatcher();

export const emailWorker = new Worker(
  "emailDispatchQueue",
  async (job: Job<UnifiedEmailPayload>) => {
    console.log(`[Email Worker] Processing email dispatch to ${job.data.to?.join(", ")} (Job: ${job.id})`);
    try {
      return await dispatcher.dispatch(job.data);
    } catch (error: any) {
      if (error?.status === 429) {
        console.warn(`[Email Worker] Rate limit encountered. Pausing queue for 5000ms.`);
        await emailWorker.rateLimit(5000);
        throw Worker.RateLimitError();
      }
      throw error;
    }
  },
  {
    connection,
    concurrency: 5,
    limiter: {
      max: 10,       // Max 10 emails
      duration: 1000 // per 1000ms
    }
  }
);
