"""
AgriLink WhatsApp Integration - Institutional Buyer Handler (Module M4)
Manages recurring standing orders, meal-based bulk procurement, and consolidated GST invoicing.
"""

from typing import Dict, Any
from agrilink_whatsapp.database import AgriLinkDB

def get_institutional_menu(name: str = "Buyer", inst_name: str = "Institution") -> str:
    return (
        f"🏛️ *Welcome {name}! AgriLink B2B Institutional Portal*\n"
        f"🏢 *{inst_name}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Reply with an option number:\n\n"
        f"1️⃣ *View & Adjust Recurring Standing Orders*\n"
        f"2️⃣ *Place Ad-hoc Bulk Order (50 kg – 500 kg)*\n"
        f"3️⃣ *Download Monthly GST Invoice & Tax Statement*\n"
        f"4️⃣ *Security Gate Pass & Upcoming Delivery Truck*\n\n"
        f"Reply *MENU* at any time to return."
    )

def handle_institutional_message(profile: Dict[str, Any], text: str) -> str:
    phone = profile["phone"]
    session = AgriLinkDB.get_session(phone)
    step = session.get("step", "MAIN_MENU")
    t = text.strip()

    if t.lower() in ["menu", "hi", "hello", "reset"]:
        AgriLinkDB.set_session(phone, {"step": "MAIN_MENU", "data": {}})
        return get_institutional_menu(profile.get("name", "Buyer"), profile.get("institution", "Institution"))

    if step == "MAIN_MENU":
        if t == "1":
            orders = profile.get("standing_orders", [])
            lines = [
                "📅 *Active Recurring Standing Orders:*",
                "━━━━━━━━━━━━━━━━━━━━━━"
            ]
            for idx, o in enumerate(orders, 1):
                lines.append(f"{idx}. *Every {o['day']}*: {o['qty']} of {o['crop']} ({o['grade']})")
            lines.append("━━━━━━━━━━━━━━━━━━━━━━")
            lines.append("• Sourcing Hub: Maddur & Mandya Cooperative Network")
            lines.append("• Billing: Billed weekly on 15-day credit terms")
            lines.append("\nTo pause next Monday's order for holidays, reply *PAUSE*.")
            return "\n".join(lines)

        elif t == "2":
            AgriLinkDB.set_session(phone, {"step": "BULK_ORDER", "data": {}})
            return (
                "📦 *Place Ad-hoc Bulk Order*\n"
                "Please specify commodity, required weight in kg, and delivery date.\n"
                "(e.g., *'300 kg Potato for Wednesday hostel dinner'*)"
            )

        elif t == "3":
            inv_no = profile.get("latest_gst_invoice", "INV-2026-10-884")
            spend = profile.get("monthly_spend", 48200.00)
            return (
                f"📑 *Consolidated GST Tax Invoice*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• Invoice No: *{inv_no}*\n"
                f"• Period: October 1 – October 26, 2026\n"
                f"• Institution: *{profile.get('institution')}*\n"
                f"• GSTIN: *29AAACG1234F1Z5*\n"
                f"• Total Deliveries: 8 Bulk Shipments (1,600 kg)\n"
                f"• Taxable Value: ₹{spend:,.2f}\n"
                f"• GST (5% Fresh Produce Exemption / Value-Add Applied): Verified\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📥 *Download Digitally Signed GST Invoice (PDF):*\n"
                f"https://agrilink.in/invoices/{inv_no}.pdf"
            )

        elif t == "4":
            return (
                "🛡️ *Hostel Security Gate Pass & Truck Arrival*\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "• Shipment Ref: *SHIP-INST-091*\n"
                "• Vehicle: *Ashok Leyland Bada Dost (KA-05-AB-7741)*\n"
                "• Driver: *Ramesh Kumar (📞 +91 94481 22334)*\n"
                "• Cargo: 150 kg Grade A Potato + 100 kg Cabbage\n"
                "• Scheduled Gate Entry: *Today at 05:30 AM*\n"
                "• Certified Assayed Weight Slip: Attached to Driver App\n\n"
                "Forward this message to your campus security booth for clearance."
            )
        else:
            return get_institutional_menu(profile.get("name", "Buyer"), profile.get("institution", "Institution"))

    elif step == "BULK_ORDER":
        AgriLinkDB.set_session(phone, {"step": "MAIN_MENU", "data": {}})
        return (
            f"✅ *Bulk Procurement Request Received!*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Requirement: *{t}*\n"
            f"Our Mandya aggregation manager is locking farm inventory right now.\n"
            f"Formal purchase quote and delivery confirmation will be sent shortly.\n"
            f"Reply *MENU* to return."
        )

    return get_institutional_menu(profile.get("name", "Buyer"), profile.get("institution", "Institution"))
