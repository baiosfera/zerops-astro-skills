import { z } from "zod";
import {
  CloudflareApiResponseSchema,
  CloudflareDnsRecord,
  CloudflareDnsRecordInput,
  CloudflareDnsRecordSchema,
} from "./dns_zod_schemas";

export interface CloudflareClientConfig {
  apiToken: string;
  zoneId?: string;
  accountId?: string;
  baseDomain?: string;
}

export class CloudflareV4Client {
  private readonly baseUrl = "https://api.cloudflare.com/client/v4";
  private readonly headers: Record<string, string>;

  constructor(private readonly config: CloudflareClientConfig) {
    if (!config.apiToken) {
      throw new Error(
        `[F1 CLARIFICATION GATE - cloudflare]\n` +
        `CLOUDFLARE_API_TOKEN is missing in environment.\n` +
        `Please configure CLOUDFLARE_API_TOKEN in Zerops environment or keys.md.`
      );
    }
    this.headers = {
      Authorization: `Bearer ${config.apiToken}`,
      "Content-Type": "application/json",
    };
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
    schema: z.ZodType<T>
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        ...this.headers,
        ...options.headers,
      },
    });

    const data = await response.json();
    const wrapped = CloudflareApiResponseSchema(schema).safeParse(data);

    if (!wrapped.success || !wrapped.data.success) {
      const errorMsg = wrapped.success
        ? wrapped.data.errors.map((e) => `[${e.code}] ${e.message}`).join(", ")
        : JSON.stringify(wrapped.error.format());
      throw new Error(`Cloudflare API Error (${response.status} on ${endpoint}): ${errorMsg}`);
    }

    return wrapped.data.result;
  }

  /** Resolves Zone ID for a domain name */
  async getZoneId(domain: string): Promise<string> {
    if (this.config.zoneId) return this.config.zoneId;

    const schema = z.array(z.object({ id: z.string(), name: z.string() }));
    const result = await this.request(`/zones?name=${encodeURIComponent(domain)}`, {}, schema);

    if (!result || result.length === 0) {
      throw new Error(`Zone for domain '${domain}' not found in Cloudflare account.`);
    }
    return result[0].id;
  }

  /** Lists all DNS records for a zone */
  async listDnsRecords(zoneId: string): Promise<CloudflareDnsRecord[]> {
    return this.request(
      `/zones/${zoneId}/dns_records?per_page=100`,
      { method: "GET" },
      z.array(CloudflareDnsRecordSchema)
    );
  }

  /** Creates a DNS record */
  async createDnsRecord(zoneId: string, record: CloudflareDnsRecordInput): Promise<CloudflareDnsRecord> {
    return this.request(
      `/zones/${zoneId}/dns_records`,
      {
        method: "POST",
        body: JSON.stringify(record),
      },
      CloudflareDnsRecordSchema
    );
  }

  /** Updates an existing DNS record */
  async updateDnsRecord(
    zoneId: string,
    recordId: string,
    record: Partial<CloudflareDnsRecordInput>
  ): Promise<CloudflareDnsRecord> {
    return this.request(
      `/zones/${zoneId}/dns_records/${recordId}`,
      {
        method: "PATCH",
        body: JSON.stringify(record),
      },
      CloudflareDnsRecordSchema
    );
  }

  /** Deletes a DNS record */
  async deleteDnsRecord(zoneId: string, recordId: string): Promise<{ id: string }> {
    return this.request(
      `/zones/${zoneId}/dns_records/${recordId}`,
      { method: "DELETE" },
      z.object({ id: z.string() })
    );
  }

  /** Declarative and idempotent DNS synchronization */
  async syncDnsRecords(
    zoneId: string,
    desiredRecords: CloudflareDnsRecordInput[],
    baseDomain: string
  ): Promise<{ created: number; updated: number; untouched: number }> {
    const liveRecords = await this.listDnsRecords(zoneId);
    let created = 0;
    let updated = 0;
    let untouched = 0;

    for (const desired of desiredRecords) {
      const fqdn = desired.name === "@" ? baseDomain : desired.name.includes(".") ? desired.name : `${desired.name}.${baseDomain}`;
      const existing = liveRecords.find((r) => r.name.toLowerCase() === fqdn.toLowerCase() && r.type === desired.type);

      if (!existing) {
        await this.createDnsRecord(zoneId, { ...desired, name: fqdn });
        created++;
      } else {
        const needsUpdate =
          existing.content !== desired.content ||
          existing.proxied !== (desired.proxied ?? false) ||
          (desired.ttl && existing.ttl !== desired.ttl);

        if (needsUpdate) {
          await this.updateDnsRecord(zoneId, existing.id, {
            content: desired.content,
            proxied: desired.proxied ?? false,
            ttl: desired.ttl ?? 1,
          });
          updated++;
        } else {
          untouched++;
        }
      }
    }

    return { created, updated, untouched };
  }

  /** Enforces SSL/TLS Full Strict mode */
  async setSslModeStrict(zoneId: string): Promise<{ value: string }> {
    return this.request(
      `/zones/${zoneId}/settings/ssl`,
      {
        method: "PATCH",
        body: JSON.stringify({ value: "strict" }),
      },
      z.object({ value: z.string() })
    );
  }

  /** Enables Always Use HTTPS */
  async enableAlwaysUseHttps(zoneId: string): Promise<{ value: string }> {
    return this.request(
      `/zones/${zoneId}/settings/always_use_https`,
      {
        method: "PATCH",
        body: JSON.stringify({ value: "on" }),
      },
      z.object({ value: z.string() })
    );
  }

  /** Purges CDN cache */
  async purgeCache(zoneId: string, purgeEverything = true, files?: string[]): Promise<{ id: string }> {
    const payload = purgeEverything ? { purge_everything: true } : { files };
    return this.request(
      `/zones/${zoneId}/purge_cache`,
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
      z.object({ id: z.string() })
    );
  }
}

/** Resolves auto-configured Cloudflare client from environment */
export function getAutoConfiguredCloudflareClient(): CloudflareV4Client {
  const apiToken = process.env.CLOUDFLARE_API_TOKEN;
  if (!apiToken) {
    throw new Error(
      `[F1 CLARIFICATION GATE - cloudflare]\n` +
      `CLOUDFLARE_API_TOKEN is not defined in process.env / zerops_env.\n` +
      `Please provide your Cloudflare API Token in keys.md.`
    );
  }

  return new CloudflareV4Client({
    apiToken,
    zoneId: process.env.CLOUDFLARE_ZONE_ID,
    accountId: process.env.CLOUDFLARE_ACCOUNT_ID,
    baseDomain: process.env.CLOUDFLARE_BASE_DOMAIN,
  });
}
