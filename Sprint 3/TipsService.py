# TipsService.py
# Provides short, supportive tips when a low mood (1 or 2) is logged.
# Has a simple "available" flag so we can simulate an outage and test fallback.

from typing import Optional
import random

# Generic fallback when tips are unavailable or no specific list exists
GENERIC_MESSAGE = "Remember, you’re not alone. Try a relaxing activity today."

class TipsService:
    def __init__(self) -> None:
        # A tiny in-memory "tips database"
        self.tips_by_level = {
            1: [
                "Try a short walk and breathe deeply.",
                "Text a friend and share one small win.",
                "Play a favorite song and stretch for 3 minutes."
            ],
            2: [
                "Drink water and take a 5-minute screen break.",
                "Write down three things you’re grateful for.",
                "Do 2 minutes of box-breathing (4-4-4-4)."
            ]
        }
        # If set to False, we return the generic message
        self.available = True

    def recommend(self, mood_value: int) -> str:
        """Pick a tip based on mood value. If unavailable, return generic message."""
        if not self.available:
            return GENERIC_MESSAGE
        options = self.tips_by_level.get(mood_value) or []
        if not options:
            return GENERIC_MESSAGE
        return random.choice(options)
