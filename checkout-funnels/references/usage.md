# Checkout Funnels, Multi-Gateway Payments & Conversion Engine Manual (v2.0)

`checkout-funnels` is the sovereign conversion engine, multi-gateway payment orchestrator, cryptographic webhook validator, 1-Click Upsell system, and cart recovery pipeline for the Zerops stack. It decouples checkout business logic via `IPaymentGatewayProvider` to support **Wompi** (Colombia), **ePayco**, **dLocal Go** (LatAm multi-country), **Stripe** (Global), **Mercado Pago**, and **Cash on Delivery (COD)** with WhatsApp OTP verification.

---

## 1. 4D Comparative Architectural Matrix

| Payment Gateway | Geographic Scope | Payment Methods Supported | Signature Algorithm | Zerops Suitability |
|---|---|---|---|---|
| **Wompi Colombia** | Colombia | Cards, PSE, Nequi, Bancolombia QR | **SHA-256** (`ref + amount + curr + secret`) | **SSoT for Colombia** |
| **ePayco** | Colombia / LatAm | Cards, PSE, Daviplata, Efecty, Gana | **SHA-256** (Concatenation with `^`) | Cash & voucher payments |
| **dLocal Go** | LatAm (15+ countries) | Pix (BR), OXXO (MX), Webpay (CL), PSE | **HMAC-SHA256** (`apiKey + ts + body`) | Cross-border LatAm multi-currency |
| **Stripe** | Global (45+ countries) | Global Cards, Apple Pay, Google Pay | **HMAC-SHA256** (`Stripe-Signature`) | International / Global SaaS |
| **Mercado Pago** | LatAm (BR, MX, AR, CO) | Checkout Pro, Pix, Cards | **HMAC-SHA256** (Manifest with `ts`) | Best for Brazil & Mexico |
| **Cash on Delivery (COD)** | Local (Colombia / LatAm) | Cash on Delivery + WhatsApp OTP | **WhatsApp OTP Verification** | Reduces shipping return rates |

---

## 2. Unified Payment Gateway Strategy (`IPaymentGatewayProvider`)

```typescript
import {
  getAutoConfiguredPaymentProvider,
  WompiPaymentAdapter,
  EpaycoPaymentAdapter,
  DLocalGoPaymentAdapter,
  StripePaymentAdapter,
  CreateCheckoutSessionInput
} from "../assets/payment_provider_interface";

// 1. Automatic runtime provider resolution from environment
export async function initiateCheckout(input: CreateCheckoutSessionInput) {
  const provider = getAutoConfiguredPaymentProvider();
  return await provider.createCheckoutSession(input);
}
```

---

## 3. Cryptographic Integrity Validation Formulas by Gateway

### A. Wompi Colombia (SHA-256)
$$\text{Signature} = \text{SHA256}(\text{reference} + \text{amount\_in\_cents} + \text{currency} + \text{integrity\_secret})$$

### B. ePayco Colombia & LatAm (SHA-256)
$$\text{Signature} = \text{SHA256}(\text{p\_cust\_id\_cliente} \parallel \text{"\textasciicircum"} \parallel \text{p\_key} \parallel \text{"\textasciicircum"} \parallel \text{x\_ref\_payco} \parallel \text{"\textasciicircum"} \parallel \text{x\_transaction\_id} \parallel \text{"\textasciicircum"} \parallel \text{x\_amount} \parallel \text{"\textasciicircum"} \parallel \text{x\_currency\_code})$$

### C. dLocal Go (HMAC-SHA256)
$$\text{Signature} = \text{HMAC-SHA256}(\text{secretKey}, \text{apiKey} + \text{timestamp} + \text{rawBody})$$

### D. Stripe (HMAC-SHA256 `Stripe-Signature`)
$$\text{Signature} = \text{HMAC-SHA256}(\text{webhookSecret}, \text{timestamp} + \text{"."} + \text{rawBody})$$

### E. Mercado Pago (HMAC-SHA256 Canonical Manifest)
$$\text{Manifest} = \text{"id:"} + \text{dataId} + \text{";request-id:"} + \text{xRequestId} + \text{";ts:"} + \text{ts} + \text{";"}$$

---

## 4. 1-Click Post-Purchase Upsells & Card Tokenization

1. **Initial Purchase:** Customer completes order on Astro checkout page.
2. **Card Tokenization:** Gateway returns a reusable `payment_source_token` or `customer_token` upon successful initial charge.
3. **Upsell Presentation:** Backend immediately returns 1-Click Upsell modal before redirecting to the Thank You page.
4. **1-Click Charge:** If the customer clicks "Add to Order", the backend calls `POST /api/checkout/upsell`, charging the saved customer token directly without requiring re-entry of card details or CVV.

---

## 5. Colombian Logistics & DANE 8-Digit Normalization

Colombian shipping carriers (Coordinadora, Servientrega, Envía, 99minutos) require canonical 8-digit DANE codes:

| Department | City / Municipality | 8-Digit DANE Code |
|---|---|---|
| Bogotá D.C. | Bogotá D.C. | `11001000` |
| Antioquia | Medellín | `05001000` |
| Valle del Cauca | Cali | `76001000` |
| Atlántico | Barranquilla | `08001000` |
| Santander | Bucaramanga | `68001000` |

```typescript
export function validateDaneCode(code: string): boolean {
  return /^\d{8}$/.test(code);
}
```

---

## 6. Cash on Delivery (COD) with WhatsApp OTP Verification

To eliminate fraudulent orders and high return shipping fees:

```typescript
import Redis from 'ioredis';

const valkey = new Redis(process.env.VALKEY_URL || 'redis://cache:6379');

export async function generateAndSendCodOtp(orderId: string, phone: string): Promise<string> {
  const otp = Math.floor(100000 + Math.random() * 900000).toString();
  await valkey.set(`cod:otp:${orderId}`, otp, 'EX', 600); // 10 min TTL

  // Send WhatsApp message via Evolution Go
  const instance = process.env.WA_INSTANCE || 'default';
  await fetch(`http://evolutiongo:8080/message/sendText/${instance}`, {
    method: 'POST',
    headers: { 'apikey': process.env.EVOGO_API_KEY || 'key', 'Content-Type': 'application/json' },
    body: JSON.stringify({
      number: phone,
      text: `Your confirmation code for order #${orderId} (Cash on Delivery) is: *${otp}*. Reply with this code to confirm shipment. 📦`
    })
  });

  return otp;
}

export async function verifyCodOtp(orderId: string, enteredOtp: string): Promise<boolean> {
  const stored = await valkey.get(`cod:otp:${orderId}`);
  if (stored && stored === enteredOtp) {
    await valkey.del(`cod:otp:${orderId}`);
    return true;
  }
  return false;
}
```

---

## 7. Server-Side Tracking with Meta Conversions API (CAPI)

```typescript
import crypto from 'node:crypto';

function hashSha256(value: string): string {
  return crypto.createHash('sha256').update(value.trim().toLowerCase()).digest('hex');
}

export async function sendMetaPurchaseEvent(order: {
  id: string;
  amount: number;
  currency: string;
  email: string;
  phone: string;
  clientIp?: string;
  userAgent?: string;
}) {
  const pixelId = process.env.META_PIXEL_ID;
  const accessToken = process.env.META_CAPI_ACCESS_TOKEN;
  if (!pixelId || !accessToken) return;

  const payload = {
    data: [
      {
        event_name: 'Purchase',
        event_time: Math.floor(Date.now() / 1000),
        event_id: order.id,
        action_source: 'website',
        user_data: {
          em: [hashSha256(order.email)],
          ph: [hashSha256(order.phone)],
          client_ip_address: order.clientIp,
          client_user_agent: order.userAgent,
        },
        custom_data: {
          currency: order.currency,
          value: order.amount,
          order_id: order.id,
        }
      }
    ]
  };

  await fetch(`https://graph.facebook.com/v20.0/${pixelId}/events?access_token=${accessToken}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  }).catch(err => console.error('[Meta CAPI] Event dispatch error:', err.message));
}
```

---

## 8. 5 Production Patterns in Zerops

### Pattern 1: Multi-Gateway Checkout Strategy with Dynamic Fallbacks
Astro Actions evaluates customer location and payment method, dispatching transactions to Wompi for PSE/Nequi or Stripe for international cards.

### Pattern 2: Idempotent Webhook Verification with Valkey Distributed Locks
Every incoming webhook sets `SET lock:tx:<transaction_id> 1 NX EX 3600` in Valkey, preventing duplicate order approvals during webhook retry storms.

### Pattern 3: Automated WhatsApp OTP Verification for Cash on Delivery (COD)
Ensures COD orders are confirmed by the customer via WhatsApp before triggering warehouse fulfillment, reducing return rates by up to 80%.

### Pattern 4: Server-Side Meta CAPI Dispatch in Astro Actions
Fires `Purchase` events directly from the server to Meta CAPI with SHA-256 hashed user data, bypassing ad-blockers and iOS tracking restrictions.

### Pattern 5: Escalated Cart Recovery Sequences with BullMQ and WhatsApp
Schedules automated follow-up messages at 15 minutes and 2 hours with pre-populated checkout URLs and discount incentives via Evolution Go.

---

## 9. Anti-Patterns & Common Gotchas

1. **Processing Payments Without Signature Validation**: Accepting webhook callbacks without verifying SHA-256 or HMAC signatures allows attackers to forge payment approvals.
2. **Missing Idempotency Locking**: Gateway retries can cause duplicate inventory deductions if webhooks lack Valkey distributed locking.
3. **Storing Raw Card Data**: Never log or store credit card numbers (PAN) or CVVs. Always rely on gateway tokenization.
