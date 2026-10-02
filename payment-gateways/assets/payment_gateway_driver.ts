import crypto from "node:crypto";

/**
 * ISO-4217 Minor Unit Currency Exponent Map
 */
const CURRENCY_EXPONENTS: Record<string, number> = {
  USD: 2, EUR: 2, GBP: 2, CAD: 2, AUD: 2,
  BRL: 2, MXN: 2, PEN: 2, ARS: 2,
  COP: 2, // Wompi/Bold operate in integer minor units (centavos)
  JPY: 0, KRW: 0, CLP: 0, PYG: 0,
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

export function safeTimingCompare(a: string, b: string): boolean {
  const bufA = Buffer.from(a);
  const bufB = Buffer.from(b);
  if (bufA.length !== bufB.length) {
    return false;
  }
  return crypto.timingSafeEqual(bufA, bufB);
}

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

// 1. Wompi Driver
export class WompiPaymentDriver implements IPaymentGatewayProvider {
  readonly gatewayId = "wompi";
  readonly publicKey: string;
  readonly integritySecret: string;
  readonly eventsSecret: string;
  readonly privateKey?: string;

  constructor(publicKey: string, integritySecret: string, eventsSecret: string, privateKey?: string) {
    this.publicKey = publicKey;
    this.integritySecret = integritySecret;
    this.eventsSecret = eventsSecret;
    this.privateKey = privateKey;
  }

  generateIntegritySignature(reference: string, amountInMinorUnits: number, currency: string): string {
    const raw = `${reference}${amountInMinorUnits}${currency}${this.integritySecret}`;
    return crypto.createHash("sha256").update(raw).digest("hex");
  }

  async createPaymentSession(input: PaymentSessionInput): Promise<PaymentSessionResult> {
    const signature = this.generateIntegritySignature(input.orderId, input.amountInMinorUnits, input.currency);
    const checkoutUrl = `https://checkout.wompi.co/p/?public-key=${this.publicKey}&currency=${input.currency}&amount-in-cents=${input.amountInMinorUnits}&reference=${input.orderId}&signature:integrity=${signature}&redirect-url=${encodeURIComponent(input.redirectUrl)}`;

    return {
      gateway: "wompi",
      orderId: input.orderId,
      transactionReference: input.orderId,
      checkoutUrl,
    };
  }

  async verifyWebhook(input: WebhookPayloadInput): Promise<VerifiedPaymentEvent> {
    const bodyStr = typeof input.rawBody === "string" ? input.rawBody : input.rawBody.toString("utf8");
    let event: any;
    try {
      event = JSON.parse(bodyStr);
    } catch {
      return { isValid: false, gateway: "wompi", transactionId: "", orderId: "", status: "ERROR", amountInMinorUnits: 0, currency: "COP", rawEvent: null };
    }

    const transaction = event?.data?.transaction;
    const signature = event?.signature;
    const timestamp = event?.timestamp;

    if (!transaction || !signature?.properties || !signature?.checksum || !timestamp) {
      return { isValid: false, gateway: "wompi", transactionId: "", orderId: "", status: "ERROR", amountInMinorUnits: 0, currency: "COP", rawEvent: event };
    }

    let concat = "";
    for (const prop of signature.properties) {
      const parts = prop.split(".");
      let val: any = event.data;
      for (const p of parts) val = val?.[p];
      if (val === undefined || val === null) {
        return { isValid: false, gateway: "wompi", transactionId: transaction.id, orderId: transaction.reference, status: "ERROR", amountInMinorUnits: 0, currency: "COP", rawEvent: event };
      }
      concat += val.toString();
    }
    const toHash = `${concat}${timestamp}${this.eventsSecret}`;
    const calculated = crypto.createHash("sha256").update(toHash).digest("hex");
    const isValid = safeTimingCompare(calculated, signature.checksum);

    const statusMap: Record<string, "APPROVED" | "DECLINED" | "VOIDED" | "ERROR" | "PENDING"> = {
      APPROVED: "APPROVED",
      DECLINED: "DECLINED",
      VOIDED: "VOIDED",
      ERROR: "ERROR",
      PENDING: "PENDING",
    };

    return {
      isValid,
      gateway: "wompi",
      transactionId: transaction.id,
      orderId: transaction.reference,
      status: statusMap[transaction.status] || "PENDING",
      amountInMinorUnits: transaction.amount_in_cents,
      currency: transaction.currency,
      paymentMethod: transaction.payment_method_type,
      rawEvent: event,
    };
  }

  async getTransactionStatus(transactionId: string) {
    const res = await fetch(`https://production.wompi.co/v1/transactions/${transactionId}`, {
      headers: { Authorization: `Bearer ${this.privateKey || this.publicKey}` },
    });
    const data = (await res.json()) as any;
    const status = data?.data?.status === "APPROVED" ? "APPROVED" : "PENDING";
    return { status: status as any, raw: data };
  }
}

// 2. Stripe Driver
export class StripePaymentDriver implements IPaymentGatewayProvider {
  readonly gatewayId = "stripe";
  readonly secretKey: string;
  readonly webhookSecret: string;

  constructor(secretKey: string, webhookSecret: string) {
    this.secretKey = secretKey;
    this.webhookSecret = webhookSecret;
  }

  async createPaymentSession(input: PaymentSessionInput): Promise<PaymentSessionResult> {
    const params = new URLSearchParams({
      "payment_method_types[]": "card",
      "mode": "payment",
      "success_url": input.redirectUrl,
      "cancel_url": input.redirectUrl,
      "client_reference_id": input.orderId,
      "customer_email": input.customerEmail,
      "line_items[0][price_data][currency]": input.currency.toLowerCase(),
      "line_items[0][price_data][unit_amount]": input.amountInMinorUnits.toString(),
      "line_items[0][price_data][product_data][name]": `Order #${input.orderId}`,
      "line_items[0][quantity]": "1",
    });

    const res = await fetch("https://api.stripe.com/v1/checkout/sessions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.secretKey}`,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: params.toString(),
    });
    const data = (await res.json()) as any;

    return {
      gateway: "stripe",
      orderId: input.orderId,
      transactionReference: data.id,
      checkoutUrl: data.url,
      rawResponse: data,
    };
  }

  async verifyWebhook(input: WebhookPayloadInput): Promise<VerifiedPaymentEvent> {
    const sigHeader = input.headers["stripe-signature"] as string;
    if (!sigHeader) {
      return { isValid: false, gateway: "stripe", transactionId: "", orderId: "", status: "ERROR", amountInMinorUnits: 0, currency: "USD", rawEvent: null };
    }

    const bodyStr = typeof input.rawBody === "string" ? input.rawBody : input.rawBody.toString("utf8");
    const elements = sigHeader.split(",");
    let timestamp = -1;
    const signatures: string[] = [];

    for (const el of elements) {
      const [k, v] = el.split("=");
      if (k === "t") timestamp = parseInt(v, 10);
      if (k === "v1") signatures.push(v);
    }

    const signedPayload = `${timestamp}.${bodyStr}`;
    const expected = crypto.createHmac("sha256", this.webhookSecret).update(signedPayload).digest("hex");
    let isValid = false;

    for (const sig of signatures) {
      if (safeTimingCompare(sig, expected)) {
        isValid = true;
        break;
      }
    }

    const event = JSON.parse(bodyStr);
    const session = event?.data?.object;

    return {
      isValid,
      gateway: "stripe",
      transactionId: session?.id || "",
      orderId: session?.client_reference_id || "",
      status: event.type === "checkout.session.completed" ? "APPROVED" : "PENDING",
      amountInMinorUnits: session?.amount_total || 0,
      currency: session?.currency?.toUpperCase() || "USD",
      rawEvent: event,
    };
  }

  async getTransactionStatus(transactionId: string) {
    const res = await fetch(`https://api.stripe.com/v1/checkout/sessions/${transactionId}`, {
      headers: { Authorization: `Bearer ${this.secretKey}` },
    });
    const data = (await res.json()) as any;
    return {
      status: data.payment_status === "paid" ? "APPROVED" : "PENDING",
      raw: data,
    };
  }
}

// 3. Bold Driver
export class BoldPaymentDriver implements IPaymentGatewayProvider {
  readonly gatewayId = "bold";
  readonly identityKey: string;
  readonly secretKey: string;

  constructor(identityKey: string, secretKey: string) {
    this.identityKey = identityKey;
    this.secretKey = secretKey;
  }

  async createPaymentSession(input: PaymentSessionInput): Promise<PaymentSessionResult> {
    const orderHash = crypto
      .createHash("sha256")
      .update(`${input.orderId}${input.amountInMinorUnits}${input.currency}${this.secretKey}`)
      .digest("hex");

    const checkoutUrl = `https://checkout.bold.co/payment/${this.identityKey}?orderId=${input.orderId}&amount=${input.amountInMinorUnits}&currency=${input.currency}&integritySignature=${orderHash}&redirectionUrl=${encodeURIComponent(input.redirectUrl)}`;

    return {
      gateway: "bold",
      orderId: input.orderId,
      transactionReference: input.orderId,
      checkoutUrl,
    };
  }

  async verifyWebhook(input: WebhookPayloadInput): Promise<VerifiedPaymentEvent> {
    const sigHeader = (input.headers["x-bold-signature"] || input.headers["bold-signature"]) as string;
    if (!sigHeader) {
      return { isValid: false, gateway: "bold", transactionId: "", orderId: "", status: "ERROR", amountInMinorUnits: 0, currency: "COP", rawEvent: null };
    }

    const bodyStr = typeof input.rawBody === "string" ? input.rawBody : input.rawBody.toString("utf8");
    const calculated = crypto.createHmac("sha256", this.secretKey).update(bodyStr).digest("hex");
    const isValid = safeTimingCompare(calculated, sigHeader);

    let event: any;
    try {
      event = JSON.parse(bodyStr);
    } catch {
      return { isValid: false, gateway: "bold", transactionId: "", orderId: "", status: "ERROR", amountInMinorUnits: 0, currency: "COP", rawEvent: null };
    }

    return {
      isValid,
      gateway: "bold",
      transactionId: event.id || event.transactionId || "",
      orderId: event.reference || event.orderId || "",
      status: event.status === "PAID" || event.status === "APPROVED" ? "APPROVED" : "PENDING",
      amountInMinorUnits: event.amount || 0,
      currency: event.currency || "COP",
      rawEvent: event,
    };
  }

  async getTransactionStatus(transactionId: string) {
    const res = await fetch(`https://api.bold.co/v2/payment-orders/${transactionId}`, {
      headers: { "x-api-key": this.secretKey },
    });
    const data = (await res.json()) as any;
    return {
      status: data.status === "PAID" ? "APPROVED" : "PENDING",
      raw: data,
    };
  }
}

// 4. Mercado Pago Driver
export class MercadoPagoPaymentDriver implements IPaymentGatewayProvider {
  readonly gatewayId = "mercadopago";
  readonly accessToken: string;
  readonly webhookSecret: string;

  constructor(accessToken: string, webhookSecret: string) {
    this.accessToken = accessToken;
    this.webhookSecret = webhookSecret;
  }

  async createPaymentSession(input: PaymentSessionInput): Promise<PaymentSessionResult> {
    const res = await fetch("https://api.mercadopago.com/checkout/preferences", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.accessToken}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        external_reference: input.orderId,
        payer: { email: input.customerEmail, name: input.customerName },
        back_urls: { success: input.redirectUrl, failure: input.redirectUrl, pending: input.redirectUrl },
        notification_url: input.notificationUrl,
        items: [{
          title: `Order #${input.orderId}`,
          unit_price: fromMinorUnits(input.amountInMinorUnits, input.currency),
          quantity: 1,
          currency_id: input.currency.toUpperCase()
        }]
      })
    });
    const data = (await res.json()) as any;
    return {
      gateway: "mercadopago",
      orderId: input.orderId,
      transactionReference: data.id,
      checkoutUrl: data.init_point || data.sandbox_init_point,
      rawResponse: data
    };
  }

  async verifyWebhook(input: WebhookPayloadInput): Promise<VerifiedPaymentEvent> {
    const xSignature = input.headers["x-signature"] as string;
    const xRequestId = input.headers["x-request-id"] as string;
    if (!xSignature || !xRequestId) {
      return { isValid: false, gateway: "mercadopago", transactionId: "", orderId: "", status: "ERROR", amountInMinorUnits: 0, currency: "USD", rawEvent: null };
    }

    const parts = xSignature.split(",");
    let ts = "";
    let hash = "";
    for (const p of parts) {
      const [k, v] = p.trim().split("=");
      if (k === "ts") ts = v;
      if (k === "v1") hash = v;
    }

    const bodyStr = typeof input.rawBody === "string" ? input.rawBody : input.rawBody.toString("utf8");
    const manifest = `id:${xRequestId};request-id:${xRequestId};ts:${ts};`;
    const calculated = crypto.createHmac("sha256", this.webhookSecret).update(manifest).digest("hex");
    const isValid = safeTimingCompare(calculated, hash);

    let event: any = {};
    try { event = JSON.parse(bodyStr); } catch {}

    return {
      isValid,
      gateway: "mercadopago",
      transactionId: event.data?.id || "",
      orderId: event.data?.external_reference || "",
      status: event.action === "payment.created" ? "APPROVED" : "PENDING",
      amountInMinorUnits: 0,
      currency: "USD",
      rawEvent: event
    };
  }

  async getTransactionStatus(transactionId: string) {
    const res = await fetch(`https://api.mercadopago.com/v1/payments/${transactionId}`, {
      headers: { Authorization: `Bearer ${this.accessToken}` }
    });
    const data = (await res.json()) as any;
    return {
      status: data.status === "approved" ? "APPROVED" : "PENDING",
      raw: data
    };
  }
}

// 5. Cash on Delivery (COD) Driver
export class CodPaymentDriver implements IPaymentGatewayProvider {
  readonly gatewayId = "cod";
  readonly otpValiditySeconds: number;

  constructor(otpValiditySeconds = 900) {
    this.otpValiditySeconds = otpValiditySeconds;
  }

  async createPaymentSession(input: PaymentSessionInput): Promise<PaymentSessionResult> {
    return {
      gateway: "cod",
      orderId: input.orderId,
      transactionReference: `COD-${input.orderId}`,
      checkoutUrl: `${input.redirectUrl}?method=cod&orderId=${input.orderId}`,
    };
  }

  async verifyWebhook(input: WebhookPayloadInput): Promise<VerifiedPaymentEvent> {
    const bodyStr = typeof input.rawBody === "string" ? input.rawBody : input.rawBody.toString("utf8");
    let event: any = {};
    try { event = JSON.parse(bodyStr); } catch {}

    const isValid = event.otpVerified === true;
    return {
      isValid,
      gateway: "cod",
      transactionId: event.transactionId || `COD-${event.orderId}`,
      orderId: event.orderId || "",
      status: isValid ? "APPROVED" : "PENDING",
      amountInMinorUnits: event.amountInMinorUnits || 0,
      currency: event.currency || "USD",
      paymentMethod: "cash_on_delivery",
      rawEvent: event
    };
  }

  async getTransactionStatus(transactionId: string) {
    return {
      status: "PENDING" as const,
      raw: { transactionId, method: "cash_on_delivery" }
    };
  }
}

// 6. Provider Registry
export class PaymentProviderRegistry {
  private providers = new Map<string, IPaymentGatewayProvider>();

  register(provider: IPaymentGatewayProvider): this {
    this.providers.set(provider.gatewayId, provider);
    return this;
  }

  get(gatewayId: string): IPaymentGatewayProvider | undefined {
    return this.providers.get(gatewayId);
  }

  list(): string[] {
    return Array.from(this.providers.keys());
  }
}
