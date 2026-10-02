# Astro 5 Developer Manual: SSR, Content Layer, Actions, Tailwind 4 & Container API (v3.0)

Astro 5 (`astro`) is the premier server-first web framework and Server-Side Rendering (SSR) engine for ultra-high-performance web applications. In Zerops, Astro serves as the sovereign frontend and client portal layer, leveraging Islands Architecture, Server Islands (`server:defer`), Content Layer APIs, type-safe Astro Actions (`astro:actions`), and sub-millisecond inter-service communication with decoupled backends (**NATS JetStream 2.12**, **Valkey 7.2**, **PostgreSQL 18**, and S3 **Object Storage**).

---

## 1. Matrix: 4D Comparative Architectural Matrix {#1-matrix}

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

## 2. Content Layer: Universal Content Loader API (`src/content.config.ts`) {#2-content-layer}

The Astro 5 Content Layer API allows fetching, validating, and caching content collections from any headless CMS, database, or API with incremental builds:

```typescript
import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';

export function universalContentLoader({
  endpoint,
  collectionName,
  authToken
}: {
  endpoint: string;
  collectionName: string;
  authToken?: string;
}) {
  return {
    name: `universal-loader-${collectionName}`,
    load: async ({ store, logger, parseData }: any) => {
      logger.info(`Loading collection '${collectionName}' from ${endpoint}...`);
      const headers: Record<string, string> = { 'Accept': 'application/json' };
      if (authToken) headers['Authorization'] = `Bearer ${authToken}`;

      const res = await fetch(endpoint, { headers });
      if (!res.ok) throw new Error(`Fetch failed for ${collectionName}: ${res.statusText}`);

      const raw = await res.json();
      const items = Array.isArray(raw) ? raw : (raw.data || []);
      store.clear();

      for (const item of items) {
        const id = String(item.id || item.slug || crypto.randomUUID());
        const parsed = await parseData({ id, data: item });
        store.set({ id, data: parsed });
      }
      logger.info(`Loaded ${items.length} items for collection '${collectionName}'.`);
    }
  };
}

const articles = defineCollection({
  loader: universalContentLoader({
    endpoint: process.env.CMS_API_URL || 'http://localhost:8055/items/articles',
    collectionName: 'articles',
    authToken: process.env.CMS_API_KEY
  }),
  schema: z.object({
    id: z.string(),
    title: z.string(),
    slug: z.string(),
    content: z.string(),
    status: z.enum(['published', 'draft']).default('published'),
    published_at: z.string().nullable().optional()
  })
});

export const collections = { articles };
```

---

## 3. Server Islands: Server Islands (`server:defer`) & Clave `ASTRO_KEY` {#3-server-islands}

Server Islands defer dynamic server components on the page, streaming fallbacks instantly while decrypting encrypted props securely with `ASTRO_KEY`:

```astro
---
// src/pages/dashboard.astro
import UserProfile from '../components/UserProfile.astro';
import ProfileSkeleton from '../components/ProfileSkeleton.astro';
import LiveMetricsIsland from '../components/LiveMetricsIsland.astro';
import MetricsSkeleton from '../components/MetricsSkeleton.astro';
---

<main class="container mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold mb-6">Portal de Clientes & Dashboard</h1>
  
  <!-- Server Island 1: User Profile -->
  <UserProfile server:defer userId={Astro.locals.userId}>
    <ProfileSkeleton slot="fallback" />
  </UserProfile>

  <!-- Server Island 2: Real-Time Dynamic Widget -->
  <div class="mt-8">
    <LiveMetricsIsland server:defer>
      <MetricsSkeleton slot="fallback" />
    </LiveMetricsIsland>
  </div>
</main>
```

---

## 4. OAuth: Universal OAuth Component (`OAuthButton.astro`) {#4-oauth}

Agnostic OAuth 2.0 / OIDC component configurable via environment variables without hardcoded provider coupling:

```astro
---
interface Props {
  provider?: "google" | "github" | "oidc";
  label?: string;
  redirectPath?: string;
}
const {
  provider = "google",
  label = "Continuar con Google",
  redirectPath = "/dashboard"
} = Astro.props;

const authBaseUrl = import.meta.env.PUBLIC_AUTH_URL || "https://auth.yourdomain.com";
const returnUrl = encodeURIComponent(`${Astro.url.origin}${redirectPath}`);
const loginUrl = `${authBaseUrl}/login/${provider}?redirect=${returnUrl}`;
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
  <span>{label}</span>
</a>
```

---

## 5. Actions: Astro Actions with NATS RPC & Valkey Rate Limit {#5-actions}

```typescript
// src/actions/index.ts
import { defineAction, ActionError } from 'astro:actions';
import { z } from 'astro/zod';
import { connect, JSONCodec } from 'nats';
import Redis from 'ioredis';

const jc = JSONCodec();
const valkey = new Redis(process.env.VALKEY_URL || 'redis://valkey:6379');

let natsConn: any = null;
async function getNats() {
  if (!natsConn || natsConn.isClosed()) {
    natsConn = await connect({ servers: process.env.NATS_URL || 'nats://nats:4222' });
  }
  return natsConn;
}

export const server = {
  submitInquiry: defineAction({
    accept: 'json',
    input: z.object({
      email: z.string().email(),
      name: z.string().min(2),
      message: z.string().min(10)
    }),
    handler: async (input, context) => {
      // 1. Sliding Window Rate Limiting in Valkey
      const clientIp = context.clientAddress || '127.0.0.1';
      const rateKey = `rate:inquiry:${clientIp}`;
      const hits = await valkey.incr(rateKey);
      if (hits === 1) await valkey.expire(rateKey, 60);
      if (hits > 10) {
        throw new ActionError({ code: 'TOO_MANY_REQUESTS', message: 'Rate limit exceeded. Please wait a minute.' });
      }

      // 2. Publish Domain Event via NATS JetStream
      const nc = await getNats();
      const eventPayload = {
        id: crypto.randomUUID(),
        timestamp: new Date().toISOString(),
        data: input
      };
      nc.publish('events.inquiry.created', jc.encode(eventPayload));

      return { success: true, eventId: eventPayload.id };
    }
  })
};
```

---

## 6. Container API: Container API Testing with Vitest {#6-container-api}

Astro 5 introduces the experimental Container API to render and test Astro components in unit testing environments:

```typescript
// src/test/container.test.ts
import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { expect, test } from 'vitest';
import OAuthButton from '../components/OAuthButton.astro';

test('OAuthButton renders with custom label', async () => {
  const container = await AstroContainer.create();
  const result = await container.renderToString(OAuthButton, {
    props: { label: 'Iniciar sesión empresarial' }
  });

  expect(result).toContain('Iniciar sesión empresarial');
  expect(result).toContain('svg');
});
```

---

## 7. Anti-Slop: Anti-Slop Craft and Design Gate {#7-anti-slop}

The Pre-flight Craft Gate eradicates generic AI layouts (*AI Slop*). Before producing HTML/CSS, the engineer calibrates three fundamental dials:

1. **Variance Dial (Layout & Hierarchy)**:
   - **High Asymmetry**: Break the predictable 3-card grid. Utilize editorial magazine grids, alternating column widths (e.g. 60/40, 70/30), overlapping z-index layers, and full-width display typography.
   - **Display Typography**: Utilize expressive display fonts for H1/H2, keeping body copy clean and legible.
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

## 8. Brand Tokens: Brandbook Token Ingestion into Tailwind 4 {#8-brand-tokens}

When a `brandbook.json` (W3C DTCG format) exists in the project root, Astro 5 ingests tokens natively into `src/styles/global.css`:

```css
@import "tailwindcss";

@theme {
  /* Colors from brandbook.json (OKLCH) */
  --color-brand-primary: var(--brand-color-primary, oklch(0.2 0.05 250));
  --color-brand-surface: var(--brand-color-surface, oklch(0.98 0.01 250));
  --color-brand-accent: var(--brand-color-accent, oklch(0.7 0.15 140));
  
  /* Typography tokens */
  --font-display: var(--brand-font-display, system-ui, sans-serif);
  --font-body: var(--brand-font-body, system-ui, sans-serif);
  
  /* Motion tokens */
  --ease-cinematic: cubic-bezier(0.16, 1, 0.3, 1);
  --duration-reveal: 600ms;
}
```

Components consume `--color-brand-primary` directly without manual color re-definitions.

---

## 9. Three Invisible Flaws Shield

Every Astro 5 deployment must guard against the 3 invisible traps:

1. **SEO & Social Preview Head (`SeoHead.astro`)**:
   Mandatory `<head>` tags: OpenGraph (`og:image`, `og:title`, `og:description`), Twitter cards (`summary_large_image`), canonical URLs, and Schema.org JSON-LD.
2. **Sovereign RGPD/GDPR Cookie Script-Blocker (`CookieConsent.astro`)**:
   Analytics scripts are embedded with `<script type="text/plain" data-category="analytics">`. They execute strictly after explicit user acceptance.
3. **Decoupled Form Processing (`ContactAction.ts`)**:
   Forms submit via Astro Actions (`defineAction`) with Zod validation, dispatching dynamically to PostgreSQL, NATS, or fallback HTTP webhooks.
