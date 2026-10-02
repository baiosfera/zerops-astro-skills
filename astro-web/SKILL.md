---
name: astro-web
description: "Trigger: astro-web, astro 5, astro ssr, server islands, content layer, astro actions, craft anti-slop, brandbook tokens, taste design, astro nats, astro valkey, astro postgresql, bun astro, deploy zerops. Astro 5 SSR on Bun with Decoupled Lego Backend, Brandbook Tokens & Anti-Slop Craft in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.0"
---

# Astro 5 — High-Performance SSR & Disruptive Craft (v3.0)

## Activation Contract
Activate for Astro 5 SSR on Zerops: Server Islands (`server:defer`), Astro Actions (`astro:actions`), Content Layer API, Brandbook W3C DTCG tokens, Pre-flight Anti-Slop Craft Gates, Universal OAuth, or decoupled backend integrations (**`nats`**, **`valkey`**, **`postgresql`**, **`objectstorage`**).

## Hard Rules
- **Host & Ports**: Listen on `HOST: "0.0.0.0"` and `PORT: "3000"`. Client vars use `PUBLIC_`. Server secrets use `astro:env/server`.
- **Server Islands Key**: In rolling zero-downtime deploys, inject `ASTRO_KEY` across replicas for prop decryption.
- **Runtime & Base**: Build on `ubuntu/bun@1.3.9` to prevent Alpine musl binding failures in Rolldown; deploy with `[dist, node_modules, package.json]`.
- **Decoupled Backend**: Astro Actions handle mutations agnostically with Zod validation. Connect via Zerops internal DNS and wire connection strings via shell env (`$queue_connectionString`, `${cache_connectionString}`, `${db_connectionString}`).
- **Tailwind CSS 4**: Integrate via `@tailwindcss/vite` in `astro.config.mjs` with CSS-first `@theme` design tokens.
- **Pre-flight Craft Gate**: Calibrate 3 Dials: *Variance* (asymmetric layout), *Motion* (smooth reveals), *Density* (brand-calibrated). Prohibit untinted gray and dark purple gradients.
- **Hygiene & Sensors**: Strict timeouts (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans, sensor HTTP 200 on `/`. Consult [`references/usage.md`](file:///var/www/.agents/skills/astro-web/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/astro-web/references/infra.md).

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Matrix | Astro 5 vs Next 15, Remix, Nuxt | [`references/usage.md#1-matrix`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Content Layer | Universal Custom Loader with caching | [`references/usage.md#2-content-layer`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Server Islands | Defer SSR with `ASTRO_KEY` | [`references/usage.md#3-server-islands`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Universal OAuth | Agnostic OAuth 2.0 / OIDC component | [`references/usage.md#4-oauth`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Actions & NATS | Typed mutations, Valkey lock & NATS | [`references/usage.md#5-actions`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Container API | Isolated component tests with Vitest | [`references/usage.md#6-container-api`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Anti-Slop Gate | Variance, Motion, Density calibration | [`references/usage.md#7-anti-slop`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Brand Tokens | Transpile DTCG to Tailwind 4 `@theme` | [`references/usage.md#8-brand-tokens`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Topology | Bun 1.3, NATS 2.12, Valkey 7.2, Postgres 18 | [`references/infra.md#2-topology`](file:///var/www/.agents/skills/astro-web/references/infra.md) |
| Lifecycle | Dev (`zsc noop`) + Prod (`bun build`) | [`references/infra.md#3-lifecycle`](file:///var/www/.agents/skills/astro-web/references/infra.md) |
| Sensor | Deterministic quality & AST sensor | [`scripts/astro-web-validate.sh`](file:///var/www/.agents/skills/astro-web/scripts/astro-web-validate.sh) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/astro-web/references/usage.md) — Recipes, Content Layer, Server Islands, Actions, Container API, Anti-Slop.
- [`references/infra.md`](file:///var/www/.agents/skills/astro-web/references/infra.md) — Multi-service topology, `import.yaml`, `zerops.yaml`, secret isolation.
- [`assets/astro_production_recipes.json`](file:///var/www/.agents/skills/astro-web/assets/astro_production_recipes.json) — 5 production deployment recipes.
- [`assets/import_template.yaml`](file:///var/www/.agents/skills/astro-web/assets/import_template.yaml) — Production import template for Astro SSR stack.
- [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/astro-web/assets/zerops_template.yaml) — Full zerops.yaml template for Astro SSR.
- [`scripts/astro-web-validate.sh`](file:///var/www/.agents/skills/astro-web/scripts/astro-web-validate.sh) — Deterministic quality & token validation sensor.
