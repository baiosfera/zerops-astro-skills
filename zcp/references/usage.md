# Zerops Operational Reference Manual: 22 MCP Tools, Manifest Schemas & Ecosystem Orchestrator (v6.3)

`zcp` is the master platform engineering, workload provisioning, and infrastructure lifecycle suite for Zerops. Operating natively on unprivileged **Incus LXC containers** with sub-millisecond private network mesh (`<0.3ms P99`), it governs the entire sovereign stack: **Astro 5 SSR**, **Directus 11+ BaaS**, **FastAPI Microservices**, **PostgreSQL 18**, **Valkey 7.2**, **NATS 2.12**, **Shared Storage**, **Evolution WhatsApp Gateways**, and **Cloudflare Edge Ingress**.

---

## 1. 4D Comparative Architectural Matrix

| Platform Dimension | Zerops Incus LXC (ZCP Target) | Kubernetes (K8s / EKS) | Closed PaaS (Render, Railway) | Serverless (AWS Lambda / Vercel) |
|---|---|---|---|---|
| **Elastic Vertical Autoscaling**| **Real-time dynamic (CPU & RAM)** | Requires Pod restarts (VPA) | Fixed tier upgrades | Per-request scale (Cold starts) |
| **Private Mesh Latency** | **Sub-millisecond native (<0.3ms P99)** | Complex CNI overlays (Calico) | HTTP proxy routing | Requires VPC + NAT Gateways |
| **Plataform Base Memory** | **0 MB Extra (Shared Linux kernel)** | ~1.5 GB RAM control plane | Docker daemon overhead | MicroVM firecracker overhead |
| **Managed Core Services** | **Postgres 18, Valkey 7.2, NATS 2.12** | Complex custom operators | Expensive proprietary addons | Cold-start serverless databases |
| **Control Plane Surface** | **22 Project-Scoped MCP Tools** | `kubectl` / Helm manifests | Proprietary web UI | Proprietary CLI / Dashboard |

---

## 2. Comprehensive Catalogue of the 22 Zerops MCP Tools (`zerops_*`)

The Zerops platform is operated exclusively through its native MCP tools:

### A. Inspection, Knowledge & Discovery
- **`zerops_discover`**:
  - *Parameters*: `service` (optional string to filter by hostname; omit for entire project), `includeEnvs` (boolean/string, lists variable keys without revealing values), `includeEnvValues` (boolean/string, reveals secret values; use strictly for deep debugging).
  - *Usage*: Mandatory Phase 0 floor sensor to discover services, runtimes, statuses (`ACTIVE`, `STOPPED`), and subdomains.
- **`zerops_knowledge`**:
  - *Parameters (Mutually Exclusive Modes)*:
    - Mode 1: `query` (string) + `limit` (int) $\implies$ Free-text search in Zerops docs.
    - Mode 2: `runtime` (string, e.g. `bun@1.3.9`) and/or `services` (array, e.g. `["postgresql@18", "valkey@7.2"]`) $\implies$ Technical stack briefing.
    - Mode 3: `scope="infrastructure"` $\implies$ YAML schemas and environment variable reference manual.
    - Mode 4: `recipe="slug"` $\implies$ Official recipe documentation (e.g. `bun-hello-world`).
    - Mode 5: `uri="zerops://..."` $\implies$ Direct fetch by URI (e.g. `zerops://guides/scaling`).
    - *Helper*: `mode="dev|standard|simple|stage"` $\implies$ Workflow mode override.
- **`zerops_workspace_manifest`**:
  - *Parameters*: `action="read|update"`, `updatePayload` (`{codebases, contracts, featuresImplemented, notes}`).
  - *Usage*: JSON context store for subagents without recursively scanning file trees.

### B. State Management, Scaling & Environment Variables
- **`zerops_workflow`**:
  - *Workflows*: `bootstrap` (provisioning/adoption), `develop` (service code editing), `launch-production` (promoting to a separate HA production project), `export` (git packaging).
  - *Actions*: `start`, `complete`, `skip`, `status`, `close`, `reset`, `iterate`, `resume`, `close-mode`, `git-push-setup`, `build-integration`, `set-default-setup`, `record-deploy`, `release`, `prod-ops`.
- **`zerops_env`**:
  - *Parameters*: `action="get|set|delete|generate-dotenv"`, `serviceHostname`, `project: true`, `variables: string[]`, `preview: true`, `force: true`, `setup: string`.
  - *Rule*: `set` expands preprocessors `<@...>` and restarts services unless `skipRestart=true`.
- **`zerops_scale`**:
  - *Parameters*: `serviceHostname`, `cpuMode` (`SHARED|DEDICATED`), `minCpu`, `maxCpu`, `startCpu`, `minRam`, `maxRam`, `minDisk`, `maxDisk`, `minContainers`, `maxContainers`, `minFreeRamGB`, `minFreeRamPercent`, `minFreeCpuCores`, `minFreeCpuPercent`.
- **`zerops_subdomain`**:
  - *Parameters*: `serviceHostname`, `action="enable|disable"`. Enables or disables `*.zerops.app` public access.
- **`zerops_manage`**:
  - *Parameters*: `action="start|stop|restart|reload|connect-storage|disconnect-storage"`, `serviceHostname`, `storageHostname`.
  - *Rule*: `restart` reloads the boot environment; `reload` performs a warm process reload (~4s).

### C. Deployment, Processes & Development Servers
- **`zerops_deploy`**:
  - *Parameters*: `targetService`, `sourceService` (for cross-deploy), `setup`, `strategy="git-push"`, `branch`, `remoteUrl`, `breakGlass`.
  - *Critical Rule*: Self-deploying services (`sourceService == targetService`) MUST declare `deployFiles: [.]` in `zerops.yaml`.
- **`zerops_deploy_batch`**:
  - *Parameters*: `targets: [{targetService, sourceService, setup, workingDir}]`. Concurrent deployments without blocking stdio.
- **`zerops_dev_server`**:
  - *Parameters*: `hostname`, `action="start|stop|status|logs|restart"`, `command`, `port`, `healthPath` (default `/`), `waitSeconds` (default 15), `noHttpProbe: true` (for background workers using PID liveness `kill -0`), `logFile` (default `/tmp/zcp-dev-server.log`), `logLines`.
  - *Rule*: Mandatory supervisor for persistent dev servers/watchers. Never use `ssh "cmd &"`.
- **`zerops_verify`**:
  - *Parameters*: `serviceHostname` (omit for entire project). Physical health sensor returning `pass`, `fail`, `skip`, or `info`.
- **`zerops_logs`**:
  - *Parameters*: `serviceHostname`, `severity="WARNING|ERROR"`, `since` (`30s`, `5m`, `1h`, `7d`), `search`, `limit`.
- **`zerops_events`**:
  - *Parameters*: `serviceHostname`, `limit`. Inspects structured build and deployment failures (`stack.build`, `appVersion`).
- **`zerops_mount`**:
  - *Parameters*: `action="mount|unmount|status"`. Mounts `/var/www/{hostname}` via SSHFS locally.
- **`zerops_export`** & **`zerops_import`**:
  - *Parameters*: `content`/`filePath`, `override: true`, `confirmDestructive`.
- **`zerops_browser`**:
  - *Parameters*: `url`, `commands: string[][]`, `timeoutSeconds: 120`. Headless Chromium browser automation without CDP lockups.
- **`zerops_preprocess`**:
  - *Parameters*: `input`/`inputs`, `order`. Evaluates preprocessor expressions like `<@generateRandomString(32)|hex>`.
- **`zerops_process`**:
  - *Parameters*: `action="wait|status|cancel"`, `service="hostname"`, `processId`/`processIds`.
- **`zerops_record_fact`**:
  - *Parameters*: `type`, `title`, `mechanism`, `failureMode`, `fixApplied`, `evidence`, `codebase`, `substep`.
- **`zerops_delete`**:
  - *Parameters*: `serviceHostname`. Deletes a service after explicit human confirmation.

---

## 3. Operational Demarcation: MCP Tools vs SSH / Bash

| Operation | Mandatory Exclusive Path | Strict Prohibition |
|---|---|---|
| Mutate infra, import YAML, scale | `zerops_import`, `zerops_scale`, `zerops_workflow` | Modifying `/etc/` or running unmanaged CLIs |
| Get or set environment variables | `zerops_env action="get|set"` | Appending `VAR=val` into `.env` on host |
| Launch dev servers / watchers (`npm run dev`) | `zerops_dev_server action="start"` | `ssh hostname "npm run dev &"` (dies with channel) |
| Physical health attestation | `zerops_verify`, `zerops_logs` | Assuming health based on stdout prose |
| Ephemeral build/test execution | `ssh {hostname} "cd /var/www && <cmd>"` | Running runtime tests in local ZCP container |
| Install ephemeral OS packages | `ssh {hostname} "sudo apk add <pkg>"` | Modifying `/opt/zerops/**` platform binaries |

---

## 4. Canonical `import.yaml` Manifest Specification

```yaml
#zeropsPreprocessor=on
project:
  name: gentle-ecosystem
  corePackage: LIGHT # LIGHT for dev/staging, SERIOUS for HA production

services:
  # 1. Astro 5 Frontend (Bun 1.3 - Frugal Resilient Recipe)
  - hostname: astro
    type: bun@1.3.9
    priority: 5
    startWithoutCode: true
    enableSubdomainAccess: true
    minContainers: 1
    maxContainers: 2
    verticalAutoscaling:
      cpuMode: SHARED
      minFreeRamGB: 0.25
      minFreeRamPercent: 10

  # 2. Directus 11+ Headless CMS (Node 24 / Ubuntu - Frugal Resilient Recipe)
  - hostname: directus
    type: nodejs@24
    os: ubuntu
    priority: 8
    startWithoutCode: true
    enableSubdomainAccess: true
    minContainers: 1
    maxContainers: 2
    verticalAutoscaling:
      cpuMode: SHARED
      minFreeRamGB: 0.25
      minFreeRamPercent: 10

  # 3. FastAPI Python Microservice (Frugal Resilient Recipe)
  - hostname: fastapi
    type: python@3.12
    priority: 7
    startWithoutCode: true
    enableSubdomainAccess: true
    minContainers: 1
    maxContainers: 2
    verticalAutoscaling:
      cpuMode: SHARED
      minFreeRamGB: 0.25
      minFreeRamPercent: 10

  # 4. Managed PostgreSQL 18 (OLTP Production)
  - hostname: db
    type: postgresql:single@18
    profile: oltp-production
    priority: 10

  # 5. Managed Valkey 7.2 Cache
  - hostname: cache
    type: valkey:single@7.2
    profile: hobby
    priority: 10

  # 6. Managed NATS 2.12
  - hostname: nats
    type: nats:single@2.12
    priority: 10

  # 7. Local Storage (Persistent Single-Kernel POSIX Volume)
  - hostname: storage
    type: local-storage:single@1
    priority: 10
    verticalAutoscaling:
      minDisk: 5
      maxDisk: 100
```

---

## 5. Canonical `zerops.yaml` Lifecycle Recipes

```yaml
zerops:
  # Setup for Development (SSH iterative workspace)
  - setup: dev
    build:
      base: bun@1.3.9
      os: ubuntu
      prepareCommands:
        - sudo apt-get update && sudo apt-get install -y ffmpeg
      buildCommands:
        - bun install
      deployFiles:
        - . # Self-deploying: MUST be [.] to preserve source files
      cache:
        - node_modules
        - .bun/install/cache
    run:
      base: bun@1.3.9
      os: ubuntu
      start: zsc noop --silent # Keepalive: zerops_dev_server starts actual process
      ports:
        - port: 3000
          httpSupport: true
      envVariables:
        PORT: 3000
        DATABASE_URL: "${db_connectionString}"
        REDIS_URL: "${cache_connectionString}"
        NATS_URL: "${nats_connectionString}"

  # Setup for Production (Zero-Downtime Rolling Release)
  - setup: prod
    build:
      base: bun@1.3.9
      os: ubuntu
      envVariables:
        BUN_INSTALL: ./.bun
      buildCommands:
        - bun install --frozen-lockfile
        - bun run build
      deployFiles:
        - dist
        - package.json
        - node_modules
    deploy:
      readinessCheck:
        httpGet:
          port: 3000
          path: /
    run:
      base: bun@1.3.9
      os: ubuntu
      ports:
        - port: 3000
          httpSupport: true
      start: bun run ./dist/server/entry.mjs
```

---

## 6. 5 Production Patterns in Zerops

### Pattern 1: Automated Multi-Service Topology Provisioning with `import.yaml`
Import multi-service topologies in a single API call using `#zeropsPreprocessor=on` to automatically generate database connection secrets.

### Pattern 2: Persistent Dev Server Supervision with `zerops_dev_server`
Supervises hot-reloading dev servers (`bun run dev`, `granian`, `uvicorn`) in the background with automatic crash restarts and PID tracking.

### Pattern 3: Zero-Downtime Rolling Release via GitHub Actions (`zeropsio/actions@v1.0.2`)
Delivers production releases on `main` branch push using GitHub Actions with `ZEROPS_TOKEN` secret.

### Pattern 4: Production Promotion with `workflow="launch-production"`
Promotes single-container dev/stage environments to multi-container High Availability (`:ha`) production projects seamlessly.

### Pattern 5: Deterministic Health Attestation with `zerops_verify` and `zerops_logs`
Validates container status, port responsiveness, and log streams before closing deployment tasks.

---

## 7. Anti-Patterns & Common Gotchas

1. **Forced Min/Max Boilerplate & Artificial Ceilings**: Do NOT force arbitrary low ceilings (`maxRam: 2.0`, `maxCpu: 2`) on native LXC runtimes in `import.yaml`. Zerops bills strictly on actual sub-second utilization; artificial ceilings do not reduce costs and cause catastrophic `OOMKilled` crashes on traffic surges. Use the canonical Frugal Resilient recipe (`minContainers: 1`, `maxContainers: 2`, `cpuMode: SHARED`, `minFreeRamGB: 0.25`, `minFreeRamPercent: 10`) and omit `min/max` boundaries to let Zerops autoscale organically across 0.125-48 GB RAM and 1-8 vCPUs.
2. **Legacy Mount Directives**: Persistent storage volumes (`local-storage:single@1`) must be declared under `services:` in `import.yaml` and mounted in `zerops.yaml` via `run.volume`. Never declare legacy `mount:` in `import.yaml` or obsolete `run.mount` in `zerops.yaml`.
3. **Backgrounding Dev Servers with `ssh "cmd &"`**: SSH background commands terminate when the channel closes. Always use `zerops_dev_server`.
4. **Self-Shadowing Environment Variables**: Never define `VAR: ${VAR}`; always use distinctive source variables like `DB_HOST: ${db_hostname}`.

---

## 8. Root-Cause Architecture Investigation: The 2-Node Incident & Local Storage Semantics in ZCP (Physical Post-Mortem 2026-10-23)

### A. The Incident & The "Disappearing / Reappearing" Data Paradox
During operational refactoring on 2026-10-22, the control-plane container `zcp` was scaled horizontally to 2 containers (`minContainers: 2, maxContainers: 2`). Immediately upon connection, users observed an empty `/var/www` directory tree, missing active repositories, and broken tool symlinks. When the service was scaled back down to a single container (`minContainers: 1, maxContainers: 1`), the entire directory tree, active sessions, and repositories instantly reappeared with zero data loss.

### B. Primary-Source Chronology (`zerops_events` for `zcp`)
Audit of the platform event stream confirms the exact state transitions:
1. `2026-10-22 14:44:50`: User scales `zcp` to horizontal mode (`minContainers: 2, maxContainers: 2`).
2. `2026-10-22 14:47:19`: Service container restart triggered.
3. `2026-10-22 22:15:27`: Container cold start completed.
4. `2026-10-22 22:19 & 22:21`: `updateUserData` operations.
5. `2026-10-22 22:34 to 23:36`: Repeated scaling adjustments (`zcp-Glamur` automation vs user manual scale).
6. `2026-10-23 00:05 to 00:18`: Final scaling convergence locking ZCP back to single-node mode (`minContainers: 1, maxContainers: 1`).

### C. Physical Mechanism: L7 Ingress Balancing & Ephemeral Replica Split-Brain
The phenomenon was not data deletion or filesystem corruption, but an **L7 ingress split-brain**:
1. **ZCP is Stateful**: ZCP functions as a stateful agentic workstation and control plane hosting interactive TTYs, SSH keys, local git working trees, and running background daemon processes. It is NOT a stateless web tier.
2. **Horizontal Scale Replication in Zerops**: When `minContainers` is increased from 1 to 2, Zerops Incus provisions a second, fresh LXC container (`container-2`) instantiated from the base image or build artifact. It does NOT clone or share the live local rootfs of `container-1`.
3. **Ingress Routing Alternation**: Incoming SSH and terminal sessions are balanced across active containers. Sessions routed to `container-2` landed on a pristine, unpopulated `/var/www` filesystem, creating the appearance of catastrophic data loss.
4. **Resolution via Scale-Down**: Scaling back to `minContainers: 1, maxContainers: 1` caused Zerops to terminate the ephemeral replica (`container-2`) and restore 100% of traffic to the persistent `container-1`, immediately revealing all files and state intact.

### D. Storage Engine Demarcation: Rootfs vs Local Storage vs SSoT
* **Container Rootfs (`/var/www`)**: Ephemeral to the container instance. Persists across restarts of the same container, but is NOT shared across horizontal replicas.
* **Local Storage (`local-storage:single@1`)**: Single-kernel POSIX block storage mounted directly via Incus LXC. Provides single-node POSIX coherence (`flock`, `mmap`, SQLite WAL), but cannot serve as a distributed multi-node filesystem across distinct host nodes.
* **Google Drive SSoT (`/var/www/baiosfera`)**: Persistent remote object mount via rclone FUSE. Acts as the universal source of truth across container rebuilds and cold starts.

### E. Architectural Invariant: Enforced Single-Node Lock
* **Mandatory Policy**: `zcp` must remain strictly configured to **1 container** (`minContainers: 1, maxContainers: 1`).
* **Deterministic Guard**: Guardrail Rule 39 in `tool-guard.py` intercepts and denies any attempt to mutate `minContainers > 1` or `maxContainers > 1` on `zcp`, preventing split-brain incidents permanently.
* **Scaling Strategy**: All ZCP resource growth must be strictly **vertical** (`cpuMode: SHARED`, `maxRam: 6-8 GB`).

