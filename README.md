# 🌾 AgriLink WhatsApp Omnichannel Integration
**Farm-to-Consumer Digital Marketplace (Seva First Innovation Challenge 2026)**

This module provides a unified WhatsApp conversational gateway tailored for all 5 AgriLink actors:
1. **Farmer** (Mandya, Karnataka) — Regional voice notes, APMC mandi rates, UPI payouts.
2. **Local Aggregator** (Maddur SHG Hub) — Pickup manifests, weighment logging & digital assay receipts.
3. **Retail Customer** (Bengaluru) — Catalog discovery, live tracking, OTP, farm provenance cards, photo disputes.
4. **Institutional Buyer** (Hostel/Hospital) — Standing orders, ad-hoc bulk orders, monthly GST invoices.
5. **Delivery Partner** (Electric 3-Wheeler) — Multi-stop route navigation, OTP handovers, daily 14% logistics payouts.

---

## 📂 Project Structure

```text
agrilink_whatsapp/
├── config.py                  # Credentials, business split ratios (68-10-14-8), languages
├── database.py                # Data access layer with Supabase integration & realistic seed data
├── schema.sql                 # Master PostgreSQL / Supabase schema with RLS & PostGIS
├── main.py                    # Production FastAPI server & universal webhooks
├── router.py                  # Omnichannel actor dispatcher
├── services/
│   ├── apmc_service.py        # Dynamic pricing engine (APMC rates + grade multipliers)
│   ├── voice_nlp_service.py   # Regional speech transcription & entity extraction (Kannada/Hindi)
│   ├── traceability_service.py# Farm provenance passports (M11) & digital assay receipts
│   └── whatsapp_client.py     # Twilio & Meta Cloud API outbound messaging
├── handlers/
│   ├── farmer_handler.py      # Actor 1: Voice harvest declarations & mandi rates
│   ├── aggregator_handler.py  # Actor 2: Collection manifests & hub logging
│   ├── customer_handler.py    # Actor 3: Conversational commerce & photo disputes
│   ├── institutional_handler.py# Actor 4: Standing orders & GST tax invoicing
│   └── delivery_handler.py    # Actor 5: Multi-stop fleet routing & OTP release
├── test_simulation.py         # Automated simulation of all 5 actor lifecycles
├── requirements.txt           # Python dependencies
└── .env.example               # Environment variables template
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and add your Twilio or Meta Cloud API credentials.

### 3. Run FastAPI WhatsApp Gateway
```bash
uvicorn agrilink_whatsapp.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Connect to WhatsApp via Ngrok
```bash
ngrok http 8000
```
- In the **Twilio Console** > **Messaging** > **WhatsApp Sandbox Settings**, set:
  - **"When a message comes in"**: `https://<your-ngrok-subdomain>.ngrok-free.app/api/v1/whatsapp/webhook` (HTTP POST)

---

## 📱 Test Profiles & Demo Numbers

You can test all 5 personas using these simulated accounts configured in `database.py`:

| Role | Test Phone | Name / Location | Key WhatsApp Commands |
| :--- | :--- | :--- | :--- |
| **Farmer** | `+919876500001` | Shivanna Gowda (Mandya) | `ನಮಸ್ಕಾರ`, `1` (Mandi rate), or send a Kannada voice note |
| **Aggregator** | `+919876500002` | Lakshmi Devi (Maddur SHG) | `menu`, `1` (Manifest), `2` (Grade batch), `3` (Truck) |
| **Customer** | `+919876500003` | Priya Verma (Bengaluru) | `menu`, `1` (Catalog), `2` (Track order), `4` (Provenance) |
| **Institution** | `+919876500004` | Warden Raghavan (Hostel) | `menu`, `1` (Standing orders), `3` (GST Invoice) |
| **Delivery** | `+919876500005` | Manjunath K (Electric 3W) | `menu`, `1` (Route map), `4829` (Submit customer OTP) |

*Any new/unrecognized phone number is greeted with an automatic multi-language role onboarding menu.*
