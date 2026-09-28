-- Extensiones requeridas
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Tabla de Órdenes
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(50) NOT NULL,
    customer_document_id VARCHAR(50),
    shipping_address_line1 TEXT NOT NULL,
    shipping_neighborhood VARCHAR(100),
    shipping_city_dane VARCHAR(8) NOT NULL,
    shipping_city_name VARCHAR(100) NOT NULL,
    shipping_department_name VARCHAR(100) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    is_cod BOOLEAN DEFAULT FALSE,
    cod_amount NUMERIC(12, 2) DEFAULT 0.00,
    subtotal_amount NUMERIC(12, 2) NOT NULL,
    shipping_fee NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    total_amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'COP',
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Tabla de Bloqueos Atómicos de Inventario
CREATE TABLE IF NOT EXISTS inventory_locks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    sku VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    status VARCHAR(30) NOT NULL DEFAULT 'active',
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. Tabla de Guías de Envío y Despacho
CREATE TABLE IF NOT EXISTS shipping_labels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE RESTRICT,
    carrier VARCHAR(50) NOT NULL,
    tracking_number VARCHAR(100) NOT NULL UNIQUE,
    reference_code VARCHAR(100),
    actual_weight_kg NUMERIC(8, 3) NOT NULL,
    volumetric_weight_kg NUMERIC(8, 3) NOT NULL,
    billed_weight_kg NUMERIC(8, 3) NOT NULL,
    declared_value NUMERIC(12, 2) NOT NULL,
    cod_collection_value NUMERIC(12, 2) DEFAULT 0.00,
    shipping_cost NUMERIC(12, 2) NOT NULL,
    label_format VARCHAR(20) NOT NULL DEFAULT 'pdf',
    label_url TEXT,
    tracking_url TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'generated',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. Tabla de Gestión de Novedades de Entrega
CREATE TABLE IF NOT EXISTS delivery_novelties (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shipping_label_id UUID NOT NULL REFERENCES shipping_labels(id) ON DELETE CASCADE,
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    novelty_type VARCHAR(100) NOT NULL,
    attempt_number INTEGER NOT NULL DEFAULT 1,
    carrier_notes TEXT,
    customer_contacted BOOLEAN DEFAULT FALSE,
    resolution_status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);
