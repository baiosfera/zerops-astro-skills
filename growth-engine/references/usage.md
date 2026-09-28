# Sovereign Growth Engine: Brand Ingestion, Copywriting & Cart Recovery (v1.0)

## 1. Brand SSoT Ingestion & Voice Calibration
All commercial copy, ad variations, and cart recovery sequences MUST inherit the brand identity directly from the local single-tenant mount:
- **Brand Identity SSoT**: `/var/www/astro/brand/fase0_system_prompt.md`
- **Design Tokens & Archetype**: `/var/www/astro/brand/brandbook.json`
- **Rejection Tropes**: Ingest `<lo_que_la_marca_rechaza>` to guarantee zero generic buzzwords (e.g., "la mejor calidad", "oferta imperdible").

```typescript
import fs from "node:fs";

export function getBrandVoiceContext(brandPath = "/var/www/astro/brand"): { prompt: string; archetype: string } {
  const promptFile = `${brandPath}/fase0_system_prompt.md`;
  const brandbookFile = `${brandPath}/brandbook.json`;

  const prompt = fs.existsSync(promptFile) ? fs.readFileSync(promptFile, "utf-8") : "You are a luxury fashion consultant.";
  let archetype = "The Ruler / Quiet Luxury";
  if (fs.existsSync(brandbookFile)) {
    try {
      const data = JSON.parse(fs.readFileSync(brandbookFile, "utf-8"));
      archetype = data?.brand?.archetype || archetype;
    } catch {}
  }
  return { prompt, archetype };
}
```

---

## 2. Bifrost LLM Gateway Pipeline
Copy generation and recovery messaging route through the local Bifrost gateway:
- **Endpoint**: `http://bifrost:8000/v1/chat/completions`
- **Model Provider**: FreeLLMAPI / OpenAI compatible
- **Prompt Structure**:
  ```json
  {
    "messages": [
      { "role": "system", "content": "${brandVoice.prompt}\nArchetype: ${brandVoice.archetype}" },
      { "role": "user", "content": "Compose a warm, non-pushy abandoned cart recovery message for a shopper who left the enterizo velvet in size M." }
    ],
    "temperature": 0.65
  }
  ```

---

## 3. Abandoned Cart Recovery Pipeline
1. **Blur Capture**: When a customer types their email or phone in the checkout form and clicks outside, an Astro Action sends an asynchronous beacon to `/api/cart/capture-lead`.
2. **Valkey Staging**:
   - `HSET cart:abandoned:${leadId} phone "${phone}" email "${email}" cart "${cartJson}" timestamp "${Date.now()}"`
   - `EXPIRE cart:abandoned:${leadId} 86400`
3. **BullMQ Delayed Worker (15 minutes)**:
   - Worker checks if order was completed (`valkey.get('status:payment:' + leadId)`).
   - If not completed, calls Bifrost with Brand System Prompt to synthesize a bespoke WhatsApp/email note.
   - Publishes to NATS `events.whatsapp.outgoing` or `events.email.dispatch`.

---

## 4. 2026 Anti-SPAM Email Standards
- **Subject Length**: Strictly 30 to 50 characters (4 to 7 words).
- **Caps & Punctuation**: Zero all-caps words, zero multiple exclamation points (`!!!`).
- **Emojis**: Maximum 1 relevant emoji per subject line.
- **Language Purity**: Zero mixing of English jargon into Spanish email bodies.
