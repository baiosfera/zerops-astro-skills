# `meta-system` — Usage & Implementation Guide

This guide establishes the operational procedures for authoring, auditing, and optimizing system-level directives, rules, and context architectures under Supreme Directive v8.4 and CoHaLo standards.

---

## 1. Directive Authoring Protocol

When authoring or modifying constitutional rules (such as `00-SUPREME-DIRECTIVE.md` or `AGENTS.md`):

1. **Calculate the Two Loads (`writing-for-agents`)**:
   - **Context Load**: The token cost of rules that are always loaded in the agent context. Every line costs attention on every turn. Prune relentlessly.
   - **Cognitive Load**: The effort required for humans and agents to navigate rules. Use clear signposting and tabular layouts.
2. **Determine Information Hierarchy**:
   - *In-Rule Step*: Core invariants that must be attended to on every turn (keep under 50 lines).
   - *Disclosed Reference*: Detailed historical context, encyclopedias, or expansive examples moved to `.agents/references/` or `references/`.
3. **Formulate Checkable Completion Criteria**:
   - Every invariant must name its physical sensor (e.g. `skills-suite-validate`, `ssot-parity-check`, `bun test`, `pytest`).
   - Eliminate vague expectations like "ensure quality" in favor of deterministic assertions like "assert exit code 0".

---

## 2. Positive Guidance Refactor Protocol

Transform open-ended negative prohibitions into deterministic, closed-domain contracts:

| Negative / Prohibitive Antipattern | Affirmative Positive Guidance Contract | Mechanical Benefit |
|---|---|---|
| *"Never hallucinate APIs or limits"* | *"Anchor all technical assertions in live primary sources (`date -u`, Context7, Exa verbatim) or physical inspection (`zerops_discover`)."* | Gives the agent an actionable execution path instead of an abstract fear. |
| *"Don't write untested code"* | *"Execute TDD test-first: author the failing test (Red), implement minimal logic (Green), clean structure (Refactor)."* | Enforces physical execution sequence. |
| *"Never respond in chat without proof"* | *"Persist all architectural findings in Linear (`linear-cli comment`) and Engram (`mem_save`) before delivering the response in chat."* | Creates audit trail and eliminates ephemeral loss. |
| *"Don't auto-scale ZCP"* | *"Maintain ZCP strictly at 1 single container (`minContainers: 1, maxContainers: 1`) in `cpuMode: SHARED`."* | Prevents split-brain by setting exact configuration parameters. |
| *"Do not truncate code to fit tokens"* | *"Develop software and scripts with full AST depth and zero arbitrary line/token limits (CoHaLo Engineering)."* | Eliminates mutilated code and stub comments. |

---

## 3. Cognitive Doc Design for System Rules

To maximize agent adherence and human review velocity:

1. **Lead with the Decision**: Put the outcome and rule first; background context belongs in references.
2. **Recognition over Recall**: Replace paragraph prose with structured markdown tables displaying State, Action, Sensor, and Evidentiary Proof.
3. **Chunking**: Group related invariants into numbered blocks (e.g., *Execution State Machine*, *7 Sovereign Invariants*).
4. **Review Empathy**: Allow a human or verifier agent to evaluate rule compliance in under 10 seconds.

---

## 4. Architectural Decision Records (ADR) Governance

When an architectural decision permanently alters ecosystem behavior:

1. **Identify the Seam**: A technology migration, storage invariant, or gateway protocol change.
2. **Draft the Record**:
   - **Title**: `ADR-<NUMBER>: <Decision Title>`
   - **Context**: Problem statement, active constraints, and evaluated alternatives.
   - **Decision**: The selected path and technical justification.
   - **Consequences**: Positive tradeoffs, eliminated risks, and operational responsibilities.
3. **Link to SSoT**: Persist in `.agents/references/adr/` or project knowledge base and record in Engram via `mem_save`.
