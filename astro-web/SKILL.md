---
name: astro-web
description: "Trigger: astro-web, astro-framework, astro 5, astro ssr, server islands, content layer, astro actions, astro directus, astro nats, astro valkey, astro postgresql, astro whatsapp, bun astro, deploy astro zerops. Enterprise Astro 5 SSR Web Framework on Bun 1.3 & Node.js 24 with Directus, NATS, Valkey & WhatsApp in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# Astro 5 Web Framework — High-Performance SSR Engine (v2.1)

## Activation Contract
Activate when architecting, building, optimizing, or deploying Astro 5 SSR applications on Zerops, implementing Content Layer loaders, Server Islands (`server:defer`), Astro Actions, 1-Click Google OAuth, or backend integrations with **`directus`**, **`nats`**, **`valkey`**, **`postgresql`**, and WhatsApp gateways ([`evolutiongo`](file:///var/www/.agents/skills/evolutiongo/SKILL.md) / [`evolution-api`](file:///var/www/.agents/skills/evolution-api/SKILL.md)).

## Hard Rules
- **Host Binding**: Servers MUST listen on `HOST: "0.0.0.0"` and `PORT: "3000"` (never `localhost`).
- **Secret Isolation**: Client variables MUST use `PUBLIC_` prefix (e.g. `PUBLIC_DIRECTUS_URL`). Server secrets MUST use `astro:env/server` or server contexts and never reach client bundles.
- **Server Islands Key**: In multi-container rolling deployments, MUST inject `ASTRO_KEY` in `project.envVariables` to prevent prop decryption errors.
- **Runtime Preference**: Default to `bun@1.3.9` for instant cold boot (<20ms) and low RAM (~45MB); use `nodejs@24` for C++ glibc addons.
- **Fractal CoHaLo**: Enforce strict hygiene (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans (`manage_task action="kill"`), sensor (HTTP `200` on `/`).
- **Zero Deletion**: Consult [`references/usage.md`](file:///var/www/.agents/skills/astro-web/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/astro-web/references/infra.md) for full lossless APIs.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 4D Matrix & Comparison | Astro 5 SSR vs Next.js 15, Remix, Nuxt 3 | [`references/usage.md#1-4d-comparative-architectural-matrix`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Content Layer API | Custom Directus loader with incremental caching | [`references/usage.md#2-content-layer-api-with-directus-custom-loader-srccontentconfigts`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Server Islands (`server:defer`) | Defer dynamic SSR components with `ASTRO_KEY` | [`references/usage.md#3-server-islands-serverdefer--clave-astro_key`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| 1-Click Google OAuth | Directus Google OAuth 2.0 login button component | [`references/usage.md#4-1-click-google-oauth-component-googleloginbuttonastro`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Astro Actions & NATS Triad | Typed mutations, NATS RPC inventory lock & Valkey | [`references/usage.md#5-astro-actions-with-nats-rpc-directus-sdk--valkey`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| WhatsApp QR Pairing Island | Live WhatsApp pairing QR island (Evolution Go) | [`references/usage.md#6-whatsapp-live-qr-pairing-island-whatsappqrislandastro`](file:///var/www/.agents/skills/astro-web/references/usage.md) |
| Multi-Service `import.yaml` | Provision Bun 1.3, Directus, NATS, Valkey & PostgreSQL 18 | [`references/infra.md#2-multi-service-provisioning-blueprint-importyaml`](file:///var/www/.agents/skills/astro-web/references/infra.md) |
| Deployment Lifecycle | Dual Setup: Dev (`zsc noop`) + Prod Release (`bun build`) | [`references/infra.md#3-production-deployment-lifecycle-zeropsyaml`](file:///var/www/.agents/skills/astro-web/references/infra.md) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/astro-web-validate.sh`](file:///var/www/.agents/skills/astro-web/scripts/astro-web-validate.sh) |

## Execution Steps
1. Provision multi-service stack via Zerops `import.yaml` with `bun@1.3.9` runtime.
2. Configure `zerops.yaml` with `@astrojs/node` standalone build and `HOST: "0.0.0.0"`.
3. Wire backend endpoints to Directus (`DIRECTUS_URL`), NATS (`NATS_URL`), and Valkey (`VALKEY_URL`).
4. Set `ASTRO_KEY` in environment variables for secure Server Islands decryption across replicas.
5. Verify application health via physical sensor probe (`curl -f http://astro:3000/`).

## Output Contract
- Production Astro 5 SSR webapp running on Zerops Incus LXC (`bun@1.3.9`) with sub-millisecond RPC.
- Fully wired frontend communicating with Directus, NATS, Valkey, PostgreSQL, and passing physical sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/astro-web/references/usage.md) — 4D matrix, Content Layer, Server Islands, Astro Actions, WhatsApp QR island, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/astro-web/references/infra.md) — Multi-service topology, `import.yaml`, `zerops.yaml`, secret isolation, and CoHaLo harness.
- [`assets/astro_production_recipes.json`](file:///var/www/.agents/skills/astro-web/assets/astro_production_recipes.json) — Production deployment recipes and loader code.
- [`assets/import_template.yaml`](file:///var/www/.agents/skills/astro-web/assets/import_template.yaml) — Production import template for Astro SSR stack.
- [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/astro-web/assets/zerops_template.yaml) — Full zerops.yaml template for Astro SSR.
- [`scripts/astro-web-validate.sh`](file:///var/www/.agents/skills/astro-web/scripts/astro-web-validate.sh) — Deterministic quality & token validation sensor.
