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

export function classifyMessageIntent(text: string): "production" | "free" {
  const normalized = text.toLowerCase();
  const salesTriggers = [
    "precio", "cuanto", "comprar", "ticket", "entrada", "reserva", "pago",
    "cuenta", "link", "transferencia", "evento", "boleta", "afiliado",
    "embajador", "reclamo", "humano", "asesor"
  ];
  return salesTriggers.some(trigger => normalized.includes(trigger)) ? "production" : "free";
}

export function calculateTypingPacing(replyLength: number): number {
  // Pacing: 1500ms floor, ~20ms per character, capped at 3000ms
  return Math.min(3000, Math.max(1500, 1500 + replyLength * 15));
}

export async function generateChatResponse(
  conversationHistory: Array<{ role: "system" | "user" | "assistant"; content: string }>,
  options?: {
    bifrostUrl?: string;
    tier?: "production" | "free";
    headers?: Record<string, string>;
  }
): Promise<string> {
  const bifrostUrl = options?.bifrostUrl || process.env.BIFROST_URL || "http://bifrost:8080/v1";
  const tier = options?.tier || "production";
  const isPro = tier === "production";

  const res = await fetch(`${bifrostUrl}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${process.env.BIFROST_VIRTUAL_KEY || "vk-evolution-wa"}`,
      "x-tier": tier,
      ...(options?.headers || {})
    },
    body: JSON.stringify({
      model: isPro ? "deepseek-chat" : (process.env.BIFROST_MODEL || "auto"),
      messages: conversationHistory,
      temperature: 0.1,
      max_tokens: 600,
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

---

## 6. Deterministic Tool Calling (Function Calling) & Anti-Hallucination
Rather than stuffing volatile business catalogs (event dates, ticket pricing, quotas) into static prompts, the worker provides OpenAI-compatible function definitions to Bifrost:

```typescript
export const BOT_TOOLS = [
  {
    type: "function",
    function: {
      name: "get_active_events",
      description: "Query live upcoming events, dates, venues, and ticket pricing in Bogotá.",
      parameters: {
        type: "object",
        properties: {
          limit: { type: "integer", default: 5 }
        }
      }
    }
  },
  {
    type: "function",
    function: {
      name: "lookup_ticket_status",
      description: "Check if a customer has paid tickets or active reservations using their phone number.",
      parameters: {
        type: "object",
        properties: {
          phone: { type: "string", description: "E.164 normalized phone number" }
        },
        "required": ["phone"]
      }
    }
  },
  {
    type: "function",
    function: {
      name: "get_affiliate_stats",
      description: "Retrieve ambassador stats, paid referrals, and free tickets earned.",
      parameters: {
        type: "object",
        properties: {
          phone: { type: "string" }
        },
        "required": ["phone"]
      }
    }
  },
  {
    type: "function",
    function: {
      name: "register_community_lead",
      description: "Register a new attendee or member in PostgreSQL with role and city.",
      parameters: {
        type: "object",
        properties: {
          alias_nombre: { type: "string" },
          rol: { type: "string", enum: ["hombre_solo", "mujer_sola", "pareja", "otro"] },
          ciudad: { type: "string", default: "Bogotá" }
        },
        "required": ["alias_nombre", "rol"]
      }
    }
  }
];
```

### pgvector vs Deterministic SQL Benchmark:
- For small-to-medium catalogs (<100 entities/events), **pgvector is an over-engineered anti-pattern**:
  - Vector similarity search is probabilistic and risks matching expired past events with upcoming dates due to semantic similarity.
  - Relational SQL with B-Tree indexes (`WHERE fecha >= CURRENT_DATE`) executes in **<0.5ms** at zero token cost.
  - Native PostgreSQL 18 Full-Text Search (`tsvector`/`tsquery` with GIN indexing) provides deterministic lexical search in **<2ms** without external embeddings.

---

## 7. Hybrid Conversational Memory Architecture (Anti-Amnesia)
To eliminate amnesia caused by naive `ltrim(0, 9)` lists, use a 3-tier memory engine:
1. **Tier 1 (Valkey 7.2 Hot Sliding Buffer)**: Stores the last 6 raw turns in `wa:session:turns:${phone}` with <0.5ms latency.
2. **Tier 2 (Incremental Summarizer via Bifrost FreeLLMAPI)**: When turns exceed 6, a fast summary model compresses older turns into an 80-word summary, trims Valkey, and updates the profile.
3. **Tier 3 (PostgreSQL 18 Profile Storage)**: Persists `leads.metadata->'chat_summary'` and auditable history in `chat_messages`. Context overhead stays fixed at ~500–700 tokens forever.

---

## 8. High-Performance Groq Whisper Large-v3-Turbo Pipeline (<350ms)
Transcribe voice notes with Groq Whisper Large v3 Turbo (216x real-time speed factor, $0.04/hr of audio):
```typescript
const formData = new FormData();
formData.append("file", new Blob([audioBuffer], { type: "audio/ogg" }), "voice.ogg");
formData.append("model", "whisper-large-v3-turbo");
formData.append("language", "es");
formData.append("response_format", "json");

const res = await fetch("https://api.groq.com/openai/v1/audio/transcriptions", {
  method: "POST",
  headers: { Authorization: `Bearer ${process.env.GROQ_API_KEY}` },
  body: formData
});
const { text } = await res.json();
```
Prepends `[Nota de voz transcrita]: "${text}"` to user messages for conversational empathy.

---

## 9. Real-Time SSoT Ingestion, Dynamic Role/Gender Adaptation & SSoT Override Rule
To guarantee that the conversational AI reflects database changes instantaneously without being anchored to stale conversation turns:
1. **Dynamic Demographic Attributes**: The worker extracts `alias`, `email`, `role`, `city`, and `affiliateAlias` from PostgreSQL in real-time.
2. **Explicit Role/Gender Instructions**:
   - `hombre_solo`: Single male profile. Addressed in masculine singular ("Embajador", "bienvenido", "tú").
   - `mujer_sola`: Single female profile. Addressed in feminine singular ("Embajadora", "bienvenida", "tú").
   - `pareja`: Couple account. Addressed strictly as a couple in plural ("ustedes", "pareja", "chicos", "ambos", "como pareja", "Embajadores"). Never address as a single woman or man.
   - `otro` / null: Neutral community profile.
3. **Real-Time SSoT Override Rule (SSoT > History)**:
   - System prompt instructs the LLM that the customer ficha is the ground truth in the current millisecond.
   - Older chat turns in Valkey that used outdated names or roles must be explicitly ignored.
   - If the customer asks if their updated name or role is recognized, the bot immediately confirms and validates the new name/role without claiming sync delays.

