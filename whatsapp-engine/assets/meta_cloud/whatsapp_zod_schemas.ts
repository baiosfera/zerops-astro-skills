import { z } from "zod";

export const WebhookVerificationQuerySchema = z.object({
  "hub.mode": z.literal("subscribe"),
  "hub.verify_token": z.string().min(1),
  "hub.challenge": z.string().min(1)
});

export const WhatsAppInboundMessageSchema = z.object({
  from: z.string(),
  id: z.string(),
  timestamp: z.string(),
  type: z.enum(["text", "interactive", "image", "document", "audio", "video", "location"]),
  text: z.object({ body: z.string() }).optional(),
  interactive: z
    .object({
      type: z.enum(["button_reply", "list_reply"]),
      button_reply: z.object({ id: z.string(), title: z.string() }).optional(),
      list_reply: z.object({ id: z.string(), title: z.string() }).optional()
    })
    .optional()
});

export const WhatsAppWebhookPayloadSchema = z.object({
  object: z.literal("whatsapp_business_account"),
  entry: z.array(
    z.object({
      id: z.string(),
      changes: z.array(
        z.object({
          field: z.literal("messages"),
          value: z.object({
            messaging_product: z.literal("whatsapp"),
            metadata: z.object({
              display_phone_number: z.string(),
              phone_number_id: z.string()
            }),
            contacts: z.array(z.object({ profile: z.object({ name: z.string() }), wa_id: z.string() })).optional(),
            messages: z.array(WhatsAppInboundMessageSchema).optional()
          })
        })
      )
    })
  )
});

export const ConversationalSessionSchema = z.object({
  waId: z.string(),
  customerName: z.string().default("Cliente"),
  currentStep: z.enum(["idle", "browsing_catalog", "tracking_order", "checkout_pending", "escalated_human"]),
  lastInteractionAt: z.number(),
  messages: z.array(
    z.object({
      role: z.enum(["user", "assistant", "system"]),
      content: z.string(),
      timestamp: z.number()
    })
  ).max(20)
});
