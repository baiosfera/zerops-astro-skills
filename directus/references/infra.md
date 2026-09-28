# Directus 11+ Infrastructure, Google OAuth & Zerops Deployment Manual (v2.0)

This manual provides production-grade infrastructure blueprints, multi-service `import.yaml` provisioning recipes (including **Astro**, **Directus 11+**, **Evolution Go**, **AI Worker**, **PostgreSQL 18**, **NATS**, and **Valkey**), `zerops.yaml` pipeline lifecycles, environment variable mapping, Google Cloud Console OAuth 2.0 runbook, and the Fractal CoHaLo operational harness for Directus running in Zerops.

---

## 1. Multi-Service Zerops Ecosystem Topology

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Enterprise Project Topology                                                                     │
│                                                                                                        │
│   ┌──────────────────────────────┐              ┌──────────────────────────────────────────────────┐   │
│   │ Astro Frontend UI (astro)    │              │ Directus 11+ Unified BaaS (directus)             │   │
│   │ (bun@1.3 / nodejs@24)        │─────────────▶│ (nodejs@24 / os: ubuntu)                         │   │
│   │ Port 3000 (HTTP Subdomain)   │              │ Port 8055 (HTTP Subdomain)                       │   │
│   └──────────────────────────────┘              └────────────────────────┬─────────────────────────┘   │
│                                                                          │                             │
│   ┌──────────────────────────────┐              ┌────────────────────────▼─────────────────────────┐   │
│   │ Evolution Go Gateway (evogo) │              │ NATS JetStream Message Broker (nats)             │   │
│   │ (go@1.22 / os: alpine)       │◀────────────▶│ (nats@2.10)                                      │   │
│   │ Port 8080 (Internal / Sub)   │              │ Port 4222 (Internal Zerops DNS)                  │   │
│   └──────────────┬───────────────┘              └────────────────────────┬─────────────────────────┘   │
│                  │                                                       │                             │
│                  │ Media uploads                                         ▼                             │
│                  ▼                              ┌──────────────────────────────────────────────────┐   │
│   ┌──────────────────────────────┐              │ Intelligent AI / LLM & Telemetry Worker (aiworker│   │
│   │ Shared Storage (baiostorage) │              │ (python@3.12 / nodejs@24)                        │   │
│   │ /mnt/baiostorage/directus    │              │ - Consumes NATS events, LLMOps Telemetry & RAG   │   │
│   └──────────────────────────────┘              └────────────────────────┬─────────────────────────┘   │
│                                                                          │                             │
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
  # 1. Managed PostgreSQL 18 for Directus Data, System Collections & pgvector
  - hostname: db
    type: postgresql@18:single
    mode: NON_HA

  # 2. Managed Valkey for Query Cache, Schema Sync & WebSockets
  - hostname: cache
    type: valkey@7.2:single
    mode: NON_HA

  # 3. NATS JetStream Event Broker
  - hostname: nats
    type: nats@2.10

  # 4. Directus 11+ Unified BaaS Engine
  - hostname: directus
    type: nodejs@24
    enableSubdomainAccess: true

  # 5. Evolution Go WhatsApp Gateway
  - hostname: evolutiongo
    type: go@1.22
    enableSubdomainAccess: true

  # 6. Intelligent AI / LLM Worker
  - hostname: aiworker
    type: nodejs@24

  # 7. Astro Frontend Webapp
  - hostname: astro
    type: nodejs@24
    enableSubdomainAccess: true

  # 8. Persistent Shared Storage for Directus Uploads & Media
  - hostname: baiostorage
    type: shared-storage
```

---

## 3. Production Deployment Lifecycle (`zerops.yaml`)

```yaml
zerops:
  - setup: directus
    build:
      os: ubuntu
      prepareCommands:
        - sudo apt-get update && sudo apt-get install -y curl ca-certificates build-essential python3
        - npm install directus @directus/extensions-sdk sharp
      deployFiles:
        - node_modules
        - package.json
        - extensions
        - uploads
      cache:
        - node_modules

    run:
      os: ubuntu
      prepareCommands:
        - sudo apt-get update && sudo apt-get install -y ffmpeg curl ca-certificates
        # Ensure uploads storage directory permissions on FUSE mount
        - sudo mkdir -p /mnt/baiostorage/directus/uploads 2>/dev/null || true
        - sudo chmod -R 777 /mnt/baiostorage/directus/uploads 2>/dev/null || true

      initCommands:
        # Atomic cluster bootstrap on every release (idempotent)
        - zsc execOnce ${appVersionId} --retryUntilSuccessful -- npx directus bootstrap

      start: npx directus start

      ports:
        - port: 8055
          httpSupport: true

      envVariables:
        # General & Server configuration
        PORT: "8055"
        HOST: "0.0.0.0"
        PUBLIC_URL: "https://cms.yourdomain.com"
        CORS_ENABLED: "true"
        CORS_ORIGIN: "*"
        
        # PostgreSQL Connection
        DB_CLIENT: "pg"
        DB_CONNECTION_STRING: "${db_connectionString}"
        
        # Valkey (Redis) Cache, Schema Sync & WebSockets
        CACHE_ENABLED: "true"
        CACHE_STORE: "redis"
        CACHE_REDIS: "${cache_connectionString}"
        CACHE_AUTO_PURGE: "true"
        CACHE_TTL: "1h"
        SYNCHRONIZATION_STORE: "redis"
        MESSENGER_STORE: "redis"
        WEBSOCKETS_ENABLED: "true"
        
        # File Storage
        STORAGE_LOCATIONS: "local"
        STORAGE_LOCAL_DRIVER: "local"
        STORAGE_LOCAL_ROOT: "/mnt/baiostorage/directus/uploads"
        
        # Security & Secrets
        KEY: "GENERATE_RANDOM_KEY_IN_ZEROPS_PROJECT"
        SECRET: "GENERATE_RANDOM_SECRET_IN_ZEROPS_PROJECT"
        ADMIN_EMAIL: "admin@yourdomain.com"
        ADMIN_PASSWORD: "CHANGE_ME_ADMIN_PASSWORD"
        
        # Google OAuth 2.0 (Optional)
        AUTH_PROVIDERS: "google"
        AUTH_GOOGLE_DRIVER: "oauth2"
        AUTH_GOOGLE_CLIENT_ID: "${AUTH_GOOGLE_CLIENT_ID}"
        AUTH_GOOGLE_CLIENT_SECRET: "${AUTH_GOOGLE_CLIENT_SECRET}"
        AUTH_GOOGLE_AUTHORIZE_URL: "https://accounts.google.com/o/oauth2/v2/auth"
        AUTH_GOOGLE_ACCESS_URL: "https://oauth2.googleapis.com/token"
        AUTH_GOOGLE_PROFILE_URL: "https://openidconnect.googleapis.com/v1/userinfo"
        AUTH_GOOGLE_ALLOW_PUBLIC_REGISTRATION: "true"
        AUTH_GOOGLE_DEFAULT_ROLE_ID: "CUSTOMER_ROLE_UUID"
        AUTH_GOOGLE_REDIRECT_URL: "https://cms.yourdomain.com/auth/login/google/callback"
```

---

## 4. Environment Variables Reference Dictionary

| Variable | Scope | Description |
|---|---|---|
| `PORT` | Server | HTTP Server port (`"8055"`) |
| `PUBLIC_URL` | Server | Canonical public domain URL |
| `DB_CLIENT` | Database | Database driver (`"pg"`) |
| `DB_CONNECTION_STRING` | Database | Full PostgreSQL connection string (`${db_connectionString}`) |
| `CACHE_ENABLED` | Cache | Enable Valkey query and schema caching (`"true"`) |
| `CACHE_STORE` | Cache | Cache store driver (`"redis"`) |
| `CACHE_REDIS` | Cache | Valkey connection URI (`${cache_connectionString}`) |
| `CACHE_AUTO_PURGE` | Cache | Automatically invalidate queries on item mutation (`"true"`) |
| `SYNCHRONIZATION_STORE`| Cluster | Multi-node cluster synchronization via Valkey (`"redis"`) |
| `MESSENGER_STORE` | Realtime | Multi-node WebSocket pub/sub store (`"redis"`) |
| `WEBSOCKETS_ENABLED` | Realtime | Enable real-time WebSocket subscriptions (`"true"`) |
| `STORAGE_LOCAL_ROOT` | Media | Path on shared storage mount (`"/mnt/baiostorage/directus/uploads"`) |
| `AUTH_PROVIDERS` | Auth | Authentication providers list (e.g. `"google"`) |
| `AUTH_GOOGLE_CLIENT_ID`| OAuth | Google Cloud Console OAuth Client ID |
| `AUTH_GOOGLE_CLIENT_SECRET`| OAuth | Google Cloud Console OAuth Client Secret |

---

## 5. Google Cloud Console OAuth 2.0 Runbook

1. Navigate to [Google Cloud Console](https://console.cloud.google.com) and create or select your project.
2. In the navigation menu, go to **APIs & Services** $\to$ **OAuth consent screen**:
   - User Type: Select **External** $\to$ Click **Create**.
   - Fill in **App Name**, **User Support Email**, and **Developer Contact Email**.
3. Under **Scopes**, click **Add or Remove Scopes** and select:
   - `openid`
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
4. In **Credentials**, click **Create Credentials** $\to$ **OAuth Client ID**:
   - Application Type: **Web application**.
   - **Authorized JavaScript origins:** `https://yourdomain.com` and `https://cms.yourdomain.com`.
   - **Authorized redirect URIs:** `https://cms.yourdomain.com/auth/login/google/callback`.
5. Copy the generated **Client ID** and **Client Secret** and inject into Zerops as `AUTH_GOOGLE_CLIENT_ID` and `AUTH_GOOGLE_CLIENT_SECRET`.

---

## 6. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with Directus must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All health check probes and API inquiries must use explicit timeouts (`timeout 10s curl -f http://directus:8055/server/health`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all lingering workers and background monitoring scripts using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Gateway health check: `curl -s -o /dev/null -w "%{http_code}" http://directus:8055/server/health` $\implies$ Expected: `200`.
  * Database connectivity: `psql "$db_connectionString" -c 'SELECT count(*) FROM "directus_collections";'`.
* **Circuit Breaker Policy**: If Directus bootstrap fails or reports table locks, retry up to 2 times. If failure persists, trigger escalation and inspect PostgreSQL migration logs.
