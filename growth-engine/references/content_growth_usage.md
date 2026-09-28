# `growth-content`: Comprehensive Usage Guide, Contracts & Implementation Recipes

> **SSoT Reference Document:** `/var/www/.agents/skills/growth-content/references/usage.md`  
> **Meta-Skill:** [`growth-content`](file:///var/www/.agents/skills/growth-content/SKILL.md)  
> **Standard:** CoHaLo v6.7, Supreme Directive v6.7, Neurocopywriting & AI-Search Optimization.

---

## 1. Sub-Skills Inventory & Physical File Pointers

* **Neurocopywriting & Offer Architecture:** [`copywriting-vanguard`](file:///var/www/.agents/skills/copywriting-vanguard/SKILL.md) ([usage](file:///var/www/.agents/skills/copywriting-vanguard/references/usage.md)).
* **SEO, AEO & Knowledge Graph:** [`seo-aeo-geo`](file:///var/www/.agents/skills/seo-aeo-geo/SKILL.md) ([usage](file:///var/www/.agents/skills/seo-aeo-geo/references/usage.md)).
* **Social Distribution Delegation:** [`social-distrib`](file:///var/www/.agents/skills/social-distrib/SKILL.md) ([usage](file:///var/www/.agents/skills/social-distrib/references/usage.md), [infra](file:///var/www/.agents/skills/social-distrib/references/infra.md)).

---

## 2. TypeScript / Zod Contract: Atomized Offer & Copywriting Structure

This schema defines the typed structure for Product Detail Pages (PDP) combining **StoryBrand 2.0** and **Hormozi's Value Equation**:

```typescript
// src/schemas/product-copywriting.ts
import { z } from 'astro:schema';

export const HormoziValueEquationSchema = z.object({
  dreamOutcome: z.string().describe('The emotional and tangible final result desired by the customer'),
  perceivedLikelihoodOfAchievement: z.string().describe('Social proof, guarantees, and case studies maximizing trust'),
  timeDelayReduction: z.string().describe('Speed of fulfillment or delivery timeline (e.g., Same-day dispatch / 24-48h delivery)'),
  effortSacrificeReduction: z.string().describe('Ease of adoption, friction-free onboarding or setup'),
  grandSlamOfferName: z.string().describe('Magnetic name for the core offer bundle (e.g., Ultimate Starter Kit + Free Priority Shipping)'),
  scarcityUrgencyHook: z.string().optional().describe('Limited batch quantity or countdown deadline'),
  riskReversalGuarantee: z.string().describe('Unconditional risk reversal (e.g., 30-day no-questions-asked full refund guarantee)'),
});

export const StoryBrandPDPContentSchema = z.object({
  characterHero: z.object({
    identity: z.string().describe('The ideal customer persona and core aspiration'),
    villain: z.string().describe('The primary antagonist causing friction and pain'),
  }),
  problemLayers: z.object({
    external: z.string().describe('Tangible physical problem'),
    internal: z.string().describe('Emotional impact and frustrations felt by the user'),
    philosophical: z.string().describe('Why it is fundamentally unjust to suffer this problem'),
  }),
  guideAuthority: z.object({
    empathyStatement: z.string().describe('Empathetic message connecting with customer struggles'),
    authorityProof: z.string().describe('Social metrics, awards, reviews, or brand credentials'),
  }),
  threeStepPlan: z.array(z.object({
    stepNumber: z.number().int().min(1).max(3),
    title: z.string(),
    description: z.string(),
  })).length(3),
  callsToAction: z.object({
    directCTA: z.string().describe('Primary button: Buy Now / Order Cash on Delivery'),
    transitionalCTA: z.string().optional().describe('Secondary button: Download Guide / Chat on WhatsApp'),
  }),
  valueEquation: HormoziValueEquationSchema,
});

export type StoryBrandPDPContent = z.infer<typeof StoryBrandPDPContentSchema>;
```

---

## 3. Schema.org JSON-LD Generator for Astro 5 SSR

Component to inject structured metadata into the page `<head>` ensuring optimal visibility in Google Rich Snippets and AI search engines (Perplexity, ChatGPT Search, SearchGPT):

```typescript
// src/components/seo/ProductJsonLd.astro
---
interface Props {
  title: string;
  description: string;
  price: number;
  currency: string;
  sku: string;
  images: string[];
  inStock: boolean;
  brandName: string;
  ratingValue?: number;
  reviewCount?: number;
}

const {
  title,
  description,
  price,
  currency = 'COP',
  sku,
  images,
  inStock,
  brandName,
  ratingValue = 4.9,
  reviewCount = 128,
} = Astro.props;

const schemaData = {
  '@context': 'https://schema.org/',
  '@type': 'Product',
  name: title,
  image: images,
  description: description,
  sku: sku,
  brand: {
    '@type': 'Brand',
    name: brandName,
  },
  offers: {
    '@type': 'Offer',
    url: Astro.url.href,
    priceCurrency: currency,
    price: price,
    priceValidUntil: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    itemCondition: 'https://schema.org/NewCondition',
    availability: inStock ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock',
    seller: {
      '@type': 'Organization',
      name: brandName,
    },
  },
  aggregateRating: {
    '@type': 'AggregateRating',
    ratingValue: ratingValue,
    reviewCount: reviewCount,
  },
};
---
<script type="application/ld+json" set:html={JSON.stringify(schemaData)} />
```

---

## 4. Static `llms.txt` Endpoint for AI Crawlers

Astro 5 route exposing key catalog and policy documentation to AI agentic crawlers:

```typescript
// src/pages/llms.txt.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  const content = `# Sovereign E-Commerce Platform ($0 SaaS)

> High-performance digital commerce platform for Latin America.

## Key Documentation & Catalog
- [Product Catalog](/api/products-catalog.json): Structured items with prices in COP, stock, and variant attributes.
- [Shipping Policies & Coverage](/policies/shipping): National carrier coverage (Coordinadora & Servientrega) with Cash on Delivery (COD).
- [Warranty & Return Policy](/policies/warranty): 30-day unconditional risk-free warranty.

## Contact & AI Support
- Official WhatsApp Support: +57 300 000 0000 (24/7 AI-Assisted Sales & Support)
- Email: support@yourcompany.com
`;

  return new Response(content, {
    headers: {
      'Content-Type': 'text/markdown; charset=utf-8',
      'Cache-Control': 'public, max-age=86400',
    },
  });
};
```

---

## 5. Neurocopywriting Formulas & Objection Handling

### Core E-Commerce Objection Framework
1. **Payment Trust Objection:**
   * *Copy Pattern:* *"Order today and pay in cash or bank transfer only when you receive your package at your doorstep via verified carriers (Coordinadora / Servientrega)."*
2. **Delivery Speed Objection:**
   * *Copy Pattern:* *"Same-day dispatch for orders placed before 2:00 PM (GMT-5). Live WhatsApp tracking updates sent automatically upon handover to carrier."*
3. **Quality & Return Hesitation:**
   * *Copy Pattern:* *"Try our product for 30 full days. If it does not exceed 100% of your expectations, we will issue a full refund immediately without any questions asked."*
