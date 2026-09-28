import Redis from "ioredis";
import { ConversationalSessionSchema } from "./whatsapp_zod_schemas";
import { z } from "zod";

export class ValkeySessionManager {
  private redis: Redis;

  constructor(connectionString: string) {
    this.redis = new Redis(connectionString);
  }

  private getKey(waId: string): string {
    return `session:whatsapp:${waId}`;
  }

  async getSession(waId: string): Promise<z.infer<typeof ConversationalSessionSchema>> {
    const raw = await this.redis.get(this.getKey(waId));
    if (!raw) {
      return {
        waId,
        customerName: "Cliente",
        currentStep: "idle",
        lastInteractionAt: Date.now(),
        messages: []
      };
    }
    return ConversationalSessionSchema.parse(JSON.parse(raw));
  }

  async saveSession(session: z.infer<typeof ConversationalSessionSchema>): Promise<void> {
    await this.redis.set(this.getKey(session.waId), JSON.stringify(session), "EX", 86400);
  }
}
