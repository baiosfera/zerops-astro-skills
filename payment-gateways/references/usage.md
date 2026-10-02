# Sovereign Payment Gateways: Architectural Contracts & Workflows (v2.0)

## 1. Unified Payment Gateway Driver SPI (`IPaymentGatewayProvider`)

To eliminate vendor lock-in across global and regional markets, the payment subsystem follows the Strategy Pattern under a unified Service Provider Interface:

```typescript
export interface PaymentSessionInput {
  orderId: string;
  amountInMinorUnits: number;
  currency: string;
  customerEmail: string;
  customerName?: string;
  customerPhone?: string;
  redirectUrl: string;
  notificationUrl: string;
  metadata?: Record<string, any>;
}

export interface PaymentSessionResult {
  gateway: string;
  orderId: string;
  transactionReference: string;
  checkoutUrl: string;
  rawResponse?: Record<string, any>;
}

export interface WebhookPayloadInput {
  rawBody: string | Buffer;
  headers: Record<string, string | string[] | undefined>;
}

export interface VerifiedPaymentEvent {
  isValid: boolean;
  gateway: string;
  transactionId: string;
  orderId: string;
  status: "APPROVED" | "DECLINED" | "VOIDED" | "ERROR" | "PENDING";
  amountInMinorUnits: number;
  currency: string;
  paymentMethod?: string;
  rawEvent: any;
}

export interface IPaymentGatewayProvider {
  readonly gatewayId: string;
  createPaymentSession(input: PaymentSessionInput): Promise<PaymentSessionResult>;
  verifyWebhook(input: WebhookPayloadInput): Promise<VerifiedPaymentEvent>;
  getTransactionStatus(transactionId: string): Promise<{
    status: "APPROVED" | "DECLINED" | "VOIDED" | "ERROR" | "PENDING";
    raw: Record<string, any>;
  }>;
}
```

---

## 2. ISO-4217 Minor Units Precision

All payment calculations must operate in integer minor units (e.g. cents) to prevent floating-point rounding errors across different currencies:

```typescript
const CURRENCY_EXPONENTS: Record<string, number> = {
  USD: 2, EUR: 2, GBP: 2, CAD: 2, AUD: 2,
  BRL: 2, MXN: 2, PEN: 2, ARS: 2,
  COP: 2, JPY: 0, KRW: 0, CLP: 0, PYG: 0,
  BHD: 3, JOD: 3, KWD: 3, OMR: 3
};

export function toMinorUnits(amount: number, currency: string): number {
  const exp = CURRENCY_EXPONENTS[currency.toUpperCase()] ?? 2;
  return Math.round(amount * Math.pow(10, exp));
}

export function fromMinorUnits(minorUnits: number, currency: string): number {
  const exp = CURRENCY_EXPONENTS[currency.toUpperCase()] ?? 2;
  return minorUnits / Math.pow(10, exp);
}
```

---

## 3. Distributed Idempotency Locking in Valkey 7.2

To eliminate race conditions between client browser redirects and incoming webhook notifications, every incoming transaction MUST acquire a distributed lock using a unique cryptographic token and release it via an atomic Lua script:

```typescript
import crypto from "node:crypto";

const UNLOCK_LUA_SCRIPT = `
if redis.call("get", KEYS[1]) == ARGV[1] then
  return redis.call("del", KEYS[1])
else
  return 0
end
`;

export async function processWebhookWithIdempotency(
  valkey: any,
  transactionId: string,
  processor: () => Promise<void>
): Promise<{ processed: boolean; reason?: string }> {
  const lockKey = `lock:payment:${transactionId}`;
  const statusKey = `status:payment:${transactionId}`;
  const ownerToken = crypto.randomUUID();

  // 1. Check if already marked as settled
  const existingStatus = await valkey.get(statusKey);
  if (existingStatus === "SETTLED") {
    return { processed: false, reason: "already_settled" };
  }

  // 2. Acquire atomic lock with 60-second TTL
  const acquired = await valkey.set(lockKey, ownerToken, "EX", 60, "NX");
  if (!acquired) {
    return { processed: false, reason: "concurrent_operation_in_progress" };
  }

  try {
    // 3. Execute business logic (database update, stock decrement)
    await processor();

    // 4. Mark transaction as permanently settled (TTL 30 days)
    await valkey.set(statusKey, "SETTLED", "EX", 86400 * 30);
    return { processed: true };
  } finally {
    // 5. Release transient lock safely via Lua script
    await valkey.eval(UNLOCK_LUA_SCRIPT, 1, lockKey, ownerToken);
  }
}
```

---

## 4. Server-to-Server Webhook Flow & Event Decoupling

The end-to-end payment lifecycle guarantees zero dropped orders even when users close browser tabs immediately:

1. **Customer Completes Payment**: Payment processed on Stripe, Mercado Pago, Wompi, Bold, or COD confirmed.
2. **Gateway Dispatches Webhook**: Gateway sends POST request to `/api/webhooks/[gateway]`.
3. **Cryptographic Validation**: The raw request body is verified against checksum/HMAC signatures using timing-safe comparisons. Invalid signatures return `401 Unauthorized`.
4. **Valkey Distributed Lock**: `SET lock:payment:<txId> <ownerToken> NX EX 60`.
5. **Database Order Update**: Order status is transitioned to `paid`.
6. **NATS JetStream Broadcast**: Event `order.payment.settled` is published with full transaction details.
7. **Downstream Event Ingestion**:
   - `orders-fulfillment`: Initiates carrier waybill generation.
   - `email-marketing`: Dispatches transactional receipt via Listmonk `/api/tx`.
   - `whatsapp-engine`: Sends order confirmation to customer.
8. **Gateway Acknowledgment**: HTTP `200 OK` is returned to the payment gateway within 1.5 seconds.
