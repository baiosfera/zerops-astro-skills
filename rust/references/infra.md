# Rust — Infrastructure & Platform Lifecycle Manual on Zerops

This manual specifies the operational platform model, build caching mechanics, binary deployment strategies, development workflows, and bounded execution harnesses for **Rust** on Zerops.

---

## 1. Platform Architecture & Build Lifecycle

Zerops compiles Rust applications inside dedicated Incus LXC build containers and deploys the resulting compiled binary artifacts to runtime LXC containers.

```
+--------------------------------------------------------------------------+
| Zerops Rust Build & Deployment Lifecycle                                 |
+--------------------------------------------------------------------------+
| 1. Build Phase (base: rust@stable):                                      |
|    - Sets CARGO_HOME: ./.cargo                                           |
|    - Restores cached .cargo/registry & target                            |
|    - Executes: cargo build --release --locked                           |
| 2. Deploy Phase (deployFiles):                                           |
|    - Ships ONLY compiled release binaries (e.g. ./target/release/app)   |
|    - Runtime footprint: ~10-25 MB (Instant startup <50ms)                |
| 3. Runtime Phase (run.initCommands):                                     |
|    - Executes atomic migration: zsc execOnce ${appVersionId} -- migrate  |
|    - Launches application binary with readinessCheck                     |
+--------------------------------------------------------------------------+
```

> **Zero-Guessing Vertical Autoscaling Invariant**:
> Do not author manual `verticalAutoscaling` min/max blocks. Zerops natively monitors CPU and memory usage and auto-scales vertically on demand with sub-second responsiveness.

---

## 2. Four-Way Architectural Comparison

| Dimensión Técnica | Rust Binary en `base: rust@stable` | Rust Static en `base: alpine@3.24` | Rust Binary en `base: ubuntu@24.04` | Rust Dev Workspace (`setup: dev`) |
|---|---|---|---|---|
| **Contenedor Runtime** | Contenedor oficial Rust en Incus LXC | Contenedor Alpine ultra-liviano (~5MB base) | Contenedor Ubuntu completo (~30MB base) | Contenedor Ubuntu con `cargo` y `rustc` interactivo |
| **Enlace Dinámico** | Toolchain Rust completo en runtime | `musl libc` (binario estático independiente) | `glibc` (para librerías C complejas) | Toolchain Rust completo para compilación local |
| **Tamaño de Imagen/Disco**| Binario (~15MB) + Runtime Rust | **Binario (~15MB) + 5MB Alpine** | Binario (~15MB) + 30MB Ubuntu | Código fuente completo + target (~500MB) |
| **Tiempo de Arranque** | **<50ms** | **<30ms** | <50ms | N/A (arranque interactivo vía SSH) |
| **Uso Recomendado** | Microservicios Axum estándar en Zerops | Microservicios de huella ultra-mínima | Apps con C-bindings dinámicos (`libpq`, etc.) | Desarrollo interactivo con `cargo run` vía SSH |

---

## 3. Cargo Caching Mechanics & OpenSSL Prevention

### A. High-Speed Incremental Build Caching
By default, Cargo stores crate sources in `$HOME/.cargo` and build artifacts in `./target`. Because `$HOME` is ephemeral across builds, always configure:
```yaml
build:
  base: rust@stable
  envVariables:
    CARGO_HOME: ./.cargo
  cache:
    - .cargo/registry
    - target
```

### B. OpenSSL vs Rustls Invariant
Zerops build containers do NOT include `pkg-config` or `libssl-dev` by default.
* **Best Practice**: Use `rustls-tls` crate features (e.g. `reqwest = { version = "0.12", features = ["rustls-tls"] }`).
* **Legacy OpenSSL Fallback**: If external C crates require native OpenSSL, install build dependencies in `prepareCommands`:
```yaml
build:
  base: rust@stable
  prepareCommands:
    - sudo apt-get update && sudo apt-get install -y pkg-config libssl-dev
```

---

## 4. Production Manifests (`import.yaml` & `zerops.yaml`)

### Production `import.yaml` Manifest
```yaml
project:
  name: rust-app

services:
  # Managed PostgreSQL Database
  - hostname: db
    type: postgresql:single@18
    profile: staging
    priority: 10

  # Rust Web Application Service
  - hostname: api
    type: rust@stable
    enableSubdomainAccess: true
```

### Dual-Environment `zerops.yaml` Configuration (Prod + Dev)
```yaml
zerops:
  # ==========================================
  # PRODUCTION SETUP: COMPILED MICRO-BINARY
  # ==========================================
  - setup: prod
    build:
      base: rust@stable
      envVariables:
        CARGO_HOME: ./.cargo
      buildCommands:
        - cargo build --release --locked
      deployFiles:
        - ./target/release/rust-app
        - ./target/release/migrate
      cache:
        - .cargo/registry
        - target

    deploy:
      readinessCheck:
        httpGet:
          port: 8080
          path: /healthz

    run:
      base: rust@stable
      initCommands:
        - zsc execOnce ${appVersionId} -- ./target/release/migrate
      ports:
        - port: 8080
          httpSupport: true
      envVariables:
        PORT: 8080
        DB_HOST: ${db_hostname}
        DB_PORT: ${db_port}
        DB_USER: ${db_user}
        DB_PASS: ${db_password}
        DB_NAME: ${db_dbName}
      start: ./target/release/rust-app

  # ==========================================
  # DEVELOPMENT SETUP: INTERACTIVE SSH WORKSPACE
  # ==========================================
  - setup: dev
    build:
      base: rust@stable
      os: ubuntu
      envVariables:
        CARGO_HOME: ./.cargo
      buildCommands:
        - cargo fetch
      deployFiles:
        - ./
      cache:
        - .cargo/registry

    run:
      base: rust@stable
      os: ubuntu
      initCommands:
        - zsc execOnce ${appVersionId} -- cargo run --bin migrate
      ports:
        - port: 8080
          httpSupport: true
      envVariables:
        PORT: 8080
        CARGO_HOME: /var/www/.cargo
        DB_HOST: ${db_hostname}
        DB_PORT: ${db_port}
        DB_USER: ${db_user}
        DB_PASS: ${db_password}
        DB_NAME: ${db_dbName}
      start: zsc noop --silent
```

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

* **Strict Synchronous Timeouts**: All terminal commands over SSH MUST execute with explicit timeouts:
  ```bash
  ssh api "timeout 10s cargo check"
  ```
* **Circuit Breaker (2-Attempt Limit)**: On consecutive build or deployment failures, halt execution and trigger human escalation.
* **Zero Orphaned Tasks Invariant**: Always terminate lingering background dev servers:
  ```typescript
  await manage_task({ Action: 'kill', TaskId: taskId });
  ```
