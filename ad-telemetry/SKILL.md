---
name: ad-telemetry
description: "Trigger: ad-telemetry, meta ads, google ads, tiktok ads, capi, consent mode v2, gtm, ga4, utm, click-id, fbp, fbc, gclid, gbraid, wbraid, ttclid, 1st-party cookie, localbusiness schema, sab, storefront, outbox telemetry. Universal Agnostic Multi-Network Advertising & Telemetry Orchestrator for Zerops Astrobranding."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `ad-telemetry` — Multi-Network Ads, Attribution & Telemetry Orchestrator (v1.0)

## Activation Contract
Activate when architecting, developing, or auditing multi-network ad telemetry (Meta CAPI v21+, Google Ads Enhanced Conversions, TikTok Events API v1.3), Google Consent Mode v2, Google Business Profile (GBP) Local SEO, 1st-party attribution cookies (`__attr_session`), or commercial signal dispatchers across Astro 5 SSR and Zerops.

## Hard Rules & Positive Guidance
1. **Vertical Isolation (Policy 19 & GMC)**: Route `physical_goods` strictly to commerce XML feeds (`/api/catalog/feed.xml`). Route `courses_education`, `memberships_mrr`, `events_ticketing`, `digital_products`, and `service_bookings` to direct conversion landing pages.
2. **Brand Presence Invariant**: Respect the 4 presence models in `BrandPresenceProfile`. If `service_area_business` (SAB), emit `ProfessionalService` with `areaServed` and suppress street address and map pins to prevent Google suspension. If `physical_storefront`, emit `hasMap` with Google Maps CID, geo-coordinates, and opening hours. If `pure_online_*`, emit `OnlineStore` or `Organization`.
3. **Synchronous Consent Mode v2**: In `<head>`, initialize Consent Mode v2 defaults to `denied` (`ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage`) synchronously before GTM or ad pixels execute.
4. **90-Day Root Domain Attribution**: Persist `first_touch` and `last_touch` UTMs and Click-IDs in `__attr_session` scoped to `.domain.com`. Format Meta `fbc` strictly as `fb.1.${timestamp}.${fbclid}` (never raw `fbclid`).
5. **Shared Idempotency Key**: Browser pixels and server CAPI must emit identical monotonic `event_id` values (UUIDv7 or order ID) for deduplication.

## Component & Asset Matrix

| Component / Utility | File | Responsibility |
|---|---|---|
| **Consent Head** | [`assets/ConsentModeHead.astro`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/ConsentModeHead.astro) | Synchronous Consent Mode v2 `<head>` injector |
| **Local SEO Schema** | [`assets/LocalBusinessSchema.astro`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/LocalBusinessSchema.astro) | Dynamic Schema.org JSON-LD (SAB vs Storefront) |
| **Attribution Engine** | [`assets/attribution.ts`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/attribution.ts) | 1st-party cookie tracker (`first_touch` / `last_touch`) |
| **Signal Dispatcher** | [`assets/commercial_signal_dispatcher.ts`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/commercial_signal_dispatcher.ts) | Tri-network browser & server CAPI dispatcher |

## Decision Gates

| Challenge / Need | Action / Protocol | Reference |
|---|---|---|
| Presence Modeling | Classify brand as SAB, Storefront, or Pure Online | [`references/usage.md#1`](file:///var/www/zerops-astro-skills/ad-telemetry/references/usage.md) |
| Consent Mode v2 | Implement default denied + reactive update | [`references/usage.md#2`](file:///var/www/zerops-astro-skills/ad-telemetry/references/usage.md) |
| Click-ID Tracking | Capture `gclid`, `gbraid`, `wbraid`, `fbc`, `ttclid` | [`references/usage.md#3`](file:///var/www/zerops-astro-skills/ad-telemetry/references/usage.md) |
| CAPI Deduplication | Fire matching `event_id` across browser and server | [`references/usage.md#4`](file:///var/www/zerops-astro-skills/ad-telemetry/references/usage.md) |
| Infrastructure | Configure Zerops environment secrets and Cloudflare | [`references/infra.md`](file:///var/www/zerops-astro-skills/ad-telemetry/references/infra.md) |

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/ad-telemetry/references/usage.md) — SSoT specification for schemas, attribution, consent, and signals.
- [`references/infra.md`](file:///var/www/zerops-astro-skills/ad-telemetry/references/infra.md) — Network topology, environment variables, and CDN headers.
