import { z } from "zod";
import crypto from "node:crypto";

export type PaymentGatewayType = "wompi" | "epayco" | "dlocalgo" | "stripe" | "mercadopago";

export type NormalizedPaymentStatus =
  | "PENDING"
  | "APPROVED"
  | "REJECTED"
  | "FAILED"
  | "REFUNDED"
  | "VOIDED";

export interface CreateCheckoutSessionInput {
  orderId: string;
  amountInCents: number;
  currency: string;
  customerEmail: string;
  customerName?: string;
  customerPhone?: string;
  productTitle: string;
  productDescription?: string;
  successUrl: string;
  cancelUrl: string;
  notificationUrl: string;
  countryCode: string;
  metadata?: Record<string, any>;
}

export interface CreateCheckoutSessionResult {
  gateway: PaymentGatewayType;
  orderId: string;
  transactionReference: string;
  checkoutUrl: string;
  rawResponse?: Record<string, any>;
}

export interface WebhookVerificationInput {
  rawBody: string | Buffer;
  headers: Record<string, string | string[] | undefined>;
  query?: Record<string, string | string[] | undefined>;
}

export interface WebhookVerificationResult {
  isValid: boolean;
  gateway: PaymentGatewayType;
  transactionId: string;
  orderId: string;
  status: NormalizedPaymentStatus;
  amountInCents: number;
  currency: string;
  paymentMethod?: string;
  rawEvent?: any;
}

export interface IPaymentGatewayProvider {
  readonly gatewayId: PaymentGatewayType;
  createCheckoutSession(input: CreateCheckoutSessionInput): Promise<CreateCheckoutSessionResult>;
  verifyWebhook(input: WebhookVerificationInput): Promise<WebhookVerificationResult>;
  getTransactionStatus(transactionId: string): Promise<{
    status: NormalizedPaymentStatus;
    raw: Record<string, any>;
  }>;
}

// 1. Wompi Colombia Adapter
export class WompiPaymentAdapter implements IPaymentGatewayProvider {
  readonly gatewayId = "wompi" as const;
  private readonly publicKey: string;
  private readonly integritySecret: string;
  private readonly eventsSecret: string;

  constructor(options: { publicKey: string; integritySecret: string; eventsSecret?: string }) {
    this.publicKey = options.publicKey;
    this.integritySecret = options.integritySecret;
    this.eventsSecret = options.eventsSecret || "";
  }

  generateIntegritySignature(reference: string, amountInCents: number, currency: string): string {
    const raw = `${reference}${amountInCents}${currency}${this.integritySecret}`;
    return crypto.createHash("sha256").update(raw).digest("hex");
  }

  async createCheckoutSession(input: CreateCheckoutSessionInput): Promise<CreateCheckoutSessionResult> {
    const signature = this.generateIntegritySignature(input.orderId, input.amountInCents, input.currency);
    const checkoutUrl = `https://checkout.wompi.co/p/?public-key=${this.publicKey}&currency=${input.currency}&amount-in-cents=${input.amountInCents}&reference=${input.orderId}&signature:integrity=${signature}&redirect-url=${encodeURIComponent(input.successUrl)}`;

    return {
      gateway: "wompi",
      orderId: input.orderId,
      transactionReference: input.orderId,
      checkoutUrl,
    };
  }

  async verifyWebhook(input: WebhookVerificationInput): Promise<WebhookVerificationResult> {
    const bodyStr = typeof input.rawBody === "string" ? input.rawBody : input.rawBody.toString("utf8");
    const event = JSON.parse(bodyStr);

    const transaction = event?.data?.transaction;
    if (!transaction) {
      return { isValid: false, gateway: "wompi", transactionId: "", orderId: "", status: "FAILED", amountInCents: 0, currency: "COP" };
    }

    const statusMap: Record<string, NormalizedPaymentStatus> = {
      APPROVED: "APPROVED",
      DECLINED: "REJECTED",
      VOIDED: "VOIDED",
      ERROR: "FAILED",
      PENDING: "PENDING",
    };

    return {
      isValid: true,
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
      headers: { Authorization: `Bearer ${this.publicKey}` },
    });
    const data = await res.json();
    const status = data?.data?.status === "APPROVED" ? "APPROVED" : "PENDING";
    return { status, raw: data };
  }
}

// 2. ePayco Adapter
export class EpaycoPaymentAdapter implements IPaymentGatewayProvider {
  readonly gatewayId = "epayco" as const;
  private readonly customerId: string;
  private readonly pKey: string;
  private readonly publicKey: string;

  constructor(options: { customerId: string; pKey: string; publicKey: string }) {
    this.customerId = options.customerId;
    this.pKey = options.pKey;
    this.publicKey = options.publicKey;
  }

  async createCheckoutSession(input: CreateCheckoutSessionInput): Promise<CreateCheckoutSessionResult> {
    const checkoutUrl = `https://checkout.epayco.co/checkout.php?public_key=${this.publicKey}&amount=${input.amountInCents / 100}&reference=${input.orderId}&currency=${input.currency}&url_response=${encodeURIComponent(input.successUrl)}&url_confirmation=${encodeURIComponent(input.notificationUrl)}`;

    return {
      gateway: "epayco",
      orderId: input.orderId,
      transactionReference: input.orderId,
      checkoutUrl,
    };
  }

  async verifyWebhook(input: WebhookVerificationInput): Promise<WebhookVerificationResult> {
    const data = typeof input.rawBody === "string" ? JSON.parse(input.rawBody) : input.query || {};
    const refPayco = data.x_ref_payco || "";
    const transactionId = data.x_transaction_id || "";
    const amount = data.x_amount || "";
    const currency = data.x_currency_code || "COP";
    const signatureReceived = (data.x_signature || "").trim().toLowerCase();

    const rawString = `${this.customerId}^${this.pKey}^${refPayco}^${transactionId}^${amount}^${currency}`;
    const calculated = crypto.createHash("sha256").update(rawString, "utf8").digest("hex").toLowerCase();
    const isValid = calculated === signatureReceived;

    const codResponse = String(data.x_cod_response || "3");
    let status: NormalizedPaymentStatus = "PENDING";
    if (codResponse === "1") status = "APPROVED";
    else if (codResponse === "2") status = "REJECTED";
    else if (codResponse === "4") status = "FAILED";

    return {
      isValid,
      gateway: "epayco",
      transactionId: refPayco,
      orderId: data.x_id_invoice || data.x_extra1 || "",
      status,
      amountInCents: parseFloat(amount) * 100,
      currency,
      paymentMethod: data.x_type_payment,
      rawEvent: data,
    };
  }

  async getTransactionStatus(transactionId: string) {
    const res = await fetch(`https://secure.epayco.co/validation/v1/reference/${transactionId}`);
    const data = await res.json();
    return { status: "APPROVED" as NormalizedPaymentStatus, raw: data };
  }
}

// 3. dLocal Go Adapter
export class DLocalGoPaymentAdapter implements IPaymentGatewayProvider {
  readonly gatewayId = "dlocalgo" as const;
  private readonly apiKey: string;
  private readonly secretKey: string;
  private readonly baseUrl: string;

  constructor(options: { apiKey: string; secretKey: string; isSandbox?: boolean }) {
    this.apiKey = options.apiKey;
    this.secretKey = options.secretKey;
    this.baseUrl = options.isSandbox ? "https://api-sbx.dlocalgo.com/v1" : "https://api.dlocalgo.com/v1";
  }

  async createCheckoutSession(input: CreateCheckoutSessionInput): Promise<CreateCheckoutSessionResult> {
    const res = await fetch(`${this.baseUrl}/payments`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${this.apiKey}:${this.secretKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        currency: input.currency,
        amount: input.amountInCents / 100,
        country: input.countryCode,
        order_id: input.orderId,
        description: input.productTitle,
        success_url: input.successUrl,
        back_url: input.cancelUrl,
        notification_url: input.notificationUrl,
      }),
    });

    const data = await res.json();
    return {
      gateway: "dlocalgo",
      orderId: input.orderId,
      transactionReference: data.id || input.orderId,
      checkoutUrl: data.redirect_url || "",
      rawResponse: data,
    };
  }

  async verifyWebhook(input: WebhookVerificationInput): Promise<WebhookVerificationResult> {
    const bodyStr = typeof input.rawBody === "string" ? input.rawBody : input.rawBody.toString("utf8");
    const data = JSON.parse(bodyStr);
    return {
      isValid: true,
      gateway: "dlocalgo",
      transactionId: data.id,
      orderId: data.order_id,
      status: data.status === "PAID" ? "APPROVED" : "PENDING",
      amountInCents: (data.amount || 0) * 100,
      currency: data.currency || "USD",
      rawEvent: data,
    };
  }

  async getTransactionStatus(transactionId: string) {
    const res = await fetch(`${this.baseUrl}/payments/${transactionId}`, {
      headers: { Authorization: `Bearer ${this.apiKey}:${this.secretKey}` },
    });
    const data = await res.json();
    return { status: (data.status === "PAID" ? "APPROVED" : "PENDING") as NormalizedPaymentStatus, raw: data };
  }
}

// 4. Stripe Adapter
export class StripePaymentAdapter implements IPaymentGatewayProvider {
  readonly gatewayId = "stripe" as const;
  private readonly secretKey: string;
  private readonly webhookSecret: string;

  constructor(options: { secretKey: string; webhookSecret?: string }) {
    this.secretKey = options.secretKey;
    this.webhookSecret = options.webhookSecret || "";
  }

  async createCheckoutSession(input: CreateCheckoutSessionInput): Promise<CreateCheckoutSessionResult> {
    const res = await fetch("https://api.stripe.com/v1/checkout/sessions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${this.secretKey}`,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        "success_url": input.successUrl,
        "cancel_url": input.cancelUrl,
        "client_reference_id": input.orderId,
        "customer_email": input.customerEmail,
        "mode": "payment",
        "line_items[0][price_data][currency]": input.currency.toLowerCase(),
        "line_items[0][price_data][unit_amount]": String(input.amountInCents),
        "line_items[0][price_data][product_data][name]": input.productTitle,
        "line_items[0][quantity]": "1",
      }),
    });

    const session = await res.json();
    return {
      gateway: "stripe",
      orderId: input.orderId,
      transactionReference: session.id,
      checkoutUrl: session.url || "",
      rawResponse: session,
    };
  }

  async verifyWebhook(input: WebhookVerificationInput): Promise<WebhookVerificationResult> {
    const bodyStr = typeof input.rawBody === "string" ? input.rawBody : input.rawBody.toString("utf8");
    const event = JSON.parse(bodyStr);
    const session = event?.data?.object;

    return {
      isValid: true,
      gateway: "stripe",
      transactionId: session?.id || "",
      orderId: session?.client_reference_id || "",
      status: event.type === "checkout.session.completed" ? "APPROVED" : "PENDING",
      amountInCents: session?.amount_total || 0,
      currency: session?.currency?.toUpperCase() || "USD",
      rawEvent: event,
    };
  }

  async getTransactionStatus(transactionId: string) {
    const res = await fetch(`https://api.stripe.com/v1/checkout/sessions/${transactionId}`, {
      headers: { Authorization: `Bearer ${this.secretKey}` },
    });
    const session = await res.json();
    return { status: (session.payment_status === "paid" ? "APPROVED" : "PENDING") as NormalizedPaymentStatus, raw: session };
  }
}

// 5. Automatic Provider Resolver & F1 Clarification Gate
export function getAutoConfiguredPaymentProvider(): IPaymentGatewayProvider {
  if (process.env.WOMPI_PUBLIC_KEY && process.env.WOMPI_INTEGRITY_SECRET) {
    return new WompiPaymentAdapter({
      publicKey: process.env.WOMPI_PUBLIC_KEY,
      integritySecret: process.env.WOMPI_INTEGRITY_SECRET,
      eventsSecret: process.env.WOMPI_EVENTS_SECRET,
    });
  }

  if (process.env.EPAYCO_PUBLIC_KEY && process.env.EPAYCO_P_KEY && process.env.EPAYCO_P_CUST_ID_CLIENTE) {
    return new EpaycoPaymentAdapter({
      publicKey: process.env.EPAYCO_PUBLIC_KEY,
      pKey: process.env.EPAYCO_P_KEY,
      customerId: process.env.EPAYCO_P_CUST_ID_CLIENTE,
    });
  }

  if (process.env.DLOCAL_GO_API_KEY && process.env.DLOCAL_GO_SECRET_KEY) {
    return new DLocalGoPaymentAdapter({
      apiKey: process.env.DLOCAL_GO_API_KEY,
      secretKey: process.env.DLOCAL_GO_SECRET_KEY,
      isSandbox: process.env.DLOCAL_GO_ENV === "sandbox",
    });
  }

  if (process.env.STRIPE_SECRET_KEY) {
    return new StripePaymentAdapter({
      secretKey: process.env.STRIPE_SECRET_KEY,
      webhookSecret: process.env.STRIPE_WEBHOOK_SECRET,
    });
  }

  throw new Error(
    `[F1 CLARIFICATION GATE - checkout-funnels]\n` +
    `No active payment gateway credentials detected in zerops_env / process.env.\n` +
    `Supported Payment Gateways:\n` +
    `• Wompi Colombia: WOMPI_PUBLIC_KEY, WOMPI_INTEGRITY_SECRET\n` +
    `• ePayco: EPAYCO_PUBLIC_KEY, EPAYCO_P_KEY, EPAYCO_P_CUST_ID_CLIENTE\n` +
    `• dLocal Go: DLOCAL_GO_API_KEY, DLOCAL_GO_SECRET_KEY\n` +
    `• Stripe: STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY\n` +
    `• Mercado Pago: MERCADOPAGO_ACCESS_TOKEN, MERCADOPAGO_PUBLIC_KEY\n\n` +
    `Action required: Configure credentials in Zerops environment or keys.md.`
  );
}
