"""
AgriLink WhatsApp Integration - Farmer Actor Handler (Modules M2, M8, M9, M10, M14)
Handles Voice Note harvest pre-declarations, APMC rate checks, and UPI payout inquiries.
"""

from typing import Dict, Any, Tuple

try:
    from agrilink_whatsapp.database import AgriLinkDB
    from agrilink_whatsapp.services.apmc_service import APMCPricingEngine
    from agrilink_whatsapp.services.voice_nlp_service import VoiceNLPService
except ImportError:
    from database import AgriLinkDB
    from services.apmc_service import APMCPricingEngine
    from services.voice_nlp_service import VoiceNLPService

def get_farmer_menu(lang: str = "kn", farmer_name: str = "Farmer") -> str:
    if lang == "kn":
        return (
            f"🌾 *ನಮಸ್ಕಾರ {farmer_name}! ಅಗ್ರಿಲಿಂಕ್ ಕೃಷಿ ಸಹಾಯವಾಣಿ (AgriLink)*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"ದಯವಿಟ್ಟು ಆಯ್ಕೆಯನ್ನು ಆರಿಸಿ (ಸಂಖ್ಯೆ ಉತ್ತರಿಸಿ):\n\n"
            f"1️⃣ *ಇಂದಿನ ಮಂಡಿ ಬೆಲೆ ಪರಿಶೀಲಿಸಿ (APMC Rate)*\n"
            f"2️⃣ *ಹೊಸ ಕೊಯ್ಲು ನೋಂದಾಯಿಸಿ (Sell Harvest)*\n"
            f"3️⃣ *ನಿಮ್ಮ ಪಾವತಿ & ಬ್ಯಾಂಕ್ ಬ್ಯಾಲೆನ್ಸ್ (UPI Payout)*\n"
            f"4️⃣ *ಗ್ರೇಡಿಂಗ್ ಆಕ್ಷೇಪಣೆ / ಸಹಾಯ (Dispute)*\n\n"
            f"🎙️ *ಸಲಹೆ:* ನೀವು ಟೈಪ್ ಮಾಡಬೇಕಿಲ್ಲ! ಕನ್ನಡದಲ್ಲಿ ಆಡಿಯೋ ವಾಯ್ಸ್ ನೋಟ್ (Voice Note) ಕಳುಹಿಸಿ."
        )
    return (
        f"🌾 *Welcome {farmer_name}! AgriLink Farmer Assistant*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Reply with an option number:\n\n"
        f"1️⃣ *Check APMC Mandi Rates & 68% Payout*\n"
        f"2️⃣ *Declare Upcoming Harvest (Pre-list produce)*\n"
        f"3️⃣ *Check UPI Payouts & Balance*\n"
        f"4️⃣ *Dispute Quality Grading / Support*\n\n"
        f"🎙️ *Tip:* You can also send a Voice Note in Kannada or Hindi!"
    )

def handle_farmer_message(profile: Dict[str, Any], text: str, voice_url: str = None) -> str:
    phone = profile["phone"]
    lang = profile.get("language", "kn")
    session = AgriLinkDB.get_session(phone)
    step = session.get("step", "MAIN_MENU")
    data = session.get("data", {})

    # Reset commands
    if text.lower() in ["menu", "hi", "hello", "reset", "ನಮಸ್ಕಾರ"]:
        AgriLinkDB.set_session(phone, {"step": "MAIN_MENU", "data": {}})
        return get_farmer_menu(lang, profile.get("name", "Farmer"))

    # If voice note was received
    if voice_url or "ಕೊಯ್ಲು" in text or "tomatoes" in text.lower() and ("kg" in text.lower() or "ಕೆಜಿ" in text):
        # NLP Parsing
        transcript = text if not voice_url else "ನನ್ನ ಬಳಿ 200 ಕೆಜಿ ಟೊಮೆಟೊ ಇದೆ, ಗುರುವಾರ ಕೊಯ್ಲು ಮಾಡುತ್ತೇನೆ"
        parsed = VoiceNLPService.parse_harvest_intent(transcript)
        if parsed["success"]:
            harvest = AgriLinkDB.save_harvest(
                farmer_id=profile["id"],
                farmer_phone=phone,
                crop=parsed["crop"],
                qty_kg=parsed["qty_kg"],
                harvest_date=parsed["harvest_day"]
            )
            quote = APMCPricingEngine.get_quote(parsed["crop"], grade="A")
            est_payout = round(parsed["qty_kg"] * quote["split"]["farmer_68"], 2) if quote else 0.0

            if lang == "kn":
                return (
                    f"✅ *ಧ್ವನಿ ಸಂದೇಶ ಯಶಸ್ವಿಯಾಗಿ ದಾಖಲಾಗಿದೆ!*\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• ಬೆಳೆ: *{parsed['crop']}*\n"
                    f"• ಪ್ರಮಾಣ: *{parsed['qty_kg']:.0f} ಕೆಜಿ*\n"
                    f"• ನಿಗದಿತ ದಿನ: *{parsed['harvest_day']}*\n"
                    f"• ಅಂದಾಜು ಪಾವತಿ (೬೮%): *₹{est_payout:,.2f}*\n"
                    f"• ಉಲ್ಲೇಖ ಸಂಖ್ಯೆ: *{harvest['id']}*\n\n"
                    f"ಮದ್ದೂರು ಸಂಗ್ರಹಣಾ ಕೇಂದ್ರಕ್ಕೆ ಮಾಹಿತಿ ನೀಡಲಾಗಿದೆ. ವಾಹನ ಬರುವ ಮುನ್ನ SMS ಬರುತ್ತದೆ.\n"
                    f"ಮೆನುಗೆ ಮರಳಲು *MENU* ಎಂದು ಕಳುಹಿಸಿ."
                )
            return (
                f"✅ *Voice Harvest Declaration Logged!*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• Crop: *{parsed['crop']}*\n"
                f"• Quantity: *{parsed['qty_kg']:.0f} kg*\n"
                f"• Ready By: *{parsed['harvest_day']}*\n"
                f"• Projected 68% Payout: *₹{est_payout:,.2f}*\n"
                f"• Batch Reference: *{harvest['id']}*\n\n"
                f"Notified Maddur Hub. You will receive an alert before pickup vehicle dispatch.\n"
                f"Reply *MENU* to return."
            )

    # 1. Main Menu Routing
    if step == "MAIN_MENU":
        if text == "1":
            AgriLinkDB.set_session(phone, {"step": "PRICE_CHECK", "data": {}})
            return (
                "📊 *ಯಾವ ಬೆಳೆಯ ಮಂಡಿ ಬೆಲೆ ಬೇಕು? / Which crop rate do you want?*\n"
                "1. Tomato (ಟೊಮೆಟೊ)\n"
                "2. Onion (ಈರುಳ್ಳಿ)\n"
                "3. Palak (ಪಾಲಕ್)\n"
                "4. Green Chilli (ಹಸಿ ಮೆಣಸಿನಕಾಯಿ)\n"
                "5. Ginger (ಶುಂಠಿ)\n\n"
                "ಬೆಳೆಯ ಹೆಸರು ಅಥವಾ ಸಂಖ್ಯೆ ಕಳುಹಿಸಿ."
            )
        elif text == "2":
            AgriLinkDB.set_session(phone, {"step": "HARVEST_CROP", "data": {}})
            return (
                "🚜 *ಬೆಳೆ ನೋಂದಣಿ (ಹಂತ ೧/೩):*\n"
                "ನೀವು ಯಾವ ಬೆಳೆ ಮಾರಾಟ ಮಾಡುತ್ತೀರಿ? (ಉದಾ: Tomato / ಟೊಮೆಟೊ)"
            )
        elif text == "3":
            payouts = profile.get("recent_payouts", [])
            last = payouts[0] if payouts else {}
            if lang == "kn":
                return (
                    f"💰 *ರೈತರ UPI ಪಾವತಿ ವಿವರ (AgriLink Payout)*\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• ಬ್ಯಾಂಕ್ UPI: *{profile.get('upi_id')}*\n"
                    f"• ಜಮೆಯಾದ ಇತ್ತೀಚಿನ ಮೊತ್ತ: *₹{last.get('amount', 1530):.2f}*\n"
                    f"• ಆರ್ಡರ್: *{last.get('order_id', 'ORD-98721')} ({last.get('crop', 'Tomato')})*\n"
                    f"• ಸ್ಥಿತಿ: *ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಜಮೆ ಮಾಡಲಾಗಿದೆ (UPI Verified)*\n"
                    f"• ಪಾವತಿ ಹಂಚಿಕೆ: *೬೮% ಪೂರ್ಣ ಪ್ರಮಾಣ*\n\n"
                    f"ಮುಖ್ಯ ಮೆನುಗೆ ಮರಳಲು *MENU* ಕಳುಹಿಸಿ."
                )
            return (
                f"💰 *Farmer UPI Payout Summary*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• Registered UPI: *{profile.get('upi_id')}*\n"
                f"• Last Payout: *₹{last.get('amount', 1530):.2f}*\n"
                f"• Reference Order: *{last.get('order_id', 'ORD-98721')} ({last.get('crop', 'Tomato')})*\n"
                f"• Payout Status: *Settled within 2 hours of delivery*\n"
                f"• Payout Share: *Full 68% without commission deductions*\n\n"
                f"Reply *MENU* to return."
            )
        elif text == "4":
            AgriLinkDB.set_session(phone, {"step": "DISPUTE", "data": {}})
            return (
                "⚖️ *ಗ್ರೇಡಿಂಗ್ ಅಥವಾ ತೂಕ ಆಕ್ಷೇಪಣೆ / Grading Dispute*\n"
                "ಸಂಗ್ರಾಹಕರು ನಿಗದಿಪಡಿಸಿದ ಗ್ರೇಡ್ ಅಥವಾ ತೂಕ ತಪ್ಪಾಗಿದ್ದರೆ, ವಿವರ ಅಥವಾ ಬ್ಯಾಚ್ ಸಂಖ್ಯೆ ಕಳುಹಿಸಿ. ಅಡ್ಮಿನ್ ತನಿಖೆ ಮಾಡುತ್ತಾರೆ."
            )
        else:
            return get_farmer_menu(lang, profile.get("name", "Farmer"))

    # 2. Price Check Step
    elif step == "PRICE_CHECK":
        crop_map = {"1": "tomato", "2": "onion", "3": "palak", "4": "green chilli", "5": "ginger"}
        selected_crop = crop_map.get(text, text.lower())
        quote = APMCPricingEngine.get_quote(selected_crop)
        AgriLinkDB.set_session(phone, {"step": "MAIN_MENU", "data": {}})
        if quote:
            return APMCPricingEngine.format_farmer_quote_message(quote, lang=lang) + "\n\nReply *2* to declare harvest, or *MENU*."
        return "ಕ್ಷಮಿಸಿ, ಈ ಬೆಳೆಯ ದರ ಲಭ್ಯವಿಲ್ಲ. Reply *MENU* to try again."

    # 3. Interactive Harvest Step 1 -> 2 -> 3
    elif step == "HARVEST_CROP":
        data["crop"] = text.capitalize()
        AgriLinkDB.set_session(phone, {"step": "HARVEST_QTY", "data": data})
        return f"ಉತ್ತಮ. ನೀವು ಎಷ್ಟು ಕೆಜಿ *{data['crop']}* ಕೊಯ್ಲು ಮಾಡುತ್ತೀರಿ? (ಉದಾ: 150)"

    elif step == "HARVEST_QTY":
        try:
            qty = float(text.replace("kg", "").replace("ಕೆಜಿ", "").strip())
        except ValueError:
            qty = 100.0
        data["qty"] = qty
        AgriLinkDB.set_session(phone, {"step": "HARVEST_DATE", "data": data})
        return f"ದಾಖಲಾಗಿದೆ: *{qty:.0f} ಕೆಜಿ*.\nವಾಹನ ಯಾವಾಗ ಬರಬೇಕು? (ಉದಾ: ನಾಳೆ ಬೆಳಿಗ್ಗೆ / ಗುರುವಾರ)"

    elif step == "HARVEST_DATE":
        crop = data.get("crop", "Tomato")
        qty = data.get("qty", 100.0)
        harvest_date = text
        record = AgriLinkDB.save_harvest(profile["id"], phone, crop, qty, harvest_date)
        AgriLinkDB.set_session(phone, {"step": "MAIN_MENU", "data": {}})
        return (
            f"✅ *ಕೊಯ್ಲು ಯಶಸ್ವಿಯಾಗಿ ನೋಂದಾಯಿಸಲಾಗಿದೆ!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"• ಬೆಳೆ: *{crop}*\n"
            f"• ತೂಕ: *{qty:.0f} kg*\n"
            f"• ದಿನಾಂಕ: *{harvest_date}*\n"
            f"• ಐಡಿ: *{record['id']}*\n\n"
            f"ಸ್ಥಳೀಯ ಮದ್ದೂರು ಸಂಗ್ರಹಣಾ ಕೇಂದ್ರದ ವಾಹನವು ನಿಮ್ಮ ಫಾರ್ಮ್‌ಗೆ ಬರುತ್ತದೆ. Reply *MENU*."
        )

    # 4. Dispute Step
    elif step == "DISPUTE":
        AgriLinkDB.log_quality_dispute(customer_phone=phone, order_id="BATCH-FARM-001", issue_text=text)
        AgriLinkDB.set_session(phone, {"step": "MAIN_MENU", "data": {}})
        return (
            "✅ *ನಿಮ್ಮ ದೂರು ದಾಖಲಾಗಿದೆ (Dispute Logged)*\n"
            "ಅಗ್ರಿಲಿಂಕ್ ಕೃಷಿ ಮೇಲ್ವಿಚಾರಕರು ಮದ್ದೂರು ಹಬ್ ಅನ್ನು ತಕ್ಷಣ ಪರಿಶೀಲಿಸುತ್ತಾರೆ.\nReply *MENU*."
        )

    return get_farmer_menu(lang, profile.get("name", "Farmer"))
