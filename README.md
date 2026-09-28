# Zerops Astro Skills (`zerops-astro-skills`)

Catalogo soberano de **65 Agentic Skills** desacopladas para desarrollo fullstack, branding, e-commerce, diagnostico metafisico e infraestructura en Zerops Cloud.

Disenadas bajo la metodologia Dual-RAG, arquitectura Fractal CoHaLo y compatibilidad nativa con Antigravity, Claude Code y OpenCode.

---

## Estructura y Compatibilidad

Todas las skills se organizan en estructura plana en la raiz del repositorio (`/<skill-name>/SKILL.md`) para resolucion directa sin overhead de subdirectorios:

- **Router Atómico**: Cada carpeta contiene un `SKILL.md` con frontmatter YAML (nombre, descripcion, triggers).
- **Dual-RAG**: Referencias profundas desacopladas en `references/usage.md` e `references/infra.md`.
- **Harness & Sensores**: Scripts de validacion determinista en `scripts/` y esquemas en `assets/`.

---

## Clusters Funcionales (65 Skills)

### 1. Flujo de Ejecucion & Metacognicion
- `cohalo`: Context, Harness, Loops y arquitectura de prompts bajo CoHaLo v7.0.
- `planner`: Planificacion maestra y gobernanza SSoT bajo Supreme Directive.
- `docu`: Arquitectura y certificacion de skills Dual-RAG.
- `research`: Pipeline de investigacion epistemica en vivo con 12 motores.

### 2. Diseno de Identidad Visual & UX (AstroBranding)
- `symbol`: Isologos, monogramas, geometria sagrada y vectores monocromaticos SVG.
- `chroma`: Ecosistemas cromaticos OKLCH y auditoria WCAG 2.2 AAA / APCA.
- `fontgen`: Matriz tipografica y emparejamientos hibridos Google Fonts / Envato.
- `kinetic`: Animacion a 60fps con GSAP y sintesis de micro-audio procedural ADSR.
- `brandbook`: Consolidacion de Brand Manual y tokens W3C DTCG.
- `orchesbrand`: Orquestador integral del pipeline de identidad de marca.

### 3. Diagnostico Metafisico & Motores Astrologicos (Oraculo)
- **Diagnosticos**: `oraculo`, `oraculo-diag-a-psy`, `oraculo-diag-b-voc`, `oraculo-diag-c-mkt`, `oraculo-diag-d-leg`, `oraculo-diag-e-geo`.
- **Motores REST & MCP**: `astrologyapi`, `astroway`, `bazi-lunar`, `freeastroapi`, `hebcal`, `kundali`, `nasa`, `vedastro`, `zmanim`.

### 4. Comercio Soberano, Pagos & Logistica (Revenue)
- `checkout-funnels`: Embudos de conversion multiautopasarela (Wompi, ePayco, Stripe, COD).
- `payment-gateways`: Validaciones criptograficas de webhooks e idempotencia con Valkey.
- `orders-fulfillment`: Despacho multicarrier (Coordinadora, Servientrega, Envia, MiPaquete, Skydropx) y rotulacion termica.
- `growth-engine`: Neurocopywriting, ofertas de alto valor y recuperacion de carritos.
- `sales-enablement`: AI SDRs, AI Closers y scoring de leads con pgvector.

### 5. Comunicacion Omnicanal & CRM
- `whatsapp-engine`: Mensajeria desacoplada con EvolutionGo, NATS y Bifrost.
- `email-marketing`: Motores transaccionales con React Email, ZeptoMail y SES v2.
- `listmonk`: Gestion de suscriptores y newsletters de alto volumen.
- `social-distrib`: Distribucion programada en Instagram, TikTok, LinkedIn y X.
- `crmfrappe`: Gestion de leads y tratos en Frappe CRM.
- `erpnext`: Sincronizacion ERPNext, ordenes y facturacion electronica DIAN Colombia.

### 6. Bases de Datos, Mensajeria & Event-Mesh
- `postgresql`: PostgreSQL 18 relacional y vector embeddings con pgvector HNSW.
- `valkey`: Cache en memoria, colas BullMQ y bloqueos de concurrencia distribuidos.
- `nats`: NATS Server 2.12, RPC de sub-milisegundo (<0.3ms P99) y JetStream.
- `qdrant`: Base de datos vectorial para busqueda hibrida y RAG.
- `directus`: Headless CMS, BaaS relacional y RAG Flows.
- `bknd`: Orquestador maestro de backend y malla de microservicios.
- `devllm-telemetry`: Telemetria de infraestructura, NATS y costos LLMOps.
- `business-insights`: Analiticas comerciales y financieras.

### 7. Infraestructura Zerops & Cloud
- `zcp`: Orquestador maestro de Zerops, 22 herramientas MCP y contenedores Incus LXC.
- `local-storage`: Volumenes persistentes POSIX nativos (`local-storage:single@1`).
- `cloudflare`: Gestion de DNS, WAF rules, SSL Full Strict y Turnstile.
- `ghcicd`: Entrega continua GitOps en 3 entornos con GitHub Actions.
- `dckr`: Despliegue de contenedores Docker en Zerops VM.

### 8. AI Gateways & Agentes Autonomos
- `bifrost`: AI Gateway de alto rendimiento (sub-100us) y enrutamiento CEL.
- `freellmapi`: Proxy agregado de inferencia gratuita con failover inteligente.
- `hermes-agent`: Agente Nous Hermes para control ejecutivo via Telegram y NATS.
- `notebooklm`: RAG de Google NotebookLM con 49 herramientas FastMCP.
- `automation-engine`: Orquestacion orientada a eventos con NATS JetStream y BullMQ.

### 9. Runtimes, Frameworks & Frontend Core
- `frnt`: Master Frontend (Astro 5, React 19, Tailwind 4, Zustand 5, Playwright).
- `astro`: Framework Astro 5 SSR en Bun y Node.js.
- `bun`: Runtime Bun 1.3, Elysia y TypeScript nativo.
- `nodejs`: Runtime Node.js 24 LTS.
- `python`: Runtime Python, Granian y ASGI.
- `fastapi`: Microservicios FastAPI con Granian Rust ASGI.
- `golang`: Runtime Go y microservicios nativos.
- `rust`: Microservicios de alto rendimiento con Axum y Tokio.
- `alpine`: Base minimalista Alpine Linux y musl libc.
- `ubuntu`: Base Ubuntu 24.04 LTS y glibc.
- `seo-aeo-geo`: Optimizacion SEO, AEO, GEO, Knowledge Graph y llms.txt.

---

## Consumo Rapido

Para clonar e integrar en cualquier entorno o contenedor en menos de 2 segundos:

```bash
git clone --depth 1 https://github.com/elplacerdc/zerops-astro-skills.git ~/.gemini/antigravity-cli/skills
```

Licencia: Apache-2.0
