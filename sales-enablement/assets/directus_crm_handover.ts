export async function createDirectusDeal(params: {
  leadId: string;
  contactName: string;
  contactPhone: string;
  totalScore: number;
  grade: string;
  summary: string;
  recommendedOffer: string;
}) {
  const directusUrl = process.env.DIRECTUS_URL || "http://directus:8055";
  const token = process.env.DIRECTUS_SERVER_TOKEN;

  const res = await fetch(`${directusUrl}/items/crm_deals`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({
      lead_id: params.leadId,
      title: `Lead Calificado: ${params.contactName} (${params.grade})`,
      status: "pending_assignment",
      priority: params.grade === "A_HOT" ? "high" : "normal",
      notes: params.summary,
      phone: params.contactPhone,
      recommended_offer: params.recommendedOffer,
      score: params.totalScore
    })
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`[Directus CRM Error] HTTP ${res.status}: ${err}`);
  }

  return await res.json();
}
