# Omni Engine Reference Manual: Protocolo de Ejecución y Opciones CLI (SSoT V13.0)

> **Documento Canónico:** `/var/www/.agents/skills/oraculo/references/omni_engine.md`  
> **Skill Gobernativa:** [`oraculo`](file:///var/www/.agents/skills/oraculo/SKILL.md)  
> **Estándar:** CoHaLo v6.8, Positive Guidance & Zero Deletion Invariant.

---

## 1. Protocolo de Activación por Lenguaje Natural

Cuando el usuario expresa una instrucción en lenguaje natural, tal como:
- `"ejecuta oraculo en juan.txt"` o `"ejecuta oraculo en /var/www/juan.txt"`
- `"ejecuta oraculo solo fase0 para juan.txt"`
- `"fase 0 para cliente.txt"`

El agente resuelve y ejecuta autónomamente el pipeline invocando de forma directa:
```bash
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py "<ruta_al_archivo>"
# O mediante el wrapper directo:
bash /var/www/.agents/skills/oraculo/scripts/fase0.sh "<ruta_al_archivo>"
```

> **Cláusula Fast-Path Anti-Parálisis:**  
> La inexistencia previa de carpetas `raw/`, `json/` o `feeds/` en el directorio del consultante es la condición normal de partida. El agente no debe explorar directorios del sistema, buscar backups, ni intentar sintetizar archivos vacíos manualmente. La invocación directa de `omni_engine.py` (o `scripts/fase0.sh`) realiza la extracción remota/local y compila la totalidad del Data Lake y Fase 0 de forma atómica.

### Flujo de Orquestación Interna Unificada (`omni_engine.py`):
1. **Lectura y Parsing Agnóstico**: Lee y parsea de forma resiliente el archivo de entrada (`.txt`, `.json` o `.md`), identificando fecha, hora, coordenadas y marcas comerciales sin suposiciones ni PII hardcodeado.
2. **Resolución Determinista de Directorio**: Resuelve la carpeta de destino en `/var/www/baiosfera/ASTROLOGÍA/DIAG/` aplicando la precedencia canónica:
   - **Prioridad 1:** Si hay nombre individual y marca $\rightarrow$ `NOMBRE_MARCA` (ej: `JUAN_DAMAREN`).
   - **Prioridad 2:** Si solo hay nombre individual $\rightarrow$ `NOMBRE` (ej: `JUAN`).
   - **Prioridad 3:** Si solo hay marca $\rightarrow$ `MARCA` (ej: `DAMAREN`).
   - **Fallback:** Nombre sanitizado o parámetro `--client-dir` explícito.
3. **Invocación del Pipeline Asíncrono en Memoria**:
   - `omni_engine.py` ejecuta directamente `asyncio.run(run_pipeline(profile, out_dir))` delegando en [`pipeline/orchestrator.py`](file:///var/www/.agents/skills/oraculo/pipeline/orchestrator.py).
   - Un único proceso Python 3.12 orquesta con `asyncio.TaskGroup` las 6 APIs REST (FreeAstroAPI, AstroWay, Astrology-API.io, VedAstro, NASA Horizons, HebCal) y los 3 servidores MCP (Lunar, Kundali, Zmanim).
4. **Consenso Canónico & Sharding Atómico**:
   - Transforma los datos en memoria delegando cálculos a las APIs oficiales (Chara Karakas a AstroWay, Numerología a FreeAstroAPI/Astrology-API.io, Skipped Steps a AstroWay).
   - Genera atómicamente los **10 Shards JSON** en `raw/json/dumps/`, los **9 Feeds Markdown** en `raw/feeds/` (<2.5 KB) y los **3 reportes LLM** en `raw/llm/`.
5. **Confirmación Inmediata de Fase 0**: Habilita a los agentes downstream (`oraculo-diag-a-psy` a `e-geo` y `orchesbrand`) a leer directamente desde el SSoT en disco.

---

## 2. Protocolo de Ejecución de Fase 0 (`omni_engine.py`)

### Opción A (Canónica): Archivo de Consultante (`.txt`, `.json`, `.md`)
```bash
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py /var/www/consultante.txt
```

#### Formato Agnóstico Universal Soportado:
```text
nombre: <NOMBRE_COMPLETO>
nombre_reporte: <NOMBRE_CORTO_O_TRATO>
marca: <NOMBRE_MARCA> (opcional)
fecha: <YYYY-MM-DD>
hora: <HH:MM>
latitud: <LAT_DECIMAL>
longitud: <LON_DECIMAL>
zona: <IANA_TIMEZONE>
ciudad: <CIUDAD_NATAL>
sexo: <F|M> (opcional)
```

---

### Opción B: Invocación con Banderas CLI Explícitas
```bash
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py \
  --client-dir "/var/www/baiosfera/ASTROLOGÍA/DIAG/<CLIENT_ID>" \
  --dob "<YYYY-MM-DD>" \
  --tob "<HH:MM>" \
  --lat <LAT_FLOAT> \
  --lon <LON_FLOAT> \
  --tz "<IANA_TIMEZONE>" \
  --city "<CIUDAD>" \
  --names "<NOMBRE_NATAL_COMPLETO>" \
  --brand-names "<MARCA_1>, <MARCA_2>"
```

#### Catálogo Completo de Banderas CLI:
- `file_pos` o `--file` (`-f`): Ruta a archivo de datos del consultante (`.txt`, `.json`, `.md`).
- `--client-dir`: Directorio destino del consultante (genera `raw/json/dumps/`, `raw/feeds/` y `raw/llm/`).
- `--dob`: Fecha de nacimiento (`YYYY-MM-DD`).
- `--tob`: Hora de nacimiento en formato 24h (`HH:MM`).
- `--lat`: Latitud decimal (e.g. `4.7110`).
- `--lon`: Longitud decimal (e.g. `-74.0721`).
- `--tz`: Zona horaria IANA canónica (e.g. `America/Bogota`).
- `--city`: Ciudad natal (e.g. `Bogota`).
- `--names`: Nombre de nacimiento completo (utilizado en numerología multidimensional).
- `--birth-name`: Nombre legal o natal del consultante (Bloque B1).
- `--current-name`: Nombre actual o elegido del consultante (Bloque B2).
- `--spoken`: Nombre de trato preferido para el reporte didáctico.
- `--brand-names`: Nombres comerciales opcionales separados por coma para numerología de marca (Bloque C).
- `--refresh-pro`: Fuerza la re-extracción remota invalidando la caché SHA-256 en disco.
- `--dry-run`: Ejecuta el consenso y sharding matemático determinista sin consumir cuotas de API.
