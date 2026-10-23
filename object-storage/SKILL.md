---
name: object-storage
description: "Trigger: object-storage, objectstorage, s3, minio, aws s3, presigned url, bucket, blob storage, s3 upload, s3 download, storage_apiUrl. Architect, configure, operate, and integrate Zerops S3-compatible Object Storage."
license: Apache-2.0
metadata:
  author: "gentleman-programming"
  version: "1.0"
  cohalo-standard: "6.7"
---

# Object Storage — S3 MinIO Persistent Blob & Media Engine (v1.0)

## Activation Contract
Activate when architecting, configuring, provisioning, integrating, or operating Zerops Object Storage (`type: object-storage` / MinIO S3 API) across runtime services (Bun, Node.js, Python, Go) for persistent binary blobs, user uploads, client dossiers, generated PDF reports, brandbook assets, or pre-signed URL distribution.

## Hard Rules & Critical Invariants
1. **Path-Style Endpoint Law**: Zerops Object Storage is S3-compatible (MinIO) and requires path-style addressing (`AWS_USE_PATH_STYLE_ENDPOINT: "true"` or `forcePathStyle: true`). Virtual-hosted style URLs fail with connection errors.
2. **Canonical HTTPS Scheme**: Cross-service access MUST use `${storage_apiUrl}` as endpoint URL (`https://...`). Never use bare HTTP or `${storage_apiHost}` without HTTPS scheme; the gateway rejects plaintext HTTP with a 301 redirect that S3 SDKs do not follow.
3. **Zero Plaintext Credentials**: S3 access keys, secret keys, and bucket names MUST be injected via platform template variables (`${storage_accessKeyId}`, `${storage_secretAccessKey}`, `${storage_bucketName}`). Never hardcode credentials.
4. **Policy Segmentation**: Assign `objectStoragePolicy: private` for confidential client documents, database backups, and raw exports; assign `public-read` strictly for public CDN assets, avatars, and public marketing media.
5. **Storage Tiering & Opt-In Principle**: `object-storage` is **strictly optional**. In starter and lean e-commerce projects, persistent assets (product photos, Brandbook files, local uploads) reside directly on `local-storage` (`run.volume`) under `/mnt/localstorage/${PROJECT_NAME}/media/` with zero extra infrastructure cost and NVMe <0.1ms latency. Both `local-storage` and `object-storage` survive deploys and container recreation. Only provision `object-storage` when horizontal multi-host scaling, public Cloudflare Edge offload, or high-volume ERPNext/Frappe digital archives are actively required.
6. **No Binary Blobs in Databases**: Store binary files (PDFs, images, archives) on filesystem disk paths (`local-storage`) or S3 keys (`object-storage`); never serialize raw binary buffers into PostgreSQL rows.

## Decision Matrix

| Task / Domain | Technical Pattern | Reference / Asset |
|---|---|---|
| Service Provisioning | `type: object-storage`, `objectStorageSize`, policy | [`references/infra.md#1-zerops-object-storage-specification`](references/infra.md) |
| Environment Injection | `${storage_apiUrl}`, `${storage_accessKeyId}`, path-style | [`references/infra.md#2-environment-variables-wiring`](references/infra.md) |
| TypeScript / Bun SDK | `@aws-sdk/client-s3`, stream upload, buffer handling | [`references/usage.md#1-typescript--bun-integration`](references/usage.md) |
| Python Integration | `boto3`, `botocore.client.Config(signature_version='s3v4')` | [`references/usage.md#2-python-boto3-integration`](references/usage.md) |
| Pre-Signed URLs | Expiring GET/PUT signed URLs for secure client downloads | [`references/usage.md#3-pre-signed-urls-generation`](references/usage.md) |
| Directus / S3 Drivers | Directus 11+ storage driver configuration | [`references/usage.md#4-directus-headless-cms-s3-driver`](references/usage.md) |
| Physical Validation | Deterministic validator of skill structure and AST | [`scripts/object-storage-validate.sh``skills-suite-validate` |

## Commands
```bash
# Execute deterministic physical validation sensor
skills-suite-validate
```

## References
- [`references/usage.md`](references/usage.md) — Node/Bun and Python S3 client patterns, uploads, downloads, pre-signed URLs, and Directus driver.
- [`references/infra.md`](references/infra.md) — Zerops manifest specification, sizing, security policies, and environment variable references.
