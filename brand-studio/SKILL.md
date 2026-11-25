---
name: brand-studio
description: "Trigger: brand-studio, crear marca, pipeline 360, playbook-first, con o sin oraculo, brand brief, estudio de marca. Sovereign 5-Phase Playbook-First Brand & Conversion Studio via Antigravity run_workflow."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
---

# `brand-studio` — Estudio Integral de Marca, Arte, SEO y Embudo (v1.0)

## Activation Contract
Activar al construir, rehacer o auditar de punta a punta cualquier marca o vertical (**con o sin Oráculo**) sobre Playbooks Maestros (`00..17`), concatenando Posicionamiento $\to$ Keywords SERP reales $\to$ Dirección de Arte + Tipografía a color $\to$ UTM/Píxeles/Remarketing $\to$ Copy SSoT (`copy/*.md`).

## Architectural Invariant (Por qué `run_workflow` y no Hermes/CrewAI)
- **ZCP Nativo (`run_workflow`):** Corre sobre [`workflows/brand-studio/brand_studio.wf`](file:///var/www/zerops-astrobranding/workflows/brand-studio/brand_studio.wf) usando los modelos frontier del usuario y MCPs reales (`firecrawl`, `exa`, `tavily`, `brave`, `jina`, `image-generator`). Cero dependencia de `hermes` (512 MB RAM), `freellmapi` ni `bifrost`.
- **Rol de Hermes / CrewAI:** Reservados exclusivamente para operación post-lanzamiento 24/7 (monitoreo Telegram, alertas y micro-clasificación con `pydanticai`), nunca para ideación ni copywriting creativo.

## Las 5 Fases Obligatorias (Playbook-First)
1. **Fase 1 — Posicionamiento & Keyword Research SERP (`PB00`, `PB06`, `PB16`):** Admite `intake_mode`: `oraculo` (psicología + arquetipos) o `client` (`brand_brief.json` sin carta natal). Valida demanda real SERP en vivo (`exa`/`tavily`/`brave`), define `public_brand_concepts` y crea Topic Clusters (`1 intención = 1 URL`) en `strategy/seo_clusters.json`.
2. **Fase 2 — Dirección de Arte & Pausa Humana (`taste-skill`, `impeccable`, `orchesbrand v4.0`):** Analiza URLs de referencia vía `firecrawl_scrape(branding)`, genera 3 paletas con carácter real en `art_direction_palettes.json` + galería full-color (`envato-font-preview v4.0` con `--envato-urls` opcional) y **detiene el workflow (`stop_after_phase="phase_2_art_direction"`) hasta recibir aprobación humana**.
3. **Fase 3 — Concatenación Total (`PB01`, `03`, `04`, `05`, `07`, `13`, `14` + `apotelos v2.0`):** Construye `strategy/concatenation_matrix.json` uniendo Cluster $\to$ Ángulo $\to$ UTM externo $\to$ Oferta $\to$ Evento Pixel+CAPI $\to$ Remarketing $\to$ Email/WA, validado con `apotelos validate-chain`.
4. **Fase 4 — Escuadrón Paralelo de Copy (`PB02`, `04`, `08..15`):** Agentes especialistas leen capítulos completos (cero recortes `[:4000]`), redactan `copy/*.md` y sincronizan `web/copy_strings.es.json` con `brand-play sync-copy`.
5. **Fase 5 — Juez Adversario Ciego:** Auditoría independiente de impacto visual, rigor comercial y trazabilidad real (cero *checklist-theater*).

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/brand-studio/references/usage.md) — Parámetros `run_workflow`, plantilla `brand_brief.json` y flujo sin Oráculo.
- [`MANUAL_BRAND_STUDIO.md`](file:///var/www/zerops-astrobranding/scripts/MANUAL_BRAND_STUDIO.md) — Manual práctico no técnico de operación 360° y guía UTM.
