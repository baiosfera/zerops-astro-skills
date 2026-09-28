import { Worker, Job } from "bullmq";
import Redis from "ioredis";
import { sendResendEmail } from "./email_dispatcher";

const connection = new Redis(process.env.VALKEY_CONNECTION_STRING || "redis://valkey:6379", {
  maxRetriesPerRequest: null,
  enableReadyCheck: false
});

export const emailWorker = new Worker(
  "emailDispatchQueue",
  async (job: Job) => {
    console.log(`[Email Worker] Procesando envío para ${job.data.to}`);
    try {
      return await sendResendEmail(job.data);
    } catch (error: any) {
      if (error?.status === 429) {
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
      max: 10,       // 10 emails máximo
      duration: 1000 // por cada 1 segundo (1000ms)
    }
  }
);
