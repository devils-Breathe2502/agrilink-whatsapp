"""
AgriLink WhatsApp Integration - Configuration Module
Supports environment settings, provider selection, and regional language configurations.
"""

import os

# Twilio Settings (Default provider as per AgriLink Architecture Module M14 / Ref R31)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "AC_mock_twilio_account_sid")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "mock_twilio_auth_token")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

# Meta Cloud API Settings (Optional direct provider)
WHATSAPP_CLOUD_API_TOKEN = os.getenv("WHATSAPP_CLOUD_API_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "agrilink_sfic_2026_secret")

# Supabase PostgreSQL Settings
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "your-supabase-key")

# Speech & AI API Settings (Bhashini / OpenAI Whisper / Gemini)
AI_API_KEY = os.getenv("AI_API_KEY", "")

# AgriLink Business Model Ratios (Illustrative 68-10-14-8 model)
ALLOCATION_RATIOS = {
    "farmer_share": 0.68,       # 68% direct to producer
    "aggregator_share": 0.10,   # 10% to SHG / Hub
    "delivery_share": 0.14,     # 14% to local youth / vehicle
    "platform_share": 0.08      # 8% platform fee
}

# Supported Regional Languages
SUPPORTED_LANGUAGES = {
    "en": "English",
    "kn": "ಕನ್ನಡ (Kannada)",
    "hi": "हिन्दी (Hindi)",
    "te": "తెలుగు (Telugu)"
}
