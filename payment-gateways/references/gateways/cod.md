# Cash on Delivery (COD) WhatsApp OTP Verification Specification (v1.0)

## 1. Architectural Motivation
Cash on Delivery in Latin America suffers from high return-to-origin (RTO) rates (20-35%) caused by bogus orders or incorrect buyer addresses. To eliminate fake deliveries, orders selected as COD require a 6-digit WhatsApp OTP verification before warehouse dispatch.

---

## 2. Verification Lifecycle

1. **Checkout Submission**: Buyer selects "Contra-Entrega" (Cash on Delivery) and submits order with mobile phone.
2. **Order Placement in Directus**: Order created with status `pending_cod_verification`.
3. **OTP Generation & Valkey Storage**:
   - Random 6-digit cryptographic PIN generated (`crypto.randomInt(100000, 999999)`).
   - Stored in Valkey: `SET otp:cod:${orderId} ${pin} EX 600` (10-minute expiry).
   - Rate limiting key: `SET rate:otp:${phone} 1 EX 120 NX` (prevents spamming).
4. **WhatsApp Dispatch via NATS**:
   - Message published to NATS subject `events.whatsapp.otp`:
   ```json
   {
     "phone": "573001234567",
     "orderId": "ORDER-9912",
     "otp": "481902",
     "template": "cod_verification"
   }
   ```
   - EvolutionGo delivers the interactive WhatsApp message.
5. **Customer Confirmation**:
   - Customer enters OTP on checkout confirmation screen or replies to WhatsApp message.
   - Valkey validates:
     ```typescript
     const storedOtp = await valkey.get(`otp:cod:${orderId}`);
     if (storedOtp === userSubmittedOtp) {
       await valkey.del(`otp:cod:${orderId}`);
       // Update Directus order to confirmed
       await directus.updateOrder(orderId, { status: "confirmed_cod" });
       await nats.publish("order.cod.confirmed", { orderId });
     }
     ```
6. **Dispatch to Courier**: `orders-fulfillment` generates shipping guide with carrier collection fee.
