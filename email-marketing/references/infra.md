# Email Marketing: Infrastructure, Zerops Topology & Console Runbooks (v3.0)

This manual provides production-grade infrastructure blueprints, DNS deliverability records (SPF, DKIM 2048-bit, DMARCbis RFC 9989, MTA-STS RFC 8461, TLS-RPT RFC 8460, BIMI), BullMQ rate-limited queue workers with stateful Circuit Breaker, and the Fractal CoHaLo operational harness for `email-marketing` running in Zerops.

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
│   │ - Circuit Breaker state cache (cooldown keys)    │                                                 │
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

## 2. 2026 Deliverability & Cryptographic DNS Standards

### 2.1. Spam Complaint Thresholds (Google Postmaster Tools & Yahoo Sender Hub)
* **Optimal Target:** Spam Complaint Rate **< 0.10%** (max 1 complaint per 1,000 sent emails).
* **Alert Zone:** 0.10% – 0.29% (progressive inbox deprioritization and greylisting).
* **Hard Block:** **$\ge$ 0.30%** (immediate rejection or universal SPAM folder placement).

### 2.2. DMARCbis (RFC 9989, RFC 9990, RFC 9991)
Published in 2026 as formal Proposed Standards:
* **`pct` Tag:** Permanently deprecated and removed.
* **`t` Tag (Testing):** Set to `t=n` for production enforcement. Replaces `pct=0`.
* **`np` Tag (Non-Existent Domain Policy):** Mandatory protection against subdomain dictionary attacks. Set to `np=reject`.
* **`psd` Tag (Public Suffix Domain):** Set to `psd=u` (unknown) or `psd=n` for sovereign organizational domains.
* **DNS Tree Walk:** Evaluates nested `_dmarc` records progressively to organizational root.

```dns
; Canonical DMARCbis RFC 9989 Record
_dmarc.yourdomain.com. IN TXT "v=DMARC1; p=quarantine; sp=quarantine; np=reject; adkim=r; aspf=r; t=n; rua=mailto:dmarc@yourdomain.com; ruf=mailto:dmarc-errors@yourdomain.com;"
```

### 2.3. DKIM (RFC 6376) & RSA 2048-Bit Floor
* 2048-bit RSA keys mandatory across all selectors (`s=`). Keys below 2048-bit are penalized by Google/Yahoo reputation engines.
* Ed25519 (RFC 8463) optional as secondary signature; RSA 2048 remains primary for legacy MTA compatibility.

### 2.4. MTA-STS (RFC 8461) & TLS-RPT (RFC 8460)
Guarantees encrypted transport and prevents STARTTLS stripping MITM attacks:
1. **DNS TXT for MTA-STS:**
   ```dns
   _mta-sts.yourdomain.com. IN TXT "v=STSv1; id=2026110201;"
   ```
2. **Policy File (`https://mta-sts.yourdomain.com/.well-known/mta-sts.txt`):**
   ```text
   version: STSv1
   mode: enforce
   mx: feedback-smtp.us-east-1.amazonses.com
   mx: mail.yourdomain.com
   max_age: 604800
   ```
3. **DNS TXT for TLS-RPT:**
   ```dns
   _smtp._tls.yourdomain.com. IN TXT "v=TLSRPTv1; rua=mailto:tls-reports@yourdomain.com;"
   ```

### 2.5. BIMI (Brand Indicators for Message Identification)
Displays verified brand logo in Gmail, Apple Mail, and Yahoo:
```dns
default._bimi.yourdomain.com. IN TXT "v=BIMI1; l=https://cdn.yourdomain.com/branding/logo-bimi.svg; a=https://cdn.yourdomain.com/branding/certificate.pem;"
```
* **Requirements:** DMARC in enforcement (`p=quarantine` or `p=reject`), SVG Tiny P/S strict format (no scripts, square aspect ratio), and Verified Mark Certificate (VMC) or Common Mark Certificate (CMC).

---

## 3. Amazon SES v2 & Custom MAIL FROM Specification

### 3.1. Envelope MAIL FROM Alignment
Default SES sending envelope uses `<id>@amazonses.com`, which breaks SPF alignment under DMARC `aspf=r`. A dedicated subdomin (`mail.yourdomain.com`) aligns the envelope:
1. **Subdomain MX Record:**
   ```dns
   mail.yourdomain.com. IN MX 10 feedback-smtp.us-east-1.amazonses.com.
   ```
2. **Subdomain SPF Record:**
   ```dns
   mail.yourdomain.com. IN TXT "v=spf1 include:amazonses.com ~all"
   ```
3. **Root Domain SPF Record:**
   ```dns
   yourdomain.com. IN TXT "v=spf1 include:amazonses.com include:zeptomail.net ~all"
   ```

### 3.2. Virtual Deliverability Manager (VDM) & SNS Event Destinations
* **VDM:** Programmatically enabled for predictive reputation routing, engagement tracking, and shared IP optimization.
* **Event Destinations:** All bounces and complaints route to an Amazon SNS Topic (`ses-deliverability-events`), which webhooks into Directus/PostgreSQL to atomically suppress failing addresses.

### 3.3. Critical Identity Precedence Gotcha (Individual Email vs Domain Identity)
* **The Trap:** If an individual email address (e.g. `mentor@yourdomain.com`) was verified in AWS SES *before* the domain identity (`yourdomain.com`), SES assigns individual identity settings higher precedence than domain settings.
* **The Failure Mode:** Individual email identities in SES do NOT automatically inherit the domain's `MailFromDomain`. When sending from `mentor@yourdomain.com`, SES falls back to `<id>@amazonses.com`, causing Gmail to display *"via amazonses.com"* or *"enviado por amazonses.com"* and failing DMARC SPF alignment.
* **The Resolution Protocol:**
  1. Inspect email identity attributes: `aws ses get-identity-mail-from-domain-attributes --identities mentor@yourdomain.com`
  2. If `MailFromDomain` is empty/null, set it explicitly:
     ```bash
     aws ses set-identity-mail-from-domain --identity "mentor@yourdomain.com" --mail-from-domain "mail.yourdomain.com" --behavior-on-mx-failure UseDefaultValue
     ```
  3. Alternatively, delete redundant individual email identities (`DeleteEmailIdentity`) to let the verified domain identity govern all addresses automatically.

### 3.4. Domain Verification Cache Reset Protocol
* **The Trap:** If domain verification is requested in SES before DNS records propagate to Cloudflare, SES records `ErrorType: HOST_NOT_FOUND` and enters an exponential backoff sleep (waiting 1 to 4 hours before the next poll).
* **The Fast-Recovery Poke:** Calling `VerifyDomainIdentity` and `VerifyDomainDkim` via API/CLI immediately flushes the `HOST_NOT_FOUND` error cache, resetting `LastCheckedTimestamp` to `null` and putting the domain at the front of the AWS validation queue for instant verification (< 60s).

### 3.5. Zero-Dollar Brand Avatar Strategy ($0 BIMI Alternative in Gmail)
* **The Problem:** Official BIMI with verified blue checkmarks in Gmail strictly requires a Verified Mark Certificate (VMC) or Common Mark Certificate (CMC), costing upwards of $1,000 USD/year.
* **The Sovereign Solution ($0 SaaS):**
  1. Go to `https://accounts.google.com/signup` in incognito mode.
  2. Select **"Use my current email address instead"** and enter the brand sender address (e.g. `contacto@brand.com` or `mentor@brand.com`). Complete email token verification.
  3. (Alternative for organizations: provision a **Google Cloud Identity Free** tenant supporting up to 50 users at zero cost).
  4. Navigate to `https://myaccount.google.com/personal-info` and upload the brand's logo / avatar as the profile picture.
  5. **Result:** Gmail and Google Workspace automatically associate the uploaded profile photo with every outbound message from that address, rendering the brand avatar in recipient inboxes across all Gmail clients for $0.

---

## 4. Environment Variables Reference Dictionary

```ini
# ============================================================================
# ZOHO ZEPTOMAIL (REST API v1.1)
# ============================================================================
ZEPTOMAIL_SEND_MAIL_TOKEN="Zoho-enczapikey wSsVR61...=="
ZEPTOMAIL_DEFAULT_FROM_EMAIL="noreply@yourdomain.com"
ZEPTOMAIL_DEFAULT_FROM_NAME="Store Notifications"
ZEPTOMAIL_BOUNCE_ADDRESS="bounce@bounce.yourdomain.com"
ZEPTOMAIL_REGION="com"

# ============================================================================
# AWS SES V2 (SDK v3 / IAM SigV4)
# ============================================================================
AWS_REGION="us-east-1"
AWS_ACCESS_KEY_ID="AKIA..."
AWS_SECRET_ACCESS_KEY="secret..."
AWS_SES_CONFIGURATION_SET="deliverability-set"
AWS_SES_DEFAULT_FROM="Store <noreply@yourdomain.com>"
AWS_SES_CUSTOM_MAIL_FROM="mail.yourdomain.com"

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
# ZEROPS QUEUE & VALKEY INFRASTRUCTURE
# ============================================================================
VALKEY_CONNECTION_STRING="redis://cache:6379"
DIRECTUS_URL="http://directus:8055"
DIRECTUS_STATIC_TOKEN="..."
NATS_URL="nats://nats:4222"
```

---

## 5. Third-Party Console Setup Runbooks

### 🟠 Runbook 1: Amazon SES v2 (`console.aws.amazon.com/ses`)
1. Log in to [AWS SES Management Console](https://console.aws.amazon.com/ses) in `us-east-1`.
2. Go to **Verified Identities** $\to$ **Create Identity** $\to$ Select **Domain**.
3. Under **DKIM**, select **Easy DKIM** with **RSA 2048-bit** key length.
4. Add the 3 generated DKIM `CNAME` records to Cloudflare DNS.
5. In **Custom MAIL FROM domain**, specify `mail.yourdomain.com`, add the MX and SPF records to Cloudflare.
6. Under **Configuration Sets**, create `deliverability-set` and configure Event Destinations for Bounces & Complaints to Amazon SNS.
7. Request Production Access to exit sandbox mode.

### 🟣 Runbook 2: Zoho ZeptoMail (`zeptomail.zoho.com`)
1. Log in to [Zoho ZeptoMail Console](https://zeptomail.zoho.com).
2. Create a Mail Agent (e.g. `Production Mail Agent`).
3. In **Domains**, add domain and configure DNS records (SPF, DKIM, Bounce CNAME).
4. Copy the **Send Mail Token** (`Zoho-enczapikey wSsVR61...==`) into `ZEPTOMAIL_SEND_MAIL_TOKEN` in Zerops.

---

## 6. BullMQ Rate-Limited Dispatcher Worker with Circuit Breaker

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

## 7. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with `email-marketing` must strictly comply with the Fractal CoHaLo standard:
* **Bounded Timeouts**: All email API calls must use explicit timeouts (`timeout 10s curl -f ...`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all lingering email queue workers using `manage_task action="kill"`.
* **Physical Sensor Attestation**: Execute `email-marketing-validate.sh` and `skills-suite-validate` with exit code 0 before completing turns.
* **Circuit Breaker Policy**: If primary provider fails with 429, 500, or 503, the dispatcher automatically opens the circuit and diverts traffic to secondary provider for 60 seconds.
