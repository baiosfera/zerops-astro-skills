# Video Worker — Developer & Operational Usage Manual (v2.0)

El motor de renderizado audiovisual opera de forma desacoplada y asíncrona dentro de la red privada de Zerops bajo Fractal CoHaLo v8.4.

---

## 1. Topología y Componentes

```
[ Cliente Web / API / ZCP ]
             │
             ▼ Publica Job
[ NATS JetStream / Valkey BullMQ ]
             │
             ▼ Consume Job (1 por vCPU)
[ videoworker (Node.js 22 Ubuntu) ]
   ├── Playwright / Timesnap (Virtual Clock Determinism)
   └── FFmpeg Memory Pipe (libx264, aac, yuv420p)
             │
             ▼ Guarda MP4
[ S3 Object Storage / Web Public Assets ]
```

---

## 2. Reloj Virtual Determinista (Anti-Freezing)

Renderizar animación web en entornos virtuales sin GPU dedicada requiere desacoplar el tiempo de render del reloj de pared:

- **Mecanismo:** Interceptar `window.requestAnimationFrame`, `setTimeout` y `performance.now()`.
- **Funcionamiento:** Avanzar el reloj en incrementos exactos de `1000 / fps` milisegundos (ej. 33.33ms para 30fps). El siguiente fotograma solo se computa cuando el actual ha sido extraído al buffer de memoria.
- **Resultado:** Cero caídas de fotogramas (*frame drops*), cero aceleraciones espasmódicas y cero congelamiento de animaciones CSS o GSAP.

---

## 3. Streaming Directo por Pipes a FFmpeg

Para evitar saturar el subsistema de I/O y el almacenamiento local con miles de archivos PNG temporales:

```typescript
import { spawn } from 'child_process';

const ffmpeg = spawn('ffmpeg', [
  '-v', 'error',
  '-y',
  '-f', 'image2pipe',
  '-vcodec', 'png',
  '-r', String(fps),
  '-i', '-', // Entrada estándar en memoria
  '-c:v', 'libx264',
  '-preset', 'medium',
  '-crf', '20',
  '-pix_fmt', 'yuv420p',
  '-movflags', '+faststart',
  outputFile
]);

// Stream cuadro a cuadro directo a stdin
for (let frame = 0; frame < totalFrames; frame++) {
  await advanceVirtualClock(frame);
  const buffer = await page.screenshot({ type: 'png' });
  ffmpeg.stdin.write(buffer);
}
ffmpeg.stdin.end();
```

---

## 4. Consumo Asíncrono y Cuotas de Recursos

- **Concurrencia:** Máximo 1 render activo por vCPU (`MAX_CONCURRENT_RENDERS=1`).
- **RAM Mínima:** 512 MB asignados al servicio con escalado vertical en Zerops.
- **Backpressure:** Si la cola acumula múltiples solicitudes, NATS JetStream o BullMQ retienen los mensajes en estado pendiente sin colapsar el contenedor.

---

## 5. Anti-Patrones Críticos & Lecciones Aprendidas

1. **Captura de CSS en Tiempo Real (Slide Congelado)**: Capturar `@keyframes` sin reloj determinista en contenedores CPU congela el video tras el primer segundo. Siempre congelar e incrementar manualmente el reloj virtual fotograma por fotograma (`timeline.seek(t)`).
2. **Botones Falsos Dibujados en Píxeles**: Dibujar botones de compra o agendamiento en el video desploma la conversión porque el usuario intenta hacer clic y solo pausa el reproductor. Los CTAs deben residir en el DOM nativo (`<button>` o `<a>`).
3. **B-Roll Desalineado de Marca**: Contrastar siempre los clips contra `brandbook.json` y el catálogo de productos antes de componer.
4. **Recorte en Móviles (Falta de Safe Area)**: Confinar textos y badges dentro del **65% central** del lienzo vertical (9:16). Generar siempre pares: 9:16 (mobile) y 16:9 (desktop).
5. **Superposición de SVG Estático vía librsvg**: `librsvg` no ejecuta JavaScript ni fuentes OpenType con swashes (`ss01`). Usar Chromium headless vía Playwright para renderizar tipografía avanzada y motion graphics en tiempo real.
