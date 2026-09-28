---
name: ubuntu
description: "Trigger: ubuntu, zerops ubuntu, base ubuntu 24, glibc, cgo, node-gyp, apt-get, native compilation. Architecture, compilation pipelines, glibc performance, and Zerops runtime deployment for Ubuntu 24.04 LTS."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# Ubuntu — Zerops Native Linux Architecture & Compilation Engine (v1.0)

## Activation Contract
Activate whenever authoring, building, or troubleshooting workloads on Ubuntu 24.04 LTS in Zerops (`base: ubuntu@24` or `os: ubuntu`), compiling C/C++/Rust/Go CGO binaries, building Python C-extension wheels, configuring native Node addons (`node-gyp`), running Deno, or evaluating Ubuntu vs Alpine runtime selection.

## Hard Rules
- **Rule 1 (Continuous Present & Version Invariant)**: Target **Ubuntu 24.04 LTS (Noble Numbat)** exclusively (`base: ubuntu@24`). Legacy versions (`ubuntu@22`) are strictly deprecated for new services.
- **Rule 2 (Native Package Management)**: Always use `sudo apt-get update && sudo apt-get install -y <pkg>` (sudo is required as Zerops runs unprivileged). Never use `apk` in Ubuntu environments. Clean `/var/lib/apt/lists/*` to minimize build layer sizes.
- **Rule 3 (Fractal CoHaLo Bounded Execution)**: All synchronous system commands MUST use strict timeouts (`timeout 10s`), synchronous wait (`WaitMsBeforeAsync: 10000`), and terminate orphan background processes with `manage_task action="kill"`.
- **Rule 4 (Zero-Guessing Scaling)**: Do NOT author arbitrary `verticalAutoscaling` ranges in `import.yaml`. Zerops manages vertical autoscaling natively out-of-the-box.

## Decision Gates

| Task / Scenario | Recommended Strategy | Reference / Asset |
|---|---|---|
| CGO, Python Wheels & Native Compilations | GCC 14, libvips, node-gyp, Deno setup | [`references/usage.md`](file:///var/www/.agents/skills/ubuntu/references/usage.md) |
| Production Recipes (Go, Python, Node, Deno) | 5 Copy-paste production patterns | [`references/usage.md`](file:///var/www/.agents/skills/ubuntu/references/usage.md) |
| Zerops `zerops.yaml` & Build Envelope | Build vs Run, 8GB RAM build envelope, deployFiles | [`references/infra.md`](file:///var/www/.agents/skills/ubuntu/references/infra.md) |
| Ubuntu LXC vs Alpine LXC Benchmarks | Direct architecture comparison on Incus LXC | [`references/infra.md`](file:///var/www/.agents/skills/ubuntu/references/infra.md) |
| Compilation Flags & apt-get Packages | JSON catalog of verified build commands | [`assets/ubuntu_compilation_recipes.json`](file:///var/www/.agents/skills/ubuntu/assets/ubuntu_compilation_recipes.json) |

## Critical Workflows / Execution Steps
1. Determine runtime requirements (glibc vs musl, CGO, wheels, Deno) and consult [`references/usage.md`](file:///var/www/.agents/skills/ubuntu/references/usage.md).
2. Configure `zerops.yaml` with `base: ubuntu@24` or `os: ubuntu` and author cached `prepareCommands`.
3. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
4. **Circuit Breaker (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500 / timeout) before escalating.
5. **Sensor Attestation**: Verify physical sensor check (exit code 0 / HTTP 200) and format output deterministically.

## Output Contract
- Validated `zerops.yaml` or `import.yaml` targeting Ubuntu 24.04 LTS.
- Verified build and compilation artifacts with zero orphaned tasks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/ubuntu/references/usage.md) — Native compilation, glibc 2.39 features, 5 production patterns, and anti-patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/ubuntu/references/infra.md) — Incus LXC model, Zerops build lifecycle, benchmarks vs Alpine LXC, and CoHaLo process hygiene.
- [`assets/ubuntu_compilation_recipes.json`](file:///var/www/.agents/skills/ubuntu/assets/ubuntu_compilation_recipes.json) — Compilation flags and package matrices for Ubuntu 24.
- [`scripts/ubuntu-validate.sh`](file:///var/www/.agents/skills/ubuntu/scripts/ubuntu-validate.sh) — Physical integrity validator for the ubuntu skill suite.
