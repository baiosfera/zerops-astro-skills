import crypto from "node:crypto";
import { TurnstileVerifyResponseSchema, type TurnstileVerifyResponse } from "./dns_zod_schemas";

export interface TurnstileValidateParams {
  token: string;
  secretKey?: string;
  remoteIp?: string;
  idempotencyKey?: string;
  timeoutMs?: number;
}

export async function validateTurnstileToken(params: TurnstileValidateParams): Promise<TurnstileVerifyResponse> {
  const secret = params.secretKey || process.env.TURNSTILE_SECRET_KEY;
  if (!secret) {
    throw new Error("[Turnstile Error] TURNSTILE_SECRET_KEY is not configured.");
  }

  if (!params.token || params.token.length > 2048) {
    return {
      success: false,
      "error-codes": ["invalid-input-response"],
    };
  }

  const idempotencyKey = params.idempotencyKey || crypto.randomUUID();
  const formData = new URLSearchParams();
  formData.append("secret", secret);
  formData.append("response", params.token);
  formData.append("idempotency_key", idempotencyKey);
  if (params.remoteIp) {
    formData.append("remoteip", params.remoteIp);
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), params.timeoutMs || 5000);

  try {
    const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST",
      body: formData,
      signal: controller.signal,
    });

    const data = await res.json();
    return TurnstileVerifyResponseSchema.parse(data);
  } catch (err) {
    const isAbort = (err as Error).name === "AbortError";
    return {
      success: false,
      "error-codes": [isAbort ? "timeout" : "internal-error"],
    };
  } finally {
    clearTimeout(timeoutId);
  }
}
