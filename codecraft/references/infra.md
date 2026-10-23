# `codecraft` — Infrastructure & Harness Contracts

This document specifies the verification gates, risk tiers, and CoHaLo software engineering standards enforced during execution.

---

## 1. Proportional Verification Matrix

Every code change must be verified proportionally to the risk of what it touches.

| Risk Tier | Scope Criteria | Required Verification Sensor | Verifier Actor |
|---|---|---|---|
| **Passive** | Documentation, comments, markdown, images, static assets with zero executable impact | Structural readback, link validation, syntax lint | Author inline |
| **Medium** | Business logic, internal helpers, UI components covered by focused unit/integration tests | Focused test runner (`pytest`, `bun test`, `go test`), physical syntax check (`py_compile`, `bash -n`) | Author inline |
| **High** | Database migrations, auth, encryption, payment gateways, concurrency, API public contracts, shared infrastructure | Full test suite, end-to-end sensor (`skills-suite-validate`, `ssot-parity-check`), independent review | Independent verification worker / clean context |

### Rules of Engagement
- If a change touches both documentation and executable code, the entire change is classified by the highest applicable risk tier.
- If uncertain between two risk tiers, classify at the higher tier.
- A failing verification check permits at most one scoped correction batch. Never enter an infinite retry loop.

---

## 2. CoHaLo Software Engineering Harness

The Dual-Domain Invariant establishes distinct execution rules for executable code versus markdown instructions:

### Software & Scripts Domain (CoHaLo Engineering)
- **Zero Token/Word Limits**: Software source code, unit tests, and operational scripts must NEVER be artificially truncated or abbreviated to satisfy word budgets.
- **Physical Syntax Gates**: Before presenting or executing code, verify physical AST validity:
  * Python: `python3 -m py_compile <path>` (exit code 0 required).
  * Bash: `bash -n <path>` (exit code 0 required).
  * TypeScript / JavaScript: `bun build --no-bundle <path>` or `tsc --noEmit`.
- **Bounded State & Zero Mutable Globals**: Operational scripts must encapsulate state within functions or classes, avoiding mutable global variables that cause race conditions.
- **Deterministic Error Handling**: Never silence exceptions with bare `except: pass` or `2>/dev/null` unless explicitly testing error cases. Always log or propagate root causes.

### Prompts & Skills Domain (CoHaLo Prompting)
- **Positive Guidance**: Directives must be formulated as affirmative, closed-domain instructions describing what TO do, rather than unbounded negative prohibitions.
- **Dual-RAG Progressive Disclosure**:
  * Router `SKILL.md`: Lean, indexical, $\le$ 480 words (~550 tokens).
  * Deep Specifications: Relocated to `references/usage.md` and `references/infra.md`.
  * Production Assets: Stored in `assets/`.

---

## 3. Git Hygiene & Work-Unit Commits

Every discrete unit of work must be captured cleanly in version control:

- **Work-Unit Boundaries**: A single commit should represent one logical change (e.g., test + implementation + documentation update for one feature or bugfix).
- **Conventional Commits**: Format commit messages strictly according to Conventional Commits:
  * `feat(scope): ...`
  * `fix(scope): ...`
  * `refactor(scope): ...`
  * `test(scope): ...`
  * `chore(scope): ...`
- **Zero AI Attribution**: Never include `Co-Authored-By`, `Generated-by`, or AI assistant watermarks in commit bodies.
- **Working Tree Cleanliness**: Confirm `git status` shows a clean working tree before marking tasks complete.
