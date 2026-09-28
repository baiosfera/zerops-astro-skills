# Bold Colombia Driver Specification (v1.0)

## 1. Overview & Credentials
Bold is a major Colombian payment provider offering checkout links, payment buttons, and direct credit card / PSE acquiring.

### Required Environment Variables:
- `BOLD_IDENTITY_KEY`: Public identity key for iframe/redirect button.
- `BOLD_SECRET_KEY`: Private secret key for integrity signing and webhook verification.

---

## 2. Integrity Signature Calculation
Bold requires an integrity hash to prevent transaction parameter tampering:

```typescript
import crypto from "node:crypto";

export function generateBoldIntegritySignature(
  orderId: string,
  amount: number,
  currency: string,
  secretKey: string
): string {
  const raw = `${orderId}${amount}${currency}${secretKey}`;
  return crypto.createHash("sha256").update(raw).digest("hex");
}
```

---

## 3. Webhook Signature Verification
Bold sends an `x-bold-signature` header with each webhook event:

```typescript
export function verifyBoldWebhook(
  rawBody: string,
  receivedSignature: string,
  secretKey: string
): boolean {
  const computed = crypto.createHmac("sha256", secretKey).update(rawBody).digest("hex");
  return crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(receivedSignature));
}
```
