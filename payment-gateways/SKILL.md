---
name: payment-gateways
description: "Trigger: payment-gateways, wompi sha256, bold signature, stripe webhook, cod otp, valkey idempotency, server-to-server webhook, payment provider driver. Sovereign Payment Gateways, Cryptographic Webhook Validation & Idempotency Locking Engine in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# `payment-gateways` — Sovereign Payment Gateways & Cryptographic Engine (v2.1)

## Activation Contract
Activate when implementing, auditing, or configuring payment gateways (Stripe, Mercado Pago, Wompi, Bold, COD OTP), HMAC/SHA-256 signatures, Server-to-Server webhooks in Astro 5 SSR on Bun, Valkey distributed locking, or order settlement on Zerops.

## Hard Rules & Positive Guidance
- **Server Webhook Authority**: Verified server-to-server webhooks are the sole authority for marking orders PAID; client redirects represent pending intents only.
- **Astro APIRoute Raw Body**: Webhook handlers must use Astro API routes (`APIRoute`) with unparsed `request.text()` to preserve the raw byte stream required for signature verification.
- **Valkey 7.2 Distributed Locking**: Webhook handlers must acquire locks with unique owner UUIDs (`SET lock:payment:${txId} ${token} NX EX 60`) and release exclusively via atomic Lua scripts.
- **Pluggable Provider SPI**: Implement drivers under `IPaymentGatewayProvider` supporting session creation, webhook verification, and status queries.
- **ISO-4217 Minor Units**: Calculate and transmit monetary amounts in integer minor units (cents) per ISO-4217 exponents.
- **Zero Socket Leak Invariant**: Use stateless `pool.query()` or wrap transactions with strict `try/finally` client release. Never hold dedicated database checkouts while awaiting external gateway HTTP responses.
- **Credential Protection**: Inject gateway API keys and webhook secrets via Zerops environment variables; never expose private credentials in client bundles.

## Decision Gates

| Task | Strategy | Reference |
|---|---|---|
| Complete Usage Guide | Unified SPI, atomic Lua locks & event mesh | [`references/usage.md`](file:///var/www/.agents/skills/payment-gateways/references/usage.md) |
| Wompi Colombia | SHA-256 integrity & checksum validation | [`references/gateways/wompi.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/wompi.md) |
| Stripe Global | Payment Elements & HMAC signature verification | [`references/gateways/stripe.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/stripe.md) |
| Bold Colombia | Checkout button & webhook verification | [`references/gateways/bold.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/bold.md) |
| dLocal Go LatAm | Dynamic sandbox/live & webhook authority | [`references/gateways/dlocal_go.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/dlocal_go.md) |
| COD WhatsApp | 6-digit WhatsApp OTP state machine | [`references/gateways/cod.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/cod.md) |
| Zerops & APIRoute Infra | Raw body preservation, ingress & env vars | [`references/infra.md`](file:///var/www/.agents/skills/payment-gateways/references/infra.md) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/payment-gateways/references/usage.md) — Unified driver SPI, atomic Lua locking, and JetStream order settlement.
- [`references/infra.md`](file:///var/www/.agents/skills/payment-gateways/references/infra.md) — APIRoute raw body handling, Valkey lock configuration, and secret management.
