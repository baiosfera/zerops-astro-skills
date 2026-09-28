import { z } from "zod";

export const DnsRecordTypeSchema = z.enum([
  "A",
  "AAAA",
  "CNAME",
  "TXT",
  "MX",
  "NS",
  "SRV",
  "CAA",
]);
export type DnsRecordType = z.infer<typeof DnsRecordTypeSchema>;

export const CloudflareDnsRecordInputSchema = z.object({
  type: DnsRecordTypeSchema,
  name: z.string().min(1).describe("Record name or FQDN (e.g. api, @, wa, _dmarc)"),
  content: z.string().min(1).describe("Record destination value (IP address, target FQDN, or TXT string)"),
  ttl: z.number().int().min(1).max(86400).default(1).describe("1 = Automatic TTL"),
  proxied: z.boolean().default(false).describe("Whether Cloudflare proxy (orange cloud) is enabled"),
  priority: z.number().int().optional().describe("Required for MX records"),
  comment: z.string().optional().describe("Internal description/metadata"),
});
export type CloudflareDnsRecordInput = z.infer<typeof CloudflareDnsRecordInputSchema>;

export const CloudflareDnsRecordSchema = CloudflareDnsRecordInputSchema.extend({
  id: z.string().min(1),
  zone_id: z.string().min(1),
  zone_name: z.string(),
  created_on: z.string(),
  modified_on: z.string(),
});
export type CloudflareDnsRecord = z.infer<typeof CloudflareDnsRecordSchema>;

export const CloudflareApiResponseSchema = <T extends z.ZodTypeAny>(resultSchema: T) =>
  z.object({
    success: z.boolean(),
    errors: z.array(z.object({ code: z.number(), message: z.string() })),
    messages: z.array(z.string()),
    result: resultSchema,
  });

export const DesiredDnsTopologySchema = z.object({
  baseDomain: z.string().min(1),
  zoneId: z.string().optional(),
  sslMode: z.enum(["strict", "full", "flexible", "off"]).default("strict"),
  alwaysUseHttps: z.boolean().default(true),
  records: z.array(CloudflareDnsRecordInputSchema),
});
export type DesiredDnsTopology = z.infer<typeof DesiredDnsTopologySchema>;
