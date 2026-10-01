---
name: astro-web
description: "Trigger: astro-web, astro 5, astro ssr, server islands, content layer, astro actions, craft anti-slop, brandbook tokens, taste design, impeccable rules, astro directus, astro nats, astro valkey, astro postgresql, bun astro, deploy zerops. Astro 5 SSR on Bun 1.3 with Decoupled Lego Backend, Brandbook Tokens & Anti-Slop Craft in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.3"
---

# Astro 5 — High-Performance SSR & Disruptive Craft (v2.3)

## Activation Contract
Activate for Astro 5 SSR on Zerops: Server Islands (`server:defer`), Astro Actions, Brandbook W3C DTCG tokens, Pre-flight Anti-Slop Craft Gates, 1-Click OAuth, or decoupled backend integrations (**`nats`**, **`valkey`**, **`postgresql`**, **`directus`** conditional, and WhatsApp [`evolutiongo`](file:///var/www/.agents/skills/evolutiongo/SKILL.md)).

## Hard Rules
- **Host & Ports**: Listen on `HOST: "0.0.0.0"` and `PORT: "3000"`. Client vars use `PUBLIC_`. Server secrets use `astro:env/server`.
- **Server Islands Key**: In rolling deploys, inject `ASTRO_KEY`. Staging/prod are independent services (`astro-stage` and `astro-prod`).
- **Runtime**: Default to `bun@1.3.9` (<20ms boot); use `nodejs@24` for C++ addons.
- **Decoupled Backend**: Astro Actions (`astro:actions`) handle data agnostically. Directus is optional via Service Discovery; never hardcoded. Forms dispatch to Postgres, Web3Forms, NATS, or Directus.
- **Pre-flight Craft Gate**: Calibrate 3 Dials: *Variance* (asymmetric layout, ban 3-card grid), *Motion* (smooth reveals, ban bounce), *Density* (brand-calibrated). Prohibit untinted gray and dark purple gradients.
- **Brandbook Ingestion**: If `brandbook.json` exists, transpile tokens into Tailwind 4 `@theme` and generate `DESIGN.md`.
- **Anti-Invisible-Flaws**: Pages include OpenGraph/Twitter `<head>`, RGPD script-blocker, and verified backend actions.
- **Hygiene & Sensors**: Strict hygiene (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans, sensor HTTP 200 on `/`. Consult [`references/usage.md`](file:///var/www/.agents/skills/astro-web/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/astro-web/references/infra.md).

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Matrix | Astro 5 vs Next 15, Remix, Nuxt | [`references/usage.md#1-4d-comparative-architectural-matrix`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Content Layer | Custom loader with caching | [`references/usage.md#2-content-layer-api-with-directus-custom-loader-srccontentconfigts`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Server Islands | Defer SSR with `ASTRO_KEY` | [`references/usage.md#3-server-islands-serverdefer--clave-astro_key`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| OAuth | 1-Click login button | [`references/usage.md#4-1-click-google-oauth-component-googleloginbuttonastro`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Actions & NATS | Typed mutations & Valkey lock | [`references/usage.md#5-astro-actions-with-nats-rpc-directus-sdk--valkey`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| WhatsApp Island | Live pairing QR island | [`references/usage.md#6-whatsapp-live-qr-pairing-island-whatsappqrislandastro`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Anti-Slop Gate | Variance, Motion, Density dials | [`references/usage.md#7-anti-slop-craft-and-design-gate`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Brandbook Tokens | Transpile DTCG to Tailwind 4 | [`references/usage.md#8-brandbook-token-ingestion-into-tailwind-4`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Topology | Bun 1.3, NATS, Valkey, Postgres | [`references/infra.md#2-multi-service-provisioning-blueprint-importyaml`](file:///var/www/.agents/skills/astro-web/references/infra.md) |
| Lifecycle | Dev (`zsc noop`) + Prod (`bun build`) | [`references/infra.md#3-production-deployment-lifecycle-zeropsyaml`](file:///var/www/.agents/skills/astro-web/references/infra.md) |
| Sensor | Deterministic quality sensor | [`scripts/astro-web-validate.sh`](file:///var/www/.agents/skills/astro-web/scripts/astro-web-validate.sh) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/astro-web/references/usage.md) — Recipes, Content Layer, Server Islands, Actions, Anti-Slop gate, Brandbook ingestion.
- [`references/infra.md`](file:///var/www/.agents/skills/astro-web/references/infra.md) — Multi-service topology, `import.yaml`, `zerops.yaml`, secret isolation, CoHaLo harness.
- [`assets/astro_production_recipes.json`](file:///var/www/.agents/skills/astro-web/assets/astro_production_recipes.json) — Production deployment recipes and loader code.
- [`assets/import_template.yaml`](file:///var/www/.agents/skills/astro-web/assets/import_template.yaml) — Production import template for Astro SSR stack.
- [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/astro-web/assets/zerops_template.yaml) — Full zerops.yaml template for Astro SSR.
- [`scripts/astro-web-validate.sh`](file:///var/www/.agents/skills/astro-web/scripts/astro-web-validate.sh) — Deterministic quality & token validation sensor.
