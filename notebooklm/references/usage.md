# Gemini Notebook & NotebookLM Dual-RAG Usage Manual (CLI & FastMCP Server)

Este manual documenta la interacción técnica exhaustiva con el ecosistema **Gemini Notebook / NotebookLM** (Septiembre 2026) bajo una arquitectura desacoplada en 3 capas:
1. **Capa 1: Plataforma & FastMCP (`notebooklm_tools` de Jacob Ben-David)**: Servidor FastMCP nativo de 49 herramientas y CLI `nlm` (transporte RPC `batchexecute`, CDP headless, rotación de cookies y CodeMappers nativos).
2. **Capa 2: Orquestador Pedagógico (`nlm-tutor` v2.2.0)**: Script socrático de alto rendimiento para Google NotebookLM Pro (Google One AI Premium / 5TB). Genera la batería de 12 artefactos directamente en Google Cloud Studio sin saturar el almacenamiento local.
3. **Capa 3: Inteligencia Operativa & Ruteo (Skill `notebooklm`)**: Router Dual-RAG que enseña a los agentes de IA a orquestar el ecosistema sin alucinaciones de flags y conociendo el tier `NOTEBOOKLM_TIER_PRO_CONSUMER_USER`.

---

## 1. Contrato Oficial de Admisión de 43 Extensiones de Archivo

El backend de Google NotebookLM y el motor de Jacob Ben-David imponen un contrato de admisión estricto verificado en tiempo de ejecución en `notebooklm_tools/core/constants.py`. Admite exactamente **43 extensiones oficiales**:

```
.pdf, .txt, .md, .docx, .csv, .pptx, .epub, .avif, .bmp, .gif, .heic, .heif, 
.ico, .jp2, .jpe, .jpeg, .jpg, .png, .tif, .tiff, .webp, .3g2, .3gp, .aac, 
.aif, .aifc, .aiff, .amr, .au, .avi, .cda, .m4a, .mid, .mp3, .mp4, .mpeg, 
.ogg, .opus, .ra, .ram, .snd, .wav, .wma
```

> **Invariante de Carga Local:** El parámetro `--file` / `-f` de `nlm source add` admite un único archivo por invocación (tipo `str | None`). La subida masiva de binarios debe ejecutarse secuencialmente mediante bucle Bash con `--wait --wait-timeout 600`.

---

## 2. Catálogo Canónico de los 49 Tools FastMCP (15 Grupos)

El servidor FastMCP (`gemini-notebook-mcp`) expone 49 herramientas organizadas por dominio operativo:

| # | Tool MCP | Grupo Funcional | Descripción Técnica | Argumentos Obligatorios | Argumentos Opcionales |
|---|---|---|---|---|---|
| 1 | `refresh_auth` | `auth` | Recarga cookies y tokens desde disco o sesión headless activa. | *Ninguno* | *Ninguno* |
| 2 | `save_auth_tokens` | `auth` | Almacena manualmente cookies y tokens Google en el perfil. | `cookies` | `csrf_token`, `session_id`, `request_body`, `request_url` |
| 3 | `batch` | `automation` | Operaciones por lotes sobre múltiples cuadernos. | `action` (`query`, `add_source`, `create`, `delete`, `studio`) | `query`, `source_url`, `titles`, `artifact_type`, `tags`, `all`, `confirm` |
| 4 | `pipeline` | `automation` | Ejecuta pipelines de múltiples pasos predefinidos. | `action` (`list`, `run`) | `notebook_id`, `pipeline_name`, `input_url` |
| 5 | `notebook_query` | `chat` | Consulta síncrona RAG con citas verbatim grounded. | `notebook_id`, `query` | `source_ids`, `conversation_id`, `timeout` (120.0), `new_conversation` |
| 6 | `chat_configure` | `chat` | Configura objetivo (`goal`) y extensión de respuesta del chat. | `notebook_id` | `goal` (`default`, `learning_guide`, `custom`), `custom_prompt`, `response_length` |
| 7 | `notebook_query_start` | `chat` | Inicia una consulta asíncrona desacoplada para evitar bloqueos. | `notebook_id`, `query` | `source_ids`, `conversation_id`, `timeout`, `new_conversation` |
| 8 | `notebook_query_status` | `chat` | Sondea el estado y respuesta de una consulta asíncrona. | `query_id` | *Ninguno* |
| 9 | `chat_list` | `chat` | Lista las sesiones de chat históricas registradas en el cuaderno. | `notebook_id` | `limit` (int=20) |
| 10 | `chat_get` | `chat` | Recupera el historial completo de mensajes y citas de un hilo. | `notebook_id` | `conversation_id` |
| 11 | `chat_export` | `chat` | Exporta la conversación a formatos Markdown o JSON. | `notebook_id` | `conversation_id`, `format` (`markdown`, `json`) |
| 12 | `collection_list` | `organization` | Lista las colecciones lógicas de cuadernos en la cuenta. | *Ninguno* | *Ninguno* |
| 13 | `collection_create` | `organization` | Agrupa cuadernos en una colección unificada. | `name` | `notebook_ids` |
| 14 | `collection_edit` | `organization` | Modifica nombre o membresía de una colección. | `collection_id` | `name`, `notebook_ids` |
| 15 | `collection_set_emoji` | `organization` | Asigna un emoji visual a una colección. | `collection_id`, `emoji` | *Ninguno* |
| 16 | `collection_delete` | `organization` | Elimina una colección lógica (preserva los cuadernos). | `collection_id` | `confirm` (bool=False) |
| 17 | `label` | `organization` | Gestión consolidada de etiquetas de fuentes internas. | `notebook_id`, `action` (`auto`, `list`, `reorganize`, `create`, `rename`, `set_emoji`, `move_source`, `delete`) | `label_id`, `label_ids`, `name`, `emoji`, `source_id`, `confirm` |
| 18 | `tag` | `organization` | Gestiona etiquetas locales de cuadernos para descubrimiento federado. | `action` (`add`, `remove`, `list`, `select`) | `notebook_id`, `tags`, `notebook_title`, `query` |
| 19 | `cross_notebook_query` | `query_multi` | Ejecuta búsquedas semánticas transversales federadas. | `query` | `notebook_names`, `tags`, `all` |
| 20 | `notebook_list` | `notebooks_read` | Lista los cuadernos de la cuenta con conteo de fuentes. | *Ninguno* | `max_results` (int=100) |
| 21 | `notebook_get` | `notebooks_read` | Obtiene metadatos profundos y fuentes del cuaderno. | `notebook_id` | *Ninguno* |
| 22 | `notebook_describe` | `notebooks_read` | Resumen global mediante IA de todo el contenido del cuaderno. | `notebook_id` | *Ninguno* |
| 23 | `notebook_create` | `notebooks_manage` | Crea un nuevo cuaderno de investigación en blanco. | *Ninguno* | `title` (str="Untitled") |
| 24 | `notebook_rename` | `notebooks_manage` | Renombra el título de un cuaderno existente. | `notebook_id`, `new_title` | *Ninguno* |
| 25 | `notebook_delete` | `notebooks_manage` | Elimina permanentemente un cuaderno y todas sus fuentes. | `notebook_id` | `confirm` (bool=False) |
| 26 | `note` | `notes` | Herramienta unificada de notas de usuario en el cuaderno. | `notebook_id`, `action` (`create`, `list`, `update`, `delete`) | `note_id`, `content`, `title`, `confirm` |
| 27 | `research_start` | `research` | Inicia Deep Research o Fast Research de fuentes en la web. | `query` | `source` (`web`, `drive`), `mode` (`fast`, `deep`), `notebook_id`, `title` |
| 28 | `research_status` | `research` | Monitorea el progreso de una tarea autónoma de research. | `notebook_id` | `task_id`, `poll_interval`, `max_wait`, `auto_import` |
| 29 | `research_import` | `research` | Importa fuentes descubiertas al cuaderno de trabajo. | `notebook_id`, `task_id` | `source_indices`, `timeout`, `cited_only` |
| 30 | `server_info` | `server` | Informa versión del servidor MCP, transporte y profile. | *Ninguno* | *Ninguno* |
| 31 | `notebook_share_status` | `sharing` | Inspecciona visibilidad y colaboradores de un cuaderno. | `notebook_id` | *Ninguno* |
| 32 | `notebook_share_public` | `sharing` | Activa o desactiva enlace público de lectura. | `notebook_id` | `is_public` (bool=True) |
| 33 | `notebook_share_invite` | `sharing` | Invita a un colaborador por correo electrónico. | `notebook_id`, `email` | `role` (`viewer`, `editor`) |
| 34 | `notebook_share_batch` | `sharing` | Envía invitaciones masivas en un solo llamado. | `notebook_id`, `recipients` | `confirm` (bool=False) |
| 35 | `source_add` | `sources_manage` | Ingesta unificada de URL, texto, Google Drive o archivo local. | `notebook_id`, `source_type` (`url`, `text`, `drive`, `file`) | `url`, `urls`, `text`, `title`, `file_path`, `document_id`, `doc_type`, `wait`, `wait_timeout` |
| 36 | `source_list_drive` | `sources_read` | Lista fuentes de Drive detectando frescura (`is_stale`). | `notebook_id` | `skip_freshness` |
| 37 | `source_sync_drive` | `sources_manage` | Sincroniza fuentes obsoletas de Google Drive. | `source_ids` | `confirm` (bool=False) |
| 38 | `source_rename` | `sources_manage` | Renombra el título asignado a una fuente en el cuaderno. | `notebook_id`, `source_id`, `new_title` | *Ninguno* |
| 39 | `source_delete` | `sources_manage` | Elimina una o múltiples fuentes indexadas. | *Ninguno* (requiere `source_id` o `source_ids`) | `source_id`, `source_ids`, `confirm` |
| 40 | `source_describe` | `sources_read` | Genera resumen de IA y keywords de una fuente específica. | `source_id` | *Ninguno* |
| 41 | `source_get_content` | `sources_read` | Extrae el texto plano crudo indexado (transcripciones/docs). | `source_id` | `wait`, `wait_timeout`, `poll_interval` |
| 42 | `studio_create` | `studio` | Generador multi-modal centralizado para 9 tipos de artefacto. (Requiere `Create Your Own` para `custom_prompt`). | `notebook_id`, `artifact_type` | Parámetros específicos por formato, `source_ids`, `confirm` |
| 43 | `studio_status` | `studio` | Lista y consulta estado de generación y descarga de artefactos (`action='rename'` exige `status='completed'`). | `notebook_id` | `action`, `artifact_id`, `new_title`, `include_details` |
| 44 | `studio_delete` | `studio` | Elimina permanentemente un artefacto de Studio. | `notebook_id`, `artifact_id` | `confirm` (bool=False) |
| 45 | `studio_revise` | `studio` | Aplica revisiones slide a slide sobre un Slide Deck existente. | `notebook_id`, `artifact_id`, `slide_instructions` | `confirm` (bool=False) |
| 46 | `download_artifact` | `studio` | Descarga un artefacto puntual hacia el sistema de archivos. | `notebook_id`, `artifact_type`, `output_path` | `artifact_id`, `output_format`, `slide_deck_format`, `wait`, `wait_timeout` |
| 47 | `download_all_artifacts` | `studio` | Descarga masiva de artefactos completados a un directorio. | *Ninguno* | `notebook_id`, `output_dir`, `artifact_types`, `slide_deck_format`, `interactive_format` |
| 48 | `export_artifact` | `studio` | Exporta reportes a Google Docs o tablas a Google Sheets. | `notebook_id`, `artifact_id`, `export_type` (`docs`, `sheets`) | `title` |
| 49 | `usage_get` | `usage` | Consulta cuotas de cómputo en ventanas rolling y semanal. | *Ninguno* | `profile` |

---

## 3. Manual de Referencia Canónico del CLI `nlm` (Sintaxis Validada)

### A. Gestión de Cuadernos y Etiquetas
```bash
# Listar cuadernos
nlm notebook list
nlm notebook list --json
nlm notebook list --quiet

# Crear cuaderno
nlm notebook create "Título del Cuaderno" -j

# Etiquetar formalmente para federación (requiere -t / --tags)
nlm tag add <UUID> -t "cat:salud,author:lavin,year:2025"

# Describir cuaderno con resumen de IA
nlm notebook describe <UUID>

# Eliminar cuaderno con confirmación
nlm notebook delete <UUID> --confirm
```

### B. Ingesta Unificada de Fuentes (`source add`)
```bash
# Subir archivo local (PDF, AAC, MP3, etc.) con espera y timeout streaming
nlm source add <UUID> -f "/ruta/archivo.aac" --wait --wait-timeout 600

# Subir URL web
nlm source add <UUID> -u "https://ejemplo.com/articulo" --wait

# Subir documento de Google Drive
nlm source add <UUID> -d "<DRIVE_DOC_ID>" --type doc --wait

# Listar fuentes del cuaderno
nlm source list <UUID> --json

# Obtener transcripción o texto plano crudo de una fuente
nlm source content <SOURCE_ID>

# Describir una fuente específica
nlm source describe <SOURCE_ID>
```

### C. Generación Multi-Modal de Studio (9 Formatos)

```bash
# 1. Reportes Estructurados (Formatos: 'Briefing Doc', 'Study Guide', 'Blog Post', 'Create Your Own')
nlm report create <UUID> --format "Briefing Doc" --language es --confirm -j
nlm report create <UUID> --format "Study Guide" --language es --confirm -j
nlm report create <UUID> --format "Blog Post" --language es --confirm -j
nlm report create <UUID> --format "Create Your Own" --prompt "Genera un resumen ejecutivo de 3 páginas" --confirm -j

# Advertencia Crítica: En notebooklm_tools/core/client.py y core/studio.py,
# los formatos 'Briefing Doc', 'Study Guide' y 'Blog Post' IGNORAN y DESCARTAN
# el parámetro custom_prompt, enviando un prompt fijo en inglés de Google.
# Para inyectar un prompt personalizado, es MANDATORIO usar: --format "Create Your Own"


# 2. Mapa Mental (Mind Map)
nlm mindmap create <UUID> --title "Mapa Mental de Arquitectura" --confirm -j

# 3. Tabla de Datos (Descripción es argumento posicional obligatorio)
nlm data-table create <UUID> "<description>" --language es --confirm -j

# 4. Quizzes y Flashcards (Dificultad de Quiz es entero 1-5; Flashcards es string: easy, medium, hard)
nlm quiz create <UUID> --count 10 --difficulty 3 --focus "Evaluación de conceptos clave" --confirm -j
nlm flashcards create <UUID> --difficulty medium --focus "Glosario de definiciones" --confirm -j

# 5. Diapositivas (Slide Deck - detailed_deck o presenter_slides | Length: default, short)
nlm slides create <UUID> --format detailed_deck --language es --focus "Presentación ejecutiva" --confirm -j

# Revisión Diapositiva a Diapositiva (FastMCP studio_revise / RPC)
# Permite modificar slides individuales sin regenerar la presentación completa:
# studio_revise(notebook_id, artifact_id, slide_instructions=[{"slide": 1, "instruction": "Ampliar título"}, {"slide": 2, "instruction": "Agregar diagrama"}])

# 6. Infografía (Orientation: landscape, portrait, square | Detail: concise, standard, detailed)
# Estilos (11 estilos oficiales en CodeMapper de jacob-bd):
# anime, auto_select, bento_grid, bricks, clay, editorial, instructional, kawaii, professional, scientific, sketch_note
nlm infographic create <UUID> --orientation landscape --style professional --language es --confirm -j
nlm infographic create <UUID> --orientation landscape --style editorial --language es --confirm -j

# 7. Resumen de Audio (Podcasts - Formatos: deep_dive, brief, critique, debate | Length: short, default, long)
nlm audio create <UUID> --format deep_dive --length default --language es --confirm -j
nlm audio create <UUID> --format critique --length long --language es --confirm -j

# 8. Resumen de Video (Formatos: explainer, brief, cinematic, short)
# Estilos (10 estilos oficiales en CodeMapper de jacob-bd):
# anime, auto_select, classic, custom, heritage, kawaii, paper_craft, retro_print, watercolor, whiteboard
nlm video create <UUID> --format explainer --style classic --confirm -j
nlm video create <UUID> --format cinematic --style anime --confirm -j
```

### D. Monitoreo, Descarga y Exportación Workspace

```bash
# Consultar estado de los artefactos de Studio
nlm studio status <UUID> --json

# Descarga puntual de un artefacto completado (UUID es posicional, ID se pasa con --id)
nlm download report <UUID> --id <ID> -o "/ruta/destino/reporte.md"
nlm download audio <UUID> --id <ID> -o "/ruta/destino/audio.mp3"
nlm download slide-deck <UUID> --id <ID> --format pdf -o "/ruta/destino/deck.pdf"
nlm download infographic <UUID> --id <ID> -o "/ruta/destino/infografia.png"

# Descarga masiva de todos los artefactos completados de un cuaderno
nlm download all <UUID> --output-dir "/ruta/destino/" --slide-format pdf --interactive-format markdown

# Renombramiento asíncrono seguro (exclusivamente tras confirmar status='completed')
nlm studio rename <UUID> --id <ARTIFACT_ID> --title "04_REPORT_Briefing-Doc-Ejecutivo"

# Exportación a Google Workspace
nlm export to-docs <UUID> <ID> --title "Reporte Oficial"
nlm export to-sheets <UUID> <ID> --title "Matriz de Datos"
```

> [!IMPORTANT]
> **Patrón de Renombramiento Asíncrono en Studio (`studio_status action='rename'`):**
> Al disparar la creación de un artefacto en Studio (`studio_create` o `nlm <type> create`), la API retorna de inmediato con `status='in_progress'`.
> - **Invariante de Renombramiento:** Si se intenta renombrar (`studio_status action='rename'` o `nlm studio rename`) mientras la generación sigue en progreso, la API de Google fallará o el backend sobreescribirá el título al finalizar, resultando en artefactos sin numerar o títulos por defecto duplicados.
> - **Protocolo Exclusivo:** Sondeo en intervalos de 15–20s mediante `studio_status` hasta confirmar `status == 'completed'`. Únicamente tras dicha confirmación se ejecuta el renombramiento vía FastMCP `studio_status(action='rename', artifact_id=..., new_title=...)` o CLI `nlm studio rename`.

> [!NOTE]
> **Principio de Almacenamiento en Google Cloud Studio (Cero Descargas Obligatorias):**
> Por diseño arquitectónico, todos los artefactos generados (podcasts, vídeos, infografías, presentaciones, reportes) residen y se consumen directamente en la nube de Google NotebookLM Studio. **NO se descargan a local automáticamente** ni deben saturar el almacenamiento local.
> Las herramientas de descarga (`download_artifact`, `download_all_artifacts`, `nlm download`) son de uso **opcional y bajo demanda explícita del usuario**, y su destino está estrictamente confinado dentro de `NOTEBOOKLM_DOWNLOAD_DIR` (por defecto `~/Downloads/gemini-notebook`).


### E. Telemetría de Cuotas de Cómputo (Septiembre 2026)
```bash
# Consultar cuotas y ventanas de reseteo rolling (~5h) y semanal (7d)
nlm usage --json
```

---

## 4. Patrones Arquitectónicos de Ingesta Masiva de Cursos (Tier Pro 300 Fuentes)

### A. Pipeline de Ingesta Streaming Desatendida
```bash
UUID="<NOTEBOOK_UUID>"
AUDIO_DIR="/var/www/baiosfera/CURSOS/MCV/.../NOTEBOOKLM_AUDIOS"

# Ingesta secuencial acotada (evita colapsar RAM y previene descarte por concurrencia)
for audio in "$AUDIO_DIR"/*.aac; do
    echo "[$(date '+%T')] Subiendo: $(basename "$audio")..."
    nlm source add "$UUID" -f "$audio" --wait --wait-timeout 600
done

# Ingesta de manual y documentación de soporte
nlm source add "$UUID" -f "$AUDIO_DIR/../Manual.pdf" --wait --wait-timeout 600
nlm source add "$UUID" -f "$AUDIO_DIR/../README.md" --wait
```

### B. Patrón de Cuaderno Matriz por Categoría (`[CAT]`)
En planes Pro Consumer (300 fuentes por cuaderno), los cursos de una misma vertical se unifican en un cuaderno matriz `[CAT] <VERTICAL>` (ej. `[CAT] VENTAS`). Esto permite a Gemini Pro contrastar y cruzar metodologías en tiempo real en una sola consulta semántica RAG:
```bash
nlm notebook query <UUID> "Compara la estrategia de seguimiento de Autor A con las tácticas de cierre de Autor B."
```

---

## 5. Arquitectura del Ecosistema NLM-Tutor (v2.2.0)

`nlm-tutor` es el orquestador socrático autónomo de alto rendimiento para Google NotebookLM Pro (Google One 5TB / AI Premium). Opera directamente sobre el SDK nativo en Python (`notebooklm_tools.services`) y prescinde de subprocesos de shell o redacción manual de prompts técnicos por parte del usuario. Los 12 artefactos generados se alojan en la nube de Google Studio, sin descargas forzadas a disco.

### A. Arquitectura Curricular de Dos Niveles: Tutor de Aula vs. Decano Curricular
`nlm_tutor.py` v2.2.0 detecta automáticamente el propósito pedagógico del cuaderno según su título:
1. **Modo Decano Curricular (`DEAN_CURRICULAR_PROMPT`)**: Se activa de forma automática si el título contiene `[00]`, `GUIA-DE-ESTUDIO` o `RUTA_DE_APRENDIZAJE`. Configura a Gemini como director curricular para diseñar la ruta formativa completa, la matriz de módulos y la secuenciación de prerrequisitos.
2. **Modo Tutor de Aula Socrático (`TUTOR_SOCRATICO_PROMPT`)**: Se activa en cuadernos temáticos regulares. Conduce la sesión interactiva con el método MIT 1972, active recall y técnica Feynman.

### B. Subcomandos Principales del Ecosistema

1. **`nlm-tutor setup <UUID> [--clean] [--collection NAME]` (Generación y Configuración Socrática)**:
   - Configura el chat del cuaderno con directivas metodológicas del MIT (1972) y rúbrica estricta en 5 dimensiones.
   - Crea en el panel de Studio la batería de 12 artefactos estructurados en 5 fases de neurociencia cognitiva (*Make It Stick*, Harvard, Ebbinghaus):
     - **Fase 1: Pre-test & Diagnóstico Inicial**: `09_QUIZ_Nivel-1-Diagnostico-Inicial` y `10_QUIZ_Nivel-3-Razonamiento-Intermedio` (quiebre de la ilusión de competencia).
     - **Fase 2: Anclaje & Inmersión Dual**: `01_AUDIO_Inmersion-Inicial-Podcast` y `02_INFOGRAPHIC_Mapa-Visual-80-20` (teoría del doble código de Paivio).
     - **Fase 3: Síntesis Profunda & Modelos Mentales**: `03_MINDMAP_Syllabus-Estructural` y `04_REPORT_Briefing-Doc-Ejecutivo` (syllabus integral y modelos base).
     - **Fase 4: Técnica Feynman & Auto-enseñanza**: `05_REPORT_Guia-de-Estudio-Feynman` y `07_SLIDES_Autoensenanza-Feynman` (explicación a libro cerrado).
     - **Fase 5: Casos Límite & Hipercorrección**: `06_TABLE_Comparativa-Conceptos-y-Matices`, `11_QUIZ_Nivel-5-Casos-Criticos-Simulacro` y `12_REPORT_Kit-de-Repaso-y-Errores-Tipicos`.
   - Inicializa las notas nativas del cuaderno: `00_CUADERNO_DE_LAGUNAS` y `00_RUTA_DE_ESTUDIO`.
   - Soporta bandera `--clean`: `nlm-tutor setup <UUID> --clean` para purgar Studio, notas 00 y chat antes de regenerar la suite.

2. **`nlm-tutor clean <UUID> [--all-notes] [--keep-chat]` (Purga Higiénica Controlada)**:
   - Elimina de forma segura y controlada los artefactos generados en Studio, las notas `00_` del tutor y el historial de chat.
   - **Invariante Crítico de Gobernanza:** NUNCA toca ni elimina fuentes (`sources`). Las fuentes subidas quedan 100% intactas.
   - Banderas: `--all-notes` para purgar todas las notas del cuaderno; `--keep-chat` para conservar el historial del chat.

3. **`nlm-tutor rename <UUID>` (Reconciliación y Renombrado Secuencial)**:
   - Reconcilia y renombra todos los artefactos en Studio aplicando títulos canónicos numerados una vez alcanzado `status == 'completed'`.

4. **`nlm-tutor session <UUID> [--duration 90]` (REPL Socrático Interactivo en Terminal)**:
   - Inicia un bucle REPL interactivo en la terminal con evaluación estricta en 5 dimensiones (acierto, superficialidad, brecha conceptual, cita de fuentes, respuesta magistral).
   - **Flujo Bidireccional en Tiempo Real:** Se ejecuta localmente en la terminal, pero sincroniza cada turno en el chat del cuaderno vía RPC `chat.send_message` y detecta automáticamente las dudas o errores del estudiante para registrarlos de forma silenciosa en la nota nativa `00_CUADERNO_DE_LAGUNAS` (`notes.update_note`).
   - Opera 100% bajo la cuota de cómputo de Google One (5TB), con **cero consumo de saldo de APIs externas pagas** (OpenAI/Anthropic).

5. **`nlm-tutor schedule <UUID>` (Calculador Matemático de Ebbinghaus)**:
   - Calcula las fechas e intervalos óptimos de repaso espaciado (+24h, +72h, +7d, +14d, +30d) basados en la curva del olvido.
   - Lee la nota nativa `00_CUADERNO_DE_LAGUNAS` vía RPC (`notes.get_notes`) para enfocar cada hito en los puntos ciegos detectados.
   - Gasta **cero tokens LLM** (cálculo algorítmico determinista en tiempo de ejecución).

6. **`nlm-tutor prompt <UUID> <1-12> [--send]` (Biblioteca de Prompts Maestros)**:
   - Permite disparar de forma atómica cualquiera de los 10 prompts pedagógicos hacia el chat del cuaderno:
     - `1`: Resumen de Máximo Detalle (Construcción del Mapa Base)
     - `2`: Explicación Didáctica Feynman (Enseñanza desde Cero)
     - `3`: Testing de 10 Preguntas de Razonamiento (No Memoria)
     - `4`: Plan de Sesión de 90 Minutos (Método MIT 1972)
     - `5`: Kit de Repaso Final & Hoja de Errores Típicos
     - `6`: Debates, Matices Críticos y Vías de Consenso
     - `7`: Mapa Mental como Syllabus Estructural
     - `8`: Kaufman 80/20 (Deconstrucción en Micro-habilidades)
     - `9`: Kaufman Autocorrección JIT (Los 3 Errores Más Comunes)
     - `10`: Anti-Bloqueo Emocional (Analogía Inmediata)

