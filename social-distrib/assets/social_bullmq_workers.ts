import { Worker, Job } from "bullmq";
import Redis from "ioredis";
import { publishToInstagram, publishToX } from "./social_publishers_client";

const connection = new Redis(process.env.VALKEY_CONNECTION_STRING || "redis://valkey:6379", {
  maxRetriesPerRequest: null,
  enableReadyCheck: false
});

export const instagramWorker = new Worker(
  "social-instagram",
  async (job: Job) => {
    console.log(`[Instagram Worker] Procesando publicación job ${job.id}`);
    const mediaId = await publishToInstagram(job.data);
    return { success: true, mediaId, platform: "INSTAGRAM" };
  },
  {
    connection,
    concurrency: 2,
    limiter: {
      max: 20, // 20 posts por hora
      duration: 3600000
    }
  }
);

export const xWorker = new Worker(
  "social-x",
  async (job: Job) => {
    console.log(`[X Worker] Procesando tweet job ${job.id}`);
    const tweetId = await publishToX(job.data);
    return { success: true, tweetId, platform: "X" };
  },
  {
    connection,
    concurrency: 5,
    limiter: {
      max: 30, // 30 posts por hora
      duration: 3600000
    }
  }
);
