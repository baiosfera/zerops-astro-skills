# Arquitectura Técnica del Motor de Video Efímero

## 1. Topología y Componentes

El motor de renderizado opera de forma desacoplada y asíncrona dentro de la red privada de Zerops:

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

## 2. Invariante de Reloj Virtual Determinista

Renderizar animación web en entornos virtuales sin GPU requiere desacoplar el tiempo de render del reloj de pared:

- **Mecanismo:** Interceptar `window.requestAnimationFrame`, `setTimeout` y `performance.now()`.
- **Funcionamiento:** El script avanza el reloj en incrementos exactos de `1000 / fps` milisegundos (ej. 33.33ms para 30fps). El siguiente fotograma solo se computa cuando el actual ha sido extraído al buffer de memoria.
- **Resultado:** Cero caídas de fotogramas (*frame drops*), cero aceleraciones espasmódicas y cero congelamiento de animaciones CSS o GSAP.

## 3. Streaming Directo por Pipes a FFmpeg

Para evitar saturar el subsistema de entrada/salida (I/O) y el almacenamiento local con miles de imágenes PNG temporales:

```javascript
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

## 4. Consumo Asíncrono y Cuotas de Recursos

- **Concurrencia:** Máximo 1 render activo por vCPU (`MAX_CONCURRENT_RENDERS=1`).
- **RAM Mínima:** 512 MB asignados al servicio con autoscaling vertical en Zerops.
- **Backpressure:** Si la cola acumula múltiples solicitudes, NATS JetStream o BullMQ retienen los mensajes en estado pendiente sin colapsar el contenedor.
