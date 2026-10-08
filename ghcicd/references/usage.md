# `ghcicd`: Universal CI/CD, Git, GitHub Actions & Zerops Delivery Manual (v3.2)

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

### C. Arquitectura Canónica de Ambientes en Zerops: Opción B (Dev/Prod) Prioritaria & Staging Opcional

Para aplicaciones web (`astro-web`, Bun, Node):

1. **Modelo Soberano Dev/Prod (Opción B — Estándar Canónico Prioritario)**:
   - **Ambiente Dev (`webdev`)**:
     * Espacio de trabajo iterativo montado en `/var/www/{service}`.
     * Supervisado en tiempo real con `zerops_dev_server action="start"` o verificado con `zerops_deploy`.
     * Accesible inmediatamente a través del subdominio de Zerops (`https://{hostname}-{port}.ny1.zerops.app`) con hot-reload instantáneo y **0 commits de spam** en Git.
   - **Ambiente Prod (`<domain>.com` / `<service>-prod`)**:
     * Contenedor Bun independiente e inmutable, conectado a su dominio oficial a través de Cloudflare (SSL Full Strict).
     * El release a producción se dispara de forma 100% automatizada únicamente cuando el trabajo en `dev` está probado y se hace push a la rama `main` en GitHub, activando GitHub Actions (`zeropsio/actions@v1.0.2`) con `ZEROPS_PROD_SERVICE_ID`.
   - **Workspaces Dev Efímeros y Desechables ($0 Costo en Reposo)**:
     * La Fuente Única de la Verdad (SSoT) del código reside en el repositorio GitHub (`main`), no en el contenedor.
     * Dado que el código final está en `main` y producción corre aislada, el contenedor de desarrollo (`webdev`) es **100% desechable**: si el hito está terminado y no se va a programar activamente durante días o semanas, el servicio `webdev` puede pausarse o eliminarse en Zerops, reduciendo el consumo de desarrollo a **$0**.
     * Cuando se requiere una nueva funcionalidad o bugfix, el agente AGY aprovisiona un nuevo `webdev` en segundos clonando desde `main`.

2. **Capa Opcional de Staging (Para Auditoría QA Multi-Usuario)**:
   - En proyectos con equipos distribuidos o clientes que exijan aprobación previa antes de fusionar a `main`, se puede incorporar de forma opcional un servicio `<service>-stage` desplegado desde la rama `stage`.
   - Staging corre en su propio contenedor independiente con variables sandbox (Stripe Test, Directus Test). Es una extensión opcional y no bloquea el ciclo prioritario Dev/Prod.
   - *Frontera de Repositorios*: Este pipeline pertenece exclusivamente a los repositorios de aplicación web (`astro-web`), **NUNCA** a la plantilla chasis `zerops-astrobranding`.

3. **Advertencia de Seguridad: Antipatrón de Simular Dev/Prod en Runtime Único**:
   - Intentar usar un solo contenedor Bun para servir dev y producción asignándole dos dominios DNS (`dev.dominio.com` y `dominio.com`) introduce graves fallas arquitectónicas:
     * **Blast Radius Total**: Un error de sintaxis o excepción no capturada en desarrollo crashea el proceso Bun y derriba la tienda de producción en ese mismo instante.
     * **Riesgo de Cache Poisoning (OWASP)**: Proxies de borde y CDNs (Cloudflare) pueden almacenar en caché respuestas de prueba o datos sandbox y servirlas a clientes reales.
     * **Incompatibilidad de Secretos**: Un solo contenedor solo puede cargar un juego de variables de entorno, impidiendo aislar pasarelas de pago reales vs. pruebas.
   - *Costo en Zerops*: En Bun (`bun@1.3.9`), un runtime Astro SSR consume apenas **~45 MB de RAM**. Dos contenedores independientes consumen ~90 MB en total (costo marginal insignificante, centavos al mes). La separación física es mandatoria.

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

### B. Development Deployment Workflow (`.github/workflows/deploy-dev.yaml`)
Deploys code to the development service whenever commits are pushed to the `dev` branch, following the Option B canonical pattern:

```yaml
name: Deploy WebDev to Zerops

on:
  push:
    branches:
      - dev

jobs:
  deploy:
    name: Deploy to Zerops Development
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Deploy to Zerops WebDev
        uses: zeropsio/actions@v1.0.2
        with:
          access-token: ${{ secrets.ZEROPS_TOKEN }}
          service-id: ${{ secrets.ZEROPS_DEV_SERVICE_ID }}
```

### C. Staging Deployment Workflow (`.github/workflows/stage.yaml`)
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

### D. Semantic Tagged Release Workflow (`.github/workflows/release.yaml`)
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

## 4. Lifecycle Canónico de Entrega: Opción B (Dev ➔ Prod) & Staging Opcional

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Opción B: Flujo Canónico Prioritario (Dev Ágil ZCP ➔ Prod Inmutable GitHub Actions)                            │
│                                                                                                                │
│   ┌────────────────────────────────────────────────┐          ┌────────────────────────────────────────────┐   │
│   │ Development Workspace (`webdev`)              │          │ Production Runtime (`appprod` / Dominio)   │   │
│   ├────────────────────────────────────────────────┤          ├────────────────────────────────────────────┤   │
│   │ • Ubicación: /var/www/{service} en Zerops      │          │ • Contenedor Bun independiente y blindado  │   │
│   │ • Supervisor: zerops_dev_server action="start" │ git push │ • Dominio público vía Cloudflare SSL Strict│   │
│   │ • Hot-reload instantáneo en subdominio Zerops  │  `main`  │ • CI/CD: zeropsio/actions@v1.0.2 en GitHub │   │
│   │ • Cero commits spam en GitHub para probar CSS  │─────────▶│ • Despliegue inmutable 100% automatizado   │   │
│   │ • 100% Desechable: se apaga o borra para $0    │          │ • Secretos y pagos reales aislados         │   │
│   └────────────────────────────────────────────────┘          └────────────────────────────────────────────┘   │
│                                   │                                                                            │
│                     (Opcional para QA multi-usuario)                                                           │
│                                   ▼                                                                            │
│                       ┌────────────────────────────┐                                                           │
│                       │ Staging Preview (`stage`)  │ (Opcional: solo si el equipo requiere                    │
│                       ├────────────────────────────┤  aprobación previa multi-dev antes de merge)              │
│                       │ • Branch: `stage`          │                                                           │
│                       │ • Service: `appstage`      │                                                           │
│                       │ • URL: stage.domain.com    │                                                           │
│                       └────────────────────────────┘                                                           │
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
| **4. Deliver changes to Staging (Opcional QA)** | `git push origin stage` | Triggers GitHub Actions ➔ Deploys `appstage` | `https://stage.domain.com` |
| **5. Deploy release to Production (Opción B)** | `git push origin main` (or `git push --tags`) | Triggers GitHub Actions ➔ Deploys `appprod` | `https://domain.com` (Cloudflare Strict) |
| **6. Save $0 resources after release (Efímero)** | Stop or delete `webdev` service in Zerops | SSoT in `main`, prod keeps running intact | $0 active compute cost in dev |

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
