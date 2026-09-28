# Cloudflare REST API v4, Turnstile, WAF & Edge Ingress Manual (v2.0)

Cloudflare (`cloudflare`) is the enterprise perimeter security, Anycast DNS, Edge CDN, WAF, and DDoS mitigation engine for the Zerops sovereign stack. It ensures sub-10ms global DNS resolution, SSL/TLS Full (Strict) termination, Turnstile bot defense for Astro forms, and automated DNS synchronization.

This manual provides the comprehensive reference for REST API v4 client operations, Turnstile integration in Astro Actions, WAF rulesets for Let's Encrypt ACME renewals, Edge Cache Rules, and RFC 9989 DMARCbis deliverability.

---

## 1. 4D Comparative Architectural Matrix

| Dimension | Cloudflare API v4 & Edge (Target) | AWS CloudFront + Route53 | Fastly Edge Cloud | Nginx / Traefik Self-Hosted |
|---|---|---|---|---|
| **DNS Resolution Latency** | **< 10 ms Anycast Global** | ~20–40 ms | ~15–30 ms | Dependent on single host (~50–150ms) |
| **DDoS & L3/L4/L7 WAF** | **Unlimited Unmetered ($0 SaaS)** | Billed per rule and request | High bandwidth cost | Consumes host CPU & network bandwidth |
| **Bot Protection (Captcha)** | **Turnstile ($0 frictionless UX)** | AWS WAF Bot Control (Expensive) | Fastly Bot Management | Self-hosted slow captchas |
| **SSL/TLS Architecture** | **Full (Strict) with Let's Encrypt** | ACM Certificate Manager | TLS Certificates | Certbot on host |
| **Declarative API Sync** | **REST API v4 with granular RBAC** | AWS IAM / Complex CLI | Fastly API | Local configuration files |
| **Zerops Suitability** | **100% Native with L7 Balancers** | Requires external proxying | Requires external proxying | Complex to scale in container clusters |

---

## 2. Programmatic Cloudflare Client Usage (TypeScript)

```typescript
import { getAutoConfiguredCloudflareClient } from "../assets/cloudflare_client";

const client = getAutoConfiguredCloudflareClient();

// 1. Resolve Zone ID for target domain
const zoneId = await client.getZoneId("yourdomain.com");

// 2. Create or Update Proxied CNAME for Directus API Ingress
await client.createDnsRecord(zoneId, {
  type: "CNAME",
  name: "api",
  content: "directus-prod.app-123.zerops.app",
  proxied: true,
  ttl: 1, // 1 = Auto TTL (Cloudflare Edge)
  comment: "Directus API Ingress on Zerops"
});

// 3. Create Unproxied Mail Authentication TXT Record (SPF)
await client.createDnsRecord(zoneId, {
  type: "TXT",
  name: "@",
  content: "v=spf1 include:zeptomail.net ~all",
  proxied: false,
  ttl: 3600,
  comment: "SPF Record for ZeptoMail"
});

// 4. Purge CDN Edge Cache
await client.purgeCache(zoneId, true);
```

---

## 3. Anti-Bot Defense with Cloudflare Turnstile ($0 Frictionless UX)

Cloudflare Turnstile replaces invasive Google reCAPTCHA widgets with invisible, frictionless cryptographic challenges.

### A. Astro Turnstile Widget Component (`src/components/TurnstileWidget.astro`)

```astro
---
interface Props {
  siteKey?: string;
  theme?: "light" | "dark" | "auto";
}
const siteKey = Astro.props.siteKey || import.meta.env.PUBLIC_TURNSTILE_SITE_KEY;
const theme = Astro.props.theme || "auto";
---

<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>

<div
  class="cf-turnstile my-3"
  data-sitekey={siteKey}
  data-theme={theme}
  data-callback="onTurnstileSuccess"
></div>
```

### B. Server-Side Turnstile Verification in Astro Actions (`src/actions/index.ts`)

```typescript
import { defineAction, ActionError } from 'astro:actions';
import { z } from 'astro/zod';

export async function verifyTurnstile(token: string, remoteIp?: string): Promise<boolean> {
  const secretKey = process.env.TURNSTILE_SECRET_KEY;
  if (!secretKey) throw new Error("TURNSTILE_SECRET_KEY is missing in server environment.");

  const formData = new FormData();
  formData.append("secret", secretKey);
  formData.append("response", token);
  if (remoteIp) formData.append("remoteip", remoteIp);

  const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    body: formData,
  });

  const outcome = await res.json();
  return outcome.success === true;
}

export const server = {
  submitContactForm: defineAction({
    accept: 'json',
    input: z.object({
      name: z.string().min(2),
      email: z.string().email(),
      message: z.string().min(10),
      turnstileToken: z.string().min(1),
    }),
    handler: async (input, context) => {
      const clientIp = context.clientAddress;
      const isValid = await verifyTurnstile(input.turnstileToken, clientIp);
      
      if (!isValid) {
        throw new ActionError({
          code: 'BAD_REQUEST',
          message: 'Anti-bot verification failed. Please refresh and try again.',
        });
      }

      // Proceed with business logic (e.g. creating lead in Directus)
      return { success: true };
    }
  })
};
```

---

## 4. WAF Custom Rulesets & Security Policies for Zerops

### A. Let's Encrypt / ACME HTTP-01 WAF Bypass Rule (Mandatory)
When Zerops provisions or renews Let's Encrypt certificates, Cloudflare WAF must never block challenge validation:

* **Rule Expression**: `(http.request.uri.path starts_with "/.well-known/acme-challenge/")`
* **Action**: **Skip $\to$ All remaining security rules**.

### B. Rate Limiting & WhatsApp Webhook Exemption
* **Login & Admin Rate Limit**: Maximum 10 requests per minute per IP on `(http.request.uri.path eq "/auth/login")`.
* **WhatsApp Inbound Webhooks**: Exempt incoming webhook calls from WhatsApp gateways (`(http.request.uri.path starts_with "/webhooks/whatsapp")`) from challenge challenges.

---

## 5. Edge Cache Rules & Dynamic Purging

Configure Cloudflare Cache Rules to maximize CDN offloading while preserving real-time dynamics:

1. **Astro Immutable Static Assets**:
   * URI Path matches: `/_astro/*`
   * Edge TTL: **1 year (31536000s)**
   * Browser TTL: **1 year**
   * Cache Level: **Cache Everything**
2. **Directus Media Assets**:
   * URI Path matches: `/assets/*`
   * Edge TTL: **30 days**
   * Browser TTL: **7 days**
   * Serve Stale Content: **Enabled** (`stale-while-revalidate`)
3. **Dynamic API & SSR Pages**:
   * URI Path matches: `/api/*`, `/instance/*`, `/actions/*`
   * Cache Level: **Bypass Cache**

---

## 6. Email Deliverability Suite (RFC 9989 DMARCbis)

Automated DNS records required for high deliverability (Listmonk, Amazon SES, ZeptoMail):

```ini
# SPF Record (Root domain TXT)
Type: TXT | Name: @ | Content: "v=spf1 include:zeptomail.net ~all" | Proxied: false

# DKIM Key (DomainKey TXT)
Type: TXT | Name: zmail._domainkey | Content: "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC..." | Proxied: false

# DMARCbis Record (RFC 9989 Compliant Strict Policy)
Type: TXT | Name: _dmarc | Content: "v=DMARC1; p=reject; sp=reject; pct=100; rua=mailto:dmarc-reports@yourdomain.com" | Proxied: false

# MX Records
Type: MX  | Name: @ | Content: "feedback-smtp.us-east-1.amazonses.com" | Priority: 10 | Proxied: false
```

---

## 7. 5 Production Patterns in Zerops

### Pattern 1: Declarative Mesh DNS Synchronization
Idempotent script `scripts/sync-dns.ts` synchronizes the entire multi-service topology (Astro, Directus, Evolution Go, sGTM, Mail) in one execution.

### Pattern 2: Astro Checkout Form Shielding with Turnstile
Protects sensitive checkout and registration forms from automated credential stuffing and bot spam without user friction.

### Pattern 3: Automated Let's Encrypt Renewal WAF Bypass
Ensures zero-downtime SSL certificate renewals on Zerops L7 dedicated balancers without false-positive Cloudflare WAF blocks.

### Pattern 4: Dynamic Edge CDN Purge in CI/CD Pipeline
Automatically triggers `POST /zones/{zone_id}/purge_cache` upon successful GitHub Actions deploy of Astro.

### Pattern 5: Private Zero Trust Access Tunnel (`cloudflared`)
Establishes a private tunnel from Zerops to Cloudflare Zero Trust, allowing developers to access internal Directus Studio or n8n instances without opening public HTTP ports.

---

## 8. Anti-Patterns & Common Gotchas

1. **Using SSL "Flexible" Mode**: Causes infinite HTTP 301/302 redirection loops because Zerops balancers enforce HTTPS. Always set SSL to **Full (strict)**.
2. **Enabling Cloudflare Proxy on Mail / ACME Records**: Setting `proxied: true` on MX, SPF, DKIM, or ACME challenge records breaks email deliverability and SSL verification.
3. **Hardcoding Cloudflare API Tokens**: Never commit API tokens to git repositories. Always inject via `CLOUDFLARE_API_TOKEN` in Zerops environment.
