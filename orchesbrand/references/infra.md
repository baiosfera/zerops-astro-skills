# Orchesbrand: Infraestructura Modular, Aislamiento SSoT y Contrato PB19 (v4.5)

Este documento define la infraestructura de coordinación desacoplada y los contratos SSoT de `orchesbrand v4.5`.

---

## 1. Topología Desacoplada en Contenedores Aislados (`ZCP`)

`orchesbrand` funciona sin depender de archivos globales entre clientes ni de Oráculo obligatorio:

```
  [Dirección de Arte: chroma_spec.json + font_spec.json] (+ Opt-in --brief / --shards)
                                       │
        ┌──────────────┬───────────────┼───────────────┬──────────────┐
        ▼              ▼               ▼               ▼              ▼
 [chroma v8.0]   [fontgen v7.0]  [envato v5.1]  [symbol v2.0]  [kinetic v2.1]
        │              │               │               │              │
        └──────────────┴───────────────┼───────────────┴──────────────┘
                                       ▼
                <ws>/brand/{brandbook.json, brandbook-theme.css}
```

---

## 2. Aislamiento por Workspace y Paridad Byte-a-Byte

- **Salida Local Única:** Todo artefacto se escribe dentro de `--output-dir` o `<project_dir>/workspaces/<vertical>/brand/` sin directorios fantasma en `/mnt/localstorage`.
- **Paridad de Scripts:** `fontgen_engine.py v7.0` mantiene hash SHA-256 idéntico entre `/var/www/zerops-astrobranding/scripts/` y `/var/www/zerops-astro-skills/fontgen/scripts/` (libre de `__pycache__`).
- **Validación:** `orchesbrand --test` ejecuta el pipeline completo multimarca + ruta sin Oráculo en directorio temporal aislado.
