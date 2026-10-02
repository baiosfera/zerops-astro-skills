import {
  type PillarContentInput,
  type OmnichannelAtomizationBundle,
  OmnichannelAtomizationBundleSchema
} from "./copywriting_zod_schemas";

export async function atomizePillarContent(
  pillar: PillarContentInput,
  options?: { bifrostUrl?: string; model?: string; apiKey?: string }
): Promise<OmnichannelAtomizationBundle> {
  const endpoint = options?.bifrostUrl || process.env.BIFROST_URL || "http://bifrost:8080/v1";
  const model = options?.model || process.env.DEFAULT_COPY_MODEL || "claude-3-7-sonnet";
  const apiKey = options?.apiKey || process.env.BIFROST_API_KEY || "dummy-key";

  const systemPrompt = `You are an elite conversion copywriter and growth architect.
Your mission is to transform the provided Pillar Content into a high-converting, omnichannel copy bundle.

PSYCHOLOGICAL AND ARCHITECTURAL DIRECTIVES:
1. StoryBrand SB7: The customer is always the Hero; the brand is the empathetic, authoritative Guide.
2. Hormozi Value Equation: Vividly convey the dream outcome, minimize friction and perceived effort, and deliver an immediate 24-48h quick win.
3. Risk Reversal: Highlight unconditional guarantees, human support availability, and low-friction access.
4. Tone & Style: Authentic, compelling, empathetic, and clear. Zero generic buzzwords, zero artificial hype.
5. Strict JSON Output: Output MUST strictly adhere to the requested schema. Return raw valid JSON only.`;

  const userPrompt = `INPUT PILLAR CONTENT:
- Title: ${pillar.title}
- Core Theme: ${pillar.coreTheme}
- Target Audience: ${pillar.targetAudience.role} in ${pillar.targetAudience.industry} (Locale: ${pillar.targetAudience.locale})
- Primary Pain Point: ${pillar.targetAudience.primaryPainPoint}
- Dream Outcome: ${pillar.targetAudience.dreamOutcome}
- Epiphany Story:
  * Low Point: ${pillar.epiphanyStory.lowPoint}
  * Breakthrough: ${pillar.epiphanyStory.breakthroughMoment}
  * Tangible Result: ${pillar.epiphanyStory.tangibleResult}
- Offer: ${pillar.primaryOffer.name}
  * Quick Win: ${pillar.primaryOffer.quickWinTimeframe}
  * Guarantee: ${pillar.primaryOffer.riskReversalGuarantee}
  * CTA: ${pillar.primaryOffer.ctaText} (${pillar.primaryOffer.ctaUrlOrKeyword})
  * Price & Currency: ${pillar.primaryOffer.price ?? "N/A"} ${pillar.primaryOffer.currency}

Generate the complete omnichannel package matching the Zod schema.`;

  const response = await fetch(`${endpoint}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt }
      ],
      response_format: { type: "json_object" },
      temperature: 0.65
    })
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`[growth-engine] Bifrost error ${response.status}: ${errorText}`);
  }

  const completion = await response.json();
  const rawContent = completion?.choices?.[0]?.message?.content;
  if (!rawContent) {
    throw new Error("[growth-engine] Received empty response from Bifrost gateway");
  }

  const parsedJson = JSON.parse(rawContent);
  return OmnichannelAtomizationBundleSchema.parse(parsedJson);
}
