#!/usr/bin/env bun
import { getAutoConfiguredCloudflareClient } from "../assets/cloudflare_client";
import { CloudflareDnsRecordInput, DesiredDnsTopologySchema } from "../assets/dns_zod_schemas";
import fs from "node:fs";

async function main() {
  console.log("============================================================");
  console.log("  🌐 Cloudflare Declarative DNS & Edge Synchronizer (v2.0)");
  console.log("============================================================");

  const baseDomain = process.env.CLOUDFLARE_BASE_DOMAIN;
  if (!baseDomain) {
    console.error("❌ Error: CLOUDFLARE_BASE_DOMAIN is not set in environment.");
    process.exit(1);
  }

  const client = getAutoConfiguredCloudflareClient();
  const zoneId = await client.getZoneId(baseDomain);
  console.log(`• Connected to Zone: ${baseDomain} (Zone ID: ${zoneId})`);

  let desiredRecords: CloudflareDnsRecordInput[] = [];

  // Check if a topology JSON file was provided as argument
  const topologyPath = process.argv[2];
  if (topologyPath && fs.existsSync(topologyPath)) {
    console.log(`• Loading declarative topology manifest: ${topologyPath}`);
    const raw = JSON.parse(fs.readFileSync(topologyPath, "utf-8"));
    const parsed = DesiredDnsTopologySchema.parse(raw);
    desiredRecords = parsed.records;
  } else {
    // Dynamic synthesis from environment variables
    const dedicatedIpv4 = process.env.ZEROPS_DEDICATED_IPV4;
    const dedicatedIpv6 = process.env.ZEROPS_DEDICATED_IPV6;

    if (dedicatedIpv4) {
      desiredRecords.push({
        type: "A",
        name: "@",
        content: dedicatedIpv4,
        proxied: true,
        comment: "Apex - Zerops Dedicated IPv4",
      });
    }
    if (dedicatedIpv6) {
      desiredRecords.push({
        type: "AAAA",
        name: "@",
        content: dedicatedIpv6,
        proxied: true,
        comment: "Apex - Zerops Dedicated IPv6",
      });
    }

    desiredRecords.push({
      type: "CNAME",
      name: "www",
      content: baseDomain,
      proxied: true,
      comment: "WWW Canonical Alias",
    });

    // Custom subdomains if provided in environment
    if (process.env.APP_SUBDOMAIN) {
      desiredRecords.push({
        type: "CNAME",
        name: process.env.APP_SUBDOMAIN_NAME || "app",
        content: process.env.APP_SUBDOMAIN,
        proxied: true,
        comment: "Application Subdomain",
      });
    }

    // RFC 9989 Compliant DMARC Policy (No 'pct' tag)
    const dmarcReportEmail = process.env.DMARC_REPORT_EMAIL || `dmarc-reports@${baseDomain}`;
    desiredRecords.push({
      type: "TXT",
      name: "_dmarc",
      content: `v=DMARC1; p=reject; sp=reject; np=reject; t=n; rua=mailto:${dmarcReportEmail};`,
      proxied: false,
      comment: "RFC 9989 Compliant DMARCbis Policy",
    });

    // SPF Policy if defined
    if (process.env.SPF_RECORD_VALUE) {
      desiredRecords.push({
        type: "TXT",
        name: "@",
        content: process.env.SPF_RECORD_VALUE,
        proxied: false,
        comment: "Authoritative SPF Record",
      });
    }
  }

  console.log(`• Synchronizing ${desiredRecords.length} desired DNS records...`);
  const result = await client.syncDnsRecords(zoneId, desiredRecords, baseDomain);

  console.log(`  ✅ Created: ${result.created}`);
  console.log(`  ✅ Updated: ${result.updated}`);
  console.log(`  ✅ Untouched (in-sync): ${result.untouched}`);

  // Enforce SSL Full Strict mode and Always Use HTTPS
  console.log("• Enforcing Cloudflare SSL/TLS Full Strict mode & Always Use HTTPS...");
  await client.setSslModeStrict(zoneId);
  await client.enableAlwaysUseHttps(zoneId);
  console.log("  ✅ SSL/TLS configured to Full (strict)");

  console.log("============================================================");
  console.log("  🎉 DNS & Edge CDN Synchronization Completed Successfully");
  console.log("============================================================");
}

main().catch((err) => {
  console.error("❌ Fatal Error:", err.message);
  process.exit(1);
});
