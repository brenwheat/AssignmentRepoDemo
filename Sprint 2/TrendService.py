# TrendService.py
# Business logic for computing a 7-day mood trend vector.

from datetime import date, timedelta
from typing import List, Optional, Tuple

class TrendService:
    """Compute a 7-day trend vector (values or None) and a user-facing message."""

    def __init__(self, storage) -> None:
        # storage must provide get_moods_in_last_n_days(email, n_days, today)
        self.storage = storage

    def weekly_trend(self, email: str, today: Optional[date] = None) -> Tuple[List[Optional[int]], str]:
        """
        Return a tuple (trend, message) where:
          - trend is a list of length 7, aligned to D-6..D
          - each element is an int mood value or None if not logged that day
        """
        today = today or date.today()

        # Construct the 7 calendar days: D-6, D-5, ..., D-1, D
        days = [today - timedelta(days=i) for i in range(6, -1, -1)]

        # Map of day -> value for the last 7 days from storage
        entries = dict(self.storage.get_moods_in_last_n_days(email, 7, today))

        # Build the aligned vector where missing entries become None
        trend: List[Optional[int]] = [entries.get(d) for d in days]

        # Determine a simple UX message
        if all(v is None for v in trend):
            message = "No data for the last 7 days."
        elif any(v is None for v in trend):
            message = "Partial trend – log more days to complete your weekly trend."
        else:
            message = "Showing last 7 days."

        return trend, message
