# Checkout Funnels: Infrastructure, Webhook Security & Console Runbooks (v2.0)

This manual provides production-grade infrastructure blueprints, environment variable specifications for all 5 payment gateways, third-party dashboard configuration runbooks, and the Fractal CoHaLo operational harness for `checkout-funnels` running in Zerops.

---

## 1. Environment Variables Reference Dictionary

```ini
# ============================================================================
# WOMPI COLOMBIA
# ============================================================================
WOMPI_PUBLIC_KEY="pub_prod_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
WOMPI_PRIVATE_KEY="prv_prod_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
WOMPI_INTEGRITY_SECRET="prod_integrity_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
WOMPI_EVENTS_SECRET="prod_events_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# ============================================================================
# EPAYCO COLOMBIA & LATAM
# ============================================================================
EPAYCO_PUBLIC_KEY="49xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
EPAYCO_PRIVATE_KEY="c8xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
EPAYCO_P_KEY="82xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
EPAYCO_P_CUST_ID_CLIENTE="12345"
EPAYCO_TEST="false"

# ============================================================================
# DLOCAL GO (MULTI-COUNTRY LATAM)
# ============================================================================
DLOCAL_GO_API_KEY="dg_live_xxxxxxxxxxxxxxxx"
DLOCAL_GO_SECRET_KEY="dg_sec_xxxxxxxxxxxxxxxx"
DLOCAL_GO_ENV="live"

# ============================================================================
# STRIPE GLOBAL
# ============================================================================
STRIPE_SECRET_KEY="$STRIPE_SECRET_KEY"
STRIPE_PUBLISHABLE_KEY="pk_test_placeholder_key"
STRIPE_WEBHOOK_SECRET="whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# ============================================================================
# MERCADO PAGO LATAM
# ============================================================================
MERCADOPAGO_ACCESS_TOKEN="APP_USR-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
MERCADOPAGO_PUBLIC_KEY="APP_USR-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
MERCADOPAGO_WEBHOOK_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# ============================================================================
# META CONVERSIONS API (CAPI)
# ============================================================================
META_PIXEL_ID="123456789012345"
META_CAPI_ACCESS_TOKEN="EAAxxxx..."
```

---

## 2. Third-Party Console Setup Runbooks

### 🟠 Runbook 1: Wompi Colombia (`comercios.wompi.co`)
1. Log in to [Wompi Dashboard](https://comercios.wompi.co).
2. Go to **Desarrolladores** $\to$ Copy **Llave Pública** and **Llave Privada**.
3. Under **Seguridad**, generate the **Secreto de Integridad** for SHA-256 signatures.
4. In **Webhooks**, set URL: `https://api.yourdomain.com/webhooks/wompi` and copy **Event Secret**.

---

### 🟢 Runbook 2: ePayco (`dashboard.epayco.com`)
1. Log in to [ePayco Dashboard](https://dashboard.epayco.com).
2. Go to **Integraciones** $\to$ **Llaves Secretas**:
   - Copy **P_CUST_ID_CLIENTE**, **P_KEY**, **PUBLIC_KEY**, and **PRIVATE_KEY**.
3. In **Propiedades del Comercio** $\to$ **URL de Respuesta** set `https://yourdomain.com/checkout/response`.
4. In **URL de Confirmación** set `https://api.yourdomain.com/webhooks/epayco` (Method: POST).

---

### 🟣 Runbook 3: dLocal Go (`dlocalgo.com`)
1. Log in to [dLocal Go Dashboard](https://dashboard.dlocalgo.com).
2. Navigate to **Developers** $\to$ **API Keys**.
3. Copy **API Key** and **Secret Key**.
4. Configure Webhooks to `https://api.yourdomain.com/webhooks/dlocal`.

---

### 🔵 Runbook 4: Stripe (`dashboard.stripe.com`)
1. Log in to [Stripe Dashboard](https://dashboard.stripe.com).
2. Go to **Developers** $\to$ **API Keys** $\to$ Copy **Publishable Key** and **Secret Key**.
3. In **Webhooks** $\to$ **Add Destination** $\to$ URL: `https://api.yourdomain.com/webhooks/stripe`.
4. Select events (`checkout.session.completed`, `payment_intent.succeeded`) $\to$ Reveal and copy **Signing Secret** (`whsec_...`).

---

### 🟡 Runbook 5: Mercado Pago (`mercadopago.com/developers`)
1. Log in to [Mercado Pago Developers](https://www.mercadopago.com/developers).
2. Go to **Tus integraciones** $\to$ Select application.
3. In **Credenciales de producción**, copy **Public Key** and **Access Token**.
4. In **Notificaciones Webhooks**, configure URL: `https://api.yourdomain.com/webhooks/mercadopago` and copy signature secret.

---

## 3. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with `checkout-funnels` must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All gateway API calls and webhook handlers must use explicit timeouts (`timeout 10s curl -f ...`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all background monitoring scripts using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Gateway ping check: `curl -s -o /dev/null -w "%{http_code}" https://production.wompi.co/v1/merchants/pub_prod_test` $\implies$ Expected HTTP status.
* **Circuit Breaker Policy**: If the primary gateway (e.g. Wompi) suffers an outage or returns 500/503 errors, dynamically route transactions to secondary fallback gateways (e.g. ePayco or Stripe).
