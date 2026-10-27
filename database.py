"""
AgriLink WhatsApp Integration - Database & Data Access Layer
Supports Supabase (PostgreSQL) with full offline fallback mock store for instant testing.
"""

from typing import Dict, Any, Optional, List
import datetime

# Mock In-Memory Store populated with realistic AgriLink test actors & data
SEED_PROFILES: Dict[str, Dict[str, Any]] = {
    # 1. Farmer in Mandya
    "+919876500001": {
        "id": "farm_001",
        "name": "Shivanna Gowda",
        "role": "farmer",
        "phone": "+919876500001",
        "language": "kn",
        "village": "Maddur Taluk, Mandya",
        "acres": 3.5,
        "crops": ["Tomato", "Green Chilli", "Palak"],
        "upi_id": "shivanna@upi",
        "unsettled_balance": 1530.00,
        "recent_payouts": [
            {"order_id": "ORD-98721", "crop": "Tomato (Grade A)", "qty": "50 kg", "amount": 1530.00, "status": "SETTLED_UPI", "date": "2026-10-24"}
        ]
    },
    # 2. Local Aggregator (SHG leader)
    "+919876500002": {
        "id": "agg_001",
        "name": "Lakshmi Devi (Annapurna SHG)",
        "role": "aggregator",
        "phone": "+919876500002",
        "language": "kn",
        "hub_name": "Maddur Aggregator Hub #1",
        "catchment_radius_km": 25,
        "farmers_count": 28,
        "unsettled_commission": 2840.00
    },
    # 3. Retail Customer in Bengaluru
    "+919876500003": {
        "id": "cust_001",
        "name": "Priya Verma",
        "role": "customer",
        "phone": "+919876500003",
        "language": "en",
        "delivery_address": "Flat 402, Sunshine Heights, Bengaluru Urban",
        "active_orders": [
            {
                "order_id": "ORD-98721",
                "status": "OUT_FOR_DELIVERY",
                "items": ["Fresh Red Tomatoes (2 kg)", "Palak (1 kg)", "Ginger (250g)"],
                "total_amount": 144.00,
                "driver_name": "Manjunath K",
                "driver_phone": "+919876500005",
                "otp": "4829",
                "eta": "25 mins",
                "farm_origin": "Shivanna's Farm, Mandya"
            }
        ],
        "last_basket": ["Tomatoes (2 kg)", "Onion (2 kg)", "Palak (2 bunches)", "Green Chilli (250g)"]
    },
    # 4. Institutional Buyer (Hostel Warden)
    "+919876500004": {
        "id": "inst_001",
        "name": "Warden Raghavan",
        "institution": "Kengeri Engineering College Hostel",
        "role": "institutional_buyer",
        "phone": "+919876500004",
        "language": "en",
        "standing_orders": [
            {"day": "Monday", "crop": "Potato", "qty": "150 kg", "grade": "Grade A"},
            {"day": "Thursday", "crop": "Mixed Veg (Tomato/Cabbage)", "qty": "100 kg", "grade": "Grade A"}
        ],
        "monthly_spend": 48200.00,
        "latest_gst_invoice": "INV-2026-10-884"
    },
    # 5. Delivery Partner
    "+919876500005": {
        "id": "del_001",
        "name": "Manjunath K",
        "role": "delivery_partner",
        "phone": "+919876500005",
        "language": "kn",
        "vehicle_type": "Mahindra Treo Electric 3-Wheeler",
        "vehicle_reg": "KA-11-EV-2041",
        "active_run": {
            "run_id": "RUN-BGL-084",
            "hub": "Maddur Hub",
            "stops": 8,
            "current_drop": "ORD-98721 (Priya Verma - Bengaluru)",
            "customer_otp": "4829",
            "est_payout": 840.00
        },
        "today_earnings": 1120.00,
        "completed_trips": 3
    }
}

# Catalog for fresh marketplace (Module M3)
FRESH_CATALOG = [
    {"id": "prod_1", "name": "Fresh Red Tomatoes", "price_per_kg": 38.00, "farmer_payout": 25.84, "origin": "Mandya"},
    {"id": "prod_2", "name": "Fresh Green Chilli", "price_per_kg": 39.36, "farmer_payout": 26.76, "origin": "Maddur"},
    {"id": "prod_3", "name": "Organic Palak", "price_per_kg": 28.69, "farmer_payout": 19.50, "origin": "Ramanagara"},
    {"id": "prod_4", "name": "Ginger (Grade A)", "price_per_kg": 72.38, "farmer_payout": 49.21, "origin": "Hassan"},
    {"id": "prod_5", "name": "Nashik Red Onion", "price_per_kg": 34.50, "farmer_payout": 23.46, "origin": "Bengaluru Rural"}
]

# State store for multi-step conversations
USER_SESSIONS: Dict[str, Dict[str, Any]] = {}

# Saved harvest declarations
HARVEST_DECLARATIONS: List[Dict[str, Any]] = []

# Quality disputes logged via WhatsApp
DISPUTES: List[Dict[str, Any]] = []


class AgriLinkDB:
    @staticmethod
    def get_profile(phone: str) -> Optional[Dict[str, Any]]:
        # Normalize phone
        clean_phone = phone.strip()
        if not clean_phone.startswith("+"):
            clean_phone = "+" + clean_phone
        return SEED_PROFILES.get(clean_phone)

    @staticmethod
    def get_session(phone: str) -> Dict[str, Any]:
        return USER_SESSIONS.get(phone, {"step": "IDLE", "data": {}})

    @staticmethod
    def set_session(phone: str, state: Dict[str, Any]):
        USER_SESSIONS[phone] = state

    @staticmethod
    def reset_session(phone: str):
        if phone in USER_SESSIONS:
            del USER_SESSIONS[phone]

    @staticmethod
    def save_harvest(farmer_id: str, farmer_phone: str, crop: str, qty_kg: float, harvest_date: str) -> Dict[str, Any]:
        record = {
            "id": f"HARV-{len(HARVEST_DECLARATIONS) + 1:04d}",
            "farmer_id": farmer_id,
            "farmer_phone": farmer_phone,
            "crop": crop,
            "qty_kg": qty_kg,
            "harvest_date": harvest_date,
            "status": "PRE_DECLARED_PENDING_PICKUP",
            "created_at": datetime.datetime.now().isoformat()
        }
        HARVEST_DECLARATIONS.append(record)
        return record

    @staticmethod
    def get_todays_manifest_for_hub(hub_name: str) -> List[Dict[str, Any]]:
        return [
            {"farmer": "Shivanna Gowda", "crop": "Tomato", "qty": "200 kg", "village": "Alur (6 km)"},
            {"farmer": "Basavaraju M", "crop": "Green Chilli", "qty": "80 kg", "village": "Gejjalagere (12 km)"},
            {"farmer": "Ningamma K", "crop": "Palak & Methi", "qty": "120 kg", "village": "Kestur (15 km)"}
        ]

    @staticmethod
    def log_quality_dispute(customer_phone: str, order_id: str, issue_text: str, photo_url: Optional[str] = None) -> Dict[str, Any]:
        dispute = {
            "id": f"DISP-{len(DISPUTES) + 101}",
            "customer_phone": customer_phone,
            "order_id": order_id,
            "issue": issue_text,
            "photo_url": photo_url,
            "status": "OPEN_UNDER_REVIEW",
            "created_at": datetime.datetime.now().isoformat()
        }
        DISPUTES.append(dispute)
        return dispute

    @staticmethod
    def verify_delivery_otp(driver_phone: str, entered_otp: str) -> bool:
        driver = SEED_PROFILES.get(driver_phone)
        if not driver or "active_run" not in driver:
            return False
        expected_otp = driver["active_run"].get("customer_otp")
        return entered_otp.strip() == expected_otp.strip()
