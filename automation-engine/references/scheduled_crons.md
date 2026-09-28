# Scheduled Crons & Periodic Reconciliation (v2.0)

## 1. Scheduled Background Routines
- **Cart Reservation Cleanup (Every 15 min)**:
  - Scans Directus orders in `pending_payment` older than 30 minutes.
  - Returns held SKU stock back to the available inventory pool.
- **WhatsApp Gateway Watchdog (Every 5 min)**:
  - Queries `GET /instance/status` on Evolution Go.
  - Emits alerts to NATS if the session transitions to `connecting` or `close`.
- **Payment Reconciliation Sweep (Daily at 02:00 UTC)**:
  - Queries Wompi and Stripe for any transactions in `PENDING` state and reconciles against Directus order records.
