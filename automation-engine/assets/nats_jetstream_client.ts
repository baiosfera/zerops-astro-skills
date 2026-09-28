import { connect, JetStreamClient, JetStreamManager, headers, StorageType, RetentionPolicy, AckPolicy } from "nats";
import { EventEnvelopeSchema } from "./automation_zod_schemas";
import { z } from "zod";

export class NatsJetStreamClient {
  private js!: JetStreamClient;
  private jsm!: JetStreamManager;

  async initialize(serverUrl = process.env.NATS_URL || "nats://127.0.0.1:4222") {
    const nc = await connect({ servers: serverUrl, name: "automation-engine" });
    this.js = nc.jetstream();
    this.jsm = await nc.jetstreamManager();
  }

  async createStream(name: string, subjects: string[]) {
    await this.jsm.streams.add({
      name,
      subjects,
      storage: StorageType.File,
      retention: RetentionPolicy.Limits,
      max_bytes: 1024 * 1024 * 1024,
      duplicate_window: 120 * 1_000_000_000
    });
  }

  async publish(subject: string, event: z.infer<typeof EventEnvelopeSchema>) {
    const validated = EventEnvelopeSchema.parse(event);
    const h = headers();
    h.set("Nats-Msg-Id", validated.id);

    return await this.js.publish(subject, Buffer.from(JSON.stringify(validated)), { headers: h });
  }

  async consumePull(streamName: string, consumerName: string, subject: string, handler: (event: any) => Promise<void>) {
    const consumer = await this.js.consumers.get(streamName, consumerName).catch(async () => {
      return await this.jsm.consumers.add(streamName, {
        durable_name: consumerName,
        filter_subject: subject,
        ack_policy: AckPolicy.Explicit,
        max_deliver: 5
      }).then(() => this.js.consumers.get(streamName, consumerName));
    });

    return await consumer.consume({
      callback: async (msg) => {
        try {
          const event = JSON.parse(msg.data.toString());
          await handler(event);
          msg.ack();
        } catch (err) {
          msg.nak();
        }
      }
    });
  }
}
