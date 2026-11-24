# `meta-plan` — Infrastructure & Optional Linear Harness (v2.0)

---

## 1. Optional Linear CLI Safe Invocation

Use `linear-cli` only when explicitly requested by the user or inside unattended `hermes`/`paperclip` workflows. Always pass `LINEAR_SERVICE` pointing to an active local directory so stopped FUSE mounts under `/var/www/{service}` are never scanned:

```bash
LINEAR_SERVICE="zerops-astro-skills" linear-cli issue <ID>
LINEAR_SERVICE="zerops-astro-skills" linear-cli comment <ID> "<note>"
LINEAR_SERVICE="zerops-astro-skills" linear-cli update-status <ID> Done --evidence "<scoped command exit 0>"
```

`linear-cli` isolates `.linear_state/<PROJECT_NAME>/` per Zerops project and enforces `--evidence` on `Done` transitions without re-running unrelated test suites.

---

## 2. Scoped Verification Gates

Run only the sensors matching the modified surface:
- **Skills changed**: `skills-suite-validate` (structural `< 0.4s`, pass `--with-tests` when skill scripts changed).
- **Catalog / hooks / governance changed**: `tool-guard.py --test` and `ssot-parity-check`.
- **Runtime service changed**: `zcp run {hostname} <test-cmd>` (`bun test`, `pytest`, `go test`) + HTTP probe if applicable.
