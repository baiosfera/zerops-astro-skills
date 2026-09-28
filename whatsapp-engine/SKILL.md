---
name: whatsapp-engine
description: "Trigger: whatsapp-engine, evolutiongo, evolution-api, whatsmeow, bifrost llm, nats whatsapp, whatsapp bot, whatsapp crm directus. High-Performance WhatsApp Messaging, Brand SSoT Ingestion & Bifrost LLM Gateway Orchestrator in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# `whatsapp-engine` — High-Performance WhatsApp Messaging & AI Orchestrator (v1.1)

## Activation Contract
Activate when deploying, configuring, or integrating Evolution Go (`whatsmeow`), Meta WhatsApp Cloud API v21.0, or WhatsApp gateways, pairing QR codes/Passkeys, warming up new numbers with anti-ban protocols, handling incoming webhooks, streaming conversational inference via **Bifrost LLM Gateway** (`http://bifrost:8000/v1`), injecting **Brand SSoT** identity from `/brand/`, or decoupling message processing with **NATS JetStream** in Zerops.

## Hard Rules & Positive Guidance
- **Brand SSoT Ingestion**: The conversational bot MUST ingest its system persona, tone, and policies directly from the local single-tenant path `/brand/fase0_system_prompt.md`.
- **Bifrost LLM Gateway Ingestion**: All AI inference MUST route through the universal OpenAI-compatible endpoint `http://bifrost:8000/v1/chat/completions`.
- **Asynchronous Webhook Decoupling**: NEVER run synchronous LLM calls or database lookups inside the HTTP webhook handler. Incoming messages MUST be published to NATS JetStream subject `events.whatsapp.incoming` (<20ms acknowledgment).
- **Anti-Ban Warmup Protocol**: New or rotated WhatsApp lines MUST strictly follow [`assets/anti_ban_warmup_guide.md`](file:///var/www/.agents/skills/whatsapp-engine/assets/anti_ban_warmup_guide.md) to prevent spam flags or number bans by Meta.
- **Valkey Idempotency & Sliding Windows**: Enforce message deduplication locks (`SET lock:wa:msg:${id} 1 NX EX 3600`) and conversational history cache in Valkey.
- **Zerops Native Footprint**: Deploy Evolution Go as a native Go service (`alpine/go@1.22`) connected to managed PostgreSQL schemas (`evogo_auth`, `evogo_users`), consuming ~25-45 MB RAM idle.
- **Strict Credential Protection**: API keys (`$GLOBAL_API_KEY`) and database credentials MUST be referenced via environment variable names.
- **Fractal CoHaLo Execution**: Enforce command hygiene (`timeout 10s`), wait limits (`WaitMsBeforeAsync: 10000`), zero orphan tasks, and sensor verification (`GET /health`).

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Gateway Architecture | 4D comparative matrix (Evolution Go vs Evolution API vs Cloud) | [`references/usage.md#1-4d-comparative-architectural-matrix`](file:///var/www/.agents/skills/whatsapp-engine/references/usage.md) |
| Bifrost LLM & Brand SSoT | System prompt ingestion from `/brand/` and Bifrost completions | [`references/drivers/bifrost_llm.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/bifrost_llm.md) |
| NATS Event Mesh Decoupling | JetStream publish pipeline and queue group workers | [`references/drivers/nats_events.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/nats_events.md) |
| Evolution Go Driver | Pairing, sessions, status watchdog & media endpoints | [`references/drivers/evolutiongo.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/evolutiongo.md) |
| Meta Cloud API v21.0 | Official Meta Cloud client SDK and webhook verification | [`references/drivers/meta_cloud.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/meta_cloud.md) |
| Anti-Ban Warmup Protocol | Multi-phase volume ramp and conversational ratios | [`assets/anti_ban_warmup_guide.md`](file:///var/www/.agents/skills/whatsapp-engine/assets/anti_ban_warmup_guide.md) |
| Production Recipes JSON | Runtime configs, carousel messages & AI worker definitions | [`assets/whatsapp_engine_recipes.json`](file:///var/www/.agents/skills/whatsapp-engine/assets/whatsapp_engine_recipes.json) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/whatsapp-engine-validate.sh`](file:///var/www/.agents/skills/whatsapp-engine/scripts/whatsapp-engine-validate.sh) |

## Execution Steps
1. Deploy Evolution Go runtime on Zerops Alpine container with dual PostgreSQL schemas.
2. Mount local brand directives at `/var/www/evolution/brand/fase0_system_prompt.md`.
3. Configure webhook ingress to broadcast incoming messages to NATS `events.whatsapp.incoming`.
4. Deploy consumer worker that reads brand system prompt and calls Bifrost LLM Gateway.
5. Apply anti-ban warmup sequence for new phone numbers.
6. Verify health check via physical sensor (`scripts/whatsapp-engine-validate.sh`).

## Output Contract
- High-throughput, memory-efficient WhatsApp sales bot running on Zerops Incus LXC.
- Sub-50ms webhook response time, brand-aligned conversations, and passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/whatsapp-engine/references/usage.md) — 4D comparative matrix, Passkey ceremonies, rich messaging, and full-stack integration.
- [`references/infra.md`](file:///var/www/.agents/skills/whatsapp-engine/references/infra.md) — Multi-service topology, `import.yaml`, `zerops.yaml`, and environment variables dictionary.
- [`references/drivers/bifrost_llm.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/bifrost_llm.md) — Bifrost LLM gateway and Brand SSoT ingestion specification.
- [`references/drivers/nats_events.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/nats_events.md) — NATS JetStream event-driven architecture and payload schemas.
- [`references/drivers/evolutiongo.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/evolutiongo.md) — Evolution Go static binary, watchdog routines, and pairing.
- [`references/drivers/meta_cloud.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/meta_cloud.md) — Official Meta Cloud API v21.0 integration manual.
- [`assets/anti_ban_warmup_guide.md`](file:///var/www/.agents/skills/whatsapp-engine/assets/anti_ban_warmup_guide.md) — Operational anti-ban warmup protocols.
- [`assets/whatsapp_engine_recipes.json`](file:///var/www/.agents/skills/whatsapp-engine/assets/whatsapp_engine_recipes.json) — Production deployment recipes and worker payloads.
- [`scripts/whatsapp-engine-validate.sh`](file:///var/www/.agents/skills/whatsapp-engine/scripts/whatsapp-engine-validate.sh) — Deterministic quality & token validation sensor.
