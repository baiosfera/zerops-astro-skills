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
5. **Epistemic Separation (POSIX vs S3)**: Use `local-storage` (`run.volume`) for embedded databases (SQLite WAL), live process sockets, and local caches; use `object-storage` for durable files that must survive deploys and container recreation.
6. **No Binary Blobs in Databases**: Files larger than 500 KB (PDFs, high-res images, archives) MUST reside in Object Storage; store only the S3 object key or canonical URL in PostgreSQL.

## Decision Matrix

| Task / Domain | Technical Pattern | Reference / Asset |
|---|---|---|
| Service Provisioning | `type: object-storage`, `objectStorageSize`, policy | [`references/infra.md#1-zerops-object-storage-specification`](references/infra.md) |
| Environment Injection | `${storage_apiUrl}`, `${storage_accessKeyId}`, path-style | [`references/infra.md#2-environment-variables-wiring`](references/infra.md) |
| TypeScript / Bun SDK | `@aws-sdk/client-s3`, stream upload, buffer handling | [`references/usage.md#1-typescript--bun-integration`](references/usage.md) |
| Python Integration | `boto3`, `botocore.client.Config(signature_version='s3v4')` | [`references/usage.md#2-python-boto3-integration`](references/usage.md) |
| Pre-Signed URLs | Expiring GET/PUT signed URLs for secure client downloads | [`references/usage.md#3-pre-signed-urls-generation`](references/usage.md) |
| Directus / S3 Drivers | Directus 11+ storage driver configuration | [`references/usage.md#4-directus-headless-cms-s3-driver`](references/usage.md) |
| Physical Validation | Deterministic validator of skill structure and AST | [`scripts/object-storage-validate.sh`](scripts/object-storage-validate.sh) |

## Commands
```bash
# Execute deterministic physical validation sensor
bash /var/www/.agents/skills/object-storage/scripts/object-storage-validate.sh
```

## References
- [`references/usage.md`](references/usage.md) — Node/Bun and Python S3 client patterns, uploads, downloads, pre-signed URLs, and Directus driver.
- [`references/infra.md`](references/infra.md) — Zerops manifest specification, sizing, security policies, and environment variable references.
