# Tests_sprint2.py
# Lightweight assertions to verify Sprint 2 behavior for UC02.
# Run with: python Tests_sprint2.py

from datetime import date, timedelta
from DataStorage import DataStorage
from User import User
from HealthTracker import HealthTracker
from TrendService import TrendService

def run_tests() -> None:
    # Arrange: initialize a fresh in-memory store
    db = DataStorage()
    db.add_user("test@example.com", "password123")
    user = User(db)
    tracker = HealthTracker(db)
    trend = TrendService(db)
    user.login_cli("test@example.com", "password123")
    today = date.today()

    # ---------- TC05 ----------
    # Exactly 7 entries from D-6..D should yield a full trend (no None).
    db.users["test@example.com"]["moods"] = []
    for i, val in enumerate([1, 2, 3, 4, 5, 4, 3]):
        tracker.log_mood("test@example.com", val, when=today - timedelta(days=6 - i))
    t, msg = trend.weekly_trend("test@example.com", today)
    assert len(t) == 7, "TC05: trend must have length 7"
    assert all(v is not None for v in t), "TC05: all entries should be present"
    assert msg == "Showing last 7 days.", "TC05: message mismatch"

    # ---------- TC06 ----------
    # Only some days populated should produce Nones and 'Partial' message.
    db.users["test@example.com"]["moods"] = []
    for offset, val in [(6, 3), (2, 4), (0, 5)]:
        tracker.log_mood("test@example.com", val, when=today - timedelta(days=offset))
    t, msg = trend.weekly_trend("test@example.com", today)
    assert len(t) == 7, "TC06: trend must have length 7"
    none_count = sum(1 for v in t if v is None)
    assert none_count == 4, f"TC06: expected 4 None entries, got {none_count}"
    assert "Partial" in msg, "TC06: expected a partial trend message"

    # ---------- TC07 ----------
    # D-7 entries are out of range and must be ignored.
    db.users["test@example.com"]["moods"] = []
    tracker.log_mood("test@example.com", 1, when=today - timedelta(days=7))  # should be ignored
    tracker.log_mood("test@example.com", 2, when=today - timedelta(days=6))
    tracker.log_mood("test@example.com", 3, when=today - timedelta(days=1))
    t, msg = trend.weekly_trend("test@example.com", today)
    # Index 0 corresponds to D-6, index 5 to D-1 (D-6..D is 0..6)
    assert t[0] == 2, f"TC07: expected D-6 value 2, got {t[0]}"
    assert t[5] == 3, f"TC07: expected D-1 value 3, got {t[5]}"

    # ---------- TC08 ----------
    # No data should produce all Nones and a "No data" message.
    db.users["test@example.com"]["moods"] = []
    t, msg = trend.weekly_trend("test@example.com", today)
    assert all(v is None for v in t), "TC08: all entries should be None"
    assert "No data" in msg, "TC08: expected 'No data' message"

    print("All Sprint 2 tests passed.")

if __name__ == "__main__":
    run_tests()
