---
name: alpine
description: "Trigger: alpine, zerops alpine, base alpine, musl, apk add, static binary, lightweight runtime. Architecture, package management, musl libc, static builds, and native LXC deployment on Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# Alpine — Zerops Native Linux Architecture & Lightweight Engine (v1.0)

## Activation Contract
Activate whenever authoring, building, deploying, or troubleshooting workloads on Alpine Linux in Zerops (`base: alpine@3.20` or `os: alpine`), managing packages via `apk`, compiling pure static Go or Rust (`musl`) binaries, configuring ultra-lean static web servers, or evaluating Alpine vs Ubuntu runtime selection.

## Hard Rules
- **Rule 1 (Default Base Invariant)**: Use Alpine as the default base for 95% of standard web applications (Node.js, Bun, Astro, pure Go, Rust, PHP-FPM, pure Python). Switch to Ubuntu ONLY when strict `glibc` binary compatibility is required (CGO dynamic libraries, Python Data Science wheels, or Deno).
- **Rule 2 (Native Package Management)**: Always install packages using `sudo apk add --no-cache <pkg>` (sudo is required as Zerops runs unprivileged). Never use `apt-get` on Alpine. Always include `--no-cache` to prevent storing index tarballs in container layers.
- **Rule 3 (Zero-Guessing Scaling)**: Do NOT author arbitrary `verticalAutoscaling` blocks in `import.yaml`. Zerops manages vertical autoscaling natively out-of-the-box.
- **Rule 4 (Fractal CoHaLo Bounded Execution)**: All synchronous system commands MUST enforce timeouts (`timeout 10s`), synchronous wait (`WaitMsBeforeAsync: 10000`), and terminate orphan background processes with `manage_task action="kill"`.

## Decision Gates

| Task / Scenario | Recommended Strategy | Reference / Asset |
|---|---|---|
| Package Installation & APK standard | `sudo apk add --no-cache <pkg>`, musl toolchains | [`references/usage.md`](file:///var/www/.agents/skills/alpine/references/usage.md) |
| Production Recipes (Static, Go, Rust, Node) | 5 Copy-paste production patterns | [`references/usage.md`](file:///var/www/.agents/skills/alpine/references/usage.md) |
| Alpine vs Ubuntu Direct Comparison | Architectural tradeoffs, musl vs glibc, RAM curves | [`references/infra.md`](file:///var/www/.agents/skills/alpine/references/infra.md) |
| Zerops Lifecycle (`zerops.yaml` & LXC) | Build envelope, Incus LXC native autoscaling | [`references/infra.md`](file:///var/www/.agents/skills/alpine/references/infra.md) |
| Verified APK Package Catalog | JSON matrix of tested build and runtime recipes | [`assets/alpine_compilation_recipes.json`](file:///var/www/.agents/skills/alpine/assets/alpine_compilation_recipes.json) |

## Critical Workflows / Execution Steps
1. Determine runtime compatibility (musl vs glibc) and consult [`references/usage.md`](file:///var/www/.agents/skills/alpine/references/usage.md).
2. Configure `zerops.yaml` with `base: alpine@3.20` or `os: alpine` and author cached `prepareCommands`.
3. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
4. **Circuit Breaker (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500 / timeout) before escalating.
5. **Sensor Attestation**: Verify physical sensor check (exit code 0 / HTTP 200) and format output deterministically.

## Output Contract
- Validated `zerops.yaml` and `import.yaml` targeting Alpine Linux on Zerops.
- Verified build and runtime execution with zero orphaned tasks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/alpine/references/usage.md) — Developer manual, APK package management, musl libc mechanics, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/alpine/references/infra.md) — Infrastructure manual, Incus LXC model, Alpine vs Ubuntu comparison, and CoHaLo process hygiene.
- [`assets/alpine_compilation_recipes.json`](file:///var/www/.agents/skills/alpine/assets/alpine_compilation_recipes.json) — Verified APK package recipes for Alpine.
- [`scripts/alpine-validate.sh`](file:///var/www/.agents/skills/alpine/scripts/alpine-validate.sh) — Physical integrity validator for the alpine skill suite.
