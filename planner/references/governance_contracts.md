# Planner Reference Manual: Governance Contracts, SSoT & Backups Policy (v2.1)

> **SSoT Reference Document:** `/var/www/.agents/skills/planner/references/governance_contracts.md`  
> **Meta-Skill:** [`planner`](file:///var/www/.agents/skills/planner/SKILL.md)  
> **Standard:** CoHaLo v7.0, Supreme Directive v7.6, SSoT Governance, unisetup.sh-first & Universal Virgin ZCP Law.

---

## 1. Universal Pre-Mutation Backup Policy in `bak/`

- **Canonical Base Path:** `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/bak/`
- **Subdirectory Categorization (Closed Taxonomy):**
  * `bak/scripts/` — Executable `.sh` scripts and tooling.
  * `bak/skills/` — Skill folders and `.md` references (flat structure exclusively).
  * `bak/rules/` — Governance `.md` rule documents.
  * `bak/apis/` — API keys and environment definitions.
  * `bak/mcp/` — MCP server schemas and authentication configs.
- **Transient Plan Lifecycle & Direct Clean Purge:**
  * Plans in `/var/www/artifacts/*.md` serve as active alignment staging documents during iteration.
  * Following physical sensor attestation (exit code 0) and Engram LTM persistence, plans are directly purged from disk (`rm -f /var/www/artifacts/<plan_name>*.md`).
- **Flat Individual Uncompressed Snapshot Taxonomy ($O(1)$):**
  * Skill snapshots are preserved strictly as uncompressed individual directories directly in:
    `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/bak/skills/<skill_name>_v<version>.bak/`
  * Taxonomy is strictly flat and individual: each skill snapshot resides directly under `bak/skills/` without grouping folders, task-named directories, or archive formats (`.tar.gz`, `.zip`).
  * **Strict Prohibition of Monolithic Repository Backups:** Code repositories (`zerops-astrobranding`, `elplacerdc`, etc.) and entire project folders rely exclusively on native Git/GitHub version control (`git commit`, `git tag`, `git checkout`). Creating `.bak` snapshots of whole repositories or monorepos to `bak/` or Google Drive is strictly prohibited to prevent storage bloat and workflow contamination.
  * **Track B and C Exemption:** Application code, Zerops service deployments (Track B), and direct Google Drive content/data ops (Track C) are exempt from `bak/` snapshots.

---

## 2. Mandatory Internal Semantic Versioning (Semver) Invariant (Track A)

- **Rule:** Every skill mutation (architectural enhancement, schema adjustment, structural optimization) MUST bump `metadata.version` in the YAML frontmatter.
- **Increment Guide:**
  * Patch (`+0.0.1`): Minor typo fixes, documentation phrasing.
  * Minor (`+0.1.0`): New references, new feature schemas, non-breaking refactors.
  * Major (`+1.0.0`): Fundamental architecture rewrite or breaking changes.

---

## 3. SSoT Indivisibility Law via `setup-*.sh` & `inject-agent-rule`

- **Invariant:** Governance rule files (`AGENTS.md`, `.agents/rules/00-SUPREME-DIRECTIVE.md`) are generated views, never hand-edited primary sources.
- **Modification Protocol:**
  1. Identify the provisioning `unisetup` script responsible for the directive:
     * General governance, Engram, GGA, subagent rules: [`setup-gentle.sh`](file:///var/www/baiosfera/0ZEROPS-AGY/0zcp-123/scripts/setup-gentle.sh).
     * Custom skills synchronization & auto-discovery: [`setup-drive.sh`](file:///var/www/baiosfera/0ZEROPS-AGY/0zcp-123/scripts/setup-drive.sh).
     * Zerops platform contracts, Docker VM, CI/CD: [`setup-zcp.sh`](file:///var/www/baiosfera/0ZEROPS-AGY/0zcp-123/scripts/setup-zcp.sh).
     * Astrology, MCPs, APIs: [`setup-astrokey.sh`](file:///var/www/baiosfera/0ZEROPS-AGY/0zcp-123/scripts/setup-astrokey.sh).
     * Browsers, crawlers: [`setup-browser.sh`](file:///var/www/baiosfera/0ZEROPS-AGY/0zcp-123/scripts/setup-browser.sh).
  2. Backup the script to `0zcp-123/bak/scripts/<script>_v#.<ext>.bak`.
  3. Bump the Semver version in the script header.
  4. Apply modifications and execute deterministic injection via `inject-agent-rule`.
  5. Replicate the script to the permanent SSoT Google Drive mirror (`/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/scripts/`).

---

## 4. Dual-Anchor Header Standard & Physical Sensor Correspondence Rule (Anti-Compliance Theater)

- **The Inseparable Duo of Planner:**
  * **Input Sentinel (Anti-AMN):** [`research`](file:///var/www/.agents/skills/research/SKILL.md) is mandatory for all master plans. Eradicates hallucinations, assumptions, and parametric drift via `<epistemic_attestation>` in Section 1.
  * **Output Sentinel (Preservation & Zero-Deletion):** [`skill-improver`](file:///var/www/.agents/skills/skill-improver/SKILL.md) is mandatory for all Track A plans mutating or refactoring existing code, rules, or skills. Guarantees 100% preservation of directives without accidental mutilations.
- **Canonical Dynamic Header:** Every plan header uses absolute markdown links and avoids cosmetic badges:
  ```markdown
  > **Marco de Gobernanza Activo:**  
  > - [`Supreme Directive`](file:///var/www/.agents/rules/00-SUPREME-DIRECTIVE.md)
  > - [`Planner`](file:///var/www/.agents/skills/planner/SKILL.md)
  > - [`Research`](file:///var/www/.agents/skills/research/SKILL.md)
  > - [`Skill-Improver`](file:///var/www/.agents/skills/skill-improver/SKILL.md)
  > - [`Ley de Indivisibilidad SSoT (unisetup.sh-first)`](file:///var/www/baiosfera/0ZEROPS-AGY/0zcp-123/scripts/unisetup.sh)
  > - *[Skills Especializadas Adicionales]: Declarar ÚNICAMENTE si la tarea ejecuta su arnés físico y cuenta con un sensor determinista en la Matriz de Control (Sección 5).*
  >  
  > **Plan Track:** `[Track A: Skill Governance & SSoT Tooling | Track B: Zerops Workload Deployment]`
  ```
- **Operative Correspondence Rule & Prohibition of Cosmetic Badging:**
  * Every governing skill declared in the header MUST map to an active, verifiable operation in the plan body.
  * Any specialized skill (e.g. `Docu`, `CoHaLo`) appearing in the header MUST have an explicit row in the Section 5 Attestation Matrix running a physical execution sensor (`*.sh` or binary returning `exit code 0`).
  * Declaring specialized skills in the header without an active physical execution sensor in Section 5 is classified as "Compliance Theater" and triggers immediate rejection by `plan-validate` (`exit code 1`).

---

## 5. Universal Clean-Room Virgin ZCP & Cross-Account Parity Contract

- **Core Rule:** Modifying `/var/www/.agents/skills/` requires immediate bidirectional mirroring to `/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/.agents/skills/`.
- **Clean-Room Virgin ZCP Benchmark:** Testing must prove reproducibility beyond the local container. The canonical standard of truth is a virgin project in an independent account executing `unisetup.sh` from scratch with **exact 0 bytes of drift** against Google Drive SSoT (`ssot-parity-check` exit code 0).
- **Dual-Target Invariant:** Tooling scripts and CLI mutators write concurrently to the local workspace and to the canonical Google Drive mirror (`0zcp-123/`).

---

## 6. Tri-Track Governance Contract & Mandatory Closed-Topology Sensor Gate

- **Track A (Skill Governance & SSoT Tooling):**
  * Applies to: Skills (`.agents/skills/`), Python platform scripts (`.bin/hooks/tool-guard.py`, etc.), provisioning scripts (`setup-*.sh`, `unisetup.sh`, `iniciar.sh`), core rules (`AGENTS.md`, `00-SUPREME-DIRECTIVE.md`).
  * Mandatory Closed Sequence (Rule 5): Plans instantiate all 8 canonical nodes:
    1. $N_1$: Flat uncompressed pre-mutation backup in `bak/skills/<skill>_v<version>.bak/` or `bak/scripts/<name>_<date>.bak`.
    2. $N_2$: `unisetup.sh-first` parity and Google Drive mirror synchronization.
    3. $N_3$: Semver version bump in YAML frontmatter and internal scripts.
    4. $N_4$: Zero Deletion Invariant audit via `skill-improver` and CoHaLo positive guidance.
    5. $N_5$: Multi-destination deployment (`/var/www/`, Google Drive SSoT, `~/.gemini/antigravity-cli/`).
    6. $N_6$: Multi-layer physical sensors (`scripts/<target>-validate.sh` + `skills-suite-validate.sh`).
    7. $N_7$: Independent Skill Registry sensor executing `gentle-ai skill-registry refresh --force` (`exit code 0`).
    8. $N_8$: Clean auto-purge (`rm -f /var/www/artifacts/...`) and Engram LTM commit (`mem_save`).
  * Rejection Invariant: Delegating $N_7$ to installer side-effects or omitting any of the 8 nodes in Section 4 or Section 5 triggers immediate plan rejection.
- **Track B (Zerops Workload Deployment):**
  * Applies to: Application code, Zerops services, database migrations, CI/CD pipelines (`/var/www/{service}/`).
  * Versioning & Rollback: Native Git/GitHub commits, tags, and branches. Zero whole-repo `.bak` copies.
  * Agile Lifecycle: Structured execution steps adapted to the workload (e.g. Topology / Manifests, Provision / Migrations, Build / Deploy, E2E Verification & Healthcheck HTTP 200).
  * Mandatory Pre-Condition: `zcp-validate yaml <import.yaml>`.
  * Master Dispatch Umbrella Rule: Umbrella skills ([`bknd`](file:///var/www/.agents/skills/bknd/SKILL.md) and [`frnt`](file:///var/www/.agents/skills/frnt/SKILL.md)) operate strictly as routing tables, never as hostnames.
  * Domain Isolation: Operates exclusively on application code and Zerops service runtimes, isolating tooling files and SSoT infrastructure from application deploys.
- **Track C (Direct SSoT Data & Content Ops):**
  * Applies to: Direct modifications of business data, Markdown documents, brandbooks, JSON configurations, email templates, and assets in Google Drive (`/var/www/baiosfera/...`).
  * Versioning & Rollback: Google Drive native version history and trash. Zero `bak/` requirements.
  * Agile Content Lifecycle: Inspection / Grounding, Surgical Mutation, Integrity & Links Validation, LTM Commit via `mem_save`.

---

## 7. Certification & Invariance Gate (Anti-Churn Contract)

- **Source Standard:** Inherited from [`docu`](file:///var/www/.agents/skills/docu/SKILL.md) (`references/certification.md`).
- **Principle:** Auditing an existing skill does not mandate modifying it. When a skill already satisfies the 5 normative criteria:
  1. **Canonical Anatomy**: `SKILL.md`, `references/`, `assets/`, `scripts/`.
  2. **Token Economy**: Executive router $\le 550$ words ($\le 750$ tokens) for leaf skills, $\le 2500$ tokens for orchestrators.
  3. **Lossless Integrity**: Zero deletion of technical domain knowledge; modular offloading intact.
  4. **Positive Guidance**: Affirmative specifications, zero negative begs or emotional prohibitions.
  5. **Physical Harness Sensors**: Deterministic validator in `scripts/` returning `exit code 0`.
- **Verdict**: Declare the skill **`Certified Optimal / Invariant / Anti-Fragile`**, attest with physical sensors, and preserve 0 byte modifications on disk.

---

## 8. Artifacts Lifecycle & Archive Retention Policy

- **Core Principle:** Implementation and governance plans stored in `/var/www/artifacts/` serve strictly as construction scaffolds.
- **Immediate Superseded Purge:** Under the Cumulative Evolutionary Truth Protocol, version `_v(N+1)` is a strict superset of `_vN`. As soon as a newer version is executed, all prior versions (`*.superseded.md`) are immediately purged from both `/var/www/artifacts/` and `/var/www/artifacts/archive/`.
- **Active Session Retention for Executed Plans:** Upon successful completion of Phase F5, active plans are moved to `/var/www/artifacts/archive/<name>_vN.executed.md` and retained throughout the active session to provide immediate provenance, auditability, and context.
- **Session-End Archive Purge:** During the session close protocol (`mem_session_end`), all `*.executed.md` files in `/var/www/artifacts/archive/` are automatically purged to prevent context contamination in subsequent cold starts.
- **Handover Immunity Invariant:** Architectural assets matching `HANDOVER_PATTERN` (`_handover`, `_blueprint`, `_roadmap`, `_dossier`) are permanent and 100% immune to any automated purge or truncation routine.

