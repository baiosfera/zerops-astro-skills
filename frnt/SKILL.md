---
name: frnt
description: "Trigger: frnt, frontend architecture, ui orchestrator, frontend stack, web frontend, client architecture, zerops frontend. Master Frontend, UI/UX & Edge CDN Orchestrator in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.2"
---

# `frnt` — Master Frontend, UI/UX & Edge CDN Orchestrator (v3.2)

## Activation Contract
Activate when designing, architecting, building, or optimizing client web applications, Astro 5 SSR Server Islands, responsive UI architectures, client state, or edge CDN delivery on Zerops. Atomic tasks on a single framework execute directly with domain skills (`astro-web`, `react-19`, `tailwind-4`).

## Hard Rules & Positive Guidance
- **Pre-Flight Epistemic Gate**: Evaluate frontend requests against the sub-skills table. Open and inspect matching sub-skills before writing client code.
- **Brand SSoT Ingestion**: Ingest client typography, colors, and tokens from `/brand/brandbook.json` and `/brand/fase0_system_prompt.md`. Transpile W3C DTCG tokens into Tailwind 4 CSS theme variables.
- **Zero Layout Shift (CLS = 0)**: Provide fallback skeletons (`slot="fallback"`) on all Astro Server Islands to guarantee 100% Core Web Vitals.
- **Secure Customer Auth**: Store Directus session tokens exclusively in `httpOnly`, `secure`, `sameSite: 'lax'` cookies handled in Astro SSR middleware.
- **Automated E2E Verification**: Cover critical customer journeys (cart, checkout, auth) with deterministic Playwright test suites.
- **Strict Typing & Schema Validation**: Enforce TypeScript interfaces and Zod schemas across product variants, cart payloads, and Action inputs.
- **Fractal CoHaLo Bounded Execution**: Run commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks. Verify UI health with HTTP 200 probes on `/`.

## Active Sub-Skills Dispatch Table

| Capability | Sub-Skill | Role & Boundary |
|---|---|---|
| **Core SSR** | `astro-web` ([`SKILL.md`](file:///var/www/.agents/skills/astro-web/SKILL.md)) | Astro 5 SSR, Server Islands & routing |
| **Interactive Islands** | `react-19` ([`SKILL.md`](file:///home/zerops/.gemini/antigravity-cli/skills/react-19/SKILL.md)) | Client components with React Compiler |
| **Client State** | `zustand-5` ([`SKILL.md`](file:///home/zerops/.gemini/antigravity-cli/skills/zustand-5/SKILL.md)) | Lightweight persistent cart store |
| **Styling & Tokens** | `tailwind-4` ([`SKILL.md`](file:///home/zerops/.gemini/antigravity-cli/skills/tailwind-4/SKILL.md)) | OKLCH colors, CSS theme variables |
| **Funnels & CAPI** | `checkout-funnels` ([`SKILL.md`](file:///var/www/.agents/skills/checkout-funnels/SKILL.md)) | Multi-country checkout UI & Meta CAPI |
| **Payment Drivers** | `payment-gateways` ([`SKILL.md`](file:///var/www/.agents/skills/payment-gateways/SKILL.md)) | Wompi, Bold, Stripe, COD OTP & locks |
| **Edge Ingress** | `cloudflare` ([`SKILL.md`](file:///var/www/.agents/skills/cloudflare/SKILL.md)) | Edge caching & Turnstile anti-bot |

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| SSR Strategy | Astro 5 Server Islands vs SPA/Next.js | [`references/usage.md#1-rendering-strategies`](file:///var/www/.agents/skills/frnt/references/usage.md) |
| Auth Middleware | Directus SDK session with HTTP-only cookies | [`references/usage.md#3-ssr-auth-middleware`](file:///var/www/.agents/skills/frnt/references/usage.md) |
| Zustand Cart | Persistent shopping cart with hydration safety | [`references/usage.md#4-zustand-cart-state`](file:///var/www/.agents/skills/frnt/references/usage.md) |
| Runtime Topology | Astro SSR on Bun 1.3 with Cloudflare Edge | [`references/infra.md#1-frontend-runtime-topology`](file:///var/www/.agents/skills/frnt/references/infra.md) |

## Output Contract
- High-converting, zero-layout-shift Astro 5 SSR frontend running on Bun in Zerops.
- Passing physical sensors (`skills-suite-validate`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/frnt/references/usage.md) — Rendering matrix, SSR auth middleware, and Zustand store patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/frnt/references/infra.md) — Bun runtime topology, zerops.yaml build pipelines, and harness.
