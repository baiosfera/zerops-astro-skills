# Kinetic: Infraestructura, Tokens W3C DTCG 2025.10 y Astro Lifecycle (`v2.0`)

- **Motor CLI:** `/var/www/zerops-astrobranding/scripts/kinetic_engine.py` (`kinetic-engine`).
- **Tokens DTCG (`dtcg_tokens`):** emite `motion.duration` (`fast: 180ms`, `normal: 520ms`, `focal: 650ms`) y `motion.easing.editorial_out` (`[0.16, 1, 0.3, 1]`).
- **Cero dependencia obligatoria de audio:** el micro-audio Web Audio API queda reservado únicamente cuando un proyecto lo solicite tras gesto explícito de usuario (`AudioContext` + `ADSR`), nunca como requisito bloqueante del manifiesto.
- **Validación:** `python3 -B -m py_compile` + `kinetic-engine --test` + `assets/schemas/kinetic_manifest.schema.json`.
