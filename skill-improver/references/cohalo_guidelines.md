# CoHaLo & Token Optimization Guidelines for Skill Architecture

Authoritative specification for auditing and refactoring skills under CoHaLo (Context, Harness, Loop) and LLM-first token engineering.

---

## 1. Pure Positive Guidance (Transformer Attention Alignment)

### 1.1 The Theoretical Foundation
In modern transformer architectures (multi-head self-attention $Q, K, V$), negation operators ("do not", "never", "avoid") allocate attention heads directly to the negated semantic token (the "Pink Elephant Effect"). The attention mechanism lacks native negative polarity; mentioning an undesired concept primes the model toward that concept in subsequent token generation.

### 1.2 Affirmative Closed-Domain Formulation
Replace negative directives with explicit, affirmative, and closed-domain operational bounds:

| Antipattern (Attention Distortion) | CoHaLo Formulation (Affirmative Closed Domain) |
|---|---|
| Ambiguous raw query advice | "Execute queries exclusively via the typed query builder or ORM interface." |
| File deletion warnings | "Retain all existing files; request explicit user authorization before removal." |
| Unverified endpoint assumptions | "Verify every route against the live primary OpenAPI schema prior to invocation." |
| Abstract prohibitive text | "Formulate directives using positive, deterministic constraints exclusively." |

---

## 2. LLM Token & Cache Optimization (Without Mutilation)

### 2.1 Preservation Over Mutilation Invariant
Token optimization must never mean summarizing, suppressing, or castrating technical depth. Technical contracts, parameter schemas, edge cases, and architectural invariants must remain 100% complete.

### 2.2 Dual-RAG Progressive Disclosure Architecture
Skills achieve radical token efficiency without knowledge loss by separating routing from depth:

```
skill-directory/
├── SKILL.md            <-- The Router (180–450 tokens): When to activate, hard rules, decision table
└── references/         <-- The Depth Lake: Exhaustive documentation loaded strictly on demand
    ├── api_schema.md   <-- Loaded only when implementing the API
    └── patterns.md     <-- Loaded only when architecting the module
```

1. **The Router (`SKILL.md`)**:
   - Concise activation contract and triggers.
   - Essential hard rules formulated affirmatively.
   - Compact decision tables instead of narrative branching prose.
   - Explicit pointers to local `references/` for detailed implementation schemas.
2. **The References (`references/`)**:
   - Preserves complete schemas, full code examples, and exhaustive parameter documentation verbatim.
   - The LLM reads only the specific reference required for the active subtask, reducing base context consumption by 70–85%.

### 2.3 KV Cache Alignment
- **Prefix Invariance**: Keep static instructions, tools, and skill definitions completely deterministic. Maintain prompt prefix stability.
- **Cache Hit Maximization**: Stable prefixes allow provider KV caching (e.g. Gemini Context Caching, Claude Prompt Caching) to serve up to 90% of prompt tokens at sub-second latency and fraction of standard cost.
