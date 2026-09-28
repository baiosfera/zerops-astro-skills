# Stripe Global Driver Specification (v1.0)

## 1. Overview & Credentials
Stripe serves as the international payment gateway for cross-border credit/debit card transactions and digital wallets (Apple Pay, Google Pay).

### Required Environment Variables:
- `STRIPE_PUBLISHABLE_KEY`: `pk_live_...` or `pk_test_...`
- `STRIPE_SECRET_KEY`: `$STRIPE_SECRET_KEY (from Stripe Dashboard)`
- `STRIPE_WEBHOOK_SECRET`: `whsec_...`

---

## 2. Server-Side Webhook Verification (HMAC-SHA256)
Stripe passes a `stripe-signature` header containing timestamp `t` and signatures `v1`.

### Verification Algorithm:
```typescript
import crypto from "node:crypto";

export function verifyStripeWebhookSignature(
  rawBody: string | Buffer,
  signatureHeader: string,
  webhookSecret: string,
  toleranceSeconds: number = 300
): boolean {
  if (!signatureHeader) return false;

  const elements = signatureHeader.split(",");
  let timestamp = -1;
  const signatures: string[] = [];

  for (const element of elements) {
    const [key, value] = element.split("=");
    if (key === "t") timestamp = parseInt(value, 10);
    if (key === "v1") signatures.push(value);
  }

  if (timestamp === -1 || signatures.length === 0) return false;

  // Replay attack prevention
  const now = Math.floor(Date.now() / 1000);
  if (now - timestamp > toleranceSeconds) return false;

  const payloadString = typeof rawBody === "string" ? rawBody : rawBody.toString("utf8");
  const signedPayload = `${timestamp}.${payloadString}`;

  const expectedSignature = crypto
    .createHmac("sha256", webhookSecret)
    .update(signedPayload)
    .digest("hex");

  for (const sig of signatures) {
    if (sig.length === expectedSignature.length &&
        crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expectedSignature))) {
      return true;
    }
  }

  return false;
}
```

---

## 3. Webhook Event Routing
- `checkout.session.completed` / `payment_intent.succeeded`: Transition order to `paid`, emit `order.payment.settled`.
- `payment_intent.payment_failed`: Transition order to `payment_failed`, emit `order.payment.failed`.
