import crypto from "node:crypto";
import Redis from "ioredis";

export interface OtpGenerationResult {
  orderId: string;
  phone: string;
  otp: string;
  expiresInSeconds: number;
}

export interface OtpVerificationResult {
  success: boolean;
  orderId: string;
  reason?: "EXPIRED" | "INVALID_CODE" | "MAX_ATTEMPTS_EXCEEDED" | "ALREADY_VERIFIED";
  remainingAttempts?: number;
}

export class CodOtpManager {
  private redis: Redis;

  constructor(redisClientOrUrl: Redis | string = process.env.VALKEY_URL || "redis://cache:6379") {
    if (typeof redisClientOrUrl === "string") {
      this.redis = new Redis(redisClientOrUrl);
    } else {
      this.redis = redisClientOrUrl;
    }
  }

  private getOtpKey(orderId: string): string {
    return `cod:otp:${orderId}`;
  }

  private getAttemptsKey(orderId: string): string {
    return `cod:otp:attempts:${orderId}`;
  }

  private getVerifiedKey(orderId: string): string {
    return `cod:verified:${orderId}`;
  }

  async generateOtp(orderId: string, phone: string, ttlSeconds: number = 300): Promise<OtpGenerationResult> {
    // Generate cryptographically secure 6-digit integer
    const otpNumber = crypto.randomInt(100000, 1000000);
    const otp = otpNumber.toString();

    const otpKey = this.getOtpKey(orderId);
    const attemptsKey = this.getAttemptsKey(orderId);

    // Save hashed OTP or raw OTP with short TTL
    await this.redis.set(otpKey, otp, "EX", ttlSeconds);
    await this.redis.set(attemptsKey, "0", "EX", ttlSeconds);

    return {
      orderId,
      phone,
      otp, // Dispatched to WhatsApp / SMS gateway
      expiresInSeconds: ttlSeconds,
    };
  }

  async verifyOtp(orderId: string, submittedCode: string, maxAttempts: number = 3): Promise<OtpVerificationResult> {
    const verifiedKey = this.getVerifiedKey(orderId);
    const isAlreadyVerified = await this.redis.get(verifiedKey);
    if (isAlreadyVerified) {
      return { success: true, orderId };
    }

    const otpKey = this.getOtpKey(orderId);
    const attemptsKey = this.getAttemptsKey(orderId);

    const storedOtp = await this.redis.get(otpKey);
    if (!storedOtp) {
      return { success: false, orderId, reason: "EXPIRED" };
    }

    const currentAttempts = await this.redis.incr(attemptsKey);
    if (currentAttempts > maxAttempts) {
      await this.redis.del(otpKey);
      return { success: false, orderId, reason: "MAX_ATTEMPTS_EXCEEDED", remainingAttempts: 0 };
    }

    // Timing-safe buffer comparison to prevent timing attacks
    const storedBuf = Buffer.from(storedOtp, "utf-8");
    const submittedBuf = Buffer.from(submittedCode.trim(), "utf-8");

    const isMatch =
      storedBuf.length === submittedBuf.length && crypto.timingSafeEqual(storedBuf, submittedBuf);

    if (isMatch) {
      // Mark verified for 24 hours, delete temporary keys
      await this.redis.set(verifiedKey, "1", "EX", 86400);
      await this.redis.del(otpKey);
      await this.redis.del(attemptsKey);
      return { success: true, orderId };
    }

    const remaining = Math.max(0, maxAttempts - currentAttempts);
    return {
      success: false,
      orderId,
      reason: "INVALID_CODE",
      remainingAttempts: remaining,
    };
  }
}
