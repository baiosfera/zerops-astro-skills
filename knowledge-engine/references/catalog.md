# Knowledge Hub Catalog & Granular Playbook Matrix (v4.0 — Drive-First)

This catalog maps the clean educational corpus in Google Drive (`baiosfera:KNOWLEDGE_HUB/01_TRANSCRIPCIONES_LIMPIAS/`, including `DIGITALMARKETER` [EN], `PLATZI`, `CA`, `MCV`, `SCVIP`, `CENOF`, `VELOCITYMEDIA`, `ESCRITURA_LIBROS`, `SEO`, `MARKETING`) into **21 specialized Master Playbooks + `INDEX.json`** in `03_PLAYBOOKS_MAESTROS/` and **3 Tactical Banks** in `04_BANCOS_TACTICOS/`. Any ZCP project syncs them automatically into `/mnt/localstorage/playbooks/` via `iniciar.sh` and `zcp-sync` with zero mandatory Qdrant runtime.

---

## 1. Master Playbooks (`03_PLAYBOOKS_MAESTROS/`)

| ID | Focus & Apotelos Role | Target Agents |
|---|---|---|
| `00_category_of_one.md` | **Corona 1 (`tau_0_corona_1`)**: Blue Ocean, categoría propia, mecanismo único, pricing por valor | `strategist`, `brand_architect`, `copywriter` |
| `01_velocity_sales_doctrine.md` | **Corona 2 (`tau_0_corona_2`)**: Venta sutil, tensión constructiva, sobredemanda, apalancamiento | `strategist`, `copywriter`, `sales_closer` |
| `02_psicologia_consumidor_y_avatar.md` | **Fundamentos (`tau_0_icp`)**: Niveles de conciencia, dolores, VoC, sesgos, prueba social | `strategist`, `copywriter`, `ads_planner` |
| `03_ofertas_irresistibles_y_pricing.md` | **Fundamentos (`tau_3_oferta`)**: Ecuación de valor, bonos, anclaje, tripwires, garantías | `strategist`, `copywriter`, `cro_architect` |
| `04_branding_autoridad_y_storytelling.md` | **Fundamentos (`tau_0_voz_marca`)**: Voz verbal, arco narrativo, autoridad | `brand_architect`, `copywriter`, `content_strategist` |
| `05_copywriting_landings_y_angulos.md` | **Conversión (`tau_3_copy_astro_web`)**: Landings SEO-first & Ads-first, hooks, bullets, objeciones | `copywriter`, `astro_web_builder` |
| `06_vsl_webinars_y_lanzamientos.md` | **Conversión (`tau_3_video_ventas`)**: Guiones VSL, webinars, retos, promociones | `copywriter`, `funnel_architect` |
| `07_funnels_checkout_y_pagos.md` | **Conversión (`tau_3_conversion_transaccional`)**: Embudos, `checkout-funnels`, bumps/upsells, `payment-gateways` (Wompi, ePayco, Bold, Stripe, dLocalGo, MercadoPago, COD OTP) | `funnel_architect`, `astro_web_builder`, `checkout_engineer` |
| `08_analitica_cro_y_experimentacion.md` | **Telemetría (`tau_1_medicion`)**: GA4, CAC/LTV/AOV, tests A/B, UX CRO | `analytics_engineer`, `cro_architect` |
| `09_seo_tecnico_y_contenidos.md` | **Descubrimiento (`tau_2_seo`)**: Keywords, topic clusters, siloing, Schema.org, Cloudflare Edge | `seo_specialist`, `copywriter`, `astro_web_builder` |
| `10_aeo_y_geo_busqueda_ia.md` | **Descubrimiento (`tau_2_aeo_geo`)**: Citabilidad en IA (ChatGPT/Perplexity/AI Overviews), `llms.txt`, JSON-LD | `seo_specialist`, `copywriter`, `astro_web_builder` |
| `11_youtube_y_video_largo.md` | **Orgánico (`tau_2_video_largo`)**: Packaging CTR, retención, SEO YouTube, captura de leads | `content_strategist`, `video_strategist` |
| `12_reels_tiktok_y_instagram_organico.md` | **Orgánico (`tau_2_social_corto`)**: Hooks 3s, formatos virales, historias, DM triggers | `content_strategist`, `social_manager` |
| `13_linkedin_b2b_y_autoridad.md` | **Orgánico (`tau_2_b2b`)**: Perfil All-Star, posts B2B, social selling | `content_strategist`, `b2b_prospector` |
| `14_meta_ads_y_creativos.md` | **Paid Media (`tau_1_paid_meta`)**: Estructura Meta Ads, testing de ángulos, escalado | `media_buyer`, `creative_strategist`, `copywriter` |
| `15_google_ads_search_y_pmax.md` | **Paid Media (`tau_1_paid_google`)**: Search intención alta, Shopping/PMax, Quality Score | `media_buyer`, `seo_specialist` |
| `16_tiktok_ads_y_linkedin_ads.md` | **Paid Media (`tau_1_paid_expansion`)**: Spark Ads UGC, LinkedIn Ads B2B | `media_buyer`, `creative_strategist` |
| `17_ad_telemetry_pixeles_y_consent.md` | **Telemetría (`tau_1_telemetria_core`)**: Meta CAPI, Google Enhanced Conversions, TikTok Events API, LinkedIn Insight/CAPI, Consent Mode v2, Outbox PG18+NATS | `telemetry_engineer`, `astro_web_builder`, `media_buyer` |
| `18_email_marketing_y_deliverability.md` | **Retención (`tau_4_email_coherente`)**: Listmonk/ZeptoMail + BullMQ, secuencias ciclo de vida, DMARC/DKIM | `lifecycle_marketer`, `copywriter` |
| `19_whatsapp_conversacional_y_cierre.md` | **Retención (`tau_4_whatsapp_coherente`)**: EvolutionGo + NATS + Valkey fencing, calificación BANT y cierre | `conversational_designer`, `sales_closer` |
| `20_ventas_consultivas_high_ticket.md` | **Retención (`tau_4_cierre_humano`)**: Cierre 1 llamada, neuroventas, manejo de objeciones | `sales_closer`, `strategist` |

---

## 2. Tactical Banks (`04_BANCOS_TACTICOS/`) & Routing (`INDEX.json`)

- `00_category_of_one_swipes_y_guiones.md` — Swipes estratégicos y guiones de autoridad.
- `01_biblioteca_210_prompts_maestros.md` — Biblioteca de prompts tácticos.
- `02_swipes_copy_email_y_paid_ads.md` — Swipes de copy, asuntos email y ángulos de pauta.
- `03_PLAYBOOKS_MAESTROS/INDEX.json` — Mapa ligero (`< 7 KB`) con `task_routes` para CrewAI / Hermes (`brand_strategy_blackboard`, `astro_web_landing_seo_ads_first`, `checkout_funnels_y_pagos`, `vsl_webinars_lanzamientos`, `paid_media_campanas`, `organic_growth_y_contenido`, `retencion_email_whatsapp_cierre`).
