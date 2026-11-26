---
name: ad-telemetry
description: "Trigger: ad-telemetry, meta ads, google ads, tiktok ads, linkedin insight, capi, consent mode v2, zaraz, posthog, clarity, gtm, ga4, utm, click-id, fbp, fbc, gclid, gbraid, wbraid, ttclid, li_fat_id, 1st-party cookie, localbusiness schema, sab, storefront, outbox telemetry. Universal Agnostic Multi-Network Advertising & Telemetry Orchestrator for Zerops Astrobranding."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# `ad-telemetry` — Hybrid Ads, Analytics & Attribution (v2.1)

## Activation Contract
Activate when building or auditing multi-network ad telemetry (Meta CAPI v21+, Google Enhanced Conversions, TikTok Events API v1.3, LinkedIn Insight), Cloudflare Zaraz, PostHog, Microsoft Clarity, GA4, Consent Mode v2, GBP Local SEO, 1st-party attribution (`__attr_session`), or Outbox dispatchers on Astro 5 SSR.

## Hard Rules
1. **Dormant-Safe Opt-In**: Zero keys required at scaffold time; unconfigured connectors no-op silently.
2. **Hybrid 2-Layer Topology**: Pair Cloudflare Zaraz, PostHog (disable replays if Clarity runs), Microsoft Clarity, LinkedIn Insight, and Astro SSR CAPI via PG18 $\to$ NATS $\to$ Valkey Outbox.
3. **Host-Aware Isolation**: Resolve `<DOMAIN_SLUG>_META_PIXEL_ID` per normalized hostname before global fallbacks.
4. **Vertical & Presence Isolation**: Route `physical_goods` to `/api/catalog/feed.xml`; route services/courses/B2B to direct conversion pages. For `service_area_business` (SAB), emit `ProfessionalService` with `areaServed` (omit `streetAddress`/`hasMap`).
5. **Consent Mode v2 & 90-Day Attribution**: Default Consent Mode v2 to `denied` in `<head>`. Persist UTMs (`utm_adset`/`utm_ad` supported), Click-IDs (`gclid`, `gbraid`, `wbraid`, `fbc` as `fb.1.${ts}.${fbclid}`, `ttclid`, `li_fat_id`), and partner `?ref=` in `__attr_session`, sharing UUIDv7 `event_id` across browser and CAPI.
6. **Cross-Domain CAPI Bridge & In-App Escape**: Decorate cross-domain checkout links (or send JSON `{...utms, ref_code}` + email pre-check) with `fbp`, `fbc`, `src`, `event_source_url`, and user-agent. Add IG/FB `"Open in Chrome/Safari"` fallback (`6s`) and `data-track` / `VslWatched90s` signals.

## Component & Asset Matrix

| Component | File | Responsibility |
|---|---|---|
| **Consent Head** | [`assets/ConsentModeHead.astro`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/ConsentModeHead.astro) | Sync Consent Mode v2 `<head>` injector |
| **Local Schema** | [`assets/LocalBusinessSchema.astro`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/LocalBusinessSchema.astro) | JSON-LD (`SAB` vs `Storefront`) |
| **Attribution** | [`assets/attribution.ts`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/attribution.ts) | 1st-party cookie (`first_touch` / `last_touch`) |
| **Dispatcher** | [`assets/commercial_signal_dispatcher.ts`](file:///var/www/zerops-astro-skills/ad-telemetry/assets/commercial_signal_dispatcher.ts) | Browser & SSR CAPI dispatcher |

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/ad-telemetry/references/usage.md) — Schemas, attribution, consent, hybrid stack, cross-domain CAPI (`#8`), playbooks (`07`/`13`/`14`).
- [`references/infra.md`](file:///var/www/zerops-astro-skills/ad-telemetry/references/infra.md) — Outbox, dormant env prefixes, Zaraz & Cloudflare WAF.
