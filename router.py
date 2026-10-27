"""
AgriLink WhatsApp Integration - Central Omnichannel Router
Identifies sender role (Farmer, Aggregator, Customer, Institutional Buyer, Delivery Partner)
and dispatches to the corresponding domain handler.
"""

from typing import Dict, Any, Optional

try:
    from agrilink_whatsapp.database import AgriLinkDB, SEED_PROFILES
    from agrilink_whatsapp.handlers.farmer_handler import handle_farmer_message
    from agrilink_whatsapp.handlers.aggregator_handler import handle_aggregator_message
    from agrilink_whatsapp.handlers.customer_handler import handle_customer_message
    from agrilink_whatsapp.handlers.institutional_handler import handle_institutional_message
    from agrilink_whatsapp.handlers.delivery_handler import handle_delivery_message
except ImportError:
    from database import AgriLinkDB, SEED_PROFILES
    from handlers.farmer_handler import handle_farmer_message
    from handlers.aggregator_handler import handle_aggregator_message
    from handlers.customer_handler import handle_customer_message
    from handlers.institutional_handler import handle_institutional_message
    from handlers.delivery_handler import handle_delivery_message


def route_inbound_whatsapp(
    from_phone: str,
    message_text: str = "",
    media_url: Optional[str] = None,
    media_content_type: Optional[str] = None
) -> str:
    """
    Main dispatching pipeline for all WhatsApp messages.
    """
    # Clean phone format
    clean_phone = from_phone.replace("whatsapp:", "").strip()
    profile = AgriLinkDB.get_profile(clean_phone)

    # 1. Handle Unregistered / New User
    if not profile:
        # Check if user is self-registering
        session = AgriLinkDB.get_session(clean_phone)
        step = session.get("step", "ONBOARDING")
        t = message_text.strip()

        if t in ["1", "2", "3", "4"]:
            role_map = {
                "1": ("farmer", "kn"),
                "2": ("customer", "en"),
                "3": ("aggregator", "kn"),
                "4": ("delivery_partner", "kn")
            }
            role, lang = role_map[t]
            SEED_PROFILES[clean_phone] = {
                "id": f"user_{len(SEED_PROFILES) + 1}",
                "name": "New User",
                "role": role,
                "phone": clean_phone,
                "language": lang
            }
            profile = SEED_PROFILES[clean_phone]
            AgriLinkDB.reset_session(clean_phone)
            # Re-dispatch with new profile
            return route_inbound_whatsapp(clean_phone, "menu")

        return (
            "🌾 *Welcome to AgriLink! / ಅಗ್ರಿಲಿಂಕ್‌ಗೆ ಸುಸ್ವಾಗತ!*\n"
            "Connecting Indian farms directly to consumers with transparent 68-10-14-8 pricing.\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "Who are you? Please reply with your role number:\n\n"
            "1️⃣ *ರೈತರು / Farmer* (Sell produce, check mandi rates)\n"
            "2️⃣ *ಗ್ರಾಹಕರು / Retail Customer* (Order fresh farm veggies)\n"
            "3️⃣ *ಸಂಗ್ರಾಹಕ ಹಬ್ / Aggregator (SHG / Youth)*\n"
            "4️⃣ *ವಿತರಣಾ ಪಾಲುದಾರ / Delivery Partner*\n\n"
            "Reply with *1*, *2*, *3*, or *4* to continue."
        )

    # 2. Dispatch by Role
    role = profile.get("role", "customer")

    if role == "farmer":
        return handle_farmer_message(profile, message_text, voice_url=media_url if media_content_type and "audio" in media_content_type else None)

    elif role == "aggregator":
        return handle_aggregator_message(profile, message_text)

    elif role == "customer":
        return handle_customer_message(profile, message_text, photo_url=media_url if media_content_type and "image" in media_content_type else None)

    elif role == "institutional_buyer":
        return handle_institutional_message(profile, message_text)

    elif role == "delivery_partner":
        return handle_delivery_message(profile, message_text)

    else:
        return "Role not recognized. Please contact AgriLink Admin at support@agrilink.in."
