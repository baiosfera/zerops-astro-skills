# NATS JetStream Decoupling & Event Mesh for WhatsApp (v1.0)

## 1. Webhook Decoupling Rationale
Evolution Go delivers webhooks for incoming WhatsApp messages (`messages.upsert`). Executing LLM generation, pgvector retrieval, or CRM updates synchronously inside the webhook callback causes request timeouts, worker pool exhaustion, and dropped messages.

### Decoupled Pipeline:
1. **Webhook Ingress**: Evolution Go posts to `/api/webhooks/whatsapp` (ultralight endpoint).
2. **NATS JetStream Publish**: The endpoint publishes the raw message to subject `events.whatsapp.incoming` with header `Nats-Msg-Id: evt_${messageId}` for native stream deduplication (120s window) and immediately returns HTTP `200 OK` (<15ms).
3. **Queue Group Worker**: A dedicated Zerops service (`whatsappbot` on `ubuntu/bun@1.3`, isolated from the web SSR container) consumes from `events.whatsapp.incoming` using durable pull consumer queue group (`qgroup:whatsapp-bot`).
4. **Valkey Deduplication & Human Takeover**: Atomic lock `SET lock:wa:msg:${messageId} 1 NX EX 3600` and check `wa:human_takeover:${phone}` (2h operator silence window).
5. **Deterministic Tool Calling & Grounding**: Executes relational SQL (`WHERE fecha >= CURRENT_DATE`) against PostgreSQL 18 via Bifrost function calling, avoiding hallucinated dates or unnecessary pgvector latency.
6. **Response Dispatch**: Calls Evolution Go's `POST /message/sendText` with paced typing delay (2.5s–7s) and acknowledges message in NATS (`msg.ack()`).

---

## 2. NATS Event Schema (`events.whatsapp.incoming`)
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "eventId": "evt_98127391",
  "timestamp": 1757182910,
  "source": "evolutiongo",
  "instance": "sales-bot",
  "sender": {
    "phone": "573001234567",
    "pushName": "Valentina"
  },
  "message": {
    "id": "BAE5F1289123",
    "conversationType": "individual",
    "text": "¿Tienen el producto en talla M?",
    "hasMedia": false
  }
}
```
