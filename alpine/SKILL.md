---
name: alpine
description: "Trigger: alpine, zerops alpine, base alpine, musl, apk add, static binary, lightweight runtime. Architecture, package management, musl libc, static builds, and native LXC deployment on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# Alpine — Zerops Native Linux Architecture & Lightweight Engine (v1.1)

## Activation Contract
Activate whenever configuring, building, or optimizing lightweight Alpine Linux runtimes (`os: alpine`), musl libc compilation, `apk` package management, or deploying static binaries in Zerops Incus LXC containers.

## Hard Rules & Positive Guidance
- **Musl libc Boundary**: Alpine uses musl libc instead of glibc. Avoid Alpine when using precompiled proprietary binaries or Python/Node wheels that strictly depend on glibc.
- **Ephemeral Package Installation**: System packages installed via `sudo apk add` are ephemeral and wiped on fresh deploys. Durable package dependencies must be declared in `prepareCommands` in `zerops.yaml`.
- **Minimal Image Sizing**: Use Alpine for microservices where minimal memory footprint and instant boot times are prioritized.
- **Process Execution**: Run application builds and commands inside the Alpine container via SSH (`ssh {hostname} "cd /var/www && <cmd>"`).

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Alpine vs Ubuntu Selection | musl lean footprint vs glibc compatibility | [`references/usage.md#base-comparison`](file:///var/www/.agents/skills/alpine/references/usage.md) |
| apk Package Management | Dependency declaration in prepareCommands | [`references/usage.md#package-management`](file:///var/www/.agents/skills/alpine/references/usage.md) |
| zerops.yaml Configuration | Alpine pipeline syntax and caching | [`references/infra.md#zerops-pipeline`](file:///var/www/.agents/skills/alpine/references/infra.md) |

## Critical Workflows
1. Specify `os: alpine` in `zerops.yaml` for compatible runtimes (Go, Bun, Node, Python).
2. Declare system packages in `prepareCommands`.
3. Verify running service with physical sensor.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/alpine/references/usage.md) — Alpine architecture, musl libc trade-offs, and package management patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/alpine/references/infra.md) — Deployment manifests, LXC container isolation, and performance optimization.
