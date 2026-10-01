# Astro 5 Developer Manual: SSR, Content Layer, Actions, Directus, NATS & Full-Stack Engine (v2.0)

Astro 5 (`astro`) is the premier server-first web framework and Server-Side Rendering (SSR) engine for ultra-high-performance web applications. In Zerops, Astro serves as the sovereign frontend and client portal layer, leveraging Islands Architecture, Server Islands (`server:defer`), Content Layer APIs, type-safe Astro Actions (`astro:actions`), and sub-millisecond inter-service communication with **Directus 11+**, **NATS JetStream**, **Valkey**, **PostgreSQL 18**, and **WhatsApp gateways** ([`evolutiongo`](file:///var/www/.agents/skills/evolutiongo/SKILL.md) / [`evolution-api`](file:///var/www/.agents/skills/evolution-api/SKILL.md)).

---

## 1. 4D Comparative Architectural Matrix

| Dimension | Astro 5 SSR (Target) | Next.js 15 (App Router) | Remix / React Router v7 | Nuxt 3 (Vue) |
|---|---|---|---|---|
| **Rendering Architecture** | **Islands + Server Islands (`server:defer`)** | React Server Components (RSC) | Server Loaders / Actions | SSR / Vue Hydration |
| **Client JavaScript Sent** | **0 KB by default** (Selective islands) | 80–150 KB minimum (React runtime) | 60–120 KB minimum | 70–130 KB minimum |
| **Idle Memory in Zerops** | **~35–55 MB RAM** (with Bun 1.3) | ~180–350 MB RAM (Node.js) | ~120–250 MB RAM | ~110–220 MB RAM |
| **Cold Boot Latency** | **< 20 ms** (Bun) / ~150 ms (Node) | ~500–1200 ms | ~300–600 ms | ~300–700 ms |
| **Content Management** | **Universal Content Layer (Loaders)** | Custom fetch scripts | Manual route loaders | Nuxt Content |
| **Server Mutations** | **Astro Actions (`astro:actions` + Zod)** | Server Actions (`'use server'`) | Route Actions | Nitro Server Routes |
| **Secret Isolation** | **`astro:env/server` vs `astro:env/client`** | Prefijo `NEXT_PUBLIC_` | `ENV` context | `runtimeConfig` |
| **Zerops Execution** | **100% Native on `bun@1.3.9` or `nodejs@24`** | Node.js Runtime in Zerops | Node.js Runtime in Zerops | Node.js / Bun Runtime |

### Zerops Runtime Profile: `bun@1.3.9` vs `nodejs@24`

| Operating Characteristic | Astro 5 on `bun@1.3.9` (Recommended SSR SSoT) | Astro 5 on `nodejs@24` |
|---|---|---|
| **Cold Boot Time** | ⚡ **< 20 ms** (Instantaneous startup) | ⏱️ ~150–300 ms |
| **Idle Memory Footprint** | 💾 **~35–55 MB RAM** | 💾 ~90–140 MB RAM |
| **Autoscaling Floor (`minRam`)**| `0.25 GB` (Maximum tenant density & cost savings) | `0.50 GB` |
| **Native TypeScript Support** | Built-in native execution (Zero transpilation overhead) | Requires build-time bundling |
| **Start Command** | `bun ./dist/server/entry.mjs` | `node ./dist/server/entry.mjs` |
| **Zerops Suitability** | **Standard SSoT for 90% of Astro webapps** | Recommended if specific native C++ glibc addons are required |

---

## 2. Content Layer API with Directus Custom Loader (`src/content.config.ts`)

The Astro 5 Content Layer API allows fetching, validating, and caching content collections from Directus with incremental builds:

```typescript
import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';

export function directusLoader({ collectionName, directusUrl }: { collectionName: string; directusUrl: string }) {
  return {
    name: `directus-${collectionName}`,
    load: async ({ store, logger, parseData }: any) => {
      logger.info(`Loading collection '${collectionName}' from Directus at ${directusUrl}...`);
      const res = await fetch(`${directusUrl}/items/${collectionName}?filter[status][_eq]=published`);
      if (!res.ok) throw new Error(`Directus fetch failed: ${res.statusText}`);
      
      const { data } = await res.json();
      store.clear();
      
      for (const item of data) {
        const parsed = await parseData({ id: String(item.id), data: item });
        store.set({ id: String(item.id), data: parsed });
      }
      logger.info(`Loaded ${data.length} items from Directus collection '${collectionName}'.`);
    }
  };
}

const posts = defineCollection({
  loader: directusLoader({
    collectionName: 'posts',
    directusUrl: process.env.PUBLIC_DIRECTUS_URL || 'http://directus:8055'
  }),
  schema: z.object({
    id: z.string(),
    title: z.string(),
    slug: z.string(),
    content: z.string(),
    status: z.enum(['published', 'draft']),
    published_at: z.string().nullable().optional()
  })
});

export const collections = { posts };
```

---

## 3. Server Islands (`server:defer`) & Clave `ASTRO_KEY`

Server Islands defer dynamic server components on the page, streaming fallbacks instantly while decrypting encrypted props securely with `ASTRO_KEY`:

```astro
---
// src/pages/dashboard.astro
import UserProfile from '../components/UserProfile.astro';
import ProfileSkeleton from '../components/ProfileSkeleton.astro';
import LiveKpiIsland from '../components/LiveKpiIsland.astro';
import KpiSkeleton from '../components/KpiSkeleton.astro';
---

<main class="container mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold mb-6">Portal de Clientes & Dashboard</h1>
  
  <!-- Server Island 1: User Profile -->
  <UserProfile server:defer userId={Astro.locals.userId}>
    <ProfileSkeleton slot="fallback" />
  </UserProfile>

  <!-- Server Island 2: Real-Time Commercial KPI Widget -->
  <div class="mt-8">
    <LiveKpiIsland server:defer>
      <KpiSkeleton slot="fallback" />
    </LiveKpiIsland>
  </div>
</main>
```

---

## 4. 1-Click Google OAuth Component (`GoogleLoginButton.astro`)

```astro
---
interface Props {
  redirectPath?: string;
}
const { redirectPath = "/dashboard" } = Astro.props;
const directusUrl = import.meta.env.PUBLIC_DIRECTUS_URL || "https://cms.yourdomain.com";
const loginUrl = `${directusUrl}/auth/login/google?redirect=${encodeURIComponent(`https://yourdomain.com${redirectPath}`)}`;
---

<a
  href={loginUrl}
  class="flex items-center justify-center gap-3 w-full bg-white hover:bg-gray-50 text-gray-800 font-semibold border border-gray-300 rounded-lg px-6 py-3 shadow-sm transition-all"
>
  <svg class="w-5 h-5" viewBox="0 0 24 24">
    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
  </svg>
  <span>Continuar con Google</span>
</a>
```

---

## 5. Astro Actions with NATS RPC, Directus SDK & Valkey

```typescript
// src/actions/index.ts
import { defineAction, ActionError } from 'astro:actions';
import { z } from 'astro/zod';
import { connect, JSONCodec } from 'nats';
import { createDirectus, rest, createItem, staticToken } from '@directus/sdk';
import Redis from 'ioredis';

const jc = JSONCodec();
const valkey = new Redis(process.env.VALKEY_URL || 'redis://cache:6379');

const directus = createDirectus(process.env.DIRECTUS_URL || 'http://directus:8055')
  .with(staticToken(process.env.DIRECTUS_STATIC_TOKEN || ''))
  .with(rest());

export const server = {
  processOrder: defineAction({
    accept: 'json',
    input: z.object({
      customerEmail: z.string().email(),
      customerName: z.string().min(2),
      customerPhone: z.string().min(10),
      items: z.array(z.object({ productId: z.string(), quantity: z.number().int().positive() })),
      totalAmount: z.number().positive(),
    }),
    handler: async (input, context) => {
      // 1. Sliding Window Rate Limiting in Valkey
      const clientIp = context.clientAddress || '127.0.0.1';
      const rateKey = `rate:checkout:${clientIp}`;
      const hits = await valkey.incr(rateKey);
      if (hits === 1) await valkey.expire(rateKey, 60);
      if (hits > 10) {
        throw new ActionError({ code: 'TOO_MANY_REQUESTS', message: 'Rate limit exceeded. Please wait a minute.' });
      }

      // 2. Invoke Atomic Inventory Lock RPC via NATS (<0.3ms P99)
      const nc = await connect({ servers: process.env.NATS_URL || 'nats://nats:4222' });
      const rpcRes = await nc.request('inventory.lock', jc.encode({ items: input.items }), { timeout: 2000 });
      const lockData = jc.decode(rpcRes.data) as { success: boolean; lockId?: string; reason?: string };

      if (!lockData.success) {
        throw new ActionError({ code: 'PRECONDITION_FAILED', message: lockData.reason || 'Inventory unavailable.' });
      }

      // 3. Persist Order in Directus 11+
      const order = await directus.request(
        createItem('orders', {
          customer_email: input.customerEmail,
          customer_name: input.customerName,
          customer_phone: input.customerPhone,
          total_amount: input.totalAmount,
          status: 'pending_payment',
          inventory_lock_id: lockData.lockId,
        })
      );

      // 4. Trigger Outbound WhatsApp Notification via NATS
      await nc.publish('events.whatsapp.outbound', jc.encode({
        phone: input.customerPhone,
        text: `Hello ${input.customerName}! Your order #${order.id} is confirmed. 🚀`
      }));

      await nc.drain();
      return { success: true, orderId: order.id };
    }
  })
};
```

---

## 6. WhatsApp Live QR Pairing Island (`WhatsAppQrIsland.astro`)

```astro
---
// src/components/WhatsAppQrIsland.astro
const evogoUrl = process.env.EVOGO_URL || 'http://evolutiongo:8080';
let qrBase64 = null;
let status = 'disconnected';

try {
  const res = await fetch(`${evogoUrl}/instance/connect/sales-main`, {
    headers: { 'apikey': process.env.EVOGO_API_KEY || 'key' },
    signal: AbortSignal.timeout(3000)
  });
  if (res.ok) {
    const data = await res.json();
    qrBase64 = data.base64 || data.qrcode;
    status = data.state || 'connecting';
  }
} catch (e) {
  status = 'error';
}
---

<div class="p-6 bg-white rounded-xl shadow-md border border-gray-100 max-w-sm mx-auto text-center">
  <h3 class="text-lg font-bold text-gray-800 mb-2">WhatsApp Gateway Status</h3>
  <p class="text-sm text-gray-500 mb-4">Estado: <span class="font-semibold text-emerald-600 uppercase">{status}</span></p>
  
  {qrBase64 ? (
    <div class="p-2 border rounded-lg bg-gray-50 inline-block">
      <img src={qrBase64} alt="WhatsApp QR Code" class="w-64 h-64 object-contain" />
    </div>
  ) : (
    <p class="text-sm text-gray-400 py-8">Instancia conectada o código no disponible.</p>
  )}
</div>
```

---

## 7. Anti-Slop Craft and Design Gate

The Pre-flight Craft Gate eradicates generic AI layouts (*AI Slop*). Before producing HTML/CSS, the engineer calibrates three fundamental dials:

1. **Variance Dial (Layout & Hierarchy)**:
   - **High Asymmetry**: Break the predictable 3-card grid. Utilize editorial magazine grids, alternating column widths (e.g. 60/40, 70/30), overlapping z-index layers, and full-width display typography.
   - **Display Typography**: Utilize expressive display fonts from `fontgen` for H1/H2, keeping body copy clean and legible.
2. **Motion Dial (Kinetic Flow)**:
   - **Hero Dynamism**: Confine rich GSAP animations to the Hero and key section reveals (scroll triggers).
   - **Easing Discipline**: Strictly ban `bounce` or `elastic` easings. Use smooth cubic-bezier (`cubic-bezier(0.16, 1, 0.3, 1)`) or spring mechanics.
3. **Density Dial (Spatial Rhythm)**:
   - **Luxury / Minimalist**: High negative space, generous padding (`py-24`, `py-32`), understated contrast.
   - **Technical / Industrial**: High information density, subtle borders, monospaced metadata badges.

### The 44 Impeccable Deterministic Rules (Enforced)
- **Never use untinted neutral gray**: Black must be tinted with the brand's primary OKLCH undertone (e.g. `oklch(0.12 0.02 260)` instead of `#000000`).
- **Never use purple-on-black cards**: Eliminate the cliché dark card with purple gradient border.
- **Strict Heading Hierarchy**: H1 must be followed by lead paragraph or H2; never jump directly to H3.
- **Minimum Touch Targets**: All interactive elements must maintain >= 44x44px clickable areas on mobile.

---

## 8. Brandbook Token Ingestion into Tailwind 4

When a `brandbook.json` (W3C DTCG format) exists in the project or `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/`, Astro 5 ingests tokens natively into `src/styles/global.css`:

```css
@import "tailwindcss";

@theme {
  /* Colors from brandbook.json (OKLCH) */
  --color-brand-primary: var(--brand-color-primary);
  --color-brand-surface: var(--brand-color-surface);
  --color-brand-accent: var(--brand-color-accent);
  
  /* Typography from fontgen */
  --font-display: var(--brand-font-display), sans-serif;
  --font-body: var(--brand-font-body), sans-serif;
  
  /* Motion from kinetic */
  --ease-cinematic: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-reveal: 600ms;
}
```

This ensures that UI components consume `--color-brand-primary` directly without manual color re-definitions.

---

## 9. Three Invisible Flaws Shield

Every Astro 5 deployment must guard against the 3 invisible traps:

1. **SEO & Social Preview Head (`SeoHead.astro`)**:
   Mandatory `<head>` tags: OpenGraph (`og:image`, `og:title`, `og:description`), Twitter cards (`summary_large_image`), canonical URLs, and Schema.org JSON-LD.
2. **Sovereign RGPD/GDPR Cookie Script-Blocker (`CookieConsent.astro`)**:
   Analytics scripts are embedded with `<script type="text/plain" data-category="analytics">`. They execute strictly after explicit user acceptance, avoiding EU fines without third-party tracker fees.
3. **Decoupled Form Processing (`ContactAction.ts`)**:
   Forms submit via Astro Actions (`defineAction`) with Zod validation. The backend dispatches dynamically:
   - Directus (if provisioned).
   - PostgreSQL (if provisioned).
   - Web3Forms API (free-tier static fallback without servers).
   - NATS JetStream (if asynchronous event queueing is active).

---

## 10. Production Patterns & Anti-Patterns

### 5 Production Patterns in Zerops:
1. **High-Performance E-Commerce**: Astro Actions + NATS RPC + Directus/PostgreSQL.
2. **Customer Portal**: Server Islands + Google OAuth + Valkey cache.
3. **Dynamic Content Hub**: Content Layer + incremental caching.
4. **Real-Time Admin**: Directus WebSockets / NATS PubSub.
5. **WhatsApp Support**: Live pairing QR island (`evolutiongo`).

### Anti-Patterns:
1. **Hardcoding Directus**: Assuming Directus is mandatory for simple landings.
2. **Token Bloat 3D (`img to 3js`)**: Burning 500k tokens to generate raw Three.js geometry instead of using lightweight canvas shaders or SVG animations.
3. **Fake Contact Forms**: Handling forms with empty `alert()` calls that drop customer inquiries.
4. **Untinted Flat Grays**: Using generic `#111111` or `#808080` without chromatic personality.

