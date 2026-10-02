# Payment Gateways Infrastructure & Environment Specification (v2.0)

## 1. Zerops Environment Variables Dictionary

All payment secrets MUST be configured as sensitive environment variables within Zerops project settings. Never commit secrets to Git.

| Variable Name | Required By | Description | Example / Format |
|---|---|---|---|
| `STRIPE_PUBLISHABLE_KEY` | Stripe | Public key for client-side Stripe Elements | `pk_live_...` |
| `STRIPE_SECRET_KEY` | Stripe | Private key for server-side PaymentIntents | `sk_live_...` |
| `STRIPE_WEBHOOK_SECRET` | Stripe | Endpoint secret for HMAC signature verification | `whsec_...` |
| `MERCADOPAGO_ACCESS_TOKEN` | Mercado Pago | Server-side REST API access token | `APP_USR-...` |
| `MERCADOPAGO_WEBHOOK_SECRET`| Mercado Pago | Secret for x-signature validation | `...` |
| `WOMPI_PUBLIC_KEY` | Wompi | Public merchant key for checkout widget | `pub_prod_...` |
| `WOMPI_PRIVATE_KEY` | Wompi | Private REST API key for transaction queries | `prv_prod_...` |
| `WOMPI_INTEGRITY_SECRET` | Wompi | Secret for checkout SHA-256 signature | `prod_integrity_...` |
| `WOMPI_EVENTS_SECRET` | Wompi | Secret for webhook event checksum verification | `prod_events_...` |
| `BOLD_IDENTITY_KEY` | Bold | Public merchant identity key | `...` |
| `BOLD_SECRET_KEY` | Bold | Secret key for webhook signature and integrity | `...` |
| `VALKEY_URL` / `$cache_connectionString` | Engine | Valkey 7.2 connection string for locks and OTPs | `valkey://...` |
| `NATS_URL` / `$nats_url` | Engine | NATS 2.12 connection string for event broadcasting | `nats://...` |

---

## 2. Ingress & Raw Body Preservation in Astro 5 SSR

Payment webhooks require verifying the exact cryptographic byte sequence sent by the gateway. If an intermediate proxy or framework parser mutates or parses the JSON payload, the SHA-256 / HMAC verification will fail.

### Cloudflare & Astro Ingress Rules:
1. **Bypass Caching**: Webhook routes (`/api/webhooks/*`) MUST bypass Cloudflare edge cache (`Cache-Control: no-store, private`).
2. **WAF Skip Rules**: Configure Cloudflare WAF Skip Rules for gateway IP ranges or verification endpoints to prevent false-positive challenge pages on webhook POSTs.
3. **Raw Body Access via Astro API Routes**: In Astro SSR routes (`src/pages/api/webhooks/[gateway].ts`), read the raw body buffer using `request.text()` or `request.arrayBuffer()`:
   ```typescript
   import type { APIRoute } from "astro";

   export const prerender = false;

   export const POST: APIRoute = async ({ request, params }) => {
     const rawBody = await request.text(); // Exact unparsed string
     const headers = Object.fromEntries(request.headers.entries());
     
     // Pass rawBody directly to cryptographic verification
     const event = await driver.verifyWebhook({ rawBody, headers });
     if (!event.isValid) {
       return new Response("Invalid signature", { status: 401 });
     }
     
     return new Response(JSON.stringify({ received: true }), {
       status: 200,
       headers: { "Content-Type": "application/json" }
     });
   };
   ```
