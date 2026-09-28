import { EvolutionWebhookEnvelopeSchema } from "./evolution_zod_schemas";

export function handleEvolutionWebhook(body: unknown) {
  const result = EvolutionWebhookEnvelopeSchema.safeParse(body);
  if (!result.success) {
    return { valid: false, error: result.error.format() };
  }

  const envelope = result.data;
  if (envelope.event === "messages.upsert") {
    const data = envelope.data as any;
    const remoteJid = data.key?.remoteJid;
    const isFromMe = data.key?.fromMe;
    const text = data.message?.conversation || data.message?.extendedTextMessage?.text || "";

    // Detección de Opt-Out
    const isOptOut = /^(SALIR|CANCELAR|NO MAS|BAJA)$/i.test(text.trim());

    return {
      valid: true,
      event: "MESSAGES_UPSERT",
      remoteJid,
      phone: remoteJid ? remoteJid.replace("@s.whatsapp.net", "") : "",
      isFromMe,
      text,
      isOptOut
    };
  }

  return { valid: true, event: envelope.event };
}
