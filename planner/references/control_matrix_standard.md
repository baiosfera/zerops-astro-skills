# Control Matrix & Honest Attestation Standard (v11.0)

Todo plan maestro concluye con criterios ejecutables por componente, distinguiendo claramente comprobación sintáctica de comportamiento en vivo.

## Esquema Estándar de Aceptación

| Componente / Alcance | Ruta Canónica | Sensor / Comando Real | Nivel de Prueba |
|---|---|---|---|
| **Gobernanza / Hooks** | `zerops-astrobranding/scripts/hooks/tool-guard.py` | `python3 -B .../tool-guard.py --test` | `BEHAVIORALLY_VERIFIED` |
| **Suite de Skills** | `zerops-astro-skills/` | `skills-suite-validate` | Separar `BEHAVIORALLY_VERIFIED` vs `SYNTAX_ONLY` |
| **Paridad Git / Symlinks** | `zerops-astrobranding` + `zerops-astro-skills` | `ssot-parity-check` (read-only) | `BEHAVIORALLY_VERIFIED` |
| **Runtime / Plantilla** | `baiosfera/runtime-*` o `/var/www/<svc>` | `bun test` / `pytest` / `go test` + `zerops_deploy` + `curl` | `BEHAVIORALLY_VERIFIED` |

## Reglas de Reporte F5
1. Incluir exclusivamente comandos ejecutados **después** de la última edición y su `exit code` real.
2. Etiquetar explícitamente cualquier componente sin suite ejecutable o sin deploy en vivo como `SYNTAX_ONLY` o `UNVERIFIED`.
3. Adjuntar esa evidencia exacta al parámetro `--evidence` de `linear-cli update-status <ID> Done`.
