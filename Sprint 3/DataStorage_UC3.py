# DataStorage_UC3.py
# In-memory storage just for UC3.
# Tracks: user credentials, tips opt-out flag, and mood logs (date, mood 1..5).
# This is intentionally simple to keep focus on the use case behavior.

from datetime import date
from typing import Dict, List, Tuple, Optional

class DataStorage_UC3:
    """
    Internal shape:
    users[email] = {
        "password": str,
        "tips_opt_out": bool,
        "moods": List[Tuple[date, int]]  # (day, mood 1..5)
    }
    """

    def __init__(self) -> None:
        # Email -> user record
        self.users: Dict[str, Dict[str, object]] = {}

    def add_user(self, email: str, password: str, tips_opt_out: bool = False) -> None:
        """Create a new user with default empty mood history."""
        self.users[email] = {
            "password": password,
            "tips_opt_out": tips_opt_out,
            "moods": []
        }

    def validate_login(self, email: str, password: str) -> bool:
        """Return True if credentials match an existing user."""
        u = self.users.get(email)
        return bool(u and u["password"] == password)

    def set_tips_opt_out(self, email: str, value: bool) -> None:
        """Enable/disable receiving tips for the user."""
        if email in self.users:
            self.users[email]["tips_opt_out"] = value

    def get_tips_opt_out(self, email: str) -> bool:
        """Return True if the user has opted out of tips."""
        return bool(self.users[email]["tips_opt_out"])

    def save_mood(self, email: str, mood_value: int, when: Optional[date] = None):
        """
        Store a new mood entry for a given day.
        Valid mood range is 1..5. Returns (ok, message) for simple CLI output.
        """
        if email not in self.users:
            return False, "Error: User not found"
        if not isinstance(mood_value, int) or not (1 <= mood_value <= 5):
            return False, "Error: Invalid mood value. Must be between 1 and 5."

        when = when or date.today()
        moods: List[Tuple[date, int]] = self.users[email]["moods"]  # type: ignore
        moods.append((when, mood_value))
        return True, "Mood saved"

    def get_last_mood(self, email: str) -> Optional[int]:
        """Return the last mood value logged by the user (or None if empty)."""
        moods: List[Tuple[date, int]] = self.users[email]["moods"]  # type: ignore
        if not moods:
            return None
        return moods[-1][1]
