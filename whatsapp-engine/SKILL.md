---
name: whatsapp-engine
description: "Trigger: whatsapp-engine, evolutiongo, evolution-api, whatsmeow, bifrost llm, nats whatsapp, whatsapp bot, whatsapp crm directus. High-Performance WhatsApp Messaging, Brand SSoT Ingestion & Bifrost LLM Gateway Orchestrator in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# `whatsapp-engine` — WhatsApp Messaging & AI Orchestrator (v2.1)

## Activation Contract
Deploying Evolution Go (`whatsmeow`), Meta Cloud API, QR/Passkey pairing, warmup, Bifrost LLM Gateway, dynamic SSoT identity, or NATS JetStream in Zerops.

## Core Directives & Invariants
- **Brand SSoT & Persona**: Ingest personas via `$BRAND_SSOT_PATH` (default: `/mnt/localstorage/${PROJECT_NAME}/dev/system_prompt.md`). The bot worker owns conversational identity; Bifrost remains an agnostic gateway. Catalog links must ground in verified Astro routes.
- **Bifrost Dual-Tier Routing**: Direct completions to `http://bifrost:8080/v1/chat/completions` using Dual-Tier routing (`x-tier: production` for transactional/sales/tools; FreeLLMAPI with 2.5s timeout for FAQs). Route audio to Groq Whisper (<350ms). Use Valkey for hot buffers and PostgreSQL for permanent lead profiles.
- **Takeover Monotonicity & PostgreSQL SSoT**: Operator commands (`#stop`, `#off`, `#silencio`, `#desactivar`) trigger a permanent 10-year pause (`EX 315360000`). Subsequent operator messages preserve `#stop` without resetting to a 2h pause. Commands `#mute` silences 24h; `#bot` reactivates. Operator manual messages without active `#stop` pause 2h. Persist `bot_status` in PostgreSQL `leads.metadata` and re-hydrate Valkey on cache miss.
- **Continuous Present & Dynamic Role Adaptation**: Filter business events in real-time continuous present (`date >= NOW()` in local UTC-5). Ingest live profile attributes (`alias`, `email`, `role`, `city`, `affiliateAlias`) and adapt grammatical gender/number (`hombre_solo`, `mujer_sola`, `pareja`, `otro`).
- **Decoupling, Replay Guard & Early ACK**: Reject webhook events older than 120s via `extractMessageEpochMs`. Enforce 24h distributed deduplication locks (`acquireLock(messageId)` with `EX 86400`) in Valkey. Run dedicated workers in Bun LXC (`whatsappbot`), never inside Astro SSR. Acknowledge webhooks <15ms before LLM inference. Stream through NATS JetStream `events.whatsapp.incoming`.
- **Infrastructure Isolation**: Separate `evogo_auth` and `evogo_users` databases in PostgreSQL with `CONNECTION LIMIT 15` and `idle_session_timeout = '2min'`. In `zerops.yaml`, prevent vault self-shadowing by using distinct names (e.g., `GROQ_API_KEY: ${WHISPER_GROQ_API_KEY}`).

## Decision Gates & References
- **Topology & Protocol**: [`usage.md`](file:///var/www/zerops-astro-skills/whatsapp-engine/references/usage.md) — 4D comparative matrix, Passkeys, and messaging API.
- **Infrastructure & Zerops**: [`infra.md`](file:///var/www/zerops-astro-skills/whatsapp-engine/references/infra.md) — Multi-service topology, `import.yaml`, and env vars.
- **Bifrost & SSoT Driver**: [`bifrost_llm.md`](file:///var/www/zerops-astro-skills/whatsapp-engine/references/drivers/bifrost_llm.md) — System prompt ingestion & LLM completions.
- **NATS JetStream Driver**: [`nats_events.md`](file:///var/www/zerops-astro-skills/whatsapp-engine/references/drivers/nats_events.md) — JetStream event mesh and schemas.
- **Evolution Go Driver**: [`evolutiongo.md`](file:///var/www/zerops-astro-skills/whatsapp-engine/references/drivers/evolutiongo.md) — Binary pairing and media endpoints.
- **Meta Cloud Driver**: [`meta_cloud.md`](file:///var/www/zerops-astro-skills/whatsapp-engine/references/drivers/meta_cloud.md) — Meta Cloud API v21.0 integration.
- **Warmup & Anti-Ban**: [`anti_ban_warmup_guide.md`](file:///var/www/zerops-astro-skills/whatsapp-engine/assets/anti_ban_warmup_guide.md) — Operational warmup guide.
- **Validation**: [`whatsapp-engine-validate.sh`](file:///var/www/zerops-astro-skills/whatsapp-engine/scripts/whatsapp-engine-validate.sh) — Quality & token validation sensor.
