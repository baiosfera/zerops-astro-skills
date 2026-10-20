---
name: video-worker
description: "Trigger: video-worker, render video, html to video, motion graphics, video queue, bullmq video, nats video, ephemeral worker zerops, remotion, timesnap, playwright video. Sovereign Ephemeral Video Rendering Worker & Queue Engine in Zerops."
---

# Video Worker (Sovereign Ephemeral Engine)

Motor de renderizado audiovisual desacoplado, asíncrono y efímero para Zerops bajo Fractal CoHaLo v8.4. Procesa plantillas HTML/CSS/Canvas y composición cinemática FFmpeg mediante colas en Valkey 7.2 (BullMQ) o NATS 2.12 JetStream. Diseñado con arquitectura Lego desechable: se aprovisiona bajo demanda para lotes de renderizado y se elimina tras finalizar para mantener costo cero.

## Directivas Operativas Obligatorias

1. **Invariante Efímero & Costo Cero**:
   - El servicio `videoworker` (`ubuntu/nodejs@22`) se aprovisiona mediante `recipes/steps/08-video-worker.yaml`.
   - Se activa únicamente para procesar colas de renderizado.
   - Una vez exportados y verificados los archivos MP4 en almacenamiento persistente (Object Storage o assets web), el servicio se destruye con `zerops_delete` para no incurrir en costos fijos.

2. **Reloj Virtual Determinista (Anti-Freezing)**:
   - Todo renderizado de HTML a video utiliza control explícito de tiempo (`timesnap`, `requestAnimationFrame` interceptado o Remotion).
   - Prohibido capturar animaciones CSS `@keyframes` en tiempo real sin congelar el reloj virtual; las aceleraciones de hardware inexistentes en contenedores CPU producen frames congelados.

3. **Pipes de Memoria Directos a FFmpeg**:
   - Conectar los buffers de captura de Chromium directamente a `stdin` de FFmpeg en memoria (`yuv420p`).
   - Prohibido volcar secuencias de miles de archivos PNG en disco local; satura el I/O del contenedor.

4. **Safe Areas en Mobile (65% Central)**:
   - Los renders en formato vertical (9:16, 1080x1920) confinan títulos, badges y elementos de marca dentro del 65% central del lienzo para evitar cortes en viewports móviles con `object-cover`.
   - Siempre generar pares: 9:16 con Safe Area para mobile y 16:9 panorámico para desktop.

5. **Agnosticismo de Marca & Tipografía Declarativa**:
   - La inyección tipográfica soporta sets estilísticos OpenType (`ss01`-`ss05`) y glifos PUA de cualquier marca mediante archivos `.otf`/`.ttf` referenciados por variable de entorno.

6. **Desacople de Conversión**:
   - El video es exclusivamente un activo audiovisual (branding, atmósfera y B-roll).
   - Los llamados a la acción (CTAs) residen en el DOM nativo de la aplicación web, garantizando interactividad real.

## Referencias Técnicas Profundas

- [`architecture.md`](file:///var/www/.agents/skills/video-worker/references/architecture.md): Especificación de colas, pipes FFmpeg y reloj virtual.
- [`ephemeral-lifecycle.md`](file:///var/www/.agents/skills/video-worker/references/ephemeral-lifecycle.md): Protocolo de ciclo de vida efímero (crear, procesar, destruir).
- [`antipatterns.md`](file:///var/www/.agents/skills/video-worker/references/antipatterns.md): Registro exhaustivo de anti-patrones y lecciones aprendidas.
