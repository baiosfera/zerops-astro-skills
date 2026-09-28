---
name: notebooklm
description: "Trigger: notebooklm, nlm, nlm-tutor, gemini notebook, jacob-bd, rag notebook, podcast notebooklm, studio create, nlm-vnc-login, auth refresh, compute quotas, usage_get. Orchestrates Gemini Notebook RAG with 49 FastMCP tools, Studio generation, and persistent Chrome sessions."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.3.0"
---

# Gemini Notebook — Autonomous Dual-RAG & Studio Orchestrator

## Activation Contract
Activate when orchestrating Gemini Notebook / Google NotebookLM via `nlm` CLI, 49 FastMCP tools, or `nlm-tutor` v2.2.0. Operates under an explicit 3-layer architecture: Capa 1 FastMCP/CLI (`notebooklm_tools`), Capa 2 Pedagogical (`nlm-tutor` immutable), and Capa 3 Router (`notebooklm` skill).

## Hard Rules
- **Google One AI Premium**: `NOTEBOOKLM_TIER_PRO_CONSUMER_USER` (300 sources/notebook, 500k words/source, 50 notebooks, Deep Research).
- **Cloud Studio Storage**: Artifacts reside in Google Cloud. Zero auto downloads; local downloads are manual and confined to `NOTEBOOKLM_DOWNLOAD_DIR`.
- **Custom Reports**: Always use `report_format='Create Your Own'`; canned formats discard `custom_prompt`.
- **Async Studio & Rename**: Launch with `--confirm -j`. Rename via `studio_status(action='rename')` ONLY after `status='completed'`.
- **Router-Reference Separation**: `SKILL.md` routes. Syntax in [`references/usage.md`](references/usage.md); infra in [`references/infra.md`](references/infra.md).
- **Sequential Ingestion**: Parameter `-f` accepts one file. Ingest sequentially via Bash loop with `--wait --wait-timeout 600`.
- **Compute Quotas & Zero Fees**: Track rolling (~5h) and weekly (7d) quotas. Uses Google One compute with zero external fees.
- **CoHaLo Harness**: Wrap commands with `timeout 10s` and background tasks with `WaitMsBeforeAsync: 10000`. Validate with `scripts/notebooklm-validate.sh` (`exit code 0`).

## Decision Gates

| Need | CLI Command (`nlm` / `nlm-tutor`) | FastMCP Tool | Reference |
|---|---|---|---|
| RAG Query | `nlm notebook query <UUID> "<P>"` | `notebook_query` | [`usage.md`](references/usage.md) |
| Socratic Tutor | `nlm-tutor session <UUID>` | `chat_configure` / `note` | [`usage.md`](references/usage.md) |
| Curricular Setup | `nlm-tutor setup <UUID>` | `studio_create` | [`usage.md`](references/usage.md) |
| Cross-Query | `nlm cross query "<Q>"` | `cross_notebook_query` | [`usage.md`](references/usage.md) |
| Ingestion | `nlm source add <UUID> -f <P>` | `source_add` | [`usage.md`](references/usage.md) |
| Studio Suite | `nlm <type> create <UUID>` | `studio_create` | [`usage.md`](references/usage.md) |
| Slide Revision | `studio_revise(notebook_id, artifact_id, ...)` | `studio_revise` | [`usage.md`](references/usage.md) |
| Download | `nlm download <type> <UUID> --id <ID>` | `download_artifact` | [`usage.md`](references/usage.md) |
| Export | `nlm export to-docs <UUID> <ID>` | `export_artifact` | [`usage.md`](references/usage.md) |
| Quotas | `nlm usage --json` | `usage_get` | [`infra.md`](references/infra.md) |
| Auth / noVNC | `nlm auth refresh` / `nlm-vnc-login` | `refresh_auth` | [`infra.md`](references/infra.md) |

## References
- [`references/usage.md`](references/usage.md) — 49 FastMCP tools, 43 file extensions, verified CLI syntax, Studio options, nlm-tutor v2.2.0.
- [`references/infra.md`](references/infra.md) — Google One AI Premium contract, cookie lifecycle (`__Secure-1PSIDTS`), CDP transport, compute quotas, CoHaLo harness.
- [`scripts/notebooklm-validate.sh`](scripts/notebooklm-validate.sh) — Deterministic physical sensor for skill integrity.
