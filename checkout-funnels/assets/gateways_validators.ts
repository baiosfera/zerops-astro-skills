import { z } from "zod";
import crypto from "node:crypto";

// ============================================================================
// 1. WOMPI COLOMBIA
// ============================================================================

export const WompiTransactionInputSchema = z.object({
  amount_in_cents: z.number().int().positive(),
  currency: z.literal("COP"),
  customer_email: z.string().email(),
  reference: z.string().min(1).max(255),
  public_key: z.string().startsWith("pub_"),
  signature: z.string().length(64),
  redirect_url: z.string().url().optional(),
  expiration_time: z.string().datetime().optional()
});

export function generateWompiIntegritySignature(params: {
  reference: string;
  amountInCents: number;
  currency: string;
  integritySecret: string;
  expirationTime?: string;
}): string {
  const raw = params.expirationTime
    ? `${params.reference}${params.amountInCents}${params.currency}${params.expirationTime}${params.integritySecret}`
    : `${params.reference}${params.amountInCents}${params.currency}${params.integritySecret}`;
  return crypto.createHash("sha256").update(raw).digest("hex");
}

export function verifyWompiWebhookChecksum(
  payload: {
    data: Record<string, any>;
    signature: { properties: string[]; checksum: string };
    timestamp: number;
  },
  eventsSecret: string
): boolean {
  const { properties, checksum } = payload.signature;
  const values = properties.map((propPath) => {
    const keys = propPath.split(".");
    let current: any = payload.data;
    for (const key of keys) {
      if (current === undefined || current === null) return "";
      current = current[key];
    }
    return String(current);
  });
  const concatenated = values.join("") + payload.timestamp + eventsSecret;
  const calculated = crypto.createHash("sha256").update(concatenated).digest("hex");
  return calculated.toLowerCase() === checksum.toLowerCase();
}

// ============================================================================
// 2. EPAYCO
// ============================================================================

export function verifyEpaycoSignature(params: {
  customerId: string;
  pKey: string;
  refPayco: string;
  transactionId: string;
  amount: string;
  currencyCode: string;
  signatureReceived: string;
}): boolean {
  const raw = `${params.customerId}^${params.pKey}^${params.refPayco}^${params.transactionId}^${params.amount}^${params.currencyCode}`;
  const calculated = crypto.createHash("sha256").update(raw).digest("hex");
  return calculated.toLowerCase() === params.signatureReceived.toLowerCase();
}

// ============================================================================
// 3. DLOCAL GO
// ============================================================================

export function verifyDLocalSignature(params: {
  secretKey: string;
  apiKey: string;
  timestamp: string;
  rawBody: string;
  headerSignature: string;
}): boolean {
  const message = `${params.apiKey}${params.timestamp}${params.rawBody}`;
  const calculated = crypto.createHmac("sha256", params.secretKey).update(message).digest("hex");
  return calculated.toLowerCase() === params.headerSignature.toLowerCase();
}
