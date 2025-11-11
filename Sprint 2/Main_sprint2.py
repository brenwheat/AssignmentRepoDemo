# Main_sprint2.py
# Console demo for Sprint 2 (UC02: View Weekly Mood Trend).
# Runs four scenarios (TC05–TC08) and prints “Expected vs Actual”-style output.

from datetime import date, timedelta
from DataStorage import DataStorage
from User import User
from HealthTracker import HealthTracker
from TrendService import TrendService

LINE = "=" * 70

def show_case(tid: str, desc: str, expected_note: str, actual_obj) -> None:
    """Helper to format test case prints in the CLI demo."""
    print(f"\n{LINE}\n{tid}: {desc}\n{LINE}")
    print("Expected:", expected_note)
    print("Actual:  ", actual_obj)
    print("-" * 70)

if __name__ == "__main__":
    # Initialize components
    db = DataStorage()
    db.add_user("test@example.com", "password123")
    user = User(db)
    tracker = HealthTracker(db)
    trend = TrendService(db)

    # Basic login to simulate authenticated usage
    assert user.login_cli("test@example.com", "password123") == "Login successful"
    today = date.today()

    # -----------------------------
    # TC05: exactly 7 entries D-6..D
    # Expect: full trend with 7 values and message "Showing last 7 days."
    # -----------------------------
    for i, val in enumerate([1, 2, 3, 4, 5, 4, 3]):
        # When offsets build day sequence D-6..D
        tracker.log_mood("test@example.com", val, when=today - timedelta(days=6 - i))
    t, msg = trend.weekly_trend("test@example.com", today)
    show_case("TC05", "Typical Weekly Trend", "7 values, 'Showing last 7 days.'", (t, msg))

    # Reset mood data and streak for next cases (keeps the same user)
    db.users["test@example.com"]["moods"] = []
    db.users["test@example.com"]["streak"] = 0

    # -----------------------------
    # TC06: only 3 days populated
    # Expect: 7-length trend with 4 None entries and a 'Partial trend' message.
    # -----------------------------
    for offset, val in [(6, 3), (2, 4), (0, 5)]:
        tracker.log_mood("test@example.com", val, when=today - timedelta(days=offset))
    t, msg = trend.weekly_trend("test@example.com", today)
    show_case("TC06", "Partial Data", "4 None slots, 'Partial trend ...'", (t, msg))

    # -----------------------------
    # TC07: D-7 entry should be ignored (out of range)
    # Expect: trend uses entries only from D-6..D, not D-7 or older.
    # -----------------------------
    db.users["test@example.com"]["moods"] = []
    tracker.log_mood("test@example.com", 1, when=today - timedelta(days=7))  # out-of-range
    tracker.log_mood("test@example.com", 2, when=today - timedelta(days=6))  # in-range
    tracker.log_mood("test@example.com", 3, when=today - timedelta(days=1))  # in-range
    t, msg = trend.weekly_trend("test@example.com", today)
    show_case("TC07", "Ignore Out-of-Range (D-7)", "Only D-6..D included", (t, msg))

    # -----------------------------
    # TC08: no data at all
    # Expect: 7 Nones and "No data for the last 7 days."
    # -----------------------------
    db.users["test@example.com"]["moods"] = []
    t, msg = trend.weekly_trend("test@example.com", today)
    show_case("TC08", "Empty Dataset", "All None, 'No data ...'", (t, msg))
