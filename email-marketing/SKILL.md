---
name: email-marketing
description: "Trigger: email-marketing, react email, zeptomail, zoho email, aws ses v2, resend api, listmonk, nodemailer smtp, dmarc rfc 9989, dkim 2048, list unsubscribe one click, bullmq email queue, brandbook email bridge, mta-sts, tls-rpt, bimi. High-deliverability email marketing engine with React Email 3.0, ZeptoMail, SES v2, Listmonk & BullMQ in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.0"
---

# `email-marketing` — Deliverability & Multi-Provider Engine (v3.0)

## Activation Contract
Activate when designing, sending, or automating email flows, transactional emails, React Email 3.0 templates, deliverability (DMARCbis RFC 9989, DKIM 2048, SPF, RFC 8058 One-Click, MTA-STS RFC 8461, TLS-RPT RFC 8460, BIMI, Spam Rate < 0.10%), Zoho ZeptoMail, Amazon SES v2, Resend, Listmonk, brandbook.json token transpilation, or SMTP dispatchers on Valkey 7.2.

## Hard Rules & Technical Invariants
- **RFC 8058 One-Click**: Marketing emails MUST include List-Unsubscribe and List-Unsubscribe-Post: List-Unsubscribe=One-Click headers signed under DKIM. Ingest POST responses atomically via dedicated HTTPS endpoint.
- **DMARCbis RFC 9989 & 2048-bit DKIM**: Maintain 2048-bit DKIM keys and p=quarantine/p=reject DMARC records (np=reject, t=n). Keep spam complaints below 0.10% in Google Postmaster Tools.
- **Anti-Clipping & Inline CSS**: Total compiled HTML size MUST stay below 85 KB to prevent Gmail message clipping. All CSS styles MUST compile 100% inline without Base64 assets.
- **Multi-Provider Failover**: Route transactional emails through UnifiedEmailDispatcher supporting Listmonk, ZeptoMail, AWS SES v2, and Resend with stateful Circuit Breaker.
- **Rate-Limited Queueing**: Bulk marketing blasts MUST be throttled through BullMQ on Valkey 7.2 (limit: 10 emails/sec).
- **Brandbook Token Transpilation**: Load palette, font stacks, and SVG marks dynamically from brandbook.json via loadEmailBrandTokens().

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Multi-Provider Engine | Listmonk, ZeptoMail, AWS SES, Resend dispatcher | [`assets/email_dispatcher.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_dispatcher.ts) |
| Transactional Template | Polymorphic React Email 3.0 component (<85 KB) | [`assets/GenericTransactionalEmail.tsx`](file:///var/www/.agents/skills/email-marketing/assets/GenericTransactionalEmail.tsx) |
| Brandbook Bridge | Dynamic W3C DTCG design token transpiler | [`assets/email_brandbook_bridge.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_brandbook_bridge.ts) |
| Schemas & Contracts | Payload validation & webhook events schemas | [`assets/email_zod_schemas.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_zod_schemas.ts) |
| Throttled BullMQ Worker | Valkey queue consumer with rate limiting | [`assets/email_bullmq_worker.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_bullmq_worker.ts) |
| Usage & 4D Matrix | Deliverability guide, Bun SSR streaming & RFC 8058 | [`references/usage.md`](file:///var/www/.agents/skills/email-marketing/references/usage.md) |
| Topology & DNS | DMARCbis, MTA-STS, TLS-RPT, BIMI & SES v2 | [`references/infra.md`](file:///var/www/.agents/skills/email-marketing/references/infra.md) |
| Physical Validation | Universal capability sensor | `skills-suite-validate` |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/email-marketing/references/usage.md) — Multi-provider matrix, RFC 8058 POST receiver, and spam rate thresholds.
- [`references/infra.md`](file:///var/www/.agents/skills/email-marketing/references/infra.md) — DMARCbis RFC 9989, MTA-STS, TLS-RPT, BIMI, SES v2 Custom MAIL FROM, and Valkey topology.
- [`assets/GenericTransactionalEmail.tsx`](file:///var/www/.agents/skills/email-marketing/assets/GenericTransactionalEmail.tsx) — Agnostic transactional React Email template.
- [`assets/email_dispatcher.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_dispatcher.ts) — Multi-provider failover dispatcher with Circuit Breaker.
- [`assets/email_brandbook_bridge.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_brandbook_bridge.ts) — W3C DTCG design token transpiler.
- [`assets/email_bullmq_worker.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_bullmq_worker.ts) — Throttled BullMQ queue worker on Valkey.
- [`assets/email_zod_schemas.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_zod_schemas.ts) — Zod email validation schemas.
- `skills-suite-validate` — Universal physical capability sensor.
