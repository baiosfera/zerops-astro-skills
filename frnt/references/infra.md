# `frnt`: Frontend Infrastructure, Bun Runtime & Edge Deployment Manual (v2.0)

This manual provides production-grade deployment architectures, Bun 1.3 runtime configuration on native Zerops Incus LXC containers, `zerops_dev_server` development workflows, and Cloudflare Edge CDN routing.

---

## 1. Frontend Runtime Topology in Zerops

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Cloudflare Edge CDN & Security Periphery                                                               │
│ ├─ DNS Anycast Proxied (apex & www)                                                                    │
│ ├─ Turnstile Anti-bot Protection                                                                       │
│ ├─ Edge Cache Rule: Static Assets (/assets/*) ➔ Cache Everything                                      │
│ └─ SSL/TLS Encryption Mode: Full (Strict)                                                              │
└──────────────────────────────────────┬─────────────────────────────────────────────────────────────────┘
                                       │ HTTPS (Port 443)
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Internal High-Speed Mesh Network                                                                │
│                                                                                                        │
│   ┌────────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Astro 5 SSR Frontend Service (astro:3000)                                                      │   │
│   │ ├─ Runtime: bun@1.3.9 (Incus LXC Container)                                                    │   │
│   │ ├─ Compute: Elastic Autoscaling (minCpu: 1, maxCpu: 4, minRam: 0.5, maxRam: 4.0)               │   │
│   │ ├─ Ports: 3000 (HTTP)                                                                          │   │
│   │ └─ Mount: /mnt/baiostorage/astro/ (POSIX FUSE Shared Storage)                                  │   │
│   └──────────────────────────────────┬─────────────────────────────┬───────────────────────────────┘   │
│                                      │                             │                                   │
│                                      │ HTTP / REST                 │ TCP / RPC                         │
│                                      ▼                             ▼                                   │
│   ┌──────────────────────────────────────────────────┐ ┌───────────────────────────────────────────┐   │
│   │ Directus 11+ BaaS (directus:8055)                │ │ NATS 2.12 Message Broker (nats:4222)      │   │
│   │ ├─ Customer Auth & PIM Catalog                   │ │ ├─ Request-Reply RPC (<0.3ms P99)         │   │
│   │ └─ Directus Flows & File Storage                 │ │ └─ JetStream Event Streaming              │   │
│   └──────────────────────────────────────────────────┘ └───────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Canonical Lifecycle Recipe (`zerops.yaml`)

```yaml
zerops:
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
      cache:
        - node_modules
        - .bun/install/cache

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
      envVariables:
        PORT: 3000
        HOST: 0.0.0.0
        NODE_ENV: production
        DIRECTUS_URL: http://directus:8055
        NATS_URL: nats://nats:4222
      start: bun run ./dist/server/entry.mjs
```

---

## 3. Persistent Dev Server Supervision

For iterative local development in Zerops, start the Astro dev server via `zerops_dev_server`:

```bash
# Start Astro dev server under process supervision
zerops_dev_server hostname="astro" action="start" command="bun run dev --host 0.0.0.0 --port 3000" port=3000 healthPath="/"
```

---

## 4. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with `frnt` must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All UI builds and health probes must use explicit timeouts (`timeout 10s curl -f http://0.0.0.0:3000/`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all lingering dev servers using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Health probe check: `curl -s http://0.0.0.0:3000/ | grep -q "<html"` $\implies$ Exit 0.
* **Circuit Breaker Policy**: If the SSR server returns 502 or 503, verify Directus availability via `zerops_verify serviceHostname="directus"` before restarting the frontend container.
