import { Worker, Job } from "bullmq";

export interface TrackingJobData {
  orderId: string;
  orderNumber: string;
  customerName: string;
  phone: string;
  carrier: string;
  trackingNumber: string;
  trackingUrl: string;
  eventType: "label_generated" | "out_for_delivery" | "delivery_failed" | "delivered";
  codAmount?: number;
  noveltyReason?: string;
}

export const trackingWhatsAppWorker = new Worker<TrackingJobData>(
  "shipping-tracking-notifications",
  async (job: Job<TrackingJobData>) => {
    const { phone, orderNumber, customerName, carrier, trackingNumber, trackingUrl, eventType, codAmount, noveltyReason } = job.data;
    
    let text = "";
    if (eventType === "label_generated") {
      text = `¡Hola ${customerName}! Tu pedido #${orderNumber} ha sido preparado y despachado con *${carrier}*. Tu número de guía es *${trackingNumber}*. Síguelo aquí: ${trackingUrl}`;
    } else if (eventType === "out_for_delivery") {
      text = `🚚 ¡Tu pedido está en reparto! El mensajero de ${carrier} te visitará hoy.${codAmount ? ` Recuerda tener listos *$${codAmount.toLocaleString("es-CO")} COP* en efectivo.` : ""}`;
    } else if (eventType === "delivery_failed") {
      text = `⚠️ Hola ${customerName}, tuvimos una novedad entregando tu pedido #${orderNumber}: "${noveltyReason}". Por favor responde a este mensaje para confirmar o corregir tu dirección.`;
    } else if (eventType === "delivered") {
      text = `🎉 ¡Tu pedido #${orderNumber} ha sido entregado exitosamente! Muchas gracias por tu compra.`;
    }

    if (process.env.EVOLUTION_API_URL && process.env.EVOLUTION_API_KEY) {
      await fetch(`${process.env.EVOLUTION_API_URL}/message/sendText/${process.env.EVOLUTION_INSTANCE || "orders-bot"}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "apikey": process.env.EVOLUTION_API_KEY
        },
        body: JSON.stringify({
          number: `57${phone}`,
          text
        })
      });
    }

    return { sent: true, orderNumber, eventType };
  },
  {
    connection: {
      host: process.env.VALKEY_HOST || "valkey",
      port: parseInt(process.env.VALKEY_PORT || "6379")
    }
  }
);
