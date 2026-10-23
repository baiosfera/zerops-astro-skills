# Kinetic: Infraestructura de Motion, Web Audio API y Rendimiento 60fps (v2.0)

Este documento define la infraestructura de animación web a 60fps, el motor de síntesis de audio procedural y las salvaguardas de rendimiento y accesibilidad.

---

## 1. Runtime de Animación (GSAP 3.12+ & Astro SSR)

Kinetic optimiza el pipeline de ejecución en aplicaciones Astro 5 con hidratación parcial:

- **Aislamiento de Contexto:** Uso estricto de `gsap.context()` dentro de hooks de ciclo de vida (`onMounted` o eventos de Server Islands) para garantizar la limpieza automática de tweens (`ctx.revert()`) y prevenir fugas de memoria.
- **Hardware Acceleration:** Animaciones acotadas exclusivamente a propiedades transformadas por GPU (`transform: translate3d/rotate/scale` y `opacity`). Prohibido animar `width`, `height`, `top`, o `left` que provoquen recalculo de layout.
- **Presupuesto de Cuadros (Frame Budget):** Límite estricto de 16.6ms por fotograma para garantizar 60fps constantes en pantallas estándar y 120fps en displays ProMotion.

---

## 2. Motor de Síntesis Procedural (Web Audio API)

Para eliminar dependencias de archivos de audio externos (MP3/WAV) y latencias de descarga:

- **AudioContext Lifecycle:** Inicialización perezosa (lazy) en el primer gesto de usuario (`click` o `touchstart`) para cumplir las políticas de autoplay de los navegadores modernos.
- **Síntesis ADSR Matemática:**
  ```javascript
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  export function playTone(freq, type = 'sine', duration = 0.15) {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, ctx.currentTime);
    gain.gain.setValueAtTime(0.1, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + duration);
  }
  ```

---

## 3. Accesibilidad y Respeto a Preferencias del Sistema

Toda implementación generada debe respetar las directivas de reducción de movimiento del sistema operativo:

```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

## 4. Contratos de Persistencia SSoT

- **Manifiesto Cinético SSoT:** `/var/www/baiosfera/ASTROLOGÍA/DIAG/[MARCA]/kinetic_manifest.json`
- **Espejo en Runtime Zerops:** `/var/www/localstorage/[MARCA]/dev/kinetic_manifest.json`
- **Validación de Integridad:** Validado contra `assets/schemas/kinetic_manifest.schema.json`.
