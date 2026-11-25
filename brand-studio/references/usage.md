# `brand-studio` — Guía Operativa `run_workflow` (v1.0)

## 1. Invocación desde ZCP
```python
run_workflow(
    ScriptPath="/var/www/zerops-astrobranding/workflows/brand-studio/brand_studio.wf",
    Description="Ejecutar Fase 1 y 2 (SEO SERP + Dirección de Arte) y esperar aprobación visual",
    Args={
        "project": "MiProyecto",
        "vertical": "mi-vertical",
        "workspace_dir": "/mnt/localstorage/MiProyecto/dev/workspaces/mi-vertical",
        "intake_mode": "auto",  # "oraculo" | "client" | "auto"
        "target_country": "Colombia y Latinoamérica",
        "reference_urls": ["https://ejemplo1.com", "https://ejemplo2.com"],
        "envato_urls": ["https://elements.envato.com/fonts/..."],
        "stop_after_phase": "phase_2_art_direction"
    }
)
```

## 2. Esquema Mínimo `brand_brief.json` (Modo Sin Oráculo)
```json
{
  "vertical_slug": "mi-vertical",
  "display_name": "Nombre Comercial — Propuesta Principal",
  "intake_mode": "client",
  "vertical_archetype": "architectural_b2b",
  "positioning_roles": ["Estratega Digital", "Mentor de Marcas"],
  "public_brand_concepts": ["Category of One (CO1)", "One-Person Business (OPB)"],
  "target_avatar": {
    "icp": "Consultores y firmas profesionales en Colombia y LatAm",
    "pain_points": ["Competir por precio", "Operación manual"]
  },
  "primary_offer": {
    "hook": "Calculadora interactiva / Diagnóstico",
    "core": "$599 USD + $900.000 COP/mes"
  },
  "reference_urls": []
}
```

## 3. Reanudar tras Aprobación Humana (Fases 3 a 5)
Una vez que el fundador aprueba los colores y fuentes en `previews/preview_gallery.html` y `chroma_preview.html`, volver a ejecutar `run_workflow` con `"stop_after_phase": "phase_5_critic"`.
