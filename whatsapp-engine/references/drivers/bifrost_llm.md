# Bifrost LLM Gateway & Brand SSoT Ingestion (v2.0)

## 1. Architectural Role
The WhatsApp bot acts as an empathetic, high-converting customer sales assistant. To maintain sovereign execution and eliminate vendor lock-in, AI inference is completely decoupled from the WhatsApp transport layer:

1. **Brand SSoT Dynamic Ingestion**:
   - The worker dynamically resolves system persona, tone, and policies from `$SYSTEM_PROMPT_PATH` or `$BRAND_SSOT_PATH`.
   - Dynamic product stock, customer context, and catalog pricing are injected into the system prompt from PostgreSQL or headless CMS.
2. **Bifrost Universal LLM Gateway**:
   - Endpoint: `http://bifrost:8080/v1/chat/completions` (OpenAI-compatible protocol).
   - Port 8080 is the authoritative Zerops internal network gateway port.
   - Streaming SSE or batch responses can be parsed into paragraph segments before replying via WhatsApp.

---

## 2. Ingestion Implementation Pattern (TypeScript / Bun / Node.js)
```typescript
import fs from "node:fs";
import path from "node:path";

export function loadBrandSystemPrompt(
  brandPromptPath: string = process.env.SYSTEM_PROMPT_PATH || process.env.BRAND_SSOT_PATH || "/var/www/brand/system_prompt.md"
): string {
  if (fs.existsSync(brandPromptPath)) {
    return fs.readFileSync(brandPromptPath, "utf-8");
  }
  return "You are a professional customer assistant. Respond with helpfulness, elegance, and precision following brand guidelines.";
}

export async function generateChatResponse(
  conversationHistory: Array<{ role: "system" | "user" | "assistant"; content: string }>,
  bifrostUrl: string = process.env.BIFROST_URL || "http://bifrost:8080/v1"
): Promise<string> {
  const res = await fetch(`${bifrostUrl}/chat/completions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: process.env.BIFROST_MODEL || "gpt-4o-mini",
      messages: conversationHistory,
      temperature: 0.7,
      max_tokens: 400,
    }),
  });

  if (!res.ok) {
    throw new Error(`Bifrost LLM gateway error: ${res.status} ${await res.text()}`);
  }

  const data = await res.json();
  return data.choices[0]?.message?.content || "";
}
```
