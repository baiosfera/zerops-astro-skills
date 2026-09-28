# Astro 5 Infrastructure, Secret Isolation & Zerops Deployment Manual (v2.0)

This manual provides production-grade infrastructure blueprints, multi-service `import.yaml` provisioning recipes (including **Astro 5**, **Directus 11+**, **Evolution Go**, **AI Worker**, **PostgreSQL 18**, **NATS**, and **Valkey**), `zerops.yaml` pipeline lifecycles on Bun 1.3.9 / Node.js 24, secret isolation contracts, and the Fractal CoHaLo operational harness for Astro running in Zerops.

---

## 1. Multi-Service Zerops Ecosystem Topology

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Enterprise Project Topology                                                                     │
│                                                                                                        │
│   ┌──────────────────────────────┐              ┌──────────────────────────────────────────────────┐   │
│   │ Astro 5 Frontend (astro)     │              │ Directus 11+ Unified BaaS (directus)             │   │
│   │ (bun@1.3.9 / nodejs@24)      │─────────────▶│ (nodejs@24 / os: ubuntu)                         │   │
│   │ Port 3000 (HTTP Subdomain)   │              │ Port 8055 (HTTP Subdomain)                       │   │
│   └──────────────┬───────────────┘              └────────────────────────┬─────────────────────────┘   │
│                  │                                                       │                             │
│                  │ NATS RPC (<0.3ms P99)                                 │ Mutation events             │
│                  ▼                                                       ▼                             │
│   ┌──────────────────────────────┐              ┌──────────────────────────────────────────────────┐   │
│   │ NATS JetStream (nats)        │◀────────────▶│ Evolution Go WhatsApp Gateway (evolutiongo)      │   │
│   │ (nats@2.10)                  │              │ (go@1.22 / os: alpine)                           │   │
│   │ Port 4222 (Internal DNS)     │              │ Port 8080 (Internal DNS)                         │   │
│   └──────────────┬───────────────┘              └────────────────────────┬─────────────────────────┘   │
│                  │                                                       │                             │
│                  │ Consume Events                                        ▼                             │
│                  ▼                              ┌──────────────────────────────────────────────────┐   │
│   ┌──────────────────────────────┐              │ Persistent Shared Storage (baiostorage)          │   │
│   │ AI / LLM Worker (aiworker)   │              │ /mnt/baiostorage/directus                        │   │
│   │ (nodejs@24 / python@3.12)    │              └──────────────────────────────────────────────────┘   │
│   └──────────────┬───────────────┘                                       │                             │
│                  │                                                       │                             │
│                  ┌───────────────────────────────────────────────────────┴─────────┐                   │
│                  ▼                                                                 ▼                   │
│   ┌──────────────────────────────────────────┐  ┌──────────────────────────────────────────────────┐   │
│   │ Valkey In-Memory Cache (cache)           │  │ Managed PostgreSQL 18 Cluster (db)               │   │
│   │ (valkey@7.2:single / HA)                 │  │ (postgresql@18:single / HA)                      │   │
│   │ Port 6379 (Internal Zerops DNS)          │  │ Port 5432 (Internal Zerops DNS)                  │   │
│   └──────────────────────────────────────────┘  └──────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Service Provisioning Blueprint (`import.yaml`)

```yaml
services:
  # 1. Astro 5 SSR Frontend Webapp (Bun 1.3.9 Runtime)
  - hostname: astro
    type: bun@1.3.9
    enableSubdomainAccess: true
    minContainers: 1
    maxContainers: 3
    verticalAutoscaling:
      cpuMode: SHARED
      minCpu: 1
      maxCpu: 4
      minRam: 0.25
      maxRam: 2.0
      minDisk: 1.0
      maxDisk: 10.0

  # 2. Directus 11+ Unified BaaS Engine
  - hostname: directus
    type: nodejs@24
    enableSubdomainAccess: true

  # 3. Evolution Go WhatsApp Gateway
  - hostname: evolutiongo
    type: go@1.22
    enableSubdomainAccess: true

  # 4. NATS JetStream Message Broker
  - hostname: nats
    type: nats@2.10

  # 5. Managed Valkey for Sessions & Rate Limiting
  - hostname: cache
    type: valkey@7.2:single
    mode: NON_HA

  # 6. Managed PostgreSQL 18 Cluster
  - hostname: db
    type: postgresql@18:single
    mode: NON_HA

  # 7. Persistent Shared Storage
  - hostname: baiostorage
    type: shared-storage
```

---

## 3. Production Deployment Lifecycle (`zerops.yaml`)

```yaml
zerops:
  - setup: astro
    build:
      os: alpine
      prepareCommands:
        - sudo apk add --no-cache curl ca-certificates
        - bun install --frozen-lockfile
        - bun run build
      deployFiles:
        - dist
        - node_modules
        - package.json
      cache:
        - node_modules

    run:
      os: alpine
      prepareCommands:
        - sudo apk add --no-cache curl ca-certificates tzdata
      start: bun ./dist/server/entry.mjs
      ports:
        - port: 3000
          httpSupport: true
      envVariables:
        HOST: "0.0.0.0"
        PORT: "3000"
        
        # Server Islands Encryption Key (Required for rolling deploys)
        ASTRO_KEY: "${ASTRO_KEY}"
        
        # Client-facing variables (Safe for client bundle)
        PUBLIC_DIRECTUS_URL: "https://cms.yourdomain.com"
        PUBLIC_SITE_URL: "https://yourdomain.com"
        
        # Internal Service Connections (Confined to Server Actions / SSR)
        DIRECTUS_URL: "http://directus:8055"
        DIRECTUS_STATIC_TOKEN: "${DIRECTUS_ADMIN_TOKEN}"
        NATS_URL: "${nats_url}"
        VALKEY_URL: "${cache_connectionString}"
        DATABASE_URL: "${db_connectionString}"
        EVOGO_URL: "http://evolutiongo:8080"
        EVOGO_API_KEY: "${EVOGO_API_KEY}"
```

---

## 4. Inviolable Security & Secret Isolation Contracts

1. **Host & Port Binding:**
   - Must listen on `HOST: "0.0.0.0"` and `PORT: "3000"` (never `localhost`).
2. **Strict Client vs. Server Variable Boundary:**
   - Client variables: MUST have `PUBLIC_` prefix (e.g. `PUBLIC_DIRECTUS_URL`).
   - Server secrets: MUST NEVER be prefixed with `PUBLIC_` and must be imported via `astro:env/server` or read in server context.
3. **`ASTRO_KEY` Rolling Update Invariant:**
   - Must configure `ASTRO_KEY` in `project.envVariables` to ensure seamless Server Islands decrypt across rolling container deploys.

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with Astro SSR must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All health check probes and API inquiries must use explicit timeouts (`timeout 10s curl -f http://astro:3000/`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all lingering workers and background monitoring scripts using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Gateway health check: `curl -s -o /dev/null -w "%{http_code}" http://astro:3000/` $\implies$ Expected: `200`.
* **Circuit Breaker Policy**: If the SSR server crashes or returns 502 Bad Gateway during deploys, verify `ASTRO_KEY` presence and `HOST: "0.0.0.0"` binding.
