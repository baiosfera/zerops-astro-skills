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
Activate when implementing, securing, or auditing payment gateways (**Wompi**, **Bold**, **Stripe**, **COD with WhatsApp OTP**), cryptographic checksums (SHA-256 / HMAC), Server-to-Server webhooks, Valkey idempotency locking, or post-payment order settlement in Zerops.

## Hard Rules & Positive Guidance
- **Server-to-Server Webhook Authority**: NEVER rely on browser redirects (`/api/order/complete`) for definitive payment state. Cryptographically verified server webhooks are the sole authority for marking orders PAID.
- **Atomic Idempotency Locking**: Webhook handlers MUST acquire distributed locks in Valkey (`SET lock:order:${txId} 1 EX 60 NX`) before processing to prevent duplicate inventory deduction or double invoicing.
- **Cryptographic Signatures**:
  - **Wompi**: Checksum verification with integrity/events secrets.
  - **Stripe**: HMAC-SHA256 signature verification with webhook secret.
  - **Bold**: Checksum verification via secret key.
- **COD OTP**: COD orders MUST verify 6-digit WhatsApp OTP before advancing to fulfillment.
- **Strict Protection**: Gateway secrets MUST use environment variables and never expose to client bundles.
- **Fractal CoHaLo**: Strict timeouts (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans, sensor checks.

## Decision Gates

| Task | Action | Reference / Asset |
|---|---|---|
| Architecture | Unified driver & Valkey locks | [`references/usage.md`](file:///var/www/.agents/skills/payment-gateways/references/usage.md) |
| Wompi Colombia | SHA-256 integrity & checksum | [`references/gateways/wompi.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/wompi.md) |
| Stripe Global | Elements & HMAC verification | [`references/gateways/stripe.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/stripe.md) |
| Bold Colombia | Button & webhook verification | [`references/gateways/bold.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/bold.md) |
| COD WhatsApp | 6-digit OTP verification | [`references/gateways/cod.md`](file:///var/www/.agents/skills/payment-gateways/references/gateways/cod.md) |
| Environment | Credentials & ingress | [`references/infra.md`](file:///var/www/.agents/skills/payment-gateways/references/infra.md) |
| Recipes JSON | Webhooks & signature recipes | [`assets/payment_gateways_recipes.json`](file:///var/www/.agents/skills/payment-gateways/assets/payment_gateways_recipes.json) |
| TypeScript Driver | Production implementation | [`assets/payment_gateway_driver.ts`](file:///var/www/.agents/skills/payment-gateways/assets/payment_gateway_driver.ts) |
| Validation Sensor | Attest skill integrity | [`scripts/payment-gateways-validate.sh`](file:///var/www/.agents/skills/payment-gateways/scripts/payment-gateways-validate.sh) |

## Execution Steps
1. Configure gateway credentials in Zerops environment.
2. Initialize unified driver in Astro server actions.
3. Deploy Server-to-Server webhook route with cryptographic verification.
4. Acquire Valkey atomic lock to guarantee idempotency.
5. Publish `order.payment.settled` event to NATS JetStream upon payment approval.
6. Run physical sensor (`scripts/payment-gateways-validate.sh`) confirming exit code 0.

## Output Contract
- Zero-leak, cryptographically verified multi-gateway payment processing.
- Elimination of orphaned orders caused by client redirect failures.
