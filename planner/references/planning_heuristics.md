# Planner Reference Manual: Planning Heuristics, Versioning & Auto-Purge (v2.2)

> **SSoT Reference Document:** `/var/www/.agents/skills/planner/references/planning_heuristics.md`  
> **Meta-Skill:** [`planner`](file:///var/www/.agents/skills/planner/SKILL.md)  
> **Standard:** CoHaLo v7.0, Supreme Directive v7.6, SSoT Governance, unisetup.sh-first & Zero-Bloat Execution.

---

## 1. Zero-Latency Artifact Synthesis Heuristic

- **Core Principle:** Fast, deterministic alignment between user intent and executable specifications.
- **Artifact File Generation:** Plans in `/var/www/artifacts/*.md` are written via terminal execution (`cat << 'EOF' > /var/www/artifacts/<plan>.md`) or standard file writing without UI artifact metadata, preventing permission boundaries.
- **Delivery Standard:** Output the updated plan artifact and provide its clickable markdown link immediately.

---

## 2. Cumulative Evolutionary Plan Versioning, Anti-Cháchara & Anti-Amnesia Law

- **Operational Standard:** Master plans record the verifiable engineering timeline:
  1. Each revision increments the version suffix: `_v1.md` $\to$ `_v2.md` $\to$ `_v3.md`.
  2. Prior versioned plan files remain immutable historical records during drafting, archived to `archive/<name>_vN.superseded.md`.
  3. Every new version MUST inherit, consolidate, and synthesize all prior state, forensic findings, and requirements, integrating new decisions into a unified single source of truth.
  4. **F4 Feedback Loop & Claridad:** Al recibir correcciones o feedback sobre un plan en F4, materializá los ajustes en la especificación o issue correspondiente antes de avanzar a ejecución, evitando respuestas vacías o performativas.
  5. **Linear Direct API Synergy:** Linear opera de forma determinista mediante `/var/www/.bin/linear-cli` consumiendo `https://api.linear.app/graphql` (<300ms). Cada nodo del plan en F5 actualiza su estado en Linear (In Progress $\to$ sensor exit 0 $\to$ Done).
  6. **Blindaje Anti-Freeze FUSE:** Para búsquedas en `/var/www/baiosfera`, podá (`-prune`) las carpetas remotas o buscá en subdirectorios locales específicos. Limpiezas de `__pycache__` se acotan localmente al directorio del script.
- **Mandatory 6-Vector Cumulative Audit Gate (Anti-Amnesia Pre-Flight)**: Before emitting `_v(N+1).md`, the agent must execute a strict comparative audit against `_v1` through `_vN` ensuring zero loss across 6 critical vectors:
  1. **Forensic Diagnoses & Root Causes**: All problem analyses and pathologies identified in earlier versions must be preserved and expanded, never silently dropped.
  2. **Inventory of Target Files**: Every file identified in prior versions remains explicitly in scope.
  3. **Universal Pre-Mutation Backups**: All backup commands for scripts, rules, and skills accumulated across prior versions must be retained in Paso 1.
  4. **Architectural Coherence**: Preserve functional domain contracts and proven invariants, pruning obsolete bureaucratic friction or redundant rules when authorized.
  5. **Executable Step Granularity**: Execution steps must be cumulatively merged; adding new layers must not displace existing execution actions.
  6. **Physical Attestation Matrix**: All rows and sensors from prior control matrices must be present in the new version.

---

## 3. Flat Pre-Mutation Backup Priority in `bak/skills/` (Track A Only)

- **Default Standard:** For Track A plans, all pre-mutation backups of skills are created directly as flat uncompressed directories inside `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/bak/skills/<skill_name>_v<version>.bak/`.
- **Track B Scope:** Workload deployments (Track B) deploy directly on application runtimes via Git/SSH, reserving `bak/skills/` snapshots exclusively for Track A tooling.

---

## 4. Mandatory Internal Semantic Version Bumping (Track A Only)

- **Operational Standard:** Every mutation, refactoring, or improvement to a skill increments the internal `metadata.version` in the YAML frontmatter (`+0.1.0` for minor, `+0.0.1` for patch).
- **Attestation:** The physical validation harness verifies that the frontmatter version matches the target milestone.

---

## 5. Language Boundary Shield & Disambiguation Priority Rule

- **Human Alignment Surfaces (Master Plans):** Master plans in `/var/www/artifacts/*.md` are human-facing alignment documents and are written in the active conversation language (Spanish by default). This rule holds priority over generic technical defaults.
- **LLM Consumption Surfaces (Skills):** All files inside `.agents/skills/` (`SKILL.md`, `references/`, schemas, code contracts, assets) are written in 100% Technical English for maximum reasoning fidelity and token economy.
- **User Interactions (Chat & Summaries):** Chat messages, summaries, and questions directed to the user match the user's active conversation language (Spanish with natural voseo by default).

---

## 6. Zero Chat Bloat & Brevity Invariant

- **Directive:** Chat responses remain concise, executive, and decision-oriented.

---

## 7. Code-Server Clickable Links Standard (`file:///`) & Anti-Name-Dropping Invariant

- **Dual-Anchor Format:** All file links and governing skill references use standard markdown file URIs with absolute paths: `[`<filename>`](file:///var/www/path/to/file)`.
- **Operative Correspondence Rule:** Every governing skill referenced in a plan header has:
  1. Its active rule or invariant explicitly cited in the body.
  2. A physical sensor of attestation (`exit code 0`, HTTP 200, token check) in the Control Matrix.

---

## 8. Comprehensive Direct Clean Auto-Purge with Engram LTM

- **Trigger Condition:** All plan execution steps are complete and all physical sensors report success (`exit code 0`, HTTP 200, `zerops_verify`).
- **Action Sequence:**
  1. Direct Clean Deletion: Remove temporary plan files: `rm -f /var/www/artifacts/<plan_name>*.md`.
  2. Persist the handover milestone to Engram LTM (`mem_save` with stable `topic_key`).
- **Plan Ephemerality:** Plans are transient human-alignment staging documents whose permanent historical record resides in Engram LTM.

---

## 9. Subagent Research Prompt Contract Injection & Fast Grounding Heuristic

- **Operational Rule:** For single-fact, version, endpoint, or local syntax checks, agents prioritize **Fast Grounding JIT Inline** in the main thread (Exa/Tavily/DDG ➔ Jina verbatim) with zero subagent overhead. Whenever delegating complex research, web extraction, or multi-file codebase analysis (>3 files) to a subagent (`invoke_subagent` with `typeName: "research"`), the parent agent injects the full text of [`subagent_prompt_contract.md`](file:///var/www/.agents/skills/research/assets/subagent_prompt_contract.md) directly into the `Prompt` parameter.
- **Attestation & Disk Report Offload:** Research subagents execute the compound epistemic grounding pipeline with verbatim Jina Reader extraction and write the complete findings to `/var/www/artifacts/<target>_research_report.md`. The parent planner ingests this report directly to construct informed decision gates and attestation criteria without inflating conversation context.

---

## 10. `unisetup.sh-first` Clean-Room Replicability Heuristic

- **Core Principle:** The workspace `/var/www/` is ephemeral. The permanent sovereign SSoT is `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/`.
- **Mandatory Flow & Physical Order:** `unisetup.sh-first` defines the architectural design contract: every solution must be reproducible by running `unisetup.sh` on a virgin ZCP container. The physical mutation order when authoring changes is:
  $$\text{Backup in bak/} \to \text{Mutación Local} \to \text{Espejo SSoT Drive (0zcp-123/)} \to \text{Sensor Físico} \to \text{Registry Refresh}$$
- **Validation:** Bootstrapping a fresh ZCP container and running `unisetup.sh` reproduces the 100% verified state without human prompts or manual corrections.

---

## 11. Deterministic Dual-Track Planning & Disambiguation Heuristic

- **Track A (Skill Governance & SSoT Tooling):** Target is `.agents/skills/`, `.agents/rules/`, or `0zcp-123/scripts/`. Requires flat backup in `bak/skills/`, Semver bump, SSoT mirror in Google Drive, unisetup sync, and the mandatory Skill Registry attestation sensor.
- **Track B (Zerops Workload Deployment):** Target is application code, Zerops services, or database migrations. Requires `zcp-validate yaml`, `zerops_workflow`, and SSH execution inside containers. Umbrella skills (`bknd`, `frnt`) operate as routing indices, never as service hostnames.

---

## 12. Positive Guidance & CoHaLo Token Economy Rule

- **Constructive Framing:** Directives define what to do, which schemas to produce, and which closed sets apply. Constructive framing optimizes attention allocation in deep reasoning models.
- **Dual-RAG Token Budget:** Executive routers (`SKILL.md`) remain concise (budget: 180–450 tokens / $\le$ 500 words for leaf skills; $\le$ 2500 tokens for domain orchestrators). In-depth algorithms, method tables, and edge cases reside in `references/`.

---

## 13. Ground-Truth OpenAPI/Schema Discovery Gate

- **Core Rule:** Extract canonical schemas directly from the official upstream source (`openapi.json`, Swagger, official SDK types, Context7) into `/var/www/artifacts/<target>_research_report.md` in Phase 0 BEFORE drafting master plans.
- **Catalog Verification:** The catalog count must be measured directly against the upstream ground truth, avoiding guesswork or inferred endpoints.

---

## 14. Universal Client-Agnostic & Zero-PII Law

- **Core Rule:** Skills, reference manuals (`references/`), skill routers (`SKILL.md`), and master plans are reusable platform SDKs and tooling.
- **Separation Law:** They must contain zero individual client data, private consultant names, or private coordinates. All schemas, examples, and test payloads must use strict parameter contracts and universal placeholders (`<YYYY>`, `<MM>`, `<DD>`, `<LAT>`, `<LNG>`, `<TZ_STR>`, `"Consultant Name"`).

---

## 15. Router-Reference Modular Separation (Token Economy vs Zero Deletion)

- **Core Rule:** `SKILL.md` is strictly an executive decision dispatcher (<550 words / <750 tokens for leaf skills).
- **Lossless Housing:** The complete universe of endpoints, JSON schemas, methods, and types belongs losslessly in `references/usage.md` and `references/infra.md`. Modularization preserves 100% of technical capabilities without truncation.

---

## 16. Closed Lifecycle Topology & Zero-Omission Gate (Rule 5 Standard)

- **Closed Alphabet Principle ($\Sigma = \{N_1, ..., N_8\}$):** Master plans for Track A (Skill Governance & SSoT Tooling) strictly instantiate the 8 canonical nodes in both `## 4. Plan de Ejecución Inmediato` and `## 5. Matriz de Control`:
  1. **$N_1$ (Respaldo Plano O(1)):** Flat uncompressed snapshot in `bak/skills/<skill>_v<version>.bak/`.
  2. **$N_2$ (SSoT Indivisibility):** Verification of `unisetup.sh-first` contract and Google Drive mirror parity.
  3. **$N_3$ (Semver Bump):** Bump version in YAML frontmatter, script headers, and docs.
  4. **$N_4$ (Cero Eliminación & CoHaLo):** Semantic diff audit via `skill-improver`, positive guidance, closed domain.
  5. **$N_5$ (Despliegue Tri-Destino & Git Push Soberano):** Mirroring to Google Drive SSoT (`0zcp-123/.agents/skills/`), sincronización hacia `/var/www/zerops-astro-skills/` y ejecución obligatoria de `git push origin main`.
  6. **$N_6$ (Sensores Físicos):** Execution of local validator (`scripts/<target>-validate.sh`) and multi-skill suite (`skills-suite-validate.sh`).
  7. **$N_7$ (Sensor de Skill Registry):** Independent execution and physical grep validation of `gentle-ai skill-registry refresh --force`.
- **Pre-Flight Validation Rejection:** Any plan that merges, skips, or renames these nodes without prior architectural authorization fails the pre-flight gate.

---

## 17. Certification & Invariance Gate Heuristic (Anti-Churn)

- **Source Standard:** Inherited from [`docu`](file:///var/www/.agents/skills/docu/SKILL.md) (`references/certification.md`).
- **Operational Heuristic:** When an audit determines that a skill or architecture already satisfies all 5 normative criteria (Anatomy, Token Budget, Lossless Integrity, Positive Guidance, Physical Sensors), the agent must declare the artifact **`Certified Optimal / Invariant / Anti-Fragile`**, run the sensor to confirm exit code 0, and perform 0 byte modifications on disk.

---

## 18. Anti-Desbocado Invariant & Mandatory F4 Halt Gate

- **Core Principle:** Rushing into code execution without a structured blueprint is classified as undisciplined hacking (vibecoding) and is strictly banned. Planning is the supreme physical safeguard against hallucinations, forgotten dependencies, regressions, and context exhaustion.
  1. **Strict Boolean Go Predicate:** Transitioning to F5 REQUIRES an explicit univoque affirmative token (`\b(go|adelante|procede|ejecuta|ejecutá|aprobado|dale|si)\b`) AND the total absence of interrogative punctuation (`?`, `¿`) or doubt phrases (`por qué`, `qué pasó`, `espera`).
  2. **Interrogative / Diagnostic Hold:** If the user turn contains questions, status queries, or discussion, the agent strictly remains in F4, answers the inquiry, and DOES NOT mutate code.
- **Single Active Plan & Artifact Lifecycle Invariant:**

---

## 19. Condensed High-Density Plan Standard (CoHaLo Token Economy & Human Readability)

- **Balanced Synthesis Law:** The antidote to execution bloat is NOT skipping planning, but designing ultra-condensed, high-density plans that minimize token spend while eliminating ambiguity.
- **Human-Centric Clarity:** Plans are written in the user's natural language (warm, direct Spanish), structured for rapid 2-minute scanning without ceremonial rhetoric or repetitive filler.
- **Agent Determinism:** Plans specify exact file paths, explicit CLI commands, concrete invariants, and physical sensors (`exit code 0`), providing an unassailable roadmap for flawless F5 execution.
- **Cumulative Versioning:** Revisions increment suffixes immutably (`_v1.md` $\to$ `_v2.md` $\to$ `_v3.md`), never overwriting prior drafts, preserving the decision rationale across rounds.

---

## 20. Linear Dual-Track Synergy: Micro-Plans vs Macro-Roadmaps

- **Bifurcated Issue Tracking Standard:**
  2. **Macro-Initiatives & Full Deployments (Linear Project Sync):** High-level roadmap initiatives, cross-service orchestrations (e.g. `zerops-astrobranding full deployment`), and multi-day epics are synchronized to Linear via Linear MCP (`linear_create_issue`, `linear_update_issue`) under the designated workspace project (e.g. `zerops-astrobranding`, Team `BAI`).
- **Context Relief:** Offloading full epic roadmaps and milestones to Linear preserves precious LLM context window across compactions and session restarts, allowing the agent to query active issues on demand while giving the human visual dashboard oversight.

