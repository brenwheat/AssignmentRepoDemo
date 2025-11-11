# HealthTracker.py
# Facade for actions like logging moods and maintaining streaks.
# Keeps presentation (CLI or GUI) separate from data storage concerns.

from datetime import date
from typing import Optional

class HealthTracker:
    def __init__(self, storage) -> None:
        # storage must provide save_mood(email, mood_value, when) and update_streak(email)
        self.storage = storage

    def log_mood(self, email: str, mood_value: int, when: Optional[date] = None) -> str:
        """
        Log a mood value for a user. Returns a human-readable message.
        This method delegates to storage and simulates a streak update.
        """
        ok, msg = self.storage.save_mood(email, mood_value, when or date.today())
        if not ok:
            # Propagate validation or user-not-found errors
            return msg

        # For this project, streak increments every time a mood is logged.
        # Real apps would check for consecutive days.
        streak_update = self.storage.update_streak(email)
        if isinstance(streak_update, str) and "Error" in streak_update:
            # Pass through error strings if any
            return streak_update

        return f"Mood logged successfully, you are on a {streak_update}-day streak"
