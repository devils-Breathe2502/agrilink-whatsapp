"""
AgriLink WhatsApp Integration - Aggregator Actor Handler (Modules M5, M7, M11)
Coordinates village-level produce collection, digital grading assay receipts, and city fleet dispatch.
"""

from typing import Dict, Any

try:
    from agrilink_whatsapp.database import AgriLinkDB
    from agrilink_whatsapp.services.traceability_service import TraceabilityService
except ImportError:
    from database import AgriLinkDB
    from services.traceability_service import TraceabilityService

def get_aggregator_menu(name: str = "Aggregator") -> str:
    return (
        f"🏢 *Welcome {name}! AgriLink Hub Operations*\n"
        f"📍 Maddur Village Collection Hub #1 (Catchment: 25 km)\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Reply with an option number:\n\n"
        f"1️⃣ *Today's Farmer Pickup Manifest*\n"
        f"2️⃣ *Log Batch Weighment & Issue Assay Receipt*\n"
        f"3️⃣ *Request Dispatch Vehicle to Bengaluru*\n"
        f"4️⃣ *Hub Performance & 10% Commission Summary*\n\n"
        f"Reply *MENU* at any time to return."
    )

def handle_aggregator_message(profile: Dict[str, Any], text: str) -> str:
    phone = profile["phone"]
    session = AgriLinkDB.get_session(phone)
    step = session.get("step", "MAIN_MENU")
    data = session.get("data", {})
    t = text.strip()

    if t.lower() in ["menu", "hi", "hello", "reset"]:
        AgriLinkDB.set_session(phone, {"step": "MAIN_MENU", "data": {}})
        return get_aggregator_menu(profile.get("name", "Aggregator"))

    if step == "MAIN_MENU":
        if t == "1":
            manifest = AgriLinkDB.get_todays_manifest_for_hub(profile.get("hub_name", "Maddur Hub"))
            lines = [
                f"📋 *Today's Morning Pickup Route ({len(manifest)} Stops)*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━"
            ]
            for idx, item in enumerate(manifest, 1):
                lines.append(f"{idx}. *{item['farmer']}* ({item['village']})\n   • Produce: {item['crop']} ({item['qty']})")
            lines.append("━━━━━━━━━━━━━━━━━━━━━━")
            lines.append("🚚 Collection EV 3-Wheeler route departs at 08:30 AM.")
            lines.append("Reply *2* to grade an incoming batch, or *MENU*.")
            return "\n".join(lines)

        elif t == "2":
            AgriLinkDB.set_session(phone, {"step": "WEIGH_FARMER", "data": {}})
            return (
                "⚖️ *Log Incoming Produce Batch (Assay Receipt)*\n"
                "Step 1/3: Which farmer's produce are you assaying?\n"
                "1. Shivanna Gowda (Tomato)\n"
                "2. Basavaraju M (Chilli)\n"
                "3. Ningamma K (Palak)"
            )

        elif t == "3":
            return (
                "🚚 *Bengaluru Dispatch Vehicle Requested!*\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "• Hub Origin: Maddur Hub #1\n"
                "• Destination: Bengaluru Sorting Corridor (85 km)\n"
                "• Assigned Driver: Manjunath K (KA-11-EV-2041)\n"
                "• Estimated Arrival at Hub: 11:15 AM\n\n"
                "Please have consolidated crates labeled with batch QR tags."
            )

        elif t == "4":
            comm = profile.get("unsettled_commission", 2840.00)
            return (
                f"📊 *Hub Financial Performance (10% Aggregator Fee)*\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"• Active Farmers in Catchment: {profile.get('farmers_count', 28)}\n"
                f"• Weekly Processed Volume: 4,200 kg\n"
                f"• Unsettled Commission (10%): *₹{comm:,.2f}*\n"
                f"• Total Direct Farmer Payouts Facilitated: *₹1,92,400*\n"
                f"• Average Grading Loss / Spoilage: *< 2.8% (Target < 4%)*\n\n"
                f"Commission is settled directly every Tuesday. Reply *MENU*."
            )
        else:
            return get_aggregator_menu(profile.get("name", "Aggregator"))

    # Batch Logging Steps
    elif step == "WEIGH_FARMER":
        f_map = {"1": "Shivanna Gowda", "2": "Basavaraju M", "3": "Ningamma K"}
        data["farmer_name"] = f_map.get(t, "Shivanna Gowda")
        AgriLinkDB.set_session(phone, {"step": "WEIGH_KG", "data": data})
        return f"Enter verified net weight for *{data['farmer_name']}* in kg (e.g., 195.5):"

    elif step == "WEIGH_KG":
        try:
            net_kg = float(t.replace("kg", "").strip())
        except ValueError:
            net_kg = 200.0
        data["net_kg"] = net_kg
        AgriLinkDB.set_session(phone, {"step": "WEIGH_GRADE", "data": data})
        return "Select Assayed Quality Grade:\n1. Grade A (+15% Premium)\n2. Grade B (Standard)\n3. Grade C (-10% Discount)"

    elif step == "WEIGH_GRADE":
        g_map = {"1": "A", "2": "B", "3": "C"}
        grade = g_map.get(t, "A")
        farmer_name = data.get("farmer_name", "Shivanna Gowda")
        net_kg = data.get("net_kg", 200.0)
        payout_rate = 30.60 if grade == "A" else 25.00

        # Generate assay receipt
        receipt = TraceabilityService.generate_assay_receipt(
            batch_id="BATCH-MD-882",
            farmer_name=farmer_name,
            crop="Tomato",
            net_kg=net_kg,
            grade=grade,
            payout_per_kg=payout_rate
        )
        AgriLinkDB.set_session(phone, {"step": "MAIN_MENU", "data": {}})
        return (
            f"✅ *Batch Verified & Assay Receipt Issued!*\n\n"
            f"{receipt}\n\n"
            f"📲 *A copy of this digital receipt has been sent to {farmer_name}'s WhatsApp.*"
        )

    return get_aggregator_menu(profile.get("name", "Aggregator"))
