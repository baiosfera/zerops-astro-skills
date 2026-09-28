# `growth-commerce`: Comprehensive Usage Guide, Contracts & Implementation Recipes

> **SSoT Reference Document:** `/var/www/.agents/skills/growth-commerce/references/usage.md`  
> **Meta-Skill:** [`growth-commerce`](file:///var/www/.agents/skills/growth-commerce/SKILL.md)  
> **Standard:** CoHaLo v6.7, Supreme Directive v6.7, Secure Transactions & LatAm Logistics.

---

## 1. Sub-Skills Inventory & Physical File Pointers

* **Checkout, Wompi & COD:** [`checkout-funnels`](file:///var/www/.agents/skills/checkout-funnels/SKILL.md) ([usage](file:///var/www/.agents/skills/checkout-funnels/references/usage.md)).
* **Carrier Logistics & Fulfillment:** [`orders-fulfillment`](file:///var/www/.agents/skills/orders-fulfillment/SKILL.md) ([usage](file:///var/www/.agents/skills/orders-fulfillment/references/usage.md)).
* **Email Marketing & Deliverability:** [`email-marketing`](file:///var/www/.agents/skills/email-marketing/SKILL.md) ([usage](file:///var/www/.agents/skills/email-marketing/references/usage.md)).
* **Official WhatsApp Cloud API:** [`whatsapp-cloud`](file:///var/www/.agents/skills/whatsapp-cloud/SKILL.md) ([usage](file:///var/www/.agents/skills/whatsapp-cloud/references/usage.md)).
* **Sovereign Evolution API:** [`evolution-api`](file:///var/www/.agents/skills/evolution-api/SKILL.md) ([usage](file:///var/www/.agents/skills/evolution-api/references/usage.md)).
* **AI SDRs & BANT Qualification:** [`sales-enablement`](file:///var/www/.agents/skills/sales-enablement/SKILL.md) ([usage](file:///var/www/.agents/skills/sales-enablement/references/usage.md)).
* **NATS Automation Engine:** [`automation-engine`](file:///var/www/.agents/skills/automation-engine/SKILL.md) ([usage](file:///var/www/.agents/skills/automation-engine/references/usage.md)).
* **Frappe Cloud DIAN Invoicing:** [`erpnext`](file:///var/www/.agents/skills/erpnext/SKILL.md) ([usage](file:///var/www/.agents/skills/erpnext/references/usage.md)).

---

## 2. TypeScript Contract: Wompi Cryptographic Webhook Verification

Module to validate payment integrity for approved transactions (PSE, Nequi, Credit Cards) via SHA-256 hash checking:

```typescript
// src/lib/payments/wompi-validator.ts
import crypto from 'node:crypto';

export interface WompiWebhookEvent {
  event: string;
  data: {
    transaction: {
      id: string;
      amount_in_cents: number;
      reference: string;
      customer_email: string;
      currency: string;
      payment_method_type: string;
      status: 'APPROVED' | 'DECLINED' | 'VOIDED' | 'ERROR';
    };
  };
  signature: {
    properties: string[];
    checksum: string;
  };
  timestamp: number;
}

export function verifyWompiSignature(event: WompiWebhookEvent, eventsSecret: string): boolean {
  const { properties, checksum } = event.signature;
  const transaction = event.data.transaction as Record<string, any>;

  // Concatenate values in specified order + timestamp + eventsSecret
  let concatenatedString = '';
  for (const prop of properties) {
    const segments = prop.split('.');
    let val = transaction;
    for (const seg of segments) {
      if (seg === 'transaction') continue;
      val = val?.[seg];
    }
    concatenatedString += val;
  }
  concatenatedString += event.timestamp;
  concatenatedString += eventsSecret;

  const calculatedChecksum = crypto.createHash('sha256').update(concatenatedString).digest('hex');
  return calculatedChecksum === checksum;
}
```

---

## 3. TypeScript Contract: Logistics Dispatch with Coordinadora & Servientrega

Generation of shipping waybills and Cash on Delivery (COD) collection orders with 8-digit DANE Divipola codes:

```typescript
// src/lib/logistics/carrier-service.ts
export interface ShippingOrderPayload {
  orderId: string;
  customerName: string;
  customerPhone: string;
  address: string;
  cityDaneCode: string; // e.g. "11001000" for Bogota D.C.
  isCOD: boolean;
  totalCollectAmountCOP: number;
  declaredValueCOP: number;
  weightKg: number;
}

export class CarrierService {
  private coordinadoraApiKey: string;

  constructor() {
    this.coordinadoraApiKey = process.env.COORDINADORA_API_KEY || '';
  }

  async createDispatchGuide(payload: ShippingOrderPayload) {
    const response = await fetch('https://api.coordinadora.com/cm-guias-ms/guias/v1/radicar', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.coordinadoraApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        codigo_remitente: process.env.COORDINADORA_CLIENT_CODE,
        nombre_destinatario: payload.customerName,
        direccion_destinatario: payload.address,
        telefono_destinatario: payload.customerPhone,
        ciudad_destinatario: payload.cityDaneCode,
        valor_declarado: payload.declaredValueCOP,
        valor_recaudo: payload.isCOD ? payload.totalCollectAmountCOP : 0,
        peso_real: payload.weightKg,
        referencia: payload.orderId,
      }),
    });

    if (!response.ok) {
      const err = await response.text();
      throw new Error(`Carrier dispatch error (${response.status}): ${err}`);
    }

    const data = await response.json();
    return {
      trackingNumber: data.guia,
      labelPdfUrl: data.pdf_url,
      estimatedDeliveryDate: data.fecha_estimada,
    };
  }
}
```

---

## 4. End-to-End Order Lifecycle Orchestration

Automated pipeline executed immediately after successful payment or confirmed COD order:

```typescript
// src/services/order-orchestrator.ts
import { ERPNextClient } from './erpnext-client';
import { CarrierService } from './carrier-service';
import { sendWhatsAppTemplate } from './whatsapp-service';
import { connect, JSONCodec } from 'nats';

const jc = JSONCodec();

export async function processConfirmedOrder(order: any) {
  const erpClient = new ERPNextClient();
  const carrierService = new CarrierService();

  // 1. Generate Carrier Shipping Guide (Coordinadora / Servientrega)
  const carrierGuide = await carrierService.createDispatchGuide({
    orderId: order.id,
    customerName: order.customer_name,
    customerPhone: order.customer_phone,
    address: order.shipping_address,
    cityDaneCode: order.dane_code,
    isCOD: order.payment_gateway === 'COD',
    totalCollectAmountCOP: order.total_amount,
    declaredValueCOP: order.total_amount,
    weightKg: 1.0,
  });

  // 2. Emit Legal Invoice in Frappe Cloud ($0 SaaS ERPNext)
  const legalInvoice = await erpClient.createSalesInvoice({
    customer: order.customer_name,
    items: order.items.map((it: any) => ({
      item_code: it.sku,
      qty: it.quantity,
      rate: it.unitPrice,
    })),
  });

  // 3. Send WhatsApp Notification with Live Tracking Link
  await sendWhatsAppTemplate({
    recipientPhone: order.customer_phone,
    templateName: 'order_dispatched_co',
    components: [
      {
        type: 'body',
        parameters: [
          { type: 'text', text: order.customer_name },
          { type: 'text', text: carrierGuide.trackingNumber },
          { type: 'text', text: legalInvoice.name },
        ],
      },
    ],
  });

  // 4. Publish Event to NATS JetStream for Analytics
  const nc = await connect({ servers: process.env.NATS_URL });
  nc.publish('events.order.completed', jc.encode({
    orderId: order.id,
    trackingNumber: carrierGuide.trackingNumber,
    invoiceNumber: legalInvoice.name,
    amountCOP: order.total_amount,
  }));
  await nc.drain();

  return { success: true, trackingNumber: carrierGuide.trackingNumber, invoiceNumber: legalInvoice.name };
}
```

---

## 5. Abandoned Cart Recovery Sequences

* **15-Minute Mark (WhatsApp Direct Hook):**
  * Interactive message: *"Hi {{1}}, we noticed you left your order in progress. Would you like to complete it now or switch to Cash on Delivery upon arrival?"*
* **2-Hour Mark (Dynamic React Email via Resend):**
  * Dynamic email displaying abandoned items, security trust badges, and an automated 5% discount checkout link.
