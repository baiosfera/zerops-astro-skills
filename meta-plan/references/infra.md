# `meta-plan` — Infrastructure & Harness Contracts

This document specifies the CLI harnesses, issue lifecycle states, and physical attestation requirements governing `meta-plan`.

---

## 1. Linear CLI Safe Invocation Harness

When executing `linear-cli` commands inside Zerops ZCP control plane, stopped runtime containers can leave disconnected FUSE SSHFS mount points at `/var/www/{service}`, causing directory scans to hang in kernel `request_wait_answer`.

To guarantee non-blocking, deterministic CLI execution:

```bash
# ALWAYS prefix linear-cli invocations with LINEAR_SERVICE targeting an active or sovereign directory
LINEAR_SERVICE="zerops-astro-skills" linear-cli issue <ID>
LINEAR_SERVICE="zerops-astro-skills" linear-cli comment <ID> "<note>"
LINEAR_SERVICE="zerops-astro-skills" linear-cli update-status <ID> "<status>" [--evidence "<proof>"]
```

---

## 2. Issue Lifecycle & Physical Attestation Gates

Transitions between issue states must be backed by verifiable reality:

| Transition | Required Evidence / Precondition | Sensor |
|---|---|---|
| **Todo $\to$ In Progress** | Scope defined, acceptance criteria established in Linear description. | Initial verification |
| **In Progress $\to$ In Progress (Checkpoint)** | Architectural findings and intermediate discoveries recorded. | `linear-cli comment` + `mem_save` |
| **In Progress $\to$ Done** | Universal sensors pass with exit code 0; physical test commands executed. Must provide `--evidence`. | `skills-suite-validate` · `ssot-parity-check` |

### Closure Contract

Closing an issue (`Done`) without `--evidence` is strictly rejected by the CLI and platform governance. The `--evidence` argument must contain the exact command, exit code, and test summary:

```bash
LINEAR_SERVICE="zerops-astro-skills" linear-cli update-status BAI-348 Done \
  --evidence "skills-suite-validate passed (125/125 exit 0). ssot-parity-check passed (exit 0)."
```

---

## 3. Sovereign SSoT Synchronization Architecture

All additions or updates to planning templates, meta-skills, or constitutional directives must maintain strict tripartite parity:

1. **Local Working Tree (`/var/www/zerops-astro-skills/`)**:
   - Active development workspace.
2. **Global Agent Customizations (`/var/www/.agents/skills/`)**:
   - Runtime discovery directory for AI agents.
3. **Google Drive SSoT (`/var/www/baiosfera/0ZEROPS-AGY/0zcp-123/`)**:
   - Immutable off-platform persistence.

Execute `ssot-parity-check` to verify that all three surfaces remain in bit-for-bit synchronization.
