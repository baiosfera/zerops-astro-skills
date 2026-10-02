# Cloudflare REST API v4, Turnstile, Ruleset Engine & Edge Ingress Manual (v2.0)

> **SSoT Reference Document:** `.agents/skills/cloudflare/references/usage.md`  
> **Scope:** REST API v4 programmatic operations, Turnstile anti-bot verification with idempotency in Astro 5 Actions, modern Cloudflare Rulesets API, Edge Cache configuration, and RFC 9989 DMARCbis deliverability.

---

## 1. 4D Comparative Architectural Matrix

| Dimension | Cloudflare API v4 & Edge (Target) | AWS CloudFront + Route53 | Fastly Edge Cloud | Nginx / Traefik Self-Hosted |
|---|---|---|---|---|
| **DNS Resolution Latency** | **< 10 ms Anycast Global** | ~20–40 ms | ~15–30 ms | Dependent on single host (~50–150ms) |
| **DDoS & L3/L4/L7 WAF** | **Unlimited Unmetered Edge Engine** | Billed per rule and request | High bandwidth cost | Consumes host CPU & network bandwidth |
| **Bot Protection** | **Turnstile (Invisible / Managed UX)** | AWS WAF Bot Control (Expensive) | Fastly Bot Management | Self-hosted visual captchas |
| **SSL/TLS Architecture** | **Full (Strict) with Origin Certs** | ACM Certificate Manager | TLS Certificates | Certbot on host |
| **Ruleset Configuration** | **Cloudflare Rulesets API Engine** | AWS WAF / CloudFront Functions | VCL Edge Dictionaries | Complex Nginx rewrite files |
| **Zerops Suitability** | **100% Native with L7 Balancers** | Requires external proxying | Requires external proxying | Complex to scale across containers |

---

## 2. Programmatic Client Usage (TypeScript)

```typescript
import { getAutoConfiguredCloudflareClient } from "../assets/cloudflare_client";

const client = getAutoConfiguredCloudflareClient();

// 1. Resolve Zone ID for target domain
const zoneId = await client.getZoneId("example.com");

// 2. Synchronize Proxied CNAME Record
await client.syncDnsRecord(zoneId, {
  type: "CNAME",
  name: "app",
  content: "origin-app.example.zerops.app",
  proxied: true,
  ttl: 1, // 1 = Automatic TTL
  comment: "Application Ingress on Zerops"
});

// 3. Enforce Full Strict SSL and Always Use HTTPS
await client.setSslModeStrict(zoneId);
await client.enableAlwaysUseHttps(zoneId);
```

---

## 3. Server-Side Turnstile Validation in Astro 5 Actions

Turnstile tokens are verified server-side inside Astro 5 Actions (`defineAction`) to protect contact forms, checkouts, and lead generation without intrusive visual captchas:

```typescript
// src/actions/contact.ts
import { defineAction } from "astro:actions";
import { z } from "zod";
import { validateTurnstileToken } from "cloudflare-skill/assets/turnstile_validator";

export const server = {
  submitContact: defineAction({
    accept: "form",
    input: z.object({
      name: z.string().min(2),
      email: z.string().email(),
      message: z.string().min(10),
      "cf-turnstile-response": z.string().min(1),
    }),
    handler: async (input, context) => {
      // 1. Extract remote client IP from Cloudflare header
      const clientIp = context.request.headers.get("cf-connecting-ip") || undefined;

      // 2. Validate token with UUID v4 idempotency protection
      const turnstileResult = await validateTurnstileToken({
        token: input["cf-turnstile-response"],
        remoteIp: clientIp,
        timeoutMs: 4000,
      });

      if (!turnstileResult.success) {
        throw new Error(`Turnstile verification failed: ${turnstileResult["error-codes"].join(", ")}`);
      }

      return { success: true, verifiedAt: turnstileResult.challenge_ts };
    },
  }),
};
```

---

## 4. Modern Cloudflare Rulesets API Engine

Legacy Page Rules are deprecated in Cloudflare. All perimeter controls must use the Cloudflare Rulesets API:

### A. WAF Skip Rule for Let's Encrypt ACME HTTP-01 Challenges
Phase: `http_request_firewall_custom`
```json
{
  "action": "skip",
  "action_parameters": {
    "phases": ["http_ratelimit", "http_request_sbfm"],
    "products": ["bic", "hot", "rateLimit", "securityLevel", "zoneLockdown"]
  },
  "expression": "http.request.uri.path starts_with \"/.well-known/acme-challenge/\"",
  "description": "Bypass Bot Defense & Rate Limiting for ACME HTTP-01 Challenges",
  "enabled": true
}
```

### B. Machine-to-Machine Inbound Webhook Bypass
Phase: `http_request_firewall_custom`
```json
{
  "action": "skip",
  "action_parameters": {
    "phases": ["http_ratelimit", "http_request_sbfm"],
    "products": ["bic", "rateLimit", "securityLevel"]
  },
  "expression": "http.request.uri.path starts_with \"/api/webhooks/\"",
  "description": "Bypass Bot Fight Mode for External Webhooks (Payment, Messaging, CI)",
  "enabled": true
}
```

### C. Edge Cache Rules for Immutable Assets (`/_astro/*`)
Phase: `http_request_cache_settings`
```json
{
  "action": "set_cache_settings",
  "action_parameters": {
    "cache": true,
    "edge_ttl": { "mode": "override_origin", "default": 31536000 },
    "browser_ttl": { "mode": "override_origin", "default": 31536000 }
  },
  "expression": "http.request.uri.path starts_with \"/_astro/\" or (http.request.uri.path.extension in {\"woff2\" \"webp\" \"avif\" \"png\" \"svg\"})",
  "description": "Cache Immutable Astro Bundles and Static Assets for 1 Year",
  "enabled": true
}
```

---

## 5. RFC 9989 DMARCbis Email Authentication Standard

The IETF RFC 9989 standard (published May 2026) officially obsoletes RFC 7489.

### Key Changes Enforced:
1. **`pct` Tag Removed**: Percentage sampling (e.g. legacy pct tag) is officially obsoleted and must not be used in new DMARC policies.
2. **`np` Tag (Non-Existent Subdomain Policy)**: Protects against spoofing on uncreated subdomains (e.g. `np=reject`).
3. **`t` Tag (Testing Mode)**: Explicit testing indicator (`t=y` or `t=n`).

### Production RFC 9989 DMARC TXT Record Example
```text
Name: _dmarc.example.com
Type: TXT
TTL: 1 (Auto)
Content: v=DMARC1; p=reject; sp=reject; np=reject; t=n; rua=mailto:dmarc-reports@example.com;
```
