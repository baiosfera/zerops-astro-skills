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
