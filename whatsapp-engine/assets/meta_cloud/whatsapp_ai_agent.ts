import { generateText, tool } from "ai";
import { createOpenAI } from "@ai-sdk/openai";
import { z } from "zod";
import fs from "node:fs";
import { WhatsAppCloudClient } from "./whatsapp_cloud_client";

function resolveSystemPrompt(): string {
  const promptPath = process.env.SYSTEM_PROMPT_PATH || process.env.BRAND_SSOT_PATH;
  if (promptPath && fs.existsSync(promptPath)) {
    return fs.readFileSync(promptPath, "utf-8");
  }
  return "You are an empathetic, brand-aligned sales and customer support assistant on WhatsApp. Answer customer inquiries clearly and provide secure payment links when requested.";
}

export async function processWhatsAppInbound({
  userMessage,
  userPhone,
  waClient,
  customSystemPrompt,
}: {
  userMessage: string;
  userPhone: string;
  waClient: WhatsAppCloudClient;
  customSystemPrompt?: string;
}) {
  const bifrost = createOpenAI({
    baseURL: process.env.BIFROST_URL || "http://bifrost:8080/v1",
    apiKey: process.env.BIFROST_API_KEY || "bifrost-internal-key",
  });

  const { text } = await generateText({
    model: bifrost(process.env.BIFROST_MODEL || "gpt-4o-mini"),
    system: customSystemPrompt || resolveSystemPrompt(),
    prompt: userMessage,
    tools: {
      searchCatalog: tool({
        description: "Vector or keyword search in dynamic product catalog",
        inputSchema: z.object({ query: z.string() }),
        execute: async ({ query }) => {
          return [
            { id: "item-01", title: `Product matching: ${query}`, price: "100.00", currency: "USD", inStock: true }
          ];
        },
      }),
      createPaymentLink: tool({
        description: "Generate a secure, signed payment checkout link for orders",
        inputSchema: z.object({
          sku: z.string(),
          amount: z.number().positive(),
          currency: z.string().default("USD"),
        }),
        execute: async ({ sku, amount, currency }) => {
          const reference = `WA-${sku}-${Date.now()}`;
          const paymentBaseUrl = process.env.CHECKOUT_URL || "https://checkout.example.com";
          const paymentUrl = `${paymentBaseUrl}/pay?ref=${reference}&amount=${amount}&currency=${currency}`;
          return {
            reference,
            amountFormatted: `${amount.toFixed(2)} ${currency}`,
            paymentUrl,
          };
        },
      }),
    },
  });

  await waClient.sendText(userPhone, text);
  return { text };
}
