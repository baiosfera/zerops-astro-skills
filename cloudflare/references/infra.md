# Cloudflare & Zerops DNS Infrastructure, Security & Tunnels Manual (v2.0)

This manual provides production-grade infrastructure blueprints, API Token RBAC configuration, SSL/TLS Full (Strict) termination architecture on Zerops L7 Dedicated Balancers, WAF ruleset policies, Cloudflare Zero Trust Tunnels (`cloudflared`), and the Fractal CoHaLo operational harness for Cloudflare.

---

## 1. Cloudflare API Token Permissions (RBAC Minimum Privilege)

To generate the API Token in [Cloudflare Dashboard](https://dash.cloudflare.com/profile/api-tokens):

1. Navigate to **My Profile** $\to$ **API Tokens** $\to$ Click **Create Custom Token**.
2. Configure the following granular permissions:
   - `Zone` $\to$ `DNS` $\to$ **Edit**
   - `Zone` $\to$ `Zone` $\to$ **Read**
   - `Zone` $\to$ `Zone Settings` $\to$ **Edit**
   - `Zone` $\to$ `Cache Purge` $\to$ **Purge**
   - `Zone` $\to$ `WAF` $\to$ **Edit**
3. Set **Zone Resources** to `Include` $\to$ `Specific zone` (select your production domain).
4. Set **Client IP Address Filtering** to your Zerops project egress IP range (optional).
5. Copy the generated token and inject it into Zerops as `CLOUDFLARE_API_TOKEN`.

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
                                                 │ Astro / Directus LXC │
                                                 └──────────────────────┘
```

> [!WARNING]
> **NEVER use SSL "Flexible" mode.**
> Flexible mode causes infinite HTTP 301/302 redirect loops because Zerops L7 balancers force HTTPS on port 443 while Cloudflare connects over insecure HTTP port 80. Always configure SSL to **Full (strict)**.

---

## 3. Let's Encrypt / ACME HTTP-01 WAF Exception Rule

When Zerops provisions or renews Let's Encrypt certificates for custom domains behind Cloudflare:

1. In Cloudflare Dashboard, go to **Security** $\to$ **WAF** $\to$ **Custom Rules** $\to$ Click **Create rule**.
2. Configure the rule:
   - **Rule Name**: `Allow Let's Encrypt ACME Validation`
   - **Field**: `URI Path` $\to$ **Operator**: `starts with` $\to$ **Value**: `/.well-known/acme-challenge/`
   - **Action**: `Skip` $\to$ Check **All remaining security rules**.
3. Save and deploy the rule.

---

## 4. Cloudflare Zero Trust Tunnels (`cloudflared`) in Zerops

To access internal Zerops microservices (Directus Admin, n8n, databases) securely without opening public ports:

```yaml
# import.yaml snippet for cloudflared tunnel container
services:
  - hostname: cftunnel
    type: ubuntu@22.04
    prepareCommands:
      - curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
      - sudo dpkg -i cloudflared.deb
    start: cloudflared tunnel run --token ${CLOUDFLARE_TUNNEL_TOKEN}
```

---

## 5. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with Cloudflare must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All DNS queries and API inquiries must use explicit timeouts (`timeout 10s dig +short @1.1.1.1 yourdomain.com`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all background monitoring scripts using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * DNS Propagation check: `dig +short @1.1.1.1 api.yourdomain.com` $\implies$ Expected: CNAME or IPv4.
  * SSL Verification: `curl -sIv https://yourdomain.com 2>&1 | grep "SSL certificate verify ok"`.
* **Circuit Breaker Policy**: If Cloudflare returns `429 Too Many Requests` or `10000 Authentication Error`, retry up to 2 times with exponential backoff (2s, 4s). If failure persists, trigger F1 clarification gate to verify `CLOUDFLARE_API_TOKEN`.
