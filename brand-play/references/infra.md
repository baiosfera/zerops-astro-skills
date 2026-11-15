# `brand-play` — Infrastructure & Zerops Topology Contracts

## 1. Storage & File Topology

The `brand-play` skill operates across three physical storage tiers in the Zerops Incus LXC infrastructure:

| Tier | Path | Purpose | Performance / Semantics |
|---|---|---|---|
| **Primary SSoT** | `/var/www/localstorage/knowledge_hub/03_PLAYBOOKS_MAESTROS/` & `04_BANCOS_TACTICOS/` | Canonical 20 Master Playbooks + 3 Tactical Banks (`baiosfera:KNOWLEDGE_HUB` mirror) | Sub-millisecond NVMe local storage + Qdrant `baiosfera_knowledge` (`http://knowledge:8000/mcp`) |
| **Brand Assets** | `/var/www/localstorage/workspaces/${PROJECT_NAME}/` · `/var/www/baiosfera/PROYECTOS/${PROJECT_NAME}/dev/brandbook.json` | Active brand W3C DTCG tokens | Isolated per client brand |
| **Transmutation Cache** | Valkey 7.2 (`valkey:single@7.2`) | Rendered copy & component cache | Sub-millisecond memory cache; key pattern `brandplay:cache:${brand}:${slug}` (TTL 24h) |

---

## 2. Runtime Execution Boundaries & ZCP Invariants

1. **Plano de Control ZCP Single-Node**:
   - `zcp` acts solely as orchestrator and state coordinator (`minContainers: 1, maxContainers: 1`) in `cpuMode: SHARED`.
   - Parsing, slot hydration, and schema validation execute in-memory inside ZCP in $< 15\text{ ms}$.
   - Heavy application builds (`bun run build`, `npm test`) are dispatched to dedicated runtime containers over SSH:
     ```bash
     ssh webdev "cd /var/www && bun run build"
     ```
2. **Bifrost Production AI Gateway**:
   - Downstream AI synthesis connects to Bifrost on the internal Zerops DNS: `http://bifrost:8080/v1/chat/completions`.
   - Headers: `x-tier: production`, `Content-Type: application/json`.
   - Bifrost CEL routing automatically failovers between Groq, Cerebras, and upstream providers with $< 100\mu\text{s}$ latency.
3. **SSoT Parity Invariant**:
   - All custom skills in `zerops-astro-skills` maintain bit-for-bit parity with Git `origin/main` and `/var/www/.agents/skills/` (verified read-only via `ssot-parity-check`).

---

## 3. Physical Certification Sensors

Compliance is verified through physical behavior sensors (exit code 0):
1. `skills-suite-validate`: Validates YAML frontmatter, word count budgets ($\le 480$ words on `SKILL.md`), and internal link integrity.
2. `ssot-parity-check`: Enforces zero drift between ZCP local files, Google Drive SSoT, and remote GitHub repositories.
