# Sovereign Growth Engine: Comprehensive Usage Guide & Engineering Reference (v2.0)

## 1. Brand SSoT Ingestion & Voice Calibration (Decoupled Provider)

Commercial copy and cart recovery sequences inherit voice guidelines dynamically from an agnostic brand provider rather than fixed client-specific paths.

```typescript
import fs from "node:fs";
import path from "node:path";

export interface BrandVoiceProfile {
  brandName: string;
  archetype: string;
  toneGuidelines: string[];
  rejectedJargon: string[];
  targetAudience: {
    role: string;
    industry: string;
    primaryPainPoint: string;
    dreamOutcome: string;
  };
}

export function getBrandVoiceContext(customPath?: string): BrandVoiceProfile {
  const candidatePaths = [
    customPath,
    process.env.BRAND_SSOT_PATH,
    path.resolve(process.cwd(), "src/config/brand.json"),
    path.resolve(process.cwd(), "brand.json")
  ].filter(Boolean) as string[];

  for (const filePath of candidatePaths) {
    if (fs.existsSync(filePath)) {
      try {
        const raw = fs.readFileSync(filePath, "utf-8");
        if (filePath.endsWith(".json")) {
          const parsed = JSON.parse(raw);
          return {
            brandName: parsed.name || "Default Brand",
            archetype: parsed.archetype || "The Guide",
            toneGuidelines: parsed.tone || ["Empathetic", "Direct", "Authoritative"],
            rejectedJargon: parsed.rejectedJargon || ["generic buzzwords", "hype"],
            targetAudience: parsed.targetAudience || {
              role: "Professional",
              industry: "General",
              primaryPainPoint: "Operational friction",
              dreamOutcome: "Seamless excellence"
            }
          };
        }
      } catch (err) {
        console.warn(`[growth-engine] Warning reading brand file at ${filePath}:`, err);
      }
    }
  }

  return {
    brandName: "Sovereign Brand",
    archetype: "The Guide / Quiet Luxury",
    toneGuidelines: ["Direct", "Empathetic", "Data-driven"],
    rejectedJargon: ["cheap", "miracle", "act now"],
    targetAudience: {
      role: "Customer",
      industry: "E-Commerce",
      primaryPainPoint: "Unresolved needs",
      dreamOutcome: "Flawless solution"
    }
  };
}
```

---

## 2. Behavioral Cart Recovery with Fencing Tokens

### 2.1. Lead Capture on Input Blur (Astro Actions)
Capture contact information progressively as customers interact with checkout inputs:

```typescript
// src/actions/growth.ts
import { defineAction } from "astro:actions";
import { z } from "astro/zod";
import { stageAbandonedCartLead } from "../lib/growth/cart-staging";

export const server = {
  captureCartLead: defineAction({
    accept: "json",
    input: z.object({
      cartId: z.string().uuid(),
      email: z.string().email().optional(),
      phone: z.string().min(7).max(20).optional(),
      cartItems: z.array(z.object({
        sku: z.string(),
        title: z.string(),
        quantity: z.number().int().positive(),
        unitPrice: z.number().nonnegative()
      })),
      currency: z.string().length(3).default("USD"),
      grossMargin: z.number().min(0).max(1).default(0.4)
    }),
    handler: async (input) => {
      return await stageAbandonedCartLead(input);
    }
  })
};
```

### 2.2. Valkey Staging with Monotonic Version Counters
Each mutation increments `cart_version`. This allows delayed background workers to discard stale jobs:

```typescript
// src/lib/growth/cart-staging.ts
import type { Redis } from "ioredis";

export async function stageAbandonedCartLead(
  redis: Redis,
  cartData: {
    cartId: string;
    email?: string;
    phone?: string;
    cartItems: any[];
    currency: string;
    grossMargin: number;
  }
): Promise<{ version: number }> {
  const key = `cart:abandoned:${cartData.cartId}`;
  
  // Pipeline: Increment version and update fields atomically
  const results = await redis
    .multi()
    .hincrby(key, "version", 1)
    .hset(key, {
      cartId: cartData.cartId,
      email: cartData.email || "",
      phone: cartData.phone || "",
      items: JSON.stringify(cartData.cartItems),
      currency: cartData.currency,
      grossMargin: cartData.grossMargin.toString(),
      status: "ABANDONED_PENDING",
      updatedAt: Date.now().toString()
    })
    .expire(key, 86400) // 24 hours TTL
    .exec();

  const newVersion = (results?.[0]?.[1] as number) || 1;
  return { version: newVersion };
}
```

### 2.3. BullMQ Worker Self-Discarding Fencing Logic
```typescript
// src/workers/cart-recovery-worker.ts
import { Worker, Job } from "bullmq";
import type { Redis } from "ioredis";

export interface CartRecoveryJobPayload {
  cartId: string;
  jobVersion: number;
  attempt: 1 | 2 | 3;
}

export function createCartRecoveryWorker(redis: Redis, connection: any) {
  return new Worker<CartRecoveryJobPayload>(
    "cart-recovery",
    async (job: Job<CartRecoveryJobPayload>) => {
      const { cartId, jobVersion, attempt } = job.data;
      const key = `cart:abandoned:${cartId}`;
      const record = await redis.hgetall(key);

      // FENCING CHECK: If cart is empty, already converted, or modified post-schedule -> DISCARD
      if (!record || !record.cartId) {
        return { status: "DISCARDED", reason: "CART_EXPIRED" };
      }
      if (record.status === "CONVERTED") {
        return { status: "DISCARDED", reason: "ALREADY_CONVERTED" };
      }
      const currentVersion = parseInt(record.version || "0", 10);
      if (currentVersion !== jobVersion) {
        return { status: "DISCARDED", reason: "STALE_VERSION", currentVersion, jobVersion };
      }

      // Calculate safe dynamic discount ceiling
      const margin = parseFloat(record.grossMargin || "0.4");
      const discount = calculateBoundedDiscount({
        grossMargin: margin,
        ltvTier: "STANDARD",
        attemptNumber: attempt
      });

      // Dispatch recovery message via NATS or Email/WhatsApp provider
      console.log(`[growth-engine] Dispatching Attempt ${attempt} for cart ${cartId} with ${discount * 100}% discount ceiling.`);
      return { status: "DISPATCHED", cartId, attempt, discount };
    },
    { connection }
  );
}
```

### 2.4. Mathematical Dynamic Capped Discounting Algorithm
Discounts protect gross profit margins and prevent shopper discount harvesting:

$$\text{Discount Ceil} = \min(\text{Gross Margin} - 0.05, \, \text{LTV Tier Cap}, \, \text{Attempt Ceiling})$$

```typescript
export interface DiscountCalculationParams {
  grossMargin: number; // e.g. 0.50 (50%)
  ltvTier?: "NEW" | "STANDARD" | "VIP";
  attemptNumber: 1 | 2 | 3;
}

export function calculateBoundedDiscount(params: DiscountCalculationParams): number {
  const { grossMargin, ltvTier = "STANDARD", attemptNumber } = params;

  // Margin cap preserves a minimum 5% net margin
  const marginCap = Math.max(0, grossMargin - 0.05);

  // Attempt ceilings
  const attemptCaps: Record<number, number> = {
    1: 0.0,   // Attempt 1 (15-30m): Assistance / 0% discount
    2: 0.10,  // Attempt 2 (2-4h): 10% maximum
    3: 0.20   // Attempt 3 (24h): 20% absolute maximum
  };
  const attemptCap = attemptCaps[attemptNumber] ?? 0.0;

  // LTV caps
  const ltvCaps: Record<string, number> = {
    NEW: 0.10,
    STANDARD: 0.15,
    VIP: 0.20
  };
  const ltvCap = ltvCaps[ltvTier] ?? 0.15;

  // Final mathematically bounded discount
  return Number(Math.min(marginCap, attemptCap, ltvCap).toFixed(2));
}
```

---

## 3. High-Converting Copywriting Frameworks

### 3.1. StoryBrand 2.0 (Donald Miller — SB7)
The customer is the **Hero**; the brand is the **Guide**:
1. **Character**: Primary goal of the customer (status, time, security, growth).
2. **Problem (Three Layers)**:
   - *External (Tangible symptom)*: "Conversion rates drop 70% at the checkout form."
   - *Internal (Emotional friction)*: "Frustration of spending on ads only to lose customers at the final step."
   - *Philosophical (Unjust reality)*: "High-quality products deserve checkout flows that respect user trust."
3. **Meets a Guide (Your Brand)**:
   - *Empathy*: "We understand the relentless work behind every traffic campaign."
   - *Authority*: Proven architecture, sub-second latency, and validated case studies.
4. **Who Gives Them a 3-Step Plan**:
   - Step 1: Integrate the unified checkout island.
   - Step 2: Configure automated recovery with self-discarding fencing tokens.
   - Step 3: Monitor recoverable revenue in real-time.
5. **Calls Them to Action**: Direct CTA ("Deploy Checkout") and Transitional CTA ("Read Documentation").
6. **Helps Them Avoid Failure**: Wasted ad spend, cart drop-off, and customer churn.
7. **Ends in Success**: Predictable revenue growth, effortless customer trust, and maximum conversion.

### 3.2. Alex Hormozi $100M Offers Value Equation

$$\text{Perceived Value} = \frac{\text{Dream Outcome} \times \text{Perceived Likelihood of Achievement}}{\text{Time Delay} \times \text{Effort \& Sacrifice}}$$

- **Dream Outcome**: Articulate the customer's desired financial or personal transformation.
- **Perceived Likelihood**: Provide proof, case studies, benchmarks, and a 30-day unconditional risk reversal guarantee.
- **Time Delay (Minimize)**: Deliver a tangible Quick Win within 24–48 hours of onboarding.
- **Effort & Sacrifice (Minimize)**: Done-for-you scaffolding, one-click installation, and zero-effort migration.

### 3.3. P.A.S.T.O.R. Framework (Ray Edwards)
- **P - Problem / Person**: Name the customer and articulate their precise frustration.
- **A - Amplify**: Calculate the compounded financial and operational cost of inaction.
- **S - Story & Solution**: The breakthrough discovery and architecture that solves the root problem.
- **T - Transformation & Testimony**: Real-world benchmarks and quantifiable results.
- **O - Offer**: 80% outcome / 20% technical specifications.
- **R - Response**: Explicit, low-friction instructions on what to do next.

---

## 4. 2026 Anti-SPAM Deliverability Linter

Every commercial or recovery email must satisfy mailbox provider mandates (Google, Yahoo, Microsoft) before dispatch:

```typescript
export interface AntiSpamValidationResult {
  valid: boolean;
  score: number; // 0 to 100
  errors: string[];
  warnings: string[];
}

export function validateEmailCopy(subject: string, previewText: string, htmlBody: string): AntiSpamValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];
  let score = 100;

  // 1. Subject length check (30 - 50 characters, 4 - 7 words recommended)
  if (subject.length < 30 || subject.length > 50) {
    warnings.push(`Subject length (${subject.length} chars) is outside optimal 30-50 character range.`);
    score -= 10;
  }

  // 2. All-caps suppression
  const words = subject.split(/\s+/);
  const allCapsWords = words.filter(w => w.length > 3 && w === w.toUpperCase() && /[A-Z]/.test(w));
  if (allCapsWords.length > 0) {
    errors.push(`Subject contains forbidden ALL-CAPS words: ${allCapsWords.join(", ")}`);
    score -= 25;
  }

  // 3. Excessive punctuation
  if (/!{2,}|\?{2,}/.test(subject)) {
    errors.push("Subject contains multiple consecutive exclamation or question marks.");
    score -= 20;
  }

  // 4. Emoji count
  const emojiRegex = /[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/gu;
  const emojis = subject.match(emojiRegex) || [];
  if (emojis.length > 1) {
    warnings.push(`Subject contains ${emojis.length} emojis (maximum recommended: 1 contextual emoji).`);
    score -= 10;
  }

  // 5. Spam trigger words
  const spamTriggers = [
    /\bfree\b/i, /\bguaranteed\b/i, /\b100%\s*free\b/i,
    /\bact\s*now\b/i, /\burgent\b/i, /\binstant\s*cash\b/i
  ];
  for (const trigger of spamTriggers) {
    if (trigger.test(subject)) {
      errors.push(`Subject matches spam trigger: ${trigger.source}`);
      score -= 20;
    }
  }

  return {
    valid: errors.length === 0,
    score: Math.max(0, score),
    errors,
    warnings
  };
}
```

### 4.1. RFC 8058 One-Click List-Unsubscribe Headers
All automated emails must emit RFC 8058 headers:
```http
List-Unsubscribe: <https://api.example.com/v1/email/unsubscribe?token=jwt_token>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

---

## 5. Multi-Touch Attribution Engine (MTA)

Decoupled attribution calculation across marketing touchpoints:

```typescript
export interface Touchpoint {
  id: string;
  channel: string;
  source: string;
  campaign: string;
  timestamp: number;
}

export type AttributionModel = "FIRST_TOUCH" | "LAST_TOUCH" | "LINEAR" | "TIME_DECAY" | "U_SHAPED";

export function calculateAttribution(
  touchpoints: Touchpoint[],
  totalConversionValue: number,
  model: AttributionModel
): Record<string, number> {
  if (touchpoints.length === 0) return {};
  const attribution: Record<string, number> = {};
  touchpoints.forEach(tp => { attribution[tp.channel] = 0; });

  switch (model) {
    case "FIRST_TOUCH": {
      const first = touchpoints[0];
      attribution[first.channel] = totalConversionValue;
      break;
    }
    case "LAST_TOUCH": {
      const last = touchpoints[touchpoints.length - 1];
      attribution[last.channel] = totalConversionValue;
      break;
    }
    case "LINEAR": {
      const share = totalConversionValue / touchpoints.length;
      touchpoints.forEach(tp => {
        attribution[tp.channel] += Number(share.toFixed(2));
      });
      break;
    }
    case "TIME_DECAY": {
      const halfLifeDays = 7;
      const conversionTime = touchpoints[touchpoints.length - 1].timestamp;
      const weights = touchpoints.map(tp => {
        const daysDiff = (conversionTime - tp.timestamp) / (1000 * 60 * 60 * 24);
        return Math.pow(0.5, daysDiff / halfLifeDays);
      });
      const totalWeight = weights.reduce((a, b) => a + b, 0);
      touchpoints.forEach((tp, idx) => {
        attribution[tp.channel] += Number(((weights[idx] / totalWeight) * totalConversionValue).toFixed(2));
      });
      break;
    }
    case "U_SHAPED": {
      if (touchpoints.length === 1) {
        attribution[touchpoints[0].channel] = totalConversionValue;
      } else if (touchpoints.length === 2) {
        attribution[touchpoints[0].channel] = totalConversionValue * 0.5;
        attribution[touchpoints[1].channel] = totalConversionValue * 0.5;
      } else {
        const firstShare = totalConversionValue * 0.4;
        const lastShare = totalConversionValue * 0.4;
        const middleShare = (totalConversionValue * 0.2) / (touchpoints.length - 2);

        attribution[touchpoints[0].channel] += firstShare;
        attribution[touchpoints[touchpoints.length - 1].channel] += lastShare;
        for (let i = 1; i < touchpoints.length - 1; i++) {
          attribution[touchpoints[i].channel] += Number(middleShare.toFixed(2));
        }
      }
      break;
    }
  }

  return attribution;
}
```

---

## 6. Decoupled Commerce Service Provider Interfaces (SPIs)

```typescript
export interface PaymentGatewayProvider {
  verifyWebhookSignature(headers: Record<string, string>, rawBody: Buffer, secret: string): boolean;
  createCheckoutSession(cart: { id: string; amount: number; currency: string }): Promise<{ checkoutUrl: string; sessionId: string }>;
}

export interface FulfillmentCarrierAdapter {
  generateWaybill(order: { id: string; recipient: any; items: any[] }): Promise<{ trackingNumber: string; labelUrl: string }>;
  getTrackingStatus(trackingNumber: string): Promise<{ status: string; estimatedDelivery?: string }>;
}

export interface InvoicingProvider {
  createLegalInvoice(order: { id: string; amount: number; tax: number; customer: any }): Promise<{ invoiceId: string; pdfUrl: string }>;
}

---

## 7. High-Ticket Positioning & Lexical Cleanse (Anti-Slop Sovereign Copy)

### 7.1 High-Ticket Filter Mechanism
For high-end or restricted-access communities, events, or VIP memberships:
- Transparently state the high-ticket price range and exclusive cover costs early in the landing and email narrative.
- Use explicit admission criteria and premium pricing as a natural filter, eliminating unqualified leads before manual reviews.

### 7.2 Secular & Anti-Slop Lexical Guidelines
- Replace pretentious jargon: replace "Curaduría" with "Dirección Artística" or "Producción Cultural".
- Replace ambiguous staff titles: replace "Anfitrión/a" with "Equipo Organizador" or "Personal de Sala".
- Eradicate pseudospiritual or dogmatic buzzwords ("sagrado", "sacrosanto") in favor of secular sovereign terms ("fundamental", "innegociable", "consentimiento informado").

