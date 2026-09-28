# Bun — Infrastructure & Platform Lifecycle Manual on Zerops

This manual specifies the operational platform model, lifecycle commands, four-way architectural comparisons, and bounded execution harnesses for deploying the **Zerops Managed Bun Runtime** (`type: bun@1.3.9` / `bun@latest`).

---

## 1. Platform Topology & Service Provisioning (`import.yaml`)

Zerops Managed Bun executes in unprivileged **Incus Linux Containers (LXC)** attached to an isolated, encrypted VXLAN private network.

```yaml
# import.yaml - Production Topology for Bun Application Stack
services:
  - hostname: api
    type: bun@1.3.9
    enableSubdomainAccess: true
```

> **Automatic Vertical Autoscaling Invariant**:
> Do not author manual `verticalAutoscaling` min/max blocks. Zerops natively monitors CPU and memory usage and auto-scales vertically on demand with sub-second responsiveness.

---

## 2. Four-Way Architectural Comparison: Managed vs Generic Containers

| Dimensión Técnica | Managed Bun en Alpine (`os: alpine` - Default) | Managed Bun en Ubuntu (`os: ubuntu`) | Generic Ubuntu LXC con Bun (`type: ubuntu@24`) | Generic Alpine LXC con Bun (`type: alpine@3.20`) |
|---|---|---|---|---|
| **Aprovisionamiento** | **1 línea en `import.yaml` (`type: bun@1.3.9`)** | **1 línea en `import.yaml` (`type: bun@1.3.9`)** | Requiere script `curl -fsSL https://bun.sh/install` | Requiere instalar binario musl manualmente |
| **C Standard Library** | **musl libc** | **glibc 2.39** | glibc 2.39 | musl libc |
| **Tamaño de Imagen Base** | **~5 MB** | ~100 MB | ~100 MB | ~5 MB |
| **Overhead de RAM en Reposo** | **~25–40 MB RAM** (25-40% menor que Node) | ~40–60 MB RAM | ~40–60 MB RAM | ~25–40 MB RAM |
| **Rendimiento JS/TS** | **Ultra-Rápido** (JavaScriptCore engine) | **Ultra-Rápido** (JavaScriptCore engine) | Ultra-Rápido | Ultra-Rápido |
| **Módulos Nativos C++ (`.node`)** | No recomendado para C++ addons | **Compatibilidad Total** (`sharp`, `canvas`, `bcrypt`) | Compatibilidad Total | Falla en librerías precompiladas glibc |
| **Ley de Bundling (`bun build`)** | **Standalone Bundle ~150KB** (Pure JS/TS) | **Omitir Bundling** (Deploy full `./` con C++) | Manual | Manual |
| **Caché de Build** | **Nativa con `BUN_INSTALL: ./.bun`** | **Nativa con `BUN_INSTALL: ./.bun`** | Manual en `prepareCommands` | Manual en `prepareCommands` |
| **Mantenimiento Operativo** | **Cero**: Zerops actualiza el runtime | **Cero**: Zerops actualiza el runtime | Alto: Mantenimiento manual de toolchain | Alto: Mantenimiento manual de toolchain |
| **Autoescalado Vertical** | **Elástico Automático Nativo (`min < max`)** | **Elástico Automático Nativo (`min < max`)** | **Elástico Automático Nativo (`min < max`)** | **Elástico Automático Nativo (`min < max`)** |
| **Casos de Uso Ideales** | 95% de apps web (Elysia, Hono, Fastify, Astro) | Procesamiento de imágenes (Sharp), N-API C++ | Requerimientos de SO altamente personalizados | Contenedores genéricos ligeros sin managed features |

---

## 3. Build & Deploy Lifecycle Mechanics (`zerops.yaml`)

```
+--------------------------------------------------------------------------+
| Zerops Build Container (Envelope: 1-5 CPU, 8GB RAM fixed, 60m timeout)   |
| - Base: bun@1.3.9 (os: alpine or os: ubuntu)                             |
| - BUN_INSTALL: ./.bun (Cached across builds)                             |
| - Commands: bun install --frozen-lockfile && bun build ...               |
+------------------------------------+-------------------------------------+
                                     |
                                     | deployFiles: [dist] (Pure TS/JS) or [./] (Native C++)
                                     v
+--------------------------------------------------------------------------+
| Zerops Runtime Container (Incus LXC - Native Dynamic Autoscaling)        |
| - Base: bun@1.3.9 (os: alpine or os: ubuntu)                             |
| - run.initCommands: zsc execOnce ${appVersionId} -- bun dist/migrate.js  |
| - run.start: bun dist/index.js (or bun src/index.ts)                     |
| - deploy.readinessCheck: HTTP 200 at /healthz                            |
+--------------------------------------------------------------------------+
```

### Complete Production `zerops.yaml` Specification (Pure JS/TS)
```yaml
zerops:
  - setup: prod
    build:
      base: bun@1.3.9
      os: alpine
      envVariables:
        BUN_INSTALL: ./.bun
      buildCommands:
        - bun install --frozen-lockfile
        - bun build src/index.ts --outfile dist/index.js --target bun
        - bun build migrate.ts --outfile dist/migrate.js --target bun
      deployFiles:
        - dist
      cache:
        - node_modules
        - .bun/install/cache

    deploy:
      readinessCheck:
        httpGet:
          port: 3000
          path: /healthz

    run:
      base: bun@1.3.9
      os: alpine
      initCommands:
        - zsc execOnce ${appVersionId} --retryUntilSuccessful -- bun dist/migrate.js
      ports:
        - port: 3000
          httpSupport: true
      envVariables:
        NODE_ENV: production
        PORT: "3000"
        DB_HOST: ${db_hostname}
        DB_PORT: ${db_port}
        DB_USER: ${db_user}
        DB_PASS: ${db_password}
        DB_NAME: ${db_dbName}
      start: bun dist/index.js
      healthCheck:
        httpGet:
          port: 3000
          path: /healthz
```

---

## 4. Environment Variables Reference (.env)

| Variable Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `PORT` | Number | Yes | `3000` | HTTP listening port for the application |
| `NODE_ENV` | String | Yes | `production` | Execution environment mode |
| `BUN_INSTALL` | String | Yes (in build) | `./.bun` | Replaces ~/.bun with relative path for persistent build caching |
| `DB_HOST` | String | No | `${db_hostname}` | Internal DNS address of Zerops PostgreSQL service |
| `DB_PORT` | Number | No | `${db_port}` | Port of Zerops PostgreSQL service |
| `DB_USER` | String | No | `${db_user}` | Database user generated by Zerops |
| `DB_PASS` | String | No | `${db_password}` | Database password generated by Zerops |
| `DB_NAME` | String | No | `${db_dbName}` | Database name matching database hostname |

---

## 5. Storage Mounts & FUSE Permission Safeguards

When mounting shared persistent storage volumes (e.g. NFS / SeaweedFS) to Bun containers:

```bash
# Mount Path Convention
/mnt/<storageHostname>/<service>/

# Mandatory FUSE Permission Shield (executed in run.initCommands or prepareCommands)
chmod -R 777 /mnt/<storageHostname>/<service>/
```

---

## 6. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

* **Strict Synchronous Timeouts**: All terminal healthchecks and diagnostics MUST execute with explicit timeouts:
  ```bash
  timeout 10s curl -s -f http://localhost:3000/healthz
  ```
* **Circuit Breaker (2-Attempt Limit)**: On consecutive HTTP 500 or timeout failures, immediately halt execution and trigger human escalation instead of entering infinite loops.
* **Zero Orphaned Tasks Invariant**: Always clean lingering background inspection tasks:
  ```typescript
  await manage_task({ Action: 'kill', TaskId: taskId });
  ```
