# WhatsApp Cloud API: Usage & Development Guide (v1.0)

> **SSoT Reference Document:** `.agents/skills/whatsapp-cloud/references/usage.md`  
> **Ámbito:** Integración oficial con Meta WhatsApp Cloud API v21.0, verificación HMAC-SHA256, agente conversacional con Vercel AI SDK 5 y búsqueda RAG en PostgreSQL 18 con pgvector.

---

## 1. Verificación de Webhooks: GET Challenge & POST HMAC-SHA256

### A. Endpoint GET (Challenge de Suscripción):
```typescript
export function handleWebhookChallenge(query: {
  "hub.mode"?: string;
  "hub.verify_token"?: string;
  "hub.challenge"?: string;
}, localVerifyToken: string): { status: number; body: string } {
  if (query["hub.mode"] === "subscribe" && query["hub.verify_token"] === localVerifyToken) {
    return { status: 200, body: query["hub.challenge"] || "" };
  }
  return { status: 403, body: "Forbidden" };
}
```

### B. Validación Criptográfica POST (X-Hub-Signature-256):
```typescript
import crypto from "node:crypto";

export function verifyMetaSignature(
  rawBody: Buffer | string,
  signatureHeader: string | null,
  appSecret: string
): boolean {
  if (!signatureHeader || !signatureHeader.startsWith("sha256=")) return false;

  const expectedSignature = signatureHeader.substring(7);
  const calculatedSignature = crypto
    .createHmac("sha256", appSecret)
    .update(rawBody)
    .digest("hex");

  const expectedBuffer = Buffer.from(expectedSignature, "hex");
  const calculatedBuffer = Buffer.from(calculatedSignature, "hex");

  if (expectedBuffer.length !== calculatedBuffer.length) return false;
  return crypto.timingSafeEqual(expectedBuffer, calculatedBuffer);
}
```

---

## 2. Cliente TypeScript Oficial Meta WhatsApp Cloud API (v21.0)

```typescript
export class WhatsAppCloudClient {
  private baseUrl = "https://graph.facebook.com/v21.0";

  constructor(
    private phoneNumberId: string,
    private accessToken: string
  ) {}

  private async post(payload: unknown) {
    const res = await fetch(`${this.baseUrl}/${this.phoneNumberId}/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${this.accessToken}`
      },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`[WhatsApp Cloud API Error] HTTP ${res.status}: ${err}`);
    }
    return (await res.json()) as { messages: [{ id: string }] };
  }

  async sendText(to: string, text: string) {
    return this.post({
      messaging_product: "whatsapp",
      recipient_type: "individual",
      to,
      type: "text",
      text: { body: text }
    });
  }

  async sendInteractiveButtons(to: string, bodyText: string, buttons: Array<{ id: string; title: string }>) {
    return this.post({
      messaging_product: "whatsapp",
      recipient_type: "individual",
      to,
      type: "interactive",
      interactive: {
        type: "button",
        body: { text: bodyText },
        action: {
          buttons: buttons.map((b) => ({ type: "reply", reply: { id: b.id, title: b.title } }))
        }
      }
    });
  }

  async sendInteractiveList(to: string, bodyText: string, buttonText: string, sections: Array<{ title: string; rows: Array<{ id: string; title: string; description?: string }> }>) {
    return this.post({
      messaging_product: "whatsapp",
      recipient_type: "individual",
      to,
      type: "interactive",
      interactive: {
        type: "list",
        body: { text: bodyText },
        action: { button: buttonText, sections }
      }
    });
  }

  async sendTemplate(to: string, templateName: string, languageCode: string, parameters: Record<string, string>) {
    return this.post({
      messaging_product: "whatsapp",
      recipient_type: "individual",
      to,
      type: "template",
      template: {
        name: templateName,
        language: { code: languageCode },
        components: [
          {
            type: "body",
            parameters: Object.entries(parameters).map(([k, v]) => ({ type: "text", parameter_name: k, text: v }))
          }
        ]
      }
    });
  }
}
```

---

## 3. Base de Datos RAG en PostgreSQL 18 con pgvector HNSW

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS product_knowledge (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  sku TEXT UNIQUE,
  category TEXT NOT NULL,
  price_cop NUMERIC(12, 2) NOT NULL,
  stock INT NOT NULL DEFAULT 0,
  content TEXT NOT NULL,
  embedding vector(1536) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_product_knowledge_hnsw 
ON product_knowledge 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 128);
```

---

## 4. Agente Conversacional AI-First con Vercel AI SDK 5

```typescript
import { generateText, tool } from "ai";
import { openai } from "@ai-sdk/openai";
import { z } from "zod";
import crypto from "node:crypto";

export async function runWhatsAppAIAgent(userMessage: string, userPhone: string) {
  return await generateText({
    model: openai("gpt-4o-mini"),
    system: `Eres la asesora comercial de Gentle AI en Colombia. Resuelve dudas de productos, rastrea pedidos y genera enlaces de pago Wompi seguros.`,
    prompt: userMessage,
    tools: {
      searchCatalog: tool({
        description: "Búsqueda vectorial en catálogo",
        inputSchema: z.object({ query: z.string() }),
        execute: async ({ query }) => {
          return [{ title: "Producto Ejemplo", price: "$150.000 COP", stock: 10 }];
        }
      }),
      createWompiPaymentLink: tool({
        description: "Genera enlace de pago firmado de Wompi para PSE y Nequi",
        inputSchema: z.object({ sku: z.string(), amountCop: z.number() }),
        execute: async ({ sku, amountCop }) => {
          const reference = `WA-${sku}-${Date.now()}`;
          const amountInCents = amountCop * 100;
          const currency = "COP";
          const raw = `${reference}${amountInCents}${currency}${process.env.WOMPI_INTEGRITY_SECRET}`;
          const signature = crypto.createHash("sha256").update(raw).digest("hex");
          const url = `https://checkout.wompi.co/p/?public-key=${process.env.WOMPI_PUBLIC_KEY}&currency=${currency}&amount-in-cents=${amountInCents}&reference=${reference}&signature:integrity=${signature}`;
          return { reference, amountFormatted: `$${amountCop.toLocaleString("es-CO")} COP`, paymentUrl: url };
        }
      })
    }
  });
}
```
