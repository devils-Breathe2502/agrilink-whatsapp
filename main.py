"""
AgriLink WhatsApp Integration - Meta Cloud API Server
Direct official integration with Meta (Facebook) WhatsApp Business Cloud API.
Zero third-party middlemen (No Twilio).
"""

import os
import sys
import json
from fastapi import FastAPI, Request, Response, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse

try:
    from config import WHATSAPP_VERIFY_TOKEN
    from router import route_inbound_whatsapp
    from services.meta_whatsapp_client import MetaWhatsAppClient
    from database import SEED_PROFILES, HARVEST_DECLARATIONS, DISPUTES
    from simulator_ui import get_simulator_html
except ImportError:
    from agrilink_whatsapp.config import WHATSAPP_VERIFY_TOKEN
    from agrilink_whatsapp.router import route_inbound_whatsapp
    from agrilink_whatsapp.services.meta_whatsapp_client import MetaWhatsAppClient
    from agrilink_whatsapp.database import SEED_PROFILES, HARVEST_DECLARATIONS, DISPUTES
    from agrilink_whatsapp.simulator_ui import get_simulator_html

app = FastAPI(
    title="AgriLink Meta WhatsApp Cloud API Service",
    description="Direct official Meta WhatsApp Cloud API gateway for Farmers, Aggregators, Customers & Logistics.",
    version="2.0.0"
)


# 1. WEB SIMULATOR & INTERFACE (for presentations & direct access)
@app.get("/", response_class=HTMLResponse)
@app.get("/demo", response_class=HTMLResponse)
async def web_simulator():
    return HTMLResponse(content=get_simulator_html(), status_code=200)


@app.get("/health")
@app.get("/api/v1/whatsapp/health")
async def health_check():
    return {
        "status": "healthy",
        "provider": "Meta WhatsApp Cloud API (Direct)",
        "registered_profiles": len(SEED_PROFILES),
        "logged_harvests": len(HARVEST_DECLARATIONS),
        "active_disputes": len(DISPUTES),
        "supported_languages": ["Kannada", "Hindi", "English", "Telugu"]
    }


# 2. META CLOUD API WEBHOOK VERIFICATION (GET HANDSHAKE)
@app.get("/webhook")
@app.get("/api/v1/whatsapp/webhook")
async def verify_meta_webhook(request: Request):
    """
    Meta Developer Portal verification handshake.
    Meta sends: hub.mode, hub.verify_token, hub.challenge
    """
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    print(f"\n[META VERIFICATION HANDSHAKE] Mode: {mode} | Token: {token}")

    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        print("✅ Meta Webhook Verification SUCCESSFUL!")
        return Response(content=challenge, media_type="text/plain")

    print("❌ Meta Webhook Verification FAILED - Token mismatch!")
    raise HTTPException(status_code=403, detail="Verification token mismatch")


# 3. META CLOUD API INBOUND WEBHOOK (POST MESSAGE RECEIVER)
@app.post("/webhook")
@app.post("/api/v1/whatsapp/webhook")
async def handle_meta_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Receives real incoming messages and voice notes from Meta WhatsApp Cloud API.
    """
    try:
        payload = await request.json()
        print(f"\n[META INBOUND RAW EVENT]: {json.dumps(payload)}")

        # Process message in background to reply to Meta with 200 OK within 2 seconds
        background_tasks.add_task(process_meta_event, payload)
        return Response(content="EVENT_RECEIVED", status_code=200)

    except Exception as e:
        print(f"[META WEBHOOK ERROR]: {e}")
        return Response(content="ERROR", status_code=200)


async def process_meta_event(payload: dict):
    """Background task to parse Meta WhatsApp message and send AgriLink reply."""
    try:
        values_to_process = []
        if "entry" in payload:
            for entry in payload.get("entry", []):
                for change in entry.get("changes", []):
                    val = change.get("value")
                    if val:
                        values_to_process.append(val)
        elif "value" in payload:
            values_to_process.append(payload.get("value"))

        if not values_to_process:
            print("[META WEBHOOK] No message values found in payload.")
            return

        for value in values_to_process:
            messages = value.get("messages", [])
            if not messages:
                continue

            msg = messages[0]
            from_phone = msg.get("from", "")  # e.g., '918800714533'
            msg_type = msg.get("type", "text")
            body = ""
            media_url = None
            media_content_type = None

            # Text Message
            if msg_type == "text":
                body = msg.get("text", {}).get("body", "")

            # Interactive Button Click
            elif msg_type == "interactive":
                interactive = msg.get("interactive", {})
                if interactive.get("type") == "button_reply":
                    body = interactive.get("button_reply", {}).get("id", "")
                elif interactive.get("type") == "list_reply":
                    body = interactive.get("list_reply", {}).get("id", "")

                # Voice Note / Audio
                elif msg_type == "audio":
                    media_id = msg.get("audio", {}).get("id")
                    media_url = MetaWhatsAppClient.get_media_url(media_id)
                    media_content_type = "audio/ogg"
                    body = "ಧ್ವನಿ ಸಂದೇಶ"  # voice note indicator

                # Image
                elif msg_type == "image":
                    media_id = msg.get("image", {}).get("id")
                    media_url = MetaWhatsAppClient.get_media_url(media_id)
                    media_content_type = "image/jpeg"
                    body = msg.get("image", {}).get("caption", "produce photo")

                print(f"[>>> REAL WHATSAPP] From: {from_phone} | Type: {msg_type} | Body: '{body}'")

                # Route message through AgriLink multi-actor engine
                reply_text = route_inbound_whatsapp(
                    from_phone=from_phone,
                    message_text=body,
                    media_url=media_url,
                    media_content_type=media_content_type
                )

                # Send response back to user via Meta Cloud API
                MetaWhatsAppClient.send_text_message(from_phone, reply_text)
                print(f"[<<< SENT REPLY] To: {from_phone} | Length: {len(reply_text)} chars")

    except Exception as e:
        print(f"[PROCESS META EVENT EXCEPTION]: {e}")
        import traceback
        traceback.print_exc()


# 4. SIMULATOR ENDPOINT (for browser testing)
@app.post("/api/v1/whatsapp/simulate")
async def simulate_message(request: Request):
    data = await request.json()
    from_phone = data.get("from_phone", "+919876500001")
    message = data.get("message", "")
    media_url = data.get("media_url")
    media_content_type = data.get("media_content_type")

    reply = route_inbound_whatsapp(
        from_phone=from_phone,
        message_text=message,
        media_url=media_url,
        media_content_type=media_content_type
    )
    return {"reply": reply, "from_phone": from_phone}
