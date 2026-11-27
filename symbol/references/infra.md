# Symbol: Infraestructura Vectorial, Seguridad SVG y Paridad (`v2.0`)

- **Motor CLI:** `/var/www/zerops-astrobranding/scripts/symbol_engine.py` (`symbol-engine`).
- **Cero scripts o rásteres embebidos:** Rechaza `<image>` y `<script>` dentro de SVG maestros; toda geometría se emite como `<path>` limpio sobre `viewBox="0 0 100 100"`.
- **Integración con `kinetic` y `astro-web`:** `kinetic-engine` consume directamente `symbol_manifest.json -> parts[]` (`#symbol-part-1..N`) y `svg_mono` para generar CSS `60fps` sin inventar selectores inexistentes.
- **Validación:** `python3 -B -m py_compile` + `symbol-engine --test` + `assets/schemas/symbol_manifest.schema.json`.
