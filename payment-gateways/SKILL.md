---
name: payment-gateways
description: "Trigger: payment-gateways, wompi sha256, bold signature, stripe webhook, cod otp, valkey idempotency, server-to-server webhook, payment provider driver. Sovereign Payment Gateways, Cryptographic Webhook Validation & Idempotency Locking Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `payment-gateways` — Sovereign Payment Gateways & Cryptographic Webhook Engine (v1.0)

## Activation Contract
Activate when implementing, securing, or auditing payment gateway integrations (**Wompi**, **Bold**, **Stripe**, **Cash on Delivery with WhatsApp OTP**), cryptographic integrity calculation (SHA-256 / HMAC), Server-to-Server webhook handlers, distributed idempotency locking in Valkey, or post-payment order settlement in Zerops.

## Hard Rules & Positive Guidance
- **Server-to-Server Webhook Authority**: NEVER rely on browser redirect callbacks (`/api/order/complete`) as the definitive payment state. Client redirects are UX-only; server-to-server webhooks with cryptographic validation are the sole authoritative source for marking orders as PAID.
- **Atomic Idempotency Locking**: All webhook handlers MUST acquire a distributed atomic lock in Valkey (`SET lock:order:${transactionId} 1 EX 60 NX`) before processing. Reject or acknowledge concurrent attempts to prevent duplicate inventory deductions or double invoicing.
- **Cryptographic Integrity Signatures**:
  - **Wompi Checkout**: `SHA256(reference + amountInCents + currency + integritySecret)`.
  - **Wompi Webhook**: Concatenate property values defined in `signature.properties` + `timestamp` + `eventsSecret`, then verify against `signature.checksum`.
  - **Stripe**: Verify `stripe-signature` header with HMAC-SHA256 using `endpointSecret`.
- **Cash on Delivery (COD) OTP**: COD orders MUST verify a 6-digit WhatsApp OTP delivered via NATS (`events.whatsapp.otp`) before advancing to warehouse fulfillment (`orders-fulfillment`).
- **Strict Credential Protection**: Gateway secrets (`$WOMPI_INTEGRITY_SECRET`, `$WOMPI_EVENTS_SECRET`, `$STRIPE_WEBHOOK_SECRET`) MUST be referenced via environment variables and never logged or exposed in client bundles.
- **Fractal CoHaLo Execution**: Enforce command timeouts (`timeout 10s`), wait limits (`WaitMsBeforeAsync: 10000`), zero orphan tasks, and sensor attestation.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Gateway Architecture | Unified driver pattern (`PaymentGatewayDriver`) and lifecycles | [`references/usage.md#1-unified-payment-gateway-driver-architecture`](file:///var/www/.agents/skills/payment-gateways/references/usage.md) |
| Valkey Idempotency | Distributed atomic locking and state synchronization | [`references/usage.md#2-distributed-idempotency-locking-in-valkey`](file:///var/www/.agents/skills/payment-gateways/references/usage.md) |
| Wompi Colombia Driver | SHA-256 integrity signature and webhook event checksum | [`references/gateways/wompi.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/wompi.md) |
| Stripe Global Driver | Stripe Elements, PaymentIntents and HMAC signature verification | [`references/gateways/stripe.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/stripe.md) |
| Bold Colombia Driver | Bold payment button and encrypted webhook verification | [`references/gateways/bold.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/bold.md) |
| COD WhatsApp OTP | 6-digit OTP generation, Valkey TTL, and phone verification | [`references/gateways/cod.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/cod.md) |
| Environment & Secrets | Secure credentials dictionary and webhook endpoint topology | [`references/infra.md`](file:///var/www/.agents/skills/payment-gateways/references/infra.md) |
| Production Recipes JSON | Webhook route templates and signature calculation scripts | [`assets/payment_gateways_recipes.json`](file:///var/www/.agents/skills/payment-gateways/assets/payment_gateways_recipes.json) |
| TypeScript Driver Code | Lossless production implementation of all gateway drivers | [`assets/payment_gateway_driver.ts`](file:///var/www/.agents/skills/payment-gateways/assets/payment_gateway_driver.ts) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/payment-gateways-validate.sh`](file:///var/www/.agents/skills/payment-gateways/scripts/payment-gateways-validate.sh) |

## Execution Steps
1. Configure gateway credentials (`WOMPI_*`, `STRIPE_*`, `BOLD_*`) in Zerops environment.
2. Initialize unified driver in Astro server actions (`/api/checkout/session`).
3. Deploy Server-to-Server webhook route (`/api/webhooks/[gateway]`) with cryptographic checksum verification.
4. Acquire Valkey atomic lock (`lock:order:${id}`) to guarantee idempotency.
5. Publish `order.payment.settled` event to NATS JetStream upon valid payment approval.
6. Run physical sensor (`scripts/payment-gateways-validate.sh`) confirming exit code 0.

## Output Contract
- Zero-leak, cryptographically verified multi-gateway payment processing.
- Elimination of orphaned orders caused by client redirect failures.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/payment-gateways/references/usage.md) — Unified driver architecture and Valkey idempotency workflows.
- [`references/infra.md`](file:///var/www/.agents/skills/payment-gateways/references/infra.md) — Environment variables, Zerops network isolation, and webhooks ingress.
- [`references/gateways/wompi.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/wompi.md) — Wompi SHA-256 integrity and event checksum verification.
- [`references/gateways/stripe.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/stripe.md) — Stripe Elements and HMAC webhook verification.
- [`references/gateways/bold.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/bold.md) — Bold Colombia integration and signature checking.
- [`references/gateways/cod.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/cod.md) — Cash on Delivery with WhatsApp OTP verification flow.
- [`assets/payment_gateways_recipes.json`](file:///var/www/.agents/skills/payment-gateways/assets/payment_gateways_recipes.json) — Production webhook routes and config templates.
- [`assets/payment_gateway_driver.ts`](file:///var/www/.agents/skills/payment-gateways/assets/payment_gateway_driver.ts) — TypeScript production driver implementation.
- [`scripts/payment-gateways-validate.sh`](file:///var/www/.agents/skills/payment-gateways/scripts/payment-gateways-validate.sh) — Deterministic quality & token validation sensor.
