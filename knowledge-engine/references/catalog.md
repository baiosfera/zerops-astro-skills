# Knowledge Hub Catalog & Emergent Playbook Matrix (v4.4 — Sequential 01 -> 02 SSoT)

This catalog maps the audited marketing, sales, and frontend design-engineering corpus (`01_TRANSCRIPCIONES_LIMPIAS/` + `PLATZI/12 DEV WEB` — `CA`, `CENOF`, `DIGITALMARKETER` [EN], `MCV`, `PLATZI`, `SCVIP`, `VELOCITYMEDIA`) into `20` specialized, self-contained **Master Playbooks (`00..19`) + `INDEX.json`** in `02_PLAYBOOKS_MAESTROS/` (with formulas, scripts, prompts, checklists, and Blackboard 360° contracts embedded per discipline). Any ZCP project syncs them automatically into `/mnt/localstorage/playbooks/` via `iniciar.sh` and `zcp-sync` with zero mandatory Qdrant runtime.

---

## 1. Master Playbooks (`02_PLAYBOOKS_MAESTROS/`)

| ID | Status | Focus & Apotelos Role | Target Agents |
|---|---|---|---|
| `00_category_of_one.md` | `compiled` | **Corona 1 (`tau_0_corona_1`)**: Blue Ocean, categoría propia, mecanismo único, pricing por valor | `strategist`, `brand_architect`, `copywriter` |
| `01_sales_and_conversion_doctrine.md` | `compiled` | **Corona 2 (`tau_0_corona_2`)**: Venta sutil, tensión constructiva, sobredemanda, apalancamiento, modelos mentales | `strategist`, `copywriter`, `sales_closer` |
| `02_copywriting_and_neurosales.md` | `compiled` | **Conversión (`tau_3_copy_astro_web`)**: Copy respuesta directa, storytelling, neuroventas, guiones | `copywriter`, `astro_web_builder` |
| `03_irresistible_offers_and_pricing.md` | `compiled` | **Fundamentos (`tau_3_oferta`)**: Ecuación de valor, producto, bonos, garantías, pricing | `strategist`, `copywriter`, `cro_architect` |
| `04_funnels_vsl_webinars_and_challenges.md` | `compiled` | **Conversión (`tau_3_video_ventas`)**: Embudos, VSLs, webinars de alta conversión, retos | `funnel_architect`, `copywriter` |
| `05_web_cro_landings_and_ecommerce.md` | `compiled` | **Conversión (`tau_3_cro_web`)**: Landings, UX/UI CRO, product pages e-commerce, testing | `cro_architect`, `astro_web_builder`, `checkout_engineer` |
| `06_seo_aeo_geo_and_organic_content.md` | `compiled` | **Descubrimiento (`tau_2_seo_aeo_geo`)**: SEO técnico, topic clusters, AEO/GEO para motores IA, Schema/GSC | `seo_specialist`, `copywriter`, `astro_web_builder` |
| `07_ad_telemetry_ga4_gtm_and_metrics.md` | `compiled` | **Telemetría (`tau_1_telemetria_core`)**: GA4, GTM, eventos, atribución, BI y métricas de negocio | `analytics_engineer`, `telemetry_engineer`, `media_buyer` |
| `08_instagram_growth_reels_and_funnels.md` | `compiled` | **Orgánico (`tau_2_instagram`)**: Algoritmo de Reels, viralidad, historias y embudos DM en Instagram | `content_strategist`, `social_manager` |
| `09_whatsapp_and_conversational_automation.md` | `compiled` | **Retención (`tau_4_whatsapp_coherente`)**: Flujos conversacionales WhatsApp/chatbots, regla 24h, cierre en chat | `conversational_designer`, `sales_closer` |
| `10_tiktok_and_shortform_video.md` | `compiled` | **Orgánico/Paid (`tau_2_tiktok`)**: Guionización short-form, TikTok orgánico, Spark/TikTok Ads y video ads | `content_strategist`, `media_buyer` |
| `11_linkedin_b2b_authority_and_ads.md` | `compiled` | **Orgánico/Paid (`tau_2_b2b_linkedin`)**: Perfil All-Star, thought leadership, outreach B2B y LinkedIn Ads | `b2b_prospector`, `content_strategist`, `media_buyer` |
| `12_email_marketing_and_lifecycle_automation.md` | `compiled` | **Retención (`tau_4_email_coherente`)**: Newsletters rentables, CR-VR, entregabilidad SPF/DKIM/DMARC, CRM automation | `lifecycle_marketer`, `copywriter` |
| `13_meta_ads_media_buying_and_scaling.md` | `compiled` | **Paid Media (`tau_1_paid_meta`)**: Estructura Meta Ads, testing creativo, atribución y escalado | `media_buyer`, `creative_strategist` |
| `14_google_ads_and_youtube_growth.md` | `compiled` | **Paid/Orgánico (`tau_1_paid_google`)**: Google Search/Display Ads, YouTube Ads y crecimiento en YouTube | `media_buyer`, `video_strategist` |
| `15_consultative_sales_and_high_ticket_closing.md` | `compiled` | **Retención (`tau_4_cierre_humano`)**: Cierre high-ticket 1 llamada, negociación y manejo de objeciones | `sales_closer`, `strategist` |
| `16_personal_branding_authority_and_communities.md` | `compiled` | **Fundamentos (`tau_0_marca_autoridad`)**: Marca personal, imperios digitales, podcast, afiliados y comunidad | `brand_architect`, `content_strategist` |
| `17_applied_ai_agents_and_prompt_systems.md` | `compiled` | **Operación IA (`tau_0_ai_systems`)**: Sistemas de prompts, asistentes, automatización y agentes | `ai_architect`, `automation_engineer` |
| `18_affiliate_referral_and_partner_growth.md` | `compiled` | **Crecimiento Socios (`tau_3_afiliados`)**: Embajadores, socios profesionales, atribución 90d y reglas anti-fraude | `strategist`, `growth_marketer`, `telemetry_engineer` |
| `19_web_design_systems_craft_and_vibecoding.md` | `compiled` | **Diseño & Craft (`tau_3_design_craft`)**: Visual world (`DESIGN.md`), Atomic Design, tokens, tipografía `@fontsource-variable`, Hero Punch Budget, RAIL y GSAP/Lenis 60fps (`PLATZI/12 DEV WEB`) | `astro_web_builder`, `brand_architect`, `cro_architect`, `ui_designer` |

---

## 2. Routing (`INDEX.json`)

- Each compiled playbook in `02_PLAYBOOKS_MAESTROS/` embeds its own discipline-specific formulas, scripts, prompts, checklists, and Blackboard 360° contracts directly.
- `02_PLAYBOOKS_MAESTROS/INDEX.json` maps `task_routes` for `hermes`, `crewai-engine`, `apotelos`, `brand-play`, and `pi-dev` across all `20/20` active Master Playbooks (`pending_playbooks: 0`).
