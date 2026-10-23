---
name: docu
description: "Trigger: docu, documentar, canonical specs, api documentation, truth documentalist, reference builder, technical specifications. Ingests research dossiers to author verified technical documentation and canonical specifications."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "9.0"
---

# `docu` — Autonomous Technical Truth & Canonical Reference Documentalist (v9.0)

## Activation Contract
Activate when ingesting research dossiers from `research` to author canonical technical specifications, reference manuals, or live API contracts. Contrasts local code against verified external reality. Focuses on factual technical truth; leaves Dual-RAG structural unbundling to `skill-improver` and prompt framing to `cohalo`.

## Hard Rules & Positive Guidance
- **Factual Grounding Supremacy**: Base all documented APIs, types, flags, and configurations strictly on verified external research dossiers from `research` (Context7, Exa, Jina, Tavily).
- **Exact Specifications (Zero Hand-Waving)**: Document complete curl requests, JSON payload schemas, environment variables, error codes, and recovery procedures with verbatim fidelity.
- **Role Boundary (Truth vs Structure)**: Author deep, exhaustive technical references in `references/usage.md` and `references/infra.md`. Leave router word budget trimming and AST unbundling strictly to `skill-improver`.
- **Reality Over Checklist Theater**: Verify that every documented code snippet passes physical syntax checks (`python3 -m py_compile` or `bash -n`).
- **Physical Attestation**: Validate documentation integrity via `skills-suite-validate` (exit code 0).

## Decision Gates

| Task / Need | Action / Protocol | Reference |
|---|---|---|
| **Research Ingestion** | Ingest raw research findings into structured facts | [`references/usage.md#1-ingestion`](file:///var/www/zerops-astro-skills/docu/references/usage.md) |
| **API & Contract Specs** | Author exhaustive curl, JSON, and type contracts | [`references/usage.md#2-contracts`](file:///var/www/zerops-astro-skills/docu/references/usage.md) |
| **Infra & Env Specs** | Document environment variables, quotas, and limits | [`references/infra.md#1-infra-specs`](file:///var/www/zerops-astro-skills/docu/references/infra.md) |
| **Truth Verification** | Validate code examples and syntax physically | [`references/infra.md#2-verification`](file:///var/www/zerops-astro-skills/docu/references/infra.md) |
| **Universal Sensor** | Execute universal capability sensor | `skills-suite-validate` |

## Commands
```bash
# Validate skill suite physical integrity
skills-suite-validate
```

## Resources
- [`references/usage.md`](file:///var/www/zerops-astro-skills/docu/references/usage.md) · [`references/infra.md`](file:///var/www/zerops-astro-skills/docu/references/infra.md)
