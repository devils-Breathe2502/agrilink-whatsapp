# 🌾 AgriLink — Official Meta WhatsApp Cloud API Service
**Farm-to-Consumer Digital Marketplace (Seva First Innovation Challenge 2026)**

Direct, official integration with **Meta (Facebook) WhatsApp Business Cloud API**.
* **Zero Middlemen:** No Twilio, no extra fees.
* **1,000 Free Monthly Conversations** included directly by Meta.
* **Full Multi-Actor Support:** Farmer (Mandi pricing, 68% split, Voice notes), Aggregator (Hub manifests), Customer (Catalog, Tracking, OTP, Provenance), Institution (Standing orders), and Delivery Fleet.

---

## 🚀 How to Connect Real WhatsApp via Meta (3 Simple Steps)

### Step 1: Push Code to GitHub
```bash
cd "C:\Users\himch\Documents\Downloads\SAD Project\agrilink_whatsapp"
git add .
git commit -m "Migrate to official Meta WhatsApp Cloud API"
git push
```
Render automatically rebuilds and makes your webhook live at:  
👉 `https://agrilink-whatsapp.onrender.com/webhook`

### Step 2: Create a Free Meta Developer App
1. Go to **[developers.facebook.com](https://developers.facebook.com)** and sign in with your Facebook account.
2. Click **My Apps** ➔ **Create App**.
3. Select **Other** ➔ Type: **Business**.
4. App Name: `AgriLink Assistant` ➔ Click **Create App**.
5. On the Products Dashboard, find **WhatsApp** and click **Set up**.

### Step 3: Configure Webhook on Meta
1. On the left menu under WhatsApp, click **Configuration**.
2. Under **Webhook**, click **Edit**:
   * **Callback URL:** `https://agrilink-whatsapp.onrender.com/webhook`
   * **Verify Token:** `agrilink_sfic_2026_secret`
3. Click **Verify and Save**.
4. Click **Manage Webhook Fields** and check **`messages`** ➔ Click **Save**.

### Step 4: Add Environment Variables in Render
In your **Render Dashboard** (Settings ➔ Environment Variables):
* `WHATSAPP_CLOUD_API_TOKEN` = *(Your Access Token from Meta)*
* `WHATSAPP_PHONE_NUMBER_ID` = *(Your Phone Number ID from Meta)*
* `WHATSAPP_VERIFY_TOKEN` = `agrilink_sfic_2026_secret`

---

## 💬 Live In-Browser Simulator & QR Scanner
Your web simulator and QR code generator are live 24/7 at:
👉 **https://agrilink-whatsapp.onrender.com**
