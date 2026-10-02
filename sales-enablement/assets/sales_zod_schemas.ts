import { z } from "zod";

export const BantDetailsSchema = z.object({
  budgetStatus: z.enum(["confirmed", "elastic", "insufficient", "unknown"]),
  budgetAmount: z.number().nonnegative().optional(),
  currency: z.string().length(3).default("USD"),
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
  primaryChallenge: z.string().min(3),
  authorityProcess: z.string().min(3),
  moneyPath: z.string().min(3),
  prioritizationLevel: z.enum(["top_1", "top_3", "backlog", "low"])
});

export const MeddpiccDetailsSchema = z.object({
  metrics: z.array(z.string()).min(1),
  economicBuyer: z.string().min(3),
  decisionCriteria: z.array(z.string()).min(1),
  decisionProcess: z.string().min(3),
  paperProcess: z.string().min(3),
  identifiedPain: z.string().min(3),
  champion: z.string().min(3),
  competition: z.array(z.string()).default([])
});

export const LeadScoreBreakdownSchema = z.object({
  explicitScore: z.number().min(0).max(100),
  implicitScore: z.number().min(0).max(100),
  semanticScore: z.number().min(0).max(100),
  totalScore: z.number().min(0).max(100),
  grade: z.enum(["A_HOT", "B_WARM", "C_NURTURE", "D_COLD"])
});

export const BattlecardObjectionSchema = z.object({
  objectionType: z.enum(["price", "competitor", "trust", "guarantee", "timing", "features"]),
  detectedKeywords: z.array(z.string()),
  coreAngle: z.string(),
  script: z.string(),
  proofPoints: z.array(z.string())
});

export const HandoverBriefingSchema = z.object({
  leadId: z.string().uuid(),
  contactName: z.string().min(1),
  contactEmail: z.string().email().optional(),
  contactPhone: z.string().min(5),
  totalScore: z.number().min(0).max(100),
  grade: z.enum(["A_HOT", "B_WARM", "C_NURTURE", "D_COLD"]),
  qualificationFramework: z.enum(["BANT", "CHAMP", "MEDDPICC"]),
  summary: z.string().min(10),
  recommendedOffer: z.string().min(3)
});

export const CrmDealPayloadSchema = z.object({
  leadId: z.string(),
  title: z.string(),
  status: z.enum(["new", "qualified", "in_progress", "won", "lost"]).default("qualified"),
  priority: z.enum(["low", "normal", "high", "urgent"]).default("normal"),
  notes: z.string(),
  phone: z.string(),
  email: z.string().optional(),
  recommendedOffer: z.string(),
  score: z.number()
});
