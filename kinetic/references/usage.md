# Kinetic: Manual de Motion Design a 60fps, 3 Presets de Animación y Web Audio ADSR

Este documento detalla la arquitectura de animación de alto rendimiento y el motor de síntesis de audio procedural para la suite de branding.

---

## 1. Arquitectura de 3 Opciones de Animación sobre el SVG Escogido

Para dar al usuario control artístico total sobre el comportamiento dinámico de su marca, `kinetic` formula 3 opciones:

### Opción A: Precesión Orbital & Respiración Armónica (Luxury / Continuo)
- **Concepto:** Rotación orbital continua asincrónica entre elipses externas e internas con pulso sutil de compresión.
- **Targets:** `#symbol-orbit-1` (rotación 24s antihoraria), `#symbol-orbit-2` (rotación 18s horaria), `#symbol-core` (respiración scale 1.025 a 6s).

### Opción B: Velocidad Cinética & Trazado Elástico (High-Performance / Activo)
- **Concepto:** Entrada con aceleración deportiva `power4.out`, destello de trazo y rotación rápida enérgica.
- **Targets:** `#symbol-orbit-1` (spin a 8s), `#symbol-geometry-star` (shimmer rápido a 2.5s).

### Opción C: Revelado Místico & Brillo Áureo (Minimal / Ethereal)
- **Concepto:** Difuminado lumínico sutil, trazo `stroke-dashoffset` progresivo y micro-elevación.
- **Targets:** `#symbol-monogram` (glow pulsante), `#symbol-geometry-star` (resplandor a 4s).

---

## 2. Sintetizador Procedural Web Audio API (ADSR + BiquadFilter)

Erradica los "clicks" y "pops" iniciales mediante una envolvente completa **ADSR** (Attack, Decay, Sustain, Release) y filtrado tímbrico con `BiquadFilterNode`:

```javascript
class BrandAudioSynthesizer {
  constructor() {
    this.ctx = null;
  }

  init() {
    if (!this.ctx) {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  playMicroSound({
    type = 'sine',
    frequency = 520,
    attack = 0.015,
    decay = 0.04,
    sustainLevel = 0.2,
    release = 0.06,
    peakGain = 0.03,
    filterFreq = 3200
  } = {}) {
    this.init();
    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gainNode = this.ctx.createGain();
    const filter = this.ctx.createBiquadFilter();

    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(filterFreq, now);

    osc.type = type;
    osc.frequency.setValueAtTime(frequency, now);

    gainNode.gain.setValueAtTime(0.0001, now);
    gainNode.gain.linearRampToValueAtTime(peakGain, now + attack);
    gainNode.gain.exponentialRampToValueAtTime(Math.max(0.0001, peakGain * sustainLevel), now + attack + decay);
    gainNode.gain.exponentialRampToValueAtTime(0.0001, now + attack + decay + release);

    osc.connect(filter);
    filter.connect(gainNode);
    gainNode.connect(this.ctx.destination);

    osc.start(now);
    osc.stop(now + attack + decay + release + 0.01);
  }
}
```

---

## 3. Arquitectura Desacoplada & Ingestión Directa SSoT

La fuente primaria y canónica de verdad es `astrobranding_[MARCA].md` compilado por Oráculo en Fase 0 a partir de los Shards 08 (Dinámica Cinética & Audio) y 10 del VirtualDataLake.
- **Desacople de Cascada:** `kinetic` puede formular las 3 opciones de animación y sintetizar el micro-audio ADSR directamente a partir de las especificaciones cinéticas del SSoT, sin requerir que las fases previas (`fontgen`, `symbol`, `chroma`) hayan completado su ciclo.
- **Cascada No Bloqueante:** La cascada entre fases es opcional y no bloqueante. Si `symbol_manifest.json` y `chroma_manifest.json` existen en disco, hereda sus nodos vectoriales y paletas; de lo contrario anima directamente sobre los IDs semánticos canónicos (`#symbol-core`, `#symbol-orbit-1`, `#symbol-orbit-2`, `#symbol-geometry-star`, `#symbol-monogram`).
- **Contratos de Salida Garantizados:** Emite `kinetic_manifest.json` (3 presets 60fps sobre IDs semánticos, tokens DTCG de aceleración/duración, presets ADSR y `selected_animation_id`) y código dev CSS/GSAP listo para `brandview`.

