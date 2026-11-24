---
name: ad-telemetry
description: "Trigger: ad-telemetry, meta ads, google ads, tiktok ads, linkedin insight, capi, consent mode v2, zaraz, posthog, clarity, gtm, ga4, utm, click-id, fbp, fbc, gclid, gbraid, wbraid, ttclid, li_fat_id, 1st-party cookie, localbusiness schema, sab, storefront, outbox telemetry. Universal Agnostic Multi-Network Advertising & Telemetry Orchestrator for Zerops Astrobranding."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `ad-telemetry` — Hybrid Ads, Product Analytics & Attribution Orchestrator (v2.0)

## Activation Contract
Activate when building or auditing multi-network ad telemetry (Meta CAPI v21+, Google Ads Enhanced Conversions, TikTok Events API v1.3, LinkedIn Insight Tag), hybrid analytics (Cloudflare Zaraz, PostHog, Microsoft Clarity, GA4), Consent Mode v2, GBP Local SEO, 1st-party attribution (`__attr_session`), or Outbox dispatchers on Astro 5 SSR.

## Hard Rules & Positive Guidance
1. **Opt-In / Dormant-Safe Telemetry**: Zero pixel or API keys are required at scaffold time. Connectors check env vars and run as silent no-ops when unconfigured.
2. **Hybrid 2-Layer Topology**: Pair **Cloudflare Zaraz** (1M free events/mo edge tags, replacing heavy client GTM.js), **PostHog** (events, feature flags, AI observability; disable session replays when Clarity is active), **Microsoft Clarity** (unlimited replays/heatmaps + AI bot insights), **LinkedIn Insight Tag**, and **Astro SSR CAPI** via PG18->NATS->Valkey Outbox.
3. **Host-Aware Multi-Domain Isolation**: Resolve env vars per normalized hostname prefix (`<DOMAIN_SLUG>_META_PIXEL_ID`) before global fallbacks so co-hosted domains stay isolated.
4. **Vertical & Presence Isolation**: Route `physical_goods` strictly to `/api/catalog/feed.xml`; route services, courses, and B2B funnels to direct conversion pages. If `service_area_business` (SAB), emit `ProfessionalService` with `areaServed` and omit `streetAddress` and `hasMap`.
5. **Consent Mode v2 & 90-Day Attribution**: Initialize Consent Mode v2 defaults to `denied` synchronously in `<head>`. Persist UTMs and Click-IDs (`gclid`, `gbraid`, `wbraid`, `fbc`, `ttclid`, `li_fat_id`) in `__attr_session` (`.domain.com`). Format Meta `fbc` as `fb.1.${timestamp}.${fbclid}` and share UUIDv7 `event_id` across browser and CAPI.

## Component & Asset Matrix

| Component / Utility | File | Responsibility |
|---|---|---|
| **Consent Head** | [`assets/ConsentModeHead.astro`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/ConsentModeHead.astro) | Synchronous Consent Mode v2 `<head>` injector |
| **Local SEO Schema** | [`assets/LocalBusinessSchema.astro`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/LocalBusinessSchema.astro) | Dynamic Schema.org JSON-LD (SAB vs Storefront) |
| **Attribution Engine** | [`assets/attribution.ts`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/attribution.ts) | 1st-party cookie tracker (`first_touch` / `last_touch`) |
| **Signal Dispatcher** | [`assets/commercial_signal_dispatcher.ts`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/commercial_signal_dispatcher.ts) | Multi-network browser & SSR CAPI dispatcher |

## Decision Gates

| Challenge / Need | Action / Protocol | Reference |
|---|---|---|
| Presence Modeling | Classify SAB, Storefront, or Pure Online | [`references/usage.md#1`](file:///var/www/zerops-astro-skills/ad-telemetry/references/usage.md) |
| Consent Mode v2 | Default denied + reactive update | [`references/usage.md#2`](file:///var/www/zerops-astro-skills/ad-telemetry/references/usage.md) |
| Hybrid Stack & Click-IDs | Zaraz, PostHog, Clarity, LinkedIn, CAPI dedup | [`references/usage.md#3`](file:///var/www/zerops-astro-skills/ad-telemetry/references/usage.md) |
| Multi-Domain & Playbooks | Host prefixes + Playbooks `07`, `13`, `14` | [`references/usage.md#5`](file:///var/www/zerops-astro-skills/ad-telemetry/references/usage.md) |
| Infrastructure | Outbox, dormant env prefixes & Cloudflare WAF | [`references/infra.md`](file:///var/www/zerops-astro-skills/ad-telemetry/references/infra.md) |

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/ad-telemetry/references/usage.md) — SSoT spec for schemas, attribution, consent, hybrid stack, and playbook mapping.
- [`references/infra.md`](file:///var/www/zerops-astro-skills/ad-telemetry/references/infra.md) — Network topology, dormant-safe env vars, Zaraz, and CDN headers.
