import { z } from "zod";

export const BantDetailsSchema = z.object({
  budgetStatus: z.enum(["confirmed", "elastic", "insufficient", "unknown"]),
  budgetAmount: z.number().optional(),
  currency: z.enum(["COP", "USD"]).default("COP"),
  authorityLevel: z.enum([
    "sole_decision_maker",
    "economic_buyer",
    "influencer",
    "champion",
    "gatekeeper",
    "unknown"
  ]),
  needUrgency: z.enum(["critical_urgency", "moderate", "low_nice_to_have", "unclear"]),
  painDescription: z.string().min(5),
  timingWindow: z.enum(["immediate", "short_term", "medium_term", "long_term", "unknown"])
});

export const ChampDetailsSchema = z.object({
  challenges: z.array(z.string()).min(1),
  primaryChallenge: z.string(),
  authorityProcess: z.string(),
  moneyPath: z.string(),
  prioritizationLevel: z.enum(["top_1", "top_3", "backlog", "low"])
});

export const LeadScoreBreakdownSchema = z.object({
  explicitScore: z.number().min(0).max(100),
  implicitScore: z.number().min(0).max(100),
  semanticScore: z.number().min(0).max(100),
  totalScore: z.number().min(0).max(100),
  grade: z.enum(["A_HOT", "B_WARM", "C_NURTURE", "D_COLD"])
});

export const BattlecardObjectionSchema = z.object({
  objectionType: z.enum(["price", "competitor", "trust", "guarantee", "payment_methods"]),
  detectedKeywords: z.array(z.string()),
  coreAngle: z.string(),
  script: z.string(),
  proofPoints: z.array(z.string())
});

export const HandoverBriefingSchema = z.object({
  leadId: z.string().uuid(),
  contactName: z.string(),
  contactPhone: z.string(),
  totalScore: z.number(),
  grade: z.enum(["A_HOT", "B_WARM", "C_NURTURE", "D_COLD"]),
  summary: z.string(),
  recommendedOffer: z.string()
});
