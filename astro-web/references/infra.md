# Astro 5 Infrastructure, Secret Isolation & Zerops Deployment Manual (v3.0)

This manual provides production-grade infrastructure blueprints, multi-service `import.yaml` provisioning recipes (**Astro 5 SSR**, **NATS JetStream 2.12**, **Valkey 7.2**, **PostgreSQL 18**, and S3 **Object Storage**), `zerops.yaml` pipeline lifecycles on Bun 1.3 / Ubuntu, secret isolation contracts, and the Fractal CoHaLo operational harness.

---

## 1. Ecosystem Topology

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Enterprise Project Topology                                                                     │
│                                                                                                        │
│   ┌──────────────────────────────────────────┐                                                         │
│   │ Astro 5 SSR Frontend (web)               │                                                         │
│   │ Base: ubuntu/bun@1.3.9                   │                                                         │
│   │ Port 3000 (HTTP Subdomain / CDN)         │                                                         │
│   └────────────────────┬─────────────────────┘                                                         │
│                        │                                                                               │
│         ┌──────────────┼──────────────────────────────┐                                                │
│         │              │                              │                                                │
│         ▼              ▼                              ▼                                                │
│   ┌──────────────┐ ┌──────────────────────────┐ ┌──────────────────────────────────────────────────┐   │
│   │ NATS 2.12    │ │ Valkey 7.2 Cache         │ │ Managed PostgreSQL 18 Cluster                    │   │
│   │ (queue)      │ │ (cache)                  │ │ (db)                                             │   │
│   │ nats:single  │ │ valkey:single@7.2        │ │ postgresql:single@18                             │   │
│   │ Port 4222    │ │ Port 6379                │ │ Port 5432                                        │   │
│   └──────────────┘ └──────────────────────────┘ └──────────────────────────────────────────────────┘   │
│         │                                                                                              │
│         ▼                                                                                              │
│   ┌──────────────────────────────────────────┐                                                         │
│   │ S3 Compatible Object Storage (storage)   │                                                         │
│   │ type: object-storage                     │                                                         │
│   └──────────────────────────────────────────┘                                                         │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Multi-Service Provisioning Blueprint (`import.yaml`) {#2-topology}

```yaml
services:
  # 1. Astro 5 SSR Frontend Webapp (Bun 1.3.9 on Ubuntu)
  - hostname: web
    type: ubuntu/bun@1.3.9
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

  # 2. Managed NATS 2.12 JetStream Message Broker
  - hostname: queue
    type: nats:single@2.12
    verticalAutoscaling:
      cpuMode: SHARED

  # 3. Managed Valkey 7.2 for Sessions, Locks & Rate Limiting
  - hostname: cache
    type: valkey:single@7.2
    mode: NON_HA

  # 4. Managed PostgreSQL 18 Cluster
  - hostname: db
    type: postgresql:single@18
    mode: NON_HA

  # 5. S3 Compatible Object Storage
  - hostname: storage
    type: object-storage
    objectStorageSize: 10
```

---

## 3. Production Deployment Lifecycle (`zerops.yaml`) {#3-lifecycle}

```yaml
zerops:
  - setup: web
    build:
      base: ubuntu/bun@1.3.9
      envVariables:
        BUN_INSTALL: ./.bun
      buildCommands:
        - bun install --frozen-lockfile
        - bun run build
      deployFiles:
        - dist
        - node_modules
        - package.json
      cache:
        - node_modules
        - .bun/install/cache

    deploy:
      readinessCheck:
        httpGet:
          port: 3000
          path: /

    run:
      base: ubuntu/bun@1.3.9
      ports:
        - port: 3000
          httpSupport: true
      start: bun run ./dist/server/entry.mjs
      envVariables:
        HOST: "0.0.0.0"
        PORT: 3000
        NODE_ENV: production
        
        # Server Islands Encryption Key (Required for zero-downtime rolling deploys)
        ASTRO_KEY: "${ASTRO_KEY}"
        
        # Managed Service Connections (Injected via Zerops Platform)
        DATABASE_URL: "${db_connectionString}"
        VALKEY_URL: "${cache_connectionString}"
        NATS_URL: "${queue_connectionString}"
        
        # S3 Object Storage Credentials
        S3_ENDPOINT: "${storage_apiUrl}"
        S3_ACCESS_KEY: "${storage_accessKeyId}"
        S3_SECRET_KEY: "${storage_secretAccessKey}"
        S3_BUCKET: "${storage_bucketName}"
      healthCheck:
        httpGet:
          port: 3000
          path: /
```

---

## 4. Inviolable Security & Secret Isolation Contracts

1. **Host & Port Binding:**
   - Must listen on `HOST: "0.0.0.0"` and `PORT: "3000"` (never bind to `localhost`).
2. **Strict Client vs. Server Variable Boundary:**
   - Client variables: MUST have `PUBLIC_` prefix (e.g. `PUBLIC_SITE_URL`).
   - Server secrets: MUST NEVER be prefixed with `PUBLIC_` and must be imported via `astro:env/server` or read in server context.
3. **`ASTRO_KEY` Rolling Update Invariant:**
   - Must configure `ASTRO_KEY` in `project.envVariables` to ensure seamless Server Islands decryption across rolling container deploys.

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

* **Bounded Timeouts**: All health check probes and API inquiries must use explicit timeouts (`timeout 10s curl -f http://web:3000/`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate lingering workers and background monitoring scripts using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Gateway health check: `curl -s -o /dev/null -w "%{http_code}" http://web:3000/` $\implies$ Expected: `200`.
* **Circuit Breaker Policy**: If the SSR server crashes or returns 502 Bad Gateway during deploys, verify `ASTRO_KEY` presence and `HOST: "0.0.0.0"` binding.
