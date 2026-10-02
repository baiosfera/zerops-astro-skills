# Email Marketing: Infrastructure, Zerops Topology & Console Runbooks (v2.0)

This manual provides production-grade infrastructure blueprints, DNS deliverability records (SPF, DKIM 2048-bit, DMARCbis RFC 9989, FCrDNS PTR), BullMQ rate-limited queue workers, and the Fractal CoHaLo operational harness for `email-marketing` running in Zerops.

---

## 1. Multi-Service Email Dispatch Topology in Zerops

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Internal High-Speed Network                                                                     │
│                                                                                                        │
│   ┌──────────────────────────────────────────────────┐                                                 │
│   │ Directus 11+ / Astro 5 Frontend (directus/astro) │                                                 │
│   │ - Emits purchase or campaign trigger             │                                                 │
│   └───────────────┬──────────────────────────────────┘                                                 │
│                   │ Emits event                                                                        │
│                   ▼                                                                                    │
│   ┌──────────────────────────────────────────────────┐                                                 │
│   │ NATS JetStream (nats:4222)                       │                                                 │
│   │ - `events.orders.completed`                      │                                                 │
│   │ - `events.auth.magic_link`                       │                                                 │
│   └───────────────┬──────────────────────────────────┘                                                 │
│                   │ Enqueues job                                                                       │
│                   ▼                                                                                    │
│   ┌──────────────────────────────────────────────────┐                                                 │
│   │ Valkey 7.2 Queue Engine (cache:6379)             │                                                 │
│   │ - Queue: `emailDispatchQueue` (BullMQ)           │                                                 │
│   │ - Rate Limiter: max 10 emails / 1000ms           │                                                 │
│   └───────────────┬──────────────────────────────────┘                                                 │
│                   │ Pulls throttled job                                                                │
│                   ▼                                                                                    │
│   ┌──────────────────────────────────────────────────┐                                                 │
│   │ Email Dispatcher Worker (aiworker / directus)    │                                                 │
│   │ (bun@1.3 / nodejs@24)                            │                                                 │
│   │ - Transpiles React Email 3.0 to inline HTML      │                                                 │
│   │ - Dispatches to active provider relay            │                                                 │
│   └───────────────┬──────────────┬──────────────┬────┘                                                 │
│                   │              │              │                                                      │
│                   ▼              ▼              ▼                                                      │
│   ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐                                       │
│   │ Zoho ZeptoMail   │ │ Amazon SES v2    │ │ Listmonk (Go)    │                                       │
│   │ (REST API v1.1)  │ │ (us-east-1)      │ │ (Self-Hosted)    │                                       │
│   └──────────────────┘ └──────────────────┘ └──────────────────┘                                       │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 2026 Deliverability & DNS Configuration Standards

1. **Spam Complaint Thresholds (Google Postmaster Tools & Yahoo Sender Hub):**
   * **Optimal Target:** Spam Complaint Rate **< 0.10%** (max 1 complaint per 1,000 sent emails).
   * **Alert Zone:** 0.10% – 0.29% (progressive inbox deprioritization).
   * **Hard Block:** **$\ge$ 0.30%** (outright rejection or universal SPAM placement).
2. **Cryptographic DNS Records:**
   * **SPF:** `TXT @ "v=spf1 include:zeptomail.net include:amazonses.com ~all"` (max 10 DNS lookups).
   * **DKIM:** 2048-bit RSA keys mandatory (`zoho._domainkey` / Amazon SES CNAME selectors).
   * **DMARCbis (RFC 9989):** `TXT _dmarc "v=DMARC1; p=quarantine; sp=quarantine; adkim=r; aspf=r; rua=mailto:dmarc@yourdomain.com;"`.
   * **Reverse DNS (PTR):** Valid FCrDNS resolving between sending IP and mail server hostname.
3. **RFC 8058 One-Click Unsubscribe:**
   * `List-Unsubscribe: <https://api.yourdomain.com/unsubscribe?id=xxx>` and `List-Unsubscribe-Post: List-Unsubscribe=One-Click` headers signed under DKIM.

---

## 3. Environment Variables Reference Dictionary

```ini
# ============================================================================
# ZOHO ZEPTOMAIL (REST API & SMTP)
# ============================================================================
ZEPTOMAIL_SEND_MAIL_TOKEN="Zoho-enczapikey wSsVR61...=="
ZEPTOMAIL_DEFAULT_FROM_EMAIL="noreply@yourdomain.com"
ZEPTOMAIL_DEFAULT_FROM_NAME="Store Notifications"
ZEPTOMAIL_BOUNCE_ADDRESS="bounce@bounce.yourdomain.com"
ZEPTOMAIL_REGION="com"

# ============================================================================
# AWS SES V2
# ============================================================================
AWS_REGION="us-east-1"
AWS_ACCESS_KEY_ID="AKIA..."
AWS_SECRET_ACCESS_KEY="secret..."
AWS_SES_CONFIGURATION_SET="deliverability-set"
AWS_SES_DEFAULT_FROM="Store <noreply@yourdomain.com>"

# ============================================================================
# RESEND API
# ============================================================================
RESEND_API_KEY="re_123456789..."
RESEND_DEFAULT_FROM="Store <noreply@yourdomain.com>"

# ============================================================================
# LISTMONK (SELF-HOSTED IN ZEROPS)
# ============================================================================
LISTMONK_URL="http://listmonk:9000"
LISTMONK_API_USER="admin"
LISTMONK_API_PASSWORD="listmonk_secure_password"

# ============================================================================
# ZEROPS QUEUE & NATS INFRASTRUCTURE
# ============================================================================
VALKEY_CONNECTION_STRING="redis://cache:6379"
DIRECTUS_URL="http://directus:8055"
DIRECTUS_STATIC_TOKEN="..."
NATS_URL="nats://nats:4222"
```

---

## 4. Third-Party Console Setup Runbooks

### 🟠 Runbook 1: Amazon SES v2 (`console.aws.amazon.com/ses`)
1. Log in to [AWS SES Management Console](https://console.aws.amazon.com/ses) in `us-east-1`.
2. Go to **Verified Identities** $\to$ **Create Identity** $\to$ Select **Domain**.
3. Under **DKIM**, select **Easy DKIM** with **RSA 2048-bit** key length.
4. Add generated DKIM `CNAME` records to Cloudflare DNS.
5. Add SPF and DMARCbis TXT records.
6. Request Production Access to exit sandbox mode.

---

### 🟣 Runbook 2: Zoho ZeptoMail (`zeptomail.zoho.com`)
1. Log in to [Zoho ZeptoMail Console](https://zeptomail.zoho.com).
2. Create a Mail Agent (e.g. `Production Mail Agent`).
3. In **Domains**, add domain and configure DNS records (SPF, DKIM, Bounce CNAME).
4. Copy the **Send Mail Token** (`Zoho-enczapikey wSsVR61...==`) into `ZEPTOMAIL_SEND_MAIL_TOKEN` in Zerops.

---

## 5. BullMQ Rate-Limited Dispatcher Worker

```typescript
import { Worker, Job } from "bullmq";
import Redis from "ioredis";
import { getAutoConfiguredDispatcher, UnifiedEmailPayload } from "../assets/email_dispatcher";

const connection = new Redis(process.env.VALKEY_CONNECTION_STRING || "redis://cache:6379", {
  maxRetriesPerRequest: null,
  enableReadyCheck: false
});

export const emailWorker = new Worker(
  "emailDispatchQueue",
  async (job: Job<UnifiedEmailPayload>) => {
    console.log(`[Email Worker] Processing email delivery for ${job.data.to.join(", ")}`);
    const dispatcher = getAutoConfiguredDispatcher();
    try {
      return await dispatcher.send(job.data);
    } catch (error: any) {
      if (error?.status === 429) {
        await emailWorker.rateLimit(5000);
        throw Worker.RateLimitError();
      }
      throw error;
    }
  },
  {
    connection,
    concurrency: 5,
    limiter: {
      max: 10,       // 10 emails maximum
      duration: 1000 // per 1 second (1000ms)
    }
  }
);
```

---

## 6. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with `email-marketing` must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All email API calls must use explicit timeouts (`timeout 10s curl -f ...`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all lingering email queue workers using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * SMTP / API Ping check: Verify relay connectivity with status 200.
* **Circuit Breaker Policy**: If primary provider returns 429 or 500, BullMQ worker automatically fails over to secondary relay (e.g. AWS SES v2 or Resend).
