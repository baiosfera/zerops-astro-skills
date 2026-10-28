# Ad Telemetry, Local SEO & Multi-Network Attribution Manual (v1.0)

This manual provides the canonical specifications and implementations for multi-network performance telemetry (Meta Ads CAPI v21+, Google Ads Enhanced Conversions, TikTok Events API v1.3), Google Consent Mode v2, Google Business Profile (GBP) Local SEO, and 1st-party cookie attribution across the Zerops stack.

---

## 1. Brand Presence Modeling (SAB vs Physical Storefront vs Pure Online)

### Architectural Taxonomies
Every business belongs to one of 4 presence models declared in `BrandPresenceProfile`:

| Presence Model | Physical Location | Schema.org `@type` | Map / Address Behavior | Typical Use Case |
|---|---|---|---|---|
| **`service_area_business`** | No public storefront (Mobile/On-site) | `ProfessionalService` or `LocalBusiness` | **Hides street address**, omits `hasMap`, declares `areaServed` | On-site bridal makeup, mobile stylists, consultants |
| **`physical_storefront`** | Walk-in store / public salon | `BeautySalon`, `Store`, `ClothingStore` | Declares full address, exact `geo`, `hasMap` with Google Maps CID | Physical boutique, salon, physical retail studio |
| **`pure_online_national`** | Online only (Domestic shipping) | `OnlineStore` or `Organization` | No map/local tags. Declares `shippingDetails` | National e-commerce, apparel, dropshipping |
| **`pure_online_global`** | Online only (Worldwide) | `OnlineStore` or `Organization` | No map/local tags. Global coverage | Digital products, courses, SaaS |

### Schema.org Implementation Guide
```typescript
import type { Thing } from 'schema-dts';
import type { BrandPresenceProfile } from '@astrobranding/contracts';

export function buildPresenceSchema(profile: BrandPresenceProfile): Thing {
  const baseEntity = {
    '@id': `${profile.website_url}/#entity`,
    name: profile.business_name,
    legalName: profile.legal_name || profile.business_name,
    url: profile.website_url,
    telephone: profile.primary_telephone,
    email: profile.primary_email,
    sameAs: profile.same_as_urls,
  };

  if (profile.presence_model === 'service_area_business') {
    return {
      '@type': 'ProfessionalService',
      ...baseEntity,
      areaServed: profile.service_areas.map((area) => ({
        '@type': 'City',
        name: area,
      })),
      // DO NOT include streetAddress or hasMap for SAB to prevent Google suspension
    };
  }

  if (profile.presence_model === 'physical_storefront') {
    return {
      '@type': profile.schema_org_type as any,
      ...baseEntity,
      hasMap: profile.has_map_url || (profile.google_maps_cid ? `https://www.google.com/maps?cid=${profile.google_maps_cid}` : undefined),
      address: {
        '@type': 'PostalAddress',
        streetAddress: profile.street_address,
        addressLocality: profile.locality,
        addressRegion: profile.region,
        postalCode: profile.postal_code,
        addressCountry: profile.country_code,
      },
      geo: profile.geo ? {
        '@type': 'GeoCoordinates',
        latitude: profile.geo.latitude,
        longitude: profile.geo.longitude,
      } : undefined,
      openingHoursSpecification: profile.opening_hours.map((oh) => ({
        '@type': 'OpeningHoursSpecification',
        dayOfWeek: oh.dayOfWeek,
        opens: oh.opens,
        closes: oh.closes,
      })),
    };
  }

  return {
    '@type': 'OnlineStore',
    ...baseEntity,
  };
}
```

---

## 2. Google Consent Mode v2 Standards

Consent Mode v2 requires 4 explicit signals:
- `ad_storage`: Access to ad cookies/storage.
- `ad_user_data`: Consent to send user data (email, phone) to Google for advertising.
- `ad_personalization`: Remarketing consent.
- `analytics_storage`: Analytics cookies/storage.

### Lifecycle in Astro 5 SSR
1. **Synchronous Default in `<head>`**: Before GTM or gtag loads, initialize all 4 keys to `denied` with `wait_for_update: 500`.
2. **Rehydration from LocalStorage**: Check if `user_consent_v2` exists from a previous session and fire `gtag('consent', 'update', ...)` immediately.
3. **Reactive Consent Banner (UI Island)**: When the user accepts or customizes consent, save to `localStorage` and trigger `gtag('consent', 'update', ...)`.

---

## 3. 1st-Party Cookie Attribution Engine (`__attr_session`)

### Cookie Taxonomy (90-Day Root Domain)
- `Domain`: Root domain with leading dot (e.g. `.catalinaglamur.com`) so it is accessible across `checkout.*`, `shop.*`, and root.
- `SameSite`: `Lax`.
- `Secure`: `true`.
- `Max-Age`: `7776000` (90 days).

### Captured Click Identifiers
- `gclid`: Google Ads standard click ID.
- `gbraid`: Google Ads iOS app-to-web click ID.
- `wbraid`: Google Ads iOS web-to-web click ID.
  *(Note: Google Data Manager API accepts simultaneous `gclid` and `gbraid`).*
- `fbclid`: Meta click ID.
  **CRITICAL CAPI REQUIREMENT:** Meta CAPI requires `fbc` in the format `fb.1.${timestamp}.${fbclid}`. Sending raw `fbclid` fails click matching silently.
- `ttclid`: TikTok click ID.
- `msclkid`: Microsoft Advertising click ID.

---

## 4. Multi-Network Tri-Red Signal Dispatching

### Deduplication Contract
Every event (browser and server) must share the identical `event_id`.
- On browser: `fbq('track', 'Purchase', payload, { eventID: signal.event_id })`
- On server: Send `event_id: signal.event_id` in CAPI payload.

### SHA-256 PII Normalization Standards
Before sending to Meta CAPI, Google Ads Enhanced Conversions, or TikTok Events API:
1. **Email**: Trim leading/trailing whitespace, lowercase, remove dots for Gmail (`john.doe@gmail.com` $\to$ `johndoe@gmail.com`), strip `+alias`. Hash with SHA-256.
2. **Phone**: Strip non-digits, format in E.164 (`+573001234567`). Hash with SHA-256.
3. **First/Last Name**: Trim, lowercase, hash with SHA-256.
