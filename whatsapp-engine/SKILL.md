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
Deploying Evolution Go (`whatsmeow`), Meta WhatsApp Cloud API v21.0, QR/Passkey pairing, anti-ban warmup, webhooks, Bifrost LLM Gateway (`http://bifrost:8080/v1`), dynamic SSoT identity (`$SYSTEM_PROMPT_PATH`), or NATS JetStream event decoupling in Zerops.

## Hard Rules & Positive Guidance
- **Brand SSoT Ingestion**: Ingest conversational personas dynamically via `$SYSTEM_PROMPT_PATH` or `$BRAND_SSOT_PATH` with continuous present temporal awareness (UTC-5) and zero hardcoded dates.
- **Bifrost LLM & Whisper Integration**: Route completions through `http://bifrost:8080/v1/chat/completions` and voice note transcriptions through `http://bifrost:8080/v1/audio/transcriptions` supplying `Authorization: Bearer <vk>`. If audio cannot be decoded, reply with graceful brand empathy instead of dropping the message.
- **Multi-Identifier Sliding Human Takeover (2h)**: When the operator replies from phone (`fromMe: true`), lock the customer's remote chat identifier (`key.remoteJid` / `info.Chat`), NEVER the operator's sender LID. Lock both phone and LID in Valkey (`wa:human_takeover:${id}`). Operator commands: `#bot` clears takeover immediately, `#mute` silences for 24h.
- **Quoted Message Context Preservation**: Parse `contextInfo.quotedMessage` from incoming messages and prepend it to the user prompt (`[Mensaje citado: "..."]\n<texto>`) so the LLM retains immediate contextual grounding when users reply to previous questions.
- **Strict Route Whitelist Grounding (Zero 404s)**: Ground all recommended URLs strictly on the verified catalog of Astro routes. The LLM is strictly prohibited from guessing, hallucinating, or synthesizing URLs outside the explicit whitelist.
- **Mandatory Tuteo & Anti-Slop Persona**: Conversational persona MUST address users with warm informal "tú", eradicating cold "usted" and generic support-bot bullet lists. Address cultural terms positively (e.g. clarify ethical facilitation vs paid hostesses without negative prompting). Simulate human typing delays (2.5s - 7s).
- **Ambassador Loop & Frequency Capping**: Promote 3-referral free ticket loop only at high-delight moments. Enforce a 7-day Valkey cooldown (`wa:affiliate_pitched:${phone}`) to prevent repetitive spam.
- **Asynchronous Decoupling**: Acknowledge webhooks under 10ms by publishing events to NATS JetStream `events.whatsapp.incoming` with `Nats-Msg-Id`.
- **Anti-Ban Protocol**: Follow progressive warmup schedules in [`anti_ban_warmup_guide.md`](file:///var/www/.agents/skills/whatsapp-engine/assets/anti_ban_warmup_guide.md).
- **Valkey Idempotency**: Enforce deduplication (`SET lock:wa:msg:${id} 1 NX EX 3600`) and buffers in Valkey 7.2.
- **Zerops Footprint**: Run Evolution Go on `alpine/go@1.22` with PostgreSQL schemas (`evogo_auth`, `evogo_users`), consuming ~25-45 MB RAM.
- **Secret Hygiene**: Reference `$GLOBAL_API_KEY` and connection strings by variable name.
- **Process Hygiene**: Bound CLI commands (`timeout 10s`) and verify state with deterministic sensors.

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
1. Deploy Evolution Go runtime on Zerops Alpine with dual PostgreSQL schemas (`evogo_auth`, `evogo_users`).
2. Inject brand directives via `$SYSTEM_PROMPT_PATH` or `$BRAND_SSOT_PATH`.
3. Configure webhook ingress to broadcast incoming events to NATS JetStream `events.whatsapp.incoming`.
4. Deploy asynchronous consumer workers calling Bifrost LLM Gateway on port 8080.
5. Apply anti-ban warmup schedule for new phone instances.
6. Verify service health and contract compliance via `scripts/whatsapp-engine-validate.sh`.

## Output Contract
- High-throughput, memory-efficient WhatsApp bot on Zerops Incus LXC.
- Sub-20ms webhook acknowledgment, brand-aligned conversations, and passing physical sensors.

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
