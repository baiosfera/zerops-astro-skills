# `docu` Usage Guide: Canonical Technical Documentation & Verification

This manual details how `docu` transforms raw empirical findings from `research` into authoritative, production-grade technical specifications.

---

## 1. Research Ingestion Protocol

When `research` completes its investigation (via subagents or compound tool execution):
1. **Source Inspection**: Read the research dossier (`/var/www/artifacts/*_research_report.md`) or tool findings verbatim.
2. **Fact Triangulation**:
   - Verify official package versions (e.g. Bun 1.3+, PostgreSQL 18, NATS 2.12).
   - Identify breaking changes compared to earlier major versions.
   - Extract exact configuration keys, CLI arguments, and environment variables.
3. **Contrast with Code**: Compare the extracted reality against local codebase implementations or existing skill instructions to flag discrepancies, deprecations, or broken syntax.

---

## 2. API & Contract Specifications Standard

Every technical spec authored by `docu` must provide concrete, runnable contracts:
1. **HTTP/RPC Endpoints**:
   - Exact URI and HTTP method.
   - Required headers (Authentication, Content-Type, idempotency keys).
   - Minimal runnable `curl` command.
2. **Payload Schemas**:
   - Verbatim JSON request and response payloads.
   - Accurate TypeScript interfaces or Pydantic models matching live library exports.
3. **Error Matrix & Recovery**:
   - Document every known status code (400, 401, 404, 429, 500).
   - Explicit recovery actions for each failure mode (e.g., exponential backoff, key rotation).

---

## 3. Hand-off Lifecycle

`docu` operates as the bridge between raw external research and structured skill deployment:
```
[research] ──(Dossiers)──> [docu] ──(Exact Specs)──> [cohalo] ──(Positive Guidance)──> [skill-improver]
```
1. `docu` outputs verified technical truth to `references/usage.md` and `references/infra.md`.
2. `cohalo` refines tone and prompt framing into positive affirmative guidance.
3. `skill-improver` ensures the router (`SKILL.md`) stays under 480 words and preserves AST code.
