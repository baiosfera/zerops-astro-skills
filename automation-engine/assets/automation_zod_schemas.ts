import { z } from "zod";

export const EventEnvelopeSchema = z.object({
  id: z.string().uuid(),
  specversion: z.literal("1.0"),
  type: z.string().min(1),
  source: z.string().min(1),
  subject: z.string().min(1),
  time: z.string().datetime(),
  datacontenttype: z.literal("application/json").default("application/json"),
  data: z.record(z.unknown()),
  traceparent: z.string().optional()
});

export const StreamConfigSchema = z.object({
  name: z.string().regex(/^[a-zA-Z0-9_-]+$/),
  subjects: z.array(z.string()).min(1),
  retention: z.enum(["limits", "interest", "workqueue"]).default("limits"),
  max_bytes: z.number().int().default(1024 * 1024 * 1024),
  duplicate_window: z.number().int().default(120 * 1_000_000_000)
});

export const DlqEventSchema = z.object({
  deadLetterId: z.string().uuid(),
  queueName: z.string(),
  jobId: z.string(),
  jobName: z.string(),
  attemptsMade: z.number().int(),
  error: z.string(),
  failedAt: z.string().datetime(),
  payload: z.record(z.unknown())
});
