# `ghcicd`: CI/CD Infrastructure, Secret Management & Port Catalog Manual (v3.2)

This manual provides technical specifications for managing deployment tokens (`ZEROPS_TOKEN`), mapping service ports and environment URLs, preventing CI/CD race conditions, and executing the Fractal CoHaLo operational harness in Zerops.

---

## 1. Complete Service Port & URL Catalog

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Zerops Ecosystem Service, Port & Environment Catalog                                                   │
│                                                                                                        │
│ ┌──────────────┬──────────────┬─────────────┬────────────────────────────────┬───────────────────────┐ │
│ │ Service Name │ Runtime Base │ HTTP Port   │ Staging / Preview URL          │ Production URL        │ │
│ ├──────────────┼──────────────┼─────────────┼────────────────────────────────┼───────────────────────┤ │
│ │ **astro**    │ bun@1.3.9    │ 3000        │ https://stage.domain.com       │ https://domain.com    │ │
│ │ **directus** │ nodejs@24    │ 8055        │ https://cms-stage.domain.com   │ https://cms.domain.com│ │
│ │ **fastapi**  │ python@3.12  │ 8000        │ https://api-stage.domain.com   │ https://api.domain.com│ │
│ │ **evogo**    │ go@1.23      │ 8080        │ https://wa-stage.domain.com    │ https://wa.domain.com │ │
│ │ **nats**     │ nats@2.12    │ 8222 (:varz)│ Interno: nats:8222/varz        │ Interno: nats:8222    │ │
│ └──────────────┴──────────────┴─────────────┴────────────────────────────────┴───────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Secret Management: `ZEROPS_TOKEN` & Service IDs

To connect GitHub Actions with Zerops securely:

1. **Generate Zerops Access Token**:
   - Go to **Zerops GUI ➔ Settings ➔ Access Token Management**.
   - Generate a token with deployment permissions for the target project.
2. **Retrieve Service ID**:
   - Go to the service dashboard in Zerops ➔ Click three dots menu ➔ **Copy Service ID** (or extract from dashboard URL).
3. **Configure GitHub Repository Secrets**:
   - In GitHub: **Repository Settings ➔ Secrets and variables ➔ Actions ➔ New repository secret**.
   - Add:
     - `ZEROPS_TOKEN`: The access token from Step 1.
     - `ZEROPS_PROD_SERVICE_ID`: The production runtime service ID (Opción B Mandatoria).
     - `ZEROPS_STAGE_SERVICE_ID`: The staging runtime service ID (Solo si se habilita la capa opcional de Staging).

---

## 3. Agnostic Delivery Contract & Race Condition Shield

When adopting GitHub Actions:

* **Strict Prohibition**: Never leave automated branch webhooks enabled in the Zerops GUI while deploying via `.github/workflows/deploy.yaml`.
* **Action to Disconnect GUI Webhook**:
  1. Navigate to **Service Details ➔ Build, Deploy, Run Pipeline Settings**.
  2. Click **Stop automatic build trigger**.
  3. This removes the legacy webhook and prevents double builds.

---

## 4. Process Hygiene, Bounded Execution & Circuit Breakers (CoHaLo)

All operations with `ghcicd` must strictly comply with the Fractal CoHaLo standard:

* **Bounded Timeouts**: All Git and deployment CLI commands must use explicit timeouts (`timeout 10s git push origin main`).
* **Synchronous Wait Enforcement**: For CLI commands and status verifications, specify `WaitMsBeforeAsync: 10000`.
* **Zero Orphan Tasks**: Terminate all lingering processes using `manage_task action="kill"`.
* **Physical Sensor Attestation**:
  * Git auth check: `gh auth status` $\implies$ Exit 0.
  * Pipeline check: `zerops_verify targetService="<serviceHostname>"` $\implies$ Exit 0.
* **Circuit Breaker Policy**: If a GitHub Actions deployment fails twice consecutively, check build logs via `zerops_logs serviceHostname="<hostname>"` and verify `prepareCommands` in `zerops.yaml` before retrying.
