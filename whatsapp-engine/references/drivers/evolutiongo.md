# Evolution Go Driver Specification (v1.0)

## 1. Engine Capabilities & Zero-Overhead Footprint
Evolution Go is written in Go (`whatsmeow` library) compiling to a single static binary running on Alpine Linux in Zerops Incus LXC.
- Memory footprint: ~25-45 MB RAM idle (vs 400+ MB for Node.js).
- Direct PostgreSQL session storage (`evogo_auth` and `evogo_users`).
- WebAuthn Passkey pairing and QR code generation.
- Media handling: Image, Video, Document, Voice note PTT, and interactive button carousels.

---

## 2. Health Monitoring & Watchdog
A connection watchdog runs periodically against `GET /instance/status` to monitor state:
- If state is `close` or `connecting`, emit alert to NATS subject `alerts.whatsapp.disconnected`.
- Auto-reconnect routine triggers `POST /instance/connect`.

---

## 3. Deep Reference Documentation
- [`references/drivers/evolutiongo_full_usage.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/evolutiongo_full_usage.md) — 4D matrix, instance lifecycle endpoints, pairing codes, WebAuthn Passkey, media endpoints, and cURLs.
- [`references/drivers/evolutiongo_infra.md`](file:///var/www/.agents/skills/whatsapp-engine/references/drivers/evolutiongo_infra.md) — Alpine LXC setup, systemd, Zerops topology, and PostgreSQL session stores.
