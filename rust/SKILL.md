---
name: rust
description: "Trigger: rust, rust@stable, axum, tokio, sqlx, cargo, rustls, cargo build --release, musl, rust-hello-world. Architect, build, cache, deploy, and operate high-performance Rust web services and microservices on Zerops Incus LXC runtimes."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# Rust — Zerops High-Performance Runtime & Compilation Engine (v1.0)

## Activation Contract
Activate whenever architecting, compiling, caching, deploying, or operating Rust applications (`rust@stable`, `rust@latest`, `rust@nightly`), Axum 0.8+ HTTP routers, Tokio async runtimes, SQLx database connection pools, Cargo build caching, or standalone binary microservices on Zerops Incus LXC runtimes.

## Hard Rules
- **Rule 1 (Cargo Cache Directory Invariant)**: In `zerops.yaml`, ALWAYS set `build.envVariables.CARGO_HOME: ./.cargo` and cache both `.cargo/registry` and `target` to enable sub-second incremental builds.
- **Rule 2 (OpenSSL & TLS Feature Invariant)**: Avoid `native-tls` crates that require missing `pkg-config`/`libssl-dev`. Always enable `rustls-tls` features (e.g. `reqwest = { version = "0.12", features = ["rustls-tls"] }` and `sqlx = { version = "0.8", features = ["runtime-tokio-rustls"] }`).
- **Rule 3 (Strict Release Validation)**: Production builds MUST invoke `cargo build --release --locked` to ensure optimized compilation and strict `Cargo.lock` dependency validation.
- **Rule 4 (Micro-Footprint Artifact Deployment)**: Deliver only compiled binary artifacts in `deployFiles` (e.g. `./target/release/app` and `./target/release/migrate`) to achieve instant startup (<50ms) and minimal RAM footprints.
- **Rule 5 (Atomic Database Migrations)**: Database migrations MUST execute in `run.initCommands` using `zsc execOnce ${appVersionId} -- ./target/release/migrate`, never in `buildCommands`.
- **Rule 6 (Fractal CoHaLo Bounded Execution)**: All synchronous commands MUST enforce timeouts (`timeout 10s`), wait limit (`WaitMsBeforeAsync: 10000`), and terminate orphan background processes with `manage_task action="kill"`.

## Decision Gates

| Task / Scenario | Recommended Strategy | Reference / Asset |
|---|---|---|
| Runtime Base Choice (Rust vs Alpine vs Ubuntu) | `rust@stable` for standard; `alpine@3.24` for minimal static binary; `ubuntu` for C-bindings | [`references/infra.md`](file:///var/www/.agents/skills/rust/references/infra.md) |
| HTTP Service & Routing | Axum 0.8+ with `State`, `Json`, `TcpListener`, and Graceful Shutdown | [`references/usage.md`](file:///var/www/.agents/skills/rust/references/usage.md) |
| Async Database Pooling | SQLx 0.8+ with `runtime-tokio-rustls` and Postgres connection pool | [`references/usage.md`](file:///var/www/.agents/skills/rust/references/usage.md) |
| Cargo Caching & zerops.yaml | `CARGO_HOME: ./.cargo`, cache `.cargo/registry` + `target`, `readinessCheck` | [`references/infra.md`](file:///var/www/.agents/skills/rust/references/infra.md) |
| Verified Production Recipes | Production Axum server, SQLx pooling, Tokio background workers | [`assets/rust_production_recipes.json`](file:///var/www/.agents/skills/rust/assets/rust_production_recipes.json) |

## Critical Workflows / Execution Steps
1. Define runtime in `import.yaml` using `type: rust@stable` (or `type: alpine@3.24` for static binaries).
2. Configure `zerops.yaml` with `CARGO_HOME: ./.cargo`, `cargo build --release --locked`, and cache directives.
3. Deliver compiled binaries via `deployFiles` and register `readinessCheck` on HTTP port.
4. **Process Hygiene & Bounded Execution (CoHaLo)**: Execute commands with `timeout 10s`, `WaitMsBeforeAsync: 10000`, and clean orphan tasks with `manage_task action="kill"`.
5. **Circuit Breaker (CoHaLo)**: Limit retries to 2 attempts on failure (HTTP 500 / timeout) before escalating.
6. **Sensor Attestation**: Verify physical sensor check (HTTP 200 on `readinessCheck` port or exit code 0).

## Output Contract
- Validated `import.yaml` and `zerops.yaml` manifests targeting Rust on Zerops.
- Verified compilation, atomic migrations, and binary execution with zero orphaned tasks.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/rust/references/usage.md) — Developer manual, Rust 1.85+, Axum 0.8+ HTTP router, Tokio 1.40+, SQLx 0.8+ with rustls, and polyglot patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/rust/references/infra.md) — Infrastructure manual, `zerops.yaml` prod/dev setups, CARGO_HOME caching, target caching, Four-Way comparison, and CoHaLo process hygiene.
- [`assets/rust_production_recipes.json`](file:///var/www/.agents/skills/rust/assets/rust_production_recipes.json) — Production-ready recipes for Axum web server, SQLx pool, and Cargo build cache.
- [`assets/import_template.yaml`](file:///var/www/.agents/skills/rust/assets/import_template.yaml) — Clean `import.yaml` template with native elastic autoscaling.
- [`assets/zerops_template.yaml`](file:///var/www/.agents/skills/rust/assets/zerops_template.yaml) — Production and development `zerops.yaml` configuration with caching and atomic migrations.
- [`scripts/rust-validate.sh`](file:///var/www/.agents/skills/rust/scripts/rust-validate.sh) — Physical integrity validator for the rust skill suite.
