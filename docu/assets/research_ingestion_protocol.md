# Research Ingestion & Progressive Disclosure Protocol (v7.0)

> **Architectural Standard:** Prior to authoring or updating any skill or reference document, the agent ingests research findings without lossy compression and projects them into normative reference files based on the target tool's Functional Archetype.

---

## 1. Decoupled Research Intake & Epistemic Autonomy

The tactical execution of research is 100% delegated to [`research`](file:///var/www/.agents/skills/research/SKILL.md) across its 12 retrieval engines (Engram, Context7, Exa, Tavily, Brave, Jina Reader, Crawl4AI, Playwright, Puppeteer, Firecrawl, DuckDuckGo).

`docu` acts as the downstream **Architect, Synthesizer, and Certifier**:
1. It ingests the research dossier (typically staged in `/var/www/artifacts/<slug>_research_report.md`).
2. It categorizes the tool into one of the **4 Functional Archetypes**.
3. It maps and unbundles (desmenuza) the technical truth into modular references in `references/`.
4. It compiles Fractal CoHaLo harnesses (`timeout 10s`, physical exit 0 sensors) directly into executable code.

---

## 2. The 4 Functional Archetypes (Lossless Mapping)

Literature and industry specifications (`agentskills.io` / arXiv:2602.12430) confirm that imposing uniform deployment templates on all tools creates artificial bloat. Documentation must reflect the tool's true operating nature:

### Archetype 1: Code, SDK & Framework Skills
* **Examples**: `bun`, `astro`, `fastapi`, `react-19`, `ai-sdk-5`, `nodejs`.
* **Primary Reference (`references/usage.md`)**:
  - SDK / Client initialization options (timeouts, retries, headers, authentication).
  - Complete method signature matrix with TypeScript interfaces or Python type hints.
  - At least 5 production code patterns (basic CRUD, async webhooks, bulk operations, error recovery, streaming).
  - Error code catalog (HTTP 4xx, 5xx, SDK exceptions) with actionable remediation.
* **Infrastructure Reference (`references/infra.md`)**:
  - Compiled *only* when the framework deploys as a long-running service (base OS, listening ports, `.env` dictionary, `zerops.yaml` build/run lifecycle, health checks).

### Archetype 2: Infrastructure & Platform Services
* **Examples**: `zcp`, `dckr`, `postgresql`, `valkey`, `nats`, `local-storage`.
* **Primary Reference (`references/infra.md`)**:
  - Service container architecture (Docker VM vs Native Incus LXC).
  - Resource scaling profiles (vertical autoscaling vs fixed limits).
  - Listening ports, public routing domains, and subdomain configuration.
  - Persistent volume mounts (`/mnt/...`), permission safeguards (`chmod -R 777`), and storage types.
  - Environment variables dictionary (`.env`) with types, defaults, and requirements.
  - Lifecycle automation (`prepareCommands`, `buildCommands`, `startCommands`, health checks).
* **Usage Reference (`references/usage.md`)**:
  - Client connection strings (`$VAR` interpolation, never hardcoded credentials).
  - Query execution patterns, CLI administrative commands, migrations, and health queries.

### Archetype 3: Domain Engines, REST APIs & Calculation Motors
* **Examples**: `vedastro`, `freeastroapi`, `astrologyapi`, `astroway`, `kundali`, `hebcal`, `nasa`.
* **Primary Reference (`references/usage.md`)**:
  - Base URLs, authentication headers, rate limits, and quota handling.
  - Complete endpoint catalog with parameter schemas (types, constraints, defaults).
  - Domain-specific calculation parameters (e.g. coordinates, Julian dates, zodiac systems, ayanamsas, ephemeris models).
  - Response schemas and precision tolerances.
  - Failover strategies, circuit breakers, and upstream error status codes.
* **Infrastructure Reference**:
  - **Omitted by default**. Domain calculation APIs have zero container ports, storage mounts, or `zerops.yaml` files. Avoid injecting fake infrastructure configs.

### Archetype 4: Cognitive, Planning, Workflow & Design Methodologies
* **Examples**: `planner`, `research`, `cohalo`, `brainstorming`, `chroma`, `fontgen`, `brandbook`.
* **Primary Reference (`references/usage.md` or `references/methodology.md`)**:
  - Closed state machines and phase transition matrices.
  - Algorithmic invariants and non-negotiable rules.
  - Token budget guardrails and prompt engineering patterns.
  - Design token schemas, mathematical ratios (WCAG AAA, APCA, OKLCH), or typographic scales.
* **Infrastructure Reference**:
  - **Omitted**. Methodological and cognitive skills operate purely in the agent reasoning loop and filesystem.

---

## 3. Staging Ingestion & Unbundling Invariant (Zero Deletion)

1. **Temporary Staging Read**: Read `/var/www/artifacts/<slug>_research_report.md` produced by `research`.
2. **Systematic Unbundling (Desmenuzamiento)**:
   - Extract 100% of method signatures, classes, arguments, and return types into `references/usage.md`.
   - Extract 100% of configuration variables, ports, and lifecycle commands into `references/infra.md` (when applicable).
   - Zero algorithms or parameters may be omitted or summarized away.
3. **Anti-Artifacts Invariant**:
   - Permanent skill files in `.agents/skills/<slug>/` must NEVER link to temporary files in `/var/www/artifacts/`.
   - All references must resolve within the skill tree or canonical system documentation.
