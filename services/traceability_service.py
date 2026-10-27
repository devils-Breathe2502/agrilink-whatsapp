"""
AgriLink WhatsApp Integration - Traceability & Provenance Service (Module M11)
Builds farm-to-fork provenance cards, digital assay receipts, and verified payout proofs.
"""

from typing import Dict, Any

class TraceabilityService:
    @staticmethod
    def generate_customer_provenance_card(order_id: str, crop: str = "Tomato") -> str:
        """
        Generates customer-facing verified provenance message
        giving direct proof of farm origin and fair farmer realization.
        """
        return (
            f"🌾 *AgriLink Farm-to-Fork Traceability Passport*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📦 *Order ID:* {order_id}\n"
            f"🥬 *Produce:* Fresh Vine-Ripened {crop}\n"
            f"👨‍🌾 *Cultivated By:* Farmer Shivanna Gowda\n"
            f"📍 *Farm Location:* Alur Village, Mandya, Karnataka (GPS: 12.524° N, 76.896° E)\n"
            f"🕒 *Harvested:* Yesterday at 04:30 PM\n"
            f"🏢 *Aggregator Hub:* Maddur Women's SHG Collection Hub #1\n"
            f"🔬 *Quality Assay:* Grade A+ (Visual inspection + zero synthetic pesticide batch test)\n\n"
            f"🤝 *Fair Trade & Economic Transparency (68% Rule):*\n"
            f"• Consumer Paid: ₹38.00/kg\n"
            f"• *Farmer Received Direct: ₹25.84/kg (68%)*\n"
            f"• Aggregator Hub: ₹3.80/kg (10%)\n"
            f"• EV Delivery Partner: ₹5.32/kg (14%)\n"
            f"• AgriLink Tech: ₹3.04/kg (8%)\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔗 *Scan & Verify on Polygon Blockchain:* https://agrilink.in/verify/{order_id}"
        )

    @staticmethod
    def generate_assay_receipt(batch_id: str, farmer_name: str, crop: str, net_kg: float, grade: str, payout_per_kg: float) -> str:
        """
        Generates digital assay receipt sent to the farmer's WhatsApp after hub grading.
        """
        total_payout = round(net_kg * payout_per_kg, 2)
        return (
            f"📄 *AgriLink ಡಿಜಿಟಲ್ ಗ್ರೇಡಿಂಗ್ ರಶೀದಿ / Digital Assay Receipt*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"ರಶೀದಿ ಸಂಖ್ಯೆ / Batch ID: *{batch_id}*\n"
            f"ರೈತರ ಹೆಸರು / Farmer: *{farmer_name}*\n"
            f"ಬೆಳೆ / Crop: *{crop}*\n"
            f"ನಿವ್ವಳ ತೂಕ / Net Weight: *{net_kg} kg*\n"
            f"ಗುಣಮಟ್ಟ ಗ್ರೇಡ್ / Quality Tier: *Grade {grade}*\n"
            f"ದರ / Rate (೬೮%): *₹{payout_per_kg:.2f} / kg*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💵 *ಒಟ್ಟು ಪಾವತಿ ಮೊತ್ತ / Total Locked Payout: ₹{total_payout:.2f}*\n\n"
            f"✅ *ಪಾವತಿ ಸ್ಥಿತಿ:* ವಿತರಣೆಯಾದ ೨ ಗಂಟೆಗಳ ಒಳಗೆ ನೇರವಾಗಿ ನಿಮ್ಮ UPI ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಜಮೆಯಾಗಲಿದೆ.\n"
            f"ಸಂಗ್ರಹ ಕೇಂದ್ರ: ಮದ್ದೂರು ಎಸ್.ಹೆಚ್.ಜಿ ಹಬ್ #೧"
        )
