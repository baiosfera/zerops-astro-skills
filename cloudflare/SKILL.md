---
name: cloudflare
description: "Trigger: cloudflare, cloudflare api, turnstile, dns sync, purge cache, ssl strict, edge cdn, waf skip rule, acme challenge, dmarc rfc 9989, cloudflared tunnel. Manage Cloudflare API v4, Turnstile anti-bot, WAF rules, SSL Full Strict, Edge CDN & DNS mesh in Zerops."
license: MIT
metadata:
  author: "gentleman-programming"
  version: "2.0"
---

# Cloudflare — Perimeter Ingress, Anycast DNS, WAF & Turnstile (v2.0)

## Activation Contract
Activate when provisioning or automating domains, DNS records (**A**, **AAAA**, **CNAME**, **TXT**, **MX**), Turnstile anti-bot in Astro, email authentication (SPF, DKIM, RFC 9989 DMARCbis), Edge CDN cache purging, SSL/TLS **Full (Strict)**, WAF rulesets, or Zero Trust tunnels (`cloudflared`) in Zerops.

## Hard Rules
- **SSL/TLS Full (Strict)**: Always enforce `ssl: strict` on Cloudflare zones pointing to Zerops. Never use "Flexible" mode to prevent redirect loops.
- **Proxy vs DNS-Only**: Web endpoints (Astro, Directus, WhatsApp) use `proxied: true`. Mail records (SPF, DKIM, DMARC, MX) MUST use `proxied: false`.
- **WAF ACME Bypass**: Configure a WAF Skip Rule for `/.well-known/acme-challenge/*` for Let's Encrypt renewals on Zerops L7 balancers.
- **Turnstile Verification**: Astro checkout and login forms MUST verify Turnstile tokens server-side via `siteverify`.
- **Fractal CoHaLo**: Enforce hygiene (`timeout 10s`), wait (`WaitMsBeforeAsync: 10000`), zero orphans (`manage_task action="kill"`), sensor (`dig +short @1.1.1.1`).
- **Zero Deletion**: Consult [`references/usage.md`](file:///var/www/.agents/skills/cloudflare/references/usage.md) and [`references/infra.md`](file:///var/www/.agents/skills/cloudflare/references/infra.md) for full lossless APIs.

## Decision Gates

| Task / Objective | Action / Protocol | Reference / Asset |
|---|---|---|
| 4D Matrix & Comparison | Cloudflare API v4 vs CloudFront, Fastly, Nginx | [`references/usage.md#1-4d-comparative-architectural-matrix`](file:///var/www/.agents/skills/cloudflare/references/usage.md) |
| Programmatic API v4 Client | Resolve Zone ID, DNS CRUD, Edge cache purge | [`references/usage.md#2-programmatic-cloudflare-client-usage-typescript`](file:///var/www/.agents/skills/cloudflare/references/usage.md) |
| Turnstile Anti-Bot Defense | Astro `<TurnstileWidget />` & server verification | [`references/usage.md#3-anti-bot-defense-with-cloudflare-turnstile-0-frictionless-ux`](file:///var/www/.agents/skills/cloudflare/references/usage.md) |
| WAF Rules & ACME Bypass | Let's Encrypt renewal bypass rule & rate limiting | [`references/usage.md#4-waf-custom-rulesets--security-policies-for-zerops`](file:///var/www/.agents/skills/cloudflare/references/usage.md) |
| Edge Cache & Dynamic Purge | Immutable asset caching (`/_astro/*`) & API purge | [`references/usage.md#5-edge-cache-rules--dynamic-purging`](file:///var/www/.agents/skills/cloudflare/references/usage.md) |
| Email Deliverability (RFC 9989)| Strict DMARCbis, DKIM & SPF records for Listmonk | [`references/usage.md#6-email-deliverability-suite-rfc-9989-dmarcbis`](file:///var/www/.agents/skills/cloudflare/references/usage.md) |
| API Token RBAC Permissions | Minimal privilege token setup in Dashboard | [`references/infra.md#1-cloudflare-api-token-permissions-rbac-minimum-privilege`](file:///var/www/.agents/skills/cloudflare/references/infra.md) |
| SSL/TLS Full Strict Setup | L7 balancer termination & redirect prevention | [`references/infra.md#2-hard-security-invariant-ssltls-full-strict-mode`](file:///var/www/.agents/skills/cloudflare/references/infra.md) |
| Zero Trust Tunnels (`cloudflared`) | Private tunnel setup for internal services | [`references/infra.md#4-cloudflare-zero-trust-tunnels-cloudflared-in-zerops`](file:///var/www/.agents/skills/cloudflare/references/infra.md) |
| Physical Validation Sensor | Attest skill structure, frontmatter, tokens & links | [`scripts/cloudflare-validate.sh`](file:///var/www/.agents/skills/cloudflare/scripts/cloudflare-validate.sh) |

## Execution Steps
1. Configure `CLOUDFLARE_API_TOKEN` with Zone permissions in Zerops environment.
2. Execute `bun scripts/sync-dns.ts` to idempotently synchronize the DNS mesh.
3. Configure Cloudflare WAF Skip Rule for `/.well-known/acme-challenge/*`.
4. Enforce SSL/TLS **Full (Strict)** mode on the zone settings.
5. Embed `<TurnstileWidget />` in Astro forms and verify tokens server-side in Astro Actions.
6. Verify DNS propagation and SSL status via physical sensor (`dig +short @1.1.1.1`).

## Output Contract
- Production DNS mesh and Edge CDN configured for Zerops services with SSL/TLS Full (Strict).
- Validated Turnstile bot protection, WAF ACME bypass rules, and passing physical validation sensors.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/cloudflare/references/usage.md) — 4D matrix, TypeScript client, Turnstile, WAF rules, Edge Cache, and 5 production patterns.
- [`references/infra.md`](file:///var/www/.agents/skills/cloudflare/references/infra.md) — API Token RBAC, SSL Full Strict topology, Zero Trust Tunnels, and CoHaLo harness.
- [`assets/cloudflare_production_recipes.json`](file:///var/www/.agents/skills/cloudflare/assets/cloudflare_production_recipes.json) — Production WAF rules, Turnstile handlers, and Cache rules.
- [`assets/cloudflare_client.ts`](file:///var/www/.agents/skills/cloudflare/assets/cloudflare_client.ts) — Full TypeScript REST v4 client with Zod validation.
- [`assets/dns_zod_schemas.ts`](file:///var/www/.agents/skills/cloudflare/assets/dns_zod_schemas.ts) — Strict Zod validation schemas for DNS records.
- [`scripts/sync-dns.ts`](file:///var/www/.agents/skills/cloudflare/scripts/sync-dns.ts) — Declarative DNS mesh synchronizer script.
- [`scripts/cloudflare-validate.sh`](file:///var/www/.agents/skills/cloudflare/scripts/cloudflare-validate.sh) — Deterministic quality & token validation sensor.
