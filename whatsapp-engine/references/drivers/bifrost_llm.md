# Bifrost LLM Gateway & Brand SSoT Ingestion (v1.0)

## 1. Architectural Role
The WhatsApp bot acts as an empathetic, high-converting customer sales assistant for shoppers. To maintain sovereign execution and eliminate vendor lock-in, AI inference is decoupled from the WhatsApp transport layer:

1. **Brand SSoT Ingestion**:
   - The worker reads `/brand/fase0_system_prompt.md` (Brand DNA, tone, luxury demeanor, policies).
   - Dynamic product stock and pricing are injected into the system prompt from PostgreSQL / Directus.
2. **Bifrost Universal LLM Gateway**:
   - Endpoint: `http://bifrost:8000/v1/chat/completions` (OpenAI-compatible protocol).
   - Backed by FreeLLMAPI or configured model providers.
   - Streaming SSE responses can be parsed into paragraph segments before replying via WhatsApp.

---

## 2. Ingestion Implementation Pattern (TypeScript / Node.js or Bun)
```typescript
import fs from "node:fs";
import path from "node:path";

export function loadBrandSystemPrompt(brandPromptPath: string = "/var/www/evolution/brand/fase0_system_prompt.md"): string {
  if (fs.existsSync(brandPromptPath)) {
    return fs.readFileSync(brandPromptPath, "utf-8");
  }
  return "You are a professional e-commerce shopping assistant. Respond with helpfulness, elegance, and precision following store brand guidelines.";
}

export async function generateChatResponse(
  conversationHistory: Array<{ role: "system" | "user" | "assistant"; content: string }>,
  bifrostUrl: string = "http://bifrost:8000/v1"
): Promise<string> {
  const res = await fetch(`${bifrostUrl}/chat/completions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "gpt-4o-mini", // or specified gateway provider
      messages: conversationHistory,
      temperature: 0.7,
      max_tokens: 300,
    }),
  });

  const data = await res.json();
  return data.choices[0].message.content;
}
```
