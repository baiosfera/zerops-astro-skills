---
name: "seo-aeo-geo"
description: "Trigger: seo, aeo, geo, llms.txt, schema.org, json-ld, opengraph, opengraph-multi-surface, favicons, favicon-suite, image-seo, image-object, iptc-metadata, sitemap, searchgpt, perplexity seo, cloudflare ai crawl control, indexnow, cloudflare edge redirects. Architect, model, and automate multi-surface SEO, AEO, GEO, Schema.org Knowledge Graph, multi-surface OpenGraph (<300KB WhatsApp budget), Favicon Suite, IPTC photo metadata, AI Crawl Control, and IndexNow on Astro 5 in Zerops."
license: "Apache-2.0"
metadata:
  author: "Gentleman Programming"
  version: "2.1"
  cohalo-standard: "6.7"
---

# SEO, AEO & GEO — Multi-Surface Search & AI Visibility Engine (v2.1)

## Activation Contract
Activate when architecting, developing, or optimizing search visibility across traditional engines (Google, Bing/IndexNow), AI Answer Engines (**Perplexity**, **SearchGPT**, **ChatGPT**, **Gemini**, **Claude**), Schema.org JSON-LD `@graph` graphs (`ImageObject`, `Person`, `Organization`, `ProfessionalService`), OpenGraph suites (1200x630, safe zone 1080x600, <300KB WhatsApp budget), 5-layer Favicon & PWA suites, IPTC metadata, host-aware `llms.txt` v2 / `robots.txt`, Cloudflare AI Crawl Control, or Edge 301 canonical rules on Astro 5 SSR.

## Hard Rules & Technical Invariants

1. **Schema.org Knowledge Graph Invariant**: Inject unified `<script type="application/ld+json">` `@graph` entities (`Organization`, `Person`, `WebSite`, `WebPage`, `ImageObject`, and presence-compliant business schema).
2. **Host-Aware `/llms.txt`, `/llms-full.txt` & `/robots.txt`**: Derive canonical origin from `request.headers.get("x-forwarded-host") || request.headers.get("host")` before falling back to `Astro.site`. Decouple from Directus unless explicitly configured, and block indexing (`Disallow: /` + `X-Robots-Tag: noindex, nofollow`) on `*.zerops.app` or `localhost`.
3. **AEO Direct-Answer & Citation Control**: Place a 40–60 word Lead Direct-Answer Block after key H1/H2 sections, expose `<link rel="describedby" href="/llms.txt">`, allow AI retrieval bots (`OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `Perplexity-User`, `Claude-SearchBot`), and enable **Cloudflare AI Crawl Control** + **Bing IndexNow**.
4. **Edge Canonical & Visual Budgets**: Enforce HTTPS + canonical host 301 redirects at Cloudflare Edge, keep universal OG images `< 300 KB` (1200x630, centered 1080x600 safe zone), and ship all 5 Favicon layers (`svg`, PNG 16/32, `ico`, `apple-touch-icon.png`, `site.webmanifest`).
5. **100% Brand-Agnostic & Zero Hardcoding**: Ingest brand metadata dynamically from `brandbook.json` or typed host-resolved props.

## References & SSoT Documents

- [`references/usage.md`](file:///var/www/.agents/skills/seo-aeo-geo/references/usage.md) — Multi-surface matrix, `@graph`, Favicon suite, IPTC, AI Crawl Control, IndexNow & Playbooks `06`, `16`.
- [`references/infra.md`](file:///var/www/.agents/skills/seo-aeo-geo/references/infra.md) — Canonical routing, AI Crawl Control, IndexNow, CDN caching, and edge headers.
- [`cloudflare`](file:///var/www/.agents/skills/cloudflare/SKILL.md) — Edge DNS, 301 redirects, HSTS, WAF, and cache rules.
- [`assets/SEO.astro`](file:///var/www/.agents/skills/seo-aeo-geo/assets/SEO.astro) · [`assets/FaviconSuite.astro`](file:///var/www/.agents/skills/seo-aeo-geo/assets/FaviconSuite.astro) · [`assets/SchemaGraph.astro`](file:///var/www/.agents/skills/seo-aeo-geo/assets/SchemaGraph.astro)
- [`assets/llms.txt.ts`](file:///var/www/.agents/skills/seo-aeo-geo/assets/llms.txt.ts) · [`assets/robots.txt.ts`](file:///var/www/.agents/skills/seo-aeo-geo/assets/robots.txt.ts) · [`scripts/generate-visual-assets.py`](file:///var/www/.agents/skills/seo-aeo-geo/scripts/generate-visual-assets.py)
- Physical validation sensor: `skills-suite-validate` · `ssot-parity-check`
