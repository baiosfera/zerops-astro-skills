---
name: astro-web
description: "Trigger: astro-web, astro 5, astro ssr, server islands, content layer, astro actions, craft anti-slop, brandbook tokens. Astro 5 SSR on Bun with Decoupled Lego Backend & Brandbook Tokens in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.1"
---

# Astro 5 — High-Performance SSR & Disruptive Craft (v3.1)

## Activation Contract
Activate when architecting, developing, or optimizing Astro 5 SSR applications on Zerops: Server Islands (`server:defer`), Astro Actions (`astro:actions`), Content Layer API, Brandbook W3C DTCG tokens, Pre-flight Anti-Slop Craft Gates, or decoupled backend integrations (`nats`, `valkey`, `postgresql`, `objectstorage`).

## Hard Rules & Positive Guidance
- **Host & Ports**: Bind listeners to `HOST: "0.0.0.0"` and `PORT: "3000"`. Prefix public client variables with `PUBLIC_`. Import server secrets via `astro:env/server`.
- **Server Islands Key**: In rolling zero-downtime deployments, inject `ASTRO_KEY` across all replicas to decrypt deferred component props securely.
- **Runtime & Base Selection**: Build on `ubuntu/bun@1.3.9` to ensure full CGO/glibc compatibility and avoid Rolldown musl binding errors. Deploy with artifacts `[dist, node_modules, package.json]`.
- **Decoupled Backend Architecture**: Handle mutations via typed Astro Actions with Zod schemas. Connect services through Zerops internal DNS (`http://<service>:<port>`) and reference credentials via environment variables (`$queue_connectionString`, `${cache_connectionString}`, `${db_connectionString}`).
- **Decoupled Staging Invariant**: Base recipe `06-astro-web.yaml` provisions production exclusively. Staging is strictly opt-in and provisioned through decoupled `06b-astro-web-staging.yaml`.
- **Tailwind CSS 4**: Integrate via `@tailwindcss/vite` in `astro.config.mjs` with CSS-first `@theme` design tokens.
- **Pre-flight Craft Gate**: Calibrate 3 Dials: *Variance* (asymmetric layouts), *Motion* (smooth reveals), *Density* (brand-calibrated). Avoid untinted gray backgrounds and saturated purple gradients.
- **Dynamic PostgreSQL SSR**: Render dynamic catalogs directly from PostgreSQL in the continuous present (`date >= NOW()`). Hydrate authenticated user profiles from session cookies to prevent checkout friction.
- **Standalone Pages & Mobile UX**: Import `theme.css` via `<style is:global>` on standalone pages lacking layouts to emit Vite CSS. Omit `capture` on file inputs to preserve native gallery choice. Scale canvas uploads with `Math.min(maxWidth/w, maxHeight/h, 1)` for strict aspect-ratio parity. Scope admin auth cookies to `path: "/"` and guard 1-click magic links against crawler prefetch.

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Architecture Matrix | Astro 5 vs Next 15, Remix, Nuxt | [`references/usage.md#1-matrix`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Content Layer | Universal Custom Loader with caching | [`references/usage.md#2-content-layer`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Server Islands | Defer SSR components with ASTRO_KEY | [`references/usage.md#3-server-islands`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Actions & NATS | Typed mutations with Valkey lock & NATS | [`references/usage.md#5-actions`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Anti-Slop Gate | Variance, Motion, Density calibration | [`references/usage.md#7-anti-slop`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Admin & Mobile UX | Standalone CSS, Gallery picker, aspect ratio, crawler defense | [`references/usage.md#11-admin-invariants`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Topology | Bun 1.3, NATS 2.12, Valkey 7.2, Postgres 18 | [`references/infra.md#2-topology`](file:///var/www/.agents/skills/astro-web/references/infra.md) |
| Lifecycle | Dev (`zsc noop`) + Prod (`bun build`) | [`references/infra.md#3-lifecycle`](file:///var/www/.agents/skills/astro-web/references/infra.md) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/astro-web/references/usage.md) — Content Layer recipes, Server Islands, typed Actions, OAuth, and Anti-Slop craft.
- [`references/infra.md`](file:///var/www/.agents/skills/astro-web/references/infra.md) — Multi-service topology, import.yaml, zerops.yaml, and secret isolation.
