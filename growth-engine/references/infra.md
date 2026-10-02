# Sovereign Growth Engine Infrastructure Specification (v2.0)

## 1. Zerops Incus LXC Topology & Internal DNS Discovery

All services run inside high-speed Linux Containers (Incus LXC) within the sovereign Zerops private virtual network. Inter-service communication uses native internal DNS hostnames:

```
┌────────────────────────────────────────────────────────┐
│               Zerops Private Network                   │
│                                                        │
│  ┌───────────────────┐        ┌─────────────────────┐  │
│  │  Astro 5 SSR      │        │  Valkey 7.2         │  │
│  │  (webdev:3000)    ├───────►│  (valkey:6379)      │  │
│  │  Bun 1.3 / 1.4    │        │  Staging & Queues   │  │
│  └─────────┬─────────┘        └─────────────────────┘  │
│            │                             ▲             │
│            ▼                             │             │
│  ┌───────────────────┐        ┌──────────┴──────────┐  │
│  │  Bifrost Gateway  │        │  Recovery Worker    │  │
│  │  (bifrost:8080)   │        │  (BullMQ / Bun)     │  │
│  │  Maxim AI LLM     │        └──────────┬──────────┘  │
│  └───────────────────┘                   │             │
│                                          ▼             │
│  ┌───────────────────┐        ┌─────────────────────┐  │
│  │  NATS JetStream   │◄───────┤  Listmonk / Email   │  │
│  │  (nats:4222)      │        │  (listmonk:9000)    │  │
│  └───────────────────┘        └─────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Port & Service Discovery Matrix

| Service | Hostname & Port | Protocol | Purpose in Growth Engine |
|---|---|---|---|
| **Maxim AI Bifrost** | `http://bifrost:8080/v1` | HTTP / OpenAI REST | Single Front Door for all LLM copy generation, objection handling & recovery synthesis |
| **Valkey 7.2** | `valkey:6379` | RESP / Redis | Cart lead staging (`cart:abandoned:${id}`) & BullMQ delayed recovery queues |
| **NATS JetStream** | `nats:4222` | NATS | Asynchronous event mesh for cart abandonment triggers & outbound notifications |
| **Listmonk** | `http://listmonk:9000` | HTTP / REST | High-performance transactional email dispatch & RFC 8058 unsubscribe tracking |
| **Astro 5 Web Service** | `0.0.0.0:3000` | HTTP / SSR | Customer storefront, Astro Action lead capture endpoints & Server Islands |

---

## 3. Environment Variables Specification

All connection strings and secrets must be injected via Zerops environment variables or container shell references:

```bash
# LLM Gateway
BIFROST_URL="http://bifrost:8080/v1"
BIFROST_API_KEY="${BIFROST_API_KEY:-}"

# Cache & Queues (Mapped automatically by Zerops)
VALKEY_URL="${valkey_connectionString}"
REDIS_URL="${valkey_connectionString}"

# Event Bus
NATS_URL="${nats_connectionString}"

# Outbound Delivery
LISTMONK_URL="http://listmonk:9000"
LISTMONK_API_KEY="${LISTMONK_API_KEY:-}"

# Brand Voice Configuration
BRAND_SSOT_PATH="/var/www/src/config/brand.json"
```

---

## 4. Production `zerops.yaml` Service Definition (Bun SSR)

```yaml
zerops:
  - setup: webdev
    build:
      base: ubuntu/bun@1.3
      buildCommands:
        - bun install --frozen-lockfile
        - bun run build
      deployFiles:
        - dist/
        - package.json
        - node_modules/
    run:
      base: ubuntu/bun@1.3
      ports:
        - port: 3000
          httpSupport: true
      envVariables:
        PORT: "3000"
        HOST: "0.0.0.0"
        NODE_ENV: "production"
        DATABASE_URL: ${database_connectionString}
        VALKEY_URL: ${valkey_connectionString}
        NATS_URL: ${nats_connectionString}
        BIFROST_URL: "http://bifrost:8080/v1"
        LISTMONK_URL: "http://listmonk:9000"
      start: bun run ./dist/server/entry.mjs
      healthCheck:
        httpGet:
          port: 3000
          path: /health
```

---

## 5. Observability, Timeouts & Sensor Hygiene

- **Execution Bounds**: All asynchronous background calls must specify explicit timeouts (`timeout 10s`).
- **Idempotency Locks**: Redis locks use unique owner UUID tokens and expire within 3600 seconds.
- **Clean-Room Verification**: Automated scripts must run with `PYTHONDONTWRITEBYTECODE=1` and purge any residual `__pycache__` artifacts upon completion.
