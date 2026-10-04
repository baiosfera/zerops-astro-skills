# Omni Engine Reference Manual: Protocolo de Ejecución y Opciones CLI (SSoT v6.3)

> **Documento Canónico:** `/var/www/.agents/skills/oraculo/references/omni_engine.md`  
> **Skill Gobernativa:** [`oraculo`](file:///var/www/.agents/skills/oraculo/SKILL.md)  
> **Estándar:** Canon 12-15-9-4, CoHaLo v8.4, Positive Guidance & Zero Deletion Invariant.

---

## 1. Protocolo de Activación por Lenguaje Natural

Cuando el usuario expresa una instrucción en lenguaje natural, tal como:
- `"ejecuta oraculo en juan.txt"` o `"ejecuta oraculo en /var/www/juan.txt"`
- `"ejecuta oraculo solo fase0 para juan.txt"`
- `"compila el cache de catalina con -c"`
- `"sintetiza los reportes de marca con -s"`
- `"fase 0 para cliente.txt"`

El agente resuelve y ejecuta autónomamente el pipeline invocando de forma directa:
```bash
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py "<ruta_al_archivo>"
# O con banderas específicas de capa desacoplada:
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py --client-dir "<ruta_dir>" -c
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py --client-dir "<ruta_dir>" -s
```

> **Cláusula Fast-Path Anti-Parálisis:**  
> La inexistencia previa de carpetas `raw/`, `json/` o `feeds/` en el directorio del consultante es la condición normal de partida. El agente no debe explorar directorios del sistema, buscar backups, ni intentar sintetizar archivos vacíos manualmente. La invocación directa de `omni_engine.py` realiza la extracción remota/local y compila la totalidad del Data Lake y Fase 0 de forma atómica.

---

## 2. Arquitectura Desacoplada del Pipeline (`pipeline/`)

El pipeline v6.3 opera bajo una separación estricta de responsabilidades en 4 capas desacopladas:

1. **Lectura y Parsing Agnóstico**:
   - Lee y parsea de forma resiliente el archivo de entrada (`.txt`, `.json` o `.md`), identificando fecha, hora, coordenadas y marcas comerciales sin suposiciones ni PII hardcodeado.
2. **Resolución Determinista de Directorio**:
   - Resuelve la carpeta de destino en `/var/www/baiosfera/ASTROLOGÍA/DIAG/` aplicando la precedencia canónica:
     * **Prioridad 1:** Si hay nombre individual y marca $\rightarrow$ `NOMBRE_MARCA` (ej: `JUAN_DAMAREN`).
     * **Prioridad 2:** Si solo hay nombre individual $\rightarrow$ `NOMBRE` (ej: `JUAN`).
     * **Prioridad 3:** Si solo hay marca $\rightarrow$ `MARCA` (ej: `DAMAREN`).
     * **Fallback:** Nombre sanitizado o parámetro `--client-dir` explícito.
3. **Capa Ingestion / Inflow (`-x` / Extracción)**:
   - Orquesta mediante `pipeline/cache_crawler.py` el rastreo dinámico de endpoints REST (FreeAstroAPI, AstroWay, Astrology-API.io, VedAstro, NASA Horizons, HebCal) y servidores MCP (Lunar, Kundali, Zmanim).
   - Genera caché estructurada en `raw/json/cache/<proveedor>/` con deduplicación por hash SHA-256.
4. **Capa Oro (`-c` / `--compile` - `SharderEngine`)**:
   - Orquesta los 9 motores de dominio en `pipeline/domains/` (`numerology.py`, `western_tropical.py`, `western_sidereal.py`, `vedic_jyotish.py`, `bazi_chinese.py`, `human_design.py`, `kabbalah_hermetic.py`, `timing_dashas.py`, `geo_acg.py`).
   - Genera atómicamente los **12 Shards Físicos Bronze JSON** en `raw/json/dumps/`, los **15 Shards Relacionales Silver** para PostgreSQL y los **9 Feeds Quirúrgicos Markdown** en `raw/feeds/` (<2.5 KB).
   - No genera reportes interpretativos LLM ni consume tokens de síntesis.
5. **Capa Platino (`-s` / `--synthesis` - `SynthesisEngine`)**:
   - Consume exclusivamente la Capa Oro (`raw/feeds/` y `raw/json/dumps/`) como SSoT inmutable en disco.
   - Sintetiza los **4 Artefactos Canónicos de Fase 0 / Platino** en `raw/llm/`:
     * `coach_technical_sheet.md` (12 secciones matemáticas puras).
     * `fase0_author_psychology.md` (Constitución ontológica y voz de autor).
     * `astrobranding_[marca].md` (Dossier semiótico, arquetípico y directivas de diseño).
     * `brandbook_[marca].json` (Tokens de diseño W3C DTCG con `$extensions.tailwind_v4` para `@theme` en Tailwind CSS v4).

---

## 3. Catálogo Canónico del Canon 12-15-9-4

### A. Los 12 Shards Bronze JSON (`raw/json/dumps/`):
1. `01_numerology_multi.json`: Pitagórica, Caldea, Ank Jyotish, Gematria (Astrology-API.io + FreeAstroAPI).
2. `02_western_tropical.json`: Placidus Tropical, 23 Casas, Sabian Symbols, Progresiones Sec/Ter/Converse.
3. `03_western_sidereal.json`: Fagan-Bradley Campanus, Casas Siderales de Astrology-API.io.
4. `04_vedic_jyotish_kp.json`: Lahiri Whole Sign, KP V2, Kundali MCP, VedAstro Predictions + AllPlanet + AllHouse, AstroWay 16 Vargas D1-D60 + Dashas.
5. `05_bazi_chinese_lunar.json`: BaZi True Solar, Da Yun Flow, AstroWay Four Pillars, Lunar MCP.
6. `06_human_design.json`: BodyGraph completo, Circuitry, Incarnation Cross, PHS Sensitivity.
7. `07_kabbalah_hermetic.json`: HebCal Converter, HebCal Zmanim, Zmanim MCP (`times` + `times_iso`), Gematria, Sefer Yetzirah, Tikkun Nodal con Skipped Steps.
8. `08_timing_dashas_timelords.json`: Timeline Aggregator (Profecciones, Firdaria, Decennials, ZR), Vimshottari Dashas a 5 niveles, 10 Elecciones Comerciales.
9. `09_geo_acg_relocation.json`: ACG Lines (FreeAstroAPI + AstroWay), Best Places, Relocalización.
10. `10_cosmobiology_hellenistic_nasa.json`: Dial 90°, 15 Lots de Chris Brennan, ZR Peak Periods, Efemérides de Asteroides y Centauros de NASA Horizons (Ceres, Chiron, Pallas, Juno, Vesta, Eris).
11. `11_traditional_medical_tcm.json`: Medicina Tradicional China BaZi (órganos Zang-Fu, desbalances de 5 elementos), temperamentos humorales y astrología médica tradicional.
12. `12_fixed_stars_constellations.json`: Catálogo de 50+ estrellas fijas mayores (Ptolemaicas y Behenias), constelaciones siderales, orbes paranatellonta y declinaciones.

### B. Los 15 Shards Relacionales Silver (PostgreSQL):
Esquemas tabulares normalizados para consulta SQL analítica y persistencia estructurada:
`silver_profiles`, `silver_natal_planets`, `silver_natal_houses`, `silver_aspects_orbs`, `silver_vargas_d1_d60`, `silver_dashas_timeline`, `silver_bazi_pillars`, `silver_numerology_scores`, `silver_human_design_gates`, `silver_kabbalah_letters`, `silver_timing_transits`, `silver_astrocartography_lines`, `silver_fixed_stars`, `silver_health_tcm_elements`, `silver_brand_archetypes`.

### C. Los 9 Feeds Quirúrgicos Markdown (< 2.5 KB en `raw/feeds/`):
- `feed_fase1_num.md`: Matriz numerológica personal y comercial.
- `feed_fase2_occ.md`: Sol, Luna, ASC, MC y balance elemental tropical.
- `feed_fase3_sid.md`: Contraste ontológico Tropical vs. Sideral Fagan-Bradley.
- `feed_fase4_ved.md`: Lagna, Nakshatra, Deidad, Shakti, D9, D10 y Shadbala.
- `feed_fase5_bazi.md`: Cuatro Pilares (60 Jiazi), Day Master, Yong Shen y 5 Elementos.
- `feed_fase6_kab.md`: Calendario Hebreo, Sefer Yetzirah, Tikkun Nodal y Zmanim.
- `feed_fase7_voc.md`: Clímax de carrera (MC, D10, Human Design, roles comerciales).
- `feed_fase8_time.md`: Reloj temporal T0 (Pináculo activo, Da Yun activo, Dasha activa).
- `feed_fase9_end.md`: Horizontes estratégicos, 4 tracks de mentoría y sesión 1:1.

### D. Los 4 Artefactos Canónicos de Capa Platino (`raw/llm/`):
1. `coach_technical_sheet.md`: 12 secciones matemáticas puras (SSoT Fase 0).
2. `fase0_author_psychology.md`: Constitución ontológica, tono y resonancia psicológica del autor.
3. `astrobranding_[marca].md`: Dossier semiótico, arquetípico y directivas de diseño para Orchesbrand.
4. `brandbook_[marca].json`: Tokens de diseño en formato W3C Design Tokens Community Group (DTCG) con extensión `$extensions.tailwind_v4` para inyección directa en `@theme` de Tailwind CSS v4.

---

## 4. Protocolo de Ejecución de Fase 0 (`omni_engine.py`)

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

---

### Opción C: Ejecución Modular por Capas (Oro / Platino)
```bash
# Solo Compilación Capa Oro (12 Bronze Shards, 15 Silver Shards, 9 Gold Feeds)
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py --client-dir "<RUTA_CLIENTE>" -c

# Solo Síntesis Capa Platino (4 Artefactos LLM y Brandbook W3C DTCG)
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py --client-dir "<RUTA_CLIENTE>" -s

# Compilación tolerante a endpoints faltantes
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py --client-dir "<RUTA_CLIENTE>" -c --allow-partial
```

---

## 5. Catálogo Completo de Banderas CLI

| Bandera | Alias | Tipo | Descripción |
|---|---|---|---|
| `file_pos` | `-f`, `--file` | `str` | Ruta a archivo de datos del consultante (`.txt`, `.json`, `.md`). |
| `--client-dir` | `-d` | `str` | Directorio destino del consultante (resuelve `raw/json/dumps/`, `raw/feeds/`, `raw/llm/`). |
| `-x` | `--extract` | `flag` | Ejecuta la fase de extracción concurrente REST/MCP a caché SHA-256. |
| `-c` | `--compile` | `flag` | **Capa Oro**: Compila los 12 Shards Bronze, 15 Silver y 9 Feeds Gold desde caché sin sintetizar reportes LLM. |
| `-s` | `--synthesis` | `flag` | **Capa Platino**: Sintetiza los 4 artefactos en `raw/llm/` a partir de los datos consolidados en Capa Oro. |
| `--allow-partial` | | `flag` | Permite compilar Capa Oro emitiendo alertas si faltan respuestas opcionales en caché. |
| `--refresh-pro` | | `flag` | Fuerza la re-extracción remota invalidando la caché SHA-256 en disco. |
| `--dry-run` | | `flag` | Ejecuta el consenso y sharding matemático determinista sin consumir cuotas de API. |
| `--dob` | | `str` | Fecha de nacimiento (`YYYY-MM-DD`). |
| `--tob` | | `str` | Hora de nacimiento en formato 24h (`HH:MM`). |
| `--lat` | | `float` | Latitud decimal (e.g. `4.7110`). |
| `--lon` | | `float` | Longitud decimal (e.g. `-74.0721`). |
| `--tz` | | `str` | Zona horaria IANA canónica (e.g. `America/Bogota`). |
| `--city` | | `str` | Ciudad natal (e.g. `Bogota`). |
| `--names` | | `str` | Nombre de nacimiento completo (utilizado en numerología multidimensional). |
| `--birth-name` | | `str` | Nombre legal o natal del consultante (Bloque B1). |
| `--current-name` | | `str` | Nombre actual o elegido del consultante (Bloque B2). |
| `--spoken` | | `str` | Nombre de trato preferido para el reporte didáctico. |
| `--brand-names` | | `str` | Nombres comerciales separados por coma para numerología y astrobranding (Bloque C). |
