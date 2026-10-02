import { type z } from "zod";
import { CrmDealPayloadSchema } from "./sales_zod_schemas";

export type CrmDealPayload = z.infer<typeof CrmDealPayloadSchema>;

export interface CrmDealResult {
  success: boolean;
  dealId: string;
  provider: "directus" | "postgres" | "webhook";
  raw?: unknown;
}

export interface ICrmAdapter {
  createDeal(payload: CrmDealPayload): Promise<CrmDealResult>;
  updateLeadScore(leadId: string, score: number, grade: string): Promise<boolean>;
}

export class DirectusCrmAdapter implements ICrmAdapter {
  private url: string;
  private token: string;

  constructor(url = process.env.DIRECTUS_URL || "http://directus:8055", token = process.env.DIRECTUS_SERVER_TOKEN || "") {
    this.url = url;
    this.token = token;
  }

  async createDeal(payload: CrmDealPayload): Promise<CrmDealResult> {
    const validated = CrmDealPayloadSchema.parse(payload);
    const res = await fetch(`${this.url}/items/crm_deals`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(this.token ? { Authorization: `Bearer ${this.token}` } : {})
      },
      body: JSON.stringify({
        lead_id: validated.leadId,
        title: validated.title,
        status: validated.status,
        priority: validated.priority,
        notes: validated.notes,
        phone: validated.phone,
        email: validated.email,
        recommended_offer: validated.recommendedOffer,
        score: validated.score
      })
    });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(`[Directus CRM Error] HTTP ${res.status}: ${err}`);
    }

    const data = await res.json() as { data?: { id?: string } };
    return {
      success: true,
      dealId: data?.data?.id || validated.leadId,
      provider: "directus",
      raw: data
    };
  }

  async updateLeadScore(leadId: string, score: number, grade: string): Promise<boolean> {
    const res = await fetch(`${this.url}/items/leads/${leadId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        ...(this.token ? { Authorization: `Bearer ${this.token}` } : {})
      },
      body: JSON.stringify({ score, grade })
    });
    return res.ok;
  }
}

export class WebhookCrmAdapter implements ICrmAdapter {
  private webhookUrl: string;

  constructor(webhookUrl = process.env.CRM_WEBHOOK_URL || "") {
    this.webhookUrl = webhookUrl;
  }

  async createDeal(payload: CrmDealPayload): Promise<CrmDealResult> {
    if (!this.webhookUrl) {
      console.warn("[Webhook CRM] No webhook URL configured, returning synthetic success.");
      return { success: true, dealId: `deal_${Date.now()}`, provider: "webhook" };
    }

    const res = await fetch(this.webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event: "crm.deal.created", data: payload })
    });

    if (!res.ok) {
      throw new Error(`[Webhook CRM Error] HTTP ${res.status}`);
    }

    return { success: true, dealId: payload.leadId, provider: "webhook" };
  }

  async updateLeadScore(leadId: string, score: number, grade: string): Promise<boolean> {
    if (!this.webhookUrl) return true;
    const res = await fetch(this.webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event: "crm.lead.scored", data: { leadId, score, grade } })
    });
    return res.ok;
  }
}

export async function createDirectusDeal(params: {
  leadId: string;
  contactName: string;
  contactPhone: string;
  totalScore: number;
  grade: string;
  summary: string;
  recommendedOffer: string;
}) {
  const adapter = new DirectusCrmAdapter();
  return await adapter.createDeal({
    leadId: params.leadId,
    title: `Qualified Lead: ${params.contactName} (${params.grade})`,
    status: "qualified",
    priority: params.grade === "A_HOT" ? "high" : "normal",
    notes: params.summary,
    phone: params.contactPhone,
    recommendedOffer: params.recommendedOffer,
    score: params.totalScore
  });
}
