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
Activate when architecting or optimizing Astro 5 SSR on Zerops: Server Islands (`server:defer`), Astro Actions, Content Layer API, Brandbook DTCG tokens, Anti-Slop Craft Gates, or decoupled backends (`nats`, `valkey`, `postgresql`, `objectstorage`).

## Hard Rules & Positive Guidance
- **Host & Ports**: Bind `HOST: "0.0.0.0"` and `PORT: "3000"`. Prefix client env vars `PUBLIC_`; import server secrets via `astro:env/server`.
- **Server Islands Key**: Inject identical `ASTRO_KEY` across rolling replicas to decrypt deferred component props.
- **Runtime & Base Selection**: Build on `ubuntu/bun@1.3.9` for glibc/CGO parity and clean Rolldown bindings. Deploy artifacts `[dist, node_modules, package.json]`.
- **Decoupled Backend**: Handle mutations via Zod-typed Astro Actions. Connect services over internal DNS (`http://<service>:<port>`) using `${queue_connectionString}`, `${cache_connectionString}`, `${db_connectionString}`.
- **Decoupled Staging**: `06-astro-web.yaml` provisions production exclusively; staging uses opt-in `06b-astro-web-staging.yaml`.
- **Tailwind CSS 4**: Integrate `@tailwindcss/vite` in `astro.config.mjs` with CSS-first `@theme` tokens.
- **Craft Gate & Human Copy SSoT (`copy/*.md` -> `web/*.json`)**: Calibrate 3 Dials (*Variance*, *Motion*, *Density*) and enforce [`impeccable`](file:///var/www/.agents/skills/impeccable/SKILL.md), [`design-taste-frontend`](file:///var/www/.agents/skills/taste-skill/SKILL.md), and [`codecraft`](file:///var/www/.agents/skills/codecraft/SKILL.md) (including zero uppercase hero eyebrows). Treat `copy/*.md` as the **authoritative human-editable SSoT** and `web/copy_strings.es.json` as a derived UI dictionary: reconcile manual edits from `copy/*.md` into `web/copy_strings.es.json` (and Drive) before compiling pages.
- **Dynamic PostgreSQL SSR**: Query dynamic catalogs in continuous present (`date >= NOW()`) and hydrate sessions from cookies.
- **Standalone & Mobile UX**: Import `theme.css` via `<style is:global>` on standalone pages, omit `capture` on file inputs, scale uploads via `Math.min(maxWidth/w, maxHeight/h, 1)`, scope admin cookies `path: "/"`, and shield magic links from crawler prefetch.

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
