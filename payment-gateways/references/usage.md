# Sovereign Payment Gateways: Architectural Contracts & Workflows (v1.0)

## 1. Unified Payment Gateway Driver Architecture

To guarantee vendor decoupling and eliminate vendor lock-in across Latin America and global markets, the payment subsystem follows the Strategy Pattern via `PaymentGatewayDriver`:

```typescript
export interface PaymentSessionInput {
  orderId: string;
  amountInCents: number;
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
  amountInCents: number;
  currency: string;
  paymentMethod?: string;
  rawEvent: any;
}

export interface PaymentGatewayDriver {
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

## 2. Distributed Idempotency Locking in Valkey

To prevent duplicate execution when both client redirection and server webhook arrive in parallel, or when webhooks are retried by gateway servers, every incoming notification MUST acquire an atomic distributed lock in Valkey:

### Atomic Lock Sequence:
```typescript
import { Valkey } from "iovalkey"; // or standard redis client

export async function processWebhookWithIdempotency(
  valkey: any,
  transactionId: string,
  processor: () => Promise<void>
): Promise<{ processed: boolean; reason?: string }> {
  const lockKey = `lock:payment:${transactionId}`;
  const statusKey = `status:payment:${transactionId}`;

  // 1. Check if already marked as settled
  const existingStatus = await valkey.get(statusKey);
  if (existingStatus === "SETTLED") {
    return { processed: false, reason: "already_settled" };
  }

  // 2. Acquire atomic lock with 60-second TTL
  const acquired = await valkey.set(lockKey, "LOCKED", "EX", 60, "NX");
  if (!acquired) {
    return { processed: false, reason: "concurrent_operation_in_progress" };
  }

  try {
    // 3. Execute business logic (Update Directus, stock deduction)
    await processor();

    // 4. Mark transaction as permanently settled (TTL 30 days)
    await valkey.set(statusKey, "SETTLED", "EX", 86400 * 30);
    return { processed: true };
  } finally {
    // 5. Release transient lock
    await valkey.del(lockKey);
  }
}
```

---

## 3. Server-to-Server Webhook Flow & Event Decoupling

The end-to-end lifecycle ensures zero loss of payment events even if the customer's browser window is closed immediately after payment:

1. **Customer Completes Payment**: Payment occurs on Wompi, PSE, Nequi, or Stripe.
2. **Gateway Dispatches Webhook**: Gateway sends POST request to `/api/webhooks/[gateway]`.
3. **Cryptographic Validation**: The raw request body is verified against checksum/HMAC signatures. Unsigned or invalid requests return `401 Unauthorized`.
4. **Valkey Distributed Lock**: `SET lock:payment:<txId> 1 EX 60 NX`.
5. **Directus Order Update**: Order status is transitioned to `paid`.
6. **NATS JetStream Broadcast**: Event `order.payment.settled` is published with order details.
7. **Downstream Worker Ingestion**:
   - `orders-fulfillment` generates shipping label (Coordinadora / Servientrega).
   - `email-marketing` dispatches transactional receipt via Listmonk.
   - `whatsapp-engine` sends WhatsApp confirmation to buyer via EvolutionGo.
   - `erpnext` posts Sales Invoice and updates General Ledger.
8. **Gateway Acknowledgment**: HTTP `200 OK` is returned to the payment gateway within 1.5 seconds.
