# Evolution Go Developer & Agent API Manual (v1.0)

Evolution Go (`evolutiongo`) is a high-performance, open-source WhatsApp integration gateway built in Go by the Evolution Foundation, powered by the [`go.mau.fi/whatsmeow`](https://github.com/tulir/whatsmeow) protocol engine. It delivers sub-second cold boot times and consumes up to 90% less memory than traditional Node.js solutions.

This manual provides the comprehensive reference for REST endpoints, WebSockets, Passkey pairing ceremonies, rich messaging payloads, and full-stack integration with **Astro**, **Directus**, **OpenAI/Whisper LLMs**, **NATS JetStream**, **Valkey**, and **PostgreSQL** in Zerops.

---

## 1. 4D Comparative Architectural Matrix

| Dimension | Evolution Go (v0.7.2 Go) | Evolution API v2 (Node.js) | WPPConnect / Baileys Direct | WhatsApp Cloud API (Meta) |
|---|---|---|---|---|
| **Runtime & Language** | **Go 1.24+ / Go Runtime** (Native binary) | Node.js 20+ / TypeScript (V8 Engine) | Node.js / JavaScript (V8 Engine) | Managed Meta Cloud SaaS |
| **Protocol Engine** | **`go.mau.fi/whatsmeow`** (Protobuf/Noise) | `@whiskeysockets/baileys` (JS) | `@wppconnect-team/wppconnect` | Official Meta Graph REST API |
| **Idle Memory (per instance)** | **~15–35 MB RAM** | ~250–600 MB RAM | ~300–700 MB RAM | 0 MB (Cloud hosted) |
| **Active Load CPU Usage** | **~1–3% vCPU** (Goroutines) | ~15–40% vCPU (Event loop) | ~20–50% vCPU (Chromium/JS) | 0% (Remote infrastructure) |
| **Cold Boot Latency** | **< 400 ms** (Instantaneous) | 5–15 seconds (Prisma + V8) | 8–15 seconds | N/A (SaaS) |
| **Concurrency Model** | **Goroutines per socket connection** | Single-threaded Event Loop | Single-threaded Event Loop | Cloud Auto-scaling |
| **Pairing Mechanisms** | **QR Code + Pairing Code + Passkey (WebAuthn)** | QR Code + Pairing Code | QR Code only | Business Manager verification |
| **Rich Message Types** | **Text, Media, List, Button, Carousel, Status** | Text, Media, List, Button, Poll, Status | Text, Media, Buttons | Approved Meta Templates |
| **Native Event Streaming** | **NATS JetStream, AMQP, WS, Webhooks** | RabbitMQ, Redis, Webhooks, WS | EventEmitter, Webhooks | HTTPS Webhooks |
| **Built-in Integrations** | **Raw High-Speed Gateway (External Workers)** | Embedded Typebot, Chatwoot, Dify | Manual custom scripts | Direct Meta Webhooks |
| **Database Architecture** | **Dual PostgreSQL** (`auth_db` + `users_db`) | PostgreSQL (Prisma) / MongoDB / Redis | Local SQLite / File store | Hosted Meta Cloud Store |
| **Zerops Operational Cost** | **Ultra-Low (~32 MB RAM / 0.1 CPU)** | Moderate (~512 MB RAM / 0.5 CPU) | High (~1 GB RAM / 1.0 CPU) | Meta per-conversation fee |

### Zerops Runtime Profile: `os: alpine` vs `os: ubuntu`

| Characteristic | Evolution Go on `os: alpine` (Recommended) | Evolution Go on `os: ubuntu` |
|---|---|---|
| **Binary Linking** | Pure static Go binary (`CGO_ENABLED=0`) | Dynamic binary linking with glibc |
| **Base Container Size** | Minimal (~10 MB filesystem base) | Standard (~120 MB filesystem base) |
| **Idle Memory in Zerops** | **~18–28 MB RAM** | **~35–55 MB RAM** |
| **Build Time with Cache** | **~15 seconds** | ~35 seconds |
| **System Packages** | `apk add --no-cache ca-certificates tzdata curl` | `apt-get install -y ca-certificates tzdata ffmpeg` |
| **Zerops Suitability** | **Optimal for 95% of production deployments** | Recommended only if compiling with custom CGO media filters |

---

## 2. Authentication & Instance Management API

All administrative endpoints require the global API key supplied via the `apikey` HTTP header.

* **Base URL**: `http://<evolutiongo-hostname>:8080` (Zerops internal DNS) or `https://<domain>`
* **Global Auth Header**: `apikey: <GLOBAL_API_KEY>`

### Instance Lifecycle Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/instance/create` | Create a new WhatsApp session instance |
| `GET` | `/instance/connect/{instance}` | Fetch live QR Code in Base64 for pairing |
| `POST` | `/instance/pair` | Generate 8-digit numeric pairing code for phone number |
| `GET` | `/instance/connectionState/{instance}` | Retrieve current connection state (`open`, `connecting`, `close`) |
| `GET` | `/instance/status` | List status of all managed instances |
| `DELETE` | `/instance/logout/{instance}` | Disconnect and invalidate WhatsApp Web session |
| `DELETE` | `/instance/delete/{instance}` | Permanently delete instance and credentials from PostgreSQL |

### Create Instance (`POST /instance/create`)

```bash
curl -s -X POST http://evolutiongo:8080/instance/create \
  -H "apikey: your-global-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "sales-bot",
    "token": "instance-token-optional",
    "qrcode": true,
    "webhook": "http://aiworker:3000/webhook",
    "webhook_by_events": true,
    "events": [
      "MESSAGES_UPSERT",
      "MESSAGES_UPDATE",
      "CONNECTION_UPDATE"
    ]
  }'
```

### Pairing with Phone Number (`POST /instance/pair`)

```bash
curl -s -X POST http://evolutiongo:8080/instance/pair \
  -H "apikey: your-global-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "instance": "sales-bot",
    "phone": "34600112233"
  }'
```
*Returns: `{"pairingCode": "ABCD-1234"}` for user input on the WhatsApp mobile app.*

### WebAuthn Passkey Pairing Ceremony (v0.7.2+)

When WhatsApp servers enforce passkey authentication (*Shortcake / CRSC flow*):
1. Evolution Go detects passkey requirement on instance startup and mints a ceremony token.
2. Endpoint `GET /passkey-ceremony/{token}` serves the WebAuthn challenge.
3. The companion extension or Astro web portal completes the WebAuthn assertion on `web.whatsapp.com`.
4. Endpoint `POST /passkey-ceremony/{token}/confirm` finalizes session establishment.

---

## 3. Messaging & Rich Media APIs

### A. Send Text Message (`POST /send/text`)

En Zerops Incus LXC, el servicio Evolution Go expone su API HTTP de forma canónica en el puerto **`:8085`** (bajo el hostname `http://evolution:8085`).

```bash
# Payload nativo Go (/send/text)
curl -s -X POST http://evolution:8085/send/text \
  -H "apikey: your-global-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "573100000000",
    "text": "Hello *Alex*! Your order *#9821* has been dispatched. 🚀"
  }'
```
*También soporta el formato con selector de instancia:* `{"instance": "sales-bot", "to": "573100000000", "text": "..."}`.

### B. Send Media & Audio PTT (`POST /send/media`)

Supports both URL resolution and Base64 payloads with automatic MIME detection:

```bash
# Sending Audio Voice Note (PTT)
curl -s -X POST http://evolutiongo:8080/send/media \
  -H "apikey: your-global-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "instance": "sales-bot",
    "to": "34611223344",
    "type": "audio",
    "url": "https://storage.zerops.app/voice-notes/response-12.opus",
    "ptt": true
  }'
```

### C. Send Multi-Card Carousel (`POST /send/carousel`)

Renders interactive sliding cards with automatic JPEG thumbnail generation:

```bash
curl -s -X POST http://evolutiongo:8080/send/carousel \
  -H "apikey: your-global-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "instance": "sales-bot",
    "to": "34611223344",
    "text": "Explore our Zerops Managed Cloud services:",
    "cards": [
      {
        "header": {"type": "image", "url": "https://zerops.io/assets/pg.jpg"},
        "title": "Managed PostgreSQL 16",
        "description": "Elastic scaling with single or HA replication.",
        "footer": "Starting at $5/mo",
        "buttons": [
          {"id": "btn_pg_deploy", "text": "Deploy DB"}
        ]
      },
      {
        "header": {"type": "image", "url": "https://zerops.io/assets/valkey.jpg"},
        "title": "Valkey In-Memory Cache",
        "description": "Ultra-fast Redis-compatible cache & pub/sub.",
        "footer": "Sub-millisecond latency",
        "buttons": [
          {"id": "btn_valkey_deploy", "text": "Deploy Cache"}
        ]
      }
    ]
  }'
```

### D. Publish WhatsApp Status (`POST /send/status/text` & `/send/status/media`)

```bash
curl -s -X POST http://evolutiongo:8080/send/status/text \
  -H "apikey: your-global-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "instance": "sales-bot",
    "text": "🎉 New Evolution Go v0.7.2 deployed on Zerops!",
    "backgroundColor": "#25D366"
  }'
```

---

## 4. Full-Stack Zerops Ecosystem Integration: Astro, Directus, LLM, NATS & Valkey

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Internal Network                                                                │
│                                                                                        │
│   ┌──────────────────────────────┐          ┌──────────────────────────────────────┐   │
│   │ Astro Frontend UI            │          │ Directus CMS / CRM (directus:8055)   │   │
│   │ (astro / Bun / Node)         │─────────▶│ - Customer profiles & conversation   │   │
│   │ - Live QR / Status Dashboard │ REST/GQL │ - Automations emit events to NATS    │   │
│   └──────────────────────────────┘          └──────────────────┬───────────────────┘   │
│                                                                │ Event emitter         │
│                                                                ▼                       │
│   ┌──────────────────────────────┐          ┌──────────────────────────────────────┐   │
│   │ Evolution Go Gateway         │          │ NATS JetStream (nats:4222)           │   │
│   │ (go@1.22 / os: alpine)       │◀────────▶│ - `events.whatsapp.incoming`         │   │
│   │ - Port 8080                  │ Pub/Sub  │ - `events.directus.leads`             │   │
│   └──────────────────────────────┘          └──────────────────┬───────────────────┘   │
│                                                                │ Consume               │
│                                                                ▼                       │
│   ┌────────────────────────────────────────────────────────────────────────────────┐   │
│   │ AI Agent Worker (FastAPI / Bun / Node)                                         │   │
│   │ 1. Transcribe voice audio with OpenAI Whisper API                              │   │
│   │ 2. Read conversational sliding window from Valkey (TTL 2h)                     │   │
│   │ 3. Execute LLM Reasoning (OpenAI / Gemini / DeepSeek) with Directus Tools      │   │
│   │ 4. Dispatch response to Evolution Go `POST /send/text` or `POST /send/media`   │   │
│   └──────────────────────────────┬─────────────────────────────┬───────────────────┘   │
│                                  │                             │                       │
│                                  ▼                             ▼                       │
│   ┌──────────────────────────────────────────┐  ┌──────────────────────────────────┐   │
│   │ Valkey Cache Layer (cache:6379)          │  │ Managed PostgreSQL (db:5432)     │   │
│   │ - Idempotency lock `SET lock:msg:* NX`   │  │ - `evogo_auth` (Session keys)    │   │
│   │ - Rate limiting per telephone number     │  │ - `evogo_users` (Chat history)   │   │
│   │ - Chat memory sliding window             │  │ - `directus_db` (CRM SSoT)       │   │
│   └──────────────────────────────────────────┘  └──────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### A. Intelligent AI / LLM Worker Pipeline with Whisper & Directus (TypeScript/Bun)

```typescript
import { connect, JSONCodec } from "nats";
import { createClient } from "redis";
import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const valkey = createClient({ url: process.env.VALKEY_URL || "redis://cache:6379" });
await valkey.connect();

const nc = await connect({ servers: process.env.NATS_URL || "nats://nats:4222" });
const js = nc.jetstream();
const jc = JSONCodec<any>();

const sub = await js.subscribe("events.whatsapp.incoming", { durable_name: "ai-whatsapp-agent" });

for await (const msg of sub) {
  try {
    const event = jc.decode(msg.data);
    const sender = event.data.key.remoteJid; // e.g. "34600112233@s.whatsapp.net"
    const messageId = event.data.key.id;

    // 1. Idempotency Check (Prevent duplicate AI processing)
    const lockKey = `lock:msg:${messageId}`;
    const acquired = await valkey.set(lockKey, "1", { NX: true, EX: 3600 });
    if (!acquired) {
      msg.ack();
      continue;
    }

    let userPrompt = "";

    // 2. Handle Voice Notes (Audio PTT) vs Text
    if (event.data.message?.audioMessage) {
      const audioUrl = event.data.message.audioMessage.url;
      // Download and transcribe with Whisper
      const audioRes = await fetch(audioUrl);
      const audioBlob = await audioRes.blob();
      const transcription = await openai.audio.transcriptions.create({
        file: new File([audioBlob], "voice.opus", { type: "audio/opus" }),
        model: "whisper-1",
      });
      userPrompt = transcription.text;
    } else {
      userPrompt = event.data.message?.conversation || event.data.message?.extendedTextMessage?.text || "";
    }

    if (!userPrompt.trim()) {
      msg.ack();
      continue;
    }

    // 3. Retrieve Conversational History from Valkey (Sliding Window)
    const historyKey = `chat:history:${sender}`;
    const rawHistory = await valkey.lRange(historyKey, 0, 9); // Last 10 messages
    const messages: any[] = [
      { role: "system", content: "You are the AI Assistant for Zerops & Directus. Be concise and friendly." },
      ...rawHistory.map((h) => JSON.parse(h)),
      { role: "user", content: userPrompt }
    ];

    // 4. LLM Inference with Directus CRM Tool Calling
    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages,
      tools: [
        {
          type: "function",
          function: {
            name: "get_directus_order_status",
            description: "Fetch order status from Directus CRM",
            parameters: {
              type: "object",
              properties: { order_id: { type: "string" } },
              required: ["order_id"]
            }
          }
        }
      ]
    });

    let botResponse = completion.choices[0].message.content || "I have received your request.";

    // 5. Save updated conversation state to Valkey
    await valkey.rPush(historyKey, JSON.stringify({ role: "user", content: userPrompt }));
    await valkey.rPush(historyKey, JSON.stringify({ role: "assistant", content: botResponse }));
    await valkey.expire(historyKey, 7200); // 2 hours TTL

    // 6. Send Response back via Evolution Go
    await fetch("http://evolutiongo:8080/send/text", {
      method: "POST",
      headers: {
        "apikey": process.env.GLOBAL_API_KEY || "your-global-api-key",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        instance: "sales-bot",
        to: sender.replace("@s.whatsapp.net", ""),
        text: botResponse
      })
    });

    msg.ack();
  } catch (err) {
    console.error("AI Worker Error:", err);
    msg.nak(5000);
  }
}
```

---

### B. Directus Webhook Flow Triggering WhatsApp Notifications

When a new lead or status update occurs in Directus:
1. Directus Flow (Filter: `items.update` on collection `orders`).
2. Action: **Webhook / Run Script** $\implies$ publishes message payload to NATS `events.directus.leads` or calls Evolution Go `POST /send/text`.
3. Customer receives automated WhatsApp confirmation within milliseconds.

---

### C. Astro Frontend Real-time Pairing Island (React / Astro)

```tsx
import React, { useEffect, useState } from "react";

export function WhatsAppPairingWidget({ instance }: { instance: string }) {
  const [qrCode, setQrCode] = useState<string | null>(null);
  const [status, setStatus] = useState<string>("connecting");

  useEffect(() => {
    async function checkState() {
      const res = await fetch(`/api/whatsapp/connect?instance=${instance}`);
      const data = await res.json();
      if (data.qrcode) setQrCode(data.qrcode);
      if (data.state) setStatus(data.state);
    }
    const interval = setInterval(checkState, 4000);
    checkState();
    return () => clearInterval(interval);
  }, [instance]);

  return (
    <div className="p-6 bg-slate-900 rounded-xl text-white border border-slate-800">
      <h3 className="text-xl font-bold mb-2">WhatsApp Session: {instance}</h3>
      <p className="text-sm text-slate-400 mb-4">Status: <span className="font-semibold text-emerald-400">{status}</span></p>
      {qrCode && status !== "open" ? (
        <img src={qrCode} alt="WhatsApp QR Code" className="w-64 h-64 mx-auto rounded-lg shadow-lg" />
      ) : status === "open" ? (
        <div className="p-4 bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 rounded-lg text-center">
          ✅ Instance Connected & Operational
        </div>
      ) : (
        <p className="text-center animate-pulse">Generating pairing code...</p>
      )}
    </div>
  );
}
```

---

## 5. 5 Production Patterns in Zerops

### Pattern 1: Autonomous AI Conversational Agent with Whisper & Valkey Memory
Incoming voice notes and text messages are routed asynchronously via NATS JetStream, transcribed by Whisper, reasoned by GPT-4o / DeepSeek using Valkey sliding-window context, and responded to automatically.

### Pattern 2: CRM Lead Notification & Campaign Flow via Directus
Directus automated flows publish transactional events to NATS. Evolution Go delivers rich carousel and button notifications to customer phones without blocking database writes.

### Pattern 3: Customer Portal with Astro Live Pairing
Astro SSR frontend embeds a reactive pairing island that renders dynamic QR codes and WebAuthn Passkeys for multi-tenant customer onboarding.

### Pattern 4: High-Throughput Marketing Broadcast Engine
Leverages Go goroutines in Evolution Go to dispatch thousands of interactive messages with rate limiting managed by Valkey token buckets.

### Pattern 5: Resilient S3/Shared Storage Media Ingestion
Stores received media, invoices, and sticker webp files durably on `/mnt/baiostorage/evolutiongo` with automatic MIME validation.

---

## 6. Anti-Patterns & Gotchas

1. **Synchronous LLM Calls in Webhooks**: Never perform 10-second LLM inference inside synchronous HTTP webhook handlers. Always decouple via NATS JetStream queues with ACK/NAK.
2. **Missing Idempotency Locks**: WhatsApp webhooks re-send events if acknowledgments take longer than 5 seconds. Always lock message IDs in Valkey (`SET lock:msg:<id> 1 NX EX 3600`).
3. **Sharing PostgreSQL Database without Schema Separation**: Keep `evogo_auth` and `evogo_users` in separate databases or schemas to avoid lock contention during high-volume message logging.
4. **Ignoring Passkey WebAuthn Support**: New WhatsApp accounts require Passkey ceremonies. Use Evolution Go v0.7.2+ to prevent broken session disconnections.
