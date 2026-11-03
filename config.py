"""
AgriLink WhatsApp Integration - Meta Cloud API Configuration
Direct official integration with Meta (Facebook) WhatsApp Business Cloud API.
Zero third-party middlemen (No Twilio).
"""

import os

# Meta Developer App Settings (from developers.facebook.com)
WHATSAPP_CLOUD_API_TOKEN = os.getenv("WHATSAPP_CLOUD_API_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "agrilink_sfic_2026_secret")
GRAPH_API_VERSION = "v21.0"
META_GRAPH_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

# Supabase / PostgreSQL Settings
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

# AgriLink 4-Way Payout Split Policy (SFIC 2026 Innovation Model)
ALLOCATION_RATIOS = {
    "farmer_share": 0.68,       # 68% direct to smallholder farmer
    "aggregator_share": 0.10,   # 10% to village SHG / collection hub
    "delivery_share": 0.14,     # 14% to local youth / vehicle fleet
    "platform_share": 0.08      # 8% AgriLink platform fee
}

# Regional Language Support
SUPPORTED_LANGUAGES = {
    "kn": "ಕನ್ನಡ (Kannada)",
    "hi": "हिन्दी (Hindi)",
    "en": "English",
    "te": "తెలుగు (Telugu)"
}
