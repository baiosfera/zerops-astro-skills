---
name: "seo-aeo-geo"
description: "Trigger: seo, aeo, geo, llms.txt, schema.org, json-ld, opengraph, opengraph-multi-surface, favicons, favicon-suite, image-seo, image-object, iptc-metadata, sitemap, searchgpt, perplexity seo, cloudflare edge redirects. Architect, model, and automate the multi-surface SEO, AEO, GEO, Schema.org Knowledge Graph, multi-surface OpenGraph/Twitter (<300KB WhatsApp budget), Favicon Suite (SVG/Apple Touch/PWA), IPTC photo metadata, and Cloudflare Edge 301/HSTS rules on Astro 5 and Directus in Zerops."
license: "Apache-2.0"
metadata:
  author: "Gentleman Programming"
  version: "2.0"
  cohalo-standard: "6.7"
---

# SEO, AEO & GEO — Multi-Surface Search & Visual Optimization Engine (v2.0)

## Activation Contract
Activate when architecting, developing, or optimizing search visibility across traditional engines (Google, Bing), AI Answer Engines (**Perplexity**, **SearchGPT**, **ChatGPT**, **Gemini**), Schema.org JSON-LD Knowledge Graphs (`ImageObject`, RDF `@graph`), multi-surface OpenGraph / Twitter visual suites (1200x630, safe zone 1080x600, <300KB WhatsApp budget), Favicon & PWA suites (SVG dark/light, `apple-touch-icon`, `site.webmanifest`), IPTC photo metadata, `llms.txt` v2, or Cloudflare Edge 301 redirections on Astro 5 SSR and Directus 11+.

---

## Hard Rules & Technical Invariants

1. **Schema.org Knowledge Graph Invariant:**
   - Every page MUST inject valid `<script type="application/ld+json">` unifying entities and `ImageObject` under an RDF `@graph`.
2. **LLMs.txt Standard Compliance:**
   - Public sites MUST serve `/llms.txt` and `/llms-full.txt` endpoints for AI crawlers.
3. **Core Web Vitals & Zero Layout Shift:**
   - Meta-tags and OpenGraph images MUST render server-side in Astro SSR for sub-1.0s LCP and zero CLS.
4. **Edge Canonical Redirection Invariant:**
   - Enforce canonical redirects (HTTP $\to$ HTTPS, non-www $\to$ www or vice versa) at Cloudflare Edge.
5. **OpenGraph WhatsApp Threshold (<300KB):**
   - Universal OG images (1200x630) MUST be compressed under 300KB to prevent silent drop in WhatsApp link previews.
6. **Safe Zone Invariant (1080x600):**
   - Key typography and logos in 1200x630 OG cards MUST stay inside the centered 1080x600 safe zone.
7. **Complete Favicon & PWA Suite:**
   - Deployments MUST include `favicon.ico`, vector `favicon.svg` (dark/light support), `apple-touch-icon.png` (180x180), and PWA icons declared in `site.webmanifest`.
8. **Agnostic Architecture & Zero Hardcoding:**
   - Skill is 100% client-agnostic. Ingests brand tokens dynamically from W3C DTCG `brandbook.json` or typed Astro props.

---

## References & SSoT Documents

- [`references/usage.md`](file:///var/www/.agents/skills/seo-aeo-geo/references/usage.md) — Multi-surface social matrix, Schema.org `ImageObject`, Favicon suite, WhatsApp budgets, and component recipes.
- [`references/infra.md`](file:///var/www/.agents/skills/seo-aeo-geo/references/infra.md) — Canonical routing, CDN immutable caching, robots.txt, and edge headers.
- [`cloudflare`](file:///var/www/.agents/skills/cloudflare/SKILL.md) — Edge DNS, 301 redirects, HSTS, and cache rules.
- [`assets/SEO.astro`](file:///var/www/.agents/skills/seo-aeo-geo/assets/SEO.astro) — Parametric Astro SEO component.
- [`assets/FaviconSuite.astro`](file:///var/www/.agents/skills/seo-aeo-geo/assets/FaviconSuite.astro) — Favicon, Apple Touch, and Manifest `<head>` injector.
- [`assets/SchemaGraph.astro`](file:///var/www/.agents/skills/seo-aeo-geo/assets/SchemaGraph.astro) — JSON-LD structured data with `ImageObject`.
- [`assets/llms.txt.ts`](file:///var/www/.agents/skills/seo-aeo-geo/assets/llms.txt.ts) — AI crawler knowledge endpoint generator.
- [`assets/robots.txt.ts`](file:///var/www/.agents/skills/seo-aeo-geo/assets/robots.txt.ts) — Dynamic robots.txt with crawler taxonomies.
- [`scripts/generate-visual-assets.py`](file:///var/www/.agents/skills/seo-aeo-geo/scripts/generate-visual-assets.py) — Universal agnostic script for favicons, PWA, and OG generation.
- [`scripts/seo-aeo-geo-validate.sh`](file:///var/www/.agents/skills/seo-aeo-geo/scripts/seo-aeo-geo-validate.sh) — Physical validation sensor.
