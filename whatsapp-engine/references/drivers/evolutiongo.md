# Evolution Go Driver Specification (v2.1)

## 1. Engine Capabilities & Zero-Overhead Footprint
Evolution Go is written in Go (`whatsmeow` library) compiling to a single static binary running on Alpine Linux in Zerops Incus LXC.
- Memory footprint: ~25-45 MB RAM idle (vs 400+ MB for Node.js).
- Direct PostgreSQL session storage (`evogo_auth` and `evogo_users`).
- WebAuthn Passkey pairing and QR code generation.
- Media handling: Image, Video, Document, Voice note PTT, and interactive button carousels.

---

## 2. Health Monitoring & Watchdog
A connection watchdog runs periodically against `GET /instance/status` to monitor state:
- If state is `close` or `connecting`, emit alert to NATS subject `alerts.whatsapp.disconnected`.
- Auto-reconnect routine triggers `POST /instance/connect`.

---

## 3. Media Extraction & Audio Ingestion Invariant
When Evolution Go receives voice notes or media through webhooks (`messages.upsert`):
- **Base64 Payload Location**: The raw base64 string is located at `data.Message.base64` (`msgObj.base64`), NOT nested within `msgObj.audioMessage.base64`.
- **Download Media Fallback**: If the incoming webhook omits inline base64 data, the worker MUST query the Evolution Go endpoint:
  `POST http://evolution:8085/message/downloadmedia` with payload `{ "message": msgObj }` and header `apikey: $EVOLUTION_API_KEY`.
- **Media Type Variations**: Ingestion logic must check `audioMessage`, `AudioMessage`, `mediaType: "audio"`, or `mimetype: audio/...`.
- **Streaming Transcription**: Decode base64 to audio buffer and stream to Groq Whisper Large v3 Turbo (`whisper-large-v3-turbo`) in <350ms.

---

## 4. WhatsApp Multi-Device Identity & `@lid` Filtering
Multi-device WhatsApp accounts emit Linked Device Identifiers (`15-digit-number@lid`) in `chatJid` or `senderJid`:
- **Silent Drop Invariant**: Dispatching messages directly to `@lid` via Evolution Go `POST /send/text` fails or drops silently.
- **Resolution Priority**: The worker must prioritize real phone numbers by checking `SenderAlt` or JIDs ending in `@s.whatsapp.net`.
- **Normalization**: Clean non-numeric characters to E.164 digits before passing to database queries or message dispatch.

---

## 5. Early Webhook ACK Invariant (<15ms)
To prevent webhook retry cascades from Evolution Go:
- Ingress proxies or workers MUST return `HTTP 200 {"status": "acknowledged"}` within 15ms.
- Asynchronous processing (Whisper audio transcription, Valkey session retrieval, PostgreSQL profile lookup, Bifrost LLM inference) executes in background promises or via NATS JetStream consumers.

---

## 6. Deep Reference Documentation
- [`references/usage.md`](file:///var/www/.agents/skills/whatsapp-engine/references/usage.md) — 4D matrix, instance lifecycle endpoints, pairing codes, WebAuthn Passkey, media endpoints, and cURLs.
- [`references/infra.md`](file:///var/www/.agents/skills/whatsapp-engine/references/infra.md) — Alpine LXC setup, systemd, Zerops topology, and PostgreSQL session stores.
