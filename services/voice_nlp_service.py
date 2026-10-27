"""
AgriLink WhatsApp Integration - Voice & NLP Intelligence Service (Module M9 & M14)
Processes regional voice notes (Kannada, Hindi, English) and extracts crop harvest entities.
"""

import re
from typing import Dict, Any, Optional

# Indic Dictionary Mapping for Entity Extraction
CROP_SYNONYMS = {
    # Kannada
    "ಟೊಮೆಟೊ": "Tomato",
    "ಹುಳಿ ಟೊಮೆಟೊ": "Tomato",
    "ಈರುಳ್ಳಿ": "Onion",
    "ಪಾಲಕ್": "Palak",
    "ಶುಂಠಿ": "Ginger",
    "ಹಸಿ ಮೆಣಸಿನಕಾಯಿ": "Green Chilli",
    "ಮೆಣಸಿನಕಾಯಿ": "Green Chilli",
    "ಆಲೂಗಡ್ಡೆ": "Potato",
    "ಎಲೆಕೋಸು": "Cabbage",
    # Hindi
    "टमाटर": "Tomato",
    "प्याज": "Onion",
    "पालक": "Palak",
    "अदरक": "Ginger",
    "मिर्च": "Green Chilli",
    "हरी मिर्च": "Green Chilli",
    "आलू": "Potato",
    # English
    "tomato": "Tomato",
    "tomatoes": "Tomato",
    "onion": "Onion",
    "onions": "Onion",
    "palak": "Palak",
    "spinach": "Palak",
    "ginger": "Ginger",
    "chilli": "Green Chilli",
    "chillies": "Green Chilli",
    "green chilli": "Green Chilli",
    "potato": "Potato",
    "potatoes": "Potato",
    "cabbage": "Cabbage"
}

DAYS_SYNONYMS = {
    "ನಾಳೆ": "Tomorrow morning",
    "ಇಂದು": "Today afternoon",
    "ಗುರುವಾರ": "Thursday",
    "ಶುಕ್ರವಾರ": "Friday",
    "ಶನಿವಾರ": "Saturday",
    "ಸೋಮವಾರ": "Monday",
    "ಬುಧವಾರ": "Wednesday",
    "कल": "Tomorrow",
    "आज": "Today",
    "गुरुवार": "Thursday",
    "शुक्रवार": "Friday",
    "tomorrow": "Tomorrow morning",
    "today": "Today afternoon",
    "thursday": "Thursday",
    "friday": "Friday",
    "saturday": "Saturday"
}


class VoiceNLPService:
    @staticmethod
    def parse_harvest_intent(transcript: str) -> Dict[str, Any]:
        """
        Parses spoken or typed text into structured crop harvest declaration:
        e.g., 'ನನ್ನ ಬಳಿ 200 ಕೆಜಿ ಟೊಮೆಟೊ ಇದೆ ಗುರುವಾರ ಕೊಯ್ಲು' ->
        {'crop': 'Tomato', 'qty_kg': 200.0, 'harvest_day': 'Thursday', 'confidence': 0.95}
        """
        text_lower = transcript.lower().strip()
        detected_crop = None
        detected_qty = None
        detected_day = "Tomorrow morning"

        # 1. Match Crop
        for syn, canonical in CROP_SYNONYMS.items():
            if syn in text_lower or syn in transcript:
                detected_crop = canonical
                break

        # 2. Match Quantity (Numbers followed by kg / quintal / ಕೆಜಿ)
        # Check quintals (1 quintal = 100 kg)
        quintal_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:quintal|ಕ್ವಿಂಟಾಲ್|क्विंटल)", text_lower)
        if quintal_match:
            detected_qty = float(quintal_match.group(1)) * 100.0
        else:
            kg_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:kg|kgs|ಕೆಜಿ|किलो|kilo)", text_lower)
            if kg_match:
                detected_qty = float(kg_match.group(1))
            else:
                # Standalone digits if mentioned
                num_match = re.search(r"\b(\d{2,4})\b", text_lower)
                if num_match:
                    detected_qty = float(num_match.group(1))

        # 3. Match Harvest Day / Schedule
        for syn, canonical in DAYS_SYNONYMS.items():
            if syn in text_lower or syn in transcript:
                detected_day = canonical
                break

        is_complete = bool(detected_crop and detected_qty)
        return {
            "success": is_complete,
            "crop": detected_crop,
            "qty_kg": detected_qty,
            "harvest_day": detected_day,
            "raw_text": transcript
        }

    @staticmethod
    async def transcribe_audio_mock(audio_bytes_or_url: str, lang_hint: str = "kn") -> str:
        """
        Production hook for OpenAI Whisper or Google Bhashini API.
        For sandbox/offline simulation, provides high-fidelity speech transcripts.
        """
        return "ನನ್ನ ಬಳಿ 200 ಕೆಜಿ ಟೊಮೆಟೊ ಇದೆ, ಗುರುವಾರ ಕೊಯ್ಲು ಮಾಡುತ್ತೇನೆ"
