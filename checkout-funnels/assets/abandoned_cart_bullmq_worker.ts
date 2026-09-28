import { Worker, Job } from "bullmq";

interface CartRecoveryData {
  cartId: string;
  customerData: { phone: string; name: string };
  touch: number;
}

export const recoveryWorker = new Worker<CartRecoveryData>(
  "abandoned-checkout-recovery",
  async (job: Job<CartRecoveryData>) => {
    const { cartId, customerData, touch } = job.data;
    
    // Verificar en Directus si el carrito ya fue pagado
    const isPaid = false; // Consulta a Directus 11+
    if (isPaid) {
      return { skipped: true, reason: "Already paid" };
    }

    // Despacho de mensaje según el toque
    if (touch === 1) {
      // T+15m: Diagnóstico técnico
      console.log(`[WhatsApp T+15m] Enviando a ${customerData.phone}: Hola ${customerData.name}, ¿tuviste problemas con el pago?`);
    } else if (touch === 2) {
      // T+4h: Garantía y Envío Gratis
      console.log(`[WhatsApp T+4h] Enviando a ${customerData.phone}: Hola ${customerData.name}, completa hoy con Envío Gratis`);
    } else if (touch === 3) {
      // T+24h: Escasez real
      console.log(`[WhatsApp T+24h] Enviando a ${customerData.phone}: Último aviso ${customerData.name}, liberaremos el inventario`);
    }

    return { success: true, cartId, touch };
  },
  {
    connection: {
      host: process.env.VALKEY_HOST || "valkey",
      port: parseInt(process.env.VALKEY_PORT || "6379")
    }
  }
);
