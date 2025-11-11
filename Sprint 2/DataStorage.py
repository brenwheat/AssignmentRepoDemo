# DataStorage.py
# Simple in-memory persistence for users, credentials, streaks, and mood logs.
# Designed for a small class project (no external DB). Dates are stored as
# datetime.date objects with integer mood values in [1..5].

from datetime import date
from typing import Dict, List, Tuple, Optional

class DataStorage:
    """
    In-memory store for users and mood logs with simple date tagging.

    users[email] = {
        "password": str,
        "streak": int,
        "moods": List[Tuple[date, int]]  # (day, moodValue)
    }
    """

    def __init__(self) -> None:
        # Using a dict makes it easy to mock persistence for tests.
        self.users: Dict[str, Dict[str, object]] = {}

    def add_user(self, email: str, password: str) -> None:
        """Create a new user with an empty mood history and 0-day streak."""
        self.users[email] = {"password": password, "streak": 0, "moods": []}

    def validate_login(self, email: str, password: str) -> bool:
        """Return True if credentials match an existing user."""
        user = self.users.get(email)
        return bool(user and user["password"] == password)

    def save_mood(self, email: str, mood_value: int, when: Optional[date] = None) -> Tuple[bool, str]:
        """
        Append a (date, mood) tuple for a user.
        Valid mood_value ∈ [1..5]. Returns (ok, message) for friendly CLI output.
        """
        if email not in self.users:
            return False, "Error: User not found"
        if not isinstance(mood_value, int) or not (1 <= mood_value <= 5):
            return False, "Error: Invalid mood value. Must be between 1 and 5."

        when = when or date.today()
        # Store as (date, int). If multiple entries occur on the same day,
        # TrendService will keep the last one for that day.
        moods: List[Tuple[date, int]] = self.users[email]["moods"]  # type: ignore
        moods.append((when, mood_value))
        return True, "Mood saved"

    def get_moods_in_last_n_days(
        self, email: str, n_days: int = 7, today: Optional[date] = None
    ) -> List[Tuple[date, int]]:
        """
        Return a list of (day, value) for entries in the inclusive window:
        [today-(n_days-1) .. today]. If user not found, return empty list.
        """
        if email not in self.users:
            return []

        today = today or date.today()
        start_ordinal = today.toordinal() - (n_days - 1)

        moods: List[Tuple[date, int]] = self.users[email]["moods"]  # type: ignore
        window: List[Tuple[date, int]] = []
        for d, v in moods:
            # Include if the day is between start and today (inclusive).
            if start_ordinal <= d.toordinal() <= today.toordinal():
                window.appen
