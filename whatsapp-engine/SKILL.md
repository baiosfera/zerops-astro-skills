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
- **Brand SSoT & Persona**: Ingest personas via `$SYSTEM_PROMPT_PATH` or `$BRAND_SSOT_PATH` (UTC-5). Use warm informal "tú", avoiding cold support lists. Ground catalog links strictly in verified Astro routes.
- **Bifrost LLM & Whisper**: Route completions to `http://bifrost:8080/v1/chat/completions` and voice notes to `http://bifrost:8080/v1/audio/transcriptions` with Bearer key.
- **Takeover & Context**: Operator messages (`fromMe: true`) lock customer chat ID (`key.remoteJid`/`info.Chat`, never LID) for 2h in Valkey (`wa:human_takeover:${id}`). Commands: `#bot` clears; `#mute` silences 24h. Prepend quoted message context (`contextInfo.quotedMessage`).
- **Ambassador Loop & Pacing**: Offer 3-referral reward loop at delight peaks with 7-day Valkey cooldown (`wa:affiliate_pitched:${phone}`). Pace with 2.5s–7s typing delays.
- **Decoupling & Hygiene**: Acknowledge webhooks <10ms via NATS JetStream `events.whatsapp.incoming`. Deduplicate in Valkey 7.2 (`SET lock:wa:msg:${id} 1 NX EX 3600`). Run Evolution Go on `alpine/go@1.22` with PostgreSQL schemas (`evogo_auth`, `evogo_users`). Bound CLI commands (`timeout 10s`).

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
