# `docu` Infrastructure Standards & Verification Harness

This document specifies the standards for infrastructure documentation, environment variable specification, and physical truth verification.

---

## 1. Infrastructure Specifications Standard

When documenting infrastructure components (e.g. databases, message queues, AI gateways, caches):
1. **Topology & Sizing**:
   - Explicit container counts (`minContainers`, `maxContainers`).
   - CPU mode requirements (`cpuMode: SHARED` for frugal control plane; dedicated for compute).
   - Network bindings, internal private hostnames, and ports.
2. **Environment Variable Contracts**:
   - Exact variable names (e.g. `DATABASE_URL`, `VALKEY_HOST`, `BIFROST_API_KEY`).
   - Injection mechanisms: platform environment injection vs runtime secret.
   - Default values and required overrides.
3. **Storage & Mounts**:
   - Volume types (local persistent storage vs S3 object storage).
   - Absolute mount paths (e.g. `/var/www/localstorage`).

---

## 2. Physical Truth Verification Harness

Documentation is worthless if code examples fail to compile or execute:
1. **Syntax Assertions**:
   - Python code blocks must be verified via `python3 -m py_compile`.
   - Bash scripts must be verified via `bash -n`.
   - JSON payloads must parse cleanly via `json.loads()`.
2. **Zero Checklist Theater**:
   - Prohibit claiming a feature or tool works without observing a live exit code 0 or physical test output.
   - Any failure during verification must be traced to root cause rather than masked.
3. **Capability Sensor**:
   - All documented skills and reference files are attested through `skills-suite-validate` and `ssot-parity-check`.
