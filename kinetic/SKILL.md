---
name: kinetic
description: "Trigger: kinetic, animacion gsap, microinteracciones, motion design, web audio api, sfx de marca, 60fps, 3 opciones animacion. Disena 3 opciones de animacion tipografica y vectorial a 60fps con GSAP y SFX procedurales."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.2"
---

# Kinetic — Motion Design a 60fps, 3 Opciones de Animación & Micro-Audio ADSR Dual-RAG

## Activation Contract
Activar para diseñar el sistema de movimiento a 60fps, formulando **3 Opciones de Animación Diferenciadas** aplicadas sobre IDs semánticos vectoriales, banco de micro-audio procedural ADSR y código dev CSS/GSAP. Opera desacoplado con ingestión directa desde `astrobranding_[MARCA].md` o en modo interactivo.

## Input Rule (Desacople SSoT)
- **Ingestión Directa Primaria:** Ingiere directamente desde `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/astrobranding_[MARCA].md` (compilado por Oráculo en Fase 0, Shards 08 y 10) sin requerir que fases previas se hayan ejecutado o bloqueen el pipeline. Si `symbol_manifest.json` o `chroma_manifest.json` existen, hereda sus nodos y paletas; de lo contrario aplica sobre los IDs semánticos canónicos.
- **Modo Standalone / Manual:** Acepta especificaciones directas del usuario o `brand_input.json`.

## Hard Rules (Directivas Obligatorias)
- **1. Generación de 3 Opciones de Animación (60fps):** Formular 3 presets de animación:
  - **Opción A (Precesión Orbital & Respiración Armónica):** Movimiento continuo suave, rotación orbital a 24s y pulso a 6s.
  - **Opción B (Velocidad Cinética & Trazado Elástico):** Aceleración atlética `cubic-bezier(0.16, 1, 0.3, 1)`, destellos enérgicos a 4s.
  - **Opción C (Revelado Místico & Brillo Áureo):** Variación sutil de opacidad, micro-pulsos y trazo `stroke-dashoffset`.
- **2. Destino Específico a IDs Semánticos:** Las reglas `@keyframes` y tweens GSAP deben apuntar a `#symbol-core`, `#symbol-orbit-1`, `#symbol-orbit-2`, `#symbol-geometry-star`, `#symbol-monogram`. Emite código dev CSS/GSAP listo para producción frontend.
- **3. Tokens de Motion W3C DTCG:** Definir duraciones (`fast`, `normal`, `slow`) y curvas cúbicas estandarizadas.
- **4. Banco de Micro-Audio Procedural ADSR (Web Audio API):** Presets de síntesis matemática nativa para `hover`, `click`, `modal_open`, `success_confirm` sin archivos MP3 externos.
- **5. Contrato de Selección:** Incluir `selected_animation_id` (ej: `"anim-orbit-precession"`).
- **6. Salida Determinista SSoT:** Escribir en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/kinetic_manifest.json` y validar contra `kinetic_manifest.schema.json`.

## Output Contract
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/kinetic_manifest.json`

## References
- `references/usage.md` — Guía de 3 presets de animación, GSAP context, desacople SSoT y síntesis procedural Web Audio API.
- `assets/schemas/kinetic_manifest.schema.json` — Esquema JSON Draft 2020-12.
- `assets/templates/kinetic_manifest_template.json` — Plantilla del manifiesto cinético.
