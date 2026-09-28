---
name: frnt
description: "Trigger: frnt, frontend, ui stack, astro 5, react 19, tailwind 4, zustand 5, checkout-funnels, payment-gateways, email-marketing, brandbook, directus auth, cloudflare cdn, ai-sdk-5, playwright, bun, typescript, seo-aeo-geo, zod-4. Master Frontend, UI/UX, Client State, Auth, E2E Testing & Edge CDN Orchestrator in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.1"
---

# `frnt` — Master Frontend, UI/UX & Edge CDN Orchestrator (v3.1)

## Activation Contract
Activate when designing, architecting, building, or optimizing client interfaces, Astro 5 SSR Server Islands, React 19 interactive components (React Compiler), Tailwind CSS 4 styling (OKLCH), Zustand 5 stores, checkout funnels, transactional emails, Directus auth, E2E testing with Playwright, or Cloudflare Edge CDN routing.

## Hard Rules & Positive Guidance
- **Pre-Flight Epistemic Gate (MANDATORY)**: BEFORE authoring frontend code, proposing implementation plans, or modifying files, the agent MUST evaluate the user request against the Active Sub-Skills Dispatch Table below. The agent MUST open and READ the matching sub-skill `SKILL.md` via its canonical `file:///` URI. Proceeding without inspecting the required sub-skills violates the architectural contract.
- **Brand SSoT Ingestion**: Ingest client typography, colors, and design tokens directly from the local single-tenant path `/brand/brandbook.json` and `/brand/fase0_system_prompt.md`. Transpile W3C DTCG tokens into Tailwind 4 theme variables.
- **Zero Layout Shift (CLS = 0)**: All Astro Server Islands MUST provide fallback skeletons (`slot="fallback"`) to ensure 100% Core Web Vitals.
- **Secure Customer Auth**: Directus session tokens MUST be stored exclusively in `httpOnly`, `secure`, `sameSite: 'lax'` cookies handled in Astro SSR middleware. Never expose JWTs in `localStorage`.
- **Automated E2E Verification**: E-commerce shopping bag and checkout flows MUST be covered by deterministic Playwright test suites (`playwright`).
- **Strict Typing**: Product variants, cart payloads, and Astro Action inputs MUST enforce TypeScript interfaces and Zod schemas.
- **Fractal CoHaLo Execution**: Enforce command hygiene (`timeout 10s`), wait limits (`WaitMsBeforeAsync: 10000`), zero orphan tasks (`manage_task action="kill"`), and sensor verification (HTTP 200 on UI endpoint).
- **Zero Deletion Invariant**: Consult [`references/usage.md`](file:///var/www/.agents/skills/frnt/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/frnt/references/infra.md) for full lossless APIs.

## Active Sub-Skills Dispatch Table

| Domain / Capability | Sub-Skill | Canonical SSoT Pointer | Role & Boundary |
|---|---|---|---|
| **Core SSR Framework** | `astro-web` | [`astro-web`](file:///var/www/.agents/skills/astro-web/SKILL.md) | Server Islands, Content Layer, SSR middleware, routing |
| **Zerops Bun Runtime** | `bun` | [`bun`](file:///var/www/.agents/skills/bun/SKILL.md) | Native `alpine/bun@1.3.9` runtime, package management, build |
| **Interactive Islands** | `react-19` | [`react-19`](file:///var/www/.agents/skills/react-19/SKILL.md) | Reactive components optimized with native React Compiler |
| **Client State Store** | `zustand-5` | [`zustand-5`](file:///var/www/.agents/skills/zustand-5/SKILL.md) | Lightweight persistent cart store and slide-over drawer |
| **E2E Test Automation** | `playwright` | [`playwright`](file:///var/www/.agents/skills/playwright/SKILL.md) | End-to-end checkout verification and regression tests |
| **Strict Type Safety** | `typescript` | [`typescript`](file:///var/www/.agents/skills/typescript/SKILL.md) | Strict typing for cart items, variants, and API payloads |
| **Schema Validation** | `zod-4` | [`zod-4`](file:///var/www/.agents/skills/zod-4/SKILL.md) | Input validation schemas for checkout forms and actions |
| **Styling & Theme** | `tailwind-4` | [`tailwind-4`](file:///var/www/.agents/skills/tailwind-4/SKILL.md) | OKLCH colors, CSS theme variables, zero-runtime styling |
| **Brand Identity SSoT** | `brandbook` | [`brandbook`](file:///var/www/.agents/skills/brandbook/SKILL.md) | Ingestion of `/brand/brandbook.json` and typography stacks |
| **Search & Discovery** | `seo-aeo-geo` | [`seo-aeo-geo`](file:///var/www/.agents/skills/seo-aeo-geo/SKILL.md) | Schema.org `Product` JSON-LD, `/llms.txt`, OpenGraph tags |
| **Checkout UI & Funnels**| `checkout-funnels` | [`checkout-funnels`](file:///var/www/.agents/skills/checkout-funnels/SKILL.md) | Multi-country checkout UI, 1-Click upsells, DANE geocoding, Meta CAPI |
| **Payment Gateways & Drivers**| `payment-gateways` | [`payment-gateways`](file:///var/www/.agents/skills/payment-gateways/SKILL.md) | Multi-gateway driver: Wompi SHA-256, Bold, Stripe, COD OTP |
| **Customer Auth BaaS** | `directus` | [`directus`](file:///var/www/.agents/skills/directus/SKILL.md) | Session cookies, customer profile endpoints, Magic Links |
| **AI Gateway & Proxy** | `bifrost` | [`bifrost`](file:///var/www/.agents/skills/bifrost/SKILL.md) | Universal OpenAI drop-in proxy for client-side AI chat & streaming |
| **Edge CDN & Ingress** | `cloudflare` | [`cloudflare`](file:///var/www/.agents/skills/cloudflare/SKILL.md) | Edge caching, Full Strict SSL, Turnstile anti-bot |

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 4D Matrix & SSR Strategy | Astro 5 Server Islands vs SPA, Next.js, SSG | [`references/usage.md#1-4d-comparative-architectural-matrix-frontend-rendering-strategies`](file:///var/www/.agents/skills/frnt/references/usage.md) |
| Sub-Skills Inventory | Direct pointers to Astro, React 19, Tailwind 4 & sub-skills | [`references/usage.md#2-sub-skills-inventory--direct-file-pointers`](file:///var/www/.agents/skills/frnt/references/usage.md) |
| SSR Auth Middleware | Directus SDK session verification with HTTP-only cookies | [`references/usage.md#3-astro-5-ssr-authentication-middleware-with-directus-sdk`](file:///var/www/.agents/skills/frnt/references/usage.md) |
| Zustand 5 Cart Store | Persistent shopping cart with hydration safety | [`references/usage.md#4-global-shopping-cart-state-with-zustand-5`](file:///var/www/.agents/skills/frnt/references/usage.md) |
| AI Shopping Assistant | Vercel AI SDK 5 chat widget with SSE streaming | [`references/usage.md#5-react-19-island-conversational-ai-assistant-with-vercel-ai-sdk-5`](file:///var/www/.agents/skills/frnt/references/usage.md) |
| Incus LXC Topology | Astro SSR on Bun 1.3 with Cloudflare Edge CDN | [`references/infra.md#1-frontend-runtime-topology-in-zerops`](file:///var/www/.agents/skills/frnt/references/infra.md) |
| zerops.yaml Lifecycle | Build commands, cache directories & readiness probes | [`references/infra.md#2-canonical-lifecycle-recipe-zeropsyaml`](file:///var/www/.agents/skills/frnt/references/infra.md) |
| Dev Server Supervision | Launch hot-reloading dev server via zerops_dev_server | [`references/infra.md#3-persistent-dev-server-supervision`](file:///var/www/.agents/skills/frnt/references/infra.md) |
| Production Recipes JSON | Middleware, store, and server island recipe indexes | [`assets/frnt_production_recipes.json`](file:///var/www/.agents/skills/frnt/assets/frnt_production_recipes.json) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/frnt-validate.sh`](file:///var/www/.agents/skills/frnt/scripts/frnt-validate.sh) |

## Execution Steps
1. Verify pre-conditions and load matching sub-skills via the Active Sub-Skills Dispatch Table.
2. Ingest brand tokens from `/brand/brandbook.json` to Tailwind 4 theme variables.
3. Configure frontend environment variables in Zerops (`DIRECTUS_URL`, `NATS_URL`).
4. Implement Astro 5 SSR middleware with secure HTTP-only cookies.
5. Author reactive islands using React 19 Compiler or lightweight client state.
6. Verify checkout flows and visual integrity via Playwright E2E suites.
7. Execute physical validation sensor (`scripts/frnt-validate.sh`) confirming exit code 0.

## Output Contract
- High-converting, zero-layout-shift Astro 5 SSR web application running on Bun 1.3 in Zerops.
- Secure Directus authentication, multi-gateway checkout, Playwright coverage, and passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/frnt/references/usage.md) — 4D matrix, sub-skills inventory, SSR auth middleware, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/frnt/references/infra.md) — Bun runtime topology, zerops.yaml, and CoHaLo harness.
- [`assets/frnt_production_recipes.json`](file:///var/www/.agents/skills/frnt/assets/frnt_production_recipes.json) — Production middleware and store recipes.
- [`scripts/frnt-validate.sh`](file:///var/www/.agents/skills/frnt/scripts/frnt-validate.sh) — Deterministic quality & token validation sensor.
