# Ad Telemetry Infrastructure & Platform Operations Manual (v1.0)

## 1. Zerops Multi-Service Topology

The telemetry mesh runs across Zerops Incus LXC containers:

```
[Browser / Edge Client]
       |
       | HTTPS (Cloudflare Edge CDN)
       v
[webprod / webdev] (Astro 5 SSR on Bun)
       |
       +---> [PostgreSQL 18] (Transactional Outbox: orders + attribution_data)
       |            |
       |            v (pg_notify + FOR UPDATE SKIP LOCKED)
       +---> [NATS 2.12 JetStream] (Deduplication: duplicate_window: 120s)
                    |
                    v
             [Valkey 7.2] (Distributed Idempotency Lock: SET lock:tx:<id> 1 NX EX 3600)
                    |
                    v
       [Meta CAPI] + [Google Ads Data Manager] + [TikTok Events API]
```

---

## 2. Platform Secrets & Environment Variables

Variables are managed centrally via `zerops_env` and injected into the runtime container environment:

| Variable | Scope | Description |
|---|---|---|
| `META_PIXEL_ID` | Public / Optional | Meta Dataset / Pixel ID (`dormant-safe` when empty) |
| `META_CAPI_ACCESS_TOKEN` | Private / Optional | System User Graph API access token (v21+) |
| `META_CATALOG_ID` | Private / Optional | Product catalog ID in Meta Commerce Manager |
| `GA4_MEASUREMENT_ID` | Public / Optional | Google Analytics 4 stream ID (`G-XXXXXXXXXX`) |
| `POSTHOG_PROJECT_KEY` | Public / Optional | PostHog project key (replays disabled when Clarity active) |
| `POSTHOG_HOST` | Public / Optional | PostHog ingestion host (`https://us.i.posthog.com`) |
| `MICROSOFT_CLARITY_ID` | Public / Optional | Clarity project ID for heatmaps & replays |
| `LINKEDIN_PARTNER_ID` | Public / Optional | LinkedIn Insight Tag partner ID |
| `ZARAZ_ENABLED` | Config / Optional | Set `"true"` when tags execute at Cloudflare Zaraz Edge |
| `BING_INDEXNOW_KEY` | Public+Private / Optional | IndexNow instant search ping key |
| `GOOGLE_ADS_CONVERSION_ID` | Public / Optional | Google Ads Tag ID (`AW-XXXXXXXXX`, dormant until active) |
| `GOOGLE_ADS_CONVERSION_LABEL` | Private / Optional | Conversion action label |
| `GOOGLE_ADS_DATA_MANAGER_TOKEN` | Private / Optional | Service account OAuth token for Enhanced Conversions |
| `TIKTOK_PIXEL_ID` | Public / Optional | TikTok Pixel ID (dormant until active) |
| `TIKTOK_EVENTS_TOKEN` | Private / Optional | TikTok Events API v1.3 Access Token |

> **Multi-Domain Prefix Convention:** For shared multi-domain runtimes, prefix any variable above with `<NORMALIZED_HOST>_` (e.g., `EXAMPLE_COM_META_PIXEL_ID`) so each host resolves isolated credentials.

---

## 3. Cloudflare Edge Rules & Cookie Scoping

1. **Root Domain Scoping**: Cookies MUST be set at `.domain.com` (with leading dot) to allow sharing across apex and subdomains (`shop.domain.com`, `checkout.domain.com`).
2. **SameSite & Secure Flags**: Set `SameSite=Lax; Secure; HttpOnly=false` (accessible to client-side tracker and SSR endpoints).
3. **Cloudflare WAF Rules**: Ensure `/api/catalog/feed.xml` bypasses bot mitigation challenges for verified Meta and Googlebot crawlers.

---

## 4. Valkey 7.2 Idempotency Locking Recipe

To prevent duplicate webhook processing or duplicate CAPI event dispatches during network retries:

```typescript
import { valkey } from '@astrobranding/database';

export async function withIdempotencyLock<T>(
  key: string,
  ttlSeconds: number,
  fn: () => Promise<T>
): Promise<T | null> {
  // SET lock:<key> 1 NX EX <ttlSeconds>
  const acquired = await valkey.set(`lock:${key}`, "1", "EX", ttlSeconds, "NX");
  if (!acquired) {
    console.warn(`[Idempotency] Key ${key} is already being processed or completed.`);
    return null;
  }

  try {
    return await fn();
  } catch (error) {
    // Release lock on fatal failure to permit retry if needed
    await valkey.del(`lock:${key}`);
    throw error;
  }
}
```
