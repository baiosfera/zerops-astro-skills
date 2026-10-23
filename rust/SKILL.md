---
name: rust
description: "Trigger: rust, rust@stable, axum, tokio, sqlx, cargo, rustls, cargo build --release, musl, rust-hello-world. Architect, build, cache, deploy, and operate high-performance Rust web services and microservices on Zerops Incus LXC runtimes."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# Rust — Zerops High-Performance Runtime & Compilation (v1.1)

## Activation Contract
Activate whenever architecting, compiling, caching, or operating high-performance Rust web services (Axum, Actix, Tokio), CLI tools, or microservices on Zerops Incus LXC runtimes (`runtime: ubuntu/rust@stable` or `alpine/rust@stable`).

## Hard Rules & Positive Guidance
- **Runtime Base Selection**:
  - `ubuntu/rust@stable`: Recommended for faster compilation and full glibc/OpenSSL compatibility.
  - `alpine/rust@stable`: Used for completely static musl binary distribution.
- **Cargo Build Caching (MANDATORY)**: Always cache `target/` and `~/.cargo/` in `zerops.yaml` to prevent rebuilding dependencies on every deployment.
- **Release Optimization**: Compile production binaries with `cargo build --release`. Strip debug symbols (`strip target/release/<binary>`) to minimize container image sizes.
- **Port Binding**: Bind Axum/Actix web listeners to `0.0.0.0` on port `3000` (or `${PORT}`).
- **Container Execution**: Run cargo tests inside the runtime container via SSH (`ssh {hostname} "cd /var/www && cargo test"`).

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Web Frameworks | Axum with Tokio and SQLx | [`references/usage.md#frameworks`](file:///var/www/.agents/skills/rust/references/usage.md) |
| Compilation Caching | Cargo cache directories in zerops.yaml | [`references/infra.md#caching`](file:///var/www/.agents/skills/rust/references/infra.md) |
| Static Linking | Musl target compilation for ultra-lean deploys | [`references/infra.md#static-linking`](file:///var/www/.agents/skills/rust/references/infra.md) |

## Critical Workflows
1. Configure Rust service in `zerops.yaml` with Cargo caches.
2. Build release binary and verify artifacts.
3. Validate endpoint health with physical probe (`curl -s http://<service>:3000/health`).

## References
- [`references/usage.md`](file:///var/www/.agents/skills/rust/references/usage.md) — Axum web patterns, Tokio async runtime, SQLx database pools, and Cargo testing.
- [`references/infra.md`](file:///var/www/.agents/skills/rust/references/infra.md) — Zerops deployment manifests, Cargo caching, compile-time tuning, and musl static builds.
