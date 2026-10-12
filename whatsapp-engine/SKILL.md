---
name: whatsapp-engine
description: "Trigger: whatsapp-engine, evolutiongo, evolution-api, whatsmeow, bifrost llm, nats whatsapp, whatsapp bot, whatsapp crm directus. High-Performance WhatsApp Messaging, Brand SSoT Ingestion & Bifrost LLM Gateway Orchestrator in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `whatsapp-engine` — WhatsApp Messaging & AI Orchestrator (v2.0)

## Activation Contract
Deploying Evolution Go (`whatsmeow`), Meta Cloud API, QR/Passkey pairing, warmup, Bifrost LLM Gateway (`http://bifrost:8080/v1`), dynamic SSoT identity (`$SYSTEM_PROMPT_PATH`), or NATS JetStream in Zerops.

## Hard Rules & Positive Guidance
- **Brand SSoT & Persona**: Ingest personas via `$BRAND_SSOT_PATH` (default: `/mnt/localstorage/${PROJECT_NAME}/dev/system_prompt.md`, fallback seed from `/var/www/baiosfera/PROYECTOS/${PROJECT_NAME}`). Worker holds exclusive identity control; Bifrost remains agnostic transport. Ground catalog links strictly in verified Astro routes.
- **Bifrost Dual-Tier & Whisper**: Route completions to `http://bifrost:8080/v1/chat/completions` using Dual-Tier Predictive Routing (`x-tier: production` for transactional/sales/tools direct to Pro Tier; FreeLLMAPI with 2.5s timeout for FAQs). Route audio to Groq Whisper (<350ms). Use hybrid memory (Valkey hot buffer + Postgres profiles, zero ltrim amnesia).
- **Takeover & SSoT Resilience**: Operator commands (`#stop`, `#off`, `#silencio`, `#desactivar`) establish permanent sovereign silence (10 years). Subsequent operator manual messages strictly preserve active `#stop` without downgrading to temporary pauses. Commands: `#mute` silences 24h; `#bot` reactivates. Operator manual messages without active `#stop` pause 2h. Persist `bot_status` (`stopped` | `muted` | `active`) in PostgreSQL `leads.metadata` (SSoT) with automatic Valkey re-hydration upon cache-miss or container restarts. Prepend quoted context (`contextInfo.quotedMessage`).
- **Pluggable Referral & Pacing**: When the brand implements affiliate mechanics, offer referral loop at delight peaks with 7-day Valkey cooldown (`wa:affiliate_pitched:${phone}`). If the project has no affiliate table, omit referral mentions (dynamic feature detection). Pace responses with 1.5s–3s typing delays.
- **Continuous Present Time & Positive CoHaLo**: Query business events and services in real-time from PostgreSQL filtering in continuous present (`date >= NOW()` in local timezone UTC-5). Omit negative prompt restrictions; present affirmatively what exists in the database.
- **Decoupling, Replay Guard & Early ACK**: Reject replayed/stale webhook events older than 120s (`ageSeconds > 120`) via `extractMessageEpochMs` to prevent restart storms from buffered queues. Enforce 24h distributed deduplication locks (`acquireLock(messageId)` with `EX 86400`) in Valkey. Run dedicated worker in Bun LXC (`whatsappbot`), never in Astro SSR. Acknowledge webhooks <15ms before LLM inference to eliminate Evolution API retry storms. Stream through NATS JetStream `events.whatsapp.incoming` with `Nats-Msg-Id` deduplication. Bound CLI commands (`timeout 10s`).
- **Real-Time SSoT & Role Adaptation**: Ingest live user profile attributes (`alias`, `email`, `role`, `city`, `affiliateAlias`). Adapt tone dynamically: `hombre_solo` (masculine singular), `mujer_sola` (feminine singular), `pareja` (couple plural: "ustedes", "chicos", "pareja", "ambos", "como pareja"), `otro` (neutral).
- **SSoT Override Rule & Deduplication**: PostgreSQL is ground truth in the current millisecond. Ignore outdated historical chat turns from Valkey when user updates profile. Lookup by phone variants and 10-digit suffix (`ORDER BY completeness DESC, updated_at DESC`) to prevent blank orphan leads.
- **Media Ingestion & @lid Invariant**: Extract audio from `data.Message.base64` (`msgObj.base64`) with fallback to `POST /message/downloadmedia`. Discard multi-device `@lid` for dispatch, resolving to real E.164 phone numbers (`SenderAlt` / `@s.whatsapp.net`).
- **Vault Self-Shadowing Invariant**: In `zerops.yaml`, never map `KEY: ${KEY}` for vault secrets. Use distinct names: `GROQ_API_KEY: ${WHISPER_GROQ_API_KEY}`.

## Decision Gates

| Objective | Protocol | Reference |
|---|---|---|
| Topology | 4D comparative matrix (Evolution Go vs Cloud API) | [`usage.md`](file:///var/www/.agents/skills/whatsapp-engine/references/usage.md) |
| Bifrost & SSoT | Dynamic system prompt ingestion & LLM completions | [`bifrost_llm.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/bifrost_llm.md) |
| NATS Mesh | JetStream publish pipeline & worker pools | [`nats_events.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/nats_events.md) |
| Evolution Go | Pairing, sessions, passkeys & media endpoints | [`evolutiongo.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/evolutiongo.md) |
| Meta Cloud | Official Cloud client SDK & webhook HMAC | [`meta_cloud.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/meta_cloud.md) |
| Warmup | Multi-phase volume ramp & conversation ratios | [`anti_ban_warmup_guide.md`](file:///var/www/.agents/skills/whatsapp-engine/assets/anti_ban_warmup_guide.md) |
| Recipes | Runtime configs & AI worker definitions | [`whatsapp_engine_recipes.json`](file:///var/www/.agents/skills/whatsapp-engine/assets/whatsapp_engine_recipes.json) |
| Validation | Attest structure, frontmatter, tokens & links | [`whatsapp-engine-validate.sh`](file:///var/www/.agents/skills/whatsapp-engine/scripts/whatsapp-engine-validate.sh) |

## Execution Steps
1. Deploy Evolution Go on Zerops Alpine with PostgreSQL schemas (`evogo_auth`, `evogo_users`).
2. Ingest brand persona via `$SYSTEM_PROMPT_PATH` or `$BRAND_SSOT_PATH`.
3. Stream webhooks to NATS JetStream `events.whatsapp.incoming`.
4. Run async AI consumers via Bifrost LLM Gateway on port 8080.
5. Apply warmup and verify with `scripts/whatsapp-engine-validate.sh`.

## Output Contract
- Memory-efficient WhatsApp bot in Zerops Incus LXC.
- Sub-20ms webhook acknowledgment, brand-aligned AI, and passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/whatsapp-engine/references/usage.md) — 4D matrix, Passkeys, and messaging API.
- [`references/infra.md`](file:///var/www/.agents/skills/whatsapp-engine/references/infra.md) — Multi-service topology and env vars.
- [`references/drivers/bifrost_llm.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/bifrost_llm.md) — Bifrost LLM gateway and SSoT ingestion.
- [`references/drivers/nats_events.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/nats_events.md) — NATS JetStream event mesh and schemas.
- [`references/drivers/evolutiongo.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/evolutiongo.md) — Evolution Go binary and pairing.
- [`references/drivers/meta_cloud.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/meta_cloud.md) — Meta Cloud API v21.0 integration.
- [`assets/anti_ban_warmup_guide.md`](file:///var/www/.agents/skills/whatsapp-engine/assets/anti_ban_warmup_guide.md) — Operational anti-ban warmup.
- [`assets/whatsapp_engine_recipes.json`](file:///var/www/.agents/skills/whatsapp-engine/assets/whatsapp_engine_recipes.json) — Production deployment recipes.
- [`scripts/whatsapp-engine-validate.sh`](file:///var/www/.agents/skills/whatsapp-engine/scripts/whatsapp-engine-validate.sh) — Quality & token validation sensor.
