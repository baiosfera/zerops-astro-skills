import { defineAction } from "astro:actions";
import { z } from "zod";
import { generateWompiIntegritySignature } from "./gateways_validators";

export const checkoutActions = {
  // 1. Toggle dinámico de Order Bump
  toggleBump: defineAction({
    input: z.object({
      cartId: z.string().uuid(),
      bumpId: z.string(),
      applied: z.boolean()
    }),
    handler: async (input) => {
      // Recálculo SSoT en servidor
      return {
        success: true,
        cartId: input.cartId,
        bumpApplied: input.applied
      };
    }
  }),

  // 2. Procesar Inicio de Checkout
  initiateCheckout: defineAction({
    input: z.object({
      orderId: z.string(),
      amountInCents: z.number().int().positive(),
      currency: z.literal("COP"),
      customerEmail: z.string().email(),
      paymentMethod: z.enum(["WOMPI", "EPAYCO", "DLOCAL", "STRIPE", "COD"])
    }),
    handler: async (input) => {
      if (input.paymentMethod === "WOMPI") {
        const signature = generateWompiIntegritySignature({
          reference: input.orderId,
          amountInCents: input.amountInCents,
          currency: "COP",
          integritySecret: process.env.WOMPI_INTEGRITY_SECRET!
        });
        return {
          gateway: "WOMPI",
          publicKey: process.env.WOMPI_PUBLIC_KEY,
          reference: input.orderId,
          amountInCents: input.amountInCents,
          signature
        };
      }
      return { gateway: input.paymentMethod, orderId: input.orderId };
    }
  })
};
