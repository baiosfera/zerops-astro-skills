# 🌌 Guía Operativa del Extractor y Ensamblador Oráculo (`omni_engine.py`)

Guía técnica canónica para operar el pipeline astronómico, astrológico y metafísico en la plataforma Zerops (`skill oraculo v6.3`).
Arquitectura desacoplada: **Capa Oro (`-c` / `--compile`)** y **Capa Platino (`-s` / `--synthesis`)** bajo el Canon 12-15-9-4.

---

## 1. Arquitectura Desacoplada de 4 Niveles

El pipeline opera en 4 capas estrictamente desacopladas para garantizar idempotencia, inmutabilidad, trazabilidad forense y paridad SSoT:

1. **Nivel 1: Caché en Disco (`raw/json/cache/`)**:
   - Cada proveedor y endpoint persiste su respuesta validada en un archivo JSON independiente:
     `{provider}_{endpoint}_{client_hash}.json`
   - **Invariante de No Sobreescritura Cruzada**: Los archivos se acumulan de forma aditiva entre proveedores (`astroway`, `freeastroapi`, `vedastro`, `astrologyapi`, `bazi_mcp`, `zmanim_mcp`, `kundali_mcp`, `hebcal`, `nasa`).
   - **Universal Dynamic Cache Crawler (`cache_crawler.py`)**: Recorre dinámicamente el 100% de los archivos de caché (sin listas estáticas ni hardcoding de 498 endpoints) y deduplica firmas SHA-256 de payload para eliminar colisiones entre volcados completos e individuales.

2. **Nivel 2: Micro-Auditorías Atómicas por API (`raw/json/audit/`)**:
   - Cada ejecución (`-x` o batch) genera un comprobante inmutable e independiente por proveedor:
     `raw/json/audit/audit_{provider}.json`
   - Registra latencia real de red, status HTTP, total de endpoints solicitados/exitosos/fallidos, créditos consumidos y timestamp UTC.
   - **Trazabilidad Forense**: Preserva la historia original de las llamadas de red incluso si la caché se reutiliza localmente (`status=CACHED, latency=0.0 ms`).

3. **Nivel 3: Capa Oro — Compilación y Sharding (`-c` / `--compile`)**:
   - Coordina los 9 motores de dominio (`numerology`, `western`, `sidereal`, `vedic`, `bazi`, `kabbalah`, `hd_cosmobiology`, `acg`, `timing`).
   - Genera el Data Lake físico y relacional en `raw/json/dumps/` y `raw/feeds/`:
     * **12 Shards Físicos JSON (Bronze)**: `shard_01.json` a `shard_12.json` (Occidental Tropical, Sideral Fagan-Bradley, Védica Jyotish KP, BaZi 4 Pilares, Human Design, Cábala Zmanim, Vocacional D10, Astrocartografía ACG, Numerología Multimarca, Timing Dashas, Cosmobiología Dial 90°, TCM Health).
     * **15 Shards Relacionales (Silver)**: `client_dumps_15_shards.json` para PostgreSQL y `manifest.json` con punteros RFC 6901.
     * **9 Feeds Enciclopédicos Gold Markdown**: En `raw/feeds/` con glosario técnico bilingüe estricto (término en inglés/sánscrito/hebreo junto a explicación técnica en español).
     * **Purga de Duplicados**: Erradica copias redundantes (`brandbook*.json` y `feed_astrobranding*.md` en `raw/feeds/`, y `brandbook*.json` en raíz).

4. **Nivel 4: Capa Platino — Síntesis LLM y Design Tokens (`-s` / `--synthesis`)**:
   - Genera los 4 artefactos canónicos consolidados estrictamente en `raw/llm/`:
     1. `coach_technical_sheet.md`: Ficha técnica SSoT matemática pura (12 secciones tabulares, cero prosa de relleno).
     2. `fase0_author_psychology.md`: System Prompt SSoT para agentes downstream (Fases 1 a 9 y `oraculo-diag-*`) redactado bajo CoHaLo Positive Guidance (cero dogmas negativos, 100% directivas constructivas).
     3. `astrobranding_[marca].md`: Master brief semiótico (Tríada del Cliente ICP: Casas 7 + 8 + 11 + Venus; Trípode de Hierro: Sol + MC + Casa 2; Paleta Bipolar OKLCH con garantías APCA y WCAG AAA; Geometría sagrada y cadencia cinética GSAP 60fps).
     4. `brandbook_[marca].json`: Especificación completa W3C DTCG Tokens con extensiones `$extensions.tailwind_v4` (`@theme`) y `$extensions.css_variables` (`:root`) para consumo nativo en `astro-web`.

---

## 2. Flujo Operativo Modular

### Paso 1: Extracción Pura (`-x` / `--extract`)
Descarga y persiste datos en caché sin sharding prematuro:
```bash
# Extraer proveedor específico
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py /ruta/consultante.md -x --apis astroway

# Extraer múltiples proveedores
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py /ruta/consultante.md -x --apis astrologyapi,freeastroapi,vedastro
```

### Paso 2: Compilación Capa Oro (`-c` / `--compile`)
Ensambla los 12 shards Bronze, los 15 shards Silver y los 9 feeds Gold desde la caché local sin llamadas externas:
```bash
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py /ruta/consultante.md -c
```

### Paso 3: Síntesis Capa Platino (`-s` / `--synthesis`)
Genera los 4 entregables de marca, psicología y tokens en `raw/llm/` a partir de la caché verificada:
```bash
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py /ruta/consultante.md -s
```

### Flujo Todo-en-Uno (Extracción + Compilación + Síntesis)
```bash
python3 /var/www/.agents/skills/oraculo/scripts/omni_engine.py /ruta/consultante.md
# O mediante el wrapper directo:
bash /var/www/.agents/skills/oraculo/scripts/fase0.sh /ruta/consultante.md
```

---

## 3. Catálogo de Banderas CLI

| Bandera | Propósito | Ejemplo |
|---|---|---|
| `-x`, `--extract` | **Solo extracción**: Guarda en caché y genera micro-audit en `audit/` sin compilar. | `-x --apis astroway` |
| `-c`, `--compile` | **Capa Oro**: Compila 12 shards Bronze, 15 Silver y 9 feeds Gold desde caché. | `-c` |
| `-s`, `--synthesis` | **Capa Platino**: Sintetiza ficha técnica, psicología, brief y Brandbook DTCG en `raw/llm/`. | `-s` |
| `--apis <lista>` | Filtra proveedores a ejecutar (separados por coma). | `--apis astroway,vedastro` |
| `--exclude <lista>` | Excluye proveedores específicos de la ejecución. | `--exclude vedastro,mcp` |
| `--allow-partial` | Permite compilar ignorando el gate estricto de cobertura completa. | `-c --allow-partial` |
| `--refresh-pro` | Fuerza la re-extracción ignorando la caché existente. | `-x --apis astroway --refresh-pro` |
| `--dry-run` | Valida parámetros y geocodificación sin escribir a disco. | `--dry-run` |
| `--client-dir <dir>` | Sobrescribe el directorio destino del consultante. | `--client-dir /var/www/output/CLIENTE` |
