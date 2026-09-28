# Wompi Colombia Driver Specification (v1.0)

## 1. Overview & Credentials
Wompi is the primary sovereign payment provider for Colombian transactions, supporting Cards, PSE (Bank debits), Nequi, Bancolombia QR, and Cash correspondents (Efecty, SuRed).

### Required Environment Variables:
- `WOMPI_PUBLIC_KEY`: `pub_prod_...` or `pub_test_...`
- `WOMPI_PRIVATE_KEY`: `prv_prod_...` or `prv_test_...`
- `WOMPI_INTEGRITY_SECRET`: `prod_integrity_...` or `test_integrity_...`
- `WOMPI_EVENTS_SECRET`: `prod_events_...` or `test_events_...`

---

## 2. Integrity Signature (Checkout Session)
Before redirecting the customer to Wompi Web Checkout, calculate the SHA-256 integrity signature:

```typescript
import crypto from "node:crypto";

export function generateWompiIntegritySignature(
  reference: string,
  amountInCents: number,
  currency: string,
  integritySecret: string
): string {
  const rawString = `${reference}${amountInCents}${currency}${integritySecret}`;
  return crypto.createHash("sha256").update(rawString).digest("hex");
}
```

---

## 3. Webhook Event Checksum Verification (Server-to-Server)
Wompi signs incoming webhook notifications with a dynamic checksum. The payload structure includes a `signature` object:

```json
{
  "event": "transaction.updated",
  "data": {
    "transaction": {
      "id": "12345-1234567890-12345",
      "status": "APPROVED",
      "amount_in_cents": 5000000,
      "reference": "ORDER-9912",
      "currency": "COP"
    }
  },
  "signature": {
    "properties": [
      "transaction.id",
      "transaction.status",
      "transaction.amount_in_cents"
    ],
    "checksum": "d2f4a..."
  },
  "timestamp": 1530291411
}
```

### Verification Algorithm:
```typescript
import crypto from "node:crypto";

function getNestedValue(obj: any, path: string): any {
  return path.split(".").reduce((curr, key) => curr?.[key], obj);
}

export function verifyWompiWebhookChecksum(
  payload: any,
  eventsSecret: string
): boolean {
  if (!payload?.signature?.properties || !payload?.signature?.checksum || !payload?.timestamp) {
    return false;
  }

  const { properties, checksum } = payload.signature;
  const timestamp = payload.timestamp;

  // 1. Concatenate values of properties in order
  let concatenatedValues = "";
  for (const prop of properties) {
    const val = getNestedValue(payload.data, prop);
    if (val === undefined || val === null) return false;
    concatenatedValues += val.toString();
  }

  // 2. Append timestamp and events secret
  const toHash = `${concatenatedValues}${timestamp}${eventsSecret}`;
  const calculatedChecksum = crypto.createHash("sha256").update(toHash).digest("hex");

  // 3. Constant-time comparison
  return crypto.timingSafeEqual(
    Buffer.from(calculatedChecksum, "hex"),
    Buffer.from(checksum, "hex")
  );
}
```

---

## 4. Status Normalization Matrix
| Wompi Status | Normalized Status | Directus Order Transition | NATS Event Emitted |
|---|---|---|---|
| `APPROVED` | `APPROVED` | `orders.status = 'paid'` | `order.payment.settled` |
| `DECLINED` | `DECLINED` | `orders.status = 'payment_failed'` | `order.payment.failed` |
| `VOIDED` | `VOIDED` | `orders.status = 'cancelled'` | `order.payment.voided` |
| `ERROR` | `ERROR` | `orders.status = 'error'` | `order.payment.error` |
| `PENDING` | `PENDING` | `orders.status = 'awaiting_payment'` | None |
