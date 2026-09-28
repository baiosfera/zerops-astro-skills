# Astrological Suite Infrastructure & Storage Specification (Dual-RAG SSoT V13.0)

Este documento formaliza la infraestructura, dependencias de sistema, variables de entorno, topología canónica de almacenamiento sharded y el arnés de ejecución CoHaLo fractal para la suite de skills de Oráculo.

---

## 1. Requisitos de Entorno y Runtime
- **Sistema Operativo Base:** Linux Ubuntu 24.04+ LTS / Debian 12 / Alpine Linux (glibc/musl).
- **Runtimes de Ejecución:**
  - `python3` (v3.12+): Con librerías estándar y dependencias de alto rendimiento: `httpx` (HTTP/2), `pydantic` (v2), `mcp` (Python SDK), `asyncio`, `zoneinfo`.
  - `uv` / `uvx`: Gestor de paquetes ultrarrápido para los servidores MCP locales (`lunar-mcp-server`, `zmanim-mcp`).
  - `node` (v20+) & `npx`: Conector `mcp-remote` para el servidor MCP de Kundali Jyotish.

---

## 2. Diccionario Canónico de Variables de Entorno & Jerarquía de Precedencia

El pipeline lee las credenciales del entorno inyectadas por Zerops respetando la jerarquía de precedencia canónica:

| Proveedor | Variable Primaria (Mayúsculas) | Variable Secundaria (CamelCase) | Nivel / Cuota Asignada |
|---|---|---|---|
| **FreeAstroAPI** | `$FREEASTROAPI_KEY` | `$freeastroapi_key` | Plan Astro Entry (50.000 req/mes) |
| **AstroWay REST** | `$ASTROWAY_API_KEY` | `$astroway_apiKey` | Plan Indie PRO (50.000 créditos/mes) |
| **Astrology-API.io** | `$ASTROLOGY_API_KEY` | `$astrology_apiKey` | Plan V3 Developer |
| **VedAstro PRO** | `$VEDASTRO_API_KEY` | `$vedastro_apiKey` | PRO Key (Sin costo marginal) |
| **NASA JPL Horizons** | `$NASA_API_KEY` | `$nasa_apiKey` | Open API Key (Fallback: `DEMO_KEY`) |
| **Kundali MCP** | `$KUNDALI_MCP_KEY` | `$kundali_mcpKey` | Sovereign MCP Remote Key |

---

## 3. Políticas de Rate-Limiting & Concurrencia (Token Bucket)

Para garantizar la integridad de las cuotas y evitar bloqueos HTTP 429:

| Proveedor | Tasa Máxima | Intervalo Mínimo | Protocolo de Transporte |
|---|---|---|---|
| **FreeAstroAPI** | 4.0 req/s | `sleep 0.25` | HTTP/2 Persistent (`httpx`) |
| **AstroWay REST** | 0.5 req/s | `sleep 2.5` | HTTP/2 Persistent (`httpx`) + Header Monitoring |
| **Astrology-API.io** | 1.0 req/s | `sleep 1.0` | HTTP/2 Persistent (`httpx`) |
| **VedAstro PRO** | 1.5 req/s | `sleep 0.6` | HTTP/2 Persistent (`httpx`) |
| **NASA JPL Horizons** | 2.0 req/s | `sleep 0.5` | HTTP/2 Persistent (`httpx`) |
| **HebCal REST** | 2.0 req/s | `sleep 0.5` | HTTP/2 Persistent (`httpx`) |

---

## 4. Protocolo de Resolución Dinámica de Almacenamiento

La suite resuelve dinámicamente la ruta de almacenamiento de forma agnóstica y transparente tanto en entornos con volúmenes NFS/SeaweedFS montados como en almacenamiento local del workspace:

```bash
resolve_astro_storage() {
    if [ -n "${ASTRO_STORAGE_DIR:-}" ] && [ -d "$ASTRO_STORAGE_DIR" ]; then
        echo "$ASTRO_STORAGE_DIR"
        return
    fi
    for m in /mnt/*; do
        if [ -d "$m" ] && [ "$(basename "$m")" != "lost+found" ] && [ "$m" != "/mnt/*" ]; then
            local target="$m/astrologia"
            mkdir -p "$target" 2>/dev/null || true
            echo "$target"
            return
        fi
    done
    local local_target="/var/www/baiosfera/ASTROLOGÍA"
    mkdir -p "$local_target" 2>/dev/null || true
    echo "$local_target"
}
```

### Estructura Canónica Sharded SSoT por Consultante:
```
<ASTRO_STORAGE_DIR>/DIAG/<CLIENTE_ID>/
├── raw/
│   ├── json/
│   │   ├── dumps/                      # 10 Shards JSON matemáticos puros (REST + MCP)
│   │   └── caches/                     # Caché SHA-256 de respuestas crudas por proveedor
│   ├── feeds/                          # 9 Feeds Markdown quirúrgicos (<2.5 KB) para Fases 1 a 9
│   └── llm/
│       ├── coach_technical_sheet.md    # 12 secciones matemáticas puras (SSoT Fase 0)
│       ├── fase0_author_psychology.md  # Constitución Ontológica del Autor
│       ├── extraction_health_audit.md  # Auditoría Financiera y Créditos de APIs
│       ├── coach_dashboard_<ID>.md     # Fase 10 (Estrategia de Mentoría, Uso Interno)
│       └── astrobranding_semiotics.md  # Fase 11 (Puente Semiótico para Orchesbrand)
├── fases/
│   ├── fase1_num.md                    # Reporte Fase 1 (Numerología Multidimensional)
│   ├── fase2_occ.md                    # Reporte Fase 2 (Occidental Tropical)
│   ├── fase3_sid.md                    # Reporte Fase 3 (Sideral Campanus)
│   ├── fase4_ved.md                    # Reporte Fase 4 (Védica Jyotish & KP)
│   ├── fase5_bazi.md                   # Reporte Fase 5 (BaZi Chino)
│   ├── fase6_kab.md                    # Reporte Fase 6 (Kabbalah Kármica)
│   ├── fase7_voc.md                    # Reporte Fase 7 (Clímax Vocacional y Negocio)
│   ├── fase8_time.md                   # Reporte Fase 8 (Expansión del Tiempo)
│   ├── fase9_end.md                    # Reporte Fase 9 (Cierre y Mentoría 1:1)
│   └── fase1_9_combined.md             # Reporte Consolidado Sanitizado (PDF/App View)
└── Notebook/                           # Reportes RAG descargados desde Google NotebookLM
```

---

## 5. Higiene de Procesos, Escudo del Filesystem & Arnés CoHaLo Fractal

En estricto cumplimiento de la Ley de Isomorfismo Fractal de CoHaLo:

### Arnés de Ejecución y Timeouts:
- **Timeouts Acotados:** `timeout 15s` en llamadas de red hacia APIs externas; `timeout 10s` en operaciones locales de terminal.
- **Synchronous Wait Enforcement:** Toda llamada de terminal debe usar `WaitMsBeforeAsync: 10000` para comandos síncronos.
- **Zero Orphaned Tasks Invariant:** Cualquier tarea en background debe ser terminada con `manage_task action="kill"` al concluir su ciclo.

### Sensores de Atestación & Circuit Breakers:
- **Sensor de Integridad HTTP:** Validar código 200 y presencia de claves de negocio antes de persistir respuestas en disco.
- **Sensor de Formato Shards & Feeds:** Verificar que los 10 archivos `.json` en `dumps/` y los 9 `.md` en `feeds/` existan con tamaño $> 0$ bytes.
- **Circuit Breakers y Retries:** Límite estricto de 2 reintentos ante fallos temporales (HTTP 500, timeouts) con backoff exponencial.
