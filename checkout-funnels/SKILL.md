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
Activate when architecting, building, or securing checkout flows, payment gateways (**Wompi**, **ePayco**, **dLocal Go**, **Stripe**, **Mercado Pago**), cryptographic signatures (SHA-256/HMAC), 1-Click upsells, COD OTP verification, DANE logistics, or cart recovery in Zerops.

## Hard Rules
- **Multi-Gateway Decoupling**: Decouple providers via `IPaymentGatewayProvider` to toggle Wompi, ePayco, dLocal Go, Stripe, and Mercado Pago without altering order models.
- **Cryptographic Verification**: Webhooks MUST be cryptographically verified (SHA-256 or HMAC-SHA256) before updating order status or stock.
- **Idempotency Locking**: Webhooks acquire distributed locks in Valkey (`SET lock:tx:<id> 1 NX EX 3600`) to prevent duplicate processing.
- **COD OTP Verification**: Cash on Delivery orders MUST verify 6-digit WhatsApp OTP before warehouse shipping.
- **Fractal CoHaLo**: Strict timeouts (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans, sensor checks.
- **Zero Deletion**: Refer to [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/checkout-funnels/references/infra.md) for full APIs.

## Decision Gates

| Objective | Protocol | Reference / Asset |
|---|---|---|
| Matrix & Comparison | Gateway feature matrix | [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| Provider Strategy | Dynamic provider resolution | [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| Cryptographic Signatures | SHA-256 & HMAC formulas | [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| 1-Click Upsell | Tokenized card re-charge | [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| DANE Logistics | 8-digit city normalization | [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| COD OTP | 6-digit WhatsApp OTP | [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| Meta CAPI | Server-side Purchase event | [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| Onboarding Runbooks | Gateway console guides | [`references/infra.md`](file:///var/www/.agents/skills/checkout-funnels/references/infra.md) |
| Validation Sensor | Skill integrity verification | [`scripts/checkout-funnels-validate.sh`](file:///var/www/.agents/skills/checkout-funnels/scripts/checkout-funnels-validate.sh) |

## Execution Steps
1. Set gateway credentials in Zerops environment.
2. Instantiate `IPaymentGatewayProvider` in Astro Actions.
3. Verify webhook signatures and acquire Valkey idempotency locks.
4. For COD orders, verify 6-digit WhatsApp OTP via Evolution Go.
5. Dispatch server-side `Purchase` event to Meta CAPI.
6. Verify gateway endpoints via physical sensor check.

## Output Contract
- High-converting multi-gateway checkout running on Astro 5 SSR in Zerops.
- Cryptographically verified webhooks, COD OTP workflows, passing physical sensors.

## References & Assets
- [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) — 4D matrix, gateway strategies, cryptographic formulas, DANE logistics, COD OTP.
- [`references/infra.md`](file:///var/www/.agents/skills/checkout-funnels/references/infra.md) — Environment variables dictionary, console runbooks, and CoHaLo harness.
- [`assets/checkout_funnels_production_recipes.json`](file:///var/www/.agents/skills/checkout-funnels/assets/checkout_funnels_production_recipes.json) — Signature calculators and Meta CAPI dispatchers.
- [`assets/payment_provider_interface.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/payment_provider_interface.ts) — Unified TypeScript provider interface for all 5 gateways.
- [`assets/gateways_validators.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/gateways_validators.ts) — Webhook signature validator functions.
- [`assets/abandoned_cart_bullmq_worker.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/abandoned_cart_bullmq_worker.ts) — BullMQ cart recovery worker.
- [`assets/astro_checkout_actions.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/astro_checkout_actions.ts) — Astro Actions checkout handler.
- [`scripts/checkout-funnels-validate.sh`](file:///var/www/.agents/skills/checkout-funnels/scripts/checkout-funnels-validate.sh) — Deterministic quality & token validation sensor.
