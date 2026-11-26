# `brand-studio` — Guía Operativa `run_workflow` (v1.2)

## 1. Invocación desde ZCP (Fase 1 + Fase 2 Visual)
```python
run_workflow(
    ScriptPath="/var/www/zerops-astrobranding/workflows/brand-studio/brand_studio.wf",
    Description="Ejecutar Fase 1 y 2 (SEO SERP + Hub Multirrama + Dirección de Arte) y esperar aprobación visual",
    Args={
        "project": "MiProyecto",
        "vertical": "hub-principal",
        "workspace_dir": "/mnt/localstorage/MiProyecto/dev/workspaces/hub-principal",
        "intake_mode": "auto",  # "oraculo" | "client" | "auto"
        "offer_archetype": "auto",  # "auto" | "multi_branch_hub" | "high_ticket_evaluation" | "saas_trial_tiers" | "transformational_product" | "community_membership"
        "target_country": "Colombia y Latinoamérica",
        "reference_urls": ["https://ejemplo1.com", "https://ejemplo2.com"],
        "envato_urls": ["https://elements.envato.com/fonts/..."],
        "hub_branches": [
            {"branch_slug": "academia", "route_path": "/academia", "future_domain": "academia.com", "delivery_tier": "diy", "public_label": "Comunidad y Academia"},
            {"branch_slug": "mentoria", "route_path": "/mentoria", "future_domain": "mentoria.com", "delivery_tier": "dwy", "public_label": "Mentoría Aplicada"},
            {"branch_slug": "agencia", "route_path": "/agencia", "future_domain": "agencia.com", "delivery_tier": "dfy", "public_label": "Implementación Llave en Mano"}
        ],
        "enable_affiliate_layer": True,
        "vsl_mode": "hybrid_smart_vsl",  # o "lazy_facade_video"
        "stop_after_phase": "phase_2_art_direction"
    }
)
```

## 2. Cortafuegos Terminológico y Única SSoT
- **SSoT de Topología:** Usar exclusivamente `/mnt/localstorage/<Proyecto>/dev/ecosystem.json` (cero duplicados en `_shared/`).
- **Uso estrictamente interno:** `verticales`, `DIY`, `DWY`, `DFY`, `BANT`, `PWYW`, `Order Bump`, `AEO/GEO`, `UPPER_SNAKE_CASE`.
- **Uso público aprobado:** Roles reales del fundador, marcas de cada línea y términos declarados en `public_brand_concepts` dentro del brief o vertical JSON. `anti-slop-linter` bloquea fugas en archivos públicos.

## 3. Esquema Mínimo `brand_brief.json` (Modo Sin Oráculo)
```json
{
  "vertical_slug": "mi-linea",
  "display_name": "Nombre Comercial — Propuesta Principal",
  "intake_mode": "client",
  "offer_archetype": "saas_trial_tiers",
  "positioning_roles": ["Estratega Digital", "Mentor de Marcas"],
  "public_brand_concepts": ["Category of One (CO1)", "One-Person Business (OPB)"],
  "target_avatar": {
    "icp": "Consultores y firmas profesionales en Colombia y LatAm",
    "pain_points": ["Competir por precio", "Operación manual"]
  },
  "primary_offer": {
    "hook": "Prueba sin riesgo / Diagnóstico",
    "core": "$599 USD + $900.000 COP/mes"
  },
  "reference_urls": []
}
```

## 4. Reanudar tras Aprobación Humana (Fases 3 a 5)
Una vez que el fundador aprueba los colores y fuentes en `previews/preview_gallery.html` y `chroma_preview.html`, volver a ejecutar `run_workflow` con `"stop_after_phase": "phase_5_critic"`.
