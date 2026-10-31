---
name: bun
description: "Trigger: bun, bun.serve, bun.sql, bun.build, bun:test, bunx, runtime bun@1.4, bun@1.3.9, elysia, hono, fast http server, typescript nativo. Architect, develop, test, and deploy high-performance TypeScript/JavaScript services on native Bun and Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.2"
---

# Bun — Zerops Native Bun Runtime Engine (v2.2)

## Activation Contract
Activate whenever developing, building, testing, or running TypeScript/JavaScript services on native Bun (`runtime: ubuntu/bun@1.4`, `alpine/bun@1.4`, or `bun@1.3`), `Bun.serve`, native SQL (`bun:sqlite`, `bun.sql`), `bun test`, or lightweight HTTP frameworks (Elysia, Hono).

## Hard Rules & Positive Guidance
- **Runtime Base Selection**:
  - `ubuntu/bun@1.4`: Latest engine with full CGO/glibc compatibility, native compilation, and complex binary dependencies.
  - `alpine/bun@1.4`: Preferred for minimal, lean microservices with static dependencies.
  - `ubuntu/bun@1.3`: Stable legacy production base.
- **Native Bun Primitives**: Use `Bun.serve()` for high-throughput HTTP servers. Use `bun:test` for fast native test suites.
- **Dependency & Cache Management**:
  - Configure `cache: [node_modules]` in `zerops.yaml` to accelerate build pipelines.
  - Install dependencies using `bun install --frozen-lockfile` in CI/CD.
- **Container Execution**: Run application builds and tests inside the runtime container via SSH (`ssh {hostname} "cd /var/www && bun test"`), never on the ZCP control plane.
- **Port Binding**: Bind web services to `0.0.0.0` on port `3000` (or `${PORT}`).

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| HTTP API Services | Bun.serve with Elysia or Hono | [`references/usage.md#http-services`](file:///var/www/.agents/skills/bun/references/usage.md) |
| Native Testing & CI | bun test with coverage and assertions | [`references/usage.md#bun-test`](file:///var/www/.agents/skills/bun/references/usage.md) |
| zerops.yaml Build Pipeline | Multi-stage build and run configuration | [`references/infra.md#zerops-pipeline`](file:///var/www/.agents/skills/bun/references/infra.md) |
| Base Image Selection | Ubuntu vs Alpine trade-offs | [`references/infra.md#base-images`](file:///var/www/.agents/skills/bun/references/infra.md) |

## Critical Workflows
1. Configure service in `zerops.yaml` under `bun@1.3` with `prepareCommands` and `start`.
2. Develop using native TypeScript without separate transpile steps.
3. Validate tests with physical sensor (`ssh {hostname} "cd /var/www && bun test"`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/bun/references/usage.md) — Bun.serve patterns, Elysia/Hono frameworks, native SQLite/SQL, and bun test suites.
- [`references/infra.md`](file:///var/www/.agents/skills/bun/references/infra.md) — Zerops deployment manifests, caching strategies, base image matrix, and process hygiene.
