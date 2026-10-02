---
name: email-marketing
description: "Trigger: email-marketing, react email, zeptomail, zoho email, aws ses v2, resend api, listmonk, nodemailer smtp, dmarc rfc 9989, dkim 2048, list unsubscribe one click, bullmq email queue, brandbook email bridge. High-deliverability email marketing engine with React Email 3.0, ZeptoMail, SES v2, Listmonk & BullMQ in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `email-marketing` — Deliverability & Multi-Provider Engine (v2.0)

## Activation Contract
Activate when designing, sending, or automating email flows, transactional emails, React Email 3.0 templates, deliverability (**DMARCbis RFC 9989**, **DKIM 2048**, **SPF**, **RFC 8058 One-Click**, **Spam Rate < 0.10%**), Zoho ZeptoMail, Amazon SES v2, Resend, Listmonk, `brandbook.json` token transpilation, or SMTP dispatchers on Valkey 7.2.

## Hard Rules & Technical Invariants
- **RFC 8058 One-Click Unsubscribe**: Marketing emails MUST include `List-Unsubscribe` and `List-Unsubscribe-Post: List-Unsubscribe=One-Click` headers signed under DKIM.
- **DMARCbis RFC 9989 & 2048-bit DKIM**: Maintain 2048-bit DKIM keys and `p=quarantine`/`p=reject` DMARC records without the obsoleted `pct` tag. Maintain spam complaints below **0.10%** in Google Postmaster Tools.
- **Anti-Clipping & Inline CSS**: Total compiled HTML size MUST stay below **85 KB** to prevent Gmail message clipping and preserve footer unsubscribe links. All CSS styles MUST compile 100% inline without Base64 assets.
- **Multi-Provider Failover**: Route transactional emails through `UnifiedEmailDispatcher` supporting Listmonk (self-hosted), ZeptoMail, AWS SES v2, and Resend with automatic cascade.
- **Rate-Limited Queueing**: Bulk marketing blasts MUST be throttled through BullMQ workers on Valkey 7.2 with a concurrency limit of 10 emails/sec.
- **Brandbook Token Transpilation**: Load palette, font stacks, and SVG marks dynamically from `brandbook.json` using `loadEmailBrandTokens()`.

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Multi-Provider Engine | Listmonk, ZeptoMail, AWS SES, Resend dispatcher | [`assets/email_dispatcher.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_dispatcher.ts) |
| Transactional Template | Polymorphic React Email 3.0 component (<85 KB) | [`assets/GenericTransactionalEmail.tsx`](file:///var/www/.agents/skills/email-marketing/assets/GenericTransactionalEmail.tsx) |
| Brandbook Bridge | Dynamic W3C DTCG design token transpiler | [`assets/email_brandbook_bridge.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_brandbook_bridge.ts) |
| Schemas & Contracts | Payload validation & webhook events schemas | [`assets/email_zod_schemas.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_zod_schemas.ts) |
| Throttled BullMQ Worker | Valkey queue consumer with rate limiting | [`assets/email_bullmq_worker.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_bullmq_worker.ts) |
| Production Recipes | Dispatcher and reactive NATS listener recipes | [`assets/email_marketing_production_recipes.json`](file:///var/www/.agents/skills/email-marketing/assets/email_marketing_production_recipes.json) |
| Usage & 4D Matrix | Deliverability guide, Bun SSR streaming & RFC 8058 | [`references/usage.md`](file:///var/www/.agents/skills/email-marketing/references/usage.md) |
| Topology & DNS | Zerops Listmonk setup, DKIM, SPF & SES runbooks | [`references/infra.md`](file:///var/www/.agents/skills/email-marketing/references/infra.md) |
| Physical Validation | Deterministic integrity sensor | [`scripts/email-marketing-validate.sh`](file:///var/www/.agents/skills/email-marketing/scripts/email-marketing-validate.sh) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/email-marketing/references/usage.md) — Multi-provider matrix, Bun SSR streaming, and RFC 8058.
- [`references/infra.md`](file:///var/www/.agents/skills/email-marketing/references/infra.md) — Zerops Listmonk topology, BullMQ worker configuration, and DNS setup.
- [`assets/WelcomeLatAmEmail.tsx`](file:///var/www/.agents/skills/email-marketing/assets/WelcomeLatAmEmail.tsx) — LatAm transactional React Email template.
- [`assets/email_dispatcher.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_dispatcher.ts) — Multi-provider failover dispatcher with Listmonk support.
- [`assets/email_brandbook_bridge.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_brandbook_bridge.ts) — W3C DTCG design token transpiler.
- [`assets/email_bullmq_worker.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_bullmq_worker.ts) — Throttled BullMQ queue worker on Valkey.
- [`assets/email_zod_schemas.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_zod_schemas.ts) — Zod email validation schemas.
- [`assets/email_marketing_production_recipes.json`](file:///var/www/.agents/skills/email-marketing/assets/email_marketing_production_recipes.json) — Production code recipes.
- [`scripts/email-marketing-validate.sh`](file:///var/www/.agents/skills/email-marketing/scripts/email-marketing-validate.sh) — Deterministic physical validator.
