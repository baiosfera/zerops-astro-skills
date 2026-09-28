import { z } from "zod";

export const SendEmailPayloadSchema = z.object({
  from: z.string().min(3),
  to: z.array(z.string().email()).min(1).max(50),
  replyTo: z.string().email().optional(),
  subject: z.string().min(1).max(200),
  templateId: z.enum(["welcome_latam", "cart_recovery", "flash_sale", "reengagement"]),
  props: z.record(z.unknown()),
  unsubscribeUrl: z.string().url(),
  campaignId: z.string().uuid().optional(),
  tags: z.record(z.string()).default({})
});

export const EmailWebhookEventSchema = z.object({
  type: z.enum([
    "email.sent",
    "email.delivered",
    "email.delivery_delayed",
    "email.complained",
    "email.bounced",
    "email.opened",
    "email.clicked"
  ]),
  created_at: z.string().datetime(),
  data: z.object({
    email_id: z.string(),
    from: z.string(),
    to: z.array(z.string()),
    subject: z.string(),
    message_id: z.string().optional()
  })
});

export type SendEmailPayload = z.infer<typeof SendEmailPayloadSchema>;
export type EmailWebhookEvent = z.infer<typeof EmailWebhookEventSchema>;
