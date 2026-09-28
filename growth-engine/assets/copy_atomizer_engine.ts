import { generateObject } from "ai";
import { anthropic } from "@ai-sdk/anthropic";
import {
  PillarContentInput,
  OmnichannelAtomizationBundle,
  OmnichannelAtomizationBundleSchema
} from "./copywriting_zod_schemas";

export async function atomizePillarContent(pillar: PillarContentInput): Promise<OmnichannelAtomizationBundle> {
  const { object } = await generateObject({
    model: anthropic(process.env.DEFAULT_COPY_MODEL || "claude-3-7-sonnet-20250219"),
    schema: OmnichannelAtomizationBundleSchema,
    prompt: `
      Eres el Director Creativo de Copywriting Vanguard para el mercado de Colombia y Latinoamérica.
      Tu misión es transformar el siguiente Contenido Pilar en un paquete de copys omnicanal de alta conversión.

      DIRECTIVAS PSICOLÓGICAS Y DE CONVERSIÓN:
      1. StoryBrand SB7: El cliente siempre es el héroe; la marca es el guía empático y con autoridad.
      2. Ecuación de Hormozi: Comunica el resultado soñado, minimiza el esfuerzo a "copiar y pegar" y asegura un Quick Win en 24h.
      3. Vacuna Anti-Fraude LatAm: Enfatiza la garantía total incondicional de 30 días, la presencia de soporte humano en WhatsApp y opciones de pago locales familiares (PSE, Nequi, Contra Entrega).
      4. Tono: Cálido, respetuoso, empático y directo. Cero frialdad robótica o anglicismos forzados.

      INPUT DEL CONTENIDO PILAR:
      - Título: ${pillar.title}
      - Eje Temático: ${pillar.coreTheme}
      - Audiencia: ${pillar.targetAudience.role} en ${pillar.targetAudience.industry} (${pillar.targetAudience.marketRegion})
      - Dolor Principal: ${pillar.targetAudience.primaryPainPoint}
      - Resultado Soñado: ${pillar.targetAudience.dreamOutcome}
      - Historia de Epifanía:
        * Punto Bajo: ${pillar.epiphanyStory.lowPoint}
        * Mecanismo Revelador: ${pillar.epiphanyStory.breakthroughMoment}
        * Resultado Tangible: ${pillar.epiphanyStory.tangibleResult}
      - Oferta: ${pillar.primaryOffer.name}
        * Quick Win: ${pillar.primaryOffer.quickWinTimeframe}
        * Garantía: ${pillar.primaryOffer.riskReversalGuarantee}
        * CTA: ${pillar.primaryOffer.ctaText} (${pillar.primaryOffer.ctaUrlOrKeyword})

      Genera todos los bloques requeridos por el esquema Zod.
    `
  });

  return object;
}
