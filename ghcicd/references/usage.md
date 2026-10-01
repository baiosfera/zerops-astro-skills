# `ghcicd`: Universal CI/CD, Git, GitHub Actions & Zerops Delivery Manual (v2.0)

`ghcicd` is the sovereign continuous integration, continuous delivery (CI/CD), Git repository synchronization, and automated deployment engine for Zerops. Operating under the **Agnostic Delivery Contract**, it establishes a deterministic strategy across **GitHub Actions (`zeropsio/actions@v1.0.2`)**, **`gh` CLI authentication**, **`zcli` push**, and native **`zerops_deploy` / `zerops_dev_server`** MCP tools.

---

## 0. Modelo Mental 4D de Git y Disciplina Anti-Commit-Spam

Para evitar confusiones entre el guardado local y el despliegue a la nube, Git opera estrictamente en 4 áreas físicas:

```
┌──────────────────┐       git add        ┌──────────────────┐      git commit      ┌──────────────────┐       git push       ┌──────────────────┐
│  Working Tree    │ ───────────────────> │  Staging Area    │ ───────────────────> │ Local Repository │ ───────────────────> │ Remote (GitHub)  │
│ (/var/www/repo/) │                      │ (Índice temporal)│                      │ (.git/objects/)  │                      │ (github.com/...) │
└──────────────────┘ <─────────────────── └──────────────────┘                      └──────────────────┘                      └──────────────────┘
```

1. **Working Tree**: Archivos físicos editados en el disco local. Cero impacto en Git hasta ejecutar `git add`.
2. **Staging Area**: La aduana de preparación para el próximo commit atómico.
3. **Local Repository (`.git/`)**: La base de datos local inmutable en disco. Los commits aquí **no consumen minutos de CI/CD, no generan alertas ni tocan la nube**.
4. **Remote GitHub**: La sincronización remota que activa flujos de revisión (PR) y automatizaciones.

### A. La Regla de Oro Anti-Commit-Spam
- **Prohibición**: NUNCA ejecutar `git push origin main` tras cada micro-arreglo o commit atómico. Empujar cada commit satura los runners de GitHub Actions, ensucia el historial de auditoría y arriesga roturas en la rama principal.
- **Las 3 Estrategias Profesionales de Entrega**:
  1. **Feature Branch + Pull Request con Squash & Merge (Recomendada Enterprise)**:
     - Crear rama de trabajo: `git checkout -b fix/feature-name`.
     - Trabajar con commits atómicos locales: `git commit -m "fix(scope): atomic fix"`.
     - Empujar la rama a GitHub: `git push origin fix/feature-name`.
     - Abrir PR vía `gh`: `gh pr create --title "fix: description" --body "Details..."`.
     - Integrar a `main` aplastando commits de prueba: `gh pr merge --squash --delete-branch`.
  2. **Trunk-Based con Milestone Pushes**:
     - Acumular 3–5 commits locales atómicos bajo Conventional Commits en `main`.
     - Probar y certificar el hito completo con sensores físicos (`exit 0`).
     - Empujar en un único `git push origin main` todo el paquete consolidado.
  3. **Release Tagged GitOps (`v*`)**:
     - Desacoplar despliegues de los pushes a `main`. El workflow en GitHub Actions sólo se activa cuando se empuja un tag semántico (`git tag v1.0.1 && git push origin v1.0.1`).

### B. `gh` (CLI en Terminal) vs. GitHub Actions (Robot en la Nube)
- **`gh` CLI (`/usr/bin/gh`)**: Herramienta de consola en el contenedor ZCP. Se usa para operar GitHub sin navegador (crear PRs con `gh pr create`, hacer merge con `gh pr merge`). **No compila contenedores ni despliega código**.
- **GitHub Actions (`.github/workflows/deploy.yaml`)**: Motor de CI/CD que corre en la nube de GitHub. Requiere secrets (`ZEROPS_TOKEN`, `ZEROPS_SERVICE_ID`). Al recibir un push en `main` o un tag, llama a la API de Zerops (`zeropsio/actions@v1.0.2`) para compilar e iniciar el nuevo release.

### C. Arquitectura Canónica de Ambientes en Zerops: Multi-Servicio vs. Riesgos de Host Routing

Para el ciclo de vida `dev` -> `stage` -> `prod` en aplicaciones web personalizadas (`astro-web`):

1. **Modelo Canónico Multi-Servicio (Recomendado & Estándar de Producción)**:
   - Se aprovisionan dos servicios independientes en Zerops: `<service>-stage` y `<service>-prod`.
   - La rama `stage` despliega en `<service>-stage` (`<staging_domain>`) vía GitHub Actions con `ZEROPS_SERVICE_ID_STAGE`.
   - La rama `main` despliega en `<service>-prod` (`<app_domain>`) vía GitHub Actions con `ZEROPS_SERVICE_ID_PROD`.
   - *Aislamiento de Procesos Total*: Si un release experimental en `stage` falla o crashea, la tienda de producción (`prod`) sigue 100% activa.
   - *Aislamiento de Secretos*: Staging utiliza credenciales sandbox (Stripe Test, Directus Staging, mock webhooks) sin riesgo de tocar dinero real.
   - *Costo en Zerops*: En Bun (`bun@1.3.9`), un runtime Astro SSR consume apenas **~45 MB de RAM**. Dos contenedores consumen ~90 MB en total (costo marginal insignificante, centavos al mes).
   - *Frontera de Repositorios*: Este pipeline pertenece exclusivamente a los repositorios de aplicación web (`astro-web`), **NUNCA** a la plantilla chasis `zerops-astrobranding`.

2. **Advertencia de Seguridad: Antipatrón de Simular Staging en Runtime Único**:
   - Simular `stage` y `prod` en un solo contenedor inspeccionando cabeceras `Host` / `X-Forwarded-Host` en `middleware.ts` introduce graves riesgos arquitectónicos:
     * **Blast Radius Total**: Al compartir el proceso Bun/Node, un crash o excepción no controlada en stage derriba producción instantáneamente.
     * **Riesgo de Cache Poisoning (OWASP)**: Proxies de borde y CDNs (Cloudflare) pueden almacenar en caché respuestas generadas bajo contexto de staging y servirlas a usuarios de producción.
     * **Incompatibilidad con Ramas Git**: Es físicamente imposible probar una rama de Git sin haberla desplegado en el contenedor único de producción.
   - *Uso legítimo de Host-Routing*: Reservado únicamente para multi-tenancy de catálogo o multi-marca sobre un **mismo release estable**.

### D. Aprovisionamiento Autónomo de Secretos en GitHub (`gh secret set`)

Para que el pipeline de CI/CD funcione de forma 100% desatendida sin intervención manual en la interfaz web de GitHub:

```bash
# 1. Inyectar token de Zerops (con permisos de deploy)
gh secret set ZEROPS_TOKEN -b "$ZEROPS_TOKEN" -R <org>/<repo>

# 2. Inyectar ID del servicio de destino en Zerops
gh secret set ZEROPS_SERVICE_ID -b "<zerops_service_id>" -R <org>/<repo>

# 3. Auditar que los secretos fueron registrados exitosamente
gh secret list -R <org>/<repo>
```

### E. Automatización Agnóstica de DNS & SSL con Cloudflare API v4

El agente opera el enrutamiento público y la seguridad de borde mediante llamadas REST a Cloudflare sin tocar el navegador:

```bash
# 1. Obtener Zone ID para el dominio configurado
ZONE_ID=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=<app_domain>" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" | jq -r '.result[0].id')

# 2. Crear o actualizar registro CNAME apuntando al subdominio de Zerops
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data "{\"type\":\"CNAME\",\"name\":\"<app_domain>\",\"content\":\"<zerops_subdomain>\",\"ttl\":1,\"proxied\":true}"

# 3. Forzar SSL Full Strict (evita bucles infinitos de redirección 301 con Zerops)
curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/ssl" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value":"strict"}'

# 4. Activar Always Use HTTPS
curl -s -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/always_use_https" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"value":"on"}'
```

---

## 1. 4D Comparative Architectural Matrix: Deployment Methods in Zerops

| Deployment Method | Trigger / Surface | Automation Level | Environment Target | Zerops Suitability |
|---|---|---|---|---|
| **GitHub Actions (`zeropsio/actions@v1.0.2`)** | `git push origin <branch>` / Tags | 100% Automated in CI | `dev`, `stage`, `prod`, Ephemeral PRs | **SSoT for Production & Teams** |
| **Zerops Native GUI Webhook** | Push to branch / Webhook | Automated in Zerops | Single branch / Simple | Quick projects without CI |
| **`zerops_deploy` (MCP Tool)** | Agent tool call in ZCP | Dispatched by Agent | In-project / Cross-service | **SSoT for Agent Testing** |
| **`zcli push / deploy` (CLI)** | Terminal command in ZCP/local | Manual / Scripted | Dev / Fast staging | Escape hatch for local deploys |
| **`zerops_dev_server` (Supervisor)** | File edits in mount | 0 commits / Hot-reload | Local `dev` in real time | **SSoT for Iterative Dev** |

---

## 2. Git & `gh` CLI Authentication in ZCP Container

To authenticate Git and the GitHub CLI (`gh`) directly inside the ZCP control container:

```bash
# 1. Authenticate GitHub CLI with a Personal Access Token (PAT with repo and workflow scopes)
echo "$GITHUB_PAT" | gh auth login --with-token

# 2. Configure Git identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 3. Add or update remote origin
git remote set-url origin https://github.com/your-org/your-repo.git 2>/dev/null || \
git remote add origin https://github.com/your-org/your-repo.git

# 4. Verify authentication status
gh auth status
```

---

## 3. GitHub Actions Workflows with `zeropsio/actions@v1.0.2`

### A. Production Deployment Workflow (`.github/workflows/deploy.yaml`)
Deploys code to the production service whenever commits are pushed to the `main` branch:

```yaml
name: Deploy Production to Zerops

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Deploy to Zerops Production Service
        uses: zeropsio/actions@v1.0.2
        with:
          access-token: ${{ secrets.ZEROPS_TOKEN }}
          service-id: ${{ secrets.ZEROPS_PROD_SERVICE_ID }}
```

### B. Staging Deployment Workflow (`.github/workflows/stage.yaml`)
Deploys code to the staging preview service whenever commits are pushed to the `stage` branch:

```yaml
name: Deploy Staging to Zerops

on:
  push:
    branches:
      - stage

jobs:
  deploy-stage:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Deploy to Zerops Staging Service
        uses: zeropsio/actions@v1.0.2
        with:
          access-token: ${{ secrets.ZEROPS_TOKEN }}
          service-id: ${{ secrets.ZEROPS_STAGE_SERVICE_ID }}
```

### C. Semantic Tagged Release Workflow (`.github/workflows/release.yaml`)
Triggers production deployments exclusively when signed semantic tags are pushed (`v1.0.0`, `v2.3.1`):

```yaml
name: Deploy Tagged Release to Zerops

on:
  push:
    tags:
      - 'v[0-9]+\.[0-9]+\.[0-9]+'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Deploy Release to Zerops
        uses: zeropsio/actions@v1.0.2
        with:
          access-token: ${{ secrets.ZEROPS_TOKEN }}
          service-id: ${{ secrets.ZEROPS_PROD_SERVICE_ID }}
```

---

## 4. Multi-Environment Branching Lifecycle (`dev` ➔ `stage` ➔ `prod`)

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Multi-Environment Delivery Pipeline                                                                           │
│                                                                                                                │
│   ┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐          │
│   │ Development (`dev`)       │      │ Staging (`stage`)         │      │ Production (`main` / Tag) │          │
│   ├───────────────────────────┤      ├───────────────────────────┤      ├───────────────────────────┤          │
│   │ • Workspace: /var/www/{h} │      │ • Branch: `stage`         │      │ • Branch: `main` / `v*`   │          │
│   │ • Supervisor: dev_server  │─────▶│ • Pipeline: GitHub Action │─────▶│ • Pipeline: GitHub Action │          │
│   │ • Ports: 3000 / 8000      │      │ • Service: `appstage`     │      │ • Service: `appprod`      │          │
│   │ • URL: *.zerops.app       │      │ • URL: stage.domain.com   │      │ • URL: domain.com (SSL)   │          │
│   └───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘          │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Direct Deployment via `zcli` & `zerops_deploy`

For immediate terminal delivery or agent-driven verification:

```bash
# 1. Deploy service using zcli
zcli service deploy <serviceHostname> --setup prod

# 2. Deploy using zerops_deploy MCP tool (inside agent execution)
# zerops_deploy targetService="<serviceHostname>" setup="prod"
```

---

## 6. Operational Decision Matrix ("What command to execute based on your goal?")

| Immediate Goal | Recommended Action | Git & Platform State | Resulting Port / URL |
|---|---|---|---|
| **1. Local hot-reload without commits** | Edit `/var/www/{hostname}/` + `zerops_dev_server action="start"` | 0 Git commits, hot-reload active | `localhost:3000`/`8000` / `*.zerops.app` |
| **2. Test build in Zerops without GitHub** | `zerops_deploy targetService="{hostname}" setup="prod"` | Deploys directly in Zerops container | Service subdominio `*.zerops.app` |
| **3. Save local Git checkpoint** | `git commit -m "feat: description"` | Work unit recorded locally | No remote server impact |
| **4. Deliver changes to Staging (QA / Preview)** | `git push origin stage` | Triggers GitHub Actions ➔ Deploys `appstage` | `https://stage.domain.com` |
| **5. Deploy final release to Production** | `git push origin main` (or `git push --tags`) | Triggers GitHub Actions ➔ Deploys `appprod` | `https://domain.com` (Cloudflare Strict) |

---

## 7. GGA Quality Gate Patterns for Zerops Deployments

To ensure AI agents (including Antigravity) do not introduce configuration defects, secret leaks, or broken syntax into Zerops runtimes, implement the Dual-Shield Quality Gate:

### A. Local Pre-Commit Gate (Container Terminal Shield)
In each service repository (e.g. `/var/www/{serviceHostname}`), configure GGA with native GitHub Models:
```ini
# .gga
PROVIDER="github:gpt-4o"
RULES_FILE="AGENTS.md"
STRICT_MODE="true"
```
Install the Git hook:
```bash
gga install
```
When an agent or developer runs `git commit`, GGA evaluates staged files using the container's native `/usr/bin/gh` session token (`gh auth token`). If requirements from [`AGENTS.md`](file:///var/www/AGENTS.md) or Zerops syntax are violated, the commit is blocked before reaching the Git log.

### B. CI Quality Gate Job in GitHub Actions (Cloud Shield)
Before triggering `zeropsio/actions@v1.0.2`, run `gga run --ci` as a gating job in `.github/workflows/deploy.yaml`:

```yaml
name: Deploy Production to Zerops with GGA Quality Gate

on:
  push:
    branches:
      - main

jobs:
  quality-gate:
    name: GGA AI Code Review Gate
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4
        with:
          fetch-depth: 2 # Required for HEAD~1 diff

      - name: Install Gentleman Guardian Angel
        run: |
          git clone --depth 1 https://github.com/Gentleman-Programming/gentleman-guardian-angel.git /tmp/gga
          chmod +x /tmp/gga/bin/gga
          echo "/tmp/gga/bin" >> $GITHUB_PATH

      - name: Run GGA Code Review
        run: gga run --ci
        env:
          GGA_PROVIDER: "github:gpt-4o"
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  deploy:
    name: Deploy to Zerops Production
    needs: quality-gate # Hard dependency: only deploys if review passes
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Deploy to Zerops Service
        uses: zeropsio/actions@v1.0.2
        with:
          access-token: ${{ secrets.ZEROPS_TOKEN }}
          service-id: ${{ secrets.ZEROPS_PROD_SERVICE_ID }}
```

---

## 8. 5 Production Patterns in CI/CD

### Pattern 1: Single-Service Continuous Delivery via GitHub Actions
Configures automated deployments on push to `main` using `zeropsio/actions@v1.0.2` and `ZEROPS_TOKEN`.

### Pattern 2: Dual-Stage (Staging & Production) Isolated Pipeline
Separates pre-release testing on branch `stage` (`https://stage.domain.com`) from production releases on `main`.

### Pattern 3: Semantic Versioning Tagged Production Pipeline
Restricts production rollouts exclusively to explicit semantic release tags (`v1.0.0`), preventing accidental deploys from draft commits.

### Pattern 4: Hot-Reloading Development Supervision with `zerops_dev_server`
Runs background watchers (`bun run dev`, `granian`) with PID tracking and crash resilience during active development.

### Pattern 5: Break-Glass Direct In-Project Deployment via `zerops_deploy`
Allows the AI agent to test and attest builds inside Zerops without polluting remote repository commit histories.

---

## 9. Anti-Patterns & Common Gotchas

1. **Dual Webhook & GitHub Actions Collision**: Never enable native repository webhooks in the Zerops GUI while simultaneously running `.github/workflows/deploy.yaml`. This causes duplicate concurrent builds.
2. **Hardcoding `ZEROPS_TOKEN` in Files**: Never commit raw tokens into `zerops.yaml` or `.github/workflows/`; always use GitHub Repository Secrets.
3. **Missing `deployFiles: [.]` in Self-Deploying Services**: When the build and deploy occur on the same service container, `deployFiles` MUST be `[.]` to avoid purging source directories.
