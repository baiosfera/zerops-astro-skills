---
name: "seo-aeo-geo"
description: "Trigger: seo, aeo, geo, llms.txt, schema.org, json-ld, opengraph, sitemap, searchgpt, perplexity seo, cloudflare edge redirects. Architect, model, and automate the multi-surface SEO, AEO (Answer Engine Optimization), GEO (Generative Engine Optimization), Schema.org JSON-LD Knowledge Graph, llms.txt pipeline, and Cloudflare Edge 301/HSTS canonical rules on Astro 5 and Directus in Zerops."
license: "Apache-2.0"
metadata:
  author: "Gentleman Programming"
  version: "1.2"
  cohalo-standard: "6.7"
---

# SEO, AEO & GEO — Multi-Surface Search Optimization Engine (v1.2)

## Activation Contract
Activate whenever architecting, developing, or optimizing organic search visibility across traditional search engines (Google, Bing), AI Answer Engines (**Perplexity**, **SearchGPT**, **ChatGPT Search**, **Gemini**), Schema.org JSON-LD Knowledge Graphs, OpenGraph / Twitter Card metadata, automated dynamic sitemaps, `llms.txt` specifications, or Cloudflare Edge canonical 301 redirections (HTTP $\to$ HTTPS, non-www $\to$ www) and HSTS policies on Astro 5 SSR and Directus 11+.

---

## Hard Rules & Technical Invariants

1. **Schema.org Knowledge Graph Invariant:**
   - Every product, article, and organization page MUST inject valid `<script type="application/ld+json">` metadata aligned with Schema.org specifications.
2. **LLMs.txt Specification Compliance:**
   - Every public deployment MUST serve `/llms.txt` and `/llms-full.txt` endpoints formatted according to the official standard for generative crawler consumption.
3. **Core Web Vitals & Zero Layout Shift:**
   - All meta-tags, canonical links, and OpenGraph images MUST render server-side in Astro SSR to guarantee sub-1.0s Largest Contentful Paint (LCP) and zero Cumulative Layout Shift (CLS).
4. **Edge Canonical Redirection Invariant:**
   - Enforce canonical redirects (HTTP to HTTPS, and root apex to www or vice versa) at the Cloudflare Edge to prevent split-ranking SEO penalties.

---

## References & SSoT Documents

- [`references/usage.md`](file:///var/www/.agents/skills/seo-aeo-geo/references/usage.md) — Schema.org components, Astro 5 SEO layout integration, and `llms.txt` endpoint generators.
- [`references/infra.md`](file:///var/www/.agents/skills/seo-aeo-geo/references/infra.md) — Canonical domain routing, robots.txt rules, and CDN caching headers on Zerops.
- [`cloudflare`](file:///var/www/.agents/skills/cloudflare/SKILL.md) — Edge DNS, 301 canonical redirects, HSTS policies, and global cache rules.
- [`assets/SEO.astro`](file:///var/www/.agents/skills/seo-aeo-geo/assets/SEO.astro) — Reusable Astro component for OpenGraph, Twitter Cards, and canonical tags.
- [`assets/SchemaGraph.astro`](file:///var/www/.agents/skills/seo-aeo-geo/assets/SchemaGraph.astro) — JSON-LD structured data graph component for Products and Breadcrumbs.
- [`assets/llms.txt.ts`](file:///var/www/.agents/skills/seo-aeo-geo/assets/llms.txt.ts) — Static API endpoint generator for AI LLM crawler ingestion.
- [`assets/robots.txt.ts`](file:///var/www/.agents/skills/seo-aeo-geo/assets/robots.txt.ts) — Dynamic robots.txt endpoint with sitemap and AI crawler rules.
- [`scripts/seo-aeo-geo-validate.sh`](file:///var/www/.agents/skills/seo-aeo-geo/scripts/seo-aeo-geo-validate.sh) — Deterministic quality & token validation sensor.
