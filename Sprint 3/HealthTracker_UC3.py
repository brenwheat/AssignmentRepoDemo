# HealthTracker_UC3.py
# UC3 behavior only: log mood and include a tip for low moods (1–2),
# unless the user opted out of tips.

from datetime import date
from typing import Optional

class HealthTracker_UC3:
    def __init__(self, storage, tips_service) -> None:
        self.storage = storage           # DataStorage_UC3
        self.tips = tips_service         # TipsService

    def log_mood(self, email: str, mood_value: int, when: Optional[date] = None) -> str:
        """
        Save the mood and, if the mood is low (<=2), attach a tip unless opted out.
        Returns a short, readable message for CLI output.
        """
        ok, msg = self.storage.save_mood(email, mood_value, when or date.today())
        if not ok:
            return msg

        # Only low moods get tips
        if mood_value <= 2:
            if self.storage.get_tips_opt_out(email):
                return "Mood logged. Tips are turned off."
            return f"Mood logged. Tip: {self.tips.recommend(mood_value)}"

        # Normal mood (>=3): no tip
        return "Mood logged."
