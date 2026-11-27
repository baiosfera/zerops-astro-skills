---
name: brand-studio
description: "Trigger: brand-studio, crear marca, pipeline 360, playbook-first, con o sin oraculo, brand brief, estudio de marca, ad-library, ad-campaign-factory, ads-first, meta ad library, rotacion barista, comprador ideal, interactive proof. Sovereign Dual-Layer Brand & Ads-First Conversion Studio via Antigravity run_workflow."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "2.1"
---

# `brand-studio` — Estudio Dual de Marca, SEO y Fábrica Ads-First (v2.1)

## Activation Contract
Activar al construir, rehacer o escalar cualquier marca o campaña (**con o sin Oráculo**) sobre Playbooks (`00..18`) con **mínima intervención del usuario**: el agente auto-resuelve `ecosystem.json`, `brandbook.json`, `ad-library` y los parámetros de `run_workflow` desde una instrucción en lenguaje natural, pausando únicamente para aprobación estratégica de arte (Fase 2) o ángulos/anuncios.

## Architectural Invariant (`run_workflow` vs Hermes/CrewAI)
- **ZCP Nativo (`run_workflow`):**
  1. `brand_studio.wf` (`v2.0`): diseño fundacional 1 vez por marca/línea (Posicionamiento $\to$ Arte $\to$ Matriz $\to$ Copy SSoT $\to$ Crítico).
  2. `ad_campaign_factory.wf` (`v1.0`): fábrica repetible **Ads-First** de bajo consumo (`ad-library` 0-tokens $\to$ ángulos $\to$ hidratación paralela `campaigns/<slug>.json` $\to$ gates deterministas $\to$ crítico).
- **Hermes / CrewAI:** Reservados para operación post-lanzamiento 24/7 (`ad-library --diff` / monitoreo), nunca ideación creativa.

## Pilares Estratégicos & Filtro Playbook-First
1. **Anti-Parroting, Desafío Socrático & Oráculo Casa 7:** Nunca repetir listas o notas crudas del usuario en copy público (prohibido efecto "ayudo a todo el mundo"). Destilar siempre mediante `PB02` (Avatar 360°, Código Simbólico, Top 3 Botones Reptilianos) y —cuando exista Oráculo— **Casa 7 (Descendente)**, **Casa 8/11** y **Venus**. Separar estrictamente `operating_protocol` (cómo trabaja el fundador) de `commercial_offer` (qué compra el cliente).
2. **Anclaje Semántico (`PB00` · Prueba de 50 Palabras) + Contraste `CO1`:** Nombrar primero la disciplina real reconocible (astrología, numerología, automatización, mentoría) antes de cualquier nombre propio o metodología inventada.
3. **Núcleo Orgánico + Capa Dinámica Ads-First:** Rutas fijas `SEO/AEO/GEO` (`index, follow`, 1 intención = 1 URL, `@graph`, `/llms.txt`) conviven sin canibalización con `/[vertical]/lp/[slug]` (`noindex, follow` por defecto salvo `seo_cluster_id`).
4. **Lead Magnet Polimórfico Opcional (`lead_magnet_mechanism`):** Nunca forzar calculadoras. Elegir por ángulo entre `none`, `freedom_leverage_index`, `diagnostic_quiz`, `roi_cost_gap`, `commission_simulator`, `resource_guide` o `micro_trial`.
5. **Cortafuegos Terminológico:** Prohibido filtrar jerga interna (`verticales`, `DIY`, `DWY`, `DFY`, `BANT`, `PWYW`, `Order Bump`, `AEO/GEO`, `Rotación Barista`, `Ads-First`, `Comprador Ideal`, `UPPER_SNAKE_CASE`) al público. Única SSoT: `/mnt/localstorage/<Proyecto>/dev/ecosystem.json`.

## Las 5 Fases de `brand_studio.wf`
1. **Fase 1:** Comprador Ideal, `CO1`, Oferta `1 → N`, Hub `1 ruta = 1 SSoT`, Anti-AMN en vivo y clústeres `seo_clusters.json`.
2. **Fase 2:** `taste-skill` + `impeccable` + `orchesbrand` (3 paletas WCAG `>= 4.5:1`, `100% WebP/AVIF`) y **pausa humana (`stop_after_phase="phase_2_art_direction"`)**.
3. **Fase 3:** `concatenation_matrix.json` (`InteractiveProofSpec`, `offer_rings`, `ViewContent` solo landing, `cross_domain_bridge`, `?ref=`, `cross_funnel_bridges`) validado con `apotelos validate-chain`.
4. **Fase 4:** Escuadrón paralelo (`copy/*.md`) + reconciliación `brand-play sync-copy --all-files`.
5. **Fase 5:** Juez Adversario Ciego (`APPROVED` / `NEEDS_REVISION`).

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/brand-studio/references/usage.md) — Parámetros `brand_studio.wf` v2.0 y contrato de piloto automático.
- [`references/ad_campaign_factory.md`](file:///var/www/zerops-astro-skills/brand-studio/references/ad_campaign_factory.md) — Protocolo `ad-library` + `ad_campaign_factory.wf`.
- [`MANUAL_BRAND_STUDIO.md`](file:///var/www/zerops-astrobranding/blueprints/MANUAL_BRAND_STUDIO.md) · [`MANUAL_AD_CAMPAIGN_FACTORY.md`](file:///var/www/zerops-astrobranding/blueprints/MANUAL_AD_CAMPAIGN_FACTORY.md)
