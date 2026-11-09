# Paperclip Zerops Infrastructure & Database Schema Manual

This reference details the infrastructure layout, persistence mechanics, and PostgreSQL 18 schema for Paperclip in Zerops.

---

## 1. Zerops Incus LXC Architecture

Paperclip is deployed as a sovereign service inside the Zerops Incus LXC infrastructure:
- **Runtime**: Node.js 26 (`nodejs@26`) on Ubuntu 24.04 LTS.
- **Port**: `3100` (HTTP LAN internal, exposed via public subdomain `paperclip-*.ny1.zerops.app`).
- **Database**: PostgreSQL 18 managed cluster (`database:5432/paperclip`).
- **Persistent Volume**: Zerops LocalStorage NVMe volume mounted at `/mnt/localstorage` (single-kernel POSIX semantics).

```
┌────────────────────────────────────────────────────────┐
│               ZEROPS PROJECT ARCHITECTURE              │
│                                                        │
│  ┌────────────────────┐       ┌─────────────────────┐  │
│  │   paperclip:3100   │──────▶│    database:5432    │  │
│  │  (Node 26 LXC)     │       │   (PostgreSQL 18)   │  │
│  └─────────┬──────────┘       └─────────────────────┘  │
│            │                                           │
│            ▼                                           │
│  ┌────────────────────┐       ┌─────────────────────┐  │
│  │  /mnt/localstorage │       │     hermes:8000     │  │
│  │   NVMe POSIX Mount │◀──────│   (Python 3.12 LXC) │  │
│  └────────────────────┘       └─────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

---

## 2. Storage & CLI Persistence Mechanics

Paperclip requires absolute state persistence across container restarts and redeployments:

### The Configuration Path
- **Canonical Storage**: `/mnt/localstorage/paperclip/instances/default/config.json`
- **Symlink**: `/home/zerops/.paperclip -> /mnt/localstorage/paperclip`
- **Environment**: `PAPERCLIP_HOME=/mnt/localstorage/paperclip` exported in `/etc/environment` and `~/.bashrc`.

### The CLI Wrapper
Paperclip's CLI defaults to searching `~/.paperclip/instances/default/config.json`. To eliminate path ambiguity and make commands immediately runnable from anywhere:
- `/usr/local/bin/paperclipai` (and `/var/www/.bin/paperclipai`) intercepts invocations:
```bash
#!/bin/bash
CONFIG_PATH="/mnt/localstorage/paperclip/instances/default/config.json"
if [ -f "$CONFIG_PATH" ]; then
    exec /var/www/paperclip/packages/cli/dist/index.js -c "$CONFIG_PATH" "$@"
else
    exec /var/www/paperclip/packages/cli/dist/index.js "$@"
fi
```
This guarantees that commands like `paperclipai auth bootstrap-ceo` or `npx paperclipai auth bootstrap-ceo` resolve with exit code 0 out-of-the-box.

---

## 3. Database Schema Overview (319 Relational Tables)

Paperclip utilizes Drizzle ORM on PostgreSQL 18. Key tables include:

### Authentication & Tenant
- `"user"`: Better-Auth user profiles (`id`, `name`, `email`, `email_verified`).
- `companies`: Tenant organization (`id`, `name`, `issue_prefix`, `created_at`).
- `company_onboarding_seeds`: Tracks completion of organizational setup (`company_id`, `revision`, `goal_id`, `agent_id`, `issue_id`, `applied_at`).

### Work & Execution Plane
- `agents`: Agent profiles, roles (`ceo`, `lead`, `worker`), `reports_to` recursion, `adapter_type`, `adapter_config` (JSONB), and monthly spend tracking (`budget_monthly_cents`, `spent_monthly_cents`).
- `goals`: High-level initiatives (`title`, `description`, `level: 'company'`, `status: 'in_progress'`).
- `projects`: Concrete project buckets (`goal_id`, `name`, `lead_agent_id`, `status: 'active'`).
- `issues`: Kanban work units (`project_id`, `goal_id`, `title`, `status`, `priority`, `assignee_agent_id`, `checkout_run_id`).
- `heartbeat_runs`: Execution logs and heartbeat traces for invokable agents.

### Governance & Security
- `budget_policies`: Monthly spend caps and concurrent reservations.
- `approvals`: Human-in-the-loop approval cards for tool actions, hirings, and sensitive deployments.
- `tool_mcp_gateways`: Security policies (`allow`, `deny`, `require_approval`) governing upstream tool execution.

---

## 4. Upstream Templates & GitOps Automation

To guarantee that any new brand or ZCP deployment initializes Paperclip without manual intervention, the following templates are integrated into `zerops-astrobranding`:
1. `apps/paperclip/zerops.yaml`: Production LXC Node.js 26 service configuration with PostgreSQL 18 and LocalStorage mounts.
2. `apps/paperclip/start.sh`: Entrypoint with automated Zod-compliant `config.json` generation and symlink creation.
3. `iniciar.sh` & `scripts/setup-zcp.sh`: Automated directory scaffolding and wrapper deployment.
