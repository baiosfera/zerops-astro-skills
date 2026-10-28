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
| `META_PIXEL_ID` | Public / Client | Meta Dataset / Pixel ID (e.g. `1547000523905487`) |
| `META_CAPI_ACCESS_TOKEN` | Private / Secret | System User Graph API access token (v21+) |
| `META_CATALOG_ID` | Private / Config | Product catalog ID in Meta Commerce Manager |
| `GOOGLE_ADS_CONVERSION_ID` | Public / Client | Google Ads Tag ID (e.g. `AW-XXXXXXXXX`) |
| `GOOGLE_ADS_CONVERSION_LABEL` | Private / Secret | Conversion action label |
| `GOOGLE_ADS_DATA_MANAGER_TOKEN` | Private / Secret | Service account OAuth token for Enhanced Conversions |
| `TIKTOK_PIXEL_ID` | Public / Client | TikTok Pixel ID |
| `TIKTOK_EVENTS_TOKEN` | Private / Secret | TikTok Events API v1.3 Access Token |

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
