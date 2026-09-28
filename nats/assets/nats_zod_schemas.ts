import { z } from "zod";

export const NatsServerConfigSchema = z.object({
  host: z.string().default("0.0.0.0"),
  port: z.number().int().default(4222),
  httpPort: z.number().int().default(8222),
  clusterPort: z.number().int().optional().default(6222),
  serverName: z.string().min(1),
  jetstream: z.object({
    enabled: z.boolean().default(true),
    storeDir: z.string().default("/var/nats/storage"),
    maxMemoryStore: z.string().default("512MB"),
    maxFileStore: z.string().default("10GB")
  })
});

export const RpcEnvelopeSchema = z.object({
  id: z.string().uuid(),
  action: z.string().min(1),
  timestamp: z.string().datetime(),
  payload: z.record(z.unknown())
});

export const RpcResponseSchema = z.object({
  id: z.string().uuid(),
  success: z.boolean(),
  data: z.unknown().optional(),
  error: z.string().optional(),
  latencyMs: z.number()
});
