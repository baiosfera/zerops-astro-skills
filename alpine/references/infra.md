# Alpine Linux — Infrastructure & Platform Lifecycle Manual on Zerops

This manual specifies the operational platform model, lifecycle commands, comparative matrices with Ubuntu, and bounded execution harnesses for deploying **Alpine Linux** (`base: alpine@3.20` / `os: alpine`) on Zerops.

---

## 1. Zerops Platform Model & Container Architecture

Zerops executes Alpine workloads inside **Incus Linux Containers (LXC)** attached to an isolated, encrypted VXLAN private network.

```
+--------------------------------------------------------------------------+
| Zerops Build Container (Envelope: 1-5 CPU, 8GB RAM fixed, 60m timeout)   |
| - Base: alpine@3.20 (~5MB base image)                                    |
| - prepareCommands: sudo apk add --no-cache ... (Cached in base layer)    |
| - buildCommands: Compilation & static asset bundling                     |
+------------------------------------+-------------------------------------+
                                     |
                                     | deployFiles (THE ONLY BRIDGE)
                                     v
+--------------------------------------------------------------------------+
| Zerops Runtime Container (Incus LXC - Native Dynamic Autoscaling)        |
| - Base: alpine@3.20 (musl libc, ~8-15MB idle RAM)                        |
| - run.prepareCommands: System packages installed before deployFiles arrive|
| - run.initCommands: Initial startup tasks / migrations                   |
| - run.start: Application launch command                                  |
| - deploy.readinessCheck: HTTP 200 health probe                           |
+--------------------------------------------------------------------------+
```

### Automatic Vertical Autoscaling Invariant
In Zerops, runtime containers auto-scale CPU cores and RAM **automatically and dynamically** according to real-time traffic and process load.
* **Best Practice**: Omit manual `verticalAutoscaling` ranges in `import.yaml` for standard workloads; Zerops automatically assigns elastic minimums and expands resources up to hardware boundaries without manual intervention.

---

## 2. Direct Architectural Comparison: Alpine vs Ubuntu on Zerops

| Dimensión Técnica | Alpine Native LXC (`base: alpine@3.20`) | Ubuntu Native LXC (`base: ubuntu@24`) |
|---|---|---|
| **C Standard Library** | **musl libc** (strict POSIX compliance) | **glibc 2.39** (GNU extensions, thread-safe ptmalloc3) |
| **Base Image Size** | **~5 MB** | ~100 MB |
| **Package Manager** | `sudo apk add --no-cache <pkg>` | `sudo apt-get update && sudo apt-get install -y <pkg>` |
| **Cold Boot Duration** | **Ultra-Fast (<1–2 seconds)** | Rápido (~2–4 seconds) |
| **Baseline RAM Overhead** | **Minimum absolute (~8–15 MB RAM)** | Low (~25–40 MB RAM) |
| **Binary Compatibility** | Pure static binaries, musl packages | Universal glibc (CGO Go, PyTorch/NumPy wheels, Deno) |
| **Multi-Thread Allocator** | Global lock contention in heavy C multi-threading | High performance multi-threaded allocator (`ptmalloc3`) |
| **Autoescalado Vertical** | **Elastic Automatic Native (`min < max`)** | **Elastic Automatic Native (`min < max`)** |
| **Primary Use Cases** | 95% of web apps, static sites, pure Go/Rust | Data Science, ML, dynamic CGO, C++ native modules |

---

## 3. Lifecycle Commands & `zerops.yaml` Specification

```yaml
zerops:
  - setup: alpineservice
    build:
      base: alpine@3.20
      prepareCommands:
        - sudo apk add --no-cache build-base ca-certificates curl git
      buildCommands:
        - make build
      deployFiles:
        - dist/
        - package.json
    run:
      base: alpine@3.20
      prepareCommands:
        - sudo apk add --no-cache ca-certificates curl
      initCommands:
        - echo "Initializing Alpine runtime container..."
      start: ./dist/app
      ports:
        - port: 3000
          httpSupport: true
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
| `NODE_ENV` / `ENVIRONMENT` | String | No | `production` | Application execution environment (`production`, `development`) |
| `DATABASE_URL` | String | No | — | Cross-service connection string expanded from Zerops environment |

---

## 5. Storage Mounts & FUSE Permission Safeguards

When mounting shared persistent storage volumes (e.g. NFS / SeaweedFS) to Alpine containers:

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
