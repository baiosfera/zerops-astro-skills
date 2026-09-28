---
name: kinetic
description: "Trigger: kinetic, animacion gsap, microinteracciones, motion design, web audio api, sfx de marca, 60fps, 3 opciones animacion. Disena 3 opciones de animacion tipografica y vectorial a 60fps con GSAP y SFX procedurales."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.1"
---

# Kinetic — Motion Design a 60fps, 3 Opciones de Animación & Micro-Audio ADSR Dual-RAG

## Activation Contract
Activar cuando se requiera diseñar el sistema de movimiento a 60fps, formulando **3 Opciones de Animación Diferenciadas** aplicadas directamente a los IDs del SVG escogido en Fase 2, y el banco de micro-audio procedural ADSR.

## Hard Rules (Directivas Obligatorias)
- **1. Generación de 3 Opciones de Animación:** Formular obligatoriamente 3 presets de animación sobre el SVG:
  - **Opción A (Precesión Orbital & Respiración Armónica):** Movimiento continuo suave, rotación orbital a 24s y pulso a 6s.
  - **Opción B (Velocidad Cinética & Trazado Elástico):** Aceleración atlética `cubic-bezier(0.16, 1, 0.3, 1)`, destellos enérgicos a 4s.
  - **Opción C (Revelado Místico & Brillo Áureo):** Variación sutil de opacidad, micro-pulsos y trazo `stroke-dashoffset`.
- **2. Destino Específico a los IDs del SVG de Fase 2:** Las reglas `@keyframes` y tweens GSAP deben apuntar a `#symbol-core`, `#symbol-orbit-1`, `#symbol-orbit-2`, `#symbol-geometry-star`, `#symbol-monogram`.
- **3. Tokens de Motion W3C DTCG:** Definir duraciones (`fast`, `normal`, `slow`) y curvas cúbicas estandarizadas.
- **4. Banco de Micro-Audio Procedural ADSR (Web Audio API):** Presets de síntesis matemática nativa para `hover`, `click`, `modal_open`, `success_confirm` sin archivos MP3 externos.
- **5. Contrato de Selección:** Incluir `selected_animation_id` (ej: `"anim-orbit-precession"`) para transferir a Fase 5.
- **6. Salida Determinista SSoT:** Escribir en `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/kinetic_manifest.json` y validar contra `kinetic_manifest.schema.json`.

## Decision Gates

| Condición | Acción |
|---|---|
| Rendimiento móvil / batería baja | Utilizar exclusivamente transformaciones CSS `transform` y `opacity` compuestas en GPU |
| GSAP en WebApp | Envolver la ejecución dentro de `gsap.context()` para evitar fugas de memoria |

## Execution Steps
1. Leer `symbol_manifest.json` y `chroma_manifest.json`.
2. Formular las 3 Opciones de Animación con reglas `@keyframes` y parámetros GSAP.
3. Configurar los tokens de duración y aceleración DTCG.
4. Diseñar los presets de síntesis ADSR con frecuencias armónicas acordes al arquetipo.
5. Emitir `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/kinetic_manifest.json` validado con `kinetic_manifest.schema.json`.

## Output Contract
- `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/kinetic_manifest.json`

## References
- `references/usage.md` — Guía de 3 presets de animación, GSAP context y síntesis procedural Web Audio API.
- `assets/schemas/kinetic_manifest.schema.json` — Esquema JSON Draft 2020-12.
- `assets/templates/kinetic_manifest_template.json` — Plantilla del manifiesto cinético.
