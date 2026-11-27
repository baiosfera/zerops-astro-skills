---
name: kinetic
description: "Trigger: kinetic, animacion gsap, microinteracciones, motion design, web audio api, sfx de marca, 60fps, 3 opciones animacion. Disena 3 opciones de animacion tipografica y vectorial a 60fps con GSAP y SFX procedurales."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.3"
---

# Kinetic — Motion Design 60fps, Lazy GSAP/Lenis Astro 5 & Micro-Audio ADSR (v1.3)

## Activation Contract
Activar para diseñar e implementar sistemas de movimiento a `60fps` sobre Astro 5 SSR + SVG/DOM semántico, formulando **3 Opciones de Animación Diferenciadas**, patrón de carga perezosa **GSAP + ScrollTrigger + Lenis** compatible con View Transitions y banco opcional de micro-audio procedural ADSR. Ingiera desde `DESIGN.md`, `astrobranding_[MARCA].md`, `kinetic_manifest.json` o especificaciones directas.

## Hard Rules (Directivas Obligatorias)
1. **Un Momento Coreografiado & Rendimiento GPU (`RAIL < 16ms`):** Diseñar **1 momento protagonista por superficie** en lugar de `fade-up` repetitivo en cada tarjeta. Animar exclusivamente propiedades compuestas (`transform`, `opacity`, `clip-path`), usando curvas exponenciales (`cubic-bezier(0.16, 1, 0.3, 1)`), prohibiendo `bounce`/`elastic` y cambios de `width`/`margin` que provoquen *Layout Thrashing*.
2. **Patrón Astro 5 Lazy Load + Lenis + View Transitions (2026):** Diferir la carga del módulo GSAP dentro de `requestIdleCallback` (fallback `150ms`) para proteger `LCP < 1.0s`; cuando se active `Lenis`, sincronizar `lenis.on('scroll', ScrollTrigger.update)` con `gsap.ticker` y `lagSmoothing(0)`. Encapsular tweens en `gsap.context()`, revertir en `astro:before-swap`, reinicializar en `astro:page-load` y degradar limpiamente bajo `prefers-reduced-motion: reduce`.
3. **3 Presets Diferenciados (60fps):** **Opción A** (*Precesión Orbital & Respiración Armónica*), **Opción B** (*Velocidad Cinética & Trazado Elástico*), **Opción C** (*Revelado Editorial & Brillo Contenido*) orientados a IDs vectoriales (`#symbol-core`, `#symbol-orbit-1/2`, `#symbol-geometry-star`, `#symbol-monogram`) o secciones marcadas.
4. **Tokens W3C DTCG & Micro-Audio Procedural (Web Audio API):** Emitir tokens (`fast`, `normal`, `slow`, easing) y presets ADSR sin MP3 externos cuando aplique SFX discreto tras gesto de usuario.
5. **Salida SSoT:** Persistir `kinetic_manifest.json` validado por esquema cuando opere el pipeline de identidad.

## References
- [`references/usage.md`](file:///var/www/.agents/skills/kinetic/references/usage.md) · [`references/infra.md`](file:///var/www/.agents/skills/kinetic/references/infra.md)
- [`assets/schemas/kinetic_manifest.schema.json`](file:///var/www/zerops-astro-skills/kinetic/assets/schemas/kinetic_manifest.schema.json)
