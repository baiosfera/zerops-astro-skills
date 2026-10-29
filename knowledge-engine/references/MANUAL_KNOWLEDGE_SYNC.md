# 📘 GUÍA OPERATIVA Y ARQUITECTÓNICA: KNOWLEDGE-SYNC (`knowledge-sync` v2.3)

> **Motor Soberano de Ingesta Dinámica, Parsers Polimórficos, Compactación Multi-Curso y Curaduría de Cuadernos Temáticos en Google NotebookLM Pro (Gemini Notebook) bajo Gobernanza CoHaLo v8.5 y Frugalidad SHARED.**

---

## 🏛️ 1. Misión y Filosofía Arquitectónica

El ecosistema pedagógico de Baiosfera contiene miles de recursos educativos (videos, subtítulos, guías, manuales y notas) distribuidos entre diversas academias y proveedores (`PLATZI`, `DIGITALMARKETER`, `CURSOS` incluyendo `CA`, `SCVIP`, `MCV`, `VELOCITYMEDIA` y autores independientes).

Subir lecciones individuales fragmentadas desborda los límites de cualquier sistema RAG tradicional. `knowledge-sync` resuelve este desafío implementando **fusión de alta densidad**:
- **NotebookLM Pro**: Límite estricto de **300 fuentes por cuaderno**, con ventana masiva de **500.000 palabras por fuente**.
- **Compactación Canónica**: Convierte 20 a 50 lecciones dispersas de un curso en **1 solo compendio maestro** estructurado en Markdown, reduciendo el consumo de fuentes en **>85%**.
- **15 Cuadernos Temáticos Soberanos**: No existen cuadernos por proveedor ("Cuaderno Platzi"). Existen **15 Cuadernos por Especialidad** (`FUNNELS`, `COPYWRITING`, `SEO`, `DATA_ANALYTICS`, `PRODUCT_MANAGEMENT`, etc.) donde convive y se cruza el conocimiento de todas las academias.
- **Invariante Zero-Drive-Creep**: Restricción estricta del perímetro a las 3 ubicaciones pedagógicas autorizadas (`/var/www/baiosfera/CURSOS`, `/var/www/baiosfera/DIGITALMARKETER`, `/var/www/baiosfera/PLATZI`). Se excluyen de forma tajante carpetas de código (`DEV VIBE CODING`, `SPEC DRIVEN DEVELOPER`), autoría literaria (`ESCRITURA LIBROS`), astrología o proyectos activos, protegiendo el almacenamiento y la pureza temática.
- **Playbooks 100% Agnósticos**: Los artefactos generados en `/var/www/baiosfera/PLAYBOOKS/` son frameworks algorítmicos puros, sin menciones a marcas de academias ni autores, listos para transmutarse por las marcas activas de Zerops.

---

## 🧠 2. Motor Polimórfico de Clasificación e Ingesta

El clasificador opera mediante una arquitectura en capas diseñada para eliminar el "brute heuristics" y la fuga de keywords entre carpetas contenedoras:

### Capa 0: Parser Universal de Tags entre Corchetes (`[TAG]`)
Evalúa tanto el nombre de archivo como las carpetas intermedias buscando patrones `[TAG]` (ej. `[SEO]`, `[PRODUCT]`, `[VENTAS]`, `[UXUI]`, `[DATA]`, `[AGILE]`). Cubre **32 tokens verificados de Platzi** y cualquier curso de otras academias que use etiquetado estándar:
- `[SEO]` $\to$ `seo`
- `[PRODUCT]`, `[PRODUCTO]` $\to$ `product_management`
- `[DATA]`, `[DATOS]` $\to$ `data_analytics`
- `[SOCIAL]`, `[COMMUNITY]` $\to$ `social_media`
- `[COPY]`, `[REDACCION]` $\to$ `copywriting`
- `[FUNNEL]`, `[CRO]` $\to$ `funnels`
- `[ECOMMERCE]` $\to$ `ecommerce`
- `[EMAIL]` $\to$ `email_marketing`
- `[ADS]`, `[MEDIA]` $\to$ `paid_ads`
- `[BRAND]`, `[DISENO]` $\to$ `branding`
- `[UX]`, `[UI]`, `[UXUI]` $\to$ `ux_ui`
- `[AUTOMATIZACION]` $\to$ `automatizaciones`
- `[IA]`, `[PROMPTING]` $\to$ `ia_prompting`

### Capa 1: Parser Polimórfico para DigitalMarketer
En DigitalMarketer no existen tags `[TAG]` y las carpetas usan la convención `Title_slug` (ej. `Meta_Ads_Playbook_meta-ads-playbook-kk`). El parser:
1. Elimina el sufijo del slug y los guiones bajos para extraer el título limpio en inglés.
2. Aplica matching léxico exacto contra palabras clave en inglés de los 15 clusters.
3. **Aislamiento de Lecciones**: Nunca busca keywords en carpetas de pasos internos (`01_PLAN`, `02_EXECUTE`, `03_REVIEW`) para evitar falsos positivos.

### Capa 2: Reglas Especiales de Enrutamiento y Agrupación
- **SCVIP**: Mapeo directo por carpetas temáticas numeradas (`06. META ADS` $\to$ `paid_ads`, `04. INSTAGRAM` $\to$ `social_media`, `05. VENTAS` $\to$ `funnels`).
- **Luis Inestrosa**: Agrupación automática de archivos sueltos bajo el curso canónico `Taller CONFERENCIAS QUE VENDEN`.
- **VelocityMedia**: Detección de sprints temáticos (`Copy Sprint` $\to$ `copywriting`, `Offer Sprint` $\to$ `ofertas`).

### Capa 3: Stem Deduplication & Peer-Docs
Para cursos con múltiples formatos por lección (video, audio, subtítulo, documento), el escáner selecciona **una única fuente canónica de máxima fidelidad**:
$$\text{Documento Directo (.docx / .pdf / .md)} > \text{Subtítulo (.es.srt > .srt > .vtt)} > \text{Audio (.aac / .mp3)} > \text{Video (.mp4)}$$

---

## 🗺️ 3. Mapa Canónico de los 15 Cuadernos Temáticos

Los 15 cuadernos en Google NotebookLM Pro están indexados con títulos canónicos fijos:

| # | Cluster Key | Cuaderno en NotebookLM | Especialidad y Cobertura Temática |
|---|---|---|---|
| 1 | `funnels` | `[ESPECIALIDAD_FUNNELS]` | Embudos de venta, VSL, tripwires, webinars, carritos, CRO. |
| 2 | `copywriting` | `[ESPECIALIDAD_COPYWRITING]` | Persuasión, ganchos, storytelling, cartas de venta, microcopy. |
| 3 | `ofertas` | `[ESPECIALIDAD_OFERTAS]` | Grand Slam Offers (Hormozi), pricing, garantías, bonus stacks. |
| 4 | `ecommerce` | `[ESPECIALIDAD_ECOMMERCE]` | Tiendas online, logística, pasarelas, AOV, checkout optimization. |
| 5 | `email_marketing` | `[ESPECIALIDAD_EMAIL_MARKETING]` | Secuencias automatizadas, lead nurturing, entregabilidad, reactivación. |
| 6 | `whatsapp_funnels` | `[ESPECIALIDAD_WHATSAPP_FUNNELS]` | Chatbots, mensajería conversacional, cierres 1 a 1, scripts WA. |
| 7 | `paid_ads` | `[ESPECIALIDAD_MEDIA_BUYING]` | Meta Ads, Google Ads, TikTok Ads, creativos, segmentación. |
| 8 | `branding` | `[ESPECIALIDAD_BRANDING]` | Identidad visual, arquetipos de marca, diseño corporativo, posicionamiento. |
| 9 | `ux_ui` | `[ESPECIALIDAD_UX_UI]` | Arquitectura de información, wireframes, diseño centrado en usuario. |
| 10 | `automatizaciones` | `[ESPECIALIDAD_AUTOMATIZACIONES]` | Webhooks, N8N, Zapier, Make, flujos event-driven, CRM sync. |
| 11 | `ia_prompting` | `[ESPECIALIDAD_IA_PROMPTING]` | Prompt engineering, agentes autónomos, LLMs, RAG, flujos agénticos. |
| 12 | `seo` | `[ESPECIALIDAD_SEO]` | Posicionamiento orgánico, SEO técnico, On-Page, Off-Page, Search Console. |
| 13 | `social_media` | `[ESPECIALIDAD_SOCIAL_MEDIA]` | Estrategia de contenidos, Instagram, TikTok, LinkedIn, calendarios. |
| 14 | `data_analytics` | `[ESPECIALIDAD_DATA_ANALYTICS]` | Métricas de negocio, analítica digital, GA4, SQL, dashboards y KPIs. |
| 15 | `product_management` | `[ESPECIALIDAD_PRODUCT_MANAGEMENT]` | Ciclo de vida del producto, Product-Market Fit, metodologías ágiles. |

---

## ⚡ 4. Cheatsheet de Comandos CLI

El ejecutable `knowledge-sync` (enlazado globalmente en `/usr/local/bin/knowledge-sync`) soporta tanto **sintaxis posicional limpia** como flags tradicionales.

### 4.1 Escaneo y Diagnóstico Rápido (`scan`)
```bash
# Escanear las 3 rutas pedagógicas autorizadas por defecto (sin gastar cuota)
knowledge-sync scan

# Escanear un directorio específico como argumento posicional (¡Nuevo!)
knowledge-sync scan /var/www/baiosfera/DIGITALMARKETER

# Escanear con flag tradicional y profundidad controlada
knowledge-sync scan --target /var/www/baiosfera/CURSOS/CA --max-depth 3
```

### 4.2 Compactación y Generación de Compendios (`compact`)
```bash
# Simular compactación sobre las rutas por defecto (modo seguro sin escribir en disco)
knowledge-sync compact --dry-run

# Simular compactación sobre una ruta específica arbitraria (argumento posicional)
knowledge-sync compact /var/www/baiosfera/CURSOS/CA --dry-run

# Compactar un cluster específico de un proveedor específico
knowledge-sync compact --cluster funnels --provider DIGITALMARKETER

# Compactar lecciones hacia un directorio de caché local personalizado
knowledge-sync compact --cluster copywriting --output-dir /var/www/localstorage/knowledge_cache/compendiums
```

### 4.3 Ingesta Idempotente hacia Google NotebookLM Pro (`push`)
```bash
# Subir compendios consolidados hacia el cuaderno de una especialidad (Recomendado)
knowledge-sync push --compendiums --cluster seo --limit 10

# Subir compendios con delay defensivo anti-rate-limit (jitter automático)
knowledge-sync push --compendiums --cluster copywriting --delay 6.0

# Subir compendios de una ruta ad-hoc hacia un cuaderno específico
knowledge-sync push /var/www/localstorage/knowledge_cache/compendiums/seo --cluster seo --limit 5
```

### 4.4 Inicialización de Cuadernos (`init-clusters`)
```bash
# Crear los 15 cuadernos temáticos con sus títulos y descripciones oficiales en NotebookLM
knowledge-sync init-clusters
```

### 4.5 Suite de Pruebas Físicas (`--test`)
```bash
# Ejecutar las 8 pruebas unitarias deterministas en memoria (exit code 0 obligatorio)
knowledge-sync --test
```

---

## 🚀 5. Ejecución Dinámica sobre Nuevas Ubicaciones (Zero Lock-In)

Aunque el script protege el perímetro por defecto para evitar leer carpetas indebidas, **es 100% dinámico y reutilizable**:
1. **Ejecución Ad-Hoc**: Si mañana descargas una carpeta `/var/www/baiosfera/CURSOS_NUEVOS_2027/`, simplemente ejecutas:
   ```bash
   knowledge-sync scan /var/www/baiosfera/CURSOS_NUEVOS_2027/
   ```
2. **Reconocimiento de Tags**: Si los cursos nuevos incluyen etiquetas entre corchetes (ej. `[SEO] Curso Avanzado`), el clasificador Capa 0 los categoriza al 100% de forma determinista.
3. **Fallback Léxico**: Si no tienen corchetes, el analizador sintáctico evalúa el título del curso contra las keywords maestras de los 15 clusters.

---

## 🔄 6. Flujo Operativo Completo (Workflow E2E)

```
┌────────────────────────────────────────────────────────┐
│  /var/www/baiosfera/{CURSOS, DIGITALMARKETER, PLATZI}  │  <- Cursos crudos (Videos, SRTs, PDFs, DOCX)
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼ 1. knowledge-sync scan [target]
┌────────────────────────────────────────────────────────┐
│      Clasificador Multi-Capa (Capa 0: [TAG])           │  <- Asigna a 1 de los 15 clusters temáticos
│          & Stem Deduplication Canónica                 │  <- Selecciona fuente de mayor fidelidad
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼ 2. knowledge-sync compact [--dry-run]
┌────────────────────────────────────────────────────────┐
│    /var/www/localstorage/knowledge_cache/compendiums/  │  <- Compendios Markdown por (Curso, Cluster)
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼ 3. knowledge-sync push --compendiums
┌────────────────────────────────────────────────────────┐
│            Google NotebookLM Pro (Gemini)              │  <- Ingesta directa a los 15 Cuadernos Temáticos
│      ([ESPECIALIDAD_FUNNELS], [ESPECIALIDAD_SEO], …)   │  <- Máximo 300 fuentes de 500k palabras c/u
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼ 4. Síntesis Agéntica (knowledge-engine)
┌────────────────────────────────────────────────────────┐
│             /var/www/baiosfera/PLAYBOOKS/              │  <- Playbooks 100% Agnósticos (Zero-Brand Slop)
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼ 5. Infusión de Marca Local (Brandbook Tokens)
┌────────────────────────────────────────────────────────┐
│                astro-web / frnt / bknd                 │  <- Componentes y Copy de Producción en Zerops
└────────────────────────────────────────────────────────┘
```

---

## 🛠️ 7. Mantenimiento y Recuperación ante Fallos

1. **Persistencia SSoT de Dependencias**:
   - `poppler-utils` (`pdftotext`) está declarado en [`setup-zcp.sh`](file:///var/www/zerops-astrobranding/scripts/setup-zcp.sh) y en Google Drive SSoT ([`setup-zcp.sh` en Drive](file:///var/www/baiosfera/0ZEROPS-AGY/0zcp-123/scripts/setup-zcp.sh)).
   - En arranques en frío, `iniciar.sh -> unisetup.sh -> setup-zcp.sh` garantiza su disponibilidad sin intervención manual.
2. **Idempotencia Absoluta**:
   - Cada compendio genera una huella SHA-256 única. Si el archivo no ha cambiado, `push` lo omite automáticamente sin consumir ancho de banda ni cuotas de API.
3. **Limpieza de Almacenamiento Local**:
   - Para regenerar compendios desde cero:
     ```bash
     rm -rf /var/www/localstorage/knowledge_cache/compendiums/
     knowledge-sync compact
     ```
