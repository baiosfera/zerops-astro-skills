# Payment Gateways Infrastructure & Environment Specification (v1.0)

## 1. Zerops Environment Variables Dictionary

All payment secrets MUST be configured as sensitive environment variables within Zerops project settings. Never commit secrets to Git.

| Variable Name | Required By | Description | Example / Format |
|---|---|---|---|
| `WOMPI_PUBLIC_KEY` | Wompi | Public merchant key for checkout widget | `pub_prod_...` |
| `WOMPI_PRIVATE_KEY` | Wompi | Private REST API key for transaction queries | `prv_prod_...` |
| `WOMPI_INTEGRITY_SECRET` | Wompi | Secret for checkout SHA-256 signature | `prod_integrity_...` |
| `WOMPI_EVENTS_SECRET` | Wompi | Secret for webhook event checksum verification | `prod_events_...` |
| `STRIPE_PUBLISHABLE_KEY` | Stripe | Public key for client-side Stripe Elements | `pk_live_...` |
| `STRIPE_SECRET_KEY` | Stripe | Private key for server-side PaymentIntents | `sk_live_...` |
| `STRIPE_WEBHOOK_SECRET` | Stripe | Endpoint secret for HMAC signature verification | `whsec_...` |
| `BOLD_IDENTITY_KEY` | Bold | Public merchant identity key | `...` |
| `BOLD_SECRET_KEY` | Bold | Secret key for webhook signature and integrity | `...` |
| `VALKEY_URL` / `$cache_connectionString` | Engine | Valkey connection string for locks and OTPs | `valkey://...` |
| `NATS_URL` / `$nats_url` | Engine | NATS connection string for event broadcasting | `nats://...` |

---

## 2. Ingress & Raw Body Preservation

Payment webhooks require verifying the exact cryptographic byte sequence sent by the gateway. If an intermediate proxy or framework parser mutates or parses the JSON payload, the SHA-256 / HMAC verification will fail.

### Cloudflare & Astro Ingress Rules:
1. **Bypass Caching**: Webhook routes (`/api/webhooks/*`) MUST bypass Cloudflare cache (`Cache-Control: no-store, private`).
2. **Raw Body Access**: In Astro SSR routes, read the raw body buffer before parsing:
   ```typescript
   export const POST: APIRoute = async ({ request }) => {
     const rawBody = await request.text(); // Exact unparsed string
     // ... pass rawBody to verification function
   };
   ```
