---
name: gentle-pi
description: "Trigger: gentle-pi, pi.dev, pidev, gentle-shell, pi coding agent, gentle pi, astro-web coding. Sovereign Code Builder and Headless Developer Agent powered by Pi Coding Agent and Gentle Shell in Zerops."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `gentle-pi` — Sovereign Pi Coding Agent & Gentle Shell Orchestrator (v1.0)

## Activation Contract
Activate whenever authoring, generating, modifying, testing, or reviewing code for web applications (Astro 5 SSR, TypeScript, Tailwind 4, Bun) using the **Pi Coding Agent** (`pidev`) runtime, running interactive Gentle Shell sessions, executing headless coding tasks (`pi -p` / `pi --mode json`), or verifying code diffs against Zerops platform state.

## Hard Rules & Positive Guidance
- **Dedicated Runtime Isolation**: Pi executes strictly inside the `pidev` container (`ubuntu/nodejs@26`), never on the ZCP control plane.
- **Sovereign Code Builder Invariant**: Pi is the sole agent authorized to write and edit frontend/store application code in `/var/www/webdev`. AGY acts purely as the platform infrastructure builder.
- **Cluster Observability**: Pi queries Zerops platform state via native Zerops MCP tools (`zerops_logs`, `zerops_env`, `zerops_discover`, `zerops_verify`) declared in `.pi/mcp.json` without platform amnesia.
- **Direct Local Storage Access**: Pi accesses shared brandbook tokens, fonts, and assets directly via `/mnt/localstorage/pidev` and `/var/www/localstorage`.
- **Atomic Diff Generation**: Pi generates surgical unified diffs (`pi-tui`) with QuickJS sandboxed verification before writing to disk.
- **Task Delegation Protocol**: Tasks dispatched from Hermes arrive via NATS RPC on `rpc.coding.execute` or local FIFO queue, executing headlessly with exit code 0 attestation.
- **Zero Hallucination Gate**: Contrast every proposed library or component against actual dependencies in `/var/www/webdev/package.json`.

## Decision Gates

| Objective | Strategy | Reference |
|---|---|---|
| Interactive Coding & Split-Rail UI | Launch Gentle Shell / Pi TUI session | [`references/usage.md#interactive-mode`](file:///var/www/.agents/skills/gentle-pi/references/usage.md) |
| Headless Batch Execution | Run `pi -p` or JSON RPC mode | [`references/usage.md#headless-mode`](file:///var/www/.agents/skills/gentle-pi/references/usage.md) |
| Zerops MCP Integration | Configure `.pi/mcp.json` observational tools | [`references/infra.md#zerops-mcp`](file:///var/www/.agents/skills/gentle-pi/references/infra.md) |
| LocalStorage & Astro 5 Mounting | Seed POSIX mount and bind `/var/www` | [`references/infra.md#storage-mounts`](file:///var/www/.agents/skills/gentle-pi/references/infra.md) |

## Critical Workflows
1. Receive coding directive from Hermes or interactive prompt.
2. Inspect target codebase in `/var/www/webdev` and check live cluster state via Zerops MCP.
3. Apply surgical edits with QuickJS pre-flight verification.
4. Run physical tests inside container (`bun test`) and report verified diff.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/gentle-pi/references/usage.md) — CLI commands, split-rail interface, headless scripting, and ODD/RDD flows.
- [`references/infra.md`](file:///var/www/.agents/skills/gentle-pi/references/infra.md) — Node 26 runtime topology, Zerops MCP mesh, LocalStorage persistence, and systemd service.
