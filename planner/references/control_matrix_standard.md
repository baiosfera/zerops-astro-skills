# Planner Reference Manual: Control Matrix & Attestation Standard (v1.1)

Este manual establece la estructura normativa obligatoria para la **Matriz de Control y Criterios de Aceptación** que debe incluirse al final de cada plan maestro.

---

## 1. Obligatoriedad de la Matriz de Control

Todo plan diseñado bajo la skill `planner` DEBE culminar con una tabla estructurada que defina:
1. **Entregable / Componente:** El elemento técnico que se creará, mutará o eliminará.
2. **Ruta SSoT:** La ruta absoluta del archivo en el workspace (`/var/www/...`).
3. **Backup Pre-Mutación en `bak/`:** La ruta exacta del archivo individual `.bak` generado antes de mutar ($N_1$).
4. **Versión Semver:** La versión resultante del archivo (`v1.0`, `v5.3`, `v6.0`, etc.) ($N_3$).
5. **Sensor de Atestación Física:** El comando determinista que atestará el éxito de la operación (`exit code 0`, prueba CLI, `zerops_verify`) ($N_6, N_7$).

---

## 2. Esquema Estándar en Markdown (Track A: 8 Nodos Cerrados)

```markdown
## 5. 🚦 Matriz de Control y Criterios de Aceptación

| Nodo / Componente | Ruta SSoT | Backup en `bak/` | Versión Semver | Sensor de Atestación Física | Criterio de Aceptación |
|---|---|---|---|---|---|
| $N_1$: Backup Pre-Mutación | `bak/skills/<name>_v<ver>_<date>.bak/` | Sí (Plano O(1)) | N/A | `test -d <path>` | Directorio plano verificado en disco |
| $N_2$: Mapeo SSoT unisetup.sh | `0zcp-123/scripts/unisetup.sh` | N/A | N/A | `grep -q <target> unisetup.sh` | Paridad en contenedor virgen garantizada |
| $N_3$: Versión Semver | `/var/www/.agents/skills/<name>/SKILL.md` | N/A | **v#.#** | `grep 'version: "#.#"' SKILL.md` | Versión incrementada en frontmatter |
| $N_4$: Cero Eliminación & CoHaLo | `/var/www/.agents/skills/<name>/` | N/A | **v#.#** | `skill-improver` / `wc -w` | Sin pérdida de directivas, <750 tokens |
| $N_5$: Espejo Google Drive | `0zcp-123/.agents/skills/<name>/` | N/A | **v#.#** | `diff -rq <local> <drive>` | Cero drift en espejo permanente |
| $N_6$: Sensor Físico Individual | `scripts/<name>-validate.sh` | N/A | N/A | `bash scripts/<name>-validate.sh` | Sensor individual retorna exit code 0 |
| $N_7$: Skill Registry Sensor | `.atl/skill-registry.md` | N/A | N/A | `gentle-ai skill-registry refresh --force` | Catálogo actualizado sin errores |
| $N_8$: Auto-Purge & LTM | `/var/www/artifacts/<plan>*.md` | N/A | N/A | `ls /var/www/artifacts/` & `mem_save` | Planes purgados de disco & LTM commit |
```

---

## 3. Esquema Estándar en Markdown (Track B: Workloads)

```markdown
## 5. 🚦 Matriz de Control y Criterios de Aceptación

| Componente / Servicio | Ruta en Repositorio | Validación Previa | Sensor de Atestación | Criterio de Aceptación |
|---|---|---|---|---|
| Manifiesto Zerops | `/var/www/{service}/zerops.yaml` | `zcp-validate yaml` | `zerops_deploy` | Despliegue exitoso sin errores |
| Runtime de Servicio | `/var/www/{service}/` | Lint / Build local | `ssh {service} "npm test"` | Tests internos pasando (exit 0) |
| Healthcheck de Red | URL de Subdominio Zerops | `zerops_subdomain` | `curl -f -s -o /dev/null -w "%{http_code}" <url>` | HTTP 200 OK |
| Limpieza & LTM | `/var/www/artifacts/<plan>*.md` | N/A | `mem_save` | Auto-Purge ejecutado & LTM commit |
```
