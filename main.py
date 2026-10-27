"""
AgriLink WhatsApp Integration - Main FastAPI Server
Serves production webhooks for Twilio WhatsApp and Meta Cloud API.
"""

import os
import sys
import json
import urllib.parse
from fastapi import FastAPI, Request, Response, HTTPException

# Ensure local imports work whether run from repo root or package root
try:
    from agrilink_whatsapp.config import WHATSAPP_VERIFY_TOKEN
    from agrilink_whatsapp.router import route_inbound_whatsapp
    from agrilink_whatsapp.services.whatsapp_client import WhatsAppClient
    from agrilink_whatsapp.database import SEED_PROFILES, HARVEST_DECLARATIONS, DISPUTES
except ImportError:
    from config import WHATSAPP_VERIFY_TOKEN
    from router import route_inbound_whatsapp
    from services.whatsapp_client import WhatsAppClient
    from database import SEED_PROFILES, HARVEST_DECLARATIONS, DISPUTES

app = FastAPI(
    title="AgriLink WhatsApp Integration Service",
    description="Multi-actor WhatsApp conversational gateway for Farmers, Aggregators, Customers, Institutions & Fleet.",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "project": "AgriLink - Farm-to-Consumer Digital Marketplace",
        "service": "WhatsApp Conversational Gateway (SFIC 2026)",
        "status": "ONLINE",
        "actors_supported": ["Farmer", "Aggregator", "Customer", "Institutional Buyer", "Delivery Partner"],
        "pricing_engine": "68-10-14-8 Split Active"
    }


@app.get("/health")
@app.get("/api/v1/whatsapp/health")
async def health_check():
    return {
        "status": "healthy",
        "registered_profiles": len(SEED_PROFILES),
        "logged_harvests": len(HARVEST_DECLARATIONS),
        "active_disputes": len(DISPUTES),
        "supported_languages": ["Kannada", "Hindi", "English", "Telugu"]
    }


# 1. Meta WhatsApp Cloud API Verification Handshake
@app.get("/api/v1/whatsapp/webhook")
async def verify_meta_webhook(request: Request):
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification token mismatch")


# 2. Universal Inbound Webhook (Twilio & Meta Cloud API)
@app.post("/")
@app.post("/api/v1/whatsapp/webhook")
async def handle_whatsapp_webhook(request: Request):
    content_type = request.headers.get("content-type", "").lower()
    raw_body = await request.body()
    print(f"\n[>>> INCOMING REQUEST] Content-Type: {content_type}, Body bytes: {len(raw_body)}")

    # Case A: Twilio Webhook (application/x-www-form-urlencoded)
    if "form" in content_type or b"From=" in raw_body or b"Body=" in raw_body:
        try:
            parsed_data = urllib.parse.parse_qs(raw_body.decode("utf-8"))
            from_phone = parsed_data.get("From", [""])[0]
            message_body = parsed_data.get("Body", [""])[0]
            media_url = parsed_data.get("MediaUrl0", [None])[0]
            media_content_type = parsed_data.get("MediaContentType0", [None])[0]

            print(f"[>>> TWILIO MESSAGE] From: {from_phone} | Body: '{message_body}'")

            # Route through AgriLink multi-actor engine
            reply_text = route_inbound_whatsapp(
                from_phone=from_phone,
                message_text=message_body,
                media_url=media_url,
                media_content_type=media_content_type
            )

            print(f"[<<< SENDING REPLY] To: {from_phone} | Length: {len(reply_text)} chars")

            # Return valid Twilio TwiML
            twiml = WhatsAppClient.build_twiml_response(reply_text)
            return Response(content=twiml, media_type="text/xml")
        except Exception as e:
            print(f"[!!! ERROR IN TWILIO WEBHOOK]: {e}")
            import traceback
            traceback.print_exc()
            return Response(content=f"<Response><Message>AgriLink Bot Error: {e}</Message></Response>", media_type="text/xml")

    # Case B: Meta Cloud API Webhook (application/json)
    elif "json" in content_type:
        try:
            payload = json.loads(raw_body.decode("utf-8"))
            entry = payload.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])

            if messages:
                msg = messages[0]
                from_phone = msg.get("from", "")
                msg_type = msg.get("type", "text")
                body = msg.get("text", {}).get("body", "") if msg_type == "text" else ""

                reply_text = route_inbound_whatsapp(from_phone, body)
                WhatsAppClient.send_outbound_message(from_phone, reply_text)

            return {"status": "processed"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    return Response(content="<Response/>", media_type="text/xml")


# 3. Outbound Proactive Alert Dispatcher (Called by Spring Boot / Order Services)
@app.post("/api/v1/whatsapp/send-alert")
async def send_proactive_alert(request: Request):
    body = await request.json()
    to_phone = body.get("to_phone")
    message = body.get("message")
    media_url = body.get("media_url")

    if not to_phone or not message:
        raise HTTPException(status_code=400, detail="Missing to_phone or message")

    success = WhatsAppClient.send_outbound_message(to_phone, message, media_url)
    return {"status": "sent" if success else "failed", "recipient": to_phone}
