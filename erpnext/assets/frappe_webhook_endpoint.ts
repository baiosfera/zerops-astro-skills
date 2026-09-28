import { defineEndpoint } from '@directus/extensions-sdk';
import crypto from 'crypto';

export default defineEndpoint((router, context) => {
  const { services, getSchema } = context;
  const { ItemsService } = services;

  router.post('/webhook', async (req: any, res: any) => {
    const signature = req.headers['x-frappe-webhook-signature'];
    const secret = process.env.FRAPPE_WEBHOOK_SECRET;

    if (!secret) {
      console.error('[Frappe Webhook] FRAPPE_WEBHOOK_SECRET no configurado en entorno.');
      return res.status(500).json({ error: 'Webhook secret missing on server' });
    }

    if (!signature) {
      return res.status(401).json({ error: 'Missing X-Frappe-Webhook-Signature header' });
    }

    try {
      const rawBody = typeof req.body === 'string' ? req.body : JSON.stringify(req.body);
      const expectedSignature = crypto
        .createHmac('sha256', secret)
        .update(rawBody)
        .digest('base64');

      const signatureBuffer = Buffer.from(signature as string, 'base64');
      const expectedBuffer = Buffer.from(expectedSignature, 'base64');

      if (
        signatureBuffer.length !== expectedBuffer.length ||
        !crypto.timingSafeEqual(signatureBuffer, expectedBuffer)
      ) {
        console.warn('[Frappe Webhook] Firma HMAC inválida recibida.');
        return res.status(401).json({ error: 'Invalid HMAC signature' });
      }

      const payload = req.body;
      const schema = await getSchema();

      if (payload.event === 'stock_update' && payload.item_code) {
        const productsService = new ItemsService('products', {
          schema,
          accountability: null
        });

        const existing = await productsService.readByQuery({
          filter: { sku: { _eq: payload.item_code } },
          limit: 1
        });

        if (existing && existing.length > 0) {
          const productId = existing[0].id;
          await productsService.updateOne(productId, {
            stock_quantity: payload.qty_after_transaction,
            _sync_source: 'frappe',
            last_stock_sync: new Date().toISOString()
          });

          console.log(`[Frappe Webhook] Stock actualizado para SKU ${payload.item_code}: ${payload.qty_after_transaction}`);
        }
      }

      return res.status(200).json({ status: 'success', received: true });
    } catch (err: any) {
      console.error('[Frappe Webhook] Error procesando webhook:', err.message);
      return res.status(500).json({ error: 'Internal processing error', message: err.message });
    }
  });
});
