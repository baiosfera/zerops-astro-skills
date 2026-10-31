---
name: nodejs
description: "Trigger: nodejs, node, nodejs@26, nodejs@24, nodejs@22, type stripping, node:test, node:sqlite, fastify, express, nestjs, zerops nodejs runtime. Architect, develop, test, and deploy high-performance TypeScript/JavaScript services on native Node.js and Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "3.0"
---

# Node.js — Zerops Native Node.js Runtime Engine (v3.0)

## Activation Contract
Activate whenever developing, building, testing, or running Node.js services (`runtime: ubuntu/nodejs@26`, `nodejs@24`, `nodejs@22`), native TypeScript type stripping (`--experimental-strip-types`), `node:test`, `node:sqlite`, or frameworks (Fastify, Express, NestJS) on Zerops.

## Hard Rules & Positive Guidance
- **Runtime Base Selection**:
  - `ubuntu/nodejs@26`: Latest engine with V8 14.6+, native type stripping, low-overhead GC, and glibc compatibility (`sharp`, native C++ addons).
  - `ubuntu/nodejs@24`: Active LTS for enterprise stability and long-term production workloads.
  - `alpine/nodejs@24`: Preferred for minimal, lean microservices with purely JavaScript dependencies.
- **Package Management & Caching**: Cache `node_modules` or `.pnpm-store` in `zerops.yaml` to speed up deployment builds.
- **Port Binding**: Bind web applications to `0.0.0.0` on port `3000` (or `${PORT}`).
- **Container Execution Boundary**: Run npm/pnpm build, test, and database scripts inside the runtime container via SSH (`ssh {hostname} "cd /var/www && npm test"`).

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Framework Selection | Fastify for high throughput vs Express/NestJS | [`references/usage.md#frameworks`](file:///var/www/.agents/skills/nodejs/references/usage.md) |
| Native Node Features | Type stripping, node:test, node:sqlite | [`references/usage.md#native-features`](file:///var/www/.agents/skills/nodejs/references/usage.md) |
| zerops.yaml Configuration | Multi-stage build pipelines and caching | [`references/infra.md#zerops-pipeline`](file:///var/www/.agents/skills/nodejs/references/infra.md) |
| Base Image Comparison | Ubuntu vs Alpine trade-offs | [`references/infra.md#base-images`](file:///var/www/.agents/skills/nodejs/references/infra.md) |

## Critical Workflows
1. Configure Node.js service in `zerops.yaml` with npm/pnpm install and start commands.
2. Declare port mapping and environment variables.
3. Validate application health with physical sensor (`curl -s http://<service>:3000/health`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/nodejs/references/usage.md) — Node.js runtime features, framework patterns, native testing, and type stripping.
- [`references/infra.md`](file:///var/www/.agents/skills/nodejs/references/infra.md) — Zerops deployment manifests, dependency caching, base OS matrix, and process hygiene.
