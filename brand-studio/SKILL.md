---
name: brand-studio
description: "Trigger: brand-studio, crear marca, pipeline 360, playbook-first, con o sin oraculo, brand brief, estudio de marca. Sovereign 5-Phase Playbook-First Brand & Conversion Studio via Antigravity run_workflow."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# `brand-studio` — Estudio Integral de Marca, Arte, SEO y Embudo (v1.1)

## Activation Contract
Activar al construir, rehacer o auditar cualquier marca o ecosistema multirrama (**con o sin Oráculo**) sobre Playbooks Maestros (`00..17`), concatenando Posicionamiento y Hub Multimarca $\to$ Keywords SERP reales $\to$ Dirección de Arte + Tipografía full-color $\to$ Smart-VSL/Simulador + UTMs + Píxeles + Afiliados (`?ref=`) $\to$ Copy SSoT (`copy/*.md`).

## Architectural Invariant (`run_workflow` vs Hermes/CrewAI)
- **ZCP Nativo (`run_workflow`):** Corre sobre [`workflows/brand-studio/brand_studio.wf`](file:///var/www/zerops-astrobranding/workflows/brand-studio/brand_studio.wf) con modelos frontier y MCPs reales (`firecrawl`, `exa`, `tavily`, `brave`, `jina`, `image-generator`). Cero dependencia de `hermes`, `freellmapi` ni `bifrost`.
- **Hermes / CrewAI:** Reservados exclusivamente para operación post-lanzamiento 24/7 (alertas Telegram y micro-clasificación con `pydanticai`), nunca para ideación ni copywriting creativo.

## Cortafuegos Terminológico (Interno vs. Público)
- **Estricto en UI/Copy:** Jamás filtrar jerga operativa (`verticales`, `DIY`, `DWY`, `DFY`, `BANT`, `PWYW`, `Order Bump`, `AEO/GEO`, `UPPER_SNAKE_CASE`) hacia el usuario final. Exponer únicamente roles reales, nombres comerciales y `public_brand_concepts` declarados (auditado con `anti-slop-linter`).

## Las 5 Fases Obligatorias (Playbook-First)
1. **Fase 1 — Posicionamiento, Hub & SERP (`PB00`, `PB06`, `PB16`):** Admite `oraculo` o `client` (`brand_brief.json`), soporta hubs multirrama (`hub_branches`) con puente a dominios futuros, valida intención SERP en vivo (`exa`/`tavily`/`brave`) y fija `1 intención = 1 URL` en `strategy/seo_clusters.json`.
2. **Fase 2 — Dirección de Arte & Pausa Humana (`taste-skill`, `impeccable`, `orchesbrand v4.0`):** Analiza referencias con `firecrawl_scrape(branding)`, diseña 3 paletas de alta convicción y acentos tipográficos editoriales en galería full-color (`envato-font-preview v4.0`) y **detiene el flujo (`stop_after_phase="phase_2_art_direction"`) hasta recibir aprobación humana**.
3. **Fase 3 — Concatenación Total & Afiliados (`PB01`, `03`, `04`, `05`, `07`, `13`, `14`, `16` Módulo 6 + `apotelos v2.1`):** Modela `strategy/concatenation_matrix.json` con telemetría Smart-VSL (`VslWatched90s`, compuerta previa de video), formulario en 3 pasos, UTMs externos, Browser+CAPI deduplicados y programa de afiliados (`?ref=`, `EPC >= $1`, `EPL >= $2`, bloqueo de autocompra), validado con `apotelos validate-chain`.
4. **Fase 4 — Escuadrón Paralelo de Copy (`PB02..16`):** Lee capítulos íntegros, redacta guion Smart-VSL, simulador de 3 pestañas, `copy/*.md`, kit opcional de afiliados (`copy/09`) y sincroniza `web/copy_strings.es.json` con `brand-play sync-copy`.
5. **Fase 5 — Juez Adversario Ciego:** Auditoría independiente de impacto visual, rigor comercial, ortografía limpia y trazabilidad real.

## References
- [`references/usage.md`](file:///var/www/zerops-astro-skills/brand-studio/references/usage.md) — Parámetros `run_workflow` v1.1, `hub_branches` y `brand_brief.json`.
- [`MANUAL_BRAND_STUDIO.md`](file:///var/www/zerops-astrobranding/scripts/MANUAL_BRAND_STUDIO.md) — Manual práctico no técnico de operación 360°, Smart-VSL, UTMs y afiliados.
