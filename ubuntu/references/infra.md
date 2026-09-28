# Ubuntu 24.04 LTS — Infrastructure & Deployment Manual

This manual specifies the operational platform model, lifecycle commands, multi-dimensional architectural comparisons with Alpine, and bounded execution harnesses for deploying **Ubuntu 24.04 LTS** on Zerops.

---

## 1. Zerops Platform Model & Container Architecture

Zerops executes workloads inside **Incus Linux Containers (LXC)** connected via isolated, encrypted VXLAN private networks.

```
+---------------------------------------------------------------+
| Zerops Build Container (Envelope: 1-5 CPU, 8GB RAM, 60m limit)|
| - Base: ubuntu@24 (glibc 2.39)                                |
| - prepareCommands: Package installation (Cached)              |
| - buildCommands: Compilation & asset bundling                 |
+-------------------------------+-------------------------------+
                                |
                                | deployFiles (THE ONLY BRIDGE)
                                v
+---------------------------------------------------------------+
| Zerops Runtime Container (Incus LXC - Native Autoscaling)     |
| - Base: ubuntu@24                                             |
| - run.prepareCommands: System setup before deploy files arrive|
| - Deploy files unpack at /var/www                             |
| - run.initCommands: Migrations / runtime setup                |
| - run.start: Service process execution                        |
+---------------------------------------------------------------+
```

### Automatic Vertical Autoscaling
In Zerops, runtime containers auto-scale CPU cores and RAM **automatically and dynamically** according to real-time traffic and process load.
* **Best Practice**: Omit manual `verticalAutoscaling` ranges in `import.yaml` for standard workloads; Zerops automatically assigns elastic minimums and expands resources up to hardware boundaries without manual intervention.

---

## 2. Direct Architectural Comparison: Ubuntu vs Alpine on Zerops

| Dimensión Técnica | Ubuntu Native LXC (`base: ubuntu@24`) | Alpine Native LXC (`base: alpine@3.20`) |
|---|---|---|
| **C Standard Library** | **glibc 2.39** (GNU extensions, thread-safe ptmalloc3) | **musl libc** (strict POSIX compliance) |
| **Base Image Size** | ~100 MB | **~5 MB** |
| **Package Manager** | `sudo apt-get update && sudo apt-get install -y <pkg>` | `sudo apk add --no-cache <pkg>` |
| **Cold Boot Duration** | Rápido (~2–4 seconds) | **Ultra-Fast (<1–2 seconds)** |
| **Baseline RAM Overhead** | Low (~25–40 MB RAM) | **Minimum absolute (~8–15 MB RAM)** |
| **Binary Compatibility** | Universal glibc (CGO Go, PyTorch/NumPy wheels, Deno) | Pure static binaries, musl packages |
| **Multi-Thread Allocator** | High performance multi-threaded allocator (`ptmalloc3`) | Global lock contention in heavy C multi-threading |
| **Autoescalado Vertical** | **Elastic Automatic Native (`min < max`)** | **Elastic Automatic Native (`min < max`)** |
| **Primary Use Cases** | Data Science, ML, dynamic CGO, C++ native modules | 95% of web apps, static sites, pure Go/Rust |

---

## 3. Lifecycle Commands & `zerops.yaml` Specification

```yaml
zerops:
  - setup: ubuntuservice
    build:
      base: ubuntu@24
      prepareCommands:
        - sudo DEBIAN_FRONTEND=noninteractive apt-get update -y
        - sudo DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends build-essential curl ca-certificates libssl-dev
        - sudo rm -rf /var/lib/apt/lists/*
      buildCommands:
        - make build
      deployFiles:
        - dist/
        - package.json
    run:
      base: ubuntu@24
      prepareCommands:
        - sudo DEBIAN_FRONTEND=noninteractive apt-get update -y && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates curl && sudo rm -rf /var/lib/apt/lists/*
      initCommands:
        - echo "Initializing Ubuntu 24 runtime container..."
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

## 4. Environment Variables Dictionary (.env)

| Variable Name | Type | Required | Default | Description |
|---|---|---|---|---|
| `PORT` | Number | Yes | `3000` | HTTP listening port for the application |
| `NODE_ENV` / `ENVIRONMENT` | String | No | `production` | Application execution environment (`production`, `development`) |
| `DEBIAN_FRONTEND` | String | No | `noninteractive` | Prevents apt-get prompts from hanging build commands |
| `DATABASE_URL` | String | No | — | Cross-service connection string expanded from Zerops environment |

---

## 5. Storage Mounts & FUSE Permission Safeguards

When mounting shared persistent storage volumes (e.g. NFS / SeaweedFS) to Ubuntu containers:

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
