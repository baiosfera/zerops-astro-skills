---
name: checkout-funnels
description: "Trigger: checkout-funnels, wompi integrity sha256, epayco sha256, dlocalgo latam, stripe checkout, mercadopago preference, 1 click upsell, cash on delivery cod, cart abandonment recovery, dane logistics, meta capi. High-converting multi-gateway checkout funnels with Wompi, ePayco, Stripe, COD OTP & Meta CAPI in Zerops."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "3.1"
---

# `checkout-funnels` — Checkout & Conversion Engine (v3.1)

## Activation Contract
Activate when architecting, building, or auditing multi-gateway checkout funnels (Wompi, ePayco, dLocal Go, Stripe, Mercado Pago), 1-Click upsells, COD OTP verification, shipping carrier SPIs, address geocoding, or Meta Conversions API (CAPI) on Zerops.

## Hard Rules & Positive Guidance
- **Multi-Gateway Decoupling**: Decouple gateway providers via `IPaymentGatewayProvider` without altering core order schemas.
- **Cryptographic Verification**: Verify webhook signatures cryptographically (SHA-256 / HMAC) before updating order states.
- **Idempotency Locking**: Acquire distributed locks in Valkey (`SET lock:tx:<id> 1 NX EX 3600`) to guarantee single-execution idempotency on webhooks.
- **Pluggable Logistics SPI**: Abstract carrier rates and address validation via `IShippingCarrierProvider` and `IAddressValidator` SPIs.
- **1-Click Upsell Protocol**: Process post-purchase upsells off-session using tokenized payment instruments with 3DS step-up handling.
- **Hardened COD OTP**: Verify secure 6-digit WhatsApp OTPs using `crypto.randomInt`, Valkey rate limiters, and timing-safe equality checks.
- **Dual-Tagging & Meta CAPI**: Emit browser and server `Purchase` events to Meta Conversions API v21.0 with shared `event_id` deduplication.
- **Connection Isolation**: Use stateless `pool.query()` exclusively for reads and single queries in checkout endpoints. Intercept database exhaustion errors (SQLSTATE `53300`) and return user-friendly HTTP 503 retryable responses.

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Architecture Matrix | 4D comparative checkout matrix | [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| Provider SPI | Dynamic payment gateway resolution | [`assets/payment_provider_interface.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/payment_provider_interface.ts) |
| Signatures | SHA-256 & HMAC formula library | [`assets/gateways_validators.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/gateways_validators.ts) |
| 1-Click Upsell | Tokenized re-authorization actions | [`assets/astro_checkout_actions.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/astro_checkout_actions.ts) |
| Shipping Rates | Multi-carrier rate shopping SPI | [`assets/shipping_carrier_provider.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/shipping_carrier_provider.ts) |
| Addresses | International & DANE Divipola normalization | [`assets/address_validator.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/address_validator.ts) |
| COD OTP | Valkey OTP state machine & WhatsApp | [`assets/cod_otp_manager.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/cod_otp_manager.ts) |
| Cart Recovery | BullMQ abandonment queue workers | [`assets/abandoned_cart_bullmq_worker.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/abandoned_cart_bullmq_worker.ts) |
| Infrastructure | Multi-service Zerops deployment | [`references/infra.md`](file:///var/www/.agents/skills/checkout-funnels/references/infra.md) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) — Checkout architecture, gateway drivers, signature validation, and CAPI.
- [`references/infra.md`](file:///var/www/.agents/skills/checkout-funnels/references/infra.md) — Multi-service topology, Valkey idempotency, and carrier logistics.
