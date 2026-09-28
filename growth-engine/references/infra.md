# Sovereign Growth Engine Infrastructure Specification (v1.0)

## 1. Environment Variables & Gateway Routing

| Variable | Target | Purpose | Example |
|---|---|---|---|
| `BIFROST_URL` | Bifrost Gateway | Universal OpenAI-compatible LLM proxy | `http://bifrost:8000/v1` |
| `VALKEY_URL` / `$cache_connectionString` | Valkey | Cart abandonment staging and BullMQ queues | `valkey://...` |
| `NATS_URL` / `$nats_url` | NATS | Event bus for outbound email/WhatsApp triggers | `nats://...` |
| `DIRECTUS_URL` | Directus | Product catalog and customer CRM ingestion | `http://directus:8055` |

---

## 2. Brand SSoT File Locations
- `/var/www/astro/brand/fase0_system_prompt.md`: Local brand guidelines and voice SSoT.
- `/var/www/astro/brand/brandbook.json`: Design tokens, colors, typography, and archetype definitions.
