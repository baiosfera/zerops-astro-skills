---
name: payment-gateways
description: "Trigger: payment-gateways, wompi sha256, bold signature, stripe webhook, cod otp, valkey idempotency, server-to-server webhook, payment provider driver. Sovereign Payment Gateways, Cryptographic Webhook Validation & Idempotency Locking Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `payment-gateways` — Sovereign Payment Gateways & Cryptographic Engine (v2.0)

## Activation Contract
Activate when implementing or auditing payment gateways (**Stripe**, **Mercado Pago**, **Wompi**, **Bold**, **COD OTP**), HMAC/SHA-256 signatures, Server-to-Server webhooks in Astro 5 SSR on Bun, Valkey distributed locking, or order settlement in Zerops.

## Hard Rules & Positive Guidance
- **Server Webhook Authority**: Verified server webhooks are the sole authority for marking orders PAID; client redirects represent pending intents only.
- **Astro APIRoute Raw Body**: Webhooks MUST use Astro API routes (`APIRoute`) with unparsed `request.text()`. Astro Actions destroy raw byte streams required for signatures.
- **Valkey 7.2 Distributed Locking**: Webhook handlers MUST acquire locks with unique owner UUIDs (`SET lock:payment:${txId} ${token} NX EX 60`) and release exclusively via atomic Lua scripts.
- **Pluggable Provider SPI**: Implement drivers under `IPaymentGatewayProvider` supporting session creation, webhook verification, and status queries.
- **ISO-4217 Minor Units**: Calculate and pass monetary values in integer minor units (cents) per ISO-4217 exponents.
- **Zero Secret Exposure**: Gateway secrets MUST reside in Zerops environment variables and never reach client bundles.

## Decision Gates

| Task | Action | Reference / Asset |
|---|---|---|
| Complete Usage Guide | Unified SPI, atomic Lua locks & event mesh | [`references/usage.md`](file:///var/www/.agents/skills/payment-gateways/references/usage.md) |
| Wompi Colombia | SHA-256 integrity & checksum | [`references/gateways/wompi.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/wompi.md) |
| Stripe Global | Elements & HMAC verification | [`references/gateways/stripe.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/stripe.md) |
| Bold Colombia | Button & webhook verification | [`references/gateways/bold.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/bold.md) |
| dLocal Go LatAm | Dynamic sandbox/live & webhook authority | [`references/gateways/dlocal_go.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/dlocal_go.md) |
| COD WhatsApp | 6-digit OTP verification | [`references/gateways/cod.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/cod.md) |
| Zerops & APIRoute Infra | Raw body preservation, ingress & env vars | [`references/infra.md`](file:///var/www/.agents/skills/payment-gateways/references/infra.md) |
| Valkey Distributed Lock | Atomic Lua acquisition and safe release | [`assets/valkey_lock.ts`](file:///var/www/.agents/skills/payment-gateways/assets/valkey_lock.ts) |
| Unified Drivers SDK | Production drivers (Stripe, Wompi, Bold, MP, COD) | [`assets/payment_gateway_driver.ts`](file:///var/www/.agents/skills/payment-gateways/assets/payment_gateway_driver.ts) |
| Production Recipes | Gateway configurations and webhook payloads | [`assets/payment_gateways_recipes.json`](file:///var/www/.agents/skills/payment-gateways/assets/payment_gateways_recipes.json) |
| Physical Validation Sensor | Attest AST, HMAC vectors & lock math | [`scripts/payment-gateways-validate.sh`](file:///var/www/.agents/skills/payment-gateways/scripts/payment-gateways-validate.sh) |

## Execution Steps
1. Inject gateway secrets into Zerops environment variables.
2. Initialize `PaymentProviderRegistry` with target gateway drivers.
3. Deploy Astro API Route (`export const POST: APIRoute`) reading unparsed raw request body.
4. Verify cryptographic webhook signature using timing-safe comparisons.
5. Acquire atomic Valkey distributed lock with unique owner token.
6. Settle order in database and publish `order.payment.settled` to NATS JetStream.
7. Atomically release Valkey lock via Lua script and return HTTP 200.
8. Verify skill integrity via physical validator (`scripts/payment-gateways-validate.sh`).

## Output Contract
- Zero-leak, cryptographically verified multi-gateway payment processing.
- Race-condition-free distributed order settlement passing all physical tests (Exit 0).
