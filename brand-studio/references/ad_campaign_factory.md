# `ad-campaign-factory` & `ad-library` — Operación Ads-First de Bajo Consumo

## 1. Principio Ads-First + Token Frugality
1. **Nunca dumpear Meta Ad Library crudo al contexto del chat:** un scrape crudo pesa ~65 KB con selectores de 200 países.
2. **Siempre usar `ad-library` CLI primero (`0` tokens LLM):**
   - `ad-library fetch --query "<tema>" --country CO --min-days 14 --limit 15 --out <ws_dir>/strategy/ad_library_brief.json`
   - Si no hay key HTTP directa para Firecrawl/Meta API, ejecutar `firecrawl_scrape` MCP una sola vez sobre la URL de Meta Ad Library, guardar en archivo temporal y correr `ad-library parse --input-file <tmp.md> --out <ws_dir>/strategy/ad_library_brief.json`.
   - Opcional: `--synth-via bifrost` resume hooks y objeciones sin gastar tokens de frontera.
3. **Lectura de URLs destino con `meta-research`:** sobre las 2–3 URLs ganadoras del brief compacto (`< 3 KB`), llamar `jina:read_url(url=..., question="oferta principal, precio, prueba social y objeción que responde")`.

## 2. Invocación de `ad_campaign_factory.wf`
```python
run_workflow(
    ScriptPath="/var/www/zerops-astrobranding/workflows/ad-campaign-factory/ad_campaign_factory.wf",
    Description="Generar ángulos Ads-First y landings dinámicas /[vertical]/lp/[slug]",
    Args={
        "project": "MiProyecto",
        "vertical": "mi-linea",
        "workspace_dir": "/mnt/localstorage/MiProyecto/dev/workspaces/mi-linea",
        "search_queries": ["marca personal", "consultoria"],
        "country": "CO",
        "min_days_active": 14,
        "angles_count": 3,
        "offer_ring": "core",
        "lead_magnet_mechanism": "auto",  # puede elegir "none" si VSL/evaluación directa convierte mejor
        "auto_approve_angles": False       # pausa tras Fase 2 para visto bueno humano
    }
)
```

## 3. Contrato de Salida (`campaigns/<slug>.json`)
Cada campaña validada con `apotelos validate-campaign` y `anti-slop-linter` materializa:
- `route_path`: `/[vertical]/lp/[slug]`
- `robots`: `"noindex, follow"` por defecto (`"index, follow"` únicamente si declara `seo_cluster_id`)
- `ad_creative`: hook 3s, primary text, headline, CTA y `UtmContract` (`allow_on_internal_links=false`)
- `hero_h1` + `message_match_keywords`: match literal anuncio $\to$ landing
- `lead_magnet`: `InteractiveProofSpec` opcional/polimórfico (`mechanism="none"` oculta la calculadora por completo)
- `wa_email_campaign_tag`: `"camp:<vertical>:<slug>"` para seguimiento aislado sin colisiones.
