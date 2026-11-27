# `brand-studio` — Guía Operativa `run_workflow` (v2.2)

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

## 3. Destilación Editorial, Pure Positive Guidance y Única SSoT
- **SSoT de Topología:** Exclusivamente `/mnt/localstorage/<Proyecto>/dev/ecosystem.json`.
- **Síntesis de Arquetipo y Oráculo Casa 7:** Destila el briefing del usuario en 1 arquetipo nítido aplicando `PB00` (disciplina humana comprensible antes de neologismos), `PB02` (Avatar 360°, Código Simbólico) y —si aplica— `astrobranding_*.md` (Casa 7 Descendente, Casa 8/11 y Venus), validando invariantes mecánicos con `anti-slop-linter v2.4` y criterio editorial con el Crítico Ciego.
- **Separación `entity_role`:** Presenta `operating_protocol` en 1 frase afirmativa como el método de fondo aplicado al trabajo propio y al de los clientes, manteniendo los selectores de compra reservados para `commercial_offer`.
- **Uso interno (`strategy/`):** `verticales`, `DIY`, `DWY`, `DFY`, `BANT`, `PWYW`, `Order Bump`, `AEO/GEO`, `Rotación Barista`, `Ads-First`, `Comprador Ideal`, `UPPER_SNAKE_CASE`.
- **Uso público aprobado:** Roles reales del fundador, marca comercial y `public_brand_concepts` anclados en lenguaje llano en su primera aparición.

## 4. Reanudar tras Aprobación Visual (Fases 3 a 5)
Tras aprobar colores y fuentes en `preview_gallery.html` / `chroma_preview.html`, ejecutar con `"start_from_phase": "phase_3_concatenation"` y `"stop_after_phase": "phase_5_critic"`.
Para iterar campañas `Ads-First` sobre anuncios nuevos, usar [`references/ad_campaign_factory.md`](file:///var/www/zerops-astro-skills/brand-studio/references/ad_campaign_factory.md).
