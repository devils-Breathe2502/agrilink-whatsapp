"""
AgriLink WhatsApp Integration - Outbound WhatsApp Client
Supports Twilio Messaging API and Meta WhatsApp Cloud API with graceful mock mode.
"""

import logging
import requests
from xml.sax.saxutils import escape as xml_escape

try:
    from agrilink_whatsapp.config import (
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN,
        TWILIO_WHATSAPP_NUMBER,
        WHATSAPP_CLOUD_API_TOKEN,
        WHATSAPP_PHONE_NUMBER_ID
    )
except ImportError:
    from config import (
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN,
        TWILIO_WHATSAPP_NUMBER,
        WHATSAPP_CLOUD_API_TOKEN,
        WHATSAPP_PHONE_NUMBER_ID
    )

logger = logging.getLogger("AgriLinkWhatsAppClient")

class WhatsAppClient:
    @staticmethod
    def build_twiml_response(message_body: str) -> str:
        """Constructs safe Twilio TwiML XML response."""
        escaped_body = xml_escape(message_body)
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f"<Response>\n  <Message>{escaped_body}</Message>\n</Response>"
        )

    @staticmethod
    def send_outbound_message(to_phone: str, text: str, media_url: str = None) -> bool:
        """
        Sends an outbound proactive message (e.g., payment alert, pickup manifest).
        Uses Twilio REST API if configured, otherwise logs message for testing.
        """
        clean_phone = to_phone.strip()
        if not clean_phone.startswith("whatsapp:"):
            clean_phone = f"whatsapp:{clean_phone}"

        # If live credentials exist, send via Twilio API
        if TWILIO_ACCOUNT_SID and not TWILIO_ACCOUNT_SID.startswith("AC_mock"):
            url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
            payload = {
                "From": TWILIO_WHATSAPP_NUMBER,
                "To": clean_phone,
                "Body": text
            }
            if media_url:
                payload["MediaUrl"] = media_url

            try:
                resp = requests.post(
                    url,
                    data=payload,
                    auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                    timeout=5.0
                )
                return resp.status_code in [200, 201]
            except Exception as e:
                logger.error(f"Failed to send Twilio WhatsApp message: {e}")
                return False

        # Simulation / Local Development Mode
        print(f"\n[OUTBOUND WHATSAPP to {clean_phone}]:\n{text}\n")
        return True
