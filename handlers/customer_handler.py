"""
AgriLink WhatsApp Integration - Retail Customer Handler (Modules M3, M6, M10, M11, M12)
Manages conversational fresh produce ordering, live order tracking, and farm provenance passports.
"""

from typing import Dict, Any, Optional

try:
    from agrilink_whatsapp.database import AgriLinkDB, FRESH_CATALOG
    from agrilink_whatsapp.services.traceability_service import TraceabilityService
except ImportError:
    from database import AgriLinkDB, FRESH_CATALOG
    from services.traceability_service import TraceabilityService

def get_customer_menu(name: str = "Customer") -> str:
    return (
        f"🌿 *Hello {name}! Welcome to AgriLink Farm-Fresh Marketplace*\n"
        f"Direct from Mandya farms to your doorstep in 12–24 hours.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Reply with an option number:\n\n"
        f"1️⃣ *Browse Today's Fresh Harvest Catalog*\n"
        f"2️⃣ *Track Active Order & View Delivery OTP*\n"
        f"3️⃣ *1-Click Reorder (Last Week's Family Basket)*\n"
        f"4️⃣ *View Farm Traceability Passport (Order #ORD-98721)*\n"
        f"5️⃣ *Report Quality Issue / Upload Photo Dispute*\n\n"
        f"Reply *MENU* at any time to return."
    )

def handle_customer_message(profile: Dict[str, Any], text: str, photo_url: Optional[str] = None) -> str:
    phone = profile["phone"]
    session = AgriLinkDB.get_session(phone)
    step = session.get("step", "MAIN_MENU")
    t = text.strip()

    if t.lower() in ["menu", "hi", "hello", "reset"]:
        AgriLinkDB.set_session(phone, {"step": "MAIN_MENU", "data": {}})
        return get_customer_menu(profile.get("name", "Customer"))

    # If customer uploads a photo of damaged produce
    if photo_url or step == "AWAITING_DISPUTE":
        dispute = AgriLinkDB.log_quality_dispute(
            customer_phone=phone,
            order_id="ORD-98721",
            issue_text=text or "Produce bruised or damaged upon arrival",
            photo_url=photo_url
        )
        AgriLinkDB.set_session(phone, {"step": "MAIN_MENU", "data": {}})
        return (
            f"🛡️ *Quality Dispute Ticket Registered!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Ticket ID: *{dispute['id']}*\n"
            f"Order ID: *ORD-98721*\n"
            f"Status: *Instant Refund / Replacement Approved*\n\n"
            f"We are sorry for the inconvenience. A credit of ₹38.00 has been applied to your AgriLink wallet.\n"
            f"Reply *MENU* to continue."
        )

    if step == "MAIN_MENU":
        if t == "1":
            lines = [
                "🥬 *Today's Farm-Harvested Arrivals (100% Traceable):*",
                "━━━━━━━━━━━━━━━━━━━━━━"
            ]
            for idx, item in enumerate(FRESH_CATALOG, 1):
                lines.append(
                    f"{idx}. *{item['name']}*\n"
                    f"   • Price: ₹{item['price_per_kg']:.2f}/kg\n"
                    f"   • Direct Farmer Payout (68%): *₹{item['farmer_payout']:.2f}*\n"
                    f"   • Origin: {item['origin']} Farm Cluster"
                )
            lines.append("━━━━━━━━━━━━━━━━━━━━━━")
            lines.append("Reply with item number to add to cart, or *3* to reorder your usual basket.")
            return "\n".join(lines)

        elif t == "2":
            orders = profile.get("active_orders", [])
            if not orders:
                return "You have no active deliveries in transit right now. Reply *1* to browse fresh produce."
            o = orders[0]
            return (
                f"🚚 *Live Delivery Tracking: {o['order_id']}*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• Status: *OUT FOR DELIVERY*\n"
                f"• Items: {', '.join(o['items'])}\n"
                f"• Estimated Arrival: *Within {o['eta']}*\n"
                f"• Delivery Driver: *{o['driver_name']}* (📞 {o['driver_phone']})\n"
                f"• Vehicle: Eco-Friendly Electric 3-Wheeler\n\n"
                f"🔑 *Your Delivery Handover OTP:* *{o['otp']}*\n"
                f"_(Share this 4-digit OTP with the driver only upon handover)_\n\n"
                f"Reply *4* to view the farm origin passport for this order."
            )

        elif t == "3":
            basket = profile.get("last_basket", ["Tomatoes", "Onion", "Palak"])
            return (
                f"🛒 *1-Click Fresh Basket Reorder Confirmed!*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Items from your favorite Mandya farms:\n"
                f"• " + "\n• ".join(basket) + "\n\n"
                f"• Subtotal: ₹182.50\n"
                f"• Delivery Fee: ₹0.00 (AgriLink Fresh Pass)\n"
                f"• *Total: ₹182.50 (Farmer Share 68%: ₹124.10)*\n\n"
                f"💳 *Pay via UPI:* https://agrilink.in/pay/ORD-98750?upi=1\n"
                f"Delivery scheduled for tomorrow morning between 07:00 AM – 09:00 AM."
            )

        elif t == "4":
            return TraceabilityService.generate_customer_provenance_card(order_id="ORD-98721", crop="Tomato")

        elif t == "5":
            AgriLinkDB.set_session(phone, {"step": "AWAITING_DISPUTE", "data": {}})
            return (
                "📸 *Quality Dispute & Guarantee*\n"
                "Please describe the issue or reply directly with a *photo of the damaged produce*. Our team will process a no-questions-asked refund or replacement immediately."
            )
        else:
            return get_customer_menu(profile.get("name", "Customer"))

    return get_customer_menu(profile.get("name", "Customer"))
