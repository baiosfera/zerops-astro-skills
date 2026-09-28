# Node.js — Infrastructure & Platform Lifecycle Manual on Zerops

This manual specifies the operational platform model, lifecycle commands, four-way architectural comparisons, and bounded execution harnesses for deploying the **Zerops Managed Node.js Runtime** (`type: nodejs@22` / `nodejs@24`).

---

## 1. Platform Topology & Service Provisioning (`import.yaml`)

Zerops Managed Node.js runs in unprivileged **Incus Linux Containers (LXC)** attached to an isolated, encrypted VXLAN private network.

```yaml
# import.yaml - Production Topology for Node.js
services:
  - hostname: api
    type: nodejs@22 # or nodejs@24
    enableSubdomainAccess: true
```

> **Automatic Vertical Autoscaling Invariant**:
> Do not author manual `verticalAutoscaling` min/max blocks. Zerops natively monitors CPU and memory usage and auto-scales vertically on demand with sub-second responsiveness.

---

## 2. Four-Way Architectural Comparison: Managed vs Generic Containers

| Dimensión Técnica | Managed Node.js en Alpine (`os: alpine` - Default) | Managed Node.js en Ubuntu (`os: ubuntu`) | Generic Ubuntu LXC con Node.js (`type: ubuntu@24`) | Generic Alpine LXC con Node.js (`type: alpine@3.20`) |
|---|---|---|---|---|
| **Aprovisionamiento** | **1 línea en `import.yaml` (`type: nodejs@22`)** | **1 línea en `import.yaml` (`type: nodejs@22`)** | Requiere instalar Node vía `apt-get` o NodeSource | Requiere instalar Node vía `apk add nodejs npm` |
| **C Standard Library** | **musl libc** | **glibc 2.39** | glibc 2.39 | musl libc |
| **Tamaño de Imagen Base** | **~5 MB** | ~100 MB | ~100 MB | ~5 MB |
| **Overhead de RAM en Reposo** | **~35–50 MB RAM** | ~50–70 MB RAM | ~50–70 MB RAM | ~35–50 MB RAM |
| **Rendimiento V8 (Pure JS/TS)** | **Idéntico** (V8 gestiona su propio heap) | **Idéntico** (V8 gestiona su propio heap) | Idéntico | Idéntico |
| **Módulos Nativos C++ (`.node`)** | No recomendado (falla o compila lento en musl) | **Compatibilidad Total** (`sharp`, `canvas`, `bcrypt`) | Compatibilidad Total | Falla en librerías precompiladas glibc |
| **Gestión de Caché de Build** | **Nativa con `npm_config_cache: .npm-cache`** | **Nativa con `npm_config_cache: .npm-cache`** | Manual en `prepareCommands` | Manual en `prepareCommands` |
| **Mantenimiento Operativo** | **Cero**: Zerops actualiza el runtime | **Cero**: Zerops actualiza el runtime | Alto: Mantenimiento manual de toolchain | Alto: Mantenimiento manual de toolchain |
| **Autoescalado Vertical** | **Elástico Automático Nativo (`min < max`)** | **Elástico Automático Nativo (`min < max`)** | **Elástico Automático Nativo (`min < max`)** | **Elástico Automático Nativo (`min < max`)** |
| **Casos de Uso Ideales** | 95% de apps web (Fastify, Express, Nest, Astro) | Procesamiento de imágenes (Sharp), Crypto C++ | Requerimientos de SO altamente personalizados | Contenedores genéricos ligeros sin managed features |

---

## 3. Build & Deploy Lifecycle Mechanics (`zerops.yaml`)

```
+--------------------------------------------------------------------------+
| Zerops Build Container (Envelope: 1-5 CPU, 8GB RAM fixed, 60m timeout)   |
| - Base: nodejs@22 (os: alpine or os: ubuntu)                             |
| - npm_config_cache: .npm-cache (Cached across builds)                    |
| - Commands: npm ci && npm run build && npm prune --omit=dev              |
+------------------------------------+-------------------------------------+
                                     |
                                     | deployFiles: [dist/, node_modules/, package.json]
                                     v
+--------------------------------------------------------------------------+
| Zerops Runtime Container (Incus LXC - Native Dynamic Autoscaling)        |
| - Base: nodejs@22 (os: alpine or os: ubuntu)                             |
| - run.initCommands: zsc execOnce ${appVersionId} -- node dist/migrate.js |
| - run.start: node dist/index.js                                          |
| - deploy.readinessCheck: HTTP 200 at /healthz                            |
+--------------------------------------------------------------------------+
```

### Complete Production `zerops.yaml` Specification
```yaml
zerops:
  - setup: prod
    build:
      base: nodejs@22
      os: alpine
      envVariables:
        npm_config_cache: .npm-cache
      buildCommands:
        - npm ci
        - npm run build
        - npm prune --omit=dev
      deployFiles:
        - ./dist
        - ./node_modules
        - ./package.json
      cache:
        - node_modules
        - .npm-cache

    deploy:
      readinessCheck:
        httpGet:
          port: 3000
          path: /healthz

    run:
      base: nodejs@22
      os: alpine
      initCommands:
        - zsc execOnce ${appVersionId} --retryUntilSuccessful -- node dist/migrate.js
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
      start: node dist/index.js
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
| `npm_config_cache` | String | Yes (in build) | `.npm-cache` | Replaces ~/.npm with relative path for persistent build caching |
| `DB_HOST` | String | No | `${db_hostname}` | Internal DNS address of Zerops PostgreSQL service |
| `DB_PORT` | Number | No | `${db_port}` | Port of Zerops PostgreSQL service |
| `DB_USER` | String | No | `${db_user}` | Database user generated by Zerops |
| `DB_PASS` | String | No | `${db_password}` | Database password generated by Zerops |
| `DB_NAME` | String | No | `${db_dbName}` | Database name matching database hostname |

---

## 5. Storage Mounts & FUSE Permission Safeguards

When mounting shared persistent storage volumes (e.g. NFS / SeaweedFS) to Node.js containers:

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
