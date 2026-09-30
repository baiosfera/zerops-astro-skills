# Object Storage Usage Manual (TypeScript, Bun & Python)

Comprehensive developer and agent reference manual for interacting with Zerops S3-compatible Object Storage (MinIO) across application runtimes.

---

## 1. TypeScript & Bun Integration

Zerops Object Storage is 100% compatible with the official AWS SDK v3 (`@aws-sdk/client-s3`) and presigned request utilities (`@aws-sdk/s3-request-presigner`).

### A. Client Initialization
```typescript
import { S3Client, PutObjectCommand, GetObjectCommand } from "@aws-sdk/client-s3";

export const s3 = new S3Client({
  endpoint: process.env.S3_ENDPOINT, // e.g. ${objectstorage_apiUrl}
  region: process.env.S3_REGION || "us-east-1",
  credentials: {
    accessKeyId: process.env.S3_ACCESS_KEY!,
    secretAccessKey: process.env.S3_SECRET_KEY!,
  },
  forcePathStyle: true, // MANDATORY: MinIO requires path-style addressing
});
```

### B. Uploading Binary Buffers & Streams
```typescript
import { PutObjectCommand } from "@aws-sdk/client-s3";

export async function uploadClientDossier(
  clientId: string,
  fileName: string,
  buffer: Buffer,
  contentType: string = "application/pdf"
): Promise<string> {
  const key = `clients/${clientId}/${fileName}`;
  
  await s3.send(
    new PutObjectCommand({
      Bucket: process.env.S3_BUCKET!,
      Key: key,
      Body: buffer,
      ContentType: contentType,
    })
  );

  return key;
}
```

### C. Reading Objects as Buffer / String
```typescript
import { GetObjectCommand } from "@aws-sdk/client-s3";
import { Readable } from "stream";

export async function getObjectBuffer(key: string): Promise<Buffer> {
  const response = await s3.send(
    new GetObjectCommand({
      Bucket: process.env.S3_BUCKET!,
      Key: key,
    })
  );

  const stream = response.Body as Readable;
  const chunks: Buffer[] = [];
  for await (const chunk of stream) {
    chunks.push(Buffer.from(chunk));
  }
  return Buffer.concat(chunks);
}
```

---

## 2. Python (boto3) Integration

For Python microservices (`engine`, `hermes`, FastAPI, Granian), use `boto3` configured with S3v4 signature and path-style addressing.

### A. Client Configuration
```python
import os
import boto3
from botocore.client import Config

s3_client = boto3.client(
    "s3",
    endpoint_url=os.environ.get("S3_ENDPOINT"),  # e.g. ${objectstorage_apiUrl}
    aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
    aws_secret_access_key=os.environ.get("S3_SECRET_KEY"),
    region_name=os.environ.get("S3_REGION", "us-east-1"),
    config=Config(
        signature_version="s3v4",
        s3={"addressing_style": "path"}  # MANDATORY: MinIO path style
    )
)
BUCKET_NAME = os.environ.get("S3_BUCKET")
```

### B. Uploading JSON Shards & Dumps
```python
import json

def upload_json_shard(client_id: str, shard_name: str, data: dict) -> str:
    key = f"dumps/{client_id}/{shard_name}.json"
    body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=body,
        ContentType="application/json; charset=utf-8"
    )
    return key
```

---

## 3. Pre-Signed URLs Generation

Pre-signed URLs allow secure, temporary direct downloads or uploads from client browsers without routing large binary streams through application servers.

### A. TypeScript / Bun Pre-Signed GET URL
```typescript
import { GetObjectCommand } from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

export async function createDownloadUrl(key: string, expiresInSeconds = 3600): Promise<string> {
  const command = new GetObjectCommand({
    Bucket: process.env.S3_BUCKET!,
    Key: key,
  });

  return await getSignedUrl(s3, command, { expiresIn: expiresInSeconds });
}
```

### B. Python Pre-Signed GET URL
```python
def generate_presigned_download_url(key: str, expiration_seconds: int = 3600) -> str:
    return s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET_NAME, "Key": key},
        ExpiresIn=expiration_seconds
    )
```

---

## 4. Directus Headless CMS S3 Driver

To bind Directus 11+ to Zerops Object Storage, set the following environment variables in Directus runtime:

```yaml
envVariables:
  STORAGE_LOCATIONS: "s3"
  STORAGE_S3_DRIVER: "s3"
  STORAGE_S3_KEY: ${objectstorage_accessKeyId}
  STORAGE_S3_SECRET: ${objectstorage_secretAccessKey}
  STORAGE_S3_BUCKET: ${objectstorage_bucketName}
  STORAGE_S3_REGION: "us-east-1"
  STORAGE_S3_ENDPOINT: ${objectstorage_apiUrl}
  STORAGE_S3_FORCE_PATH_STYLE: "true"
```
