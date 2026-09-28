import { z } from "zod";

// ============================================================================
// 1. Zod Domain Schemas & Types for Unified Logistics
// ============================================================================

export const AddressSchema = z.object({
  fullName: z.string().min(2),
  documentId: z.string().optional(),
  phone: z.string().min(7),
  email: z.string().email(),
  addressLine1: z.string().min(5),
  addressLine2: z.string().optional(),
  neighborhood: z.string().optional(),
  daneCode8: z.string().length(8), // DANE 8 digits (e.g. 05001000)
  cityName: z.string(),
  departmentName: z.string(),
  countryCode: z.string().default("CO"),
  postalCode: z.string().optional(),
});

export const PackageDimensionsSchema = z.object({
  weightKg: z.number().positive(),
  lengthCm: z.number().positive(),
  widthCm: z.number().positive(),
  heightCm: z.number().positive(),
  declaredValueCop: z.number().nonnegative(),
  contentDescription: z.string().default("Mercancía e-commerce"),
});

export const QuoteRequestSchema = z.object({
  origin: AddressSchema,
  destination: AddressSchema,
  packages: z.array(PackageDimensionsSchema).min(1),
  isCashOnDelivery: z.boolean().default(false),
  codAmountCop: z.number().nonnegative().optional(),
});

export const CarrierRateSchema = z.object({
  providerName: z.string(),
  carrierCode: z.string(),
  carrierName: z.string(),
  rateId: z.string(),
  shippingCostCop: z.number().nonnegative(),
  codFeeCop: z.number().nonnegative().default(0),
  insuranceCostCop: z.number().nonnegative().default(0),
  totalCostCop: z.number().nonnegative(),
  estimatedDeliveryDays: z.number().int().positive(),
  serviceLevel: z.string(),
});

export const CreateShipmentRequestSchema = z.object({
  orderNumber: z.string(),
  selectedRateId: z.string(),
  carrierCode: z.string(),
  origin: AddressSchema,
  destination: AddressSchema,
  packages: z.array(PackageDimensionsSchema).min(1),
  isCashOnDelivery: z.boolean().default(false),
  codAmountCop: z.number().nonnegative().optional(),
  collectionBankDetails: z.object({
    bankName: z.string(),
    accountType: z.enum(["AHO", "CTE"]),
    accountNumber: z.string(),
    beneficiaryName: z.string(),
    beneficiaryDocument: z.string(),
  }).optional(),
  labelFormat: z.enum(["PDF", "ZPL"]).default("PDF"),
  notes: z.string().optional(),
});

export const ShipmentResultSchema = z.object({
  providerName: z.string(),
  carrierName: z.string(),
  shipmentId: z.string(),
  trackingNumber: z.string(),
  labelUrl: z.string().url().optional(),
  labelBase64: z.string().optional(),
  trackingUrl: z.string().url(),
  billedWeightKg: z.number(),
  totalCostCop: z.number(),
  status: z.enum([
    "CREATED",
    "LABEL_GENERATED",
    "PICKED_UP",
    "IN_TRANSIT",
    "OUT_FOR_DELIVERY",
    "DELIVERED",
    "FAILED_ATTEMPT",
    "NOVELTY",
    "RETURNED",
    "CANCELLED"
  ]),
});

export const NormalizedWebhookEventSchema = z.object({
  provider: z.string(),
  carrier: z.string(),
  trackingNumber: z.string(),
  orderNumber: z.string().optional(),
  status: z.enum([
    "LABEL_GENERATED",
    "PICKED_UP",
    "IN_TRANSIT",
    "OUT_FOR_DELIVERY",
    "DELIVERED",
    "FAILED_ATTEMPT",
    "NOVELTY",
    "RETURNED",
    "CANCELLED"
  ]),
  rawStatus: z.string(),
  statusDescription: z.string(),
  timestamp: z.date(),
  noveltyReason: z.string().optional(),
  collectedAmountCop: z.number().optional(),
});

export type Address = z.infer<typeof AddressSchema>;
export type PackageDimensions = z.infer<typeof PackageDimensionsSchema>;
export type QuoteRequest = z.infer<typeof QuoteRequestSchema>;
export type CarrierRate = z.infer<typeof CarrierRateSchema>;
export type CreateShipmentRequest = z.infer<typeof CreateShipmentRequestSchema>;
export type ShipmentResult = z.infer<typeof ShipmentResultSchema>;
export type NormalizedWebhookEvent = z.infer<typeof NormalizedWebhookEventSchema>;

// ============================================================================
// 2. Unified Logistics Provider Interface
// ============================================================================

export interface ILogisticsProvider {
  readonly providerId: "mipaquete" | "skydropx" | "envia" | "coordinadora" | "servientrega";

  quote(request: QuoteRequest): Promise<CarrierRate[]>;
  createShipment(request: CreateShipmentRequest): Promise<ShipmentResult>;
  getLabel(shipmentId: string, format: "PDF" | "ZPL"): Promise<{ url?: string; base64?: string }>;
  track(trackingNumber: string): Promise<NormalizedWebhookEvent>;
  cancelShipment(shipmentId: string, reason?: string): Promise<{ success: boolean; cancellationCode: string }>;
  parseWebhook(rawBody: unknown, headers?: Record<string, string>): NormalizedWebhookEvent;
}

// ============================================================================
// 3. MiPaquete Adapter (Primary Multi-Carrier & COD Aggregator in Colombia)
// ============================================================================

export class MiPaqueteAdapter implements ILogisticsProvider {
  readonly providerId = "mipaquete" as const;
  private readonly baseUrl: string;
  private readonly apiKey: string;

  constructor(apiKey: string, isSandbox = false) {
    this.apiKey = apiKey;
    this.baseUrl = isSandbox ? "https://api.test.mipaquete.com/api" : "https://api-v2.mipaquete.com";
  }

  async quote(request: QuoteRequest): Promise<CarrierRate[]> {
    const pkg = request.packages[0];
    const payload = {
      origin_town: request.origin.daneCode8,
      destination_town: request.destination.daneCode8,
      weight: pkg.weightKg,
      width: pkg.widthCm,
      high: pkg.heightCm,
      long: pkg.lengthCm,
      declared_value: pkg.declaredValueCop,
      quantity: request.packages.length,
      type_of_load: "Estándar",
      payment_type: request.isCashOnDelivery ? 5 : 1,
      special_services: request.isCashOnDelivery ? 2 : 0,
      value_collection: request.codAmountCop ?? 0,
    };

    const res = await fetch(`${this.baseUrl}/quote`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "apikey": this.apiKey,
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error(`MiPaquete Quote Error (${res.status}): ${res.statusText}`);
    }

    const data = await res.json();
    return (data.delivery_options || []).map((opt: any) => ({
      providerName: "mipaquete",
      carrierCode: opt.delivery_company_name,
      carrierName: opt.delivery_company_name,
      rateId: opt.delivery_company_id,
      shippingCostCop: opt.shipping_cost,
      codFeeCop: opt.collection_cost || 0,
      insuranceCostCop: opt.insurance_cost || 0,
      totalCostCop: opt.total_cost,
      estimatedDeliveryDays: opt.delivery_days,
      serviceLevel: "Estándar",
    }));
  }

  async createShipment(request: CreateShipmentRequest): Promise<ShipmentResult> {
    const pkg = request.packages[0];
    const payload = {
      type: 1,
      weight: pkg.weightKg,
      width: pkg.widthCm,
      height: pkg.heightCm,
      large: pkg.lengthCm,
      declared_value: pkg.declaredValueCop,
      quantity: request.packages.length,
      comments: request.notes || "",
      origin: request.origin.daneCode8,
      destiny: request.destination.daneCode8,
      delivery: request.selectedRateId,
      payment_type: request.isCashOnDelivery ? 5 : 1,
      special_service: request.isCashOnDelivery ? 2 : 0,
      value_collection: request.codAmountCop || 0,
      sender: {
        name: request.origin.fullName,
        surname: "",
        phone: request.origin.phone,
        cell_phone: request.origin.phone,
        email: request.origin.email,
        collection_address: request.origin.addressLine1,
        nit: request.origin.documentId || "900000000",
      },
      receiver: {
        name: request.destination.fullName,
        surname: "",
        phone: request.destination.phone,
        cell_phone: request.destination.phone,
        email: request.destination.email,
        destination_address: request.destination.addressLine1,
      },
      collection_information: request.collectionBankDetails ? {
        bank: request.collectionBankDetails.bankName,
        type_account: request.collectionBankDetails.accountType,
        number_account: request.collectionBankDetails.accountNumber,
        name_beneficiary: request.collectionBankDetails.beneficiaryName,
        number_beneficiary: request.collectionBankDetails.beneficiaryDocument,
      } : undefined,
    };

    const res = await fetch(`${this.baseUrl}/sendings`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "apikey": this.apiKey,
      },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (!res.ok || data.error) {
      throw new Error(`MiPaquete CreateShipment Error: ${data.message || res.statusText}`);
    }

    return {
      providerName: "mipaquete",
      carrierName: data.delivery_company_name || "Carrier",
      shipmentId: data._id || data.sending_id,
      trackingNumber: data.mp_code || data.guide_number,
      labelUrl: data.guide_url || `${this.baseUrl}/sendings/${data._id}/label`,
      trackingUrl: `https://mipaquete.com/rastreo?guide=${data.mp_code}`,
      billedWeightKg: pkg.weightKg,
      totalCostCop: data.value || 0,
      status: "LABEL_GENERATED",
    };
  }

  async getLabel(shipmentId: string, format: "PDF" | "ZPL"): Promise<{ url?: string }> {
    return {
      url: `${this.baseUrl}/sendings/${shipmentId}/label?format=${format.toLowerCase()}`,
    };
  }

  async track(trackingNumber: string): Promise<NormalizedWebhookEvent> {
    const res = await fetch(`${this.baseUrl}/sendings/tracking/${trackingNumber}`, {
      headers: { "apikey": this.apiKey },
    });
    const data = await res.json();
    return this.parseWebhook(data);
  }

  async cancelShipment(shipmentId: string, reason?: string): Promise<{ success: boolean; cancellationCode: string }> {
    const res = await fetch(`${this.baseUrl}/sendings/${shipmentId}/cancel`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "apikey": this.apiKey,
      },
      body: JSON.stringify({ reason: reason || "Cancelado por el comercio" }),
    });
    const data = await res.json();
    return { success: res.ok, cancellationCode: data.cancellation_code || "CANCELLED" };
  }

  parseWebhook(rawBody: any): NormalizedWebhookEvent {
    const statusMap: Record<string, NormalizedWebhookEvent["status"]> = {
      CREATED: "LABEL_GENERATED",
      GENERATED: "LABEL_GENERATED",
      PICKED_UP: "PICKED_UP",
      SENDING: "IN_TRANSIT",
      IN_TRANSIT: "IN_TRANSIT",
      OUT_FOR_DELIVERY: "OUT_FOR_DELIVERY",
      DELIVERED: "DELIVERED",
      NOVELTY: "NOVELTY",
      RETURNED: "RETURNED",
      CANCELLED: "CANCELLED",
    };

    const rawStatus = (rawBody.status || rawBody.shipping_status || "CREATED").toUpperCase();
    return {
      provider: "mipaquete",
      carrier: rawBody.carrier_name || rawBody.delivery_company_name || "Carrier",
      trackingNumber: rawBody.carrier_tracking_number || rawBody.mp_code || rawBody.guide_number,
      orderNumber: rawBody.reference || rawBody.order_number,
      status: statusMap[rawStatus] || "IN_TRANSIT",
      rawStatus: rawStatus,
      statusDescription: rawBody.status_description || rawStatus,
      timestamp: rawBody.timestamp ? new Date(rawBody.timestamp) : new Date(),
      noveltyReason: rawBody.novelty_reason,
      collectedAmountCop: rawBody.collected_amount,
    };
  }
}

// ============================================================================
// 4. Skydropx Adapter (LatAm Multi-Carrier Aggregator)
// ============================================================================

export class SkydropxAdapter implements ILogisticsProvider {
  readonly providerId = "skydropx" as const;
  private readonly token: string;
  private readonly baseUrl = "https://api-pro.skydropx.com/api/v1";

  constructor(token: string) {
    this.token = token;
  }

  async quote(request: QuoteRequest): Promise<CarrierRate[]> {
    const pkg = request.packages[0];
    const res = await fetch(`${this.baseUrl}/quotations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${this.token}`,
      },
      body: JSON.stringify({
        quotation: {
          address_from: {
            country_code: request.origin.countryCode || "CO",
            postal_code: request.origin.postalCode || "050001",
            area_level1: request.origin.departmentName,
            area_level2: request.origin.cityName,
          },
          address_to: {
            country_code: request.destination.countryCode || "CO",
            postal_code: request.destination.postalCode || "110111",
            area_level1: request.destination.departmentName,
            area_level2: request.destination.cityName,
          },
          parcels: [
            {
              length: pkg.lengthCm,
              width: pkg.widthCm,
              height: pkg.heightCm,
              weight: pkg.weightKg,
              declared_amount: pkg.declaredValueCop,
            },
          ],
        },
      }),
    });

    const data = await res.json();
    return (data.rates || []).map((r: any) => ({
      providerName: "skydropx",
      carrierCode: r.carrier,
      carrierName: r.carrier,
      rateId: r.id,
      shippingCostCop: parseFloat(r.total_pricing),
      codFeeCop: 0,
      insuranceCostCop: 0,
      totalCostCop: parseFloat(r.total_pricing),
      estimatedDeliveryDays: r.days || 2,
      serviceLevel: r.service_level_name || "Standard",
    }));
  }

  async createShipment(request: CreateShipmentRequest): Promise<ShipmentResult> {
    const res = await fetch(`${this.baseUrl}/shipments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${this.token}`,
      },
      body: JSON.stringify({
        shipment: {
          rate_id: request.selectedRateId,
          address_from: {
            name: request.origin.fullName,
            street1: request.origin.addressLine1,
            city: request.origin.cityName,
            province: request.origin.departmentName,
            zip: request.origin.postalCode || "050001",
            country: request.origin.countryCode || "CO",
            phone: request.origin.phone,
            email: request.origin.email,
          },
          address_to: {
            name: request.destination.fullName,
            street1: request.destination.addressLine1,
            city: request.destination.cityName,
            province: request.destination.departmentName,
            zip: request.destination.postalCode || "110111",
            country: request.destination.countryCode || "CO",
            phone: request.destination.phone,
            email: request.destination.email,
          },
          label_format: request.labelFormat.toLowerCase(),
        },
      }),
    });

    const data = await res.json();
    return {
      providerName: "skydropx",
      carrierName: data.carrier || "Carrier",
      shipmentId: data.id,
      trackingNumber: data.tracking_number,
      labelUrl: data.label_url,
      trackingUrl: data.tracking_url || `https://radar.skydropx.com/tracking/${data.tracking_number}`,
      billedWeightKg: request.packages[0].weightKg,
      totalCostCop: 0,
      status: "LABEL_GENERATED",
    };
  }

  async getLabel(shipmentId: string, format: "PDF" | "ZPL"): Promise<{ url?: string }> {
    return { url: `https://api.skydropx.com/labels/${shipmentId}.${format.toLowerCase()}` };
  }

  async track(trackingNumber: string): Promise<NormalizedWebhookEvent> {
    return {
      provider: "skydropx",
      carrier: "Skydropx",
      trackingNumber,
      status: "IN_TRANSIT",
      rawStatus: "IN_TRANSIT",
      statusDescription: "En tránsito",
      timestamp: new Date(),
    };
  }

  async cancelShipment(shipmentId: string, reason?: string): Promise<{ success: boolean; cancellationCode: string }> {
    return { success: true, cancellationCode: "CANCELLED" };
  }

  parseWebhook(rawBody: any): NormalizedWebhookEvent {
    return {
      provider: "skydropx",
      carrier: rawBody.carrier || "Carrier",
      trackingNumber: rawBody.tracking_number,
      status: "IN_TRANSIT",
      rawStatus: rawBody.status || "UNKNOWN",
      statusDescription: rawBody.status || "Updated",
      timestamp: new Date(),
    };
  }
}

// ============================================================================
// 5. Automatic Logistics Provider Resolver & F1 Clarification Gate
// ============================================================================

export function getAutoConfiguredLogisticsProvider(): ILogisticsProvider {
  if (process.env.MIPAQUETE_API_KEY && process.env.MIPAQUETE_API_KEY.trim() !== "") {
    return new MiPaqueteAdapter(process.env.MIPAQUETE_API_KEY);
  }

  if (process.env.SKYDROPX_TOKEN && process.env.SKYDROPX_TOKEN.trim() !== "") {
    return new SkydropxAdapter(process.env.SKYDROPX_TOKEN);
  }

  throw new Error(
    `[F1 CLARIFICATION GATE - orders-fulfillment]\n` +
    `No active logistics provider credentials detected in zerops_env / process.env.\n` +
    `Supported Multi-Carrier Aggregators & Carriers:\n` +
    `• MiPaquete (Colombia COD & Multi-carrier): MIPAQUETE_API_KEY\n` +
    `• Skydropx (LatAm Multi-carrier): SKYDROPX_TOKEN\n` +
    `• Envia.com: ENVIA_API_KEY\n` +
    `• Coordinadora Direct: COORDINADORA_API_KEY, COORDINADORA_CLIENT_ID\n` +
    `• Servientrega Direct: SERVIENTREGA_USER, SERVIENTREGA_PASSWORD\n\n` +
    `Action required: Configure MIPAQUETE_API_KEY in Zerops environment or keys.md.`
  );
}
