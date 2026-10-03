# dLocal Go Driver Specification (v1.0)

## 1. Overview & Credentials
dLocal Go is a key payment provider for cross-border and local currency transactions in Latin America (Colombia: Cards, PSE, Nequi, Daviplata).

### Required Environment Variables:
- `DLOCAL_GO_API_KEY`: Api Key string.
- `DLOCAL_GO_SECRET_KEY`: Secret Key string.
- `DLOCAL_GO_ENV`: `sandbox` (for test/staging) or `live` (for production).

---

## 2. Dynamic Endpoint Resolution (Sandbox vs Live)
Always resolve the upstream API URL dynamically based on the environment flag:

```typescript
export function getDLocalGoUrl(env?: string): string {
  const isSandbox = (env || process.env.DLOCAL_GO_ENV || "").toLowerCase() === "sandbox";
  return isSandbox 
    ? "https://api-sbx.dlocalgo.com/v1/payments" 
    : "https://api.dlocalgo.com/v1/payments";
}
```

---

## 3. Session Creation Contract (`POST /v1/payments`)
To generate a checkout redirect session:

```typescript
const response = await fetch(getDLocalGoUrl(), {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${apiKey}:${secretKey}`,
  },
  body: JSON.stringify({
    amount: amountInPesos, // e.g. 100000 COP
    currency: "COP",
    country: "CO",
    order_id: ticketId,
    description: `Ticket de acceso — ${orderId}`,
    success_url: `https://${domain}/ticket?hash=${ticketHash}`,
    back_url: `https://${domain}/checkout`,
    notification_url: `https://${domain}/api/webhooks/dlocal`,
  }),
});

const data = await response.json();
if (data.redirect_url) {
  // Redirect customer to data.redirect_url
}
```

---

## 4. Concurrency Guard & Idempotency Rules
1. **Frontend Button Debounce:** Disable the checkout button on first click (`btn.disabled = true`) to prevent concurrent duplicate orders.
2. **Backend 60s Window Lock:** Before inserting a new order, check for an existing `pendiente` record created by the same contact within the last 60 seconds. Re-use existing `id` and `ticket_hash` if present.

---

## 5. Webhook Verification & Authority
The webhook handler (`/api/webhooks/dlocal`) is the **sole authority** for issuing digital credentials and confirmed tickets:
- Evaluate `status === "PAID"` or `status === "COMPLETED"`.
- Mark ticket as `confirmado` in database.
- Trigger asynchronous confirmation notifications (Email + WhatsApp) with real dynamic QR code link.
- Return HTTP 200 immediately to acknowledge receipt.
