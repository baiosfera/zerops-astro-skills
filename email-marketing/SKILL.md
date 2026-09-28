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
Activate when designing, sending, or automating email flows, transactional emails, React Email 3.0 templates, deliverability (**DMARCbis RFC 9989**, **DKIM 2048**, **SPF**, **RFC 8058 One-Click**, **Spam Rate < 0.10%**), Zoho ZeptoMail, Amazon SES v2, Resend, Listmonk, `brandbook.json` token transpilation, or SMTP dispatchers on Valkey 7.2 and Directus 11+.

## Hard Rules
- **RFC 8058 One-Click**: Marketing emails MUST include `List-Unsubscribe` and `List-Unsubscribe-Post: List-Unsubscribe=One-Click` headers signed under DKIM.
- **DMARCbis & Spam Rates**: Maintain 2048-bit DKIM keys and `p=quarantine`/`p=reject` DMARC. Keep spam complaints below **0.10%** in Google Postmaster.
- **`brandbook.json` SSoT**: Transpile colors, SVG marks, and progressive font stacks directly from `brandbook.json`.
- **Anti-Clipping & Inline CSS**: HTML size MUST NOT exceed **85 KB** (Gmail limit). All styles MUST compile inline. Zero Base64 in HTML/CSS.
- **Language Resguard**: Include `<meta name="google" content="notranslate" />` and `<html lang="es" translate="no" class="notranslate">`.
- **Queue Throttling**: Broadcasts MUST be throttled through BullMQ on Valkey 7.2 (`10 emails/sec`).
- **Fractal CoHaLo**: Enforce hygiene (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans (`manage_task action="kill"`), sensor (relay ping probe).
- **Zero Deletion**: Consult [`references/usage.md`](file:///var/www/.agents/skills/email-marketing/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/email-marketing/references/infra.md) for full lossless APIs.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 4D Matrix & Relays | ZeptoMail vs AWS SES v2, Resend, Listmonk, SMTP | [`references/usage.md#1-4d-comparative-architectural-matrix-email-relays--providers`](file:///var/www/.agents/skills/email-marketing/references/usage.md) |
| Brandbook Bridge | Transpile colors, fonts & monogram from brandbook.json | [`references/usage.md#2-deterministic-connection-with-brandbookjson-w3c-dtcg-ssot`](file:///var/www/.agents/skills/email-marketing/references/usage.md) |
| HTML Hygiene | Gmail 102 KB limit, CSS inline, no Base64 | [`references/usage.md#3-html-hygiene--email-rendering-invariants`](file:///var/www/.agents/skills/email-marketing/references/usage.md) |
| Anti-SPAM Compliance | DMARCbis RFC 9989, DKIM 2048, spam rate < 0.10% | [`references/usage.md#6-2026-deliverability--anti-spam-compliance-standards`](file:///var/www/.agents/skills/email-marketing/references/usage.md) |
| NATS Consumer | Reactive email delivery on purchase/magic link | [`references/usage.md#7-nats-jetstream-event-consumer-for-reactive-emails`](file:///var/www/.agents/skills/email-marketing/references/usage.md) |
| Multi-Service Topology | Connect Directus, NATS, Valkey BullMQ, and Relays | [`references/infra.md#1-multi-service-email-dispatch-topology-in-zerops`](file:///var/www/.agents/skills/email-marketing/references/infra.md) |
| DNS Setup Runbooks | Amazon SES v2 and Zoho ZeptoMail DKIM/SPF setup | [`references/infra.md#4-third-party-console-setup-runbooks`](file:///var/www/.agents/skills/email-marketing/references/infra.md) |
| BullMQ Worker Asset | Rate-limited worker on Valkey 7.2 (10 emails/sec) | [`assets/email_bullmq_worker.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_bullmq_worker.ts) |
| Production Recipes JSON | Dispatcher and NATS listener recipes | [`assets/email_marketing_production_recipes.json`](file:///var/www/.agents/skills/email-marketing/assets/email_marketing_production_recipes.json) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/email-marketing-validate.sh`](file:///var/www/.agents/skills/email-marketing/scripts/email-marketing-validate.sh) |

## Execution Steps
1. Configure relay credentials in Zerops environment.
2. Verify DNS records (SPF, DKIM 2048, DMARCbis RFC 9989).
3. Transpile tokens from `brandbook.json` and compile React Email template.
4. Launch BullMQ rate-limited worker and NATS consumer.
5. Verify relay connectivity via physical sensor check.

## Output Contract
- High-deliverability multi-provider email engine running on Zerops.
- Validated RFC 8058 headers, anti-clipping compliant HTML, and passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/email-marketing/references/usage.md) — 4D matrix, brandbook bridge, HTML hygiene, deliverability, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/email-marketing/references/infra.md) — Multi-service topology, DNS standards, console runbooks, and CoHaLo harness.
- [`assets/email_marketing_production_recipes.json`](file:///var/www/.agents/skills/email-marketing/assets/email_marketing_production_recipes.json) — Production dispatchers and NATS consumer recipes.
- [`assets/email_brandbook_bridge.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_brandbook_bridge.ts) — SSoT bridge connecting `brandbook.json` with inline email tokens.
- [`assets/WelcomeLatAmEmail.tsx`](file:///var/www/.agents/skills/email-marketing/assets/WelcomeLatAmEmail.tsx) — React Email 3.0 responsive template component.
- [`assets/email_dispatcher.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_dispatcher.ts) — Unified TypeScript sending service with multi-provider strategy.
- [`assets/email_bullmq_worker.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_bullmq_worker.ts) — Rate-limited BullMQ worker on Valkey 7.2.
- [`assets/email_zod_schemas.ts`](file:///var/www/.agents/skills/email-marketing/assets/email_zod_schemas.ts) — Strict Zod validation schemas for email payloads.
- [`scripts/email-marketing-validate.sh`](file:///var/www/.agents/skills/email-marketing/scripts/email-marketing-validate.sh) — Deterministic quality & token validation sensor.
