"""
AgriLink WhatsApp Integration - Official Meta Cloud API Client
Direct communication with Meta WhatsApp Graph API v21.0.
"""

import logging
import requests
from typing import List, Dict, Any, Optional
from config import (
    WHATSAPP_CLOUD_API_TOKEN,
    WHATSAPP_PHONE_NUMBER_ID,
    META_GRAPH_URL
)

logger = logging.getLogger("MetaWhatsAppClient")

class MetaWhatsAppClient:
    @staticmethod
    def _get_headers() -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {WHATSAPP_CLOUD_API_TOKEN}",
            "Content-Type": "application/json"
        }

    @staticmethod
    def _clean_phone(phone: str) -> str:
        """Strips symbols like + or spaces for Meta format (e.g., 918800714533)."""
        return "".join(c for c in phone if c.isdigit())

    @classmethod
    def send_text_message(cls, to_phone: str, message_text: str) -> bool:
        """Sends a standard text message directly through Meta Cloud API."""
        if not WHATSAPP_CLOUD_API_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
            print(f"\n[META SIMULATION -> {to_phone}]:\n{message_text}\n")
            return True

        clean_number = cls._clean_phone(to_phone)
        url = f"{META_GRAPH_URL}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": clean_number,
            "type": "text",
            "text": {
                "preview_url": True,
                "body": message_text
            }
        }

        try:
            resp = requests.post(url, headers=cls._get_headers(), json=payload, timeout=8.0)
            if resp.status_code in [200, 201]:
                return True
            logger.error(f"Meta API Error ({resp.status_code}): {resp.text}")
            print(f"[META API ERROR] Status {resp.status_code}: {resp.text}")
            return False
        except Exception as e:
            logger.error(f"Failed to send Meta WhatsApp message: {e}")
            return False

    @classmethod
    def send_interactive_buttons(cls, to_phone: str, body_text: str, buttons: List[Dict[str, str]]) -> bool:
        """
        Sends native WhatsApp interactive quick-reply buttons (Max 3 buttons).
        Example: buttons = [{'id': 'btn_mandi', 'title': 'Mandi Rates'}, {'id': 'btn_sell', 'title': 'Sell Produce'}]
        """
        if not WHATSAPP_CLOUD_API_TOKEN or not WHATSAPP_PHONE_NUMBER_ID:
            print(f"\n[META BUTTONS SIMULATION -> {to_phone}]: {body_text} | Buttons: {buttons}\n")
            return True

        clean_number = cls._clean_phone(to_phone)
        url = f"{META_GRAPH_URL}/{WHATSAPP_PHONE_NUMBER_ID}/messages"

        button_elements = [
            {
                "type": "reply",
                "reply": {
                    "id": btn["id"],
                    "title": btn["title"][:20]  # Meta limit is 20 chars per button title
                }
            }
            for btn in buttons[:3]
        ]

        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": clean_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {"buttons": button_elements}
            }
        }

        try:
            resp = requests.post(url, headers=cls._get_headers(), json=payload, timeout=8.0)
            return resp.status_code in [200, 201]
        except Exception as e:
            logger.error(f"Failed to send interactive buttons: {e}")
            return False

    @classmethod
    def get_media_url(cls, media_id: str) -> Optional[str]:
        """Fetches the temporary download URL for incoming audio/voice notes from Meta."""
        if not WHATSAPP_CLOUD_API_TOKEN:
            return None
        url = f"{META_GRAPH_URL}/{media_id}"
        try:
            resp = requests.get(url, headers=cls._get_headers(), timeout=6.0)
            if resp.status_code == 200:
                return resp.json().get("url")
            return None
        except Exception:
            return None
