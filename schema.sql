-- =====================================================================
-- AgriLink Platform: Supabase / PostgreSQL Master Schema
-- Supports WhatsApp Integration, 68-10-14-8 Split, PostGIS Catchment, & RLS
-- =====================================================================

-- 1. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- 2. ENUMS
CREATE TYPE user_role AS ENUM (
    'farmer',
    'aggregator',
    'customer',
    'institutional_buyer',
    'delivery_partner',
    'admin'
);

CREATE TYPE order_status AS ENUM (
    'PENDING',
    'CONFIRMED',
    'PACKED',
    'ASSIGNED',
    'OUT_FOR_DELIVERY',
    'DELIVERED',
    'CANCELLED'
);

CREATE TYPE quality_grade AS ENUM ('A', 'B', 'C');

-- 3. PROFILES TABLE (Multi-role users)
CREATE TABLE profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(20) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role user_role NOT NULL,
    preferred_language VARCHAR(5) DEFAULT 'kn', -- 'kn', 'hi', 'en', 'te'
    upi_id VARCHAR(50),
    location_coordinates GEOMETRY(Point, 4326),
    address_text TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. FARMS TABLE (Module M2)
CREATE TABLE farms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    farm_name VARCHAR(100),
    acreage NUMERIC(5,2),
    soil_type VARCHAR(50),
    village VARCHAR(100),
    taluk VARCHAR(100) DEFAULT 'Maddur',
    district VARCHAR(100) DEFAULT 'Mandya',
    state VARCHAR(50) DEFAULT 'Karnataka',
    gps_coordinates GEOMETRY(Point, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. CROP HARVEST DECLARATIONS & LISTINGS (Module M2)
CREATE TABLE crop_listings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    crop_name VARCHAR(50) NOT NULL,
    quantity_kg NUMERIC(8,2) NOT NULL,
    expected_harvest_date DATE NOT NULL,
    is_organic BOOLEAN DEFAULT FALSE,
    status VARCHAR(30) DEFAULT 'PRE_DECLARED', -- 'PRE_DECLARED', 'COLLECTED', 'SOLD'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. AGGREGATOR HUBS & BATCH ASSAYS (Module M5 & M11)
CREATE TABLE aggregator_hubs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hub_name VARCHAR(100) NOT NULL,
    manager_id UUID REFERENCES profiles(id),
    catchment_radius_km INT DEFAULT 25,
    location_coordinates GEOMETRY(Point, 4326),
    address_text TEXT
);

CREATE TABLE produce_batches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch_code VARCHAR(30) UNIQUE NOT NULL, -- e.g. BATCH-MD-882
    hub_id UUID REFERENCES aggregator_hubs(id),
    farmer_id UUID REFERENCES profiles(id),
    crop_name VARCHAR(50) NOT NULL,
    net_weight_kg NUMERIC(8,2) NOT NULL,
    grade quality_grade DEFAULT 'A',
    locked_farmer_rate_per_kg NUMERIC(8,2) NOT NULL,
    total_farmer_payout NUMERIC(10,2) NOT NULL,
    qr_provenance_hash VARCHAR(128),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 7. ORDERS & 4-WAY SETTLEMENT LEDGER (Modules M6 & M10)
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_code VARCHAR(30) UNIQUE NOT NULL, -- e.g. ORD-98721
    customer_id UUID REFERENCES profiles(id),
    delivery_partner_id UUID REFERENCES profiles(id),
    status order_status DEFAULT 'PENDING',
    total_amount NUMERIC(10,2) NOT NULL,
    delivery_otp VARCHAR(6) NOT NULL,
    delivery_address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE settlement_ledger (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES orders(id) ON DELETE RESTRICT,
    recipient_id UUID REFERENCES profiles(id),
    recipient_role user_role NOT NULL,
    allocation_percentage NUMERIC(5,2) NOT NULL, -- 68%, 10%, 14%, 8%
    amount NUMERIC(10,2) NOT NULL,
    upi_reference VARCHAR(100),
    status VARCHAR(20) DEFAULT 'PENDING', -- 'PENDING', 'SETTLED'
    settled_at TIMESTAMP WITH TIME ZONE
);

-- 8. WHATSAPP CONVERSATION SESSIONS
CREATE TABLE whatsapp_sessions (
    phone VARCHAR(20) PRIMARY KEY,
    current_step VARCHAR(50) DEFAULT 'MAIN_MENU',
    session_data JSONB DEFAULT '{}'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 9. ROW-LEVEL SECURITY (RLS) POLICIES
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE crop_listings ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE settlement_ledger ENABLE ROW LEVEL SECURITY;

-- Farmers can only see their own listings and payouts
CREATE POLICY farmer_own_listings ON crop_listings
    FOR ALL USING (auth.uid() = farmer_id);

CREATE POLICY farmer_own_payouts ON settlement_ledger
    FOR SELECT USING (auth.uid() = recipient_id);

-- Customers can only see their own orders
CREATE POLICY customer_own_orders ON orders
    FOR SELECT USING (auth.uid() = customer_id);
