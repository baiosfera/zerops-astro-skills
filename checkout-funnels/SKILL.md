---
name: checkout-funnels
description: "Trigger: checkout-funnels, wompi integrity sha256, epayco sha256, dlocalgo latam, stripe checkout, mercadopago preference, 1 click upsell, cash on delivery cod, cart abandonment recovery, dane logistics, meta capi. High-converting multi-gateway checkout funnels with Wompi, ePayco, Stripe, COD OTP & Meta CAPI in Zerops."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "3.0"
---

# `checkout-funnels` — Checkout & Conversion Engine (v3.0)

## Activation Contract
Architecting checkout funnels, payment gateways (**Wompi**, **ePayco**, **dLocal Go**, **Stripe**, **Mercado Pago**), signatures, 1-Click upsells, COD OTP verification, shipping carrier SPIs, or Meta CAPI in Zerops.

## Hard Rules & Positive Guidance
- **Multi-Gateway Decoupling**: Decouple providers via `IPaymentGatewayProvider` without altering core order schemas.
- **Cryptographic Verification**: Webhooks MUST be cryptographically verified (SHA-256/HMAC) before mutating orders.
- **Idempotency Locking**: Webhooks acquire distributed locks in Valkey (`SET lock:tx:<id> 1 NX EX 3600`) to guarantee single execution.
- **Pluggable Logistics SPI**: Abstract carrier rates and address validation via `IShippingCarrierProvider` and `IAddressValidator` SPIs.
- **1-Click Upsell Protocol**: Process post-purchase upsells off-session using tokenized instruments with 3DS step-up handling.
- **Hardened COD OTP**: Verify secure 6-digit WhatsApp OTPs (`crypto.randomInt`, Valkey rate limits, timing-safe equality).
- **Dual-Tagging & CAPI**: Emit browser and server `Purchase` events to Meta CAPI v21.0 with shared `event_id` deduplication.
- **Process Hygiene**: Bound CLI commands (`timeout 10s`) and verify state with deterministic physical sensors.

## Decision Gates

| Objective | Protocol | Reference |
|---|---|---|
| Architecture | 4D comparative matrix | [`usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) |
| Provider SPI | Dynamic gateway resolution | [`payment_provider_interface.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/payment_provider_interface.ts) |
| Signatures | SHA-256 & HMAC formulas | [`gateways_validators.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/gateways_validators.ts) |
| 1-Click Upsell | Tokenized re-authorization | [`astro_checkout_actions.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/astro_checkout_actions.ts) |
| Shipping Rates | Multi-carrier rate shopping | [`shipping_carrier_provider.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/shipping_carrier_provider.ts) |
| Addresses | International & DANE Divipola | [`address_validator.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/address_validator.ts) |
| COD OTP | Valkey OTP state machine | [`cod_otp_manager.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/cod_otp_manager.ts) |
| Cart Recovery | BullMQ abandonment queue | [`abandoned_cart_bullmq_worker.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/abandoned_cart_bullmq_worker.ts) |
| Topology | Multi-service Zerops infra | [`infra.md`](file:///var/www/.agents/skills/checkout-funnels/references/infra.md) |
| Validation | Deterministic sensor | [`checkout-funnels-validate.sh`](file:///var/www/.agents/skills/checkout-funnels/scripts/checkout-funnels-validate.sh) |

## Execution Steps
1. Configure gateway credentials and Valkey strings in Zerops.
2. Instantiate `IPaymentGatewayProvider` in Astro Actions.
3. Verify signatures and acquire distributed idempotency locks.
4. Normalize addresses via `IAddressValidator` and quote carrier rates.
5. Verify COD orders with 6-digit WhatsApp OTPs via `CodOtpManager`.
6. Dispatch `Purchase` events to Meta Conversions API v21.0.
7. Verify contracts via `scripts/checkout-funnels-validate.sh`.

## Output Contract
- High-converting checkout running on Astro 5 SSR in Zerops.
- Verified webhooks, COD OTP workflows, passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/checkout-funnels/references/usage.md) — 4D matrix, gateway strategies, and COD OTP.
- [`references/infra.md`](file:///var/www/.agents/skills/checkout-funnels/references/infra.md) — Topology, environment variables, and runbooks.
- [`assets/checkout_funnels_production_recipes.json`](file:///var/www/.agents/skills/checkout-funnels/assets/checkout_funnels_production_recipes.json) — Production recipes.
- [`assets/payment_provider_interface.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/payment_provider_interface.ts) — Gateway provider SPI.
- [`assets/gateways_validators.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/gateways_validators.ts) — Signature validator functions.
- [`assets/abandoned_cart_bullmq_worker.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/abandoned_cart_bullmq_worker.ts) — BullMQ cart recovery.
- [`assets/astro_checkout_actions.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/astro_checkout_actions.ts) — Astro Actions checkout handler.
- [`assets/shipping_carrier_provider.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/shipping_carrier_provider.ts) — Shipping carrier SPI.
- [`assets/address_validator.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/address_validator.ts) — Address validators.
- [`assets/cod_otp_manager.ts`](file:///var/www/.agents/skills/checkout-funnels/assets/cod_otp_manager.ts) — Hardened COD OTP manager.
- [`scripts/checkout-funnels-validate.sh`](file:///var/www/.agents/skills/checkout-funnels/scripts/checkout-funnels-validate.sh) — Quality sensor.
