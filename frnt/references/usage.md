# `frnt`: Universal Frontend, UI/UX, Checkout & Client State Architecture Manual (v2.0)

`frnt` is the master frontend orchestrator commanding the client-facing layer: **Astro 5 SSR server islands**, **React 19 with the native React Compiler**, atomic design systems with **Tailwind CSS 4 (OKLCH)**, global client state with **Zustand 5**, multi-country conversion funnels via **`checkout-funnels`**, transactional email components via **`email-marketing`**, conversational streaming with **Vercel AI SDK 5**, native customer authentication via **Directus SDK** (secure HTTP-only cookies), and **Cloudflare Edge CDN** routing.

---

## 1. 4D Comparative Architectural Matrix: Frontend Rendering Strategies

| Strategy | Engine / Framework | Baseline JS Payload | TTFB / LCP | Best Use Case |
|---|---|---|---|---|
| **Astro 5 SSR Islands (Target)** | **Astro 5 + React 19 Compiler** | **0 KB JS base + on-demand islands** | **<150ms / <0.8s** | **E-Commerce & High-Converting Web Apps** |
| **Full SPA (Vite / React Router)**| React 19 Client SPA | ~250–500 KB bundle | ~800ms / ~2.5s | Internal backoffice dashboards |
| **Next.js App Router** | Next.js 15 Server Components | ~120–200 KB framework runtime | ~350ms / ~1.6s | Standard fullstack enterprise apps |
| **Static Site Generation (SSG)** | Pure Static HTML | 0 KB JS | ~80ms / <0.5s | Blogs and static marketing docs |

---

## 2. Sub-Skills Inventory & Direct File Pointers

| Sub-Skill | Role in Frontend Ecosystem | Direct SSoT Pointer |
|---|---|---|
| **`astro`** | Core SSR framework, Server Islands, View Transitions, Content Layer | [`astro`](file:///var/www/.agents/skills/astro/SKILL.md) |
| **`react-19`** | Interactive island components optimized with React Compiler | [`react-19`](file:///var/www/.agents/skills/react-19/SKILL.md) |
| **`tailwind-4`** | Modern styling engine with CSS variables and OKLCH color palettes | [`tailwind-4`](file:///var/www/.agents/skills/tailwind-4/SKILL.md) |
| **`zustand-5`** | Lightweight client-side global state (shopping cart, navigation drawer) | [`zustand-5`](file:///var/www/.agents/skills/zustand-5/SKILL.md) |
| **`checkout-funnels`**| Multi-country payment gateways, COD WhatsApp OTP, DANE logistics | [`checkout-funnels`](file:///var/www/.agents/skills/checkout-funnels/SKILL.md) |
| **`email-marketing`** | React Email 3.0 template styling, brandbook tokens, DMARCbis RFC 9989 | [`email-marketing`](file:///var/www/.agents/skills/email-marketing/SKILL.md) |
| **`business-insights`**| Client analytics, e-commerce conversion tracking, Meta CAPI | [`business-insights`](file:///var/www/.agents/skills/business-insights/SKILL.md) |
| **`brandbook`** | Design token SSoT (`brandbook.json`), typography & palette compiler | [`brandbook`](file:///var/www/.agents/skills/brandbook/SKILL.md) |
| **`ai-sdk-5`** | Streaming chat widgets, conversational shopping assistants | [`ai-sdk-5`](file:///var/www/.agents/skills/ai-sdk-5/SKILL.md) |
| **`directus`** | Native customer authentication (Magic Links, OTPs, HTTP-only cookies) | [`directus`](file:///var/www/.agents/skills/directus/SKILL.md) |
| **`cloudflare`** | Edge CDN caching, Turnstile anti-bot, SSL Full Strict | [`cloudflare`](file:///var/www/.agents/skills/cloudflare/SKILL.md) |
| **`react-native`** | Cross-platform native mobile applications sharing TypeScript schemas | [`react-native`](file:///var/www/.agents/skills/react-native/SKILL.md) |

---

## 3. Astro 5 SSR Authentication Middleware with Directus SDK

```typescript
// src/middleware.ts
import { defineMiddleware } from 'astro:middleware';
import { createDirectus, rest, authentication, readMe } from '@directus/sdk';

export const onRequest = defineMiddleware(async (context, next) => {
  const token = context.cookies.get('directus_session_token')?.value;

  if (token) {
    try {
      const client = createDirectus(import.meta.env.DIRECTUS_URL || 'http://directus:8055')
        .with(rest())
        .with(authentication('json'));

      client.setToken(token);
      const user = await client.request(readMe({
        fields: ['id', 'first_name', 'last_name', 'email', 'role.name'],
      }));

      context.locals.user = {
        id: user.id,
        name: `${user.first_name || ''} ${user.last_name || ''}`.trim(),
        email: user.email,
        role: user.role?.name || 'customer',
      };
    } catch (err) {
      // Expired or invalid token: purge cookie
      context.cookies.delete('directus_session_token', { path: '/' });
      context.locals.user = null;
    }
  } else {
    context.locals.user = null;
  }

  // Protected routes (e.g. Account Dashboard / Orders)
  if (context.url.pathname.startsWith('/account') && !context.locals.user) {
    return context.redirect('/login?redirect=' + encodeURIComponent(context.url.pathname));
  }

  return next();
});
```

---

## 4. Global Shopping Cart State with Zustand 5

```typescript
// src/stores/cart-store.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export interface CartItem {
  id: string;
  name: string;
  priceCOP: number;
  quantity: number;
  imageUrl?: string;
  sku: string;
}

interface CartState {
  items: CartItem[];
  isOpen: boolean;
  addItem: (item: Omit<CartItem, 'quantity'>, qty?: number) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, qty: number) => void;
  clearCart: () => void;
  toggleDrawer: () => void;
  totalCOP: () => number;
  itemCount: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],
      isOpen: false,
      addItem: (item, qty = 1) => {
        set((state) => {
          const existing = state.items.find((it) => it.id === item.id);
          if (existing) {
            return {
              items: state.items.map((it) =>
                it.id === item.id ? { ...it, quantity: it.quantity + qty } : it
              ),
              isOpen: true,
            };
          }
          return { items: [...state.items, { ...item, quantity: qty }], isOpen: true };
        });
      },
      removeItem: (id) => {
        set((state) => ({ items: state.items.filter((it) => it.id !== id) }));
      },
      updateQuantity: (id, qty) => {
        if (qty <= 0) {
          get().removeItem(id);
          return;
        }
        set((state) => ({
          items: state.items.map((it) => (it.id === id ? { ...it, quantity: qty } : it)),
        }));
      },
      clearCart: () => set({ items: [] }),
      toggleDrawer: () => set((state) => ({ isOpen: !state.isOpen })),
      totalCOP: () => get().items.reduce((sum, it) => sum + it.priceCOP * it.quantity, 0),
      itemCount: () => get().items.reduce((sum, it) => sum + it.quantity, 0),
    }),
    {
      name: 'shopping_cart_storage',
      storage: createJSONStorage(() => localStorage),
    }
  )
);
```

---

## 5. React 19 Island: Conversational AI Assistant with Vercel AI SDK 5

```tsx
// src/components/islands/AIChatWidget.tsx
import React, { useState } from 'react';
import { useChat } from 'ai/react';

export function AIChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-primary text-white p-4 rounded-full shadow-lg hover:scale-105 transition-all flex items-center gap-2 font-medium"
        >
          <span>AI Shopping Assistant</span>
        </button>
      )}

      {isOpen && (
        <div className="bg-surface border border-outline w-80 sm:w-96 h-[480px] rounded-2xl shadow-2xl flex flex-col overflow-hidden">
          <div className="bg-primary text-white p-4 flex justify-between items-center">
            <h3 className="font-semibold text-sm">AI Shopping Concierge</h3>
            <button onClick={() => setIsOpen(false)} className="text-white/80 hover:text-white text-lg">✕</button>
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-3">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`p-3 rounded-xl text-sm ${
                  m.role === 'user' ? 'bg-primary/10 text-on-surface self-end ml-8' : 'bg-surface-variant text-on-surface mr-8'
                }`}
              >
                {m.content}
              </div>
            ))}
            {isLoading && <div className="text-xs text-muted animate-pulse">Generating recommendation...</div>}
          </div>

          <form onSubmit={handleSubmit} className="p-3 border-t border-outline flex gap-2">
            <input
              value={input}
              onChange={handleInputChange}
              placeholder="What product are you looking for today?"
              className="flex-1 bg-surface-variant text-sm px-3 py-2 rounded-lg focus:outline-none"
            />
            <button type="submit" className="bg-primary text-white text-xs px-3 py-2 rounded-lg font-medium">
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
```

---

## 6. 5 Production Patterns in Frontend Architecture

### Pattern 1: SSR Middleware with Secure Directus Auth
Validates user sessions on every request using secure HTTP-only cookies in `src/middleware.ts` before rendering protected pages.

### Pattern 2: Anti-CLS Server Islands with Fallback Skeletons
Renders personalized header and user account slots using `<UserSlot server:defer><Skeleton slot="fallback"/></UserSlot>` to guarantee zero cumulative layout shift.

### Pattern 3: Persistent Client State with Zustand 5
Persists shopping cart items in `localStorage` with automated hydration safety and reactive drawer triggers.

### Pattern 4: Multi-Gateway Checkout Action with Zod Validation
Processes payments through Wompi, ePayco, dLocal Go, Stripe, Mercado Pago, or COD with WhatsApp OTP verification in Astro Actions.

### Pattern 5: Streaming AI Concierge with Tool Calling
Connects Vercel AI SDK 5 `useChat()` with server-side LLM endpoints to query Directus catalog items dynamically.

---

## 7. Anti-Patterns & Common Gotchas

1. **Exposing JWTs in Client Storage**: Never save Directus access or refresh tokens in `localStorage` or `sessionStorage`. Always use `httpOnly` cookies handled in Astro SSR middleware.
2. **Unnecessary Client-Side Hydration**: Avoid attaching `client:load` to static content; default to zero-JS Astro components.
3. **Missing Fallback Slots on Server Islands**: Failing to provide a placeholder slot in `<Widget server:defer>` leads to layout shift (CLS).
