# Anti-Patrones y Lecciones Aprendidas en Producción Audiovisual

Este documento registra los errores críticos detectados durante la sesión de implementación y las soluciones arquitectónicas definitivas para evitar su repetición en futuros proyectos ZCP.

---

### Anti-Patrón 1: Captura de CSS en Tiempo Real (Slide Congelado)

- **Falla:** Intentar grabar animaciones CSS `@keyframes` con Puppeteer o Chromium sin reloj virtual determinista.
- **Consecuencia:** En un contenedor CPU sin aceleración gráfica dedicada, el navegador corre la animación en los primeros 1.2 segundos y luego se detiene en su estado terminal (`opacity: 1`, `transform: none`). El resultado fue un video de 8 segundos donde 7 segundos eran una imagen completamente estática.
- **Regla Invariable:** Todo renderizado de código a video debe congelar e incrementar manualmente el reloj virtual (`virtual time`) fotograma por fotograma, o utilizar composición cinemática directa con FFmpeg.

---

### Anti-Patrón 2: Botones Falsos Dibujados en Píxeles

- **Falla:** Incluir un botón de "Agendar Cita" o "Comprar Ahora" como elemento gráfico dentro de los fotogramas del video.
- **Consecuencia:** El usuario ve un botón en pantalla pero al hacer clic solo pausa o despausa el reproductor de video. La tasa de conversión se desploma y genera frustración inmediata.
- **Regla Invariable:** El video es exclusivamente un activo visual y de atmósfera. Todos los llamados a la acción (CTAs) deben residir en el DOM nativo de la página web (`<button>` o `<a>` en Astro/React/Solid) con eventos reales y accesibilidad completa.

---

### Anti-Patrón 3: B-Roll No Alineado al Dominio de Marca

- **Falla:** Descargar clips de video bajo etiquetas genéricas (`sportswear`) sin validar su contenido contra el `brandbook.json` de la marca.
- **Consecuencia:** Se incrustaron tomas de boxeo masculino y fútbol en una marca de estética femenina, maquillaje social y enterizos seamless de lujo.
- **Regla Invariable:** Los activos de video deben contrastarse explícitamente contra el manifiesto de marca, sus arquetipos y el catálogo de productos antes de ser incluidos en la composición final.

---

### Anti-Patrón 4: Recorte de Tipografía en Dispositivos Móviles

- **Falla:** Diseñar composiciones verticales (9:16) con textos pegados a los márgenes superior e inferior sin contemplar el comportamiento de `object-cover` en pantallas móviles.
- **Consecuencia:** Los títulos y badges de propuesta de valor quedaban cortados en teléfonos compactos.
- **Regla Invariable:** Toda composición vertical debe confinar los textos dentro de una **Safe Area central del 65%**, y se deben generar siempre pares de video: **Vertical (9:16 con Safe Area)** para mobile/reels y **Panorámica (16:9)** para desktop.

---

### Anti-Patrón 5: Contenedores Fijos Ociosos (Desperdicio de Recursos)

- **Falla:** Mantener un servicio de renderizado pesado activo las 24 horas del día consumiendo memoria y presupuesto cuando solo se producen videos de forma esporádica.
- **Regla Invariable:** Adoptar el modelo **Lego Efímero (Hito 8)**: se aprovisiona bajo demanda, procesa el lote de videos, exporta los archivos finales a almacenamiento persistente y se destruye inmediatamente para mantener **costo cero**.

---

### Anti-Patrón 6: Superposición de SVG Estático vía librsvg (Falso Motion Graphics)

- **Falla:** Usar FFmpeg con `librsvg` para quemar un archivo SVG plano a PNG y estamparlo como un overlay estático (`overlay=0:0`) sobre los clips de fondo.
- **Consecuencia:** `librsvg` es un parser elemental en C que no ejecuta JavaScript, no corre animaciones CSS, carece de soporte completo para el layout OpenType avanzado (swashes `ss01`, ligaduras contextuales de fuentes como Kalieb Luxury) y congela el texto inmóvil durante todo el video.
- **Regla Invariable:** La capa de motion graphics debe renderizarse mediante un motor de navegador completo (Chromium headless vía Playwright) que soporte tipografía OpenType nativa (`font-feature-settings: 'ss01' 1`) y animaciones procedurales deterministas (GSAP) controladas fotograma por fotograma con `timeline.seek(t)`, transmitidas en streaming directo a FFmpeg por memoria `stdin` (`image2pipe`).
