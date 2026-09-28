import { z } from "zod";

export const MessageKeySchema = z.object({
  remoteJid: z.string(),
  fromMe: z.boolean(),
  id: z.string(),
  participant: z.string().optional()
});

export const MessageUpsertDataSchema = z.object({
  key: MessageKeySchema,
  pushName: z.string().optional(),
  message: z.record(z.unknown()).optional(),
  messageType: z.string().optional(),
  messageTimestamp: z.union([z.number(), z.string()]).optional()
});

export const EvolutionWebhookEnvelopeSchema = z.object({
  event: z.string(),
  instance: z.string(),
  data: z.union([MessageUpsertDataSchema, z.record(z.unknown())]),
  date_time: z.string().optional(),
  sender: z.string().optional(),
  server_url: z.string().optional(),
  apikey: z.string().optional()
});

export const SendTextRequestSchema = z.object({
  number: z.string(),
  text: z.string().min(1),
  delay: z.number().optional().default(1200),
  linkPreview: z.boolean().optional().default(true)
});

export const SendAudioRequestSchema = z.object({
  number: z.string(),
  audio: z.string().url(),
  delay: z.number().optional().default(1500)
});
