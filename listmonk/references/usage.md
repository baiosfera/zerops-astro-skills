# Listmonk Developer & Agent API Manual (v2.0)

Listmonk is a self-hosted, high-performance newsletter, mailing list manager, and transactional email engine written in Go with a PostgreSQL 18 backend. This manual covers complete REST API interactions, templating syntax, transactional dispatch, bounce webhooks, production patterns, and deep integration with Zerops runtime environments (**PostgreSQL 18**, **NATS 2.12**, and **Valkey 7.2**).

---

## 1. 4D Comparative Architectural Matrix

| Dimension | Listmonk (Target) | Ghost | Mailcoach | Sendy | Resend / SES (SaaS) |
|---|---|---|---|---|---|
| **Runtime Architecture** | **Go Single Binary** (Ultra-lightweight, concurrent) | Node.js (Full CMS + Portal + Newsletter) | PHP / Laravel (Monolith / Package) | PHP 7/8 (Legacy LAMP stack) | Multi-tenant Serverless REST API |
| **Idle Memory Footprint** | **~15–35 MB RAM** | ~250–500 MB RAM | ~150–300 MB RAM | ~80–150 MB RAM | 0 MB (Managed externally) |
| **Throughput (Emails/min)** | **10,000+ emails/min** (Native goroutines) | ~1,000 emails/min | ~3,000 emails/min | ~2,500 emails/min | API Rate-limited / Quota |
| **Database Engine** | **PostgreSQL (>=12)** with `pg_trgm` | MySQL / SQLite | PostgreSQL / MySQL | MySQL | Managed Cloud Data Store |
| **Transactional Engine (`/api/tx`)** | **Yes, native high-throughput** (JSON payloads) | No (Editorial broadcasts only) | Yes (Via Mailcoach API) | Limited (Basic autoresponders) | Core primary focus |
| **Multi-Messenger Gateways** | **SMTP, Webhooks, Telegram, WhatsApp** | Mailgun SMTP only | SMTP, SES, Postmark | Amazon SES only | Email SMTP/HTTP only |
| **License & Commercial Cost** | **100% Free Open Source (AGPLv3)** | MIT / Hosted Ghost(Pro) | Commercial license per domain | $69 one-time license | Tiered monthly billing |
| **Zerops Execution Profile** | **Native Incus LXC (`os: alpine`)** | Node.js Runtime in Zerops | PHP Runtime in Zerops | PHP Runtime in Zerops | External REST HTTP calls |

### Zerops Runtime Profile: `os: alpine` vs `os: ubuntu`

| Operating Characteristic | Listmonk on `os: alpine` (Recommended) | Listmonk on `os: ubuntu` |
|---|---|---|
| **Binary Linking** | Pure static Go binary (`CGO_ENABLED=0`) | Dynamic / CGO compatible binary |
| **Filesystem Size** | Minimal (~10 MB base container) | Standard (~120 MB base container) |
| **Idle Memory (Zerops)** | **~18–25 MB RAM** | **~35–50 MB RAM** |
| **Cold Boot Latency** | **< 800 ms** | ~2–3 seconds |
| **System Utilities** | `apk add --no-cache curl ca-certificates tzdata` | `apt-get install -y curl ca-certificates tzdata` |
| **Zerops Suitability** | **Optimal for 99% of production services** | Useful for custom CGO image processing plugins |

---

## 2. Authentication & Core Conventions

All Listmonk administrative endpoints (`/api/*`) accept either HTTP Basic Authentication or API bot token headers (`Authorization: token ...`).

* **Base URL**: `http://<listmonk-hostname>:9000` (internal Zerops DNS) or `https://<custom-domain>`
* **HTTP Basic Auth**: `Authorization: Basic <base64(username:password)>` or `curl -u 'username:password'`
* **API Token Header (Preferred for Microservices)**: `Authorization: token <bot_api_token>`
* **Headers**: `Content-Type: application/json`
* **Response Envelope**:
  ```json
  {
    "data": { ... },
    "message": "optional status message"
  }
  ```

---

## 3. Zerops Ecosystem Integrations: PostgreSQL, NATS & Valkey

In a complete Zerops production architecture, Listmonk acts as the email delivery engine synchronized with managed persistence, event streaming, and in-memory caching layers:

```
                  ┌────────────────────────────────────────────────────────┐
                  │ Zerops Microservices (Node.js / Bun / Go / Python)     │
                  └─────────┬────────────────────────────┬─────────────────┘
                            │ Domain Events              │ Idempotency & Rate Limit
                            ▼                            ▼
                 ┌────────────────────┐        ┌────────────────────┐
                 │ NATS JetStream     │        │ Valkey Cache       │
                 │ (events.orders.*)  │        │ (redis-compatible) │
                 └──────────┬─────────┘        └─────────┬──────────┘
                            │ Consumes events            │ Validates locks
                            ▼                            │
                 ┌───────────────────────────────────────▼──────────┐
                 │ Async Email Worker / Orchestrator                │
                 └──────────────────────────┬───────────────────────┘
                                            │ HTTP POST /api/tx
                                            ▼
                 ┌──────────────────────────────────────────────────┐
                 │ Listmonk Service (go@1.22 / os: alpine)          │
                 └──────────────────────────┬───────────────────────┘
                                            │ Pool: max_open 50
                                            ▼
                 ┌──────────────────────────────────────────────────┐
                 │ Zerops Managed PostgreSQL (postgresql@16)        │
                 │ (Subscribers, Lists, Logs, pg_trgm GIN indexes)  │
                 └──────────────────────────────────────────────────┘
```

### A. PostgreSQL Managed Database Integration
Listmonk leverages PostgreSQL as its single source of persistent truth:
* **Connection String Wiring**: Zerops injects `${db_hostname}`, `${db_port}`, `${db_user}`, `${db_password}`, `${db_database}` directly into `LISTMONK_db__*` environment variables.
* **Full-Text & JSONB Indexing (`pg_trgm`)**: Enables fast fuzzy searching across subscriber names, emails, and nested `attribs` JSONB attributes.
* **Connection Pool Tuning**:
  - `max_open: 50`: Allows concurrent campaign workers and transactional API requests without exhausting database connections.
  - `max_idle: 25`: Retains warm pool sockets for instant query execution.
  - `max_lifetime: "300s"`: Recycles connections periodically to avoid stale TCP connections during Zerops vertical autoscaling.

---

### B. NATS JetStream Event-Driven Ingestion Pipeline
When microservices emit domain events (user signup, payment received, cart abandoned), publishing directly to NATS JetStream guarantees zero lost emails during spikes. A dedicated worker consumes from NATS and posts to Listmonk:

#### Node.js / Bun NATS Consumer to Listmonk `/api/tx`
```typescript
import { connect, JSONCodec } from "nats";

interface OrderEvent {
  order_id: string;
  customer_email: string;
  customer_name: string;
  total_amount: string;
  items: Array<{ name: string; qty: number; price: string }>;
}

async function startEmailWorker() {
  const nc = await connect({ servers: process.env.NATS_URL || "nats://nats:4222" });
  const js = nc.jetstream();
  const jc = JSONCodec<OrderEvent>();

  const sub = await js.subscribe("events.orders.completed", {
    durable_name: "listmonk-email-dispatcher",
  });

  console.log("Listening for order events on NATS...");

  for await (const msg of sub) {
    try {
      const event = jc.decode(msg.data);

      // Dispatch to Listmonk Transactional API over internal Zerops DNS
      const res = await fetch("http://listmonk:9000/api/tx", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Basic " + Buffer.from(`${process.env.LISTMONK_ADMIN_USER}:${process.env.LISTMONK_ADMIN_PASSWORD}`).toString("base64"),
        },
        body: JSON.stringify({
          subscriber_mode: "external",
          subscriber_emails: [event.customer_email],
          template_id: 2, // Order confirmation template
          subject: `Confirmation for Order #${event.order_id}`,
          data: {
            customer_name: event.customer_name,
            order_id: event.order_id,
            total_amount: event.total_amount,
            items: event.items,
          },
        }),
      });

      if (res.ok) {
        msg.ack();
      } else {
        console.error("Listmonk API error:", await res.text());
        msg.nak(5000); // Re-queue after 5s
      }
    } catch (err) {
      console.error("Worker processing failed:", err);
      msg.nak(5000);
    }
  }
}

startEmailWorker();
```

---

### C. Valkey (Redis-Compatible) Caching & Idempotency Layer
Valkey sits between external client traffic and Listmonk to ensure transactional idempotency and protection against subscription spam:

#### 1. Idempotency Lock Pattern (Prevents Duplicate Emails)
```typescript
import { createClient } from "redis";

const valkey = createClient({ url: process.env.VALKEY_URL || "redis://cache:6379" });
await valkey.connect();

export async function sendTransactionalEmailOnce(orderId: string, payload: any) {
  const lockKey = `idempotency:tx:order:${orderId}`;
  
  // SET lockKey 1 NX EX 86400 (Set only if Not Exists, TTL 24h)
  const acquired = await valkey.set(lockKey, "processing", { NX: true, EX: 86400 });
  if (!acquired) {
    console.log(`Duplicate request ignored for order ${orderId}`);
    return { status: "already_sent" };
  }

  // Call Listmonk /api/tx
  const response = await fetch("http://listmonk:9000/api/tx", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Basic " + Buffer.from("admin:password").toString("base64"),
    },
    body: JSON.stringify(payload),
  });

  return response.json();
}
```

#### 2. Public Subscription Rate-Limiting
```typescript
// Rate limit public newsletter subscriptions by IP (max 5 per minute)
export async function checkRateLimit(clientIp: string): Promise<boolean> {
  const key = `ratelimit:subscribe:${clientIp}`;
  const count = await valkey.incr(key);
  if (count === 1) {
    await valkey.expire(key, 60);
  }
  return count <= 5;
}
```

---

## 4. Subscribers Management API

### Endpoint Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/subscribers` | Query, filter, and paginate subscribers |
| `GET` | `/api/subscribers/{id}` | Retrieve single subscriber by ID |
| `POST` | `/api/subscribers` | Create a new subscriber with attributes |
| `PUT` | `/api/subscribers/{id}` | Update existing subscriber profile and list memberships |
| `PATCH` | `/api/subscribers/{id}` | Partially update subscriber attributes |
| `PUT` | `/api/subscribers/lists` | Modify bulk list memberships for multiple subscriber IDs |
| `PUT` | `/api/subscribers/{id}/blocklist` | Add subscriber to global suppression/blocklist |
| `DELETE` | `/api/subscribers/{id}` | Delete single subscriber permanently |
| `DELETE` | `/api/subscribers/{id}/bounces` | Clear bounce records for a subscriber |

### Create Subscriber (`POST /api/subscribers`)

```bash
curl -s -u 'admin:password' -X POST http://listmonk:9000/api/subscribers \
  -H 'Content-Type: application/json' \
  -d '{
    "email": "user@example.com",
    "name": "Jane Doe",
    "status": "enabled",
    "lists": [1, 2],
    "attribs": {
      "city": "Madrid",
      "tier": "enterprise",
      "company": "Zerops Corp"
    },
    "preconfirm_subscriptions": true
  }'
```

### Advanced Subscriber Querying (`GET /api/subscribers`)

Listmonk supports arbitrary PostgreSQL SQL expressions against `subscribers` columns and JSONB attributes:

```bash
# Query subscribers where city is 'Madrid' and created in 2026
curl -s -u 'admin:password' -G http://listmonk:9000/api/subscribers \
  --data-urlencode "query=subscribers.attribs->>'city' = 'Madrid' AND subscribers.status = 'enabled'" \
  --data-urlencode "page=1" \
  --data-urlencode "per_page=50" \
  --data-urlencode "order_by=created_at" \
  --data-urlencode "order=DESC"
```

---

## 5. High-Performance Transactional Engine (`POST /api/tx`)

Listmonk provides a dedicated high-throughput transactional endpoint that renders preconfigured Go templates on-the-fly and sends individual emails.

### Request Schema

| Parameter | Type | Required | Description |
|---|---|---|---|
| `subscriber_email` | string | Optional* | Target email (required if `subscriber_id` is not provided) |
| `subscriber_id` | number | Optional* | Target subscriber ID |
| `subscriber_emails` | string[] | Optional* | Array of emails for multi-recipient dispatch |
| `subscriber_mode` | string | No | Mode: `default` (registered only), `fallback` (look up or send raw), `external` (send to non-subscribers) |
| `template_id` | number | **Yes** | ID of the transactional email template |
| `from_email` | string | No | Custom sender address (e.g. `orders@example.com`) |
| `subject` | string | No | Overrides default template subject line |
| `data` | JSON object | No | Payload injected into template as `{{ .Tx.Data.* }}` |
| `headers` | JSON array | No | Custom MIME headers (e.g. `[{"X-Tracking-ID": "12345"}]`) |
| `content_type` | string | No | `html` (default), `markdown`, or `plain` |

### Transactional Order Confirmation Dispatch

```bash
curl -s -u 'admin:password' -X POST http://listmonk:9000/api/tx \
  -H 'Content-Type: application/json' \
  -d '{
    "subscriber_mode": "external",
    "subscriber_emails": ["customer@example.com"],
    "template_id": 3,
    "subject": "Your Order #98421 Confirmation",
    "data": {
      "customer_name": "Alice Smith",
      "order_id": "98421",
      "total_amount": "$149.00",
      "items": [
        {"name": "Zerops Managed Cloud Node", "qty": 1, "price": "$120.00"},
        {"name": "Dedicated Storage Volume", "qty": 1, "price": "$29.00"}
      ]
    }
  }'
```

---

## 6. Templating Engine Syntax & Sprig Functions

Listmonk uses standard Go `html/template` with Sprig helper functions.

### Reserved System Variables & Tags

| Tag / Syntax | Description | Example |
|---|---|---|
| `{{ UnsubscribeURL }}` | Generates direct 1-click unsubscribe link | `<a href="{{ UnsubscribeURL }}">Unsubscribe</a>` |
| `{{ MessageURL }}` | Generates web archive link to view email in browser | `<a href="{{ MessageURL }}">View in Browser</a>` |
| `{{ TrackView }}` | Injects 1x1 transparent tracking pixel | `{{ TrackView }}` |
| `{{ TrackLink "https://url" }}` | Wraps URL for click tracking and redirection | `<a href="{{ TrackLink "https://zerops.io" }}">Zerops</a>` |
| `{{ .Subscriber.Email }}` | Subscriber email address | `Hello {{ .Subscriber.Email }}` |
| `{{ .Subscriber.Name }}` | Subscriber full name | `Welcome, {{ .Subscriber.Name }}` |
| `{{ .Subscriber.Attribs.key }}` | Custom subscriber JSONB attributes | `Location: {{ .Subscriber.Attribs.city }}` |
| `{{ .Tx.Data.key }}` | Transactional payload parameters | `Order ID: {{ .Tx.Data.order_id }}` |
| `{{ DateFormat .Date "2006-01-02" }}` | Sprig date formatting helper | `Issued: {{ DateFormat .Date "02 Jan 2006" }}` |

### Sample Transactional Template

```html
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
  <h2>Order Confirmation #{{ .Tx.Data.order_id }}</h2>
  <p>Hello {{ if .Subscriber.Name }}{{ .Subscriber.Name }}{{ else }}{{ .Tx.Data.customer_name }}{{ end }},</p>
  <p>Thank you for your order with total amount of <strong>{{ .Tx.Data.total_amount }}</strong>.</p>
  <ul>
    {{ range .Tx.Data.items }}
      <li>{{ .qty }}x {{ .name }} - {{ .price }}</li>
    {{ end }}
  </ul>
  <hr>
  <p><small><a href="{{ UnsubscribeURL }}">Unsubscribe</a> | <a href="{{ MessageURL }}">Web Version</a></small></p>
  {{ TrackView }}
</body>
</html>
```

---

## 7. Campaigns & Mailing Lists API

### Create Campaign (`POST /api/campaigns`)

```bash
curl -s -u 'admin:password' -X POST http://listmonk:9000/api/campaigns \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "August 2026 Developer Update",
    "subject": "What is new in Zerops & Gentle AI",
    "lists": [1],
    "type": "regular",
    "content_type": "html",
    "body": "<h1>Monthly Update</h1><p>Check out our latest releases!</p>{{ TrackView }}",
    "send_at": null
  }'
```

### Campaign State Transitions (`PUT /api/campaigns/{id}/status`)

Valid status values: `draft`, `scheduled`, `running`, `paused`, `cancelled`.

```bash
# Start campaign execution
curl -s -u 'admin:password' -X PUT http://listmonk:9000/api/campaigns/5/status \
  -H 'Content-Type: application/json' \
  -d '{"status": "running"}'
```

---

## 8. Bounce & Complaint Webhooks

Listmonk includes built-in webhook parsers to automatically suppress addresses that bounce or report spam:

* **Amazon SES**: `POST /webhooks/service/ses` (Configure SNS HTTPS subscription to this URL).
* **SendGrid**: `POST /webhooks/service/sendgrid` (Configure Event Webhook).
* **Postmark**: `POST /webhooks/service/postmark` (Configure Bounce Webhook).
* **Generic Webhook**: `POST /webhooks/bounce` (Accepts `{ "email": "bounced@example.com", "type": "hard" }`).

---

## 9. 5 Production Patterns in Zerops

### Pattern 1: High-Throughput Newsletter Broadcast
Connects Listmonk to Zerops Managed PostgreSQL with connection pooling (`max_open: 50`, `max_idle: 25`) and Amazon SES / Resend SMTP credentials to deliver 50,000+ emails in minutes.

### Pattern 2: Event-Driven Order Notifications via NATS
Microservices publish `order.completed` events to NATS JetStream. A lightweight Node.js/Go worker consumes messages and dispatches transactional emails to Listmonk `/api/tx` over internal Zerops DNS with zero public egress costs.

### Pattern 3: Valkey-Protected Subscription Gateway
A public-facing API routes user newsletter signups through Valkey rate-limiting (sliding window 5 req/min) and writes pre-confirmed subscribers into Listmonk via `POST /api/subscribers`.

### Pattern 4: Multi-Messenger Routing (Telegram / WhatsApp)
Listmonk routes campaigns and alerts simultaneously to email inboxes and Telegram channels by enabling custom messenger gateways in the admin console.

### Pattern 5: Zero-Downtime Migration & Auto-Upgrade
Using `zsc execOnce ${appVersionId} -- ./listmonk --upgrade --yes --config=""` in `run.initCommands` ensures schema migrations execute once across all horizontal containers on every release.

---

## 10. Anti-Patterns & Common Gotchas

1. **Missing `pg_trgm` Extension**: Listmonk requires the `pg_trgm` extension for fast subscriber search. Zerops Managed PostgreSQL includes this natively.
2. **Exposing Port 9000 without Auth Proxy**: If exposing Listmonk to public subdomains, secure the `/admin` and `/api` paths with strong admin passwords.
3. **Hardcoding DB Credentials**: Never hardcode database credentials in `config.toml`. Use Zerops runtime variables (`LISTMONK_db__host: ${db_hostname}`).
4. **Omitting `zsc execOnce` on Deploy**: Running `./listmonk --install` without `zsc execOnce` on multi-container setups will cause concurrent table creation race conditions.
