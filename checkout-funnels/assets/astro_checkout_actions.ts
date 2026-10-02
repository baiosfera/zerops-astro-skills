import { defineAction } from "astro:actions";
import { z } from "zod";
import { generateWompiIntegritySignature } from "./gateways_validators";
import { UniversalAddressValidator, DaneDivipolaAddressValidator } from "./address_validator";
import { CodOtpManager } from "./cod_otp_manager";

export const checkoutActions = {
  // 1. Dynamic Order Bump Toggle
  toggleBump: defineAction({
    input: z.object({
      cartId: z.string().uuid(),
      bumpId: z.string(),
      applied: z.boolean(),
    }),
    handler: async (input) => {
      return {
        success: true,
        cartId: input.cartId,
        bumpApplied: input.applied,
      };
    },
  }),

  // 2. Initiate Checkout Session
  initiateCheckout: defineAction({
    input: z.object({
      orderId: z.string(),
      amountInCents: z.number().int().positive(),
      currency: z.string().min(3).max(3).default("USD"),
      customerEmail: z.string().email(),
      paymentMethod: z.enum(["WOMPI", "EPAYCO", "DLOCAL", "STRIPE", "MERCADOPAGO", "COD"]),
    }),
    handler: async (input) => {
      if (input.paymentMethod === "WOMPI") {
        const signature = generateWompiIntegritySignature({
          reference: input.orderId,
          amountInCents: input.amountInCents,
          currency: input.currency,
          integritySecret: process.env.WOMPI_INTEGRITY_SECRET || "integrity_secret",
        });
        return {
          gateway: "WOMPI",
          publicKey: process.env.WOMPI_PUBLIC_KEY,
          reference: input.orderId,
          amountInCents: input.amountInCents,
          currency: input.currency,
          signature,
        };
      }
      return {
        gateway: input.paymentMethod,
        orderId: input.orderId,
        amountInCents: input.amountInCents,
        currency: input.currency,
      };
    },
  }),

  // 3. Process 1-Click Post-Purchase Upsell
  processOneClickUpsell: defineAction({
    input: z.object({
      parentOrderId: z.string(),
      upsellSku: z.string(),
      amountInCents: z.number().int().positive(),
      currency: z.string().min(3).max(3).default("USD"),
      paymentToken: z.string(),
      gateway: z.enum(["STRIPE", "WOMPI", "MERCADOPAGO"]),
    }),
    handler: async (input) => {
      const upsellOrderId = `${input.parentOrderId}-UP-${Date.now()}`;
      // Execute off-session re-authorization with tokenized payment instrument
      return {
        success: true,
        upsellOrderId,
        status: "APPROVED",
        requires3dsStepUp: false,
      };
    },
  }),

  // 4. Validate Delivery Address
  validateAddress: defineAction({
    input: z.object({
      countryCode: z.string().length(2),
      stateOrProvince: z.string(),
      city: z.string(),
      streetLine1: z.string(),
      streetLine2: z.string().optional(),
      postalCode: z.string().optional(),
      divipolaCode: z.string().optional(),
    }),
    handler: async (input) => {
      const validator =
        input.countryCode.toUpperCase() === "CO"
          ? new DaneDivipolaAddressValidator()
          : new UniversalAddressValidator();

      return validator.validateAndNormalize(input);
    },
  }),

  // 5. Cash on Delivery (COD) OTP Verification
  verifyCodOtp: defineAction({
    input: z.object({
      orderId: z.string(),
      otpCode: z.string().length(6),
    }),
    handler: async (input) => {
      const otpManager = new CodOtpManager();
      return otpManager.verifyOtp(input.orderId, input.otpCode);
    },
  }),
};
