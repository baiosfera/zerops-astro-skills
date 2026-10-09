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

---

## 3. Audio & Voice Note Transcription (Whisper Invariant)
Voice notes (`audioMessage`) received through Evolution Go or WhatsApp Cloud API must be transcribed into text before routing to the conversational model:
- **Endpoint**: `http://bifrost:8080/v1/audio/transcriptions`
- **Headers**: `Authorization: Bearer <virtual_key>`
- **Payload**: `multipart/form-data` with `file: <buffer/stream>` and `model: "whisper-1"`.
- **Empathetic Fallback**: If audio transcription fails or cannot be decoded, the bot must reply with genuine brand empathy (e.g., apologizing and asking the customer to clarify in text or resend) rather than dropping the message silently.

---

## 4. Multi-Identifier Sliding Human Takeover (2h Lock)
When a human operator replies directly from the phone (`fromMe: true`):
1. **Chat Identifier Isolation**: The system must extract the customer's remote chat identifier from `key.remoteJid` or `info.Chat`. It must NEVER lock the operator's sender LID (`info.Sender`).
2. **Dual-Key Valkey Locking**: Lock both the phone number and LID representation in Valkey (`wa:human_takeover:${id}`) with a 2-hour TTL (7200s).
3. **Operator Control Commands**:
   - `#bot`: Clears the takeover lock immediately, returning control to the AI.
   - `#mute`: Silences the bot for 24 hours (86400s) for extended human negotiations.

---

## 5. Inbound Quoted Context & Route Whitelist Grounding
- **Quoted Messages**: When incoming messages contain `contextInfo.quotedMessage`, parse the quoted content and prepend it to the user prompt (`[Mensaje citado: "..."]\n<texto>`). This ensures the LLM retains full conversational grounding when customers reply to specific earlier messages.
- **Strict Route Whitelist (Zero 404s)**: All recommended URLs must be strictly grounded in the verified catalog of Astro routes (e.g., `/eventos/...`, `/dashboard`, etc.). Hallucinating unverified routes is strictly prohibited.
- **Ambassador Loop**: The 3-referral reward loop is offered only at moments of high customer delight, protected by a 7-day Valkey cooldown (`wa:affiliate_pitched:${phone}`).
