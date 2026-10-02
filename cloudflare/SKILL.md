---
name: cloudflare
description: "Trigger: cloudflare, cloudflare api, turnstile, dns sync, purge cache, ssl strict, edge cdn, waf skip rule, acme challenge, dmarc rfc 9989, cloudflared tunnel. Manage Cloudflare API v4, Turnstile anti-bot, WAF rules, SSL Full Strict, Edge CDN & DNS mesh in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# `cloudflare` — Perimeter Ingress, Anycast DNS, WAF & Turnstile (v2.0)

## Activation Contract
Activate when automating domains, DNS records (**A**, **AAAA**, **CNAME**, **TXT**, **MX**, **SRV**, **CAA**), Turnstile anti-bot verification in Astro Actions, email authentication (SPF, DKIM, RFC 9989 DMARCbis), Edge CDN cache purging, SSL/TLS **Full (Strict)**, Cloudflare Rulesets API policies, or Zero Trust tunnels (`cloudflared`) in Zerops.

## Hard Rules & Technical Invariants
- **SSL/TLS Full (Strict)**: Configure zones pointing to Zerops Dedicated L7 Balancers with `ssl: strict`. Both edge and origin connections must terminate with valid certificates, eliminating redirect loops.
- **Proxy Partitioning**: Public HTTP web services use `proxied: true` for DDoS mitigation and edge caching. Mail records (SPF, DKIM, DMARC, MX) and ACME challenge endpoints must maintain `proxied: false`.
- **WAF Ruleset ACME & Webhook Bypass**: Deploy custom rules in `http_request_firewall_custom` skipping Super Bot Fight Mode and Rate Limiting for `/.well-known/acme-challenge/*` and `/api/webhooks/*`.
- **Turnstile Idempotency**: Verify Turnstile tokens server-side in Astro Actions passing a UUID v4 `idempotency_key` and client IP to prevent replay attacks and race conditions.
- **RFC 9989 DMARCbis Standard**: Author DMARC TXT records conforming to RFC 9989, omitting the obsoleted `pct` tag and enforcing non-existent domain policy (`np=reject`) and testing mode (`t=n`).

## Decision Gates

| Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| Programmatic API Client | REST v4 client with DNS CRUD & cache purge | [`assets/cloudflare_client.ts`](file:///var/www/.agents/skills/cloudflare/assets/cloudflare_client.ts) |
| Declarative Schemas | RFC 9989 DMARC & DNS topology Zod contracts | [`assets/dns_zod_schemas.ts`](file:///var/www/.agents/skills/cloudflare/assets/dns_zod_schemas.ts) |
| Turnstile Verification | Astro Action server-side validator with idempotency | [`assets/turnstile_validator.ts`](file:///var/www/.agents/skills/cloudflare/assets/turnstile_validator.ts) |
| Rulesets & Cache Rules | WAF skip rules & immutable edge caching templates | [`assets/cloudflare_production_recipes.json`](file:///var/www/.agents/skills/cloudflare/assets/cloudflare_production_recipes.json) |
| Declarative DNS Runner | Ingests topology manifest or environment variables | [`scripts/sync-dns.ts`](file:///var/www/.agents/skills/cloudflare/scripts/sync-dns.ts) |
| Implementation Manual | REST client usage, 4D matrix, and Action snippets | [`references/usage.md`](file:///var/www/.agents/skills/cloudflare/references/usage.md) |
| Topology & Ingress | Zerops L7 Balancer, Full Strict SSL & tunnels | [`references/infra.md`](file:///var/www/.agents/skills/cloudflare/references/infra.md) |
| Physical Validation | Deterministic integrity sensor | [`scripts/cloudflare-validate.sh`](file:///var/www/.agents/skills/cloudflare/scripts/cloudflare-validate.sh) |

## References
- [`references/usage.md`](file:///var/www/.agents/skills/cloudflare/references/usage.md) — REST API v4 usage, Turnstile in Astro Actions, Rulesets API, and RFC 9989.
- [`references/infra.md`](file:///var/www/.agents/skills/cloudflare/references/infra.md) — Zerops L7 SSL Full Strict setup, RBAC permissions, and cloudflared tunnels.
- [`assets/cloudflare_client.ts`](file:///var/www/.agents/skills/cloudflare/assets/cloudflare_client.ts) — TypeScript API client with batch DNS sync.
- [`assets/dns_zod_schemas.ts`](file:///var/www/.agents/skills/cloudflare/assets/dns_zod_schemas.ts) — RFC 9989 DMARC and DNS topology Zod schemas.
- [`assets/turnstile_validator.ts`](file:///var/www/.agents/skills/cloudflare/assets/turnstile_validator.ts) — Server-side Turnstile validation module.
- [`assets/cloudflare_production_recipes.json`](file:///var/www/.agents/skills/cloudflare/assets/cloudflare_production_recipes.json) — Production Ruleset templates.
- [`scripts/sync-dns.ts`](file:///var/www/.agents/skills/cloudflare/scripts/sync-dns.ts) — Declarative DNS synchronization runner.
- [`scripts/cloudflare-validate.sh`](file:///var/www/.agents/skills/cloudflare/scripts/cloudflare-validate.sh) — Deterministic physical validator.
