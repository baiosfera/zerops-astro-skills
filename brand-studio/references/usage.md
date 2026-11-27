# `brand-studio` — Guía Operativa `run_workflow` (v2.0)

## 1. Contrato de Piloto Automático (Mínima Intervención Humana)
Cuando el usuario pida crear o replantear una marca, línea o campaña en lenguaje natural:
1. El agente resuelve automáticamente `/mnt/localstorage/<Project>/dev/ecosystem.json`, `verticals/<vertical>.json`, `brandbook.json` y el `workspace_dir` activo.
2. El usuario **nunca** debe redactar JSONs ni invocar `run_workflow` manualmente: el agente arma `Args` con valores seguros (`lead_magnet_mechanism="auto"`, `offer_model="auto"`, `enable_ads_first_layer=True`) y ejecuta.
3. Solo se detiene la ejecución para decisiones estratégicas del fundador: aprobación visual (`phase_2_art_direction`) o aprobación de ángulos (`ad_campaign_factory.wf` Fase 2).

## 2. Invocación desde ZCP (`brand_studio.wf` v2.0)
```python
run_workflow(
    ScriptPath="/var/www/zerops-astrobranding/workflows/brand-studio/brand_studio.wf",
    Description="Ejecutar Fase 1 y 2 (Posicionamiento Comprador Ideal + SEO + Arte) y esperar aprobación visual",
    Args={
        "project": "MiProyecto",
        "vertical": "linea-principal",
        "workspace_dir": "/mnt/localstorage/MiProyecto/dev/workspaces/linea-principal",
        "intake_mode": "auto",
        "offer_archetype": "auto",
        "offer_model": "one_to_n_rings",  # "auto" | "one_to_n_rings" | "multi_branch_hub" | "direct_checkout" | "saas_tiers"
        "lead_magnet_mechanism": "auto",  # "auto" | "none" | "freedom_leverage_index" | "diagnostic_quiz" | "roi_cost_gap" | "commission_simulator" | "resource_guide" | "micro_trial"
        "enable_ads_first_layer": True,
        "enable_affiliate_layer": True,
        "enable_cross_funnel_mesh": True,
        "target_country": "Colombia y Latinoamérica",
        "stop_after_phase": "phase_2_art_direction"
    }
)
```

## 3. Cortafuegos Terminológico, Destilación Socrática y Única SSoT
- **SSoT de Topología:** Exclusivamente `/mnt/localstorage/<Proyecto>/dev/ecosystem.json`.
- **Filtro Anti-Parroting y Oráculo Casa 7:** El briefing del usuario se destila con `PB00` (Anclaje Semántico: disciplina humana antes que neologismos, `proprietary_terms_anchors`), `PB02` (Avatar 360°, Código Simbólico) y —si aplica— `astrobranding_*.md` (Casa 7 Descendente, Casa 8/11 y Venus). Nunca listar 5+ profesiones/áreas en hero/subtítulos (`anti-slop-linter` bloquea `audience_laundry_list` y `unanchored_proprietary_term`).
- **Separación `entity_role`:** Un `operating_protocol` transversal se explica como método interno de trabajo, jamás mezclado como producto comercial dentro de los selectores de compra (`commercial_offer`).
- **Uso estrictamente interno (prohibido en textos/JSON públicos):** `verticales`, `DIY`, `DWY`, `DFY`, `BANT`, `PWYW`, `Order Bump`, `AEO/GEO`, `Rotación Barista`, `Ads-First`, `Comprador Ideal`, `UPPER_SNAKE_CASE`.
- **Uso público aprobado:** Roles reales del fundador, marca comercial y `public_brand_concepts` declarados (anclados en lenguaje llano en su primera aparición).

## 4. Reanudar tras Aprobación Visual (Fases 3 a 5)
Tras aprobar colores y fuentes en `preview_gallery.html` / `chroma_preview.html`, ejecutar con `"start_from_phase": "phase_3_concatenation"` y `"stop_after_phase": "phase_5_critic"`.
Para iterar campañas `Ads-First` sobre anuncios nuevos, usar [`references/ad_campaign_factory.md`](file:///var/www/zerops-astro-skills/brand-studio/references/ad_campaign_factory.md).
