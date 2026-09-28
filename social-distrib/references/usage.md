# Social Media Distribution: Usage & Development Guide (v1.0)

> **SSoT Reference Document:** `.agents/skills/social-distrib/references/usage.md`  
> **Ámbito:** Integración con Instagram Graph API, TikTok Content Posting API, LinkedIn REST API, X API v2, matriz horaria GMT-5 y colas BullMQ.

---

## 1. Instagram Graph API (v26.0+): Ciclo de Publicación de 3 Pasos

```typescript
export async function publishInstagramReel(params: {
  igUserId: string;
  accessToken: string;
  videoUrl: string;
  caption: string;
  coverUrl?: string;
}): Promise<string> {
  // Paso 1: Crear Contenedor de Medios
  const containerRes = await fetch(`https://graph.instagram.com/v26.0/${params.igUserId}/media`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${params.accessToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      media_type: "REELS",
      video_url: params.videoUrl,
      caption: params.caption,
      cover_url: params.coverUrl,
      share_to_feed: true
    })
  });

  const { id: containerId } = await containerRes.json();

  // Paso 2: Polling de Estado (Obligatorio esperar FINISHED)
  let status = "IN_PROGRESS";
  let attempts = 0;
  while (status === "IN_PROGRESS" && attempts < 20) {
    await new Promise((resolve) => setTimeout(resolve, 10000));
    const statusRes = await fetch(`https://graph.instagram.com/v26.0/${containerId}?fields=status_code`, {
      headers: { "Authorization": `Bearer ${params.accessToken}` }
    });
    const statusJson = await statusRes.json();
    status = statusJson.status_code;
    attempts++;
  }

  if (status !== "FINISHED") {
    throw new Error(`IG Container ${containerId} finalizó con error o timeout: ${status}`);
  }

  // Paso 3: Publicar Contenedor
  const publishRes = await fetch(`https://graph.instagram.com/v26.0/${params.igUserId}/media_publish`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${params.accessToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ creation_id: containerId })
  });

  const { id: publishedMediaId } = await publishRes.json();
  return publishedMediaId;
}
```

---

## 2. LinkedIn REST API (v202604): Publicación de Carruseles en PDF

```typescript
export async function publishLinkedInDocumentCarousel(params: {
  authorUrn: string; // ej. "urn:li:organization:123456"
  accessToken: string;
  title: string;
  commentary: string;
  pdfBuffer: Buffer;
}): Promise<string> {
  // 1. Inicializar Registro de Documento
  const initRes = await fetch("https://api.linkedin.com/rest/documents?action=initializeUpload", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${params.accessToken}`,
      "Linkedin-Version": "202604",
      "X-Restli-Protocol-Version": "2.0.0",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      initializeUploadRequest: { owner: params.authorUrn }
    })
  });

  const initData = await initRes.json();
  const { uploadUrl, document: documentUrn } = initData.value;

  // 2. Subida Binaria del PDF
  await fetch(uploadUrl, {
    method: "PUT",
    headers: { "Content-Type": "application/pdf" },
    body: params.pdfBuffer
  });

  // 3. Crear el Post en LinkedIn
  const postRes = await fetch("https://api.linkedin.com/rest/posts", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${params.accessToken}`,
      "Linkedin-Version": "202604",
      "X-Restli-Protocol-Version": "2.0.0",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      author: params.authorUrn,
      commentary: params.commentary,
      visibility: "PUBLIC",
      distribution: { feedDistribution: "MAIN_FEED" },
      content: {
        document: {
          id: documentUrn,
          title: params.title
        }
      },
      lifecycleState: "PUBLISHED"
    })
  });

  return postRes.headers.get("x-restli-id") || "published";
}
```

---

## 3. Matriz de Horarios Pico en Colombia y Latinoamérica (GMT-5 / COT)

| Plataforma | Audiencia Objetivo | Días Recomendados | Ventana Óptima (GMT-5 / COT) | Formato de Máximo Rendimiento |
|---|---|---|---|---|
| **LinkedIn** | B2B & Ejecutivos | Martes a Jueves | **07:30 – 09:00 COT**<br/>**11:45 – 13:30 COT** | Carruseles PDF de 7 a 10 láminas |
| **X (Twitter)** | B2B, Tech & Noticias | Lunes a Viernes | **08:30 – 10:30 COT**<br/>**12:30 – 14:00 COT** | Hilos de 4 a 6 tweets con hook visual |
| **Instagram** | B2C & Comercio | Miércoles a Domingo | **12:00 – 14:00 COT**<br/>**19:00 – 21:30 COT** | Reels 9:16 (<60s) y Carruseles 4:5 |
| **TikTok** | B2C & Consumo Masivo | Jueves a Domingo | **13:00 – 15:00 COT**<br/>**19:30 – 22:30 COT** | Videos verticales de 15 a 35 segundos |

---

## 4. Programación y Manejo de Colas con BullMQ en Valkey 7.2

```typescript
import { Queue } from "bullmq";
import Redis from "ioredis";

const connection = new Redis(process.env.VALKEY_CONNECTION_STRING || "redis://valkey:6379", {
  maxRetriesPerRequest: null,
  enableReadyCheck: false
});

export const instagramQueue = new Queue("social-instagram", {
  connection,
  defaultJobOptions: {
    attempts: 5,
    backoff: { type: "exponential", delay: 10000 },
    removeOnComplete: 1000
  }
});

export async function scheduleDelayedPost(params: {
  platform: "INSTAGRAM" | "LINKEDIN" | "TIKTOK" | "X";
  scheduledTimeIso: string;
  payload: Record<string, any>;
}) {
  const targetTime = new Date(params.scheduledTimeIso).getTime();
  const delay = Math.max(0, targetTime - Date.now());

  return await instagramQueue.add(`publish-${params.platform.toLowerCase()}`, params.payload, {
    delay
  });
}
```
