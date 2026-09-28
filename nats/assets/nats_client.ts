import { connect, JSONCodec, NatsConnection, headers, StorageType, RetentionPolicy, AckPolicy } from "nats";

export class GentleNatsClient {
  private nc!: NatsConnection;
  private jc = JSONCodec();

  async connect(serverUrl = process.env.NATS_URL || "nats://127.0.0.1:4222") {
    this.nc = await connect({
      servers: serverUrl,
      name: "gentle-ts-service",
      reconnect: true,
      maxReconnectAttempts: -1
    });
  }

  async requestRpc<TReq, TRes>(subject: string, payload: TReq, timeoutMs = 2000): Promise<TRes> {
    const msg = await this.nc.request(subject, this.jc.encode(payload), { timeout: timeoutMs });
    return this.jc.decode(msg.data) as TRes;
  }

  registerWorker<TReq, TRes>(subject: string, queueGroup: string, handler: (req: TReq) => Promise<TRes>) {
    const sub = this.nc.subscribe(subject, { queue: queueGroup });
    (async () => {
      for await (const msg of sub) {
        try {
          const req = this.jc.decode(msg.data) as TReq;
          const res = await handler(req);
          if (msg.reply) {
            msg.respond(this.jc.encode(res));
          }
        } catch (err: any) {
          if (msg.reply) {
            msg.respond(this.jc.encode({ error: err.message }));
          }
        }
      }
    })();
  }

  async close() {
    await this.nc.drain();
  }
}
