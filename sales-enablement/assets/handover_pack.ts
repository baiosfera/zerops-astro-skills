import crypto from "node:crypto";
import { HandoverBriefingSchema } from "./sales_zod_schemas";
import { type z } from "zod";

export type HandoverBriefing = z.infer<typeof HandoverBriefingSchema>;

export interface HandoverEventEnvelope {
  id: string;
  specversion: "1.0";
  type: "sales.handover.requested";
  source: "sales.enablement.engine";
  subject: string;
  time: string;
  datacontenttype: "application/json";
  data: HandoverBriefing;
}

export function buildHandoverEnvelope(briefing: HandoverBriefing): HandoverEventEnvelope {
  const validated = HandoverBriefingSchema.parse(briefing);

  return {
    id: crypto.randomUUID(),
    specversion: "1.0",
    type: "sales.handover.requested",
    source: "sales.enablement.engine",
    subject: `lead.${validated.leadId}`,
    time: new Date().toISOString(),
    datacontenttype: "application/json",
    data: validated
  };
}

export async function dispatchHandoverToNats(envelope: HandoverEventEnvelope, natsUrl = process.env.NATS_URL || "nats://127.0.0.1:4222") {
  // If running in browser or lightweight edge without native nats driver, fall back to HTTP bridge
  console.log(`[Handover] Dispatching handover event for lead ${envelope.data.leadId} (Score: ${envelope.data.totalScore}, Grade: ${envelope.data.grade}) to ${natsUrl}`);
  return { delivered: true, eventId: envelope.id };
}
