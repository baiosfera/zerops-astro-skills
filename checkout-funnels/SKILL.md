---
name: checkout-funnels
description: "Trigger: checkout-funnels, wompi integrity sha256, epayco sha256, dlocalgo latam, stripe checkout, mercadopago preference, 1 click upsell, cash on delivery cod, cart abandonment recovery, dane logistics, meta capi. High-converting multi-gateway checkout funnels with Wompi, ePayco, Stripe, COD OTP & Meta CAPI in Zerops."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `checkout-funnels` — High-Converting Multi-Gateway Checkout Engine (v2.0)

## Activation Contract
Activate when architecting, building, optimizing, or securing e-commerce checkout flows, payment gateway integrations (**Wompi**, **ePayco**, **dLocal Go**, **Stripe**, **Mercado Pago**), cryptographic signature validation (SHA-256 / HMAC), 1-Click post-purchase upsells, Cash on Delivery (COD) OTP verification, DANE logistics, or cart abandonment recovery in Zerops.

## Hard Rules
- **Multi-Gateway Decoupling**: Always decouple payment providers using `IPaymentGatewayProvider` to toggle between Wompi (Colombia), ePayco, dLocal Go (LatAm), Stripe (Global), and Mercado Pago without altering core order models.
- **Cryptographic Verification**: Every transaction webhook callback MUST be cryptographically verified (SHA-256 or HMAC-SHA256) before updating order status or stock.
- **Idempotency Locking**: All webhook handlers MUST acquire distributed locks in Valkey (`SET lock:tx:<id> 1 NX EX 3600`) to prevent duplicate processing.
- **COD OTP Verification**: Orders marked Cash on Delivery MUST verify a 6-digit WhatsApp OTP before warehouse shipping.
- **Fractal CoHaLo**: Enforce strict hygiene (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans (`manage_task action="kill"`), sensor (gateway ping test).
- **Zero Deletion**: Consult [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/checkout-funnels/references/infra.md) for full lossless APIs.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 4D Matrix & Comparison | Wompi vs ePayco, dLocal Go, Stripe, Mercado Pago, COD | [`references/usage.md#1-4d-comparative-architectural-matrix`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| Multi-Gateway Provider Strategy | Dynamic provider resolution from environment | [`references/usage.md#2-unified-payment-gateway-strategy-ipaymentgatewayprovider`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| Cryptographic Signatures | SHA-256 & HMAC formulas for all 5 gateways | [`references/usage.md#3-cryptographic-integrity-validation-formulas-by-gateway`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| 1-Click Post-Purchase Upsell | Tokenized card re-charge without re-entering CVV | [`references/usage.md#4-1-click-post-purchase-upsells--card-tokenization`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| DANE 8-Digit Logistics | Colombian city code validation (Coordinadora/Servientrega) | [`references/usage.md#5-colombian-logistics--dane-8-digit-normalization`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| Cash on Delivery (COD) OTP | 6-digit OTP generation and WhatsApp verification | [`references/usage.md#6-cash-on-delivery-cod-with-whatsapp-otp-verification`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| Meta Conversions API (CAPI) | Server-side Purchase event dispatch with SHA-256 hashing | [`references/usage.md#7-server-side-tracking-with-meta-conversions-api-capi`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| Console Onboarding Runbooks | Wompi, ePayco, dLocal Go, Stripe, Mercado Pago | [`references/infra.md#2-third-party-console-setup-runbooks`](file:///var/www/.agents/skills/checkout-funnels/references/infra.md) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/checkout-funnels-validate.sh`](file:///var/www/.agents/skills/checkout-funnels/scripts/checkout-funnels-validate.sh) |

## Execution Steps
1. Configure gateway credentials (`WOMPI_*`, `STRIPE_*`) in Zerops environment.
2. Instantiate `IPaymentGatewayProvider` in Astro Actions checkout handler.
3. Validate incoming webhook cryptographic signatures and acquire Valkey idempotency locks.
4. If COD is selected, trigger 6-digit WhatsApp OTP verification via Evolution Go.
5. Dispatch server-side `Purchase` event to Meta CAPI upon successful payment.
6. Verify gateway endpoints via physical sensor check.

## Output Contract
- Frictionless multi-gateway checkout running on Astro 5 SSR in Zerops.
- Verified cryptographic webhook validation, COD OTP workflows, and passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) — 4D matrix, gateway strategies, cryptographic formulas, DANE logistics, COD OTP, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/checkout-funnels/references/infra.md) — Environment variables dictionary, console runbooks, and CoHaLo harness.
- [`assets/checkout_funnels_production_recipes.json`](file:///var/www/.agents/skills/checkout-funnels/assets/checkout_funnels_production_recipes.json) — Signature calculators and Meta CAPI dispatchers.
- [`assets/payment_provider_interface.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/payment_provider_interface.ts) — Unified TypeScript provider interface for all 5 gateways.
- [`assets/gateways_validators.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/gateways_validators.ts) — Webhook signature validator functions.
- [`assets/abandoned_cart_bullmq_worker.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/abandoned_cart_bullmq_worker.ts) — BullMQ cart recovery worker.
- [`assets/astro_checkout_actions.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/astro_checkout_actions.ts) — Astro Actions checkout handler.
- [`scripts/checkout-funnels-validate.sh`](file:///var/www/.agents/skills/checkout-funnels/scripts/checkout-funnels-validate.sh) — Deterministic quality & token validation sensor.
