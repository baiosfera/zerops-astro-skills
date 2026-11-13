# Governance Contracts: Git-First SSoT & Clean Isolation (v11.0)

> **Standard:** Supreme Directive v9.1 · Positive Guidance · Zero Plaintext Secrets

---

## 1. Fuente Única de Verdad (Git-First, Sin `bak/` Manual)

Git es el sistema canónico de versionado y rollback para el upstream soberano:
- [`zerops-astrobranding`](file:///var/www/zerops-astrobranding/iniciar.sh): catálogo, recetas, blueprints, templates y scripts (`scripts/`, `bin/`).
- [`zerops-astro-skills`](file:///var/www/zerops-astro-skills): skills soberanas symlinkeadas a `/var/www/.agents/skills/` y `~/.gemini/antigravity-cli/skills/`.
- `baiosfera/runtime-*` + `template-astro-web`: plantillas agnósticas por runtime.

`iniciar.sh` sincroniza repos por Git (`--ff-only`) y enlaza binarios directamente desde `zerops-astrobranding/scripts/` hacia `/var/www/.bin/` y `/usr/local/bin/`. Evitar snapshots duplicados en carpetas `bak/` o copias desincronizadas en `localstorage/bin/`.

## 2. Aislamiento Multi-Tenant (Upstream vs Cliente)

- **Upstream (`baiosfera/*`)**: 100% libre de nombres, dossiers, manifiestos, tokens o variables reales de marcas o clientes.
- **Proyectos de Cliente**: Código en repo del cliente (`<marca>/<app>`); secretos en `zerops_env` (`$VAR` / `process.env`); archivo documental en `/var/www/baiosfera/PROYECTOS/<Marca>/` y llaves en `users-apis/<Marca>/<marca>-keys.md`; estado холодный de Engram en `/var/www/baiosfera/0ZEROPS-AGY/${ENGRAM_PROJECT}/engram`.

## 3. Verificación Sin Teatro

- Cada sensor reporta la verdad binaria y el alcance exacto ejecutado (`BEHAVIORALLY_VERIFIED` vs `SYNTAX_ONLY` vs `UNVERIFIED`).
- `ssot-parity-check` opera en modo **solo lectura** por defecto; sincronizar explícitamente con `--fix` solo cuando corresponda.
- `skills-suite-validate` distingue cuántas skills corrieron tests ejecutables reales frente a las que solo pasaron revisión sintáctica.
