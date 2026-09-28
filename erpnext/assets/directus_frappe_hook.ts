import { defineHook } from '@directus/extensions-sdk';
import { Queue } from 'bullmq';
import IORedis from 'ioredis';

const redisConnection = new IORedis(process.env.REDIS_URL || 'redis://cache:6379', {
  maxRetriesPerRequest: null,
  enableReadyCheck: false
});

const frappeQueue = new Queue('sync-to-frappe', {
  connection: redisConnection,
  defaultJobOptions: {
    attempts: 5,
    backoff: {
      type: 'exponential',
      delay: 2000
    },
    removeOnComplete: 100,
    removeOnFail: 500
  }
});

export default defineHook(({ action }) => {
  // Disparo tras creación de pedido en Directus
  action('orders.items.create', async (meta) => {
    const { key, payload } = meta;

    // Escudo Anti-Bucle: Omitir si la mutación proviene de Frappe
    if (payload._sync_source === 'frappe') {
      return;
    }

    try {
      await frappeQueue.add(
        'sync-order-to-frappe',
        {
          directusOrderId: key,
          customerEmail: payload.customer_email,
          customerName: payload.customer_name,
          items: payload.items,
          totalAmount: payload.total,
          createdAt: new Date().toISOString()
        },
        {
          jobId: `order-sync-${key}` // Clave de idempotencia
        }
      );

      console.log(`[Directus -> Frappe Hook] Pedido encolado exitosamente: ${key}`);
    } catch (err: any) {
      console.error(`[Directus -> Frappe Hook] Error encolando pedido ${key}:`, err.message);
    }
  });
});
