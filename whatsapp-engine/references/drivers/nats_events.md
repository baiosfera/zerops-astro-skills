# NATS JetStream Decoupling & Event Mesh for WhatsApp (v1.0)

## 1. Webhook Decoupling Rationale
Evolution Go delivers webhooks for incoming WhatsApp messages (`messages.upsert`). Executing LLM generation, pgvector retrieval, or CRM updates synchronously inside the webhook callback causes request timeouts, worker pool exhaustion, and dropped messages.

### Decoupled Pipeline:
1. **Webhook Ingress**: Evolution Go posts to `/api/webhooks/whatsapp`.
2. **NATS JetStream Publish**: The endpoint publishes the raw message to subject `events.whatsapp.incoming` and immediately returns HTTP `200 OK` (<20ms).
3. **Queue Group Worker**: Multiple instances of the conversational agent consume from `events.whatsapp.incoming` using a shared queue group (`qgroup:whatsapp-bot`).
4. **Valkey Deduplication**: Lock key `lock:wa:msg:${messageId}` prevents duplicate processing on webhook retries.
5. **Response Dispatch**: After LLM reasoning and CRM lookups, the worker calls Evolution Go's `POST /message/sendText` or publishes to `events.whatsapp.outgoing`.

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
    "text": "¿Tienen el enterizo velvet en talla M?",
    "hasMedia": false
  }
}
```
