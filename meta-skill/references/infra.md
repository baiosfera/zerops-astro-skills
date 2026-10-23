# `meta-skill` Technical Architecture & Epistemic Standards

This document establishes the invariant technical requirements, role demarcations, and quality gates governing skills in the ecosystem.

---

## 1. Epistemic Inflow Invariant (Anti-AMN Gate)

1. **Mandatory Live Grounding**:
   - Every skill must reflect verified external reality (APIs, package versions, configuration flags, syntax).
   - Authoring or auditing skills based on unverified pre-trained memory (AMN) is strictly blocked by `tool-guard.py`.
2. **Subagent Delegation Standard**:
   - For multi-file skills or complex technology stacks, ground facts using dedicated `research` subagents.
   - The orchestrator maintains a thin thread and delegates deep retrieval to subagents.
3. **Compound Engine Triangulation**:
   - Cross-check findings across multiple independent engines (Exa neural search, Context7 live AST/types, Jina Reader verbatim markdown, Tavily documentation sitemaps).

---

## 2. Sovereign Role Demarcation Contract

To prevent architectural confusion and role overlap:

| Role / Entity | Exact Boundary | What It Does NOT Do |
|---|---|---|
| `research` | Epistemic search engine (12 live tools, subagents, raw dossiers) | Does NOT write markdown skill routers |
| `docu` | Canonical technical documentation and exact specification author | Does NOT perform Dual-RAG unbundling or router trimming |
| `cohalo` | Positive Guidance, deterministic prompt contracts, closed domains | Does NOT perform web search or scaffolding |
| `skill-improver` | Dual-RAG unbundling ($\le 480$ words), AST preservation, lossless offloading | Upstream package; never modified directly on disk |
| `skill-creator` | Clean-room scaffolding for new skill directories and YAML headers | Upstream package; never modified directly on disk |
| `writing-for-agents` | Interface seams, agent cognitive ergonomics, navigation friction | Does NOT author technical facts or API specs |
| `meta-skill` | Master orchestrator binding the end-to-end pipeline and enforcing physical gates | Does NOT replace the specialized sub-skills |

---

## 3. Dual-RAG Architecture & Progressive Disclosure

| Component | Strict Threshold | Rationale |
|---|---|---|
| Router (`SKILL.md`) | $\le$ 480 words (~550 tokens) | Prevents context window saturation; loaded on activation |
| Trigger Frontmatter | 3 to 10 specific, deterministic keywords | Eliminates false positive activations |
| Reference Modules | Modular files in `references/` ($\le$ 30KB) | JIT retrieval via file reading only when activated |
| Total References Depth | Bounded to 2 hierarchy levels | Prevents multi-hop reference confusion |

---

## 4. AST Preservation & Lossless Invariant

1. **AST Node Preservation**:
   - Every function, method, class, and exported type in associated scripts must retain its signature and implementation.
   - Placeholder comments (`// TODO`, `# pass`, `implement later`) are strictly prohibited.
2. **Deterministic Syntax Verification**:
   - Python code: `python3 -m py_compile <file>`
   - Bash scripts: `bash -n <file>`
   - TypeScript/JSON: Validated via compiler or runtime lint before committing.

---

## 5. Physical Validation Harness (Reality Over Checklist Theater)

Verification of skills is governed by physical assertions with exit code 0:
1. `skills-suite-validate`: Universally validates YAML frontmatter, router word budgets, and AST contracts across all 127+ skills.
2. `ssot-parity-check`: Asserts zero byte-level drift between local runtime, Google Drive SSoT, and GitHub repositories.
