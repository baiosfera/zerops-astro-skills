# Brandbook: Topología de Persistencia y Validación SSoT (`v2.0`)

- **Workspace Canónico por Vertical:** `/var/www/localstorage/<Proyecto>/dev/workspaces/<vertical>/brand/` (`brandbook.json` + `brandbook-theme.css`).
- **Espejo Drive SSoT (cuando existe proyecto en Drive):** `/var/www/baiosfera/PROYECTOS/<Proyecto>/dev/workspaces/<vertical>/brand/`.
- **Compilador de Fusión:** `/var/www/zerops-astrobranding/bin/orchesbrand` (`merge_brandbook_non_destructive`).
- **Bootstrap Superfull (Oráculo):** `scripts/brandbook_pipeline_runner.py`.
- **Certificación:** `orchesbrand --test` + `python3 -B -m py_compile`.
