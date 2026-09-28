import crypto from "node:crypto";

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

// 1. Wompi Driver
export class WompiPaymentDriver implements PaymentGatewayDriver {
  readonly gatewayId = "wompi";

  constructor(
    private publicKey: string,
    private integritySecret: string,
    private eventsSecret: string,
    private privateKey?: string
  ) {}

  generateIntegritySignature(reference: string, amountInCents: number, currency: string): string {
    const raw = `${reference}${amountInCents}${currency}${this.integritySecret}`;
    return crypto.createHash("sha256").update(raw).digest("hex");
  }

  async createPaymentSession(input: PaymentSessionInput): Promise<PaymentSessionResult> {
    const signature = this.generateIntegritySignature(input.orderId, input.amountInCents, input.currency);
    const checkoutUrl = `https://checkout.wompi.co/p/?public-key=${this.publicKey}&currency=${input.currency}&amount-in-cents=${input.amountInCents}&reference=${input.orderId}&signature:integrity=${signature}&redirect-url=${encodeURIComponent(input.redirectUrl)}`;

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
      return { isValid: false, gateway: "wompi", transactionId: "", orderId: "", status: "ERROR", amountInCents: 0, currency: "COP", rawEvent: null };
    }

    const transaction = event?.data?.transaction;
    const signature = event?.signature;
    const timestamp = event?.timestamp;

    if (!transaction || !signature?.properties || !signature?.checksum || !timestamp) {
      return { isValid: false, gateway: "wompi", transactionId: "", orderId: "", status: "ERROR", amountInCents: 0, currency: "COP", rawEvent: event };
    }

    // Checksum verification
    let concat = "";
    for (const prop of signature.properties) {
      const parts = prop.split(".");
      let val = event.data;
      for (const p of parts) val = val?.[p];
      if (val === undefined || val === null) {
        return { isValid: false, gateway: "wompi", transactionId: transaction.id, orderId: transaction.reference, status: "ERROR", amountInCents: 0, currency: "COP", rawEvent: event };
      }
      concat += val.toString();
    }
    const toHash = `${concat}${timestamp}${this.eventsSecret}`;
    const calculated = crypto.createHash("sha256").update(toHash).digest("hex");

    const isValid = crypto.timingSafeEqual(Buffer.from(calculated, "hex"), Buffer.from(signature.checksum, "hex"));

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
      amountInCents: transaction.amount_in_cents,
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
export class StripePaymentDriver implements PaymentGatewayDriver {
  readonly gatewayId = "stripe";

  constructor(
    private secretKey: string,
    private webhookSecret: string
  ) {}

  async createPaymentSession(input: PaymentSessionInput): Promise<PaymentSessionResult> {
    const params = new URLSearchParams({
      "payment_method_types[]": "card",
      "mode": "payment",
      "success_url": input.redirectUrl,
      "cancel_url": input.redirectUrl,
      "client_reference_id": input.orderId,
      "customer_email": input.customerEmail,
      "line_items[0][price_data][currency]": input.currency.toLowerCase(),
      "line_items[0][price_data][unit_amount]": input.amountInCents.toString(),
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
      return { isValid: false, gateway: "stripe", transactionId: "", orderId: "", status: "ERROR", amountInCents: 0, currency: "USD", rawEvent: null };
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
      if (sig.length === expected.length && crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected))) {
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
      amountInCents: session?.amount_total || 0,
      currency: session?.currency || "usd",
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
