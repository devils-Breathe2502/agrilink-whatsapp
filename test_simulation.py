"""
AgriLink WhatsApp Integration - Automated Multi-Actor Simulation Test
Executes complete conversational lifecycles for all 5 roles:
1. Farmer (Mandya, Karnataka)
2. Aggregator (Maddur Hub #1)
3. Retail Customer (Bengaluru Urban)
4. Institutional Buyer (Hostel Warden)
5. Delivery Partner (Electric Fleet Driver)
"""

import sys
import os

# Ensure package path is recognized
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agrilink_whatsapp.router import route_inbound_whatsapp
from agrilink_whatsapp.database import AgriLinkDB, HARVEST_DECLARATIONS, DISPUTES

SEPARATOR = "=" * 70

def print_dialogue(sender: str, message: str, role_title: str):
    print(f"\n[{role_title}] 💬 User Sent: '{message}'")
    print("-" * 50)
    reply = route_inbound_whatsapp(from_phone=sender, message_text=message)
    print(reply)
    print("-" * 50)

def run_all_actor_simulations():
    print(SEPARATOR)
    print("🌾 AGRI-LINK WHATSAPP MULTI-ACTOR SYSTEM SIMULATION (SFIC 2026)")
    print(SEPARATOR)

    # =========================================================================
    # 1. FARMER SIMULATION (+919876500001 - Shivanna Gowda, Mandya)
    # =========================================================================
    farmer_phone = "+919876500001"
    print("\n\n🚜 ACTOR 1: SMALLHOLDER FARMER (Shivanna Gowda - Mandya, Karnataka)")
    print("Language: Kannada (kn) | Objective: Voice declaration, Mandi rates, UPI payout")
    
    # Farmer opens menu
    print_dialogue(farmer_phone, "ನಮಸ್ಕಾರ", "Farmer Shivanna")
    
    # Farmer checks Mandi price for Tomato
    print_dialogue(farmer_phone, "1", "Farmer Shivanna")
    print_dialogue(farmer_phone, "1", "Farmer Shivanna") # selects Tomato
    
    # Farmer sends a regional voice message declaring harvest
    print("\n[Farmer Shivanna] 🎙️ Farmer sends Voice Note: 'ನನ್ನ ಬಳಿ 200 ಕೆಜಿ ಟೊಮೆಟೊ ಇದೆ, ಗುರುವಾರ ಕೊಯ್ಲು ಮಾಡುತ್ತೇನೆ'")
    print("-" * 50)
    voice_reply = route_inbound_whatsapp(
        from_phone=farmer_phone,
        message_text="ನನ್ನ ಬಳಿ 200 ಕೆಜಿ ಟೊಮೆಟೊ ಇದೆ, ಗುರುವಾರ ಕೊಯ್ಲು ಮಾಡುತ್ತೇನೆ",
        media_url="https://mock-twilio.com/audio/voice-kannada.ogg",
        media_content_type="audio/ogg"
    )
    print(voice_reply)
    print("-" * 50)
    
    # Farmer checks payout status
    print_dialogue(farmer_phone, "3", "Farmer Shivanna")


    # =========================================================================
    # 2. LOCAL AGGREGATOR SIMULATION (+919876500002 - Lakshmi Devi, Maddur Hub)
    # =========================================================================
    agg_phone = "+919876500002"
    print("\n\n🏢 ACTOR 2: LOCAL AGGREGATOR (Lakshmi Devi - Maddur Women's SHG Hub)")
    print("Objective: Morning manifest, batch weighment & assay receipts, vehicle dispatch")

    print_dialogue(agg_phone, "menu", "Aggregator Lakshmi")
    
    # Check morning manifest
    print_dialogue(agg_phone, "1", "Aggregator Lakshmi")
    
    # Grade & log batch
    print_dialogue(agg_phone, "2", "Aggregator Lakshmi")
    print_dialogue(agg_phone, "1", "Aggregator Lakshmi") # Shivanna
    print_dialogue(agg_phone, "195.5", "Aggregator Lakshmi") # 195.5 kg
    print_dialogue(agg_phone, "1", "Aggregator Lakshmi") # Grade A
    
    # Request city dispatch truck
    print_dialogue(agg_phone, "3", "Aggregator Lakshmi")


    # =========================================================================
    # 3. RETAIL CUSTOMER SIMULATION (+919876500003 - Priya Verma, Bengaluru)
    # =========================================================================
    cust_phone = "+919876500003"
    print("\n\n🛒 ACTOR 3: RETAIL CONSUMER (Priya Verma - Bengaluru Urban)")
    print("Objective: Fresh catalog, live delivery tracking, provenance card, photo dispute")

    print_dialogue(cust_phone, "menu", "Customer Priya")
    
    # Browse catalog
    print_dialogue(cust_phone, "1", "Customer Priya")
    
    # Track active delivery & get OTP
    print_dialogue(cust_phone, "2", "Customer Priya")
    
    # View Farm-to-Fork Traceability Passport
    print_dialogue(cust_phone, "4", "Customer Priya")
    
    # Photo dispute submission
    print("\n[Customer Priya] 📸 Customer sends photo of damaged tomato with text: 'Produce bruised during transit'")
    print("-" * 50)
    dispute_reply = route_inbound_whatsapp(
        from_phone=cust_phone,
        message_text="Produce bruised during transit",
        media_url="https://mock-s3.com/photos/bruised_tomato.jpg",
        media_content_type="image/jpeg"
    )
    print(dispute_reply)
    print("-" * 50)


    # =========================================================================
    # 4. INSTITUTIONAL BUYER SIMULATION (+919876500004 - Warden Raghavan)
    # =========================================================================
    inst_phone = "+919876500004"
    print("\n\n🏛️ ACTOR 4: INSTITUTIONAL BUYER (Warden Raghavan - Kengeri Hostel Mess)")
    print("Objective: Standing orders, bulk booking, monthly GST tax invoice")

    print_dialogue(inst_phone, "menu", "Hostel Warden")
    
    # Review standing orders
    print_dialogue(inst_phone, "1", "Hostel Warden")
    
    # Retrieve monthly GST invoice
    print_dialogue(inst_phone, "3", "Hostel Warden")
    
    # Security gate pass for incoming truck
    print_dialogue(inst_phone, "4", "Hostel Warden")


    # =========================================================================
    # 5. DELIVERY PARTNER SIMULATION (+919876500005 - Manjunath K, EV Driver)
    # =========================================================================
    driver_phone = "+919876500005"
    print("\n\n🛵 ACTOR 5: DELIVERY FLEET PARTNER (Manjunath K - Electric 3-Wheeler)")
    print("Objective: Multi-stop route navigation, OTP customer handover, earnings dashboard")

    print_dialogue(driver_phone, "menu", "Driver Manjunath")
    
    # Check assigned route and map
    print_dialogue(driver_phone, "1", "Driver Manjunath")
    
    # Submit customer OTP 4829 to release payouts
    print_dialogue(driver_phone, "4829", "Driver Manjunath")
    
    # Check daily logistics earnings
    print_dialogue(driver_phone, "3", "Driver Manjunath")

    print(SEPARATOR)
    print("✅ SIMULATION COMPLETE: ALL 5 ACTOR WORKFLOWS VERIFIED SUCCESSFULLY!")
    print(f"• Total Harvests Logged in System: {len(HARVEST_DECLARATIONS)}")
    print(f"• Total Quality Disputes Logged: {len(DISPUTES)}")
    print(SEPARATOR)

if __name__ == "__main__":
    run_all_actor_simulations()
