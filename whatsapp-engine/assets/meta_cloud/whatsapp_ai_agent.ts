import { generateText, tool } from "ai";
import { openai } from "@ai-sdk/openai";
import { z } from "zod";
import crypto from "node:crypto";
import { WhatsAppCloudClient } from "./whatsapp_cloud_client";

export async function processWhatsAppInbound({
  userMessage,
  userPhone,
  waClient
}: {
  userMessage: string;
  userPhone: string;
  waClient: WhatsAppCloudClient;
}) {
  const { text } = await generateText({
    model: openai("gpt-4o-mini"),
    system: `Eres la asesora comercial de Gentle AI en Colombia por WhatsApp. Resuelve dudas y genera links de pago Wompi seguros.`,
    prompt: userMessage,
    tools: {
      searchCatalog: tool({
        description: "Búsqueda vectorial en catálogo de productos",
        inputSchema: z.object({ query: z.string() }),
        execute: async ({ query }) => {
          return [{ title: "Consultoría Growth", price: "$250.000 COP", stock: 5 }];
        }
      }),
      createWompiPaymentLink: tool({
        description: "Genera enlace de pago Wompi firmado con SHA-256 para PSE, Nequi y Tarjetas",
        inputSchema: z.object({ sku: z.string(), amountCop: z.number() }),
        execute: async ({ sku, amountCop }) => {
          const reference = `WA-${sku}-${Date.now()}`;
          const amountInCents = amountCop * 100;
          const currency = "COP";
          const raw = `${reference}${amountInCents}${currency}${process.env.WOMPI_INTEGRITY_SECRET || "integrity_secret"}`;
          const signature = crypto.createHash("sha256").update(raw).digest("hex");
          const url = `https://checkout.wompi.co/p/?public-key=${process.env.WOMPI_PUBLIC_KEY}&currency=${currency}&amount-in-cents=${amountInCents}&reference=${reference}&signature:integrity=${signature}`;
          return { reference, amountFormatted: `$${amountCop.toLocaleString("es-CO")} COP`, paymentUrl: url };
        }
      })
    }
  });

  await waClient.sendText(userPhone, text);
  return { text };
}
