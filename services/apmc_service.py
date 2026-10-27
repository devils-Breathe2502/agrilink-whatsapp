"""
AgriLink WhatsApp Integration - APMC Mandi Pricing Engine (Module M8)
Calculates real-time indicative reference quotes and 68-10-14-8 payout splits.
"""

from typing import Dict, Any, Optional

APMC_MARKET_BENCHMARKS = {
    "tomato": {
        "commodity": "Tomato (Hybrid)",
        "primary_mandi": "Mandya APMC",
        "benchmark_price": 25.00,  # ₹25/kg base rate
        "grade_multipliers": {"A": 1.15, "B": 1.00, "C": 0.90},
        "transport_est": 3.00,
        "source": "Agmarknet DMI Govt of India"
    },
    "onion": {
        "commodity": "Onion (Nashik Red)",
        "primary_mandi": "Yeshwanthpur APMC (Bengaluru)",
        "benchmark_price": 32.00,
        "grade_multipliers": {"A": 1.10, "B": 1.00, "C": 0.88},
        "transport_est": 2.50,
        "source": "Agmarknet DMI Govt of India"
    },
    "palak": {
        "commodity": "Palak (Spinach Greens)",
        "primary_mandi": "Ramanagara APMC",
        "benchmark_price": 20.00,
        "grade_multipliers": {"A": 1.20, "B": 1.00, "C": 0.85},
        "transport_est": 2.00,
        "source": "Agmarknet DMI Govt of India"
    },
    "ginger": {
        "commodity": "Ginger (Green)",
        "primary_mandi": "Hassan APMC",
        "benchmark_price": 70.00,
        "grade_multipliers": {"A": 1.15, "B": 1.00, "C": 0.90},
        "transport_est": 4.00,
        "source": "Agmarknet DMI Govt of India"
    },
    "green chilli": {
        "commodity": "Green Chilli",
        "primary_mandi": "Kolar APMC",
        "benchmark_price": 35.00,
        "grade_multipliers": {"A": 1.15, "B": 1.00, "C": 0.90},
        "transport_est": 3.00,
        "source": "Agmarknet DMI Govt of India"
    }
}


class APMCPricingEngine:
    @staticmethod
    def get_quote(crop_name: str, grade: str = "A", is_organic: bool = False) -> Optional[Dict[str, Any]]:
        key = crop_name.strip().lower()
        if key not in APMC_MARKET_BENCHMARKS:
            return None

        mandi_data = APMC_MARKET_BENCHMARKS[key]
        base_rate = mandi_data["benchmark_price"]
        multiplier = mandi_data["grade_multipliers"].get(grade.upper(), 1.00)
        
        # Organic certification adds 20% premium
        organic_multiplier = 1.20 if is_organic else 1.00
        
        consumer_price = round(base_rate * multiplier * organic_multiplier + mandi_data["transport_est"], 2)

        # AgriLink 68-10-14-8 Split
        farmer_payout = round(consumer_price * 0.68, 2)
        aggregator_payout = round(consumer_price * 0.10, 2)
        delivery_payout = round(consumer_price * 0.14, 2)
        platform_fee = round(consumer_price * 0.08, 2)

        return {
            "commodity": mandi_data["commodity"],
            "mandi": mandi_data["primary_mandi"],
            "base_benchmark": base_rate,
            "quality_grade": f"Grade {grade.upper()}",
            "is_organic": is_organic,
            "consumer_retail_price": consumer_price,
            "split": {
                "farmer_68": farmer_payout,
                "aggregator_10": aggregator_payout,
                "delivery_14": delivery_payout,
                "platform_8": platform_fee
            },
            "source": mandi_data["source"]
        }

    @staticmethod
    def format_farmer_quote_message(quote: Dict[str, Any], lang: str = "en") -> str:
        s = quote["split"]
        if lang == "kn":
            return (
                f"📊 *ಇಂದಿನ ಮಂಡಿ ಬೆಲೆ ({quote['commodity']})*\n"
                f"• ಮಾರುಕಟ್ಟೆ: *{quote['mandi']}*\n"
                f"• ಸರ್ಕಾರಿ ಉಲ್ಲೇಖ ಬೆಲೆ: *₹{quote['base_benchmark']:.2f}/kg*\n"
                f"• ಗುಣಮಟ್ಟ: *{quote['quality_grade']}*\n\n"
                f"💰 *ರೈತರ ನೇರ ಪಾವತಿ (೬೮% ಹಂಚಿಕೆ):*\n"
                f"👉 *₹{s['farmer_68']:.2f} ಪ್ರತಿ ಕೆಜಿಗೆ*\n"
                f"_(ಮಧ್ಯವರ್ತಿಗಳಿಲ್ಲದೆ ನೇರವಾಗಿ ನಿಮ್ಮ UPI ಗೆ ಬರುತ್ತದೆ)_\n\n"
                f"ಉಳಿದ ಹಂಚಿಕೆ: ಸಂಗ್ರಾಹಕ ಹಬ್ ₹{s['aggregator_10']:.2f} | ಡೆಲಿವರಿ ₹{s['delivery_14']:.2f} | ತಂತ್ರಜ್ಞಾನ ₹{s['platform_8']:.2f}\n"
                f"ಮೂಲ: {quote['source']}"
            )
        return (
            f"📊 *Today's Mandi Benchmark ({quote['commodity']})*\n"
            f"• Mandi Yard: *{quote['mandi']}*\n"
            f"• APMC Benchmark: *₹{quote['base_benchmark']:.2f}/kg*\n"
            f"• Quality Tier: *{quote['quality_grade']}*\n\n"
            f"💰 *Proposed Farmer Net Realization (68% Split):*\n"
            f"👉 *₹{s['farmer_68']:.2f} / kg*\n"
            f"_(Credited directly to your bank account via UPI upon delivery)_\n\n"
            f"4-Way Breakdown: Aggregator ₹{s['aggregator_10']:.2f} | Delivery ₹{s['delivery_14']:.2f} | Platform ₹{s['platform_8']:.2f}\n"
            f"Source: {quote['source']}"
        )
