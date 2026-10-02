# Cloudflare & Zerops DNS Infrastructure, Security & Tunnels Manual (v2.0)

> **SSoT Reference Document:** `.agents/skills/cloudflare/references/infra.md`  
> **Scope:** Cloudflare API Token RBAC configuration, SSL/TLS Full (Strict) termination architecture on Zerops Dedicated L7 Balancers, Cloudflare Zero Trust Tunnels (`cloudflared`), and environment variables.

---

## 1. Cloudflare API Token Permissions (RBAC Minimum Privilege)

In [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens), create a custom token with minimum necessary permissions:
- `Zone` $\to$ `DNS` $\to$ **Edit**
- `Zone` $\to$ `Zone` $\to$ **Read**
- `Zone` $\to$ `Zone Settings` $\to$ **Edit**
- `Zone` $\to$ `Cache Purge` $\to$ **Purge**
- `Zone` $\to$ `WAF` $\to$ **Edit**

Scope the token to `Include` $\to$ `Specific zone` (your target domain). Inject the token into Zerops environment variables as `CLOUDFLARE_API_TOKEN`.

---

## 2. Hard Security Invariant: SSL/TLS Full (Strict) Mode

```
┌─────────────────┐       HTTPS (Port 443)       ┌──────────────────────┐
│ Browser/Client  │ ───────────────────────────▶ │ Cloudflare Edge CDN  │
└─────────────────┘                              └──────────┬───────────┘
                                                            │
                                                            │ HTTPS Full (Strict) Port 443
                                                            ▼
                                                 ┌──────────────────────┐
                                                 │ Zerops L7 Balancer   │
                                                 └──────────┬───────────┘
                                                            │
                                                            │ Private Mesh
                                                            ▼
                                                 ┌──────────────────────┐
                                                 │ Application LXC      │
                                                 └──────────────────────┘
```

1. **Full (Strict) Requirement:** Both the edge connection (Client to Cloudflare) and the origin connection (Cloudflare to Zerops L7 Balancer) MUST terminate with valid TLS certificates.
2. **Zero Infinite Redirect Loops:** Flexible mode terminates SSL at Cloudflare and requests HTTP (port 80) to origin. When the origin issues a 301 redirect to HTTPS, an infinite redirect loop (`ERR_TOO_MANY_REDIRECTS`) occurs. Full (Strict) prevents this defect.

---

## 3. Cloudflare Zero Trust Ingress Tunnels (`cloudflared`) on Zerops

For private internal administrative microservices (e.g. databases, internal telemetry) that must not expose public IPv4/IPv6 addresses, deploy a `cloudflared` daemon container on Zerops:

```yaml
# zerops.yaml for dedicated cloudflared service
zerops:
  - setup: tunnel
    run:
      base: ubuntu@24.04
      prepareCommands:
        - curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        - dpkg -i cloudflared.deb && rm cloudflared.deb
      start: cloudflared tunnel run --token ${TUNNEL_TOKEN}
```

---

## 4. Required Environment Variables

```ini
# ============================================================================
# CLOUDFLARE REST API V4
# ============================================================================
CLOUDFLARE_API_TOKEN="cf-token-with-dns-edit-permissions"
CLOUDFLARE_ZONE_ID="023e105f4ecef8ad9ca31a8372d0c353"
CLOUDFLARE_BASE_DOMAIN="example.com"

# ============================================================================
# CLOUDFLARE TURNSTILE (ASTRO 5 ACTIONS)
# ============================================================================
PUBLIC_TURNSTILE_SITE_KEY="0x4AAAAAA..." # Client-side widget key
TURNSTILE_SECRET_KEY="0x4AAAAAA..."      # Server-side validation secret

# ============================================================================
# ZEROPS L7 BALANCER INGRESS
# ============================================================================
ZEROPS_DEDICATED_IPV4="192.0.2.1"
ZEROPS_DEDICATED_IPV6="2001:db8::1"
```
